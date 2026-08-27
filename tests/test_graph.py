"""Integration tests against a deployed kraph.

These exercise the two halves the rewrite separated: declaring a **view** (a graph and the
categories that say what its words mean) and recording a **claim** (which names a word and no
graph at all).
"""

import pytest

from kraph.api.schema import (
    CreateEntityCategoryInput,
    CreateGraphInput,
    EntityDescriptorInput,
    StructureDescriptorInput,
    assert_entity_exists,
    create_entity_category,
    create_graph,
    create_structure_relation_category,
    get_standings,
    retract_entity,
)

from .conftest import DeployedKraph


@pytest.mark.integration
def test_create_graph(deployed_app: DeployedKraph) -> None:
    """A graph is a view; creating one records no claim."""
    t = create_graph(
        input=CreateGraphInput(
            name="Christians GOLD GRAPH",
            description="A graph for Christians masterlist",
        )
    )
    assert t.description == "A graph for Christians masterlist"


@pytest.mark.integration
def test_create_structure_relation_category(deployed_app: DeployedKraph) -> None:
    """Structure kinds are referenced by identifier, not created.

    There is no ``createStructureCategory`` any more: a ``StructureKind`` is minted by the first
    write that names it, so a descriptor just points at the identifier.
    """
    graph = create_graph(input=CreateGraphInput(name="Image Masking Example"))

    images = StructureDescriptorInput(identifiers=["@mikro/image"])
    category = create_structure_relation_category(
        input={
            "key": "is_mask_for",
            "source": images,
            "target": images,
            "graph": graph.id,
        }
    )
    assert category.key == "is_mask_for"


@pytest.mark.integration
def test_claim_names_a_word_not_a_graph(deployed_app: DeployedKraph) -> None:
    """A claim names a term. A view that declares that word then draws it."""
    graph = create_graph(input=CreateGraphInput(name="Evidence smoke"))
    create_entity_category(
        input=CreateEntityCategoryInput(key="Neuron", graph=graph.id, backfill=True)
    )

    asserted = assert_entity_exists(input={"term": "Neuron"})

    assert asserted.assertion.seq > 0
    assert asserted.instance.kind.value == "ENTITY"
    # The view declares the word, so it draws the claim.
    assert asserted.is_drawn
    assert asserted.drawn_in(graph) is not None


@pytest.mark.integration
def test_claim_under_an_undeclared_word_still_succeeds(deployed_app: DeployedKraph) -> None:
    """``drawings == []`` is an ordinary answer, not an error.

    A claim names a word the organization owns; a view that declares no category for it simply
    does not draw it. The write still succeeds and is still addressable.
    """
    asserted = assert_entity_exists(input={"term": "AWordNoViewDeclares"})

    assert asserted.assertion.seq > 0
    assert asserted.is_drawn is False
    assert asserted.drawings == []


@pytest.mark.integration
def test_retraction_records_a_position_rather_than_deleting(
    deployed_app: DeployedKraph,
) -> None:
    """Retracting is evidence, not deletion — and both positions survive."""
    asserted = assert_entity_exists(input={"term": "Neuron"})
    retract_entity(input={"id": asserted.instance.id})

    standings = get_standings(id=asserted.instance.id)
    # Newest first, and the retraction did not remove anything.
    assert standings[0].stands is False
