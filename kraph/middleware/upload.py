"""Upload middleware: files in a request's variables go to kraph's datalayer first.

The same protocol every service's client runs (mikro, elektro): a ``BigFile`` found anywhere
in the serialized variables is uploaded -- a grant requested, the bytes written with
credentials that renew themselves, the upload finished -- and the finished store's id is sent
in its place. A write that fails is reported (``valid=False``), so the server ends the upload
and releases what it reserved, and the error propagates unchanged.

Grants are requested through the rath directly, never through the client, so the middleware
does not run on its own requests.
"""

import asyncio
import contextvars
import io
import logging
from collections.abc import Awaitable, Callable
from functools import partial
from typing import TYPE_CHECKING, Any

from pydantic import ConfigDict
from rath.turms.funcs import TOperation

from kraph.api.schema import (
    FinishBigFileUploadInput,
    FinishBigfileUploadMutation,
    RefreshBigfileUploadMutation,
    RefreshUploadInput,
    RequestBigFileUploadInput,
    RequestBigfileUploadMutation,
)
from kraph.datalayer import DataLayer
from kraph.io.obstore import upload_refresher
from kraph.io.upload import aupload_bigfile, upload_bigfile
from kraph.middleware.base import OperationMiddleware
from kraph.scalars import BigFile

if TYPE_CHECKING:
    from kraph.rath import KraphRath

logger = logging.getLogger(__name__)


async def _apply_async(func: Callable[[Any], Awaitable[Any]], obj: Any) -> Any:  # noqa: ANN401
    """Replace every ``BigFile`` in a nested structure with what ``func`` makes of it."""
    if isinstance(obj, dict):
        return {key: await _apply_async(func, value) for key, value in obj.items()}
    if isinstance(obj, list):
        return list(await asyncio.gather(*[_apply_async(func, value) for value in obj]))
    if isinstance(obj, tuple):
        return tuple(await asyncio.gather(*[_apply_async(func, value) for value in obj]))
    if isinstance(obj, BigFile):
        return await func(obj)
    return obj


def _apply_sync(func: Callable[[Any], Any], obj: Any) -> Any:  # noqa: ANN401
    """Replace every ``BigFile`` in a nested structure with what ``func`` makes of it."""
    if isinstance(obj, dict):
        return {key: _apply_sync(func, value) for key, value in obj.items()}
    if isinstance(obj, list):
        return [_apply_sync(func, value) for value in obj]
    if isinstance(obj, tuple):
        return tuple(_apply_sync(func, value) for value in obj)
    if isinstance(obj, BigFile):
        return func(obj)
    return obj


def _byte_size(value: Any) -> int:  # noqa: ANN401
    """How many bytes an upload will send: the size it declares, and is then held to.

    A file object is measured from where it stands to its end -- that is what gets read --
    and left where it was.
    """
    if isinstance(value, (bytes, bytearray, memoryview)):
        return len(value)
    position = value.tell()
    end = value.seek(0, io.SEEK_END)
    value.seek(position)
    return end - position


def _variables(mutation: Any, input: Any) -> dict[str, Any]:  # noqa: ANN401
    return mutation.Arguments(input=input).model_dump(by_alias=True, exclude_unset=True)


class UploadMiddleware(OperationMiddleware):
    """Uploads every ``BigFile`` in a request to kraph's datalayer and sends its store id instead."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    datalayer: DataLayer

    async def aenter(self) -> None:
        """Nothing to set up: every upload opens its own store."""

    async def aexit(self) -> None:
        """Nothing to tear down."""

    # --- one upload: request a grant, write under it, finish it ------------------------

    @staticmethod
    def _request(file: BigFile) -> dict[str, Any]:
        return _variables(RequestBigfileUploadMutation, RequestBigFileUploadInput(original_file_name=file.file_name, file_size=_byte_size(file.value)))

    @staticmethod
    def _finish(store_id: str, valid: bool) -> dict[str, Any]:
        return _variables(FinishBigfileUploadMutation, FinishBigFileUploadInput(store_id=store_id, valid=valid))

    def _refresher(self, rath: "KraphRath") -> Callable[[str], Any]:
        """How to renew the grant, callable from obstore's own worker threads.

        obstore asks for credentials from a thread of its runtime, which carries none of the
        caller's context -- and koil finds its loop through context. So the context is captured
        here and every refresh runs in a copy of it.
        """
        captured = contextvars.copy_context()

        def refresh(store_id: str) -> Any:  # noqa: ANN401
            variables = _variables(RefreshBigfileUploadMutation, RefreshUploadInput(store_id=store_id))
            result = captured.copy().run(rath.query, RefreshBigfileUploadMutation.Meta.document, variables)
            return RefreshBigfileUploadMutation(**result.data).refresh_bigfile_upload

        return refresh

    def _upload(self, rath: "KraphRath", file: BigFile) -> str:
        """Grant, write with self-renewing credentials, finish; or report the failure and re-raise."""
        grant = RequestBigfileUploadMutation(**rath.query(RequestBigfileUploadMutation.Meta.document, self._request(file)).data).request_bigfile_upload
        token = upload_refresher.set(self._refresher(rath))
        try:
            store_id = upload_bigfile(file, grant, self.datalayer)
        except BaseException:
            try:
                rath.query(FinishBigfileUploadMutation.Meta.document, self._finish(grant.store, valid=False))
            except Exception:  # noqa: BLE001 - the write's own error is the one to raise
                logger.warning("Could not report the failed upload of store %s; it is collected once its deadline passes.", grant.store, exc_info=True)
            raise
        finally:
            upload_refresher.reset(token)
        rath.query(FinishBigfileUploadMutation.Meta.document, self._finish(store_id, valid=True))
        return store_id

    async def _aupload(self, rath: "KraphRath", file: BigFile) -> str:
        """Grant, write with self-renewing credentials, finish; or report the failure and re-raise."""
        grant = RequestBigfileUploadMutation(**(await rath.aquery(RequestBigfileUploadMutation.Meta.document, self._request(file))).data).request_bigfile_upload
        token = upload_refresher.set(self._refresher(rath))
        try:
            store_id = await aupload_bigfile(file, grant, self.datalayer)
        except BaseException:
            try:
                await rath.aquery(FinishBigfileUploadMutation.Meta.document, self._finish(grant.store, valid=False))
            except Exception:  # noqa: BLE001 - the write's own error is the one to raise
                logger.warning("Could not report the failed upload of store %s; it is collected once its deadline passes.", grant.store, exc_info=True)
            raise
        finally:
            upload_refresher.reset(token)
        await rath.aquery(FinishBigfileUploadMutation.Meta.document, self._finish(store_id, valid=True))
        return store_id

    # --- the middleware ----------------------------------------------------------------

    def process_variables(self, variables: dict[str, Any], operation: type[TOperation], rath: "KraphRath") -> dict[str, Any]:
        """Upload every ``BigFile`` in ``variables`` and put its store id in its place."""
        return _apply_sync(partial(self._upload, rath), variables)

    async def aprocess_variables(self, variables: dict[str, Any], operation: type[TOperation], rath: "KraphRath") -> dict[str, Any]:
        """Upload every ``BigFile`` in ``variables`` and put its store id in its place."""
        return await _apply_async(partial(self._aupload, rath), variables)
