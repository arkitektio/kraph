"""Which client a call on a kraph object goes through.

The one passed explicitly, else the one that fetched the object: every result
remembers its client (``Kraph._origin``), so a follow-up call from an object
reaches the same server, rath and datalayer that produced it. Nothing is looked up
in what happens to be current.
"""

from typing import TYPE_CHECKING, Any

from rath.origin import get_origin

from kraph.errors import NoKraphFound

if TYPE_CHECKING:
    from kraph.kraph import Kraph


def client_of(obj: Any, kraph: "Kraph | None" = None) -> "Kraph":  # noqa: ANN401
    """The client for a call on ``obj``: ``kraph`` if given, else the one that fetched it.

    Raises:
        NoKraphFound: If none was given and ``obj`` was not fetched through a
            client (built by hand, or unpickled: an origin does not travel).
    """
    if kraph is not None:
        return kraph

    from kraph.kraph import Kraph

    origin = get_origin(obj)
    client = origin.client if origin is not None else None
    if isinstance(client, Kraph):
        return client
    raise NoKraphFound(
        f"{type(obj).__name__} was not fetched through a Kraph client, so there is "
        "none to call through. Pass one explicitly (kraph=...)."
    )


__all__ = ["client_of"]
