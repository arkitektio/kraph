from types import TracebackType
from pydantic import Field
from kraph.links.upload import UploadLink
from rath import rath

from rath.links.auth import AuthTokenLink

from rath.links.compose import TypedComposedLink
from rath.links.dictinglink import DictingLink
from rath.links.shrink import ShrinkingLink
from rath.links.split import SplitLink


class KraphLinkComposition(TypedComposedLink):
    shrinking: ShrinkingLink = Field(default_factory=ShrinkingLink)
    dicting: DictingLink = Field(default_factory=DictingLink)
    upload: UploadLink
    auth: AuthTokenLink
    split: SplitLink


class KraphRath(rath.Rath):
    """Kraph Rath

    Args:
        rath (_type_): _description_
    """

    async def __aenter__(self):
        """Enter the client.

        Entering does not make it "the current client", and kraph never looks one up: calls go
        through the :class:`kraph.kraph.Kraph` client that owns this rath.
        """
        await super().__aenter__()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await super().__aexit__(exc_type, exc_val, exc_tb)
