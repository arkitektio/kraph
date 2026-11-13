"""The S3 store an upload or download goes through, built from a kraph datalayer grant.

The same shape as every service's client (mikro, elektro): obstore, rustls, and during an
upload credentials that renew themselves against the same key (:data:`upload_refresher`).
"""

import datetime
import threading
from collections.abc import Callable
from contextvars import ContextVar
from typing import TYPE_CHECKING, Protocol

from obstore.store import S3Store

if TYPE_CHECKING:
    from obstore.store import ClientConfig, RetryConfig, S3Credential


class S3UploadGrantLike(Protocol):
    """Protocol for grants that carry S3 credentials and object coordinates."""

    @property
    def access_key(self) -> str: ...  # noqa: D102

    @property
    def secret_key(self) -> str: ...  # noqa: D102

    @property
    def session_token(self) -> str: ...  # noqa: D102

    @property
    def bucket(self) -> str: ...  # noqa: D102

    @property
    def key(self) -> str: ...  # noqa: D102


#: How to get fresh credentials for the store an upload is writing, set by the upload
#: middleware around exactly one write (:meth:`kraph.middleware.upload.UploadMiddleware`).
#: Called with the store id; returns a new grant for the *same* key. A context variable rather
#: than a parameter because the store is built several calls down, in every writer the
#: middleware drives, and the refresher is the middleware's to know about.
upload_refresher: ContextVar["Callable[[str], S3UploadGrantLike] | None"] = ContextVar("upload_refresher", default=None)

#: How long before a grant runs out a fresh one is asked for. obstore asks its credential
#: provider again shortly before the expiry it reported; refreshing a little earlier than that
#: keeps a request in flight from crossing the boundary.
UPLOAD_REFRESH_MARGIN_SECONDS = 300


class RefreshingUploadCredentials:
    """An obstore credential provider for one upload: its grant, renewed before it expires.

    A write that outlives its grant used to die partway through with a 403, and the only way
    out was a new store and a lost upload. obstore calls this whenever it needs credentials, so
    it hands back the grant it was made with until that is close to expiring and then asks the
    server for a fresh session against the same key -- the write carries on where it was.

    Thread-safe: obstore may ask from several of its workers at once, and two concurrent
    refreshes would mint two sessions for nothing.
    """

    def __init__(self, grant: "S3UploadGrantLike", refresh: "Callable[[], S3UploadGrantLike]") -> None:
        """Wrap the grant an upload started with, and how to renew it."""
        self._refresh = refresh
        self._lock = threading.Lock()
        self._install(grant)

    def _install(self, grant: "S3UploadGrantLike") -> None:
        self._grant = grant
        expires_in = getattr(grant, "expires_in", None)
        self._expires_at = datetime.datetime.now(datetime.UTC) + datetime.timedelta(seconds=expires_in) if expires_in else None

    def __call__(self) -> "S3Credential":
        """The credentials to sign the next request with."""
        with self._lock:
            if self._expires_at is not None:
                remaining = (self._expires_at - datetime.datetime.now(datetime.UTC)).total_seconds()
                if remaining < UPLOAD_REFRESH_MARGIN_SECONDS:
                    self._install(self._refresh())
            return {
                "access_key_id": self._grant.access_key,
                "secret_access_key": self._grant.secret_key,
                "token": self._grant.session_token or None,
                "expires_at": self._expires_at,
            }


def create_s3_store(
    endpoint_url: str,
    grant: "S3UploadGrantLike",
    client_options: "ClientConfig | None" = None,
    retry_config: "RetryConfig | None" = None,
    prefix: str | None = None,
    *,
    proxy: str | None = None,
) -> S3Store:
    """Create an obstore S3 client from an kraph grant and endpoint.

    ``prefix`` roots the store inside the bucket, so every key the caller passes is
    relative to it. Zarr needs this (see :func:`create_zarr_store_path`); the
    single-object paths address their key directly and leave it unset.

    ``proxy`` is the HTTP forward proxy the datalayer is only reachable through
    (see :attr:`DataLayer.proxy`). It is merged into the client options, never
    replacing them -- dropping ``allow_http`` would break every ``http://`` store.
    """
    normalized_client_options: dict[str, object] = dict(client_options or {})
    if endpoint_url.startswith("http://"):
        normalized_client_options.setdefault("allow_http", True)
    if proxy:
        normalized_client_options["proxy_url"] = proxy

    store_kwargs: dict[str, object] = {
        "endpoint": endpoint_url,
        "virtual_hosted_style_request": False,
        "client_options": normalized_client_options or None,
        "retry_config": retry_config,
    }
    refresh = upload_refresher.get()
    store_id = getattr(grant, "store", None)
    if refresh is not None and store_id:
        # Inside an upload: credentials that renew themselves against the same store.
        store_kwargs["credential_provider"] = RefreshingUploadCredentials(grant, lambda: refresh(store_id))
    else:
        store_kwargs["access_key_id"] = grant.access_key
        store_kwargs["secret_access_key"] = grant.secret_key
        if grant.session_token:
            store_kwargs["session_token"] = grant.session_token
    if prefix:
        store_kwargs["prefix"] = prefix

    return S3Store(
        grant.bucket,
        **store_kwargs,
    )
