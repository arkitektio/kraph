import pytest
from kraph.api.schema import create_graph
from .conftest import DeployedKraph


@pytest.mark.integration
def test_create_graph(deployed_app: DeployedKraph) -> None:
    """Test the creation of a graph."""
    t = create_graph(name="Christians GOLD GRAPH", description="A graph for Christians masterlist")
    assert t.description == "A graph for Christians masterlist"
