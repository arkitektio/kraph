"""Upload link — currently a pass-through.

The old link implemented a presigned-POST flow: it walked operation variables for a
``RemoteUpload`` scalar, called ``requestUpload`` mid-parse, and POSTed the file with the
returned policy and signature.

None of that survives the evidence-log rewrite. The ``RemoteUpload`` scalar and the
``requestUpload`` mutation are both gone from the schema, replaced by three request/finish pairs
that hand back **STS credentials** rather than a signed form::

    requestMediaUpload(RequestMediaUploadInput!)     -> MediaUploadGrant
    finishMediaUpload(FinishMediaUploadInput!)       -> MediaStore
    requestBigFileUpload / finishBigFileUpload       -> BigFileUploadGrant / BigFileStore
    requestZarrUpload    / finishZarrUpload          -> ZarrUploadGrant    / ZarrStore

A ``ParsingLink`` cannot drive that shape on its own: the ``finish*`` call has to happen after
the bytes land, which is a step later than a link that rewrites variables in flight. Implementing
it properly means a small uploader that a caller invokes explicitly, not a transparent link.

The class is kept — rather than deleted — because ``KraphLinkComposition.upload`` is a required
field and ``tests/conftest.py`` imports the name. It passes operations through untouched.
"""

from typing import Optional

from pydantic import ConfigDict, Field
from rath.links.parsing import ParsingLink
from rath.operation import Operation

from kraph.datalayer import DataLayer


class UploadLink(ParsingLink):
    """Passes operations through unchanged.

    See the module docstring for what this used to do and what replacing it requires.
    """

    datalayer: Optional[DataLayer] = Field(default=None, exclude=True)

    async def aparse(self, operation: Operation) -> Operation:
        """Return the operation untouched — there is nothing to rewrite."""
        return operation

    model_config = ConfigDict(arbitrary_types_allowed=True)
