from types import TracebackType
from typing import TypeVar

from pydantic import Field
from rath import rath
from rath.links.auth import AuthTokenLink
from rath.links.compose import TypedComposedLink
from rath.links.dictinglink import DictingLink
from rath.links.shrink import ShrinkingLink
from rath.links.split import SplitLink

from kraph.links.upload import UploadLink
from kraph.middleware.base import OperationMiddleware


class KraphLinkComposition(TypedComposedLink):
    shrinking: ShrinkingLink = Field(default_factory=ShrinkingLink)
    dicting: DictingLink = Field(default_factory=DictingLink)
    upload: UploadLink
    auth: AuthTokenLink
    split: SplitLink


_KraphRath = TypeVar("_KraphRath", bound="KraphRath")


class KraphRath(rath.Rath):
    """Kraph Rath

    Attributes:
        middlewares: What a request's serialized variables go through before they are sent,
            in order: the upload middleware puts files in the datalayer and sends their store ids.
    """

    middlewares: list[OperationMiddleware] = Field(default_factory=list)

    async def __aenter__(self: _KraphRath) -> _KraphRath:
        """Enter the client and its middlewares.

        Entering does not make it "the current client", and kraph never looks one up: calls go
        through the :class:`kraph.kraph.Kraph` client that owns this rath.
        """
        await super().__aenter__()
        for middleware in self.middlewares:
            await middleware.aenter()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        for middleware in self.middlewares:
            await middleware.aexit()
        await super().__aexit__(exc_type, exc_val, exc_tb)
