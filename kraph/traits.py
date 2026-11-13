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

from typing import TYPE_CHECKING, Any

from koil import unkoil
from pydantic import BaseModel
from rath.origin import ContextBound
from rath.turms.utils import get_attributes_or_error

from kraph.client import client_of

if TYPE_CHECKING:
    from arkitekt_spec.declare.structures.registry import StructureRegistry

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

    def drawn_in(self, graph: Any) -> Any | None:
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
    """A view's declaration of a structure-relation word: a claim under it is drawn as an edge
    between two structure vertices where the view mounts both ends (RFC 0027). Claim a pair
    under it with :func:`kraph.pairs.pair`; select pairs with a pairs query."""


class StructureCategoryTrait(BaseModel):
    """A structure kind a view mounts: the vertex label its data are drawn under (RFC 0027)."""


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
        kraph: "Kraph | None" = None,
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


#: The descriptor keys a paired dataset is required by, as kraph's server declares them.
SOURCE_IDENTIFIER = "@kraph/source_identifier"
TARGET_IDENTIFIER = "@kraph/target_identifier"


def structure_identifier(end: Any) -> str:  # noqa: ANN401
    """The structure identifier one end of a pair names: a string, or a class stamped with one.

    mikro's generated models carry ``__identifier__`` (``ArrayLens`` is ``'@mikro/arraylens'``),
    so ``PairsQueryRun[ArrayLens, ArrayLens]`` reads the same as the strings.
    """
    if isinstance(end, str):
        return end
    stamped = getattr(end, "__identifier__", None)
    if isinstance(stamped, str):
        return stamped
    raise TypeError(f"A pair's end is a structure identifier ('@mikro/arraylens') or a class stamped with one, not {end!r}")


def _typed_by_ends(cls: type, ends: Any, name: str) -> Any:  # noqa: ANN401
    """``cls`` narrowed to the given ends: ``Annotated[cls, Requires(source), Requires(target)]``.

    A plain ``Annotated`` (never a PEP 695 alias: rekuest drops markers on those) with two
    ``Requires`` on the identifier descriptors a pairs query and its runs both carry. An end
    constrained to no single identifier carries null, so it satisfies neither.
    """
    from typing import Annotated

    from arkitekt_spec.actions import DescriptorOperator
    from arkitekt_spec.declare.annotations.markers import Requires

    if not isinstance(ends, tuple) or len(ends) != 2:
        raise TypeError(f"{name} takes two ends, {name}[source, target]")
    source, target = (structure_identifier(end) for end in ends)
    return Annotated[
        cls,
        Requires(key=SOURCE_IDENTIFIER, operator=DescriptorOperator.EQUALS, value=source),
        Requires(key=TARGET_IDENTIFIER, operator=DescriptorOperator.EQUALS, value=target),
    ]


def _read_pairs(fetch: Any, page: int) -> list[Any]:  # noqa: ANN401
    """Every pair, page by page: ``fetch(pagination)`` returns one page."""
    from kraph.api.schema import OffsetPaginationInput

    found: list[Any] = []
    while True:
        chunk = list(fetch(OffsetPaginationInput(offset=len(found), limit=page)))
        found.extend(chunk)
        if len(chunk) < page:
            return found


def _expanded(registry: "StructureRegistry", pairs: list[Any]) -> list[tuple[Any, Any]]:
    """Each pair as the objects themselves, expanded by their own services through ``registry``."""

    def expand(identifier: str, object_id: str) -> Any:  # noqa: ANN401
        return unkoil(registry.get_fullfilled_structure(identifier).expand, object_id)

    return [(expand(pair.source_identifier, pair.source_object), expand(pair.target_identifier, pair.target_object)) for pair in pairs]


class GraphPairsQueryTrait(ContextBound):
    """A pairs query: an insight over a view that selects pairs from its drawing.

    Typed in a port as ``GraphPairsQuery[source, target]``, it requires queries whose ends
    are constrained to those identifiers, and the picker offers only those. :meth:`preview`
    reads its pairs live; :meth:`run` stores them as a training set.
    """

    def __class_getitem__(cls, ends: Any) -> Any:  # noqa: ANN401
        """``GraphPairsQuery["@mikro/arraylens", "@mikro/arraylens"]``: image-pair queries only."""
        return _typed_by_ends(cls, ends, "GraphPairsQuery")

    def preview(self, *, kraph: "Kraph | None" = None, page: int = 1000) -> list[Any]:
        """Every pair the query answers now, from the view's drawing. Not a record: run it for one."""
        client = client_of(self, kraph)
        query_id = get_attributes_or_error(self, "id")
        return _read_pairs(lambda pagination: client.render_graph_pairs(id=query_id, pagination=pagination), page)

    def run(self, name: str, *, description: str | None = None, kraph: "Kraph | None" = None) -> Any:  # noqa: ANN401
        """Run the query: its answer, stored with where the drawing stood. What a model cites."""
        return client_of(self, kraph).run_pairs_query(query=get_attributes_or_error(self, "id"), name=name, description=description)


class PairsQueryRunTrait(ContextBound):
    """A pairs query's stored answer: the exact pairs a model learned from, with ``as_of_seq``.

    Typed in a port as ``PairsQueryRun[source, target]``, it requires runs whose every pair has
    those identifiers, and the picker offers only those. A run mixing kinds carries a null
    identifier and satisfies no typed port.
    """

    def __class_getitem__(cls, ends: Any) -> Any:  # noqa: ANN401
        """``PairsQueryRun["@mikro/arraylens", "@mikro/arraylens"]``: runs of image pairs only."""
        return _typed_by_ends(cls, ends, "PairsQueryRun")

    def read_entries(self, *, kraph: "Kraph | None" = None, page: int = 1000) -> list[Any]:
        """Every stored pair, in the run's order, as ``(identifier, object)`` addresses."""
        client = client_of(self, kraph)
        run_id = get_attributes_or_error(self, "id")
        return _read_pairs(lambda pagination: client.get_run_entries(id=run_id, pagination=pagination).page, page)

    def pairs(self, registry: "StructureRegistry", *, kraph: "Kraph | None" = None) -> list[tuple[Any, Any]]:
        """Every pair as the objects themselves: ``(source, target)``, each expanded by its own service.

        ``registry`` is a structure registry bound to its clients (the one a running task
        expands its arguments with), so an ``@mikro/arraylens`` end comes back as an
        ``ArrayLens`` fetched through mikro, the way `StructureTrait.resolve` does it.
        """
        return _expanded(registry, self.read_entries(kraph=kraph))


class BigFileStoreTrait(ContextBound):
    """A big file in kraph's datalayer: read back through an access grant, never by its path."""

    def download(self, file_name: str | None = None, *, kraph: "Kraph | None" = None) -> str:
        """Stream the file to ``file_name`` (its uploaded name by default). Returns the path written."""
        from kraph.io.download import download_bigfile, file_name_of

        return download_bigfile(str(get_attributes_or_error(self, "id")), file_name_of(self, file_name), client_of(self, kraph))

    async def adownload(self, file_name: str | None = None, *, kraph: "Kraph | None" = None) -> str:
        """Stream the file to ``file_name`` (its uploaded name by default). Returns the path written."""
        from kraph.io.download import adownload_bigfile, file_name_of

        return await adownload_bigfile(str(get_attributes_or_error(self, "id")), file_name_of(self, file_name), client_of(self, kraph))


class ModelTrait(ContextBound):
    """A trained model: its weights in kraph's datalayer, and the pairs query run it learned from.

    Registered with ``create_model(store=<path or open file>, ...)``: the upload middleware
    sends the file and passes the finished store on, as every service's files are uploaded.
    """

    def download(self, file_name: str | None = None, *, kraph: "Kraph | None" = None) -> str:
        """Stream the weights to ``file_name`` (their uploaded name by default). Returns the path written."""
        from kraph.io.download import download_bigfile, file_name_of

        store = get_attributes_or_error(self, "store")
        return download_bigfile(str(get_attributes_or_error(store, "id")), file_name_of(store, file_name), client_of(self, kraph))

    async def adownload(self, file_name: str | None = None, *, kraph: "Kraph | None" = None) -> str:
        """Stream the weights to ``file_name`` (their uploaded name by default). Returns the path written."""
        from kraph.io.download import adownload_bigfile, file_name_of

        store = get_attributes_or_error(self, "store")
        return await adownload_bigfile(str(get_attributes_or_error(store, "id")), file_name_of(store, file_name), client_of(self, kraph))
