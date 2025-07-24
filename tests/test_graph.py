import pytest
from kraph.api.schema import (
    create_graph,
    create_structure_relation_category,
    create_structure_category,
)
from .conftest import DeployedKraph


@pytest.mark.integration
def test_create_graph(deployed_app: DeployedKraph) -> None:
    """Test the creation of a graph."""
    t = create_graph(name="Christians GOLD GRAPH", description="A graph for Christians masterlist")
    assert t.description == "A graph for Christians masterlist"


@pytest.mark.integration
def test_create_structure_category(deployed_app: DeployedKraph) -> None:
    """Test the creation of a structure category."""
    graph = create_graph("Image Masking Example")

    image_s = create_structure_category(
        graph, "@mikro/image", description="An image structure category"
    )

    IS_MASK_FOR = create_structure_relation_category(
        graph, "is_mask_for", source_definition=image_s, target_definition=image_s
    )
