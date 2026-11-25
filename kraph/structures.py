"""The types kraph sends by id: each expanded by the ``Kraph`` client.

Imported by ``kraph/__init__``, so each class is marked whenever kraph is.

The ``@kraph/…`` identifier strings are a wire contract: other arkitekt services
resolve against them, so renaming one is a coordinated cross-service change, not a
local refactor. Two of them therefore keep their old spelling while pointing at a
renamed type — ``@kraph/structurecategory`` now names a :class:`StructureKind`, and
``@kraph/metriccategory`` a :class:`MetricKind`.

One identifier changed meaning and could not keep its type. ``@kraph/entity`` used
to expand through ``get_node(id)``, but the view-grain readers (``node``/``entity``)
now require a graph as well as an id, and an expander is handed only the id.
``instance(id:)`` is the graph-free addressable claim, so that is what the identifier
resolves to — visible now in the expander itself rather than in a separate map.

``Reagent`` and ``GraphQuery`` are gone: reagents are ordinary entities now, and
``GraphQuery`` is an interface whose only concrete member is the deferred
table-query surface.
"""

from arkitekt_spec.actions import AssignWidgetInput
from arkitekt_spec.declare.structures.declare import structure
from arkitekt_spec.declare.widgets import SearchWidget

from kraph.api.schema import (
    EntityCategory,
    Graph,
    GraphPairsQuery,
    Instance,
    Link,
    MeasurementCategory,
    Metric,
    MetricKind,
    Model,
    NaturalEventCategory,
    PairsQueryRun,
    ProtocolEventCategory,
    RelationCategory,
    SearchEntityCategoriesQuery,
    SearchGraphPairsQueriesQuery,
    SearchGraphsQuery,
    SearchMeasurementCategoriesQuery,
    SearchMetricKindsQuery,
    SearchModelsQuery,
    SearchNaturalEventCategoriesQuery,
    SearchPairsQueryRunsQuery,
    SearchProtocolEventCategoriesQuery,
    SearchRelationCategoriesQuery,
    SearchStructureKindsQuery,
    SearchStructureRelationCategoriesQuery,
    SearchStructuresQuery,
    SearchTermsQuery,
    Structure,
    StructureKind,
    StructureRelationCategory,
    Term,
)
from kraph.kraph import Kraph


def _search(query: object) -> AssignWidgetInput:
    """The widget that picks one of these out of the deployment."""
    return SearchWidget(query=query.Meta.document, ward="kraph")  # type: ignore[attr-defined]


# --- views and their declarations ------------------------------------------------


@structure("@kraph/graph", widget=_search(SearchGraphsQuery))
async def expand_graph(id: str, kraph: Kraph) -> Graph:
    """A graph, by id."""
    return await kraph.aget_graph(id)


@structure("@kraph/entitycategory", widget=_search(SearchEntityCategoriesQuery))
async def expand_entity_category(id: str, kraph: Kraph) -> EntityCategory:
    """An entity category, by id."""
    return await kraph.aget_entity_category(id)


@structure(
    "@kraph/relationcategory",
    widget=_search(SearchRelationCategoriesQuery),
)
async def expand_relation_category(id: str, kraph: Kraph) -> RelationCategory:
    """A relation category, by id."""
    return await kraph.aget_relation_category(id)


@structure(
    "@kraph/measurementcategory",
    widget=_search(SearchMeasurementCategoriesQuery),
)
async def expand_measurement_category(id: str, kraph: Kraph) -> MeasurementCategory:
    """A measurement category, by id."""
    return await kraph.aget_measurement_category(id)


@structure(
    "@kraph/structurerelationcategory",
    widget=_search(SearchStructureRelationCategoriesQuery),
)
async def expand_structure_relation_category(
    id: str, kraph: Kraph
) -> StructureRelationCategory:
    """A structure relation category, by id."""
    return await kraph.aget_structure_relation_category(id)


@structure(
    "@kraph/naturaleventcategory",
    widget=_search(SearchNaturalEventCategoriesQuery),
)
async def expand_natural_event_category(id: str, kraph: Kraph) -> NaturalEventCategory:
    """A natural event category, by id."""
    return await kraph.aget_natural_event_category(id)


@structure(
    "@kraph/protocoleventcategory",
    widget=_search(SearchProtocolEventCategoriesQuery),
)
async def expand_protocol_event_category(
    id: str, kraph: Kraph
) -> ProtocolEventCategory:
    """A protocol event category, by id."""
    return await kraph.aget_protocol_event_category(id)


# --- claims ----------------------------------------------------------------------


# `Instance` has no scalar label -- its name lives at `term { key }` -- so it gets no
# search widget: a two-field `value`/`label` projection cannot reach it.
@structure("@kraph/entity")
async def expand_entity(id: str, kraph: Kraph) -> Instance:
    """The graph-free addressable claim an `@kraph/entity` names, by id."""
    return await kraph.aget_instance(id)


@structure("@kraph/link")
async def expand_link(id: str, kraph: Kraph) -> Link:
    """A link, by id."""
    return await kraph.aget_link(id)


@structure("@kraph/structure", widget=_search(SearchStructuresQuery))
async def expand_structure(id: str, kraph: Kraph) -> Structure:
    """A structure, by id."""
    return await kraph.aget_structure(id)


@structure("@kraph/metric")
async def expand_metric(id: str, kraph: Kraph) -> Metric:
    """A metric, by id."""
    return await kraph.aget_metric(id)


# --- vocabulary ------------------------------------------------------------------


@structure("@kraph/term", widget=_search(SearchTermsQuery))
async def expand_term(id: str, kraph: Kraph) -> Term:
    """A term, by id."""
    return await kraph.aget_term(id)


# Identifier kept for wire compatibility; the type behind it is now StructureKind.
@structure("@kraph/structurecategory", widget=_search(SearchStructureKindsQuery))
async def expand_structure_kind(id: str, kraph: Kraph) -> StructureKind:
    """A structure kind, by id -- it travels as `@kraph/structurecategory`."""
    return await kraph.aget_structure_kind(id)


# Identifier kept for wire compatibility; the type behind it is now MetricKind.
@structure("@kraph/metriccategory", widget=_search(SearchMetricKindsQuery))
async def expand_metric_kind(id: str, kraph: Kraph) -> MetricKind:
    """A metric kind, by id -- it travels as `@kraph/metriccategory`."""
    return await kraph.aget_metric_kind(id)


# --- derived datasets -------------------------------------------------------------


def describe_pairs_query(query: GraphPairsQuery) -> dict:
    """What a pairs query says about itself: the descriptors the server stored on it.

    A port typed ``GraphPairsQuery["@mikro/arraylens", "@mikro/arraylens"]`` requires
    ``@kraph/source_identifier`` and ``@kraph/target_identifier``; the runtime tests them
    against this when it expands the argument.
    """
    return dict(query.descriptors or {})


# The search widgets forward a port's `requires` ($requires), so a picker for a typed port
# offers only the queries and runs that port accepts.
@structure(
    "@kraph/pairsquery",
    widget=_search(SearchGraphPairsQueriesQuery),
    describe=describe_pairs_query,
)
async def expand_pairs_query(id: str, kraph: Kraph) -> GraphPairsQuery:
    """A pairs query, by id: an insight over a view that selects pairs from its drawing."""
    return await kraph.aget_graph_pairs_query(id)


def describe_pairs_run(run: PairsQueryRun) -> dict:
    """What a run says about itself: its query, size, position, and the identifiers every pair shares."""
    return dict(run.descriptors or {})


@structure(
    "@kraph/pairsrun",
    widget=_search(SearchPairsQueryRunsQuery),
    describe=describe_pairs_run,
)
async def expand_pairs_run(id: str, kraph: Kraph) -> PairsQueryRun:
    """A run, by id: a pairs query's answer stored with where the drawing stood."""
    return await kraph.aget_pairs_query_run(id)


def describe_model(model: Model) -> dict:
    """What a trained model says about itself: the descriptors the server stored on it.

    Its framework and what it was trained on, so a prediction port can require, say,
    ``@kraph/framework`` EQUALS ``care`` and ``@kraph/source_identifier`` EQUALS
    ``@mikro/arraylens``; the runtime tests them against this when it expands the argument.
    """
    return dict(model.descriptors or {})


@structure("@kraph/model", widget=_search(SearchModelsQuery), describe=describe_model)
async def expand_model(id: str, kraph: Kraph) -> Model:
    """A trained model, by id: its weights and the pairs query run it learned from."""
    return await kraph.aget_model(id)
