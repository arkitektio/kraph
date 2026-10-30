"""Integration tests against a deployed kraph.

These exercise the two halves the rewrite separated: declaring a **view** (a graph and the
categories that say what its words mean) and recording a **claim** (which names a word and no
graph at all).
"""

import uuid

import pytest

from kraph.api.schema import Cardinality, MetricValueInput, StructureDescriptorInput, ValueKind
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


def _value(object: str, value: float, *, source: uuid.UUID | None = None) -> MetricValueInput:
    return MetricValueInput(identifier="@mikro/annotation", object=object, key="area", value=value, value_kind=ValueKind.FLOAT, uuid=source)


@pytest.mark.integration
def test_many_values_about_many_data_are_one_act(kraph: Kraph) -> None:
    """One assertion covers the batch; the structures are created by the write that needed them."""
    asserted = kraph.assert_metric_values(metrics=[_value("batch-1", 2.0), _value("batch-2", 3.0)])

    assert asserted.recorded == 2
    assert asserted.assertion is not None and asserted.assertion.seq > 0
    assert [metric.value for metric in asserted.metrics] == [2.0, 3.0]


@pytest.mark.integration
def test_a_metric_that_names_its_uuid_is_recorded_once(kraph: Kraph) -> None:
    """A retry with the same uuid reports the metric on the record and makes no act."""
    source = uuid.uuid4()
    first = kraph.assert_metric_values(metrics=[_value("retried", 2.0, source=source)])
    again = kraph.assert_metric_values(metrics=[_value("retried", 2.0, source=source)])

    assert (first.recorded, again.recorded) == (1, 0)
    assert again.assertion is None
    assert again.metrics[0].id == first.metrics[0].id


@pytest.mark.integration
def test_rerunning_without_a_uuid_is_a_second_measurement(kraph: Kraph) -> None:
    first = kraph.assert_metric_values(metrics=[_value("rerun", 2.0)])
    second = kraph.assert_metric_values(metrics=[_value("rerun", 2.0)])

    assert second.recorded == 1
    assert second.metrics[0].id != first.metrics[0].id
