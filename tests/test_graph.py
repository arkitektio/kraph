"""Integration tests against a deployed kraph.

These exercise the two halves the rewrite separated: declaring a **view** (a graph and the
categories that say what its words mean) and recording a **claim** (which names a word and no
graph at all).
"""

import pytest

from kraph.api.schema import Cardinality, StructureDescriptorInput
from kraph.kraph import Kraph


@pytest.mark.integration
def test_create_graph(kraph: Kraph) -> None:
    """A graph is a view; creating one records no claim."""
    t = kraph.create_graph(
        name="Christians GOLD GRAPH",
        description="A graph for Christians masterlist",
        backfill=False,
    )
    assert t.description == "A graph for Christians masterlist"


@pytest.mark.integration
def test_create_structure_relation_category(kraph: Kraph) -> None:
    """Structure kinds are referenced by identifier, not created.

    There is no ``createStructureCategory`` any more: a ``StructureKind`` is minted by the first
    write that names it, so a descriptor just points at the identifier.
    """
    graph = kraph.create_graph(name="Image Masking Example", backfill=False)

    images = StructureDescriptorInput(identifiers=["@mikro/image"])
    category = kraph.create_structure_relation_category(
        key="is_mask_for",
        ontology_references=[],
        properties=[],
        source=images,
        target=images,
        cardinality=Cardinality.ONE_TO_ONE,
        graph=graph.id,
    )
    assert category.key == "is_mask_for"


@pytest.mark.integration
def test_claim_names_a_word_not_a_graph(kraph: Kraph) -> None:
    """A claim names a term. A view that declares that word then draws it."""
    graph = kraph.create_graph(name="Evidence smoke", backfill=False)
    kraph.create_entity_category(
        key="Neuron",
        ontology_references=[],
        property_definitions=[],
        graph=graph.id,
        backfill=True,
    )

    asserted = kraph.assert_entity_exists(
        term="Neuron", supporting_evidence=[], derived_from=[], same_as=[]
    )

    assert asserted.assertion.seq > 0
    assert asserted.instance.kind.value == "ENTITY"
    # The view declares the word, so it draws the claim.
    assert asserted.is_drawn
    assert asserted.drawn_in(graph) is not None


@pytest.mark.integration
def test_claim_under_an_undeclared_word_still_succeeds(kraph: Kraph) -> None:
    """``drawings == []`` is an ordinary answer, not an error.

    A claim names a word the organization owns; a view that declares no category for it simply
    does not draw it. The write still succeeds and is still addressable.
    """
    asserted = kraph.assert_entity_exists(
        term="AWordNoViewDeclares", supporting_evidence=[], derived_from=[], same_as=[]
    )

    assert asserted.assertion.seq > 0
    assert asserted.is_drawn is False
    assert list(asserted.drawings) == []


@pytest.mark.integration
def test_retraction_records_a_position_rather_than_deleting(
    kraph: Kraph,
) -> None:
    """Retracting is evidence, not deletion — and both positions survive."""
    asserted = kraph.assert_entity_exists(
        term="Neuron", supporting_evidence=[], derived_from=[], same_as=[]
    )
    kraph.retract_entity(id=asserted.instance.id)

    standings = kraph.get_standings(id=asserted.instance.id)
    # Newest first, and the retraction did not remove anything.
    assert standings[0].stands is False
