"""The kraph service of an arkitekt app, and the types it sends by id.

Declared on one registry: the service first, then the structures whose expanders
ask for the ``Kraph`` it returns. Each type is declared once -- the class, the
identifier it travels under, the widget a user picks one with, and how to fetch it
back. An app takes all of it in with ``App(services=[kraph_service])``.

The ``@kraph/…`` identifier strings are a wire contract: other arkitekt services
resolve against them, so renaming one is a coordinated cross-service change, not a
local refactor. Two of them therefore keep their old spelling while pointing at a
renamed type — ``@kraph/structurecategory`` now names a :class:`StructureKind`, and
``@kraph/metriccategory`` a :class:`MetricKind`.

One registration changed meaning and could not keep its type. ``@kraph/entity`` used
to expand through ``get_node(id)``, but the view-grain readers (``node``/``entity``)
now require a graph as well as an id, and an expander is handed only the id.
``instance(id:)`` is the graph-free addressable claim, so that is what the identifier
resolves to — visible now in the expander itself rather than in a separate map.

``Reagent`` and ``GraphQuery`` are gone: reagents are ordinary entities now, and
``GraphQuery`` is an interface whose only concrete member is the deferred
table-query surface.
"""

import os
from typing import Annotated, Optional

from fakts import Alias, Require, TokenLoader
from fakts.contrib.rath.auth import FaktsAuthLink
from graphql import OperationType
from rath.links import compose
from rath.links.aiohttp import AIOHttpLink
from rath.links.dictinglink import DictingLink
from rath.links.graphql_ws import GraphQLWSLink
from rath.links.shrink import ShrinkingLink
from rath.links.split import SplitLink

from rekuest.app import AppRegistry
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
)

from kraph.datalayer import DataLayer
from kraph.kraph import Kraph
from kraph.links.upload import UploadLink
from kraph.rath import KraphRath


def build_relative_path(*path: str) -> str:
    """Build a path relative to this file, for the files shipped beside it."""
    return os.path.join(os.path.dirname(__file__), *path)


registry = AppRegistry()
"""What kraph brings to an app: its service, and the types it can send by id."""


@registry.service(
    schema=build_relative_path("api", "schema.graphql"),
    turms=build_relative_path("api", "project.json"),
)
def kraph(
    kraph: Annotated[
        Alias,
        Require("live.arkitekt.kraph", "Where the knowledge graph relating entities lives"),
    ],
    datalayer: Annotated[
        Optional[Alias],
        Require("live.arkitekt.s3", "Where the graph's files are stored", optional=True),
    ],
    tokens: TokenLoader,
) -> Kraph:
    """Kraph: the knowledge graph relating entities.

    The datalayer is optional, so a deployment that offers no store still gets a
    working client -- uploads are what stop working, not the graph.
    """
    store = DataLayer.from_alias(datalayer) if datalayer is not None else DataLayer()

    return Kraph(
        rath=KraphRath(
            link=compose(
                ShrinkingLink(),
                DictingLink(),
                FaktsAuthLink(token_loader=tokens),
                UploadLink(datalayer=store),
                SplitLink(
                    left=AIOHttpLink(endpoint_url=kraph.to_http_path("graphql")),
                    right=GraphQLWSLink(ws_endpoint_url=kraph.to_ws_path("graphql")),
                    split=lambda o: o.node.operation != OperationType.SUBSCRIPTION,
                ),
            )
        ),
        datalayer=store,
    )


def _search(query: object) -> SearchWidget:
    """The widget that picks one of these out of the deployment."""
    return SearchWidget(query=query.Meta.document, ward="kraph")  # type: ignore[attr-defined]


# --- views and their declarations ------------------------------------------------


@registry.structure("@kraph/graph", widget=_search(SearchGraphsQuery))
async def expand_graph(id: str, kraph: Kraph) -> Graph:
    """A graph, by id."""
    return await kraph.aget_graph(id)


@registry.structure("@kraph/entitycategory", widget=_search(SearchEntityCategoriesQuery)
)
async def expand_entity_category(id: str, kraph: Kraph) -> EntityCategory:
    """An entity category, by id."""
    return await kraph.aget_entity_category(id)


@registry.structure("@kraph/relationcategory",
    widget=_search(SearchRelationCategoriesQuery),
)
async def expand_relation_category(id: str, kraph: Kraph) -> RelationCategory:
    """A relation category, by id."""
    return await kraph.aget_relation_category(id)


@registry.structure("@kraph/measurementcategory",
    widget=_search(SearchMeasurementCategoriesQuery),
)
async def expand_measurement_category(id: str, kraph: Kraph) -> MeasurementCategory:
    """A measurement category, by id."""
    return await kraph.aget_measurement_category(id)


@registry.structure("@kraph/structurerelationcategory",
    widget=_search(SearchStructureRelationCategoriesQuery),
)
async def expand_structure_relation_category(
    id: str, kraph: Kraph
) -> StructureRelationCategory:
    """A structure relation category, by id."""
    return await kraph.aget_structure_relation_category(id)


@registry.structure("@kraph/naturaleventcategory",
    widget=_search(SearchNaturalEventCategoriesQuery),
)
async def expand_natural_event_category(id: str, kraph: Kraph) -> NaturalEventCategory:
    """A natural event category, by id."""
    return await kraph.aget_natural_event_category(id)


@registry.structure("@kraph/protocoleventcategory",
    widget=_search(SearchProtocolEventCategoriesQuery),
)
async def expand_protocol_event_category(id: str, kraph: Kraph) -> ProtocolEventCategory:
    """A protocol event category, by id."""
    return await kraph.aget_protocol_event_category(id)


# --- claims ----------------------------------------------------------------------

# `Instance` has no scalar label -- its name lives at `term { key }` -- so it gets no
# search widget: a two-field `value`/`label` projection cannot reach it.
@registry.structure("@kraph/entity")
async def expand_entity(id: str, kraph: Kraph) -> Instance:
    """The graph-free addressable claim an `@kraph/entity` names, by id."""
    return await kraph.aget_instance(id)


@registry.structure("@kraph/link")
async def expand_link(id: str, kraph: Kraph) -> Link:
    """A link, by id."""
    return await kraph.aget_link(id)


@registry.structure("@kraph/structure", widget=_search(SearchStructuresQuery))
async def expand_structure(id: str, kraph: Kraph) -> Structure:
    """A structure, by id."""
    return await kraph.aget_structure(id)


@registry.structure("@kraph/metric")
async def expand_metric(id: str, kraph: Kraph) -> Metric:
    """A metric, by id."""
    return await kraph.aget_metric(id)


# --- vocabulary ------------------------------------------------------------------


@registry.structure("@kraph/term", widget=_search(SearchTermsQuery))
async def expand_term(id: str, kraph: Kraph) -> Term:
    """A term, by id."""
    return await kraph.aget_term(id)


# Identifier kept for wire compatibility; the type behind it is now StructureKind.
@registry.structure("@kraph/structurecategory", widget=_search(SearchStructureKindsQuery)
)
async def expand_structure_kind(id: str, kraph: Kraph) -> StructureKind:
    """A structure kind, by id -- it travels as `@kraph/structurecategory`."""
    return await kraph.aget_structure_kind(id)


# Identifier kept for wire compatibility; the type behind it is now MetricKind.
@registry.structure("@kraph/metriccategory", widget=_search(SearchMetricKindsQuery)
)
async def expand_metric_kind(id: str, kraph: Kraph) -> MetricKind:
    """A metric kind, by id -- it travels as `@kraph/metriccategory`."""
    return await kraph.aget_metric_kind(id)
