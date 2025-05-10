import pytest
from kraph.api.schema import create_graph


@pytest.mark.integration
def test_create_graph(deployed_app) -> None:
    """Test the creation of a graph."""
    with deployed_app.kraph_watcher:
        t = create_graph(
            name="Christians GOLD GRAPH", description="A graph for Christians masterlist"
        )
        assert t.description == "A graph for Christians masterlist"
