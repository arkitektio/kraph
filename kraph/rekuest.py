"""Registration of kraph types with the rekuest structure registry.

The ``@kraph/…`` identifier strings are a wire contract: other arkitekt services resolve against
them, so renaming one is a coordinated cross-service change, not a local refactor. Two of them
therefore keep their old spelling while pointing at a renamed type — ``@kraph/structurecategory``
now names a :class:`StructureKind`, and ``@kraph/metriccategory`` a :class:`MetricKind`.

One registration changed meaning and could not keep its type. ``@kraph/entity`` used to expand
through ``aget_node(id)``, but the view-grain readers (``node``/``entity``) now require a graph
as well as an id, and ``aexpand`` is handed only the id. ``instance(id:)`` is the graph-free
addressable claim, so that is what the identifier resolves to.

``Reagent`` and ``GraphQuery`` are gone: reagents are ordinary entities now, and ``GraphQuery``
is an interface whose only concrete member is the deferred table-query surface.
"""

from rekuest.structures.default import get_default_structure_registry, id_shrink
from rekuest.widgets import SearchWidget

from kraph.api.schema import (
    EntityCategory,
    Graph,
    Instance,
    Link,
    MeasurementCategory,
    Metric,
    MetricKind,
    NaturalEventCategory,
    ProtocolEventCategory,
    RelationCategory,
    SearchEntityCategoriesQuery,
    SearchGraphsQuery,
    SearchMeasurementCategoriesQuery,
    SearchMetricKindsQuery,
    SearchNaturalEventCategoriesQuery,
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
    aget_entity_category,
    aget_graph,
    aget_instance,
    aget_link,
    aget_measurement_category,
    aget_metric,
    aget_metric_kind,
    aget_natural_event_category,
    aget_protocol_event_category,
    aget_relation_category,
    aget_structure,
    aget_structure_kind,
    aget_structure_relation_category,
    aget_term,
)

structure_reg = get_default_structure_registry()


def _register(cls, identifier, aexpand, query=None):
    structure_reg.register_as_structure(
        cls,
        identifier=identifier,
        aexpand=aexpand,
        ashrink=id_shrink,
        default_widget=SearchWidget(query=query.Meta.document, ward="kraph")
        if query is not None
        else None,
    )


# --- views and their declarations -----------------------------------------------------------
_register(Graph, "@kraph/graph", aget_graph, SearchGraphsQuery)
_register(EntityCategory, "@kraph/entitycategory", aget_entity_category, SearchEntityCategoriesQuery)
_register(RelationCategory, "@kraph/relationcategory", aget_relation_category, SearchRelationCategoriesQuery)
_register(MeasurementCategory, "@kraph/measurementcategory", aget_measurement_category, SearchMeasurementCategoriesQuery)
_register(StructureRelationCategory, "@kraph/structurerelationcategory", aget_structure_relation_category, SearchStructureRelationCategoriesQuery)
_register(NaturalEventCategory, "@kraph/naturaleventcategory", aget_natural_event_category, SearchNaturalEventCategoriesQuery)
_register(ProtocolEventCategory, "@kraph/protocoleventcategory", aget_protocol_event_category, SearchProtocolEventCategoriesQuery)

# --- claims ---------------------------------------------------------------------------------
# `Instance` has no scalar label — its name lives at `term { key }` — so it gets no search
# widget: a two-field `value`/`label` projection cannot reach it.
_register(Instance, "@kraph/entity", aget_instance)
_register(Link, "@kraph/link", aget_link)
_register(Structure, "@kraph/structure", aget_structure, SearchStructuresQuery)
_register(Metric, "@kraph/metric", aget_metric)

# --- vocabulary -----------------------------------------------------------------------------
_register(Term, "@kraph/term", aget_term, SearchTermsQuery)
# Identifier kept for wire compatibility; the type behind it is now StructureKind/MetricKind.
_register(StructureKind, "@kraph/structurecategory", aget_structure_kind, SearchStructureKindsQuery)
_register(MetricKind, "@kraph/metriccategory", aget_metric_kind, SearchMetricKindsQuery)
