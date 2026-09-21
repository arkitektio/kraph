"""Errors raised by the kraph client."""


class KraphError(Exception):
    """Base class for every error this client raises."""


class NoKraphFound(KraphError):
    """A call on an object needs a client, and none was passed nor fetched the object."""


class UnregisteredStructure(KraphError):
    """A Python object was used as a structure but names no registered identifier.

    Pass an explicit ``(identifier, object)`` pair instead, or register the class with the
    rekuest structure registry.
    """


class ProjectionTimeout(KraphError):
    """A view did not draw a claim within the time allowed.

    Carries the last projection read, so the caller can tell a view that is merely behind
    (``status=REBUILDING``, large ``lag``) from one that will never draw the claim because it
    declares no category for the word.
    """


class NotDrawn(KraphError):
    """A view does not draw this claim.

    Raised only by an explicit request for a view's account of a claim. An empty ``drawings``
    list on a write result is *not* an error and never raises.
    """
