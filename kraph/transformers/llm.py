from kraph.api.schema import (
    Graph,
    ListEntityCategory,
    ListStructureCategory,
    ListMetricCategory,
    ListRelationCategory,
    ListMeasurementCategory,
    ListProtocolEventCategory,
    ListNaturalEventCategory,
    ListStructureRelationCategory,
    EntityRoleDefinition,
    ReagentRoleDefinition,
)
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field


@dataclass
class GraphSchemaText:
    """Container for formatted graph schema text for LLM consumption."""

    graph_name: str
    graph_description: Optional[str]
    full_text: str
    node_types: List[str] = field(default_factory=list)
    edge_types: List[str] = field(default_factory=list)
    cypher_examples: List[str] = field(default_factory=list)


def _format_entity_category(cat: ListEntityCategory, id_map: Dict[Any, str]) -> str:
    """Format an entity category for LLM consumption."""
    id_map[cat.id] = cat.label
    lines = [
        f"  - **{cat.label}** (AGE label: `{cat.age_name}`)",
        f"    - Type: Entity (instance kind: {cat.instance_kind.value})",
    ]
    if cat.description:
        lines.append(f"    - Description: {cat.description}")
    if cat.tags:
        tags = [t.value for t in cat.tags]
        lines.append(f"    - Tags: {', '.join(tags)}")
    return "\n".join(lines)


def _format_structure_category(
    cat: ListStructureCategory, id_map: Dict[Any, str]
) -> str:
    """Format a structure category for LLM consumption."""
    id_map[cat.id] = cat.identifier
    lines = [
        f"  - **{cat.identifier}** (AGE label: `{cat.age_name}`)",
        "    - Type: Structure (external data reference)",
    ]
    if cat.description:
        lines.append(f"    - Description: {cat.description}")
    return "\n".join(lines)


def _format_metric_category(cat: ListMetricCategory, id_map: Dict[Any, str]) -> str:
    """Format a metric category for LLM consumption."""
    id_map[cat.id] = cat.label
    lines = [
        f"  - **{cat.label}** (AGE label: `{cat.age_name}`)",
        f"    - Type: Metric (value kind: {cat.metric_kind.value})",
    ]
    if cat.description:
        lines.append(f"    - Description: {cat.description}")
    return "\n".join(lines)


def _format_entity_role(role: EntityRoleDefinition, id_map: Dict[Any, str]) -> str:
    """Format an entity role definition."""
    optional_str = " (optional)" if role.optional else " (required)"
    multiple_str = ", allows multiple" if role.allow_multiple else ""

    # Resolve category filters to names
    cat_names = []
    if role.category_definition.category_filters:
        for cat_id in role.category_definition.category_filters:
            cat_names.append(id_map.get(cat_id, str(cat_id)))

    cats_str = f" [{', '.join(cat_names)}]" if cat_names else ""
    return f"{role.role}{optional_str}{multiple_str}{cats_str}"


def _format_reagent_role(role: ReagentRoleDefinition, id_map: Dict[Any, str]) -> str:
    """Format a reagent role definition."""
    optional_str = " (optional)" if role.optional else " (required)"
    quantity_str = ", needs quantity" if role.needs_quantity else ""

    cat_names = []
    if role.category_definition.category_filters:
        for cat_id in role.category_definition.category_filters:
            cat_names.append(id_map.get(cat_id, str(cat_id)))

    cats_str = f" [{', '.join(cat_names)}]" if cat_names else ""
    return f"{role.role}{optional_str}{quantity_str}{cats_str}"


def _format_relation_category(cat: ListRelationCategory, id_map: Dict[Any, str]) -> str:
    """Format a relation category for LLM consumption."""
    id_map[cat.id] = cat.label

    # Resolve source/target definitions
    source_cats = []
    if cat.source_definition.category_filters:
        for cat_id in cat.source_definition.category_filters:
            source_cats.append(id_map.get(cat_id, str(cat_id)))

    target_cats = []
    if cat.target_definition.category_filters:
        for cat_id in cat.target_definition.category_filters:
            target_cats.append(id_map.get(cat_id, str(cat_id)))

    source_str = ", ".join(source_cats) if source_cats else "any entity"
    target_str = ", ".join(target_cats) if target_cats else "any entity"

    lines = [
        f"  - **{cat.label}** (AGE label: `{cat.age_name}`)",
        "    - Type: Relation (edge between entities)",
        f"    - Source: {source_str}",
        f"    - Target: {target_str}",
    ]
    if cat.description:
        lines.append(f"    - Description: {cat.description}")
    return "\n".join(lines)


def _format_measurement_category(
    cat: ListMeasurementCategory, id_map: Dict[Any, str]
) -> str:
    """Format a measurement category for LLM consumption."""
    id_map[cat.id] = cat.label

    source_cats = []
    if cat.source_definition.category_filters:
        for cat_id in cat.source_definition.category_filters:
            source_cats.append(id_map.get(cat_id, str(cat_id)))

    target_cats = []
    if cat.target_definition.category_filters:
        for cat_id in cat.target_definition.category_filters:
            target_cats.append(id_map.get(cat_id, str(cat_id)))

    source_str = ", ".join(source_cats) if source_cats else "any structure"
    target_str = ", ".join(target_cats) if target_cats else "any entity"

    lines = [
        f"  - **{cat.label}** (AGE label: `{cat.age_name}`)",
        "    - Type: Measurement (edge from structure to entity)",
        f"    - Source (structure): {source_str}",
        f"    - Target (entity): {target_str}",
    ]
    if cat.description:
        lines.append(f"    - Description: {cat.description}")
    return "\n".join(lines)


def _format_structure_relation_category(
    cat: ListStructureRelationCategory, id_map: Dict[Any, str]
) -> str:
    """Format a structure relation category for LLM consumption."""
    id_map[cat.id] = cat.label

    source_cats = []
    if cat.source_definition.category_filters:
        for cat_id in cat.source_definition.category_filters:
            source_cats.append(id_map.get(cat_id, str(cat_id)))

    target_cats = []
    if cat.target_definition.category_filters:
        for cat_id in cat.target_definition.category_filters:
            target_cats.append(id_map.get(cat_id, str(cat_id)))

    source_str = ", ".join(source_cats) if source_cats else "any structure"
    target_str = ", ".join(target_cats) if target_cats else "any structure"

    lines = [
        f"  - **{cat.label}** (AGE label: `{cat.age_name}`)",
        "    - Type: Structure Relation (edge between structures)",
        f"    - Source: {source_str}",
        f"    - Target: {target_str}",
    ]
    if cat.description:
        lines.append(f"    - Description: {cat.description}")
    return "\n".join(lines)


def _format_protocol_event_category(
    cat: ListProtocolEventCategory, id_map: Dict[Any, str]
) -> str:
    """Format a protocol event category for LLM consumption."""
    id_map[cat.id] = cat.label

    lines = [
        f"  - **{cat.label}** (AGE label: `{cat.age_name}`)",
        "    - Type: Protocol Event (experimental step with reagents)",
    ]
    if cat.description:
        lines.append(f"    - Description: {cat.description}")

    if cat.source_entity_roles:
        roles = [_format_entity_role(r, id_map) for r in cat.source_entity_roles]
        lines.append(f"    - Source Entity Roles: {'; '.join(roles)}")

    if cat.target_entity_roles:
        roles = [_format_entity_role(r, id_map) for r in cat.target_entity_roles]
        lines.append(f"    - Target Entity Roles: {'; '.join(roles)}")

    if cat.source_reagent_roles:
        roles = [_format_reagent_role(r, id_map) for r in cat.source_reagent_roles]
        lines.append(f"    - Source Reagent Roles: {'; '.join(roles)}")

    if cat.target_reagent_roles:
        roles = [_format_reagent_role(r, id_map) for r in cat.target_reagent_roles]
        lines.append(f"    - Target Reagent Roles: {'; '.join(roles)}")

    return "\n".join(lines)


def _format_natural_event_category(
    cat: ListNaturalEventCategory, id_map: Dict[Any, str]
) -> str:
    """Format a natural event category for LLM consumption."""
    id_map[cat.id] = cat.label

    lines = [
        f"  - **{cat.label}** (AGE label: `{cat.age_name}`)",
        "    - Type: Natural Event (biological/natural process)",
    ]
    if cat.description:
        lines.append(f"    - Description: {cat.description}")

    if cat.source_entity_roles:
        roles = [_format_entity_role(r, id_map) for r in cat.source_entity_roles]
        lines.append(f"    - Source Entity Roles: {'; '.join(roles)}")

    if cat.target_entity_roles:
        roles = [_format_entity_role(r, id_map) for r in cat.target_entity_roles]
        lines.append(f"    - Target Entity Roles: {'; '.join(roles)}")

    return "\n".join(lines)


def _generate_cypher_examples(graph: Graph, id_map: Dict[Any, str]) -> List[str]:
    """Generate example Cypher/AGE queries based on the graph schema."""
    examples = []
    graph_name = graph.name.lower().replace(" ", "_")

    # Basic node query examples
    if graph.entity_categories:
        cat = graph.entity_categories[0]
        examples.append(
            f"-- Find all {cat.label} entities:\n"
            f"SELECT * FROM cypher('{graph_name}', $$ MATCH (n:{cat.age_name}) RETURN n $$) as (n agtype);"
        )

    if graph.structure_categories:
        cat = graph.structure_categories[0]
        examples.append(
            f"-- Find all {cat.identifier} structures:\n"
            f"SELECT * FROM cypher('{graph_name}', $$ MATCH (n:{cat.age_name}) RETURN n $$) as (n agtype);"
        )

    # Relation query examples
    if graph.relation_categories and graph.entity_categories:
        rel = graph.relation_categories[0]
        examples.append(
            f"-- Find entities connected by {rel.label}:\n"
            f"SELECT * FROM cypher('{graph_name}', $$ "
            f"MATCH (a)-[r:{rel.age_name}]->(b) RETURN a, r, b $$) as (a agtype, r agtype, b agtype);"
        )

    # Measurement query examples
    if (
        graph.measurement_categories
        and graph.structure_categories
        and graph.entity_categories
    ):
        meas = graph.measurement_categories[0]
        examples.append(
            f"-- Find measurements of type {meas.label}:\n"
            f"SELECT * FROM cypher('{graph_name}', $$ "
            f"MATCH (s)-[m:{meas.age_name}]->(e) RETURN s, m, e $$) as (s agtype, m agtype, e agtype);"
        )

    # Metric query example
    if graph.metric_categories:
        met = graph.metric_categories[0]
        examples.append(
            f"-- Find metrics of type {met.label}:\n"
            f"SELECT * FROM cypher('{graph_name}', $$ "
            f"MATCH (n:{met.age_name}) RETURN n.value as value $$) as (value agtype);"
        )

    # Path query example
    if graph.entity_categories and len(graph.entity_categories) >= 2:
        cat1 = graph.entity_categories[0]
        cat2 = graph.entity_categories[1] if len(graph.entity_categories) > 1 else cat1
        examples.append(
            f"-- Find paths between {cat1.label} and {cat2.label}:\n"
            f"SELECT * FROM cypher('{graph_name}', $$ "
            f"MATCH p = (a:{cat1.age_name})-[*1..3]->(b:{cat2.age_name}) RETURN p $$) as (p agtype);"
        )

    return examples


def transform_to_llm_format(
    graph: Graph, include_examples: bool = True
) -> GraphSchemaText:
    """
    Transforms a Kraph Graph schema into a text format suitable for LLM processing.

    This formatter creates a structured text representation of the knowledge graph
    schema that helps LLMs understand:
    - What types of nodes exist (entities, structures, metrics, events)
    - What types of edges exist (relations, measurements, structure relations)
    - The constraints on edges (source/target types)
    - Example Cypher/AGE queries

    Args:
        graph: The Graph object containing the schema
        include_examples: Whether to include example Cypher queries

    Returns:
        GraphSchemaText containing the formatted schema text and metadata
    """
    sections = []
    node_types = []
    edge_types = []
    id_map = {}  # Map category IDs to human-readable names

    # Header
    sections.append(f"# Knowledge Graph Schema: {graph.name}")
    if graph.description:
        sections.append(f"\n{graph.description}")
    sections.append("")

    # AGE/Cypher context
    sections.append("## Query Language")
    sections.append("This graph uses Apache AGE (A Graph Extension for PostgreSQL).")
    sections.append("Queries use Cypher syntax wrapped in `cypher()` function calls.")
    sections.append("")

    # Node Types Section
    sections.append("## Node Types (Vertices)")
    sections.append("Nodes in this graph can be of the following types:")
    sections.append("")

    # Entity Categories
    if graph.entity_categories:
        sections.append("### Entities")
        sections.append(
            "Entities represent real-world objects or concepts being studied:"
        )
        for cat in graph.entity_categories:
            sections.append(_format_entity_category(cat, id_map))
            node_types.append(f"Entity:{cat.label}")
        sections.append("")

    # Structure Categories
    if graph.structure_categories:
        sections.append("### Structures")
        sections.append(
            "Structures are references to external data (images, files, etc.):"
        )
        for cat in graph.structure_categories:
            sections.append(_format_structure_category(cat, id_map))
            node_types.append(f"Structure:{cat.identifier}")
        sections.append("")

    # Metric Categories
    if graph.metric_categories:
        sections.append("### Metrics")
        sections.append("Metrics are measured values attached to entities:")
        for cat in graph.metric_categories:
            sections.append(_format_metric_category(cat, id_map))
            node_types.append(f"Metric:{cat.label}")
        sections.append("")

    # Protocol Event Categories
    if graph.protocol_event_categories:
        sections.append("### Protocol Events")
        sections.append(
            "Protocol events represent experimental steps involving reagents:"
        )
        for cat in graph.protocol_event_categories:
            sections.append(_format_protocol_event_category(cat, id_map))
            node_types.append(f"ProtocolEvent:{cat.label}")
        sections.append("")

    # Natural Event Categories
    if graph.natural_event_categories:
        sections.append("### Natural Events")
        sections.append("Natural events represent biological or natural processes:")
        for cat in graph.natural_event_categories:
            sections.append(_format_natural_event_category(cat, id_map))
            node_types.append(f"NaturalEvent:{cat.label}")
        sections.append("")

    # Edge Types Section
    sections.append("## Edge Types (Relationships)")
    sections.append("Edges connect nodes and represent relationships:")
    sections.append("")

    # Relation Categories
    if graph.relation_categories:
        sections.append("### Relations")
        sections.append("Relations connect entities to other entities:")
        for cat in graph.relation_categories:
            sections.append(_format_relation_category(cat, id_map))
            edge_types.append(f"Relation:{cat.label}")
        sections.append("")

    # Measurement Categories
    if graph.measurement_categories:
        sections.append("### Measurements")
        sections.append("Measurements connect structures to the entities they measure:")
        for cat in graph.measurement_categories:
            sections.append(_format_measurement_category(cat, id_map))
            edge_types.append(f"Measurement:{cat.label}")
        sections.append("")

    # Structure Relation Categories
    if graph.structure_relation_categories:
        sections.append("### Structure Relations")
        sections.append("Structure relations connect structures to other structures:")
        for cat in graph.structure_relation_categories:
            sections.append(_format_structure_relation_category(cat, id_map))
            edge_types.append(f"StructureRelation:{cat.label}")
        sections.append("")

    # Example Queries Section
    cypher_examples = []
    if include_examples:
        cypher_examples = _generate_cypher_examples(graph, id_map)
        if cypher_examples:
            sections.append("## Example Cypher/AGE Queries")
            sections.append("Here are example queries for this graph:")
            sections.append("")
            sections.append("```sql")
            sections.append("\n\n".join(cypher_examples))
            sections.append("```")
            sections.append("")

    # Query Tips
    sections.append("## Query Construction Tips")
    sections.append(
        "- Use the AGE label names (shown in backticks) for node/edge matching"
    )
    sections.append("- Node properties can be accessed with dot notation: `n.property`")
    sections.append("- Common properties: `id`, `label`, `value` (for metrics)")
    sections.append("- Use `[*1..N]` for variable-length paths")
    sections.append("- Filter with WHERE clauses: `WHERE n.label = 'value'`")
    sections.append("- Aggregate with functions: `count()`, `avg()`, `collect()`")
    sections.append("")

    full_text = "\n".join(sections)

    return GraphSchemaText(
        graph_name=graph.name,
        graph_description=graph.description,
        full_text=full_text,
        node_types=node_types,
        edge_types=edge_types,
        cypher_examples=cypher_examples,
    )


def format_graph_for_query_generation(
    graph: Graph, user_question: str, max_examples: int = 3
) -> str:
    """
    Creates a prompt-ready text that combines the graph schema with a user question.

    This is designed to be used as context for an LLM to generate Cypher queries.

    Args:
        graph: The Graph object containing the schema
        user_question: The natural language question from the user
        max_examples: Maximum number of example queries to include

    Returns:
        A formatted string ready to be used as LLM context
    """
    schema_text = transform_to_llm_format(graph, include_examples=True)

    prompt = f"""You are a knowledge graph query assistant. Given the following graph schema and a user question, generate a valid Apache AGE Cypher query.

{schema_text.full_text}

## User Question
{user_question}

## Instructions
Generate a Cypher query that answers the user's question. The query should:
1. Use the correct AGE label names from the schema
2. Be wrapped in the cypher() function for PostgreSQL
3. Include appropriate RETURN clause with column aliases
4. Use WHERE clauses for filtering if needed

## Your Query
"""
    return prompt


def get_schema_summary(graph: Graph) -> str:
    """
    Returns a brief summary of the graph schema.

    Useful for quick context or when full schema would be too verbose.
    """
    summary_parts = [f"Graph: {graph.name}"]

    if graph.description:
        summary_parts.append(f"Description: {graph.description}")

    node_counts = []
    if graph.entity_categories:
        node_counts.append(f"{len(graph.entity_categories)} entity types")
    if graph.structure_categories:
        node_counts.append(f"{len(graph.structure_categories)} structure types")
    if graph.metric_categories:
        node_counts.append(f"{len(graph.metric_categories)} metric types")
    if graph.protocol_event_categories:
        node_counts.append(
            f"{len(graph.protocol_event_categories)} protocol event types"
        )
    if graph.natural_event_categories:
        node_counts.append(f"{len(graph.natural_event_categories)} natural event types")

    edge_counts = []
    if graph.relation_categories:
        edge_counts.append(f"{len(graph.relation_categories)} relation types")
    if graph.measurement_categories:
        edge_counts.append(f"{len(graph.measurement_categories)} measurement types")
    if graph.structure_relation_categories:
        edge_counts.append(
            f"{len(graph.structure_relation_categories)} structure relation types"
        )

    if node_counts:
        summary_parts.append(f"Nodes: {', '.join(node_counts)}")
    if edge_counts:
        summary_parts.append(f"Edges: {', '.join(edge_counts)}")

    return " | ".join(summary_parts)
