"""Kraph traits — behaviour mixed into the turms-generated models.

These classes are attached by GraphQL type name through ``additional_bases`` in
``graphql.config.yaml``. turms emits ``class Instance(InstanceTrait, BaseModel)`` and imports the
base **by name at generation time**, so every name referenced by that config must exist here
before codegen runs.

The shape of this module follows the server's evidence-log model:

* A **claim** names a *word* (a ``Term.key``), never a graph and never a category. Recording is
  therefore graph-free, and the write functions live on the generated module, not here.
* A **view** (``Graph``) declares what a word means *there*. Categories are read-side and
  schema-side only — they never author a claim, which is why no category trait is callable.
* Nothing is edited in place. ``attest`` and ``retract`` both record a *position*
  (``Standing``); neither deletes, and ``attest`` is not an undo.

Two consequences worth stating, because both were bugs in the previous design:

* There is no folded ``stands`` boolean on an instance — whether a node exists is a per-view
  question. Read ``standings`` for every recorded position, or ``drawings`` for one view's answer.
* An empty ``drawings`` is an ordinary outcome, not an error: a claim names a word the
  organization owns, and a view that declares no category for that word simply will not draw it.
"""

from typing import TYPE_CHECKING, Any, Optional

from koil import unkoil
from pydantic import BaseModel
from rath.origin import ContextBound
from rath.turms.utils import get_attributes_or_error

from kraph.client import client_of

if TYPE_CHECKING:
    from rekuest.structures.registry import StructureRegistry

    from kraph.kraph import Kraph


class AssertedTrait(BaseModel):
    """Common behaviour for the fourteen ``Asserted*`` write payloads.

    Every write records exactly one :class:`Assertion` and returns it alongside the claim it
    made. The payloads are deliberately *not* uniform — seven carry ``drawings`` and seven do
    not, because a measurement or a structure has no vertex to draw — so this trait only covers
    what all of them genuinely share.
    """

    @property
    def seq(self) -> int:
        """Position of this write in the organization-spanning log.

        Compare against ``Graph.projection.projectedThroughSeq`` to know whether a given view has
        drawn this claim yet.
        """
        return get_attributes_or_error(self, "assertion").seq

    @property
    def claim(self) -> Any:
        """The thing this write recorded, whichever field the payload carries it in."""
        for field in ("instance", "instances", "link", "links", "structure", "metric", "comment"):
            value = getattr(self, field, None)
            if value is not None:
                return value
        raise AttributeError(f"{type(self).__name__} carries no recognised claim field")

    @property
    def id(self) -> str:
        """Id of the recorded claim, so a result can be passed straight back as a reference."""
        claim = self.claim
        if isinstance(claim, list):
            raise AttributeError(
                f"{type(self).__name__} recorded {len(claim)} claims under one assertion; "
                "use .claim and pick one"
            )
        return get_attributes_or_error(claim, "id")


class HasDrawings(BaseModel):
    """Mixed into the seven payloads that report how views drew the claim."""

    @property
    def is_drawn(self) -> bool:
        """Whether any view draws this claim.

        ``False`` is an ordinary answer, not a failure — see the module docstring.
        """
        return bool(get_attributes_or_error(self, "drawings"))

    def drawn_in(self, graph: Any) -> Optional[Any]:
        """This view's account of the claim, or ``None`` if this view does not draw it."""
        wanted = graph if isinstance(graph, str) else get_attributes_or_error(graph, "id")
        for drawing in get_attributes_or_error(self, "drawings"):
            if str(drawing.graph.id) == str(wanted):
                return drawing
        return None


class InstanceTrait(BaseModel):
    """A claimed individual — an entity or an event — as the log holds it."""

    @property
    def ref(self) -> str:
        """The claim's durable identity: a bare uuid, stable across reprojects."""
        return get_attributes_or_error(self, "id")


class LinkTrait(BaseModel):
    """A claim relating two things. ``kind`` says what it says and which end is which."""

    @property
    def ref(self) -> str:
        return get_attributes_or_error(self, "id")


class NodeTrait(BaseModel):
    """A node as one view draws it."""


class EdgeTrait(BaseModel):
    """An edge as one view draws it."""


class EntityTrait(BaseModel):
    """An instance that is not an event, drawn by a view."""


class TermTrait(BaseModel):
    """A word the organization uses. Usable directly wherever a ``term: String!`` is wanted."""

    def __str__(self) -> str:
        return get_attributes_or_error(self, "key")


class StructureKindTrait(BaseModel):
    """A kind of external datum. Minted lazily by the first write that names it."""

    def __str__(self) -> str:
        return get_attributes_or_error(self, "identifier")


class MetricKindTrait(BaseModel):
    """A kind of measured value. Minted by the write that knows the value kind."""

    def __str__(self) -> str:
        return get_attributes_or_error(self, "key")


class StandingTrait(BaseModel):
    """Somebody's position on whether a claim still holds."""

    def __bool__(self) -> bool:
        return bool(get_attributes_or_error(self, "stands"))


class AssertionTrait(BaseModel):
    """The act: who claimed it, with what tool, when, and where it sits in the log."""

    def __str__(self) -> str:
        subject, asserted_at, seq = get_attributes_or_error(
            self, "subject", "assertedAt", "seq"
        )
        return f"{subject} at {asserted_at} (seq {seq})"


class MetricTrait(BaseModel):
    """A measured value about a structure."""


class StructureTrait(BaseModel):
    """A pointer to an external datum, addressed by ``(identifier, object)``.

    Immutable: repointing at a different object is refused rather than superseded, and the row is
    idempotent per ``(organization, identifier, object)``.
    """

    @property
    def ref(self) -> tuple[str, str]:
        """The ``(identifier, object)`` pair that addresses this datum."""
        return get_attributes_or_error(self, "identifier", "object")

    def resolve(self, registry: "StructureRegistry") -> Any:
        """Expand this structure back into the concrete Python object it points at.

        Uses ``registry``, a structure registry bound to its clients (the one a running task
        expands its arguments with), so the datum's own service (mikro, and so on) does the
        loading, through the client of that service the registry was bound to.
        """
        identifier, object_id = get_attributes_or_error(self, "identifier", "object")
        fullfilled = registry.get_fullfilled_structure(identifier)
        return unkoil(fullfilled.expand, object_id)


class CategoryTrait(BaseModel):
    """One view's rule for a word.

    Read-side and schema-side only. A category is deliberately **not callable**: in the evidence
    model a claim names a word, so authoring one through a view would state a fact in terms of
    one reader's opinion of it.
    """

    def __str__(self) -> str:
        return get_attributes_or_error(self, "key")


class NodeCategoryTrait(BaseModel):
    """A category that draws vertices."""


class EdgeCategoryTrait(BaseModel):
    """A category that draws edges."""


class EntityCategoryTrait(BaseModel):
    """A view's declaration of an entity word."""


class RelationCategoryTrait(BaseModel):
    """A view's declaration of a relation word."""


class MeasurementCategoryTrait(BaseModel):
    """A view's declaration of a measurement word."""


class StructureRelationCategoryTrait(BaseModel):
    """A view's declaration of a structure-relation word."""


class NaturalEventCategoryTrait(BaseModel):
    """A view's declaration of a natural-event word."""


class ProtocolEventCategoryTrait(BaseModel):
    """A view's declaration of a protocol-event word."""


class ProjectionTrait(BaseModel):
    """Where a view's drawing stands relative to the organization's log."""

    def is_current_for(self, seq: int) -> bool:
        """Whether this view has drawn everything up to ``seq``."""
        return get_attributes_or_error(self, "projectedThroughSeq") >= seq

    def __str__(self) -> str:
        status, through, lag, pending = get_attributes_or_error(
            self, "status", "projectedThroughSeq", "lag", "pending"
        )
        return f"{status} through seq {through} (lag {lag}, {pending} pending)"


class GraphTrait(ContextBound):
    """A view over the organization's claims.

    Not a container — a reconstruction. A node can be drawn by several views at once, and a
    claim recorded under a word this view does not declare is simply not drawn here.

    Context bound: a graph polls its projection through the client that fetched it.
    """

    @property
    def projection_state(self) -> Any:
        return get_attributes_or_error(self, "projection")

    def wait_until_projected(
        self,
        seq: int,
        *,
        timeout: float = 30.0,
        poll: float = 0.5,
        kraph: Optional["Kraph"] = None,
    ) -> Any:
        """Block until this view has drawn everything up to ``seq``.

        Never implicit: a backfill or a category edit redraws in-request and is unbounded in the
        size of the graph, so no write waits on its own. Raises :class:`ProjectionTimeout`
        carrying the last projection read, rather than returning a stale answer.

        Polls through ``kraph`` if given, else through the client that fetched this graph.
        """
        import time

        from kraph.errors import ProjectionTimeout

        client = client_of(self, kraph)
        graph_id = get_attributes_or_error(self, "id")
        deadline = time.monotonic() + timeout
        projection = None
        while time.monotonic() < deadline:
            projection = client.get_graph(id=graph_id).projection
            if projection.projected_through_seq >= seq:
                return projection
            time.sleep(poll)
        raise ProjectionTimeout(
            f"view {graph_id} did not draw seq {seq} within {timeout}s: {projection}"
        )


class HasPresignedDownloadAccessor(ContextBound):
    """Download accessor for media stores."""

    _accessor = ("key", "bucket")

    def download(self, file_name: Optional[str] = None, kraph: Optional["Kraph"] = None) -> str:
        """Download this file through the datalayer of ``kraph``, else of the client that fetched it."""
        from kraph.io import download_file

        url, key = get_attributes_or_error(self, "presigned_url", "key")
        return download_file(client_of(self, kraph).datalayer, url, file_name=file_name or key)
