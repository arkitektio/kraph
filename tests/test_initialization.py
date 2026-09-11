"""Lightweight initialization tests that need no deployed stack.

These carry no ``integration`` marker, so they run on every OS in the CI matrix, exercising pure
Python construction of the client and the generated models without touching the network or
Docker.

They double as the regression guard for the two things that silently break a regeneration: the
traits failing to attach, and the two ``valueKind`` enums being conflated.
"""

import kraph.api.schema as schema
from kraph.api.schema import (
    GraphFilter,
    InstanceKind,
    LinkKind,
    OffsetPaginationInput,
    PropertyType,
    TermKind,
    ValueKind,
)
from kraph.kraph import Kraph
from kraph.traits import AssertedTrait, GraphTrait, HasDrawings, InstanceTrait, StructureTrait


def test_kraph_importable() -> None:
    """The top-level ``Kraph`` composition imports and is a class."""
    assert isinstance(Kraph, type)


def test_instance_kind_values() -> None:
    """Instances are entities or one of the two event kinds — nothing else."""
    assert {k.value for k in InstanceKind} == {"ENTITY", "NATURAL_EVENT", "PROTOCOL_EVENT"}


def test_link_kind_has_ten_members() -> None:
    """The ten things one claim can say about two others."""
    assert {k.value for k in LinkKind} == {
        "INFORMS",
        "RELATION",
        "STRUCTURE_RELATION",
        "MEASUREMENT",
        "PARTICIPATES_AS_INPUT",
        "PARTICIPATES_AS_OUTPUT",
        "CLASSIFIES",
        "SAME_AS",
        "DIFFERENT_FROM",
        "DERIVED_FROM",
    }


def test_term_kind_no_longer_carries_reagent() -> None:
    """``REAGENT`` left the term kinds with the evidence-log rewrite; nothing mints one."""
    assert not hasattr(TermKind, "REAGENT")


def test_write_and_schema_value_kinds_are_different_enums() -> None:
    """``valueKind`` means two different things depending on direction.

    Writes take :class:`PropertyType`; schema property definitions take :class:`ValueKind`. The
    members do not line up — ``INTEGER`` versus ``INT`` — and ``CATEGORY`` exists only on the
    schema side. Conflating them records a metric the property definition never sees.
    """
    assert PropertyType.INTEGER.value == "INTEGER"
    assert ValueKind.INT.value == "INT"
    assert "CATEGORY" in {k.value for k in ValueKind}
    assert "CATEGORY" not in {k.value for k in PropertyType}


def test_offset_pagination_input_constructs() -> None:
    """``OffsetPaginationInput`` builds from plain values."""
    pagination = OffsetPaginationInput(offset=0, limit=10)
    assert pagination.offset == 0
    assert pagination.limit == 10


def test_graph_filter_defaults_to_empty() -> None:
    """``GraphFilter`` is fully optional and constructs with no arguments."""
    assert GraphFilter().model_dump(exclude_none=True) == {}


def test_traits_attached_to_generated_models() -> None:
    """The regeneration hazard: codegen stays green when a trait attaches to nothing."""
    assert issubclass(schema.Instance, InstanceTrait)
    assert issubclass(schema.Structure, StructureTrait)
    assert issubclass(schema.Graph, GraphTrait)


def test_only_the_right_payloads_report_drawings() -> None:
    """Seven of the fourteen write payloads carry ``drawings``; seven genuinely do not.

    A measurement or a structure has no vertex to draw, so the field is absent rather than
    empty — and selecting it would be a validation error.
    """
    for name in ("AssertedEntity", "AssertedLinks", "AssertedInstances"):
        assert issubclass(getattr(schema, name), HasDrawings), name
    for name in ("AssertedMetric", "AssertedStructure", "AssertedMeasurement"):
        payload = getattr(schema, name)
        assert issubclass(payload, AssertedTrait), name
        assert not issubclass(payload, HasDrawings), name


def test_write_surface_is_assertion_shaped() -> None:
    """Writes are assert/attest/retract, and the old create* verbs are gone."""
    for gone in (
        "create_entity",
        "create_relation",
        "create_measurement",
        "create_structure",
        # The get-or-create and in-place update verbs went the same way: a
        # structure is asserted, attested or retracted, never ensured or updated.
        "ensure_structure",
        "update_structure",
        "update_relation",
        "update_structure_relation",
        "link_structure_to_entity",
    ):
        assert not hasattr(schema, gone), gone
    for present in ("assert_entity_exists", "retract_entity", "attest_entity", "attest_structure"):
        assert hasattr(schema, present), present
