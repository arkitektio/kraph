import builtins
from datetime import datetime
from enum import Enum
from kraph.scalars import (
    StructureIdentifier,
    StructureIdentifierCoercible,
    StructureObject,
    StructureObjectCoercible,
)
from kraph.traits import (
    AssertedTrait,
    AssertionTrait,
    CategoryTrait,
    EntityCategoryTrait,
    EntityTrait,
    GraphTrait,
    HasDrawings,
    HasPresignedDownloadAccessor,
    InstanceTrait,
    LinkTrait,
    MeasurementCategoryTrait,
    MetricKindTrait,
    MetricTrait,
    NaturalEventCategoryTrait,
    NodeTrait,
    ProjectionTrait,
    ProtocolEventCategoryTrait,
    RelationCategoryTrait,
    StandingTrait,
    StructureKindTrait,
    StructureRelationCategoryTrait,
    StructureTrait,
    TermTrait,
)
from pydantic import AliasChoices, BaseModel, ConfigDict, Field
from rath.scalars import ID, IDCoercible
from rath.task import TaskLike
from typing import Annotated, Any, Iterable, Literal


class GraphQLDefault:
    """Records a GraphQL field schema default value. The client omits the field so the server applies its own default; this preserves the value for introspection."""

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "GraphQLDefault(" + repr(self.value) + ")"


class UnsetType:
    """Sentinel for arguments the caller did not provide. Such fields are omitted on serialization so the GraphQL server applies its own default."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __repr__(self):
        return "UNSET"

    def __bool__(self):
        return False


UNSET = UnsetType()


class AggregationFunction(str, Enum):
    """No documentation"""

    MEAN = "MEAN"
    SUM = "SUM"
    MAX = "MAX"
    MIN = "MIN"
    COUNT = "COUNT"
    RANGE = "RANGE"
    EUCLIDEAN_RANGE = "EUCLIDEAN_RANGE"
    LATEST = "LATEST"
    __str__ = str.__str__


class Cardinality(str, Enum):
    """No documentation"""

    ONE_TO_ONE = "ONE_TO_ONE"
    ONE_TO_MANY = "ONE_TO_MANY"
    MANY_TO_ONE = "MANY_TO_ONE"
    __str__ = str.__str__


class ClaimField(str, Enum):
    """No documentation"""

    WORD = "WORD"
    SUBJECT = "SUBJECT"
    APP = "APP"
    ACTION = "ACTION"
    KIND = "KIND"
    KEY = "KEY"
    ASSERTED_AT = "ASSERTED_AT"
    OBSERVED_AT = "OBSERVED_AT"
    CONFIDENCE = "CONFIDENCE"
    __str__ = str.__str__


class ClaimOperator(str, Enum):
    """No documentation"""

    IS = "IS"
    IN = "IN"
    NOT_IN = "NOT_IN"
    BEFORE = "BEFORE"
    SINCE = "SINCE"
    AT_LEAST = "AT_LEAST"
    BELOW = "BELOW"
    __str__ = str.__str__


class DerivationType(str, Enum):
    """No documentation"""

    LATEST = "LATEST"
    PRIORITY_LATEST = "PRIORITY_LATEST"
    ROLLUP = "ROLLUP"
    LATEST_ASSERTION_TOOL = "LATEST_ASSERTION_TOOL"
    __str__ = str.__str__


class DescendantKind(str, Enum):
    """The kind of a comment descendant — how one node of the rich-text tree renders"""

    LEAF = "LEAF"
    MENTION = "MENTION"
    PARAGRAPH = "PARAGRAPH"
    __str__ = str.__str__


class EventKind(str, Enum):
    """No documentation"""

    INTRINSIC = "INTRINSIC"
    EXTRINSIC = "EXTRINSIC"
    __str__ = str.__str__


class InstanceKind(str, Enum):
    """No documentation"""

    ENTITY = "ENTITY"
    NATURAL_EVENT = "NATURAL_EVENT"
    PROTOCOL_EVENT = "PROTOCOL_EVENT"
    __str__ = str.__str__


class LinkKind(str, Enum):
    """No documentation"""

    INFORMS = "INFORMS"
    RELATION = "RELATION"
    STRUCTURE_RELATION = "STRUCTURE_RELATION"
    MEASUREMENT = "MEASUREMENT"
    PARTICIPATES_AS_INPUT = "PARTICIPATES_AS_INPUT"
    PARTICIPATES_AS_OUTPUT = "PARTICIPATES_AS_OUTPUT"
    CLASSIFIES = "CLASSIFIES"
    SAME_AS = "SAME_AS"
    DIFFERENT_FROM = "DIFFERENT_FROM"
    DERIVED_FROM = "DERIVED_FROM"
    __str__ = str.__str__


class Ordering(str, Enum):
    """No documentation"""

    ASC = "ASC"
    ASC_NULLS_FIRST = "ASC_NULLS_FIRST"
    ASC_NULLS_LAST = "ASC_NULLS_LAST"
    DESC = "DESC"
    DESC_NULLS_FIRST = "DESC_NULLS_FIRST"
    DESC_NULLS_LAST = "DESC_NULLS_LAST"
    __str__ = str.__str__


class ProjectionStatus(str, Enum):
    """Whether a view's drawing reflects the log, has never been drawn, or is mid-replay"""

    CONSISTENT = "CONSISTENT"
    NEEDS_BACKFILL = "NEEDS_BACKFILL"
    REBUILDING = "REBUILDING"
    __str__ = str.__str__


class PropertyType(str, Enum):
    """No documentation"""

    STRING = "STRING"
    FLOAT = "FLOAT"
    INTEGER = "INTEGER"
    BOOLEAN = "BOOLEAN"
    DATETIME = "DATETIME"
    POINT_3D = "POINT_3D"
    __str__ = str.__str__


class TermKind(str, Enum):
    """No documentation"""

    ENTITY = "ENTITY"
    NATURAL_EVENT = "NATURAL_EVENT"
    PROTOCOL_EVENT = "PROTOCOL_EVENT"
    MEASUREMENT = "MEASUREMENT"
    RELATION = "RELATION"
    STRUCTURE_RELATION = "STRUCTURE_RELATION"
    __str__ = str.__str__


class ValueKind(str, Enum):
    """No documentation"""

    INT = "INT"
    FLOAT = "FLOAT"
    DATETIME = "DATETIME"
    STRING = "STRING"
    CATEGORY = "CATEGORY"
    BOOLEAN = "BOOLEAN"
    THREE_D_VECTOR = "THREE_D_VECTOR"
    TWO_D_VECTOR = "TWO_D_VECTOR"
    ONE_D_VECTOR = "ONE_D_VECTOR"
    FOUR_D_VECTOR = "FOUR_D_VECTOR"
    N_VECTOR = "N_VECTOR"
    __str__ = str.__str__


class WhereOperator(str, Enum):
    """No documentation"""

    EQUALS = "EQUALS"
    NOT_EQUALS = "NOT_EQUALS"
    GREATER_THAN = "GREATER_THAN"
    LESS_THAN = "LESS_THAN"
    GREATER_OR_EQUAL = "GREATER_OR_EQUAL"
    LESS_OR_EQUAL = "LESS_OR_EQUAL"
    IN = "IN"
    NOT_IN = "NOT_IN"
    CONTAINS = "CONTAINS"
    STARTS_WITH = "STARTS_WITH"
    ENDS_WITH = "ENDS_WITH"
    __str__ = str.__str__


class ArchiveGraphInput(BaseModel):
    """Input for archiving a graph"""

    id: str = Field(description="The ID of the graph to archive")
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class AssertEntityExistsInput(BaseModel):
    """Input for creating a new entity"""

    term: str = Field(
        description="The organization's word for what is being claimed — a term's `key`, e.g. 'AIS'. Not a category id and not a graph: a claim names a word, and every view that declares that word will hold what you write. The word is created if the organization has not used it before; a view that declares no category for it simply will not draw it."
    )
    supporting_evidence: Annotated[
        tuple["StructureReferenceInput", ...] | None, GraphQLDefault("[]")
    ] = Field(
        validation_alias=AliasChoices("supporting_evidence", "supportingEvidence"),
        serialization_alias="supportingEvidence",
        default=None,
        description="List of evidence structures with measurements",
    )
    "List of evidence structures with measurements\nDefault: []"
    observed_at: datetime | None = Field(
        validation_alias=AliasChoices("observed_at", "observedAt"),
        serialization_alias="observedAt",
        default=None,
        description="When the world was in this state — world time, the axis a scientist means by 'when'. Distinct from when it is claimed, which the assertion records; left unset, the two are equal. A point, not an interval: a duration is a metric.",
    )
    confidence: float | None = Field(
        default=None,
        description="How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.",
    )
    derived_from: Annotated[tuple[str, ...] | None, GraphQLDefault("[]")] = Field(
        validation_alias=AliasChoices("derived_from", "derivedFrom"),
        serialization_alias="derivedFrom",
        default=None,
        description='The claims this one came from — ids of instances, links, metrics or structures in your organization. Each is recorded as a DERIVED_FROM link under the same assertion as the claim itself, because "this, because of that" is one act (RFC 0017). Read back as `derivedFrom`; the cited claim lists it under `derivations`.',
    )
    'The claims this one came from — ids of instances, links, metrics or structures in your organization. Each is recorded as a DERIVED_FROM link under the same assertion as the claim itself, because "this, because of that" is one act (RFC 0017). Read back as `derivedFrom`; the cited claim lists it under `derivations`.\nDefault: []'
    same_as: Annotated[tuple[str, ...] | None, GraphQLDefault("[]")] = Field(
        validation_alias=AliasChoices("same_as", "sameAs"),
        serialization_alias="sameAs",
        default=None,
        description='Instances this new one is the same as. Saying "this is AIS 6" mints a fresh instance and claims it is the same as the one already known as AIS 6 — all under **one assertion**, because it is one act. Sameness is an equivalence with no primary, so which id you send is immaterial; entities only, never structures.',
    )
    'Instances this new one is the same as. Saying "this is AIS 6" mints a fresh instance and claims it is the same as the one already known as AIS 6 — all under **one assertion**, because it is one act. Sameness is an equivalence with no primary, so which id you send is immaterial; entities only, never structures.\nDefault: []'
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class AssertMeasurementExistsInput(BaseModel):
    """Input for creating a new measurement edge"""

    source_id: str = Field(
        validation_alias=AliasChoices("source_id", "sourceId"),
        serialization_alias="sourceId",
        description="The ID of the source entity/structure",
    )
    target_id: str = Field(
        validation_alias=AliasChoices("target_id", "targetId"),
        serialization_alias="targetId",
        description="The ID of the target entity/structure",
    )
    supporting_evidence: Annotated[
        tuple["StructureReferenceInput", ...] | None, GraphQLDefault("[]")
    ] = Field(
        validation_alias=AliasChoices("supporting_evidence", "supportingEvidence"),
        serialization_alias="supportingEvidence",
        default=None,
        description="List of evidence structures with measurements",
    )
    "List of evidence structures with measurements\nDefault: []"
    observed_at: datetime | None = Field(
        validation_alias=AliasChoices("observed_at", "observedAt"),
        serialization_alias="observedAt",
        default=None,
        description="When the world was in this state — world time, the axis a scientist means by 'when'. Distinct from when it is claimed, which the assertion records; left unset, the two are equal. A point, not an interval: a duration is a metric.",
    )
    confidence: float | None = Field(
        default=None,
        description="How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.",
    )
    derived_from: Annotated[tuple[str, ...] | None, GraphQLDefault("[]")] = Field(
        validation_alias=AliasChoices("derived_from", "derivedFrom"),
        serialization_alias="derivedFrom",
        default=None,
        description='The claims this one came from — ids of instances, links, metrics or structures in your organization. Each is recorded as a DERIVED_FROM link under the same assertion as the claim itself, because "this, because of that" is one act (RFC 0017). Read back as `derivedFrom`; the cited claim lists it under `derivations`.',
    )
    'The claims this one came from — ids of instances, links, metrics or structures in your organization. Each is recorded as a DERIVED_FROM link under the same assertion as the claim itself, because "this, because of that" is one act (RFC 0017). Read back as `derivedFrom`; the cited claim lists it under `derivations`.\nDefault: []'
    term: str = Field(
        description="The organization's word for what is being claimed — a term's `key`, e.g. 'AIS'. Not a category id and not a graph: a claim names a word, and every view that declares that word will hold what you write. The word is created if the organization has not used it before; a view that declares no category for it simply will not draw it."
    )
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class AssertMetricValueForStructureInput(BaseModel):
    """Input for creating a new metric"""

    key: str
    value: Any
    value_kind: PropertyType = Field(
        validation_alias=AliasChoices("value_kind", "valueKind"),
        serialization_alias="valueKind",
        description="What type of value this is. Required: it decides which column the value is stored in and which measurement term it is recorded under, and nothing infers it. Two callers may declare the same key differently — a float `confidence` and a category-label `confidence` are two terms, and both are recorded.",
    )
    confidence: float | None = Field(
        default=None,
        description="How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.",
    )
    confidence_type: str | None = Field(
        validation_alias=AliasChoices("confidence_type", "confidenceType"),
        serialization_alias="confidenceType",
        default=None,
        description="What kind of number `confidence` is — a method's own score, a p-value. Measurement-only",
    )
    unit: str | None = None
    observed_at: datetime | None = Field(
        validation_alias=AliasChoices("observed_at", "observedAt"),
        serialization_alias="observedAt",
        default=None,
        description="When the world was observed. Defaults to when it was claimed.",
    )
    derived_from: Annotated[tuple[str, ...] | None, GraphQLDefault("[]")] = Field(
        validation_alias=AliasChoices("derived_from", "derivedFrom"),
        serialization_alias="derivedFrom",
        default=None,
        description='The claims this one came from — ids of instances, links, metrics or structures in your organization. Each is recorded as a DERIVED_FROM link under the same assertion as the claim itself, because "this, because of that" is one act (RFC 0017). Read back as `derivedFrom`; the cited claim lists it under `derivations`.',
    )
    'The claims this one came from — ids of instances, links, metrics or structures in your organization. Each is recorded as a DERIVED_FROM link under the same assertion as the claim itself, because "this, because of that" is one act (RFC 0017). Read back as `derivedFrom`; the cited claim lists it under `derivations`.\nDefault: []'
    structure: ID = Field(
        description="The unique ID of the structure this metric is associated with"
    )
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class AssertMetricValueInput(BaseModel):
    """Input for creating a new metric"""

    key: str
    value: Any
    value_kind: PropertyType = Field(
        validation_alias=AliasChoices("value_kind", "valueKind"),
        serialization_alias="valueKind",
        description="What type of value this is. Required: it decides which column the value is stored in and which measurement term it is recorded under, and nothing infers it. Two callers may declare the same key differently — a float `confidence` and a category-label `confidence` are two terms, and both are recorded.",
    )
    confidence: float | None = Field(
        default=None,
        description="How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.",
    )
    confidence_type: str | None = Field(
        validation_alias=AliasChoices("confidence_type", "confidenceType"),
        serialization_alias="confidenceType",
        default=None,
        description="What kind of number `confidence` is — a method's own score, a p-value. Measurement-only",
    )
    unit: str | None = None
    observed_at: datetime | None = Field(
        validation_alias=AliasChoices("observed_at", "observedAt"),
        serialization_alias="observedAt",
        default=None,
        description="When the world was observed. Defaults to when it was claimed.",
    )
    derived_from: Annotated[tuple[str, ...] | None, GraphQLDefault("[]")] = Field(
        validation_alias=AliasChoices("derived_from", "derivedFrom"),
        serialization_alias="derivedFrom",
        default=None,
        description='The claims this one came from — ids of instances, links, metrics or structures in your organization. Each is recorded as a DERIVED_FROM link under the same assertion as the claim itself, because "this, because of that" is one act (RFC 0017). Read back as `derivedFrom`; the cited claim lists it under `derivations`.',
    )
    'The claims this one came from — ids of instances, links, metrics or structures in your organization. Each is recorded as a DERIVED_FROM link under the same assertion as the claim itself, because "this, because of that" is one act (RFC 0017). Read back as `derivedFrom`; the cited claim lists it under `derivations`.\nDefault: []'
    identifier: str = Field(
        description="The schema identifier for this metric (e.g. '@mikro/roi_volume')"
    )
    object: str = Field(
        description="The unique ID of the object this metric references"
    )
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class AssertNaturalEventExistsInput(BaseModel):
    """Input for creating a new natural event instance"""

    term: str = Field(
        description="The organization's word for what is being claimed — a term's `key`, e.g. 'AIS'. Not a category id and not a graph: a claim names a word, and every view that declares that word will hold what you write. The word is created if the organization has not used it before; a view that declares no category for it simply will not draw it."
    )
    inputs: Annotated[
        tuple["RoleMappingInput", ...] | None, GraphQLDefault("[]")
    ] = Field(
        default=None, description="List of entity IDs that are inputs to this event"
    )
    "List of entity IDs that are inputs to this event\nDefault: []"
    outputs: Annotated[
        tuple["RoleMappingInput", ...] | None, GraphQLDefault("[]")
    ] = Field(
        default=None, description="List of entity IDs that are outputs of this event"
    )
    "List of entity IDs that are outputs of this event\nDefault: []"
    supporting_evidence: Annotated[
        tuple["StructureReferenceInput", ...] | None, GraphQLDefault("[]")
    ] = Field(
        validation_alias=AliasChoices("supporting_evidence", "supportingEvidence"),
        serialization_alias="supportingEvidence",
        default=None,
        description="List of evidence structures with measurements",
    )
    "List of evidence structures with measurements\nDefault: []"
    observed_at: datetime | None = Field(
        validation_alias=AliasChoices("observed_at", "observedAt"),
        serialization_alias="observedAt",
        default=None,
        description="When the world was in this state — world time, the axis a scientist means by 'when'. Distinct from when it is claimed, which the assertion records; left unset, the two are equal. A point, not an interval: a duration is a metric.",
    )
    confidence: float | None = Field(
        default=None,
        description="How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.",
    )
    derived_from: Annotated[tuple[str, ...] | None, GraphQLDefault("[]")] = Field(
        validation_alias=AliasChoices("derived_from", "derivedFrom"),
        serialization_alias="derivedFrom",
        default=None,
        description='The claims this one came from — ids of instances, links, metrics or structures in your organization. Each is recorded as a DERIVED_FROM link under the same assertion as the claim itself, because "this, because of that" is one act (RFC 0017). Read back as `derivedFrom`; the cited claim lists it under `derivations`.',
    )
    'The claims this one came from — ids of instances, links, metrics or structures in your organization. Each is recorded as a DERIVED_FROM link under the same assertion as the claim itself, because "this, because of that" is one act (RFC 0017). Read back as `derivedFrom`; the cited claim lists it under `derivations`.\nDefault: []'
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class AssertParticipationInput(BaseModel):
    """Input for claiming that an entity took part in an event"""

    event: str = Field(description="The ID of the event the entity took part in")
    entity: str = Field(description="The ID of the entity that took part")
    role: str = Field(
        description="Which role the entity played — the caller's own word; the write names no graph and no category"
    )
    is_input: Annotated[bool | None, GraphQLDefault("True")] = Field(
        validation_alias=AliasChoices("is_input", "isInput"),
        serialization_alias="isInput",
        default=None,
        description="True if the entity went into the event, False if it came out of it",
    )
    "True if the entity went into the event, False if it came out of it\nDefault: True"
    observed_at: datetime | None = Field(
        validation_alias=AliasChoices("observed_at", "observedAt"),
        serialization_alias="observedAt",
        default=None,
        description="When the world was in this state — world time, the axis a scientist means by 'when'. Distinct from when it is claimed, which the assertion records; left unset, the two are equal. A point, not an interval: a duration is a metric.",
    )
    confidence: float | None = Field(
        default=None,
        description="How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.",
    )
    derived_from: Annotated[tuple[str, ...] | None, GraphQLDefault("[]")] = Field(
        validation_alias=AliasChoices("derived_from", "derivedFrom"),
        serialization_alias="derivedFrom",
        default=None,
        description='The claims this one came from — ids of instances, links, metrics or structures in your organization. Each is recorded as a DERIVED_FROM link under the same assertion as the claim itself, because "this, because of that" is one act (RFC 0017). Read back as `derivedFrom`; the cited claim lists it under `derivations`.',
    )
    'The claims this one came from — ids of instances, links, metrics or structures in your organization. Each is recorded as a DERIVED_FROM link under the same assertion as the claim itself, because "this, because of that" is one act (RFC 0017). Read back as `derivedFrom`; the cited claim lists it under `derivations`.\nDefault: []'
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class AssertParticipationsInput(BaseModel):
    """Input for claiming that several entities took part in one event, as one act"""

    event: str = Field(description="The event the entities took part in")
    participants: tuple["ParticipantInput", ...] = Field(
        description="Everyone who took part, and how"
    )
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class AssertProtocolEventExistsInput(BaseModel):
    """Input for creating a new protocol event instance"""

    term: str = Field(
        description="The organization's word for what is being claimed — a term's `key`, e.g. 'AIS'. Not a category id and not a graph: a claim names a word, and every view that declares that word will hold what you write. The word is created if the organization has not used it before; a view that declares no category for it simply will not draw it."
    )
    inputs: Annotated[
        tuple["RoleMappingInput", ...] | None, GraphQLDefault("[]")
    ] = Field(
        default=None, description="List of entity IDs that are inputs to this event"
    )
    "List of entity IDs that are inputs to this event\nDefault: []"
    outputs: Annotated[
        tuple["RoleMappingInput", ...] | None, GraphQLDefault("[]")
    ] = Field(
        default=None, description="List of entity IDs that are outputs of this event"
    )
    "List of entity IDs that are outputs of this event\nDefault: []"
    supporting_evidence: Annotated[
        tuple["StructureReferenceInput", ...] | None, GraphQLDefault("[]")
    ] = Field(
        validation_alias=AliasChoices("supporting_evidence", "supportingEvidence"),
        serialization_alias="supportingEvidence",
        default=None,
        description="List of evidence structures with measurements",
    )
    "List of evidence structures with measurements\nDefault: []"
    observed_at: datetime | None = Field(
        validation_alias=AliasChoices("observed_at", "observedAt"),
        serialization_alias="observedAt",
        default=None,
        description="When the world was in this state — world time, the axis a scientist means by 'when'. Distinct from when it is claimed, which the assertion records; left unset, the two are equal. A point, not an interval: a duration is a metric.",
    )
    confidence: float | None = Field(
        default=None,
        description="How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.",
    )
    derived_from: Annotated[tuple[str, ...] | None, GraphQLDefault("[]")] = Field(
        validation_alias=AliasChoices("derived_from", "derivedFrom"),
        serialization_alias="derivedFrom",
        default=None,
        description='The claims this one came from — ids of instances, links, metrics or structures in your organization. Each is recorded as a DERIVED_FROM link under the same assertion as the claim itself, because "this, because of that" is one act (RFC 0017). Read back as `derivedFrom`; the cited claim lists it under `derivations`.',
    )
    'The claims this one came from — ids of instances, links, metrics or structures in your organization. Each is recorded as a DERIVED_FROM link under the same assertion as the claim itself, because "this, because of that" is one act (RFC 0017). Read back as `derivedFrom`; the cited claim lists it under `derivations`.\nDefault: []'
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class AssertRelationExistsInput(BaseModel):
    """Input for creating a new relation between two entities with supporting evidence"""

    source_id: str = Field(
        validation_alias=AliasChoices("source_id", "sourceId"),
        serialization_alias="sourceId",
        description="The ID of the source entity/structure",
    )
    target_id: str = Field(
        validation_alias=AliasChoices("target_id", "targetId"),
        serialization_alias="targetId",
        description="The ID of the target entity/structure",
    )
    supporting_evidence: Annotated[
        tuple["StructureReferenceInput", ...] | None, GraphQLDefault("[]")
    ] = Field(
        validation_alias=AliasChoices("supporting_evidence", "supportingEvidence"),
        serialization_alias="supportingEvidence",
        default=None,
        description="List of evidence structures with measurements",
    )
    "List of evidence structures with measurements\nDefault: []"
    observed_at: datetime | None = Field(
        validation_alias=AliasChoices("observed_at", "observedAt"),
        serialization_alias="observedAt",
        default=None,
        description="When the world was in this state — world time, the axis a scientist means by 'when'. Distinct from when it is claimed, which the assertion records; left unset, the two are equal. A point, not an interval: a duration is a metric.",
    )
    confidence: float | None = Field(
        default=None,
        description="How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.",
    )
    derived_from: Annotated[tuple[str, ...] | None, GraphQLDefault("[]")] = Field(
        validation_alias=AliasChoices("derived_from", "derivedFrom"),
        serialization_alias="derivedFrom",
        default=None,
        description='The claims this one came from — ids of instances, links, metrics or structures in your organization. Each is recorded as a DERIVED_FROM link under the same assertion as the claim itself, because "this, because of that" is one act (RFC 0017). Read back as `derivedFrom`; the cited claim lists it under `derivations`.',
    )
    'The claims this one came from — ids of instances, links, metrics or structures in your organization. Each is recorded as a DERIVED_FROM link under the same assertion as the claim itself, because "this, because of that" is one act (RFC 0017). Read back as `derivedFrom`; the cited claim lists it under `derivations`.\nDefault: []'
    term: str = Field(
        description="The organization's word for what is being claimed — a term's `key`, e.g. 'AIS'. Not a category id and not a graph: a claim names a word, and every view that declares that word will hold what you write. The word is created if the organization has not used it before; a view that declares no category for it simply will not draw it."
    )
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class AssertSameInstanceInput(BaseModel):
    """Input for claiming that several recorded instances are one thing"""

    instances: tuple[str, ...] = Field(
        description="Two or more instance ids that name the same thing — entities or events alike. Every pair among them is claimed, under one assertion."
    )
    observed_at: datetime | None = Field(
        validation_alias=AliasChoices("observed_at", "observedAt"),
        serialization_alias="observedAt",
        default=None,
        description="When the world was in this state — world time, the axis a scientist means by 'when'. Distinct from when it is claimed, which the assertion records; left unset, the two are equal. A point, not an interval: a duration is a metric.",
    )
    confidence: float | None = Field(
        default=None,
        description="How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.",
    )
    derived_from: Annotated[tuple[str, ...] | None, GraphQLDefault("[]")] = Field(
        validation_alias=AliasChoices("derived_from", "derivedFrom"),
        serialization_alias="derivedFrom",
        default=None,
        description='The claims this one came from — ids of instances, links, metrics or structures in your organization. Each is recorded as a DERIVED_FROM link under the same assertion as the claim itself, because "this, because of that" is one act (RFC 0017). Read back as `derivedFrom`; the cited claim lists it under `derivations`.',
    )
    'The claims this one came from — ids of instances, links, metrics or structures in your organization. Each is recorded as a DERIVED_FROM link under the same assertion as the claim itself, because "this, because of that" is one act (RFC 0017). Read back as `derivedFrom`; the cited claim lists it under `derivations`.\nDefault: []'
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class AssertStructureExistsInput(BaseModel):
    """Input for claiming that an external datum exists"""

    object: str = Field(
        description="The unique ID of the object this structure references"
    )
    metrics: Annotated[tuple["MetricInput", ...] | None, GraphQLDefault("[]")] = Field(
        default=None, description="List of measurements associated with this structure"
    )
    "List of measurements associated with this structure\nDefault: []"
    derived_from: Annotated[tuple[str, ...] | None, GraphQLDefault("[]")] = Field(
        validation_alias=AliasChoices("derived_from", "derivedFrom"),
        serialization_alias="derivedFrom",
        default=None,
        description='The claims this one came from — ids of instances, links, metrics or structures in your organization. Each is recorded as a DERIVED_FROM link under the same assertion as the claim itself, because "this, because of that" is one act (RFC 0017). Read back as `derivedFrom`; the cited claim lists it under `derivations`.',
    )
    'The claims this one came from — ids of instances, links, metrics or structures in your organization. Each is recorded as a DERIVED_FROM link under the same assertion as the claim itself, because "this, because of that" is one act (RFC 0017). Read back as `derivedFrom`; the cited claim lists it under `derivations`.\nDefault: []'
    identifier: str = Field(description="The structure identifier, e.g. '@mikro/roi'")
    observed_at: datetime | None = Field(
        validation_alias=AliasChoices("observed_at", "observedAt"),
        serialization_alias="observedAt",
        default=None,
        description="When the world was in this state — world time, the axis a scientist means by 'when'. Distinct from when it is claimed, which the assertion records; left unset, the two are equal. A point, not an interval: a duration is a metric.",
    )
    confidence: float | None = Field(
        default=None,
        description="How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.",
    )
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class AssertStructureRelationExistsInput(BaseModel):
    """Input for creating a new structure relation"""

    source_id: str = Field(
        validation_alias=AliasChoices("source_id", "sourceId"),
        serialization_alias="sourceId",
        description="The ID of the source entity/structure",
    )
    target_id: str = Field(
        validation_alias=AliasChoices("target_id", "targetId"),
        serialization_alias="targetId",
        description="The ID of the target entity/structure",
    )
    supporting_evidence: Annotated[
        tuple["StructureReferenceInput", ...] | None, GraphQLDefault("[]")
    ] = Field(
        validation_alias=AliasChoices("supporting_evidence", "supportingEvidence"),
        serialization_alias="supportingEvidence",
        default=None,
        description="List of evidence structures with measurements",
    )
    "List of evidence structures with measurements\nDefault: []"
    observed_at: datetime | None = Field(
        validation_alias=AliasChoices("observed_at", "observedAt"),
        serialization_alias="observedAt",
        default=None,
        description="When the world was in this state — world time, the axis a scientist means by 'when'. Distinct from when it is claimed, which the assertion records; left unset, the two are equal. A point, not an interval: a duration is a metric.",
    )
    confidence: float | None = Field(
        default=None,
        description="How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.",
    )
    derived_from: Annotated[tuple[str, ...] | None, GraphQLDefault("[]")] = Field(
        validation_alias=AliasChoices("derived_from", "derivedFrom"),
        serialization_alias="derivedFrom",
        default=None,
        description='The claims this one came from — ids of instances, links, metrics or structures in your organization. Each is recorded as a DERIVED_FROM link under the same assertion as the claim itself, because "this, because of that" is one act (RFC 0017). Read back as `derivedFrom`; the cited claim lists it under `derivations`.',
    )
    'The claims this one came from — ids of instances, links, metrics or structures in your organization. Each is recorded as a DERIVED_FROM link under the same assertion as the claim itself, because "this, because of that" is one act (RFC 0017). Read back as `derivedFrom`; the cited claim lists it under `derivations`.\nDefault: []'
    term: str = Field(
        description="The organization's word for what is being claimed — a term's `key`, e.g. 'AIS'. Not a category id and not a graph: a claim names a word, and every view that declares that word will hold what you write. The word is created if the organization has not used it before; a view that declares no category for it simply will not draw it."
    )
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class AttestCommentInput(BaseModel):
    """Input for claiming a remark stands again — reopening, as new evidence"""

    id: str = Field(description="The ID of the comment to attest")
    at: datetime | None = Field(
        default=None,
        description="When this position took effect — world time. Left unset, the moment of the claim. A rule bounding OBSERVED_AT on EXISTENCE reads this.",
    )
    confidence: float | None = Field(
        default=None,
        description="How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.",
    )
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class AttestEntityInput(BaseModel):
    """Input for claiming that an entity exists"""

    id: str = Field(
        description="The uuid of the node being attested. The same id `retract*` returns, so the two round-trip."
    )
    at: datetime | None = Field(
        default=None,
        description="When this position took effect — world time. Left unset, the moment of the claim. A rule bounding OBSERVED_AT on EXISTENCE reads this.",
    )
    confidence: float | None = Field(
        default=None,
        description="How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.",
    )
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class AttestLinkInput(BaseModel):
    """Input for claiming that a link claim still stands"""

    id: str = Field(
        description="The ID of the claim to attest — its `Link` primary key"
    )
    at: datetime | None = Field(
        default=None,
        description="When this position took effect — world time. Left unset, the moment of the claim. A rule bounding OBSERVED_AT on EXISTENCE reads this.",
    )
    confidence: float | None = Field(
        default=None,
        description="How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.",
    )
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class AttestMetricInput(BaseModel):
    """Input for claiming that a measurement still stands"""

    id: str = Field(
        description="The ID of the metric to attest — a bare uuid, its evidence primary key"
    )
    at: datetime | None = Field(
        default=None,
        description="When this position took effect — world time. Left unset, the moment of the claim. A rule bounding OBSERVED_AT on EXISTENCE reads this.",
    )
    confidence: float | None = Field(
        default=None,
        description="How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.",
    )
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class AttestNaturalEventInput(BaseModel):
    """Input for claiming that a natural event exists"""

    id: str = Field(
        description="The uuid of the node being attested. The same id `retract*` returns, so the two round-trip."
    )
    at: datetime | None = Field(
        default=None,
        description="When this position took effect — world time. Left unset, the moment of the claim. A rule bounding OBSERVED_AT on EXISTENCE reads this.",
    )
    confidence: float | None = Field(
        default=None,
        description="How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.",
    )
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class AttestProtocolEventInput(BaseModel):
    """Input for claiming that a protocol event exists"""

    id: str = Field(
        description="The uuid of the node being attested. The same id `retract*` returns, so the two round-trip."
    )
    at: datetime | None = Field(
        default=None,
        description="When this position took effect — world time. Left unset, the moment of the claim. A rule bounding OBSERVED_AT on EXISTENCE reads this.",
    )
    confidence: float | None = Field(
        default=None,
        description="How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.",
    )
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class AttestStructureInput(BaseModel):
    """Input for claiming that a structure still stands"""

    id: str = Field(
        description="The ID of the structure to attest — a bare uuid, its evidence primary key"
    )
    at: datetime | None = Field(
        default=None,
        description="When this position took effect — world time. Left unset, the moment of the claim. A rule bounding OBSERVED_AT on EXISTENCE reads this.",
    )
    confidence: float | None = Field(
        default=None,
        description="How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.",
    )
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class CategoryDefinitionInput(BaseModel):
    """What a category means: a union of clauses over classification claims — flat form for one clause, anyOf for several, never both (RFC 0007)"""

    rules: tuple["ClaimRuleInput", ...] = Field(
        description="A claim counts when any rule matches"
    )
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class CategoryNodePositionInput(BaseModel):
    """Input for specifying the position of a node in the graph visualization"""

    category: str = Field(description="The category of the node")
    position_x: float = Field(
        validation_alias=AliasChoices("position_x", "positionX"),
        serialization_alias="positionX",
        description="The x-coordinate of the node position",
    )
    position_y: float = Field(
        validation_alias=AliasChoices("position_y", "positionY"),
        serialization_alias="positionY",
        description="The y-coordinate of the node position",
    )
    width: float | None = Field(
        default=None,
        description="Optional width for the node (for visualization purposes)",
    )
    height: float | None = Field(
        default=None,
        description="Optional height for the node (for visualization purposes)",
    )
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class ClaimConditionGroupInput(BaseModel):
    """An exception: a conjunction that, when it holds whole, blocks its rule"""

    when: tuple["ClaimConditionInput", ...] = Field(
        description="All of these must hold for the exception to apply"
    )
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class ClaimConditionInput(BaseModel):
    """One condition: (field, operator, value) — IS/IN/NOT_IN on WORD/SUBJECT/APP/ACTION/KIND/KEY, BEFORE/SINCE on ASSERTED_AT/OBSERVED_AT, AT_LEAST/BELOW on CONFIDENCE (RFC 0010, 0015, 0016)"""

    field: ClaimField = Field(description="What this condition looks at")
    operator: ClaimOperator = Field(
        description="How it compares. BEFORE/SINCE are inclusive"
    )
    value: Any = Field(
        description="One string for IS, a non-empty string list for IN/NOT_IN, a datetime for BEFORE/SINCE, a number in [0, 1] for AT_LEAST/BELOW. For field KIND: kinds from CLASSIFICATION, EXISTENCE, SAMENESS, EVIDENCE, MEASUREMENT. For field KEY: metric keys"
    )
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class ClaimRuleInput(BaseModel):
    """One rule: matches when all `when` conditions hold and no `unless` group does"""

    when: tuple[ClaimConditionInput, ...] = Field(description="All of these must hold")
    unless: tuple[ClaimConditionGroupInput, ...] | None = Field(
        default=None,
        description="Exceptions: the rule does not match when any group holds whole",
    )
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class ClassificationInput(BaseModel):
    """One claim that a node is of a word, inside a batch"""

    node: str = Field(description="The node being classified")
    term: str = Field(
        description="The organization's word for what is being claimed — a term's `key`, e.g. 'AIS'. Not a category id and not a graph: a claim names a word, and every view that declares that word will hold what you write. The word is created if the organization has not used it before; a view that declares no category for it simply will not draw it."
    )
    observed_at: datetime | None = Field(
        validation_alias=AliasChoices("observed_at", "observedAt"),
        serialization_alias="observedAt",
        default=None,
        description="When the world was in this state — world time, the axis a scientist means by 'when'. Distinct from when it is claimed, which the assertion records; left unset, the two are equal. A point, not an interval: a duration is a metric.",
    )
    confidence: float | None = Field(
        default=None,
        description="How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.",
    )
    derived_from: Annotated[tuple[str, ...] | None, GraphQLDefault("[]")] = Field(
        validation_alias=AliasChoices("derived_from", "derivedFrom"),
        serialization_alias="derivedFrom",
        default=None,
        description='The claims this one came from — ids of instances, links, metrics or structures in your organization. Each is recorded as a DERIVED_FROM link under the same assertion as the claim itself, because "this, because of that" is one act (RFC 0017). Read back as `derivedFrom`; the cited claim lists it under `derivations`.',
    )
    'The claims this one came from — ids of instances, links, metrics or structures in your organization. Each is recorded as a DERIVED_FROM link under the same assertion as the claim itself, because "this, because of that" is one act (RFC 0017). Read back as `derivedFrom`; the cited claim lists it under `derivations`.\nDefault: []'
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class ClassifyNodesInput(BaseModel):
    """Input for claiming that several nodes are of a word, as one act"""

    classifications: tuple[ClassificationInput, ...] = Field(
        description="The claims to record"
    )
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class CommentOnStructureInput(BaseModel):
    """Input for remarking on an external datum, minting its structure if new"""

    identifier: str = Field(
        description="The structure identifier of the datum, e.g. '@mikro/roi'"
    )
    object: str = Field(description="The id of the external object on its service")
    descendants: tuple["DescendantInput", ...] = Field(
        description="The rich body of the remark — a tree of LEAF/MENTION/PARAGRAPH nodes"
    )
    parent: ID | None = Field(
        default=None,
        description="The comment this replies to. Must be on the same structure's thread",
    )
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class CreateEntityCategoryInput(BaseModel):
    """Input for creating a new entity definition in the graph schema"""

    key: str = Field(description="The label of the node participating in the event")
    description: str | None = Field(
        default=None, description="Description of this node role"
    )
    ontology_references: Annotated[
        tuple["OntologyReferenceInput", ...] | None, GraphQLDefault("[]")
    ] = Field(
        validation_alias=AliasChoices("ontology_references", "ontologyReferences"),
        serialization_alias="ontologyReferences",
        default=None,
        description="Ontology references for this event",
    )
    "Ontology references for this event\nDefault: []"
    color: tuple[int, ...] | None = Field(
        default=None,
        description="Optional RGBA color for this node role (e.g. [255, 0, 0, 128])",
    )
    image: str | None = Field(
        default=None,
        description="Optional media store ID for an image representing this node role",
    )
    label: str | None = Field(
        default=None,
        description="Optional human-readable label for this node role (defaults to 'key' if not provided)",
    )
    pin: bool | None = Field(
        default=None, description="Whether to pin this node role in the UI"
    )
    instance_kind: str | None = Field(
        validation_alias=AliasChoices("instance_kind", "instanceKind"),
        serialization_alias="instanceKind",
        default=None,
        description="Optional instance kind for this entity category (e.g. 'neuron', 'synapse', 'behavior'). This is used for further categorization and filtering of entities within the graph.",
    )
    property_definitions: Annotated[
        tuple["PropertyDefinitionInput", ...] | None, GraphQLDefault("[]")
    ] = Field(
        validation_alias=AliasChoices("property_definitions", "propertyDefinitions"),
        serialization_alias="propertyDefinitions",
        default=None,
        description="Property definitions",
    )
    "Property definitions\nDefault: []"
    definition: CategoryDefinitionInput | None = Field(
        default=None,
        description="What this category *means*: a predicate over classification claims (RFC 0007). Omitted means primitive — membership is whatever was asserted under this word",
    )
    graph: str = Field(description="The graph id this entity will belong to")
    backfill: Annotated[bool | None, GraphQLDefault("False")] = Field(
        default=None,
        description="Draw the evidence this word already admits. Claims made under it before this category existed are in the organization's evidence base; with this on they are projected into the graph now, instead of waiting for the next reproject. Off by default because the work is proportional to the graph's evidence and happens before this mutation returns.",
    )
    "Draw the evidence this word already admits. Claims made under it before this category existed are in the organization's evidence base; with this on they are projected into the graph now, instead of waiting for the next reproject. Off by default because the work is proportional to the graph's evidence and happens before this mutation returns.\nDefault: False"
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class CreateGraphInput(BaseModel):
    """Input for creating a new graph from a schema definition"""

    name: str = Field(description="Name of the graph")
    description: str | None = Field(
        default=None, description="Description of the graph"
    )
    definition: "GraphDefinitionInput | None" = Field(
        default=None, description="The complete graph schema definition"
    )
    sameness_rule: "SamenessRuleInput | None" = Field(
        validation_alias=AliasChoices("sameness_rule", "samenessRule"),
        serialization_alias="samenessRule",
        default=None,
        description="Whose sameness claims this view counts (RFC 0024). Omitted means everyone",
    )
    backfill: Annotated[bool | None, GraphQLDefault("False")] = Field(
        default=None,
        description="Draw the evidence this graph's words already admit. A graph is a view over the organization's evidence, so a new one can be a view over history: with this on, every node and edge already claimed under a word this schema declares is projected as the graph is created. Off by default because the work is proportional to the organization's evidence and happens before this mutation returns.",
    )
    "Draw the evidence this graph's words already admit. A graph is a view over the organization's evidence, so a new one can be a view over history: with this on, every node and edge already claimed under a word this schema declares is projected as the graph is created. Off by default because the work is proportional to the organization's evidence and happens before this mutation returns.\nDefault: False"
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class CreateMeasurementCategoryInput(BaseModel):
    """Input for creating a new measurement definition in the graph schema"""

    key: str = Field(description="Relation type name/key")
    description: str | None = Field(
        default=None, description="Description of this node role"
    )
    ontology_references: Annotated[
        tuple["OntologyReferenceInput", ...] | None, GraphQLDefault("[]")
    ] = Field(
        validation_alias=AliasChoices("ontology_references", "ontologyReferences"),
        serialization_alias="ontologyReferences",
        default=None,
        description="Ontology references for this event",
    )
    "Ontology references for this event\nDefault: []"
    color: tuple[int, ...] | None = Field(
        default=None,
        description="Optional RGBA color for this node role (e.g. [255, 0, 0, 128])",
    )
    image: str | None = Field(
        default=None,
        description="Optional media store ID for an image representing this node role",
    )
    label: str | None = Field(
        default=None,
        description="Optional human-readable label for this node role (defaults to 'key' if not provided)",
    )
    pin: bool | None = Field(
        default=None, description="Whether to pin this node role in the UI"
    )
    source: "StructureDescriptorInput" = Field(description="Source entity type(s)")
    target: "EntityDescriptorInput" = Field(description="Target entity type(s)")
    cardinality: Annotated[Cardinality | None, GraphQLDefault("ONE_TO_ONE")] = Field(
        default=None, description="Relation cardinality"
    )
    "Relation cardinality\nDefault: ONE_TO_ONE"
    properties: Annotated[
        tuple["PropertyDefinitionInput", ...] | None, GraphQLDefault("[]")
    ] = Field(default=None, description="Derived property definitions")
    "Derived property definitions\nDefault: []"
    definition: CategoryDefinitionInput | None = Field(
        default=None,
        description="This measurement category's complete rule (RFC 0012): which measurement claims count and whose standings fold. Omitted means primitive",
    )
    graph: str = Field(
        description="The graph id this measurement category will belong to"
    )
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class CreateNaturalEventCategoryInput(BaseModel):
    """Input for creating a new natural event definition in the graph schema"""

    key: str = Field(description="The label of the node participating in the event")
    description: str | None = Field(
        default=None, description="Description of this node role"
    )
    ontology_references: Annotated[
        tuple["OntologyReferenceInput", ...] | None, GraphQLDefault("[]")
    ] = Field(
        validation_alias=AliasChoices("ontology_references", "ontologyReferences"),
        serialization_alias="ontologyReferences",
        default=None,
        description="Ontology references for this event",
    )
    "Ontology references for this event\nDefault: []"
    color: tuple[int, ...] | None = Field(
        default=None,
        description="Optional RGBA color for this node role (e.g. [255, 0, 0, 128])",
    )
    image: str | None = Field(
        default=None,
        description="Optional media store ID for an image representing this node role",
    )
    label: str | None = Field(
        default=None,
        description="Optional human-readable label for this node role (defaults to 'key' if not provided)",
    )
    pin: bool | None = Field(
        default=None, description="Whether to pin this node role in the UI"
    )
    kind: EventKind = Field(
        description="Whether the event arises in the system itself (INTRINSIC, e.g. mitosis) or is applied from outside (EXTRINSIC, e.g. a protocol step)"
    )
    inputs: Annotated[
        tuple["EventRoleInput", ...] | None, GraphQLDefault("[]")
    ] = Field(default=None, description="Input node roles")
    "Input node roles\nDefault: []"
    outputs: Annotated[
        tuple["EventRoleInput", ...] | None, GraphQLDefault("[]")
    ] = Field(default=None, description="Output node roles")
    "Output node roles\nDefault: []"
    properties: Annotated[
        tuple["PropertyDefinitionInput", ...] | None, GraphQLDefault("[]")
    ] = Field(default=None, description="Property definitions")
    "Property definitions\nDefault: []"
    definition: CategoryDefinitionInput | None = Field(
        default=None,
        description="This event category's complete rule (RFC 0009): which classification claims admit an event, whose existence standings count, and whose participation claims draw its edges. Omitted means primitive",
    )
    graph: str = Field(description="The graph id this event will belong to")
    backfill: Annotated[bool | None, GraphQLDefault("False")] = Field(
        default=None,
        description="Draw the evidence this word already admits. Claims made under it before this category existed are in the organization's evidence base; with this on they are projected into the graph now, instead of waiting for the next reproject. Off by default because the work is proportional to the graph's evidence and happens before this mutation returns.",
    )
    "Draw the evidence this word already admits. Claims made under it before this category existed are in the organization's evidence base; with this on they are projected into the graph now, instead of waiting for the next reproject. Off by default because the work is proportional to the graph's evidence and happens before this mutation returns.\nDefault: False"
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class CreateProtocolEventCategoryInput(BaseModel):
    """Input for creating a new protocol event definition in the graph schema"""

    key: str = Field(description="The label of the node participating in the event")
    description: str | None = Field(
        default=None, description="Description of this node role"
    )
    ontology_references: Annotated[
        tuple["OntologyReferenceInput", ...] | None, GraphQLDefault("[]")
    ] = Field(
        validation_alias=AliasChoices("ontology_references", "ontologyReferences"),
        serialization_alias="ontologyReferences",
        default=None,
        description="Ontology references for this event",
    )
    "Ontology references for this event\nDefault: []"
    color: tuple[int, ...] | None = Field(
        default=None,
        description="Optional RGBA color for this node role (e.g. [255, 0, 0, 128])",
    )
    image: str | None = Field(
        default=None,
        description="Optional media store ID for an image representing this node role",
    )
    label: str | None = Field(
        default=None,
        description="Optional human-readable label for this node role (defaults to 'key' if not provided)",
    )
    pin: bool | None = Field(
        default=None, description="Whether to pin this node role in the UI"
    )
    kind: EventKind = Field(
        description="Whether the event arises in the system itself (INTRINSIC, e.g. mitosis) or is applied from outside (EXTRINSIC, e.g. a protocol step)"
    )
    inputs: Annotated[
        tuple["EventRoleInput", ...] | None, GraphQLDefault("[]")
    ] = Field(default=None, description="Input node roles")
    "Input node roles\nDefault: []"
    outputs: Annotated[
        tuple["EventRoleInput", ...] | None, GraphQLDefault("[]")
    ] = Field(default=None, description="Output node roles")
    "Output node roles\nDefault: []"
    properties: Annotated[
        tuple["PropertyDefinitionInput", ...] | None, GraphQLDefault("[]")
    ] = Field(default=None, description="Property definitions")
    "Property definitions\nDefault: []"
    definition: CategoryDefinitionInput | None = Field(
        default=None,
        description="This event category's complete rule (RFC 0009): which classification claims admit an event, whose existence standings count, and whose participation claims draw its edges. Omitted means primitive",
    )
    protocol: str = Field(description="The protocol this event definition belongs to")
    graph: str = Field(description="The graph id this event will belong to")
    backfill: Annotated[bool | None, GraphQLDefault("False")] = Field(
        default=None,
        description="Draw the evidence this word already admits. Claims made under it before this category existed are in the organization's evidence base; with this on they are projected into the graph now, instead of waiting for the next reproject. Off by default because the work is proportional to the graph's evidence and happens before this mutation returns.",
    )
    "Draw the evidence this word already admits. Claims made under it before this category existed are in the organization's evidence base; with this on they are projected into the graph now, instead of waiting for the next reproject. Off by default because the work is proportional to the graph's evidence and happens before this mutation returns.\nDefault: False"
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class CreateRelationCategoryInput(BaseModel):
    """Input for creating a new relation definition in the graph schema"""

    key: str = Field(description="The label of the node participating in the event")
    description: str | None = Field(
        default=None, description="Description of this node role"
    )
    ontology_references: Annotated[
        tuple["OntologyReferenceInput", ...] | None, GraphQLDefault("[]")
    ] = Field(
        validation_alias=AliasChoices("ontology_references", "ontologyReferences"),
        serialization_alias="ontologyReferences",
        default=None,
        description="Ontology references for this event",
    )
    "Ontology references for this event\nDefault: []"
    color: tuple[int, ...] | None = Field(
        default=None,
        description="Optional RGBA color for this node role (e.g. [255, 0, 0, 128])",
    )
    image: str | None = Field(
        default=None,
        description="Optional media store ID for an image representing this node role",
    )
    label: str | None = Field(
        default=None,
        description="Optional human-readable label for this node role (defaults to 'key' if not provided)",
    )
    pin: bool | None = Field(
        default=None, description="Whether to pin this node role in the UI"
    )
    instance_kind: str | None = Field(
        validation_alias=AliasChoices("instance_kind", "instanceKind"),
        serialization_alias="instanceKind",
        default=None,
        description="Optional instance kind for this entity category (e.g. 'neuron', 'synapse', 'behavior'). This is used for further categorization and filtering of entities within the graph.",
    )
    property_definitions: Annotated[
        tuple["PropertyDefinitionInput", ...] | None, GraphQLDefault("[]")
    ] = Field(
        validation_alias=AliasChoices("property_definitions", "propertyDefinitions"),
        serialization_alias="propertyDefinitions",
        default=None,
        description="Property definitions",
    )
    "Property definitions\nDefault: []"
    definition: CategoryDefinitionInput | None = Field(
        default=None,
        description="What this category *means*: a predicate over classification claims (RFC 0007). Omitted means primitive — membership is whatever was asserted under this word",
    )
    graph: str = Field(description="The graph id this entity will belong to")
    backfill: Annotated[bool | None, GraphQLDefault("False")] = Field(
        default=None,
        description="Draw the evidence this word already admits. Claims made under it before this category existed are in the organization's evidence base; with this on they are projected into the graph now, instead of waiting for the next reproject. Off by default because the work is proportional to the graph's evidence and happens before this mutation returns.",
    )
    "Draw the evidence this word already admits. Claims made under it before this category existed are in the organization's evidence base; with this on they are projected into the graph now, instead of waiting for the next reproject. Off by default because the work is proportional to the graph's evidence and happens before this mutation returns.\nDefault: False"
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class CreateStructureRelationCategoryInput(BaseModel):
    """Input for creating a new structure relation definition in the graph schema"""

    key: str = Field(description="Relation type name/key")
    description: str | None = Field(
        default=None, description="Description of this node role"
    )
    ontology_references: Annotated[
        tuple["OntologyReferenceInput", ...] | None, GraphQLDefault("[]")
    ] = Field(
        validation_alias=AliasChoices("ontology_references", "ontologyReferences"),
        serialization_alias="ontologyReferences",
        default=None,
        description="Ontology references for this event",
    )
    "Ontology references for this event\nDefault: []"
    color: tuple[int, ...] | None = Field(
        default=None,
        description="Optional RGBA color for this node role (e.g. [255, 0, 0, 128])",
    )
    image: str | None = Field(
        default=None,
        description="Optional media store ID for an image representing this node role",
    )
    label: str | None = Field(
        default=None,
        description="Optional human-readable label for this node role (defaults to 'key' if not provided)",
    )
    pin: bool | None = Field(
        default=None, description="Whether to pin this node role in the UI"
    )
    properties: Annotated[
        tuple["PropertyDefinitionInput", ...] | None, GraphQLDefault("[]")
    ] = Field(default=None, description="Derived property definitions")
    "Derived property definitions\nDefault: []"
    source: "StructureDescriptorInput" = Field(description="Source entity type(s)")
    target: "StructureDescriptorInput" = Field(description="Target entity type(s)")
    cardinality: Annotated[Cardinality | None, GraphQLDefault("ONE_TO_ONE")] = Field(
        default=None, description="Relation cardinality"
    )
    "Relation cardinality\nDefault: ONE_TO_ONE"
    definition: CategoryDefinitionInput | None = Field(
        default=None,
        description="This structure-relation category's complete rule (RFC 0012): which structure-relation claims count — by word, annotator, app and window — and whose standings fold. Omitted means primitive",
    )
    graph: str = Field(description="The graph id this entity will belong to")
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class CreateTermInput(BaseModel):
    """Input for declaring one of the organization's words"""

    kind: TermKind = Field(
        description="What sort of thing this word names. Part of its identity."
    )
    key: str = Field(description="The word itself, e.g. 'AIS'")
    label: str | None = Field(default=None, description="Human-readable name")
    description: str | None = Field(default=None, description="What this word means")
    purl: str | None = Field(
        default=None,
        description="Persistent URL, where this corresponds to a published ontology term",
    )
    color: tuple[int, ...] | None = Field(
        default=None, description="Optional RGBA colour"
    )
    image: str | None = Field(
        default=None, description="Optional media store ID for an illustrative image"
    )
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class DeleteEntityCategoryInput(BaseModel):
    """Input for deleting an existing entity definition in the graph schema"""

    id: ID = Field(description="The ID of the structure category to delete")
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class DeleteGraphInput(BaseModel):
    """Input for deleting a graph"""

    id: str = Field(description="The ID of the graph to delete")
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class DeleteMeasurementCategoryInput(BaseModel):
    """Input for deleting an existing measurement definition in the graph schema"""

    id: str = Field(description="The ID of the measurement category to delete")
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class DeleteMetricKindInput(BaseModel):
    """Input for deleting an existing metric definition in the graph schema"""

    id: str = Field(description="The ID of the metric kind to retire")
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class DeleteNaturalEventCategoryInput(BaseModel):
    """Input for deleting an existing natural event definition in the graph schema"""

    id: str = Field(description="The ID of the event category to delete")
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class DeleteProtocolEventCategoryInput(BaseModel):
    """Input for deleting an existing protocol event definition in the graph schema"""

    id: str = Field(description="The ID of the event category to delete")
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class DeleteRelationCategoryInput(BaseModel):
    """Input for deleting an existing relation definition in the graph schema"""

    id: str = Field(description="The ID of the relation category to delete")
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class DeleteStructureKindInput(BaseModel):
    """Input for deleting an existing structure definition in the graph schema"""

    id: str = Field(description="The ID of the structure kind to retire")
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class DeleteStructureRelationCategoryInput(BaseModel):
    """Input for deleting an existing structure relation definition in the graph schema"""

    id: str = Field(description="The ID of the structure relation category to delete")
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class DeleteTermInput(BaseModel):
    """Input for retiring one of the organization's words"""

    id: str = Field(description="The ID of the term to delete")
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class DerivationRuleInput(BaseModel):
    """Configuration for property derivation rules"""

    source_node: str | None = Field(
        validation_alias=AliasChoices("source_node", "sourceNode"),
        serialization_alias="sourceNode",
        default=None,
        description="The label of the describing structure to read from",
    )
    key: str | None = Field(
        default=None, description="The property key on the source node"
    )
    source_value_kind: ValueKind | None = Field(
        validation_alias=AliasChoices("source_value_kind", "sourceValueKind"),
        serialization_alias="sourceValueKind",
        default=None,
        description="Which value kind of the source key to read, when the key has terms in more than one. Distinct from the property's own `value_kind`, which is the aggregation's result type: COUNT yields INT over STRING sources. Leave unset when the key is unambiguous. INT and FLOAT are read together either way.",
    )
    aggregation: AggregationFunction | None = Field(
        default=None,
        description="Aggregation function (MEAN, SUM, MAX, MIN, COUNT, etc.)",
    )
    evidence: "MetricEvidenceInput | None" = Field(
        default=None,
        description="This property's own metric rule: a rule list over SUBJECT/APP/ACTION/KEY/ASSERTED_AT/OBSERVED_AT/CONFIDENCE — any rule admits, all its `when` conditions must hold, `unless` groups subtract. When present it replaces the owning category's rules as the metric scope (classification annotators and measurement producers are usually different populations, so intersecting them would routinely produce nothing); when absent, the category's MEASUREMENT rules apply, and a primitive category folds everything.",
    )
    subject_priority: Annotated[tuple[str, ...] | None, GraphQLDefault("[]")] = Field(
        validation_alias=AliasChoices("subject_priority", "subjectPriority"),
        serialization_alias="subjectPriority",
        default=None,
        description="Subjects in descending order of trust, for PRIORITY_LATEST. The first subject with any measurement wins; subjects not listed are considered only if none of the listed ones have measured.",
    )
    "Subjects in descending order of trust, for PRIORITY_LATEST. The first subject with any measurement wins; subjects not listed are considered only if none of the listed ones have measured.\nDefault: []"
    tool_priority: Annotated[tuple[str, ...] | None, GraphQLDefault("[]")] = Field(
        validation_alias=AliasChoices("tool_priority", "toolPriority"),
        serialization_alias="toolPriority",
        default=None,
        description="App ids in descending order of trust, for LATEST_ASSERTION_TOOL.",
    )
    "App ids in descending order of trust, for LATEST_ASSERTION_TOOL.\nDefault: []"
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class DescendantInput(BaseModel):
    """One node of a comment's rich body — shape-compatible with lok's komment descendants"""

    kind: DescendantKind = Field(
        description="LEAF, MENTION or PARAGRAPH — see `core.enums.DescendantKind`"
    )
    children: tuple["DescendantInput", ...] | None = Field(
        default=None, description="The children of this node. Always empty for leafs"
    )
    text: str | None = Field(default=None, description="The text of a leaf")
    bold: bool | None = None
    italic: bool | None = None
    underline: bool | None = None
    code: bool | None = None
    user: str | None = Field(
        default=None,
        description="The mentioned subject id — `Assertion.subject`'s vocabulary. Named `user` for shape-compatibility with lok's tree",
    )
    size: str | None = Field(default=None, description="The size of a paragraph")
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class EntityCategoryFilter(BaseModel):
    """No documentation"""

    graph: "GraphFilter | None" = None
    id: ID | None = None
    label: str | None = None
    and_: "EntityCategoryFilter | None" = Field(
        validation_alias=AliasChoices("and_", "AND"),
        serialization_alias="AND",
        default=None,
    )
    or_: "EntityCategoryFilter | None" = Field(
        validation_alias=AliasChoices("or_", "OR"),
        serialization_alias="OR",
        default=None,
    )
    not_: "EntityCategoryFilter | None" = Field(
        validation_alias=AliasChoices("not_", "NOT"),
        serialization_alias="NOT",
        default=None,
    )
    distinct: bool | None = Field(
        validation_alias=AliasChoices("distinct", "DISTINCT"),
        serialization_alias="DISTINCT",
        default=None,
    )
    ids: tuple[ID, ...] | None = Field(
        default=None, description="Filter by list of IDs"
    )
    pinned: bool | None = Field(default=None, description="Filter by list of IDs")
    search: str | None = Field(default=None, description="Filter by list of IDs")
    matches_descriptor: "EntityDescriptorInput | None" = Field(
        validation_alias=AliasChoices("matches_descriptor", "matchesDescriptor"),
        serialization_alias="matchesDescriptor",
        default=None,
        description="Filter by list of IDs",
    )
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class EntityDefinitionInput(BaseModel):
    """Definition of an entity type in the graph schema"""

    key: str = Field(description="The label of the node participating in the event")
    description: str | None = Field(
        default=None, description="Description of this node role"
    )
    ontology_references: Annotated[
        tuple["OntologyReferenceInput", ...] | None, GraphQLDefault("[]")
    ] = Field(
        validation_alias=AliasChoices("ontology_references", "ontologyReferences"),
        serialization_alias="ontologyReferences",
        default=None,
        description="Ontology references for this event",
    )
    "Ontology references for this event\nDefault: []"
    color: tuple[int, ...] | None = Field(
        default=None,
        description="Optional RGBA color for this node role (e.g. [255, 0, 0, 128])",
    )
    image: str | None = Field(
        default=None,
        description="Optional media store ID for an image representing this node role",
    )
    label: str | None = Field(
        default=None,
        description="Optional human-readable label for this node role (defaults to 'key' if not provided)",
    )
    pin: bool | None = Field(
        default=None, description="Whether to pin this node role in the UI"
    )
    instance_kind: str | None = Field(
        validation_alias=AliasChoices("instance_kind", "instanceKind"),
        serialization_alias="instanceKind",
        default=None,
        description="Optional instance kind for this entity category (e.g. 'neuron', 'synapse', 'behavior'). This is used for further categorization and filtering of entities within the graph.",
    )
    property_definitions: Annotated[
        tuple["PropertyDefinitionInput", ...] | None, GraphQLDefault("[]")
    ] = Field(
        validation_alias=AliasChoices("property_definitions", "propertyDefinitions"),
        serialization_alias="propertyDefinitions",
        default=None,
        description="Property definitions",
    )
    "Property definitions\nDefault: []"
    definition: CategoryDefinitionInput | None = Field(
        default=None,
        description="What this category *means*: a predicate over classification claims (RFC 0007). Omitted means primitive — membership is whatever was asserted under this word",
    )
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class EntityDescriptorInput(BaseModel):
    """Filters that select which entity categories a descriptor matches"""

    keys: tuple[str, ...] | None = Field(
        default=None, description="Filter by entity key/label"
    )
    ontology_terms: tuple[str, ...] | None = Field(
        validation_alias=AliasChoices("ontology_terms", "ontologyTerms"),
        serialization_alias="ontologyTerms",
        default=None,
        description="Filter by ontology references on the entity (format: 'PREFIX:TERM_ID')",
    )
    default_category_key: str | None = Field(
        validation_alias=AliasChoices("default_category_key", "defaultCategoryKey"),
        serialization_alias="defaultCategoryKey",
        default=None,
        description="Default category to link to if no entities match the filters",
    )
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class EventDefinitionInput(BaseModel):
    """Definition of an event type in the graph schema"""

    key: str = Field(description="The label of the node participating in the event")
    description: str | None = Field(
        default=None, description="Description of this node role"
    )
    ontology_references: Annotated[
        tuple["OntologyReferenceInput", ...] | None, GraphQLDefault("[]")
    ] = Field(
        validation_alias=AliasChoices("ontology_references", "ontologyReferences"),
        serialization_alias="ontologyReferences",
        default=None,
        description="Ontology references for this event",
    )
    "Ontology references for this event\nDefault: []"
    color: tuple[int, ...] | None = Field(
        default=None,
        description="Optional RGBA color for this node role (e.g. [255, 0, 0, 128])",
    )
    image: str | None = Field(
        default=None,
        description="Optional media store ID for an image representing this node role",
    )
    label: str | None = Field(
        default=None,
        description="Optional human-readable label for this node role (defaults to 'key' if not provided)",
    )
    pin: bool | None = Field(
        default=None, description="Whether to pin this node role in the UI"
    )
    kind: EventKind = Field(
        description="Whether the event arises in the system itself (INTRINSIC, e.g. mitosis) or is applied from outside (EXTRINSIC, e.g. a protocol step)"
    )
    inputs: Annotated[
        tuple["EventRoleInput", ...] | None, GraphQLDefault("[]")
    ] = Field(default=None, description="Input node roles")
    "Input node roles\nDefault: []"
    outputs: Annotated[
        tuple["EventRoleInput", ...] | None, GraphQLDefault("[]")
    ] = Field(default=None, description="Output node roles")
    "Output node roles\nDefault: []"
    properties: Annotated[
        tuple["PropertyDefinitionInput", ...] | None, GraphQLDefault("[]")
    ] = Field(default=None, description="Property definitions")
    "Property definitions\nDefault: []"
    definition: CategoryDefinitionInput | None = Field(
        default=None,
        description="This event category's complete rule (RFC 0009): which classification claims admit an event, whose existence standings count, and whose participation claims draw its edges. Omitted means primitive",
    )
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class EventRoleInput(BaseModel):
    """One declared role on an event category"""

    key: str = Field(description="The label of the node participating in the event")
    role: str = Field(description="What type of role does this node play in the event")
    descriptor: EntityDescriptorInput = Field(
        description="Optional filters to apply when linking entities to structures for this role"
    )
    ontology_references: Annotated[
        tuple["OntologyReferenceInput", ...] | None, GraphQLDefault("[]")
    ] = Field(
        validation_alias=AliasChoices("ontology_references", "ontologyReferences"),
        serialization_alias="ontologyReferences",
        default=None,
        description="Ontology references for this role",
    )
    "Ontology references for this role\nDefault: []"
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class GraphDefinitionInput(BaseModel):
    """A complete graph schema definition"""

    system_version: Annotated[str | None, GraphQLDefault("0.0.1")] = Field(
        validation_alias=AliasChoices("system_version", "systemVersion"),
        serialization_alias="systemVersion",
        default=None,
        description="Semantic version for this schema definition (e.g., '1.0.0')",
    )
    "Semantic version for this schema definition (e.g., '1.0.0')\nDefault: 0.0.1"
    extensions: "GraphExtensionsInput" = Field(
        description="The graph extensions containing all type definitions"
    )
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class GraphExtensionsInput(BaseModel):
    """The categories a graph schema declares"""

    entities: Annotated[
        tuple[EntityDefinitionInput, ...] | None, GraphQLDefault("[]")
    ] = Field(default=None, description="Entity definitions")
    "Entity definitions\nDefault: []"
    relations: Annotated[
        tuple["RelationDefinitionInput", ...] | None, GraphQLDefault("[]")
    ] = Field(default=None, description="Relation definitions")
    "Relation definitions\nDefault: []"
    structure_relations: Annotated[
        tuple["StructureRelationDefinitionInput", ...] | None, GraphQLDefault("[]")
    ] = Field(
        validation_alias=AliasChoices("structure_relations", "structureRelations"),
        serialization_alias="structureRelations",
        default=None,
        description="Structure relation definitions",
    )
    "Structure relation definitions\nDefault: []"
    measurements: Annotated[
        tuple["MeasurementDefinitionInput", ...] | None, GraphQLDefault("[]")
    ] = Field(default=None, description="Measurement definitions")
    "Measurement definitions\nDefault: []"
    events: Annotated[
        tuple[EventDefinitionInput, ...] | None, GraphQLDefault("[]")
    ] = Field(default=None, description="Event definitions")
    "Event definitions\nDefault: []"
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class GraphFilter(BaseModel):
    """No documentation"""

    id: ID | None = None
    name: str | None = None
    description: str | None = None
    and_: "GraphFilter | None" = Field(
        validation_alias=AliasChoices("and_", "AND"),
        serialization_alias="AND",
        default=None,
    )
    or_: "GraphFilter | None" = Field(
        validation_alias=AliasChoices("or_", "OR"),
        serialization_alias="OR",
        default=None,
    )
    not_: "GraphFilter | None" = Field(
        validation_alias=AliasChoices("not_", "NOT"),
        serialization_alias="NOT",
        default=None,
    )
    distinct: bool | None = Field(
        validation_alias=AliasChoices("distinct", "DISTINCT"),
        serialization_alias="DISTINCT",
        default=None,
    )
    pinned: bool | None = Field(default=None, description="Filter by list of IDs")
    ids: tuple[ID, ...] | None = Field(
        default=None, description="Filter by list of IDs"
    )
    search: str | None = Field(default=None, description="Filter by list of IDs")
    is_archived: bool | None = Field(
        validation_alias=AliasChoices("is_archived", "isArchived"),
        serialization_alias="isArchived",
        default=None,
        description="Only archived graphs, or only live ones. Omitted shows both",
    )
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class MeasurementCategoryFilter(BaseModel):
    """No documentation"""

    graph: GraphFilter | None = None
    id: ID | None = None
    label: str | None = None
    and_: "MeasurementCategoryFilter | None" = Field(
        validation_alias=AliasChoices("and_", "AND"),
        serialization_alias="AND",
        default=None,
    )
    or_: "MeasurementCategoryFilter | None" = Field(
        validation_alias=AliasChoices("or_", "OR"),
        serialization_alias="OR",
        default=None,
    )
    not_: "MeasurementCategoryFilter | None" = Field(
        validation_alias=AliasChoices("not_", "NOT"),
        serialization_alias="NOT",
        default=None,
    )
    distinct: bool | None = Field(
        validation_alias=AliasChoices("distinct", "DISTINCT"),
        serialization_alias="DISTINCT",
        default=None,
    )
    ids: tuple[ID, ...] | None = Field(
        default=None, description="Filter by list of IDs"
    )
    pinned: bool | None = Field(default=None, description="Filter by list of IDs")
    search: str | None = Field(default=None, description="Filter by list of IDs")
    source_identifier: str | None = Field(
        validation_alias=AliasChoices("source_identifier", "sourceIdentifier"),
        serialization_alias="sourceIdentifier",
        default=None,
        description="Filter by the structure identifier this measurement's source selects",
    )
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class MeasurementDefinitionInput(BaseModel):
    """Declares a measurement category in a graph schema"""

    key: str = Field(description="Relation type name/key")
    description: str | None = Field(
        default=None, description="Description of this node role"
    )
    ontology_references: Annotated[
        tuple["OntologyReferenceInput", ...] | None, GraphQLDefault("[]")
    ] = Field(
        validation_alias=AliasChoices("ontology_references", "ontologyReferences"),
        serialization_alias="ontologyReferences",
        default=None,
        description="Ontology references for this event",
    )
    "Ontology references for this event\nDefault: []"
    color: tuple[int, ...] | None = Field(
        default=None,
        description="Optional RGBA color for this node role (e.g. [255, 0, 0, 128])",
    )
    image: str | None = Field(
        default=None,
        description="Optional media store ID for an image representing this node role",
    )
    label: str | None = Field(
        default=None,
        description="Optional human-readable label for this node role (defaults to 'key' if not provided)",
    )
    pin: bool | None = Field(
        default=None, description="Whether to pin this node role in the UI"
    )
    source: "StructureDescriptorInput" = Field(description="Source entity type(s)")
    target: EntityDescriptorInput = Field(description="Target entity type(s)")
    cardinality: Annotated[Cardinality | None, GraphQLDefault("ONE_TO_ONE")] = Field(
        default=None, description="Relation cardinality"
    )
    "Relation cardinality\nDefault: ONE_TO_ONE"
    properties: Annotated[
        tuple["PropertyDefinitionInput", ...] | None, GraphQLDefault("[]")
    ] = Field(default=None, description="Derived property definitions")
    "Derived property definitions\nDefault: []"
    definition: CategoryDefinitionInput | None = Field(
        default=None,
        description="This measurement category's complete rule (RFC 0012): which measurement claims count and whose standings fold. Omitted means primitive",
    )
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class MetricEvidenceInput(BaseModel):
    """A property's own metric rule: the definition's rule list over metric rows — no WORD or KIND, KEY allowed anywhere"""

    rules: tuple[ClaimRuleInput, ...] = Field(
        description="A metric counts when any rule matches"
    )
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class MetricInput(BaseModel):
    """One measured value about a structure"""

    key: str
    value: Any
    value_kind: PropertyType = Field(
        validation_alias=AliasChoices("value_kind", "valueKind"),
        serialization_alias="valueKind",
        description="What type of value this is. Required: it decides which column the value is stored in and which measurement term it is recorded under, and nothing infers it. Two callers may declare the same key differently — a float `confidence` and a category-label `confidence` are two terms, and both are recorded.",
    )
    confidence: float | None = Field(
        default=None,
        description="How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.",
    )
    confidence_type: str | None = Field(
        validation_alias=AliasChoices("confidence_type", "confidenceType"),
        serialization_alias="confidenceType",
        default=None,
        description="What kind of number `confidence` is — a method's own score, a p-value. Measurement-only",
    )
    unit: str | None = None
    observed_at: datetime | None = Field(
        validation_alias=AliasChoices("observed_at", "observedAt"),
        serialization_alias="observedAt",
        default=None,
        description="When the world was observed. Defaults to when it was claimed.",
    )
    derived_from: Annotated[tuple[str, ...] | None, GraphQLDefault("[]")] = Field(
        validation_alias=AliasChoices("derived_from", "derivedFrom"),
        serialization_alias="derivedFrom",
        default=None,
        description='The claims this one came from — ids of instances, links, metrics or structures in your organization. Each is recorded as a DERIVED_FROM link under the same assertion as the claim itself, because "this, because of that" is one act (RFC 0017). Read back as `derivedFrom`; the cited claim lists it under `derivations`.',
    )
    'The claims this one came from — ids of instances, links, metrics or structures in your organization. Each is recorded as a DERIVED_FROM link under the same assertion as the claim itself, because "this, because of that" is one act (RFC 0017). Read back as `derivedFrom`; the cited claim lists it under `derivations`.\nDefault: []'
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class MetricKindFilter(BaseModel):
    """No documentation"""

    and_: "MetricKindFilter | None" = Field(
        validation_alias=AliasChoices("and_", "AND"),
        serialization_alias="AND",
        default=None,
    )
    or_: "MetricKindFilter | None" = Field(
        validation_alias=AliasChoices("or_", "OR"),
        serialization_alias="OR",
        default=None,
    )
    not_: "MetricKindFilter | None" = Field(
        validation_alias=AliasChoices("not_", "NOT"),
        serialization_alias="NOT",
        default=None,
    )
    distinct: bool | None = Field(
        validation_alias=AliasChoices("distinct", "DISTINCT"),
        serialization_alias="DISTINCT",
        default=None,
    )
    ids: tuple[ID, ...] | None = Field(
        default=None, description="Filter by list of IDs"
    )
    search: str | None = Field(default=None, description="Search label and key")
    value_kind: ValueKind | None = Field(
        validation_alias=AliasChoices("value_kind", "valueKind"),
        serialization_alias="valueKind",
        default=None,
        description="Filter by the kind of value this measurement carries",
    )
    structure_kind: ID | None = Field(
        validation_alias=AliasChoices("structure_kind", "structureKind"),
        serialization_alias="structureKind",
        default=None,
        description="Filter by the structure kind this describes",
    )
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class NaturalEventCategoryFilter(BaseModel):
    """No documentation"""

    graph: GraphFilter | None = None
    id: ID | None = None
    label: str | None = None
    and_: "NaturalEventCategoryFilter | None" = Field(
        validation_alias=AliasChoices("and_", "AND"),
        serialization_alias="AND",
        default=None,
    )
    or_: "NaturalEventCategoryFilter | None" = Field(
        validation_alias=AliasChoices("or_", "OR"),
        serialization_alias="OR",
        default=None,
    )
    not_: "NaturalEventCategoryFilter | None" = Field(
        validation_alias=AliasChoices("not_", "NOT"),
        serialization_alias="NOT",
        default=None,
    )
    distinct: bool | None = Field(
        validation_alias=AliasChoices("distinct", "DISTINCT"),
        serialization_alias="DISTINCT",
        default=None,
    )
    ids: tuple[ID, ...] | None = Field(
        default=None, description="Filter by list of IDs"
    )
    pinned: bool | None = Field(default=None, description="Filter by list of IDs")
    search: str | None = Field(default=None, description="Filter by list of IDs")
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class NodeFilters(BaseModel):
    """Filter options for querying nodes"""

    ids: tuple[ID, ...] | None = Field(
        default=None, description="Filter by specific node IDs"
    )
    search: str | None = Field(
        default=None,
        description="Substring match on the claim's term key or label. A column of the log, not a derived property",
    )
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class NodeOrder(BaseModel):
    """Ordering options for node queries"""

    created_at: Ordering | None = Field(
        validation_alias=AliasChoices("created_at", "createdAt"),
        serialization_alias="createdAt",
        default=None,
        description="Order by when the row was stored — arrival time. Prefer `seq`, the log's order",
    )
    seq: Ordering | None = Field(
        default=None,
        description="Order by the act's position in the log (`Assertion.seq`) — the log's own total order (RFC 0025)",
    )
    observed_at: Ordering | None = Field(
        validation_alias=AliasChoices("observed_at", "observedAt"),
        serialization_alias="observedAt",
        default=None,
        description="Order by world time — when the claim says the world was so (RFC 0015)",
    )
    id: Ordering | None = Field(default=None, description="Order by node ID")
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class NodePaginationInput(BaseModel):
    """Pagination options for querying nodes"""

    offset: Annotated[int | None, GraphQLDefault("0")] = Field(
        default=None, description="Number of items to skip"
    )
    "Number of items to skip\nDefault: 0"
    limit: Annotated[int | None, GraphQLDefault("100")] = Field(
        default=None, description="Maximum number of items to return"
    )
    "Maximum number of items to return\nDefault: 100"
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class OffsetPaginationInput(BaseModel):
    """No documentation"""

    offset: Annotated[int | None, GraphQLDefault("0")] = None
    "Default: 0"
    limit: int | None = None
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class OntologyReferenceInput(BaseModel):
    """A reference to a published ontology term"""

    prefix: str = Field(
        description="The ontology prefix (e.g. 'OBI'). Must be defined in graph prefixes."
    )
    uri: str = Field(description="The full URI for the ontology term")
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class ParticipantInput(BaseModel):
    """One entity's part in an event, inside a batch"""

    entity: str = Field(description="The ID of the entity that took part")
    role: str = Field(
        description="Which role the entity played — the caller's own word; the write names no graph and no category"
    )
    is_input: Annotated[bool | None, GraphQLDefault("True")] = Field(
        validation_alias=AliasChoices("is_input", "isInput"),
        serialization_alias="isInput",
        default=None,
        description="True if the entity went into the event, False if it came out of it",
    )
    "True if the entity went into the event, False if it came out of it\nDefault: True"
    observed_at: datetime | None = Field(
        validation_alias=AliasChoices("observed_at", "observedAt"),
        serialization_alias="observedAt",
        default=None,
        description="When the world was in this state — world time, the axis a scientist means by 'when'. Distinct from when it is claimed, which the assertion records; left unset, the two are equal. A point, not an interval: a duration is a metric.",
    )
    confidence: float | None = Field(
        default=None,
        description="How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.",
    )
    derived_from: Annotated[tuple[str, ...] | None, GraphQLDefault("[]")] = Field(
        validation_alias=AliasChoices("derived_from", "derivedFrom"),
        serialization_alias="derivedFrom",
        default=None,
        description='The claims this one came from — ids of instances, links, metrics or structures in your organization. Each is recorded as a DERIVED_FROM link under the same assertion as the claim itself, because "this, because of that" is one act (RFC 0017). Read back as `derivedFrom`; the cited claim lists it under `derivations`.',
    )
    'The claims this one came from — ids of instances, links, metrics or structures in your organization. Each is recorded as a DERIVED_FROM link under the same assertion as the claim itself, because "this, because of that" is one act (RFC 0017). Read back as `derivedFrom`; the cited claim lists it under `derivations`.\nDefault: []'
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class PropertyDefinitionInput(BaseModel):
    """Definition of a property on an entity, structure, or relation"""

    label: str | None = Field(
        default=None,
        description="Optional human-readable label for this property (defaults to 'key' if not provided)",
    )
    key: str = Field(description="Property key/name")
    value_kind: ValueKind = Field(
        validation_alias=AliasChoices("value_kind", "valueKind"),
        serialization_alias="valueKind",
    )
    unit: str | None = Field(default=None, description="Unit of measurement")
    description: str | None = Field(
        default=None, description="Description of this property"
    )
    derivation: Annotated[DerivationType | None, GraphQLDefault("LATEST")] = Field(
        default=None,
        description="Derivation type: LATEST, PRIORITY_LATEST, ROLLUP, LATEST_ASSERTION_TOOL",
    )
    "Derivation type: LATEST, PRIORITY_LATEST, ROLLUP, LATEST_ASSERTION_TOOL\nDefault: LATEST"
    rule: DerivationRuleInput | None = Field(
        default=None, description="Rule configuration for ROLLUP derivation"
    )
    index: Annotated[bool | None, GraphQLDefault("False")] = Field(
        default=None,
        description="Whether to create an index on this property for faster queries",
    )
    "Whether to create an index on this property for faster queries\nDefault: False"
    searchable: Annotated[bool | None, GraphQLDefault("False")] = Field(
        default=None, description="Whether this property should be full-text searchable"
    )
    "Whether this property should be full-text searchable\nDefault: False"
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class PropertyMatch(BaseModel):
    """A property match condition for filtering structures"""

    key: str = Field(description="The property matching")
    operator: WhereOperator = Field(description="The operator to use")
    value: str = Field(description="The value to filter against")
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class ProtocolEventCategoryFilter(BaseModel):
    """No documentation"""

    graph: GraphFilter | None = None
    id: ID | None = None
    label: str | None = None
    and_: "ProtocolEventCategoryFilter | None" = Field(
        validation_alias=AliasChoices("and_", "AND"),
        serialization_alias="AND",
        default=None,
    )
    or_: "ProtocolEventCategoryFilter | None" = Field(
        validation_alias=AliasChoices("or_", "OR"),
        serialization_alias="OR",
        default=None,
    )
    not_: "ProtocolEventCategoryFilter | None" = Field(
        validation_alias=AliasChoices("not_", "NOT"),
        serialization_alias="NOT",
        default=None,
    )
    distinct: bool | None = Field(
        validation_alias=AliasChoices("distinct", "DISTINCT"),
        serialization_alias="DISTINCT",
        default=None,
    )
    ids: tuple[ID, ...] | None = Field(
        default=None, description="Filter by list of IDs"
    )
    pinned: bool | None = Field(default=None, description="Filter by list of IDs")
    search: str | None = Field(default=None, description="Filter by list of IDs")
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class RelationCategoryFilter(BaseModel):
    """No documentation"""

    graph: GraphFilter | None = None
    id: ID | None = None
    label: str | None = None
    and_: "RelationCategoryFilter | None" = Field(
        validation_alias=AliasChoices("and_", "AND"),
        serialization_alias="AND",
        default=None,
    )
    or_: "RelationCategoryFilter | None" = Field(
        validation_alias=AliasChoices("or_", "OR"),
        serialization_alias="OR",
        default=None,
    )
    not_: "RelationCategoryFilter | None" = Field(
        validation_alias=AliasChoices("not_", "NOT"),
        serialization_alias="NOT",
        default=None,
    )
    distinct: bool | None = Field(
        validation_alias=AliasChoices("distinct", "DISTINCT"),
        serialization_alias="DISTINCT",
        default=None,
    )
    ids: tuple[ID, ...] | None = Field(
        default=None, description="Filter by list of IDs"
    )
    pinned: bool | None = Field(default=None, description="Filter by list of IDs")
    search: str | None = Field(default=None, description="Filter by list of IDs")
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class RelationDefinitionInput(BaseModel):
    """Definition of a relation type in the graph schema"""

    key: str = Field(description="Relation type name/key")
    description: str | None = Field(
        default=None, description="Description of this node role"
    )
    ontology_references: Annotated[
        tuple[OntologyReferenceInput, ...] | None, GraphQLDefault("[]")
    ] = Field(
        validation_alias=AliasChoices("ontology_references", "ontologyReferences"),
        serialization_alias="ontologyReferences",
        default=None,
        description="Ontology references for this event",
    )
    "Ontology references for this event\nDefault: []"
    color: tuple[int, ...] | None = Field(
        default=None,
        description="Optional RGBA color for this node role (e.g. [255, 0, 0, 128])",
    )
    image: str | None = Field(
        default=None,
        description="Optional media store ID for an image representing this node role",
    )
    label: str | None = Field(
        default=None,
        description="Optional human-readable label for this node role (defaults to 'key' if not provided)",
    )
    pin: bool | None = Field(
        default=None, description="Whether to pin this node role in the UI"
    )
    source: EntityDescriptorInput = Field(description="Source entity type(s)")
    target: EntityDescriptorInput = Field(description="Target entity type(s)")
    cardinality: Annotated[Cardinality | None, GraphQLDefault("ONE_TO_ONE")] = Field(
        default=None, description="Relation cardinality"
    )
    "Relation cardinality\nDefault: ONE_TO_ONE"
    properties: Annotated[
        tuple[PropertyDefinitionInput, ...] | None, GraphQLDefault("[]")
    ] = Field(default=None, description="Derived property definitions")
    "Derived property definitions\nDefault: []"
    definition: CategoryDefinitionInput | None = Field(
        default=None,
        description="This relation category's complete rule (RFC 0009): which relation claims draw its edges — by word, annotator, app and window — and whose standings count for them. Omitted means primitive: any claim naming its word draws",
    )
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class RetractCommentInput(BaseModel):
    """Input for claiming a remark no longer stands — withdrawn or resolved; the assertion records whose position it is"""

    id: str = Field(description="The ID of the comment to retract")
    at: datetime | None = Field(
        default=None,
        description="When this position took effect — world time. Left unset, the moment of the claim. A rule bounding OBSERVED_AT on EXISTENCE reads this.",
    )
    confidence: float | None = Field(
        default=None,
        description="How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.",
    )
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class RetractEntityInput(BaseModel):
    """Input for retracting an entity claim"""

    id: ID = Field(description="The ID of the entity to retract")
    at: datetime | None = Field(
        default=None,
        description="When this position took effect — world time. Left unset, the moment of the claim. A rule bounding OBSERVED_AT on EXISTENCE reads this.",
    )
    confidence: float | None = Field(
        default=None,
        description="How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.",
    )
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class RetractLinksInput(BaseModel):
    """Input for retracting several link claims as one act"""

    ids: tuple[str, ...] = Field(
        description="The `Link` primary keys of the claims to retract"
    )
    at: datetime | None = Field(
        default=None,
        description="When this position took effect — world time. Left unset, the moment of the claim. A rule bounding OBSERVED_AT on EXISTENCE reads this.",
    )
    confidence: float | None = Field(
        default=None,
        description="How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.",
    )
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class RetractMeasurementInput(BaseModel):
    """Input for retracting a measurement claim — a Standing(stands=false), not a deletion"""

    id: str = Field(
        description="The ID of the measurement claim to retract — its `Link` primary key"
    )
    at: datetime | None = Field(
        default=None,
        description="When this position took effect — world time. Left unset, the moment of the claim. A rule bounding OBSERVED_AT on EXISTENCE reads this.",
    )
    confidence: float | None = Field(
        default=None,
        description="How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.",
    )
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class RetractMetricInput(BaseModel):
    """Input for retracting a metric claim — a Standing(stands=false), not a deletion"""

    id: str = Field(
        description="The ID of the metric to retract — a bare uuid, its evidence primary key"
    )
    at: datetime | None = Field(
        default=None,
        description="When this position took effect — world time. Left unset, the moment of the claim. A rule bounding OBSERVED_AT on EXISTENCE reads this.",
    )
    confidence: float | None = Field(
        default=None,
        description="How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.",
    )
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class RetractNaturalEventInput(BaseModel):
    """Input for retracting a natural event claim — a Standing(stands=false), not a deletion"""

    id: str = Field(description="The ID of the natural event to retract")
    at: datetime | None = Field(
        default=None,
        description="When this position took effect — world time. Left unset, the moment of the claim. A rule bounding OBSERVED_AT on EXISTENCE reads this.",
    )
    confidence: float | None = Field(
        default=None,
        description="How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.",
    )
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class RetractParticipationInput(BaseModel):
    """Input for retracting one participation claim"""

    id: str = Field(description="The evidence ID of the participation claim to retract")
    at: datetime | None = Field(
        default=None,
        description="When this position took effect — world time. Left unset, the moment of the claim. A rule bounding OBSERVED_AT on EXISTENCE reads this.",
    )
    confidence: float | None = Field(
        default=None,
        description="How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.",
    )
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class RetractProtocolEventInput(BaseModel):
    """Input for retracting a protocol event claim — a Standing(stands=false), not a deletion"""

    id: str = Field(description="The ID of the protocol event to retract")
    at: datetime | None = Field(
        default=None,
        description="When this position took effect — world time. Left unset, the moment of the claim. A rule bounding OBSERVED_AT on EXISTENCE reads this.",
    )
    confidence: float | None = Field(
        default=None,
        description="How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.",
    )
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class RetractRelationInput(BaseModel):
    """Input for retracting a relation claim — a Standing(stands=false), not a deletion"""

    id: ID = Field(
        description="The ID of the relation claim to retract — its `Link` primary key"
    )
    at: datetime | None = Field(
        default=None,
        description="When this position took effect — world time. Left unset, the moment of the claim. A rule bounding OBSERVED_AT on EXISTENCE reads this.",
    )
    confidence: float | None = Field(
        default=None,
        description="How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.",
    )
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class RetractSameInstanceInput(BaseModel):
    """Input for withdrawing one sameness claim"""

    id: str = Field(description="The id of the sameness claim to retract")
    at: datetime | None = Field(
        default=None,
        description="When this position took effect — world time. Left unset, the moment of the claim. A rule bounding OBSERVED_AT on EXISTENCE reads this.",
    )
    confidence: float | None = Field(
        default=None,
        description="How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.",
    )
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class RetractStructureInput(BaseModel):
    """Input for retracting a structure claim — a Standing(stands=false), not a deletion"""

    id: ID = Field(
        description="The ID of the structure to retract — a bare uuid, its evidence primary key"
    )
    at: datetime | None = Field(
        default=None,
        description="When this position took effect — world time. Left unset, the moment of the claim. A rule bounding OBSERVED_AT on EXISTENCE reads this.",
    )
    confidence: float | None = Field(
        default=None,
        description="How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.",
    )
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class RetractStructureRelationInput(BaseModel):
    """Input for retracting a structure relation claim — a Standing(stands=false), not a deletion"""

    id: str = Field(
        description="The ID of the structure relation claim to retract — its `Link` primary key"
    )
    at: datetime | None = Field(
        default=None,
        description="When this position took effect — world time. Left unset, the moment of the claim. A rule bounding OBSERVED_AT on EXISTENCE reads this.",
    )
    confidence: float | None = Field(
        default=None,
        description="How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.",
    )
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class RoleMappingInput(BaseModel):
    """How a participant maps onto a declared event role"""

    role: str = Field(description="The role name")
    entity_id: str = Field(
        validation_alias=AliasChoices("entity_id", "entityId"),
        serialization_alias="entityId",
        description="The ID of the entity assigned to this role",
    )
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class SamenessRuleInput(BaseModel):
    """A view's sameness rule: whose SAME_AS / DIFFERENT_FROM claims it counts when folding nodes into individuals (RFC 0024). No rules means everyone"""

    rules: Annotated[tuple[ClaimRuleInput, ...] | None, GraphQLDefault("[]")] = Field(
        default=None,
        description="A sameness claim counts when any rule matches; no rules means every claim counts",
    )
    "A sameness claim counts when any rule matches; no rules means every claim counts\nDefault: []"
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class StructureDescriptorInput(BaseModel):
    """Input for creating a new structure relation definition in the graph schema"""

    default_category_key: str | None = Field(
        validation_alias=AliasChoices("default_category_key", "defaultCategoryKey"),
        serialization_alias="defaultCategoryKey",
        default=None,
        description="Default category to link to if no entities match the filters",
    )
    identifiers: tuple[str, ...] | None = Field(
        default=None,
        description="Structure identifiers to filter by (e.g. '@mikro/roi')",
    )
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class StructureFilter(BaseModel):
    """Filter options for querying structures"""

    ids: tuple[ID, ...] | None = Field(
        default=None, description="Filter by specific structure IDs"
    )
    has_property: str | None = Field(
        validation_alias=AliasChoices("has_property", "hasProperty"),
        serialization_alias="hasProperty",
        default=None,
        description="Filter structures that have a metric under this key",
    )
    search: str | None = Field(
        default=None,
        description="Substring match on the structure's `object`, not its properties",
    )
    matches: tuple[PropertyMatch, ...] | None = Field(
        default=None,
        description="Filter structures whose metrics match these conditions",
    )
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class StructureKindFilter(BaseModel):
    """No documentation"""

    and_: "StructureKindFilter | None" = Field(
        validation_alias=AliasChoices("and_", "AND"),
        serialization_alias="AND",
        default=None,
    )
    or_: "StructureKindFilter | None" = Field(
        validation_alias=AliasChoices("or_", "OR"),
        serialization_alias="OR",
        default=None,
    )
    not_: "StructureKindFilter | None" = Field(
        validation_alias=AliasChoices("not_", "NOT"),
        serialization_alias="NOT",
        default=None,
    )
    distinct: bool | None = Field(
        validation_alias=AliasChoices("distinct", "DISTINCT"),
        serialization_alias="DISTINCT",
        default=None,
    )
    ids: tuple[ID, ...] | None = Field(
        default=None, description="Filter by list of IDs"
    )
    search: str | None = Field(default=None, description="Search label and identifier")
    identifiers: tuple[str, ...] | None = Field(
        default=None, description="Filter by structure identifiers"
    )
    matches_descriptor: StructureDescriptorInput | None = Field(
        validation_alias=AliasChoices("matches_descriptor", "matchesDescriptor"),
        serialization_alias="matchesDescriptor",
        default=None,
        description="Filter by whether the kind matches a descriptor",
    )
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class StructureOrder(BaseModel):
    """Ordering options for structure queries"""

    created_at: Ordering | None = Field(
        validation_alias=AliasChoices("created_at", "createdAt"),
        serialization_alias="createdAt",
        default=None,
        description="Order by when the row was stored — arrival time. Prefer `seq`, the log's order",
    )
    seq: Ordering | None = Field(
        default=None,
        description="Order by the act's position in the log (`Assertion.seq`) — the log's own total order (RFC 0025)",
    )
    observed_at: Ordering | None = Field(
        validation_alias=AliasChoices("observed_at", "observedAt"),
        serialization_alias="observedAt",
        default=None,
        description="Order by world time — when the claim says the world was so (RFC 0015)",
    )
    id: Ordering | None = Field(default=None, description="Order by structure ID")
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class StructurePaginationInput(BaseModel):
    """Pagination options for querying structures"""

    offset: Annotated[int | None, GraphQLDefault("0")] = Field(
        default=None, description="Number of items to skip"
    )
    "Number of items to skip\nDefault: 0"
    limit: Annotated[int | None, GraphQLDefault("100")] = Field(
        default=None, description="Maximum number of items to return"
    )
    "Maximum number of items to return\nDefault: 100"
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class StructureReferenceInput(BaseModel):
    """A reference to a structure by identifier and object"""

    identifier: str = Field(description="Schema identifier, e.g. '@mikro/roi'")
    object: str = Field(
        description="The unique ID of the object this structure references"
    )
    metrics: Annotated[tuple[MetricInput, ...] | None, GraphQLDefault("[]")] = None
    "Default: []"
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class StructureRelationCategoryFilter(BaseModel):
    """No documentation"""

    graph: GraphFilter | None = None
    id: ID | None = None
    label: str | None = None
    and_: "StructureRelationCategoryFilter | None" = Field(
        validation_alias=AliasChoices("and_", "AND"),
        serialization_alias="AND",
        default=None,
    )
    or_: "StructureRelationCategoryFilter | None" = Field(
        validation_alias=AliasChoices("or_", "OR"),
        serialization_alias="OR",
        default=None,
    )
    not_: "StructureRelationCategoryFilter | None" = Field(
        validation_alias=AliasChoices("not_", "NOT"),
        serialization_alias="NOT",
        default=None,
    )
    distinct: bool | None = Field(
        validation_alias=AliasChoices("distinct", "DISTINCT"),
        serialization_alias="DISTINCT",
        default=None,
    )
    ids: tuple[ID, ...] | None = Field(
        default=None, description="Filter by list of IDs"
    )
    pinned: bool | None = Field(default=None, description="Filter by list of IDs")
    search: str | None = Field(default=None, description="Filter by list of IDs")
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class StructureRelationDefinitionInput(BaseModel):
    """Declares a structure relation category in a graph schema"""

    key: str = Field(description="Relation type name/key")
    description: str | None = Field(
        default=None, description="Description of this node role"
    )
    ontology_references: Annotated[
        tuple[OntologyReferenceInput, ...] | None, GraphQLDefault("[]")
    ] = Field(
        validation_alias=AliasChoices("ontology_references", "ontologyReferences"),
        serialization_alias="ontologyReferences",
        default=None,
        description="Ontology references for this event",
    )
    "Ontology references for this event\nDefault: []"
    color: tuple[int, ...] | None = Field(
        default=None,
        description="Optional RGBA color for this node role (e.g. [255, 0, 0, 128])",
    )
    image: str | None = Field(
        default=None,
        description="Optional media store ID for an image representing this node role",
    )
    label: str | None = Field(
        default=None,
        description="Optional human-readable label for this node role (defaults to 'key' if not provided)",
    )
    pin: bool | None = Field(
        default=None, description="Whether to pin this node role in the UI"
    )
    properties: Annotated[
        tuple[PropertyDefinitionInput, ...] | None, GraphQLDefault("[]")
    ] = Field(default=None, description="Derived property definitions")
    "Derived property definitions\nDefault: []"
    source: StructureDescriptorInput = Field(description="Source entity type(s)")
    target: StructureDescriptorInput = Field(description="Target entity type(s)")
    cardinality: Annotated[Cardinality | None, GraphQLDefault("ONE_TO_ONE")] = Field(
        default=None, description="Relation cardinality"
    )
    "Relation cardinality\nDefault: ONE_TO_ONE"
    definition: CategoryDefinitionInput | None = Field(
        default=None,
        description="This structure-relation category's complete rule (RFC 0012): which structure-relation claims count — by word, annotator, app and window — and whose standings fold. Omitted means primitive",
    )
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class SupersedeMetricValueInput(BaseModel):
    """Input for superseding a metric value"""

    key: str
    value: Any
    value_kind: PropertyType = Field(
        validation_alias=AliasChoices("value_kind", "valueKind"),
        serialization_alias="valueKind",
        description="What type of value this is. Required: it decides which column the value is stored in and which measurement term it is recorded under, and nothing infers it. Two callers may declare the same key differently — a float `confidence` and a category-label `confidence` are two terms, and both are recorded.",
    )
    confidence: float | None = Field(
        default=None,
        description="How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.",
    )
    confidence_type: str | None = Field(
        validation_alias=AliasChoices("confidence_type", "confidenceType"),
        serialization_alias="confidenceType",
        default=None,
        description="What kind of number `confidence` is — a method's own score, a p-value. Measurement-only",
    )
    unit: str | None = None
    observed_at: datetime | None = Field(
        validation_alias=AliasChoices("observed_at", "observedAt"),
        serialization_alias="observedAt",
        default=None,
        description="When the world was observed. Defaults to when it was claimed.",
    )
    derived_from: Annotated[tuple[str, ...] | None, GraphQLDefault("[]")] = Field(
        validation_alias=AliasChoices("derived_from", "derivedFrom"),
        serialization_alias="derivedFrom",
        default=None,
        description='The claims this one came from — ids of instances, links, metrics or structures in your organization. Each is recorded as a DERIVED_FROM link under the same assertion as the claim itself, because "this, because of that" is one act (RFC 0017). Read back as `derivedFrom`; the cited claim lists it under `derivations`.',
    )
    'The claims this one came from — ids of instances, links, metrics or structures in your organization. Each is recorded as a DERIVED_FROM link under the same assertion as the claim itself, because "this, because of that" is one act (RFC 0017). Read back as `derivedFrom`; the cited claim lists it under `derivations`.\nDefault: []'
    id: str = Field(description="The ID of the metric to update")
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class TermFilter(BaseModel):
    """No documentation"""

    and_: "TermFilter | None" = Field(
        validation_alias=AliasChoices("and_", "AND"),
        serialization_alias="AND",
        default=None,
    )
    or_: "TermFilter | None" = Field(
        validation_alias=AliasChoices("or_", "OR"),
        serialization_alias="OR",
        default=None,
    )
    not_: "TermFilter | None" = Field(
        validation_alias=AliasChoices("not_", "NOT"),
        serialization_alias="NOT",
        default=None,
    )
    distinct: bool | None = Field(
        validation_alias=AliasChoices("distinct", "DISTINCT"),
        serialization_alias="DISTINCT",
        default=None,
    )
    ids: tuple[ID, ...] | None = Field(
        default=None, description="Filter by list of IDs"
    )
    search: str | None = Field(
        default=None, description="Search key, label and description"
    )
    kinds: tuple[TermKind, ...] | None = Field(
        default=None, description="Filter by what sort of thing the word names"
    )
    keys: tuple[str, ...] | None = Field(
        default=None, description="Filter by the words themselves"
    )
    declared: bool | None = Field(
        default=None,
        description="Filter to terms at least one graph declares a category for",
    )
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class UpdateEntityCategoryInput(BaseModel):
    """Input for updating an existing entity definition in the graph schema"""

    id: ID = Field(description="The ID of the definition to update")
    key: str | None = Field(
        default=None, description="The label of the node participating in the event"
    )
    description: str | None = Field(
        default=None, description="Description of this node role"
    )
    ontology_references: tuple[OntologyReferenceInput, ...] | None = Field(
        validation_alias=AliasChoices("ontology_references", "ontologyReferences"),
        serialization_alias="ontologyReferences",
        default=None,
        description="Ontology references for this event",
    )
    color: tuple[int, ...] | None = Field(
        default=None,
        description="Optional RGBA color for this node role (e.g. [255, 0, 0, 128])",
    )
    image: str | None = Field(
        default=None,
        description="Optional media store ID for an image representing this node role",
    )
    label: str | None = Field(
        default=None,
        description="Optional human-readable label for this node role (defaults to 'key' if not provided)",
    )
    pin: bool | None = Field(
        default=None, description="Whether to pin this node role in the UI"
    )
    instance_kind: str | None = Field(
        validation_alias=AliasChoices("instance_kind", "instanceKind"),
        serialization_alias="instanceKind",
        default=None,
        description="Optional instance kind for this entity category (e.g. 'neuron', 'synapse', 'behavior'). This is used for further categorization and filtering of entities within the graph.",
    )
    property_definitions: tuple[PropertyDefinitionInput, ...] | None = Field(
        validation_alias=AliasChoices("property_definitions", "propertyDefinitions"),
        serialization_alias="propertyDefinitions",
        default=None,
        description="Property definitions",
    )
    definition: CategoryDefinitionInput | None = Field(
        default=None,
        description="New meaning for this category (RFC 0007). Omitted means unchanged; to make the category primitive again, use clearDefinition",
    )
    clear_definition: Annotated[bool | None, GraphQLDefault("False")] = Field(
        validation_alias=AliasChoices("clear_definition", "clearDefinition"),
        serialization_alias="clearDefinition",
        default=None,
        description="Reset the category to primitive — membership becomes whatever was asserted under its word",
    )
    "Reset the category to primitive — membership becomes whatever was asserted under its word\nDefault: False"
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class UpdateGraphInput(BaseModel):
    """Input for updating an existing graph"""

    id: str = Field(description="The ID of the graph to update")
    name: str | None = Field(default=None, description="New graph name")
    description: str | None = Field(default=None, description="New graph description")
    archived: bool | None = Field(
        default=None, description="Optional archived flag update"
    )
    pin: bool | None = Field(
        default=None,
        description="Optional pin flag update for the user making the request",
    )
    sameness_rule: SamenessRuleInput | None = Field(
        validation_alias=AliasChoices("sameness_rule", "samenessRule"),
        serialization_alias="samenessRule",
        default=None,
        description="Replace whose sameness claims this view counts (RFC 0024); an empty rule list means everyone. Omitted means unchanged. Changing it refolds the view's individuals — the projection is rebuilt",
    )
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class UpdateGraphVisualInput(BaseModel):
    """Input for updating the visual properties of a graph element"""

    id: str = Field(description="The ID of the graph element to update")
    node_positions: Annotated[
        tuple[CategoryNodePositionInput, ...] | None, GraphQLDefault("[]")
    ] = Field(
        validation_alias=AliasChoices("node_positions", "nodePositions"),
        serialization_alias="nodePositions",
        default=None,
        description="List of node positions to update",
    )
    "List of node positions to update\nDefault: []"
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class UpdateMeasurementCategoryInput(BaseModel):
    """Input for updating an existing measurement definition in the graph schema"""

    id: str = Field(description="The ID of the measurement category to update")
    key: str | None = Field(
        default=None, description="The label of the node participating in the event"
    )
    description: str | None = Field(
        default=None, description="Description of this node role"
    )
    ontology_references: tuple[OntologyReferenceInput, ...] | None = Field(
        validation_alias=AliasChoices("ontology_references", "ontologyReferences"),
        serialization_alias="ontologyReferences",
        default=None,
        description="Ontology references for this event",
    )
    color: tuple[int, ...] | None = Field(
        default=None,
        description="Optional RGBA color for this node role (e.g. [255, 0, 0, 128])",
    )
    image: str | None = Field(
        default=None,
        description="Optional media store ID for an image representing this node role",
    )
    label: str | None = Field(
        default=None,
        description="Optional human-readable label for this node role (defaults to 'key' if not provided)",
    )
    pin: bool | None = Field(
        default=None, description="Whether to pin this node role in the UI"
    )
    definition: CategoryDefinitionInput | None = Field(
        default=None,
        description="New rule for this category (RFC 0012). Omitted means unchanged; to make it primitive again, use clearDefinition",
    )
    clear_definition: Annotated[bool | None, GraphQLDefault("False")] = Field(
        validation_alias=AliasChoices("clear_definition", "clearDefinition"),
        serialization_alias="clearDefinition",
        default=None,
        description="Reset the category to primitive — any claim naming its word counts, standings organization grain",
    )
    "Reset the category to primitive — any claim naming its word counts, standings organization grain\nDefault: False"
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class UpdateMetricKindInput(BaseModel):
    """Input for updating an existing metric definition in the graph schema"""

    id: str = Field(description="The ID of the definition to update")
    key: str | None = Field(
        default=None, description="The label of the node participating in the event"
    )
    description: str | None = Field(
        default=None, description="Description of this node role"
    )
    ontology_references: tuple[OntologyReferenceInput, ...] | None = Field(
        validation_alias=AliasChoices("ontology_references", "ontologyReferences"),
        serialization_alias="ontologyReferences",
        default=None,
        description="Ontology references for this event",
    )
    color: tuple[int, ...] | None = Field(
        default=None,
        description="Optional RGBA color for this node role (e.g. [255, 0, 0, 128])",
    )
    image: str | None = Field(
        default=None,
        description="Optional media store ID for an image representing this node role",
    )
    label: str | None = Field(
        default=None,
        description="Optional human-readable label for this node role (defaults to 'key' if not provided)",
    )
    pin: bool | None = Field(
        default=None, description="Whether to pin this node role in the UI"
    )
    identifier: str | None = Field(
        default=None,
        description="Read by nothing: a metric kind is identified by `(organization, structure_kind, key, value_kind)`. `update_metric_kind` writes label, description and colour only",
    )
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class UpdateNaturalEventCategoryInput(BaseModel):
    """Input for updating an existing natural event definition in the graph schema"""

    id: str = Field(description="The ID of the natural event category to update")
    key: str | None = Field(
        default=None, description="The label of the node participating in the event"
    )
    description: str | None = Field(
        default=None, description="Description of this node role"
    )
    ontology_references: tuple[OntologyReferenceInput, ...] | None = Field(
        validation_alias=AliasChoices("ontology_references", "ontologyReferences"),
        serialization_alias="ontologyReferences",
        default=None,
        description="Ontology references for this event",
    )
    color: tuple[int, ...] | None = Field(
        default=None,
        description="Optional RGBA color for this node role (e.g. [255, 0, 0, 128])",
    )
    image: str | None = Field(
        default=None,
        description="Optional media store ID for an image representing this node role",
    )
    label: str | None = Field(
        default=None,
        description="Optional human-readable label for this node role (defaults to 'key' if not provided)",
    )
    pin: bool | None = Field(
        default=None, description="Whether to pin this node role in the UI"
    )
    definition: CategoryDefinitionInput | None = Field(
        default=None,
        description="New rule for this category (RFC 0009). Omitted means unchanged; to make it primitive again, use clearDefinition",
    )
    clear_definition: Annotated[bool | None, GraphQLDefault("False")] = Field(
        validation_alias=AliasChoices("clear_definition", "clearDefinition"),
        serialization_alias="clearDefinition",
        default=None,
        description="Reset the category to primitive — any claim naming its word counts, standings organization grain",
    )
    "Reset the category to primitive — any claim naming its word counts, standings organization grain\nDefault: False"
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class UpdateProtocolEventCategoryInput(BaseModel):
    """Input for updating an existing protocol event definition in the graph schema"""

    id: str = Field(description="The ID of the protocol event category to update")
    key: str | None = Field(
        default=None, description="The label of the node participating in the event"
    )
    description: str | None = Field(
        default=None, description="Description of this node role"
    )
    ontology_references: tuple[OntologyReferenceInput, ...] | None = Field(
        validation_alias=AliasChoices("ontology_references", "ontologyReferences"),
        serialization_alias="ontologyReferences",
        default=None,
        description="Ontology references for this event",
    )
    color: tuple[int, ...] | None = Field(
        default=None,
        description="Optional RGBA color for this node role (e.g. [255, 0, 0, 128])",
    )
    image: str | None = Field(
        default=None,
        description="Optional media store ID for an image representing this node role",
    )
    label: str | None = Field(
        default=None,
        description="Optional human-readable label for this node role (defaults to 'key' if not provided)",
    )
    pin: bool | None = Field(
        default=None, description="Whether to pin this node role in the UI"
    )
    definition: CategoryDefinitionInput | None = Field(
        default=None,
        description="New rule for this category (RFC 0012). Omitted means unchanged; to make it primitive again, use clearDefinition",
    )
    clear_definition: Annotated[bool | None, GraphQLDefault("False")] = Field(
        validation_alias=AliasChoices("clear_definition", "clearDefinition"),
        serialization_alias="clearDefinition",
        default=None,
        description="Reset the category to primitive — any claim naming its word counts, standings organization grain",
    )
    "Reset the category to primitive — any claim naming its word counts, standings organization grain\nDefault: False"
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class UpdateRelationCategoryInput(BaseModel):
    """Input for updating an existing relation definition in the graph schema"""

    id: str = Field(description="The ID of the relation category to update")
    key: str | None = Field(
        default=None, description="The label of the node participating in the event"
    )
    description: str | None = Field(
        default=None, description="Description of this node role"
    )
    ontology_references: tuple[OntologyReferenceInput, ...] | None = Field(
        validation_alias=AliasChoices("ontology_references", "ontologyReferences"),
        serialization_alias="ontologyReferences",
        default=None,
        description="Ontology references for this event",
    )
    color: tuple[int, ...] | None = Field(
        default=None,
        description="Optional RGBA color for this node role (e.g. [255, 0, 0, 128])",
    )
    image: str | None = Field(
        default=None,
        description="Optional media store ID for an image representing this node role",
    )
    label: str | None = Field(
        default=None,
        description="Optional human-readable label for this node role (defaults to 'key' if not provided)",
    )
    pin: bool | None = Field(
        default=None, description="Whether to pin this node role in the UI"
    )
    definition: CategoryDefinitionInput | None = Field(
        default=None,
        description="New rule for this category (RFC 0009). Omitted means unchanged; to make it primitive again, use clearDefinition",
    )
    clear_definition: Annotated[bool | None, GraphQLDefault("False")] = Field(
        validation_alias=AliasChoices("clear_definition", "clearDefinition"),
        serialization_alias="clearDefinition",
        default=None,
        description="Reset the category to primitive — any claim naming its word counts, standings organization grain",
    )
    "Reset the category to primitive — any claim naming its word counts, standings organization grain\nDefault: False"
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class UpdateStructureKindInput(BaseModel):
    """Input for updating an existing structure definition in the graph schema"""

    id: str = Field(description="The ID of the definition to update")
    key: str | None = Field(
        default=None, description="The label of the node participating in the event"
    )
    description: str | None = Field(
        default=None, description="Description of this node role"
    )
    ontology_references: tuple[OntologyReferenceInput, ...] | None = Field(
        validation_alias=AliasChoices("ontology_references", "ontologyReferences"),
        serialization_alias="ontologyReferences",
        default=None,
        description="Ontology references for this event",
    )
    color: tuple[int, ...] | None = Field(
        default=None,
        description="Optional RGBA color for this node role (e.g. [255, 0, 0, 128])",
    )
    image: str | None = Field(
        default=None,
        description="Optional media store ID for an image representing this node role",
    )
    label: str | None = Field(
        default=None,
        description="Optional human-readable label for this node role (defaults to 'key' if not provided)",
    )
    pin: bool | None = Field(
        default=None, description="Whether to pin this node role in the UI"
    )
    identifier: str | None = Field(
        default=None,
        description="Read by nothing: `(organization, identifier)` is a structure kind's identity and cannot be reassigned. `update_structure_kind` writes label, description and colour only",
    )
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class UpdateStructureRelationCategoryInput(BaseModel):
    """Input for updating an existing structure relation definition in the graph schema"""

    id: str = Field(description="The ID of the structure relation category to update")
    key: str | None = Field(
        default=None, description="The label of the node participating in the event"
    )
    description: str | None = Field(
        default=None, description="Description of this node role"
    )
    ontology_references: tuple[OntologyReferenceInput, ...] | None = Field(
        validation_alias=AliasChoices("ontology_references", "ontologyReferences"),
        serialization_alias="ontologyReferences",
        default=None,
        description="Ontology references for this event",
    )
    color: tuple[int, ...] | None = Field(
        default=None,
        description="Optional RGBA color for this node role (e.g. [255, 0, 0, 128])",
    )
    image: str | None = Field(
        default=None,
        description="Optional media store ID for an image representing this node role",
    )
    label: str | None = Field(
        default=None,
        description="Optional human-readable label for this node role (defaults to 'key' if not provided)",
    )
    pin: bool | None = Field(
        default=None, description="Whether to pin this node role in the UI"
    )
    definition: CategoryDefinitionInput | None = Field(
        default=None,
        description="New rule for this category (RFC 0012). Omitted means unchanged; to make it primitive again, use clearDefinition",
    )
    clear_definition: Annotated[bool | None, GraphQLDefault("False")] = Field(
        validation_alias=AliasChoices("clear_definition", "clearDefinition"),
        serialization_alias="clearDefinition",
        default=None,
        description="Reset the category to primitive — any claim naming its word counts, standings organization grain",
    )
    "Reset the category to primitive — any claim naming its word counts, standings organization grain\nDefault: False"
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class UpdateTermInput(BaseModel):
    """Input for editing how one of the organization's words presents itself"""

    id: str = Field(description="The ID of the term to update")
    label: str | None = Field(default=None, description="Human-readable name")
    description: str | None = Field(default=None, description="What this word means")
    purl: str | None = Field(
        default=None,
        description="Persistent URL, where this corresponds to a published ontology term",
    )
    color: tuple[int, ...] | None = Field(
        default=None, description="Optional RGBA colour"
    )
    image: str | None = Field(
        default=None, description="Optional media store ID for an illustrative image"
    )
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class VocabularyPaginationInput(BaseModel):
    """Pagination options for querying the organization's vocabulary"""

    offset: Annotated[int | None, GraphQLDefault("0")] = Field(
        default=None, description="Number of items to skip"
    )
    "Number of items to skip\nDefault: 0"
    limit: Annotated[int | None, GraphQLDefault("100")] = Field(
        default=None, description="Maximum number of items to return"
    )
    "Maximum number of items to return\nDefault: 100"
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class CategoryRefBase(CategoryTrait, BaseModel):
    """Base interface for structure categories"""

    id: ID
    "Database ID of the category"
    key: str
    "The unique key/identifier for this category, used for linking to entities or structures (e.g. 'Cell', 'ROI')"
    label: str
    "Label/name of the category"
    age_name: str = Field(alias="ageName")
    "The label this view draws the category's nodes or edges under — its name in the projection namespace. One view's rename of the word; never what a node *is* (that is the claim's kind)"


class CategoryRefCatch(CategoryRefBase):
    """Catch all class for CategoryRefBase"""

    typename: str = Field(alias="__typename", exclude=True)
    "Base interface for structure categories"
    id: ID
    "Database ID of the category"
    key: str
    "The unique key/identifier for this category, used for linking to entities or structures (e.g. 'Cell', 'ROI')"
    label: str
    "Label/name of the category"
    age_name: str = Field(alias="ageName")
    "The label this view draws the category's nodes or edges under — its name in the projection namespace. One view's rename of the word; never what a node *is* (that is the claim's kind)"


class CategoryRefEntityCategory(CategoryRefBase, EntityCategoryTrait, BaseModel):
    """An entity category definition"""

    typename: Literal["EntityCategory"] = Field(
        alias="__typename", default="EntityCategory", exclude=True
    )


class CategoryRefMeasurementCategory(
    CategoryRefBase, MeasurementCategoryTrait, BaseModel
):
    """A measurement category definition"""

    typename: Literal["MeasurementCategory"] = Field(
        alias="__typename", default="MeasurementCategory", exclude=True
    )


class CategoryRefNaturalEventCategory(
    CategoryRefBase, NaturalEventCategoryTrait, BaseModel
):
    """A relation category definition"""

    typename: Literal["NaturalEventCategory"] = Field(
        alias="__typename", default="NaturalEventCategory", exclude=True
    )


class CategoryRefProtocolEventCategory(
    CategoryRefBase, ProtocolEventCategoryTrait, BaseModel
):
    """A relation category definition"""

    typename: Literal["ProtocolEventCategory"] = Field(
        alias="__typename", default="ProtocolEventCategory", exclude=True
    )


class CategoryRefRelationCategory(CategoryRefBase, RelationCategoryTrait, BaseModel):
    """A relation category definition"""

    typename: Literal["RelationCategory"] = Field(
        alias="__typename", default="RelationCategory", exclude=True
    )


class CategoryRefStructureRelationCategory(
    CategoryRefBase, StructureRelationCategoryTrait, BaseModel
):
    """A relation category definition"""

    typename: Literal["StructureRelationCategory"] = Field(
        alias="__typename", default="StructureRelationCategory", exclude=True
    )


class PropertyDefinition(BaseModel):
    """A property definition from the graph schema"""

    typename: Literal["PropertyDefinition"] = Field(
        alias="__typename", default="PropertyDefinition", exclude=True
    )
    key: str
    "Property key/name"
    label: str | None = Field(default=None)
    "Optional human-readable label for this property (defaults to 'key' if not provided)"
    value_kind: ValueKind = Field(alias="valueKind")
    unit: str | None = Field(default=None)
    "Unit of measurement"
    description: str | None = Field(default=None)
    "Description of this property"
    derivation: DerivationType
    "Derivation type: LATEST, PRIORITY_LATEST, ROLLUP, LATEST_ASSERTION_TOOL"
    index: bool
    "Whether to create an index on this property for faster queries"
    searchable: bool
    "Whether this property should be full-text searchable"
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for PropertyDefinition"""

        document = "fragment PropertyDefinition on PropertyDefinition {\n  key\n  label\n  valueKind\n  unit\n  description\n  derivation\n  index\n  searchable\n  __typename\n}"
        name = "PropertyDefinition"
        type = "PropertyDefinition"


class EntityDescriptor(BaseModel):
    """Input type for creating a new graph query"""

    typename: Literal["EntityDescriptor"] = Field(
        alias="__typename", default="EntityDescriptor", exclude=True
    )
    keys: tuple[str, ...] | None = Field(default=None)
    "Filter by entity key/label"
    ontology_terms: tuple[str, ...] | None = Field(default=None, alias="ontologyTerms")
    "Filter by ontology references on the entity (format: 'PREFIX:TERM_ID')"
    default_category_key: str | None = Field(default=None, alias="defaultCategoryKey")
    "Default category to link to if no entities match the filters"
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for EntityDescriptor"""

        document = "fragment EntityDescriptor on EntityDescriptor {\n  keys\n  ontologyTerms\n  defaultCategoryKey\n  __typename\n}"
        name = "EntityDescriptor"
        type = "EntityDescriptor"


class StructureDescriptor(BaseModel):
    """Input type for creating a new graph query"""

    typename: Literal["StructureDescriptor"] = Field(
        alias="__typename", default="StructureDescriptor", exclude=True
    )
    default_category_key: str | None = Field(default=None, alias="defaultCategoryKey")
    "Default category to link to if no entities match the filters"
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for StructureDescriptor"""

        document = "fragment StructureDescriptor on StructureDescriptor {\n  defaultCategoryKey\n  __typename\n}"
        name = "StructureDescriptor"
        type = "StructureDescriptor"


class LinkRef(LinkTrait, BaseModel):
    """A claim relating two things — as the log has it, whether or not any view draws it"""

    typename: Literal["Link"] = Field(alias="__typename", default="Link", exclude=True)
    id: ID
    "The claim's durable identity — the `Link` primary key"
    kind: LinkKind
    "What this claim says — and therefore what each of its two refs points at"
    source_ref: ID = Field(alias="sourceRef")
    "The source ref, as the log holds it: an opaque uuid. `source` resolves it"
    target_ref: ID = Field(alias="targetRef")
    "The target ref, as the log holds it: an opaque uuid. `target` resolves it"
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for LinkRef"""

        document = "fragment LinkRef on Link {\n  id\n  kind\n  sourceRef\n  targetRef\n  __typename\n}"
        name = "LinkRef"
        type = "Link"


class Metric(MetricTrait, BaseModel):
    """A measured value about a structure — a claim, not a graph node"""

    typename: Literal["Metric"] = Field(
        alias="__typename", default="Metric", exclude=True
    )
    id: ID
    "This claim's durable identity — the `Metric` primary key, a bare uuid"
    kind_id: str | None = Field(default=None, alias="kindId")
    "ID of the metric kind this instantiates"
    key: str | None = Field(default=None)
    "The measurement key"
    value: Any
    "The metric value"
    unit: str | None = Field(default=None)
    "Unit of measurement, where the source gave one"
    confidence: float | None = Field(default=None)
    "How sure the claimant was of this measurement, 0 to 1. Null when they gave no number (RFC 0016)"
    confidence_type: str | None = Field(default=None, alias="confidenceType")
    "What kind of confidence this is"
    observed_at: datetime | None = Field(default=None, alias="observedAt")
    "When the world was observed"
    asserted_at: datetime | None = Field(default=None, alias="assertedAt")
    "When this measurement was claimed"
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for Metric"""

        document = "fragment Metric on Metric {\n  id\n  kindId\n  key\n  value\n  unit\n  confidence\n  confidenceType\n  observedAt\n  assertedAt\n  __typename\n}"
        name = "Metric"
        type = "Metric"


class Structure(StructureTrait, BaseModel):
    """An individual with an external identity — an ROI, an image, a file. A claim about the world, never a graph node (RFC 0023)"""

    typename: Literal["Structure"] = Field(
        alias="__typename", default="Structure", exclude=True
    )
    id: ID
    "This claim's durable identity — the `Structure` primary key, a bare uuid"
    identifier: StructureIdentifier
    "Schema identifier (e.g. '@mikro/roi')"
    object: str
    "External object ID this structure references"
    kind_id: str = Field(alias="kindId")
    "ID of the structure kind this instantiates"
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for Structure"""

        document = "fragment Structure on Structure {\n  id\n  identifier\n  object\n  kindId\n  __typename\n}"
        name = "Structure"
        type = "Structure"


class Assertion(AssertionTrait, BaseModel):
    """Who claimed something, with what tool, and when — one row of the append-only log"""

    typename: Literal["Assertion"] = Field(
        alias="__typename", default="Assertion", exclude=True
    )
    id: ID
    "The assertion's durable identity"
    subject: str
    "Who made the claim — a user id, or the identity of an automated agent"
    app_id: str | None = Field(default=None, alias="appId")
    "Which application made the claim"
    action_id: str | None = Field(default=None, alias="actionId")
    "Which action within that application made the claim"
    action_name: str | None = Field(default=None, alias="actionName")
    "Human-readable name of the action that produced this assertion"
    asserted_at: datetime = Field(alias="assertedAt")
    "When the claim was made — belief time, the axis `as_of` filters on"
    recorded_at: datetime = Field(alias="recordedAt")
    "When the claim was durably stored — arrival time. Never equal to assertedAt, and for debugging ingest rather than for answering questions"
    seq: int
    "Position in the organization-spanning log. Monotonic, assigned by the database, and the order a replay runs in. Assigned at insert, not at commit — `changes(afterSeq:)` is the reader that knows the difference"
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for Assertion"""

        document = "fragment Assertion on Assertion {\n  id\n  subject\n  appId\n  actionId\n  actionName\n  assertedAt\n  recordedAt\n  seq\n  __typename\n}"
        name = "Assertion"
        type = "Assertion"


class TermRef(TermTrait, BaseModel):
    """A word this organization uses for a kind of thing"""

    typename: Literal["Term"] = Field(alias="__typename", default="Term", exclude=True)
    id: ID
    "Database ID of the term"
    key: str
    "The word itself, e.g. 'AIS'"
    kind: TermKind
    "What sort of thing this word names. Part of its identity, so 'AIS' as an entity and 'AIS' as a relation are two terms."
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for TermRef"""

        document = "fragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}"
        name = "TermRef"
        type = "Term"


class StructureKind(StructureKindTrait, BaseModel):
    """A kind of external datum this organization knows about"""

    typename: Literal["StructureKind"] = Field(
        alias="__typename", default="StructureKind", exclude=True
    )
    id: ID
    "Database ID of the kind"
    identifier: str
    "The structure identifier, e.g. '@mikro/roi'"
    label: str | None = Field(default=None)
    "Human-readable name"
    description: str | None = Field(default=None)
    "What this kind of datum is"
    purl: str | None = Field(default=None)
    "Persistent URL, where this corresponds to a published term"
    color: tuple[int, ...] | None = Field(default=None)
    "Display colour as RGBA"
    created_at: datetime = Field(alias="createdAt")
    "When this organization first saw this kind"
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for StructureKind"""

        document = "fragment StructureKind on StructureKind {\n  id\n  identifier\n  label\n  description\n  purl\n  color\n  createdAt\n  __typename\n}"
        name = "StructureKind"
        type = "StructureKind"


class MetricKindStructureKind(StructureKindTrait, BaseModel):
    """A kind of external datum this organization knows about"""

    typename: Literal["StructureKind"] = Field(
        alias="__typename", default="StructureKind", exclude=True
    )
    id: ID
    "Database ID of the kind"
    identifier: str
    "The structure identifier, e.g. '@mikro/roi'"
    model_config = ConfigDict(frozen=True)


class MetricKind(MetricKindTrait, BaseModel):
    """A kind of measurement that can be made about a structure kind"""

    typename: Literal["MetricKind"] = Field(
        alias="__typename", default="MetricKind", exclude=True
    )
    id: ID
    "Database ID of the kind"
    key: str
    "The measurement key, e.g. 'vector_length'"
    value_kind: ValueKind = Field(alias="valueKind")
    "What type of value this measurement carries"
    label: str | None = Field(default=None)
    "Human-readable name"
    description: str | None = Field(default=None)
    "What this measurement is"
    purl: str | None = Field(default=None)
    "Persistent URL, where this corresponds to a published term"
    color: tuple[int, ...] | None = Field(default=None)
    "Display colour as RGBA"
    created_at: datetime = Field(alias="createdAt")
    "When this organization first saw this kind"
    structure_kind: MetricKindStructureKind = Field(alias="structureKind")
    "The kind of structure this measurement describes"
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for MetricKind"""

        document = "fragment MetricKind on MetricKind {\n  id\n  key\n  valueKind\n  label\n  description\n  purl\n  color\n  createdAt\n  structureKind {\n    id\n    identifier\n    __typename\n  }\n  __typename\n}"
        name = "MetricKind"
        type = "MetricKind"


class MediaStore(HasPresignedDownloadAccessor, BaseModel):
    """No documentation"""

    typename: Literal["MediaStore"] = Field(
        alias="__typename", default="MediaStore", exclude=True
    )
    id: ID
    key: str
    presigned_url: str = Field(alias="presignedUrl")
    "Compatibility field returning the canonical S3 object path."
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for MediaStore"""

        document = "fragment MediaStore on MediaStore {\n  id\n  key\n  presignedUrl\n  __typename\n}"
        name = "MediaStore"
        type = "MediaStore"


class NodeRefBase(NodeTrait, BaseModel):
    """Base interface for all graph nodes"""

    id: ID
    "This node's durable identity — a bare uuid, world-unique and stable across reprojects. In a view it is the individual's representative: the lowest of `members`, which may differ from the member id you asked for"
    label: str
    "The first of `drawnLabels`, for a reader that shows one — or the claim's word when the view has not drawn it yet"


class NodeRefCatch(NodeRefBase):
    """Catch all class for NodeRefBase"""

    typename: str = Field(alias="__typename", exclude=True)
    "Base interface for all graph nodes"
    id: ID
    "This node's durable identity — a bare uuid, world-unique and stable across reprojects. In a view it is the individual's representative: the lowest of `members`, which may differ from the member id you asked for"
    label: str
    "The first of `drawnLabels`, for a reader that shows one — or the claim's word when the view has not drawn it yet"


class NodeRefEntity(NodeRefBase, EntityTrait, BaseModel):
    """An entity in the knowledge graph with derived properties"""

    typename: Literal["Entity"] = Field(
        alias="__typename", default="Entity", exclude=True
    )


class NodeRefNaturalEvent(NodeRefBase, BaseModel):
    """A natural event in the knowledge graph"""

    typename: Literal["NaturalEvent"] = Field(
        alias="__typename", default="NaturalEvent", exclude=True
    )


class NodeRefProtocolEvent(NodeRefBase, BaseModel):
    """A protocol event in the graph"""

    typename: Literal["ProtocolEvent"] = Field(
        alias="__typename", default="ProtocolEvent", exclude=True
    )


class GraphProjection(ProjectionTrait, BaseModel):
    """How far along the organization's log one view's drawing is. The projection is a cache of the evidence; this says how current a cache it is. `projectedThroughSeq` is a safe cursor: every assertion at or below it has been drawn here. `lag` is the distance to the log head; `pending` is how many assertions organization-wide nobody has finished drawing. `schemaStale` is the other axis — a category's rules moved and the vertices have not been redrawn under them."""

    typename: Literal["GraphProjection"] = Field(
        alias="__typename", default="GraphProjection", exclude=True
    )
    kind: str
    "Which kind of projection. Only the table kind exists today — ordinary Postgres tables plus a per-graph property graph"
    status: ProjectionStatus
    projected_through_seq: int = Field(alias="projectedThroughSeq")
    "Every assertion with seq at or below this has been drawn in this view. 0 while undrawn or mid-rebuild"
    derived_through_seq: int = Field(alias="derivedThroughSeq")
    "Log head the last bulk operation (rebuild, backfill, replay) read at. Informational — the cursor is `projectedThroughSeq`"
    lag: int
    "Assertions between the cursor and the organization's log head"
    pending: int
    "Assertions across the organization whose synchronous projection did not finish"
    schema_stale: bool = Field(alias="schemaStale")
    "The drawing was last fully derived under a schema that is no longer the active one"
    schema_hash: str | None = Field(default=None, alias="schemaHash")
    "GraphSchema hash the drawing was last fully derived under"
    derived_at: datetime | None = Field(default=None, alias="derivedAt")
    "When derived properties were last written here"
    rebuilt_at: datetime | None = Field(default=None, alias="rebuiltAt")
    "When this view was last dropped and replayed in full"
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for GraphProjection"""

        document = "fragment GraphProjection on GraphProjection {\n  kind\n  status\n  projectedThroughSeq\n  derivedThroughSeq\n  lag\n  pending\n  schemaStale\n  schemaHash\n  derivedAt\n  rebuiltAt\n  __typename\n}"
        name = "GraphProjection"
        type = "GraphProjection"


class ListGraph(GraphTrait, BaseModel):
    """One view over the organization's evidence log"""

    typename: Literal["Graph"] = Field(
        alias="__typename", default="Graph", exclude=True
    )
    id: ID
    "Database ID of the graph"
    name: str
    "Name of the graph"
    description: str | None = Field(default=None)
    "Description of the graph"
    age_name: str = Field(alias="ageName")
    "Internal handle of the graph's projection namespace — the per-graph Postgres schema its property graph lives in. Random, read-only, and not an identifier: address a graph by `id`."
    is_archived: bool = Field(alias="isArchived")
    "Whether this graph has been archived. Archiving is the reversible alternative to deleting it — a delete destroys every rule for reading the evidence, which survives without them"
    pinned: bool
    "Whether the requesting user has pinned this graph for quick access"
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for ListGraph"""

        document = "fragment ListGraph on Graph {\n  id\n  name\n  description\n  ageName\n  isArchived\n  pinned\n  __typename\n}"
        name = "ListGraph"
        type = "Graph"


class EntityViewRichProperties(BaseModel):
    """A rich property with metadata from schema and graph"""

    typename: Literal["RichProperty"] = Field(
        alias="__typename", default="RichProperty", exclude=True
    )
    key: str | None = Field(default=None)
    "The property key/name"
    value: Any | None = Field(default=None)
    "The property value"
    n_evidence: int | None = Field(default=None, alias="nEvidence")
    "How many measurements contribute to this value"
    spread: float | None = Field(default=None)
    "Spread of the contributing measurements (max - min), where numeric"
    measured_from: datetime | None = Field(default=None, alias="measuredFrom")
    "When the earliest contributing measurement was observed"
    measured_to: datetime | None = Field(default=None, alias="measuredTo")
    "When the latest contributing measurement was observed"
    model_config = ConfigDict(frozen=True)


class EntityView(EntityTrait, BaseModel):
    """An entity in the knowledge graph with derived properties"""

    typename: Literal["Entity"] = Field(
        alias="__typename", default="Entity", exclude=True
    )
    id: ID
    "This node's durable identity — a bare uuid, world-unique and stable across reprojects. In a view it is the individual's representative: the lowest of `members`, which may differ from the member id you asked for"
    label: str
    "The first of `drawnLabels`, for a reader that shows one — or the claim's word when the view has not drawn it yet"
    category_ids: tuple[str, ...] = Field(alias="categoryIds")
    "The ids of every category the view this was read through draws it under (RFC 0019). Empty when no view does"
    valid_from: datetime | None = Field(default=None, alias="validFrom")
    "When this entity became valid. When did it start existing?"
    valid_to: datetime | None = Field(default=None, alias="validTo")
    "When this entity stopped being valid. . When did it stop existing?"
    properties: Any
    "The current derived properties for this entity"
    rich_properties: tuple[EntityViewRichProperties, ...] = Field(
        alias="richProperties"
    )
    "List of properties derived for this entity — the union over its categories in this view. Empty when this reading has no category — a property definition is one view's rule, and a claim no view draws has none"
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for EntityView"""

        document = "fragment EntityView on Entity {\n  id\n  label\n  categoryIds\n  validFrom\n  validTo\n  properties\n  richProperties {\n    key\n    value\n    nEvidence\n    spread\n    measuredFrom\n    measuredTo\n    __typename\n  }\n  __typename\n}"
        name = "EntityView"
        type = "Entity"


class EdgeDrawingGraph(GraphTrait, BaseModel):
    """One view over the organization's evidence log"""

    typename: Literal["Graph"] = Field(
        alias="__typename", default="Graph", exclude=True
    )
    id: ID
    "Database ID of the graph"
    name: str
    "Name of the graph"
    model_config = ConfigDict(frozen=True)


class EdgeDrawingCategoryBase(CategoryTrait, BaseModel):
    """Base interface for structure categories"""

    model_config = ConfigDict(frozen=True)


class EdgeDrawingCategoryBaseEntityCategory(
    CategoryRefEntityCategory, EdgeDrawingCategoryBase, EntityCategoryTrait, BaseModel
):
    """An entity category definition"""

    typename: Literal["EntityCategory"] = Field(
        alias="__typename", default="EntityCategory", exclude=True
    )


class EdgeDrawingCategoryBaseMeasurementCategory(
    CategoryRefMeasurementCategory,
    EdgeDrawingCategoryBase,
    MeasurementCategoryTrait,
    BaseModel,
):
    """A measurement category definition"""

    typename: Literal["MeasurementCategory"] = Field(
        alias="__typename", default="MeasurementCategory", exclude=True
    )


class EdgeDrawingCategoryBaseNaturalEventCategory(
    CategoryRefNaturalEventCategory,
    EdgeDrawingCategoryBase,
    NaturalEventCategoryTrait,
    BaseModel,
):
    """A relation category definition"""

    typename: Literal["NaturalEventCategory"] = Field(
        alias="__typename", default="NaturalEventCategory", exclude=True
    )


class EdgeDrawingCategoryBaseProtocolEventCategory(
    CategoryRefProtocolEventCategory,
    EdgeDrawingCategoryBase,
    ProtocolEventCategoryTrait,
    BaseModel,
):
    """A relation category definition"""

    typename: Literal["ProtocolEventCategory"] = Field(
        alias="__typename", default="ProtocolEventCategory", exclude=True
    )


class EdgeDrawingCategoryBaseRelationCategory(
    CategoryRefRelationCategory,
    EdgeDrawingCategoryBase,
    RelationCategoryTrait,
    BaseModel,
):
    """A relation category definition"""

    typename: Literal["RelationCategory"] = Field(
        alias="__typename", default="RelationCategory", exclude=True
    )


class EdgeDrawingCategoryBaseStructureRelationCategory(
    CategoryRefStructureRelationCategory,
    EdgeDrawingCategoryBase,
    StructureRelationCategoryTrait,
    BaseModel,
):
    """A relation category definition"""

    typename: Literal["StructureRelationCategory"] = Field(
        alias="__typename", default="StructureRelationCategory", exclude=True
    )


class EdgeDrawingCategoryBaseCatchAll(EdgeDrawingCategoryBase, BaseModel):
    """Catch all class for EdgeDrawingCategoryBase"""

    typename: str = Field(alias="__typename", exclude=True)


class EdgeDrawing(BaseModel):
    """One view that draws a claimed edge, and how it draws it"""

    typename: Literal["EdgeDrawing"] = Field(
        alias="__typename", default="EdgeDrawing", exclude=True
    )
    graph: EdgeDrawingGraph
    "The view this drawing belongs to"
    category: Annotated[
        EdgeDrawingCategoryBaseEntityCategory
        | EdgeDrawingCategoryBaseMeasurementCategory
        | EdgeDrawingCategoryBaseNaturalEventCategory
        | EdgeDrawingCategoryBaseProtocolEventCategory
        | EdgeDrawingCategoryBaseRelationCategory
        | EdgeDrawingCategoryBaseStructureRelationCategory,
        Field(discriminator="typename"),
    ] | EdgeDrawingCategoryBaseCatchAll
    "The category this view draws the claim under. A participation names the *event's* category, which is a node category — hence the base interface rather than EdgeCategory"
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for EdgeDrawing"""

        document = "fragment CategoryRef on Category {\n  id\n  key\n  label\n  ageName\n  __typename\n}\n\nfragment EdgeDrawing on EdgeDrawing {\n  graph {\n    id\n    name\n    __typename\n  }\n  category {\n    ...CategoryRef\n    __typename\n  }\n  __typename\n}"
        name = "EdgeDrawing"
        type = "EdgeDrawing"


class EventRole(BaseModel):
    """Input type for defining roles in an event category"""

    typename: Literal["EventRole"] = Field(
        alias="__typename", default="EventRole", exclude=True
    )
    key: str
    "The label of the node participating in the event"
    role: str
    "What type of role does this node play in the event"
    descriptor: EntityDescriptor
    "Optional filters to apply when linking entities to structures for this role"
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for EventRole"""

        document = "fragment EntityDescriptor on EntityDescriptor {\n  keys\n  ontologyTerms\n  defaultCategoryKey\n  __typename\n}\n\nfragment EventRole on EventRole {\n  key\n  role\n  descriptor {\n    ...EntityDescriptor\n    __typename\n  }\n  __typename\n}"
        name = "EventRole"
        type = "EventRole"


class StructureWithMetrics(Structure, StructureTrait, BaseModel):
    """An individual with an external identity — an ROI, an image, a file. A claim about the world, never a graph node (RFC 0023)"""

    typename: Literal["Structure"] = Field(
        alias="__typename", default="Structure", exclude=True
    )
    metrics: tuple[Metric, ...]
    "Every un-retracted measurement of this structure, in observation order"
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for StructureWithMetrics"""

        document = "fragment Metric on Metric {\n  id\n  kindId\n  key\n  value\n  unit\n  confidence\n  confidenceType\n  observedAt\n  assertedAt\n  __typename\n}\n\nfragment Structure on Structure {\n  id\n  identifier\n  object\n  kindId\n  __typename\n}\n\nfragment StructureWithMetrics on Structure {\n  ...Structure\n  metrics {\n    ...Metric\n    __typename\n  }\n  __typename\n}"
        name = "StructureWithMetrics"
        type = "Structure"


class AssertedMetric(AssertedTrait, BaseModel):
    """An assertion about a metric — a measured value about a structure"""

    typename: Literal["AssertedMetric"] = Field(
        alias="__typename", default="AssertedMetric", exclude=True
    )
    assertion: Assertion
    "The claim this call recorded. Not the subject's original assertion — for an attestation or a retraction those are different acts, possibly years apart."
    metric: Metric
    "The metric this act was about"
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for AssertedMetric"""

        document = "fragment Assertion on Assertion {\n  id\n  subject\n  appId\n  actionId\n  actionName\n  assertedAt\n  recordedAt\n  seq\n  __typename\n}\n\nfragment Metric on Metric {\n  id\n  kindId\n  key\n  value\n  unit\n  confidence\n  confidenceType\n  observedAt\n  assertedAt\n  __typename\n}\n\nfragment AssertedMetric on AssertedMetric {\n  assertion {\n    ...Assertion\n    __typename\n  }\n  metric {\n    ...Metric\n    __typename\n  }\n  __typename\n}"
        name = "AssertedMetric"
        type = "AssertedMetric"


class CommentParent(BaseModel):
    """A remark somebody made about a structure — a claim, as the log has it"""

    typename: Literal["Comment"] = Field(
        alias="__typename", default="Comment", exclude=True
    )
    id: ID
    "The claim's durable identity — a bare uuid"
    model_config = ConfigDict(frozen=True)


class Comment(BaseModel):
    """A remark somebody made about a structure — a claim, as the log has it"""

    typename: Literal["Comment"] = Field(
        alias="__typename", default="Comment", exclude=True
    )
    id: ID
    "The claim's durable identity — a bare uuid"
    created_at: datetime = Field(alias="createdAt")
    "When the remark was recorded"
    text: str
    "The plain-text rendering of the body's leaves. Searchable; the body itself is `descendants`"
    resolved: bool
    "Whether the winning position says this remark no longer stands — resolved by a reviewer or withdrawn by its author; `standings` says which and by whom. The fold a comment can honestly carry, because nothing scopes it per view"
    mentions: tuple[str, ...]
    "The subjects mentioned in the body, extracted at write time"
    parent: CommentParent | None = Field(default=None)
    "The comment this replies to, for threading. Null for a top-level remark"
    assertion: Assertion
    "The act of commenting: who said it, with which app, and when"
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for Comment"""

        document = "fragment Assertion on Assertion {\n  id\n  subject\n  appId\n  actionId\n  actionName\n  assertedAt\n  recordedAt\n  seq\n  __typename\n}\n\nfragment Comment on Comment {\n  id\n  createdAt\n  text\n  resolved\n  mentions\n  parent {\n    id\n    __typename\n  }\n  assertion {\n    ...Assertion\n    __typename\n  }\n  __typename\n}"
        name = "Comment"
        type = "Comment"


class Standing(StandingTrait, BaseModel):
    """Somebody's position on whether a claim still holds"""

    typename: Literal["Standing"] = Field(
        alias="__typename", default="Standing", exclude=True
    )
    id: ID
    "This position's own identity"
    stands: bool
    "Whether the claimant says the claim holds. True attests, False retracts"
    at: datetime
    "When the position took effect — world time, the axis that decides which claim is newest"
    assertion: Assertion
    "Who took this position, with what tool, and when they recorded it"
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for Standing"""

        document = "fragment Assertion on Assertion {\n  id\n  subject\n  appId\n  actionId\n  actionName\n  assertedAt\n  recordedAt\n  seq\n  __typename\n}\n\nfragment Standing on Standing {\n  id\n  stands\n  at\n  assertion {\n    ...Assertion\n    __typename\n  }\n  __typename\n}"
        name = "Standing"
        type = "Standing"


class InstanceRef(InstanceTrait, BaseModel):
    """A claimed individual — an entity or an event, as the log has it"""

    typename: Literal["Instance"] = Field(
        alias="__typename", default="Instance", exclude=True
    )
    id: ID
    "The claim's durable identity — a bare uuid, world-unique and stable across reprojects"
    kind: InstanceKind
    "What sort of individual this is. Entities and events are told apart here, not by a vertex label — a label is one view's rename of a word"
    term: TermRef
    "The organization's word this was first claimed under. Which view draws it, and as what, is decided from the claims"
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for InstanceRef"""

        document = "fragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment InstanceRef on Instance {\n  id\n  kind\n  term {\n    ...TermRef\n    __typename\n  }\n  __typename\n}"
        name = "InstanceRef"
        type = "Instance"


class Link(LinkRef, LinkTrait, BaseModel):
    """A claim relating two things — as the log has it, whether or not any view draws it"""

    typename: Literal["Link"] = Field(alias="__typename", default="Link", exclude=True)
    role: str | None = Field(default=None)
    "Which role the source plays, for participation claims — the asserter's own word; the claim names no graph, so no schema names this"
    created_at: datetime = Field(alias="createdAt")
    "When the claim was recorded"
    term: TermRef | None = Field(default=None)
    "The organization's word this claim is stated in. Null for a plain INFORMS link, which names no word"
    assertion: Assertion
    "The act that made this claim"
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for Link"""

        document = "fragment Assertion on Assertion {\n  id\n  subject\n  appId\n  actionId\n  actionName\n  assertedAt\n  recordedAt\n  seq\n  __typename\n}\n\nfragment LinkRef on Link {\n  id\n  kind\n  sourceRef\n  targetRef\n  __typename\n}\n\nfragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment Link on Link {\n  ...LinkRef\n  role\n  createdAt\n  term {\n    ...TermRef\n    __typename\n  }\n  assertion {\n    ...Assertion\n    __typename\n  }\n  __typename\n}"
        name = "Link"
        type = "Link"


class Term(TermRef, TermTrait, BaseModel):
    """A word this organization uses for a kind of thing"""

    typename: Literal["Term"] = Field(alias="__typename", default="Term", exclude=True)
    label: str | None = Field(default=None)
    "Human-readable name"
    description: str | None = Field(default=None)
    "What this word means"
    purl: str | None = Field(default=None)
    "Persistent URL, where this corresponds to a published ontology term"
    color: tuple[int, ...] | None = Field(default=None)
    "Display colour as RGBA"
    created_at: datetime = Field(alias="createdAt")
    "When this organization first used this word"
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for Term"""

        document = "fragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment Term on Term {\n  ...TermRef\n  label\n  description\n  purl\n  color\n  createdAt\n  __typename\n}"
        name = "Term"
        type = "Term"


class CategoryBaseGraph(GraphTrait, BaseModel):
    """One view over the organization's evidence log"""

    typename: Literal["Graph"] = Field(
        alias="__typename", default="Graph", exclude=True
    )
    id: ID
    "Database ID of the graph"
    name: str
    "Name of the graph"
    model_config = ConfigDict(frozen=True)


class CategoryBaseBase(CategoryTrait, BaseModel):
    """Base interface for structure categories"""

    description: str | None = Field(default=None)
    "Description of the category"
    purl: str | None = Field(default=None)
    "Persistent URL for this category"
    color: tuple[int, ...] | None = Field(default=None)
    "Color as RGBA list (0-255)"
    pinned: bool
    "Whether the requesting user has pinned this graph for quick access"
    image: MediaStore | None = Field(default=None)
    "An image representing this category, for visualization purposes"
    graph: CategoryBaseGraph
    "The graph this category belongs to"
    term: TermRef | None = Field(default=None)
    "The organization's word this category declares. Claims name the term, not this row — so a category is what the word means *here*, and another graph declaring the same word sees the same claims."


class CategoryBaseCatch(CategoryBaseBase):
    """Catch all class for CategoryBaseBase"""

    typename: str = Field(alias="__typename", exclude=True)
    "Base interface for structure categories"
    description: str | None = Field(default=None)
    "Description of the category"
    purl: str | None = Field(default=None)
    "Persistent URL for this category"
    color: tuple[int, ...] | None = Field(default=None)
    "Color as RGBA list (0-255)"
    pinned: bool
    "Whether the requesting user has pinned this graph for quick access"
    image: MediaStore | None = Field(default=None)
    "An image representing this category, for visualization purposes"
    graph: CategoryBaseGraph
    "The graph this category belongs to"
    term: TermRef | None = Field(default=None)
    "The organization's word this category declares. Claims name the term, not this row — so a category is what the word means *here*, and another graph declaring the same word sees the same claims."


class CategoryBaseEntityCategory(
    CategoryRefEntityCategory, CategoryBaseBase, EntityCategoryTrait, BaseModel
):
    """An entity category definition"""

    typename: Literal["EntityCategory"] = Field(
        alias="__typename", default="EntityCategory", exclude=True
    )


class CategoryBaseMeasurementCategory(
    CategoryRefMeasurementCategory,
    CategoryBaseBase,
    MeasurementCategoryTrait,
    BaseModel,
):
    """A measurement category definition"""

    typename: Literal["MeasurementCategory"] = Field(
        alias="__typename", default="MeasurementCategory", exclude=True
    )


class CategoryBaseNaturalEventCategory(
    CategoryRefNaturalEventCategory,
    CategoryBaseBase,
    NaturalEventCategoryTrait,
    BaseModel,
):
    """A relation category definition"""

    typename: Literal["NaturalEventCategory"] = Field(
        alias="__typename", default="NaturalEventCategory", exclude=True
    )


class CategoryBaseProtocolEventCategory(
    CategoryRefProtocolEventCategory,
    CategoryBaseBase,
    ProtocolEventCategoryTrait,
    BaseModel,
):
    """A relation category definition"""

    typename: Literal["ProtocolEventCategory"] = Field(
        alias="__typename", default="ProtocolEventCategory", exclude=True
    )


class CategoryBaseRelationCategory(
    CategoryRefRelationCategory, CategoryBaseBase, RelationCategoryTrait, BaseModel
):
    """A relation category definition"""

    typename: Literal["RelationCategory"] = Field(
        alias="__typename", default="RelationCategory", exclude=True
    )


class CategoryBaseStructureRelationCategory(
    CategoryRefStructureRelationCategory,
    CategoryBaseBase,
    StructureRelationCategoryTrait,
    BaseModel,
):
    """A relation category definition"""

    typename: Literal["StructureRelationCategory"] = Field(
        alias="__typename", default="StructureRelationCategory", exclude=True
    )


class NodeDrawingGraph(GraphTrait, BaseModel):
    """One view over the organization's evidence log"""

    typename: Literal["Graph"] = Field(
        alias="__typename", default="Graph", exclude=True
    )
    id: ID
    "Database ID of the graph"
    name: str
    "Name of the graph"
    model_config = ConfigDict(frozen=True)


class NodeDrawingCategoryBase(CategoryTrait, BaseModel):
    """Base interface for structure categories"""

    model_config = ConfigDict(frozen=True)


class NodeDrawingCategoryBaseEntityCategory(
    CategoryRefEntityCategory, NodeDrawingCategoryBase, EntityCategoryTrait, BaseModel
):
    """An entity category definition"""

    typename: Literal["EntityCategory"] = Field(
        alias="__typename", default="EntityCategory", exclude=True
    )


class NodeDrawingCategoryBaseMeasurementCategory(
    CategoryRefMeasurementCategory,
    NodeDrawingCategoryBase,
    MeasurementCategoryTrait,
    BaseModel,
):
    """A measurement category definition"""

    typename: Literal["MeasurementCategory"] = Field(
        alias="__typename", default="MeasurementCategory", exclude=True
    )


class NodeDrawingCategoryBaseNaturalEventCategory(
    CategoryRefNaturalEventCategory,
    NodeDrawingCategoryBase,
    NaturalEventCategoryTrait,
    BaseModel,
):
    """A relation category definition"""

    typename: Literal["NaturalEventCategory"] = Field(
        alias="__typename", default="NaturalEventCategory", exclude=True
    )


class NodeDrawingCategoryBaseProtocolEventCategory(
    CategoryRefProtocolEventCategory,
    NodeDrawingCategoryBase,
    ProtocolEventCategoryTrait,
    BaseModel,
):
    """A relation category definition"""

    typename: Literal["ProtocolEventCategory"] = Field(
        alias="__typename", default="ProtocolEventCategory", exclude=True
    )


class NodeDrawingCategoryBaseRelationCategory(
    CategoryRefRelationCategory,
    NodeDrawingCategoryBase,
    RelationCategoryTrait,
    BaseModel,
):
    """A relation category definition"""

    typename: Literal["RelationCategory"] = Field(
        alias="__typename", default="RelationCategory", exclude=True
    )


class NodeDrawingCategoryBaseStructureRelationCategory(
    CategoryRefStructureRelationCategory,
    NodeDrawingCategoryBase,
    StructureRelationCategoryTrait,
    BaseModel,
):
    """A relation category definition"""

    typename: Literal["StructureRelationCategory"] = Field(
        alias="__typename", default="StructureRelationCategory", exclude=True
    )


class NodeDrawingCategoryBaseCatchAll(NodeDrawingCategoryBase, BaseModel):
    """Catch all class for NodeDrawingCategoryBase"""

    typename: str = Field(alias="__typename", exclude=True)


class NodeDrawingNodeBase(NodeTrait, BaseModel):
    """Base interface for all graph nodes"""

    model_config = ConfigDict(frozen=True)


class NodeDrawingNodeBaseEntity(
    NodeRefEntity, NodeDrawingNodeBase, EntityTrait, BaseModel
):
    """An entity in the knowledge graph with derived properties"""

    typename: Literal["Entity"] = Field(
        alias="__typename", default="Entity", exclude=True
    )


class NodeDrawingNodeBaseNaturalEvent(
    NodeRefNaturalEvent, NodeDrawingNodeBase, BaseModel
):
    """A natural event in the knowledge graph"""

    typename: Literal["NaturalEvent"] = Field(
        alias="__typename", default="NaturalEvent", exclude=True
    )


class NodeDrawingNodeBaseProtocolEvent(
    NodeRefProtocolEvent, NodeDrawingNodeBase, BaseModel
):
    """A protocol event in the graph"""

    typename: Literal["ProtocolEvent"] = Field(
        alias="__typename", default="ProtocolEvent", exclude=True
    )


class NodeDrawingNodeBaseCatchAll(NodeDrawingNodeBase, BaseModel):
    """Catch all class for NodeDrawingNodeBase"""

    typename: str = Field(alias="__typename", exclude=True)


class NodeDrawing(BaseModel):
    """One view that draws a claimed node, and how it draws it"""

    typename: Literal["NodeDrawing"] = Field(
        alias="__typename", default="NodeDrawing", exclude=True
    )
    graph: NodeDrawingGraph
    "The view this drawing belongs to"
    category: Annotated[
        NodeDrawingCategoryBaseEntityCategory
        | NodeDrawingCategoryBaseMeasurementCategory
        | NodeDrawingCategoryBaseNaturalEventCategory
        | NodeDrawingCategoryBaseProtocolEventCategory
        | NodeDrawingCategoryBaseRelationCategory
        | NodeDrawingCategoryBaseStructureRelationCategory,
        Field(discriminator="typename"),
    ] | NodeDrawingCategoryBaseCatchAll
    "The category this view draws the claim under — what the word means here"
    node: Annotated[
        NodeDrawingNodeBaseEntity
        | NodeDrawingNodeBaseNaturalEvent
        | NodeDrawingNodeBaseProtocolEvent,
        Field(discriminator="typename"),
    ] | NodeDrawingNodeBaseCatchAll
    "The node as this view holds it, with the properties this view derives. Its graph and label are true here, which they cannot be on a result that stands for every view at once"
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for NodeDrawing"""

        document = "fragment CategoryRef on Category {\n  id\n  key\n  label\n  ageName\n  __typename\n}\n\nfragment NodeRef on Node {\n  id\n  label\n  __typename\n}\n\nfragment NodeDrawing on NodeDrawing {\n  graph {\n    id\n    name\n    __typename\n  }\n  category {\n    ...CategoryRef\n    __typename\n  }\n  node {\n    ...NodeRef\n    __typename\n  }\n  __typename\n}"
        name = "NodeDrawing"
        type = "NodeDrawing"


class AssertedStructure(AssertedTrait, BaseModel):
    """An assertion about a structure — a pointer to an external datum"""

    typename: Literal["AssertedStructure"] = Field(
        alias="__typename", default="AssertedStructure", exclude=True
    )
    assertion: Assertion
    "The claim this call recorded. Not the subject's original assertion — for an attestation or a retraction those are different acts, possibly years apart."
    structure: StructureWithMetrics
    "The structure this act was about"
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for AssertedStructure"""

        document = "fragment Metric on Metric {\n  id\n  kindId\n  key\n  value\n  unit\n  confidence\n  confidenceType\n  observedAt\n  assertedAt\n  __typename\n}\n\nfragment Structure on Structure {\n  id\n  identifier\n  object\n  kindId\n  __typename\n}\n\nfragment Assertion on Assertion {\n  id\n  subject\n  appId\n  actionId\n  actionName\n  assertedAt\n  recordedAt\n  seq\n  __typename\n}\n\nfragment StructureWithMetrics on Structure {\n  ...Structure\n  metrics {\n    ...Metric\n    __typename\n  }\n  __typename\n}\n\nfragment AssertedStructure on AssertedStructure {\n  assertion {\n    ...Assertion\n    __typename\n  }\n  structure {\n    ...StructureWithMetrics\n    __typename\n  }\n  __typename\n}"
        name = "AssertedStructure"
        type = "AssertedStructure"


class AssertedComment(AssertedTrait, BaseModel):
    """An assertion about a comment — a remark recorded about a structure"""

    typename: Literal["AssertedComment"] = Field(
        alias="__typename", default="AssertedComment", exclude=True
    )
    assertion: Assertion
    "The claim this call recorded. Not the subject's original assertion — for an attestation or a retraction those are different acts, possibly years apart."
    comment: Comment
    "The remark this act was about — recorded it, withdrew it, or reopened it; the assertion says which"
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for AssertedComment"""

        document = "fragment Assertion on Assertion {\n  id\n  subject\n  appId\n  actionId\n  actionName\n  assertedAt\n  recordedAt\n  seq\n  __typename\n}\n\nfragment Comment on Comment {\n  id\n  createdAt\n  text\n  resolved\n  mentions\n  parent {\n    id\n    __typename\n  }\n  assertion {\n    ...Assertion\n    __typename\n  }\n  __typename\n}\n\nfragment AssertedComment on AssertedComment {\n  assertion {\n    ...Assertion\n    __typename\n  }\n  comment {\n    ...Comment\n    __typename\n  }\n  __typename\n}"
        name = "AssertedComment"
        type = "AssertedComment"


class Instance(InstanceRef, InstanceTrait, BaseModel):
    """A claimed individual — an entity or an event, as the log has it"""

    typename: Literal["Instance"] = Field(
        alias="__typename", default="Instance", exclude=True
    )
    created_at: datetime = Field(alias="createdAt")
    "When the claim was recorded"
    component: tuple[ID, ...]
    "Every instance claimed to be this same thing, this one included. A component of one means nobody has merged it"
    assertion: Assertion
    "The act that first claimed this exists. Not the latest — for that, read `standings`"
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for Instance"""

        document = "fragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment Assertion on Assertion {\n  id\n  subject\n  appId\n  actionId\n  actionName\n  assertedAt\n  recordedAt\n  seq\n  __typename\n}\n\nfragment InstanceRef on Instance {\n  id\n  kind\n  term {\n    ...TermRef\n    __typename\n  }\n  __typename\n}\n\nfragment Instance on Instance {\n  ...InstanceRef\n  createdAt\n  component\n  assertion {\n    ...Assertion\n    __typename\n  }\n  __typename\n}"
        name = "Instance"
        type = "Instance"


class AssertedRelation(AssertedTrait, HasDrawings, BaseModel):
    """An assertion about a relation, and everywhere that relation is now drawn"""

    typename: Literal["AssertedRelation"] = Field(
        alias="__typename", default="AssertedRelation", exclude=True
    )
    assertion: Assertion
    "The claim this call recorded. Not the subject's original assertion — for an attestation or a retraction those are different acts, possibly years apart."
    link: Link
    "What was claimed, as the log has it. Not a drawing of it: derived properties, a label and a category are one view's account and live on each entry in `drawings`. This is addressable whether or not any view draws it, which is the case a write has to answer for."
    drawings: tuple[EdgeDrawing, ...]
    "Every view that draws this claim, after this assertion. Empty means no view does — which is an ordinary answer, not an error: a claim names a word the organization owns, and a view that declares no category for that word simply will not draw it. For a retraction this is usually empty and deliberately not hardcoded so: existence is folded under each view's own selector, so a view that does not count the retracting subject still draws the node."
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for AssertedRelation"""

        document = "fragment CategoryRef on Category {\n  id\n  key\n  label\n  ageName\n  __typename\n}\n\nfragment LinkRef on Link {\n  id\n  kind\n  sourceRef\n  targetRef\n  __typename\n}\n\nfragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment Assertion on Assertion {\n  id\n  subject\n  appId\n  actionId\n  actionName\n  assertedAt\n  recordedAt\n  seq\n  __typename\n}\n\nfragment EdgeDrawing on EdgeDrawing {\n  graph {\n    id\n    name\n    __typename\n  }\n  category {\n    ...CategoryRef\n    __typename\n  }\n  __typename\n}\n\nfragment Link on Link {\n  ...LinkRef\n  role\n  createdAt\n  term {\n    ...TermRef\n    __typename\n  }\n  assertion {\n    ...Assertion\n    __typename\n  }\n  __typename\n}\n\nfragment AssertedRelation on AssertedRelation {\n  assertion {\n    ...Assertion\n    __typename\n  }\n  link {\n    ...Link\n    __typename\n  }\n  drawings {\n    ...EdgeDrawing\n    __typename\n  }\n  __typename\n}"
        name = "AssertedRelation"
        type = "AssertedRelation"


class AssertedParticipation(AssertedTrait, HasDrawings, BaseModel):
    """An assertion about one participation, and everywhere it is now drawn"""

    typename: Literal["AssertedParticipation"] = Field(
        alias="__typename", default="AssertedParticipation", exclude=True
    )
    assertion: Assertion
    "The claim this call recorded. Not the subject's original assertion — for an attestation or a retraction those are different acts, possibly years apart."
    link: Link
    "What was claimed, as the log has it. Not a drawing of it: derived properties, a label and a category are one view's account and live on each entry in `drawings`. This is addressable whether or not any view draws it, which is the case a write has to answer for."
    drawings: tuple[EdgeDrawing, ...]
    "Every view that draws this claim, after this assertion. Empty means no view does — which is an ordinary answer, not an error: a claim names a word the organization owns, and a view that declares no category for that word simply will not draw it. For a retraction this is usually empty and deliberately not hardcoded so: existence is folded under each view's own selector, so a view that does not count the retracting subject still draws the node."
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for AssertedParticipation"""

        document = "fragment CategoryRef on Category {\n  id\n  key\n  label\n  ageName\n  __typename\n}\n\nfragment LinkRef on Link {\n  id\n  kind\n  sourceRef\n  targetRef\n  __typename\n}\n\nfragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment Assertion on Assertion {\n  id\n  subject\n  appId\n  actionId\n  actionName\n  assertedAt\n  recordedAt\n  seq\n  __typename\n}\n\nfragment EdgeDrawing on EdgeDrawing {\n  graph {\n    id\n    name\n    __typename\n  }\n  category {\n    ...CategoryRef\n    __typename\n  }\n  __typename\n}\n\nfragment Link on Link {\n  ...LinkRef\n  role\n  createdAt\n  term {\n    ...TermRef\n    __typename\n  }\n  assertion {\n    ...Assertion\n    __typename\n  }\n  __typename\n}\n\nfragment AssertedParticipation on AssertedParticipation {\n  assertion {\n    ...Assertion\n    __typename\n  }\n  link {\n    ...Link\n    __typename\n  }\n  drawings {\n    ...EdgeDrawing\n    __typename\n  }\n  __typename\n}"
        name = "AssertedParticipation"
        type = "AssertedParticipation"


class AssertedLinks(AssertedTrait, HasDrawings, BaseModel):
    """An assertion about several link claims made as one act, and everywhere they are now drawn"""

    typename: Literal["AssertedLinks"] = Field(
        alias="__typename", default="AssertedLinks", exclude=True
    )
    assertion: Assertion
    "The single claim covering the whole batch"
    links: tuple[Link, ...]
    "The claims this act was about, as the log has them"
    drawings: tuple[EdgeDrawing, ...]
    "Every view that draws this claim, after this assertion. Empty means no view does — which is an ordinary answer, not an error: a claim names a word the organization owns, and a view that declares no category for that word simply will not draw it. For a retraction this is usually empty and deliberately not hardcoded so: existence is folded under each view's own selector, so a view that does not count the retracting subject still draws the node."
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for AssertedLinks"""

        document = "fragment CategoryRef on Category {\n  id\n  key\n  label\n  ageName\n  __typename\n}\n\nfragment LinkRef on Link {\n  id\n  kind\n  sourceRef\n  targetRef\n  __typename\n}\n\nfragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment Assertion on Assertion {\n  id\n  subject\n  appId\n  actionId\n  actionName\n  assertedAt\n  recordedAt\n  seq\n  __typename\n}\n\nfragment EdgeDrawing on EdgeDrawing {\n  graph {\n    id\n    name\n    __typename\n  }\n  category {\n    ...CategoryRef\n    __typename\n  }\n  __typename\n}\n\nfragment Link on Link {\n  ...LinkRef\n  role\n  createdAt\n  term {\n    ...TermRef\n    __typename\n  }\n  assertion {\n    ...Assertion\n    __typename\n  }\n  __typename\n}\n\nfragment AssertedLinks on AssertedLinks {\n  assertion {\n    ...Assertion\n    __typename\n  }\n  links {\n    ...Link\n    __typename\n  }\n  drawings {\n    ...EdgeDrawing\n    __typename\n  }\n  __typename\n}"
        name = "AssertedLinks"
        type = "AssertedLinks"


class AssertedMeasurement(AssertedTrait, BaseModel):
    """An assertion about a measurement — a structure measuring a node"""

    typename: Literal["AssertedMeasurement"] = Field(
        alias="__typename", default="AssertedMeasurement", exclude=True
    )
    assertion: Assertion
    "The claim this call recorded. Not the subject's original assertion — for an attestation or a retraction those are different acts, possibly years apart."
    link: Link
    "What was claimed, as the log has it. Not a drawing of it: derived properties, a label and a category are one view's account and live on each entry in `drawings`. This is addressable whether or not any view draws it, which is the case a write has to answer for."
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for AssertedMeasurement"""

        document = "fragment LinkRef on Link {\n  id\n  kind\n  sourceRef\n  targetRef\n  __typename\n}\n\nfragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment Assertion on Assertion {\n  id\n  subject\n  appId\n  actionId\n  actionName\n  assertedAt\n  recordedAt\n  seq\n  __typename\n}\n\nfragment Link on Link {\n  ...LinkRef\n  role\n  createdAt\n  term {\n    ...TermRef\n    __typename\n  }\n  assertion {\n    ...Assertion\n    __typename\n  }\n  __typename\n}\n\nfragment AssertedMeasurement on AssertedMeasurement {\n  assertion {\n    ...Assertion\n    __typename\n  }\n  link {\n    ...Link\n    __typename\n  }\n  __typename\n}"
        name = "AssertedMeasurement"
        type = "AssertedMeasurement"


class AssertedStructureRelation(AssertedTrait, BaseModel):
    """An assertion about a structure relation — a claim between two external data"""

    typename: Literal["AssertedStructureRelation"] = Field(
        alias="__typename", default="AssertedStructureRelation", exclude=True
    )
    assertion: Assertion
    "The claim this call recorded. Not the subject's original assertion — for an attestation or a retraction those are different acts, possibly years apart."
    link: Link
    "What was claimed, as the log has it. Not a drawing of it: derived properties, a label and a category are one view's account and live on each entry in `drawings`. This is addressable whether or not any view draws it, which is the case a write has to answer for."
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for AssertedStructureRelation"""

        document = "fragment LinkRef on Link {\n  id\n  kind\n  sourceRef\n  targetRef\n  __typename\n}\n\nfragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment Assertion on Assertion {\n  id\n  subject\n  appId\n  actionId\n  actionName\n  assertedAt\n  recordedAt\n  seq\n  __typename\n}\n\nfragment Link on Link {\n  ...LinkRef\n  role\n  createdAt\n  term {\n    ...TermRef\n    __typename\n  }\n  assertion {\n    ...Assertion\n    __typename\n  }\n  __typename\n}\n\nfragment AssertedStructureRelation on AssertedStructureRelation {\n  assertion {\n    ...Assertion\n    __typename\n  }\n  link {\n    ...Link\n    __typename\n  }\n  __typename\n}"
        name = "AssertedStructureRelation"
        type = "AssertedStructureRelation"


class AssertedSameness(AssertedTrait, BaseModel):
    """An assertion that instances are one thing, and the claims it recorded"""

    typename: Literal["AssertedSameness"] = Field(
        alias="__typename", default="AssertedSameness", exclude=True
    )
    assertion: Assertion
    "The claim this call recorded. Not the subject's original assertion — for an attestation or a retraction those are different acts, possibly years apart."
    links: tuple[Link, ...]
    "The sameness claims this act recorded. Asserting that three instances are one records every pair among them, under one assertion"
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for AssertedSameness"""

        document = "fragment LinkRef on Link {\n  id\n  kind\n  sourceRef\n  targetRef\n  __typename\n}\n\nfragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment Assertion on Assertion {\n  id\n  subject\n  appId\n  actionId\n  actionName\n  assertedAt\n  recordedAt\n  seq\n  __typename\n}\n\nfragment Link on Link {\n  ...LinkRef\n  role\n  createdAt\n  term {\n    ...TermRef\n    __typename\n  }\n  assertion {\n    ...Assertion\n    __typename\n  }\n  __typename\n}\n\nfragment AssertedSameness on AssertedSameness {\n  assertion {\n    ...Assertion\n    __typename\n  }\n  links {\n    ...Link\n    __typename\n  }\n  __typename\n}"
        name = "AssertedSameness"
        type = "AssertedSameness"


class EntityCategory(CategoryBaseEntityCategory, EntityCategoryTrait, BaseModel):
    """An entity category definition"""

    typename: Literal["EntityCategory"] = Field(
        alias="__typename", default="EntityCategory", exclude=True
    )
    instance_kind: str | None = Field(default=None, alias="instanceKind")
    "What type of instance, (taking from the universe) 'LOT', 'BIOLOGICAL', 'PHYSICAL'"
    position_x: float | None = Field(default=None, alias="positionX")
    "X coordinate"
    position_y: float | None = Field(default=None, alias="positionY")
    "Y coordinate"
    width: float | None = Field(default=None)
    "Width for visualization (optional)"
    height: float | None = Field(default=None)
    "Height for visualization (optional)"
    property_definitions: tuple[PropertyDefinition, ...] = Field(
        alias="propertyDefinitions"
    )
    "The graph this category belongs to"
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for EntityCategory"""

        document = "fragment CategoryRef on Category {\n  id\n  key\n  label\n  ageName\n  __typename\n}\n\nfragment MediaStore on MediaStore {\n  id\n  key\n  presignedUrl\n  __typename\n}\n\nfragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment CategoryBase on Category {\n  ...CategoryRef\n  description\n  purl\n  color\n  pinned\n  image {\n    ...MediaStore\n    __typename\n  }\n  graph {\n    id\n    name\n    __typename\n  }\n  term {\n    ...TermRef\n    __typename\n  }\n  __typename\n}\n\nfragment PropertyDefinition on PropertyDefinition {\n  key\n  label\n  valueKind\n  unit\n  description\n  derivation\n  index\n  searchable\n  __typename\n}\n\nfragment EntityCategory on EntityCategory {\n  ...CategoryBase\n  instanceKind\n  positionX\n  positionY\n  width\n  height\n  propertyDefinitions {\n    ...PropertyDefinition\n    __typename\n  }\n  __typename\n}"
        name = "EntityCategory"
        type = "EntityCategory"


class RelationCategory(CategoryBaseRelationCategory, RelationCategoryTrait, BaseModel):
    """A relation category definition"""

    typename: Literal["RelationCategory"] = Field(
        alias="__typename", default="RelationCategory", exclude=True
    )
    source_descriptor: EntityDescriptor = Field(alias="sourceDescriptor")
    "Which nodes this edge category admits as its source"
    target_descriptor: EntityDescriptor = Field(alias="targetDescriptor")
    "Which nodes this edge category admits as its target"
    property_definitions: tuple[PropertyDefinition, ...] = Field(
        alias="propertyDefinitions"
    )
    "List of property definitions for this entity category"
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for RelationCategory"""

        document = "fragment CategoryRef on Category {\n  id\n  key\n  label\n  ageName\n  __typename\n}\n\nfragment MediaStore on MediaStore {\n  id\n  key\n  presignedUrl\n  __typename\n}\n\nfragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment CategoryBase on Category {\n  ...CategoryRef\n  description\n  purl\n  color\n  pinned\n  image {\n    ...MediaStore\n    __typename\n  }\n  graph {\n    id\n    name\n    __typename\n  }\n  term {\n    ...TermRef\n    __typename\n  }\n  __typename\n}\n\nfragment EntityDescriptor on EntityDescriptor {\n  keys\n  ontologyTerms\n  defaultCategoryKey\n  __typename\n}\n\nfragment PropertyDefinition on PropertyDefinition {\n  key\n  label\n  valueKind\n  unit\n  description\n  derivation\n  index\n  searchable\n  __typename\n}\n\nfragment RelationCategory on RelationCategory {\n  ...CategoryBase\n  sourceDescriptor {\n    ...EntityDescriptor\n    __typename\n  }\n  targetDescriptor {\n    ...EntityDescriptor\n    __typename\n  }\n  propertyDefinitions {\n    ...PropertyDefinition\n    __typename\n  }\n  __typename\n}"
        name = "RelationCategory"
        type = "RelationCategory"


class MeasurementCategory(
    CategoryBaseMeasurementCategory, MeasurementCategoryTrait, BaseModel
):
    """A measurement category definition"""

    typename: Literal["MeasurementCategory"] = Field(
        alias="__typename", default="MeasurementCategory", exclude=True
    )
    source_descriptor: StructureDescriptor = Field(alias="sourceDescriptor")
    "Which nodes this edge category admits as its source"
    target_descriptor: EntityDescriptor = Field(alias="targetDescriptor")
    "Which nodes this edge category admits as its target"
    property_definitions: tuple[PropertyDefinition, ...] = Field(
        alias="propertyDefinitions"
    )
    "List of property definitions for this entity category"
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for MeasurementCategory"""

        document = "fragment CategoryRef on Category {\n  id\n  key\n  label\n  ageName\n  __typename\n}\n\nfragment MediaStore on MediaStore {\n  id\n  key\n  presignedUrl\n  __typename\n}\n\nfragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment CategoryBase on Category {\n  ...CategoryRef\n  description\n  purl\n  color\n  pinned\n  image {\n    ...MediaStore\n    __typename\n  }\n  graph {\n    id\n    name\n    __typename\n  }\n  term {\n    ...TermRef\n    __typename\n  }\n  __typename\n}\n\nfragment EntityDescriptor on EntityDescriptor {\n  keys\n  ontologyTerms\n  defaultCategoryKey\n  __typename\n}\n\nfragment PropertyDefinition on PropertyDefinition {\n  key\n  label\n  valueKind\n  unit\n  description\n  derivation\n  index\n  searchable\n  __typename\n}\n\nfragment StructureDescriptor on StructureDescriptor {\n  defaultCategoryKey\n  __typename\n}\n\nfragment MeasurementCategory on MeasurementCategory {\n  ...CategoryBase\n  sourceDescriptor {\n    ...StructureDescriptor\n    __typename\n  }\n  targetDescriptor {\n    ...EntityDescriptor\n    __typename\n  }\n  propertyDefinitions {\n    ...PropertyDefinition\n    __typename\n  }\n  __typename\n}"
        name = "MeasurementCategory"
        type = "MeasurementCategory"


class StructureRelationCategory(
    CategoryBaseStructureRelationCategory, StructureRelationCategoryTrait, BaseModel
):
    """A relation category definition"""

    typename: Literal["StructureRelationCategory"] = Field(
        alias="__typename", default="StructureRelationCategory", exclude=True
    )
    source_descriptor: StructureDescriptor = Field(alias="sourceDescriptor")
    "Which nodes this edge category admits as its source"
    target_descriptor: StructureDescriptor = Field(alias="targetDescriptor")
    "Which nodes this edge category admits as its target"
    property_definitions: tuple[PropertyDefinition, ...] = Field(
        alias="propertyDefinitions"
    )
    "List of property definitions for this entity category"
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for StructureRelationCategory"""

        document = "fragment CategoryRef on Category {\n  id\n  key\n  label\n  ageName\n  __typename\n}\n\nfragment MediaStore on MediaStore {\n  id\n  key\n  presignedUrl\n  __typename\n}\n\nfragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment CategoryBase on Category {\n  ...CategoryRef\n  description\n  purl\n  color\n  pinned\n  image {\n    ...MediaStore\n    __typename\n  }\n  graph {\n    id\n    name\n    __typename\n  }\n  term {\n    ...TermRef\n    __typename\n  }\n  __typename\n}\n\nfragment PropertyDefinition on PropertyDefinition {\n  key\n  label\n  valueKind\n  unit\n  description\n  derivation\n  index\n  searchable\n  __typename\n}\n\nfragment StructureDescriptor on StructureDescriptor {\n  defaultCategoryKey\n  __typename\n}\n\nfragment StructureRelationCategory on StructureRelationCategory {\n  ...CategoryBase\n  sourceDescriptor {\n    ...StructureDescriptor\n    __typename\n  }\n  targetDescriptor {\n    ...StructureDescriptor\n    __typename\n  }\n  propertyDefinitions {\n    ...PropertyDefinition\n    __typename\n  }\n  __typename\n}"
        name = "StructureRelationCategory"
        type = "StructureRelationCategory"


class NaturalEventCategory(
    CategoryBaseNaturalEventCategory, NaturalEventCategoryTrait, BaseModel
):
    """A relation category definition"""

    typename: Literal["NaturalEventCategory"] = Field(
        alias="__typename", default="NaturalEventCategory", exclude=True
    )
    position_x: float | None = Field(default=None, alias="positionX")
    "X coordinate"
    position_y: float | None = Field(default=None, alias="positionY")
    "Y coordinate"
    width: float | None = Field(default=None)
    "Width for visualization (optional)"
    height: float | None = Field(default=None)
    "Height for visualization (optional)"
    inputs: tuple[EventRole, ...]
    "The roles an entity can play going into an event of this category"
    outputs: tuple[EventRole, ...]
    "The roles an entity can play coming out of an event of this category"
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for NaturalEventCategory"""

        document = "fragment CategoryRef on Category {\n  id\n  key\n  label\n  ageName\n  __typename\n}\n\nfragment EntityDescriptor on EntityDescriptor {\n  keys\n  ontologyTerms\n  defaultCategoryKey\n  __typename\n}\n\nfragment MediaStore on MediaStore {\n  id\n  key\n  presignedUrl\n  __typename\n}\n\nfragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment CategoryBase on Category {\n  ...CategoryRef\n  description\n  purl\n  color\n  pinned\n  image {\n    ...MediaStore\n    __typename\n  }\n  graph {\n    id\n    name\n    __typename\n  }\n  term {\n    ...TermRef\n    __typename\n  }\n  __typename\n}\n\nfragment EventRole on EventRole {\n  key\n  role\n  descriptor {\n    ...EntityDescriptor\n    __typename\n  }\n  __typename\n}\n\nfragment NaturalEventCategory on NaturalEventCategory {\n  ...CategoryBase\n  positionX\n  positionY\n  width\n  height\n  inputs {\n    ...EventRole\n    __typename\n  }\n  outputs {\n    ...EventRole\n    __typename\n  }\n  __typename\n}"
        name = "NaturalEventCategory"
        type = "NaturalEventCategory"


class ProtocolEventCategory(
    CategoryBaseProtocolEventCategory, ProtocolEventCategoryTrait, BaseModel
):
    """A relation category definition"""

    typename: Literal["ProtocolEventCategory"] = Field(
        alias="__typename", default="ProtocolEventCategory", exclude=True
    )
    position_x: float | None = Field(default=None, alias="positionX")
    "X coordinate"
    position_y: float | None = Field(default=None, alias="positionY")
    "Y coordinate"
    width: float | None = Field(default=None)
    "Width for visualization (optional)"
    height: float | None = Field(default=None)
    "Height for visualization (optional)"
    inputs: tuple[EventRole, ...]
    "The roles an entity can play going into an event of this category"
    outputs: tuple[EventRole, ...]
    "The roles an entity can play coming out of an event of this category"
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for ProtocolEventCategory"""

        document = "fragment CategoryRef on Category {\n  id\n  key\n  label\n  ageName\n  __typename\n}\n\nfragment EntityDescriptor on EntityDescriptor {\n  keys\n  ontologyTerms\n  defaultCategoryKey\n  __typename\n}\n\nfragment MediaStore on MediaStore {\n  id\n  key\n  presignedUrl\n  __typename\n}\n\nfragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment CategoryBase on Category {\n  ...CategoryRef\n  description\n  purl\n  color\n  pinned\n  image {\n    ...MediaStore\n    __typename\n  }\n  graph {\n    id\n    name\n    __typename\n  }\n  term {\n    ...TermRef\n    __typename\n  }\n  __typename\n}\n\nfragment EventRole on EventRole {\n  key\n  role\n  descriptor {\n    ...EntityDescriptor\n    __typename\n  }\n  __typename\n}\n\nfragment ProtocolEventCategory on ProtocolEventCategory {\n  ...CategoryBase\n  positionX\n  positionY\n  width\n  height\n  inputs {\n    ...EventRole\n    __typename\n  }\n  outputs {\n    ...EventRole\n    __typename\n  }\n  __typename\n}"
        name = "ProtocolEventCategory"
        type = "ProtocolEventCategory"


class AssertedEntity(AssertedTrait, HasDrawings, BaseModel):
    """An assertion about an entity: the act, the claim it recorded, and everywhere that claim is now drawn"""

    typename: Literal["AssertedEntity"] = Field(
        alias="__typename", default="AssertedEntity", exclude=True
    )
    assertion: Assertion
    "The claim this call recorded. Not the subject's original assertion — for an attestation or a retraction those are different acts, possibly years apart."
    instance: Instance
    "What was claimed, as the log has it. Not a drawing of it: derived properties, a label and a category are one view's account and live on each entry in `drawings`. This is addressable whether or not any view draws it, which is the case a write has to answer for."
    drawings: tuple[NodeDrawing, ...]
    "Every view that draws this claim, after this assertion. Empty means no view does — which is an ordinary answer, not an error: a claim names a word the organization owns, and a view that declares no category for that word simply will not draw it. For a retraction this is usually empty and deliberately not hardcoded so: existence is folded under each view's own selector, so a view that does not count the retracting subject still draws the node."
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for AssertedEntity"""

        document = "fragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment CategoryRef on Category {\n  id\n  key\n  label\n  ageName\n  __typename\n}\n\nfragment InstanceRef on Instance {\n  id\n  kind\n  term {\n    ...TermRef\n    __typename\n  }\n  __typename\n}\n\nfragment NodeRef on Node {\n  id\n  label\n  __typename\n}\n\nfragment Assertion on Assertion {\n  id\n  subject\n  appId\n  actionId\n  actionName\n  assertedAt\n  recordedAt\n  seq\n  __typename\n}\n\nfragment Instance on Instance {\n  ...InstanceRef\n  createdAt\n  component\n  assertion {\n    ...Assertion\n    __typename\n  }\n  __typename\n}\n\nfragment NodeDrawing on NodeDrawing {\n  graph {\n    id\n    name\n    __typename\n  }\n  category {\n    ...CategoryRef\n    __typename\n  }\n  node {\n    ...NodeRef\n    __typename\n  }\n  __typename\n}\n\nfragment AssertedEntity on AssertedEntity {\n  assertion {\n    ...Assertion\n    __typename\n  }\n  instance {\n    ...Instance\n    __typename\n  }\n  drawings {\n    ...NodeDrawing\n    __typename\n  }\n  __typename\n}"
        name = "AssertedEntity"
        type = "AssertedEntity"


class AssertedNaturalEvent(AssertedTrait, HasDrawings, BaseModel):
    """An assertion about a natural event, and everywhere it is now drawn"""

    typename: Literal["AssertedNaturalEvent"] = Field(
        alias="__typename", default="AssertedNaturalEvent", exclude=True
    )
    assertion: Assertion
    "The claim this call recorded. Not the subject's original assertion — for an attestation or a retraction those are different acts, possibly years apart."
    instance: Instance
    "What was claimed, as the log has it. Not a drawing of it: derived properties, a label and a category are one view's account and live on each entry in `drawings`. This is addressable whether or not any view draws it, which is the case a write has to answer for."
    drawings: tuple[NodeDrawing, ...]
    "Every view that draws this claim, after this assertion. Empty means no view does — which is an ordinary answer, not an error: a claim names a word the organization owns, and a view that declares no category for that word simply will not draw it. For a retraction this is usually empty and deliberately not hardcoded so: existence is folded under each view's own selector, so a view that does not count the retracting subject still draws the node."
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for AssertedNaturalEvent"""

        document = "fragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment CategoryRef on Category {\n  id\n  key\n  label\n  ageName\n  __typename\n}\n\nfragment InstanceRef on Instance {\n  id\n  kind\n  term {\n    ...TermRef\n    __typename\n  }\n  __typename\n}\n\nfragment NodeRef on Node {\n  id\n  label\n  __typename\n}\n\nfragment Assertion on Assertion {\n  id\n  subject\n  appId\n  actionId\n  actionName\n  assertedAt\n  recordedAt\n  seq\n  __typename\n}\n\nfragment Instance on Instance {\n  ...InstanceRef\n  createdAt\n  component\n  assertion {\n    ...Assertion\n    __typename\n  }\n  __typename\n}\n\nfragment NodeDrawing on NodeDrawing {\n  graph {\n    id\n    name\n    __typename\n  }\n  category {\n    ...CategoryRef\n    __typename\n  }\n  node {\n    ...NodeRef\n    __typename\n  }\n  __typename\n}\n\nfragment AssertedNaturalEvent on AssertedNaturalEvent {\n  assertion {\n    ...Assertion\n    __typename\n  }\n  instance {\n    ...Instance\n    __typename\n  }\n  drawings {\n    ...NodeDrawing\n    __typename\n  }\n  __typename\n}"
        name = "AssertedNaturalEvent"
        type = "AssertedNaturalEvent"


class AssertedProtocolEvent(AssertedTrait, HasDrawings, BaseModel):
    """An assertion about a protocol event, and everywhere it is now drawn"""

    typename: Literal["AssertedProtocolEvent"] = Field(
        alias="__typename", default="AssertedProtocolEvent", exclude=True
    )
    assertion: Assertion
    "The claim this call recorded. Not the subject's original assertion — for an attestation or a retraction those are different acts, possibly years apart."
    instance: Instance
    "What was claimed, as the log has it. Not a drawing of it: derived properties, a label and a category are one view's account and live on each entry in `drawings`. This is addressable whether or not any view draws it, which is the case a write has to answer for."
    drawings: tuple[NodeDrawing, ...]
    "Every view that draws this claim, after this assertion. Empty means no view does — which is an ordinary answer, not an error: a claim names a word the organization owns, and a view that declares no category for that word simply will not draw it. For a retraction this is usually empty and deliberately not hardcoded so: existence is folded under each view's own selector, so a view that does not count the retracting subject still draws the node."
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for AssertedProtocolEvent"""

        document = "fragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment CategoryRef on Category {\n  id\n  key\n  label\n  ageName\n  __typename\n}\n\nfragment InstanceRef on Instance {\n  id\n  kind\n  term {\n    ...TermRef\n    __typename\n  }\n  __typename\n}\n\nfragment NodeRef on Node {\n  id\n  label\n  __typename\n}\n\nfragment Assertion on Assertion {\n  id\n  subject\n  appId\n  actionId\n  actionName\n  assertedAt\n  recordedAt\n  seq\n  __typename\n}\n\nfragment Instance on Instance {\n  ...InstanceRef\n  createdAt\n  component\n  assertion {\n    ...Assertion\n    __typename\n  }\n  __typename\n}\n\nfragment NodeDrawing on NodeDrawing {\n  graph {\n    id\n    name\n    __typename\n  }\n  category {\n    ...CategoryRef\n    __typename\n  }\n  node {\n    ...NodeRef\n    __typename\n  }\n  __typename\n}\n\nfragment AssertedProtocolEvent on AssertedProtocolEvent {\n  assertion {\n    ...Assertion\n    __typename\n  }\n  instance {\n    ...Instance\n    __typename\n  }\n  drawings {\n    ...NodeDrawing\n    __typename\n  }\n  __typename\n}"
        name = "AssertedProtocolEvent"
        type = "AssertedProtocolEvent"


class AssertedInstances(AssertedTrait, HasDrawings, BaseModel):
    """An assertion about several instances made as one act, and everywhere they are now drawn"""

    typename: Literal["AssertedInstances"] = Field(
        alias="__typename", default="AssertedInstances", exclude=True
    )
    assertion: Assertion
    "The single claim covering the whole batch. One act by one actor is one assertion, which is why this is not a list"
    instances: tuple[Instance, ...]
    "The instances this act was about, as the log has them"
    drawings: tuple[NodeDrawing, ...]
    "Every view that draws this claim, after this assertion. Empty means no view does — which is an ordinary answer, not an error: a claim names a word the organization owns, and a view that declares no category for that word simply will not draw it. For a retraction this is usually empty and deliberately not hardcoded so: existence is folded under each view's own selector, so a view that does not count the retracting subject still draws the node."
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for AssertedInstances"""

        document = "fragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment CategoryRef on Category {\n  id\n  key\n  label\n  ageName\n  __typename\n}\n\nfragment InstanceRef on Instance {\n  id\n  kind\n  term {\n    ...TermRef\n    __typename\n  }\n  __typename\n}\n\nfragment NodeRef on Node {\n  id\n  label\n  __typename\n}\n\nfragment Assertion on Assertion {\n  id\n  subject\n  appId\n  actionId\n  actionName\n  assertedAt\n  recordedAt\n  seq\n  __typename\n}\n\nfragment Instance on Instance {\n  ...InstanceRef\n  createdAt\n  component\n  assertion {\n    ...Assertion\n    __typename\n  }\n  __typename\n}\n\nfragment NodeDrawing on NodeDrawing {\n  graph {\n    id\n    name\n    __typename\n  }\n  category {\n    ...CategoryRef\n    __typename\n  }\n  node {\n    ...NodeRef\n    __typename\n  }\n  __typename\n}\n\nfragment AssertedInstances on AssertedInstances {\n  assertion {\n    ...Assertion\n    __typename\n  }\n  instances {\n    ...Instance\n    __typename\n  }\n  drawings {\n    ...NodeDrawing\n    __typename\n  }\n  __typename\n}"
        name = "AssertedInstances"
        type = "AssertedInstances"


class Graph(ListGraph, GraphTrait, BaseModel):
    """One view over the organization's evidence log"""

    typename: Literal["Graph"] = Field(
        alias="__typename", default="Graph", exclude=True
    )
    purl: str | None = Field(default=None)
    "Persistent URL for this graph"
    projection: GraphProjection
    "Where this view's drawing stands relative to the organization's log: the assertion seq it is caught up to, how far behind it is, and whether its derived properties are current under the active schema. Compare a write's `assertion.seq` with `projectedThroughSeq` to know whether this view has drawn it. See `graph_engine/watermark.py` for why the cursor is safe."
    entity_categories: tuple[EntityCategory, ...] = Field(alias="entityCategories")
    "List of entity categories defined in this graph"
    relation_categories: tuple[RelationCategory, ...] = Field(
        alias="relationCategories"
    )
    "List of relation categories defined in this graph"
    measurement_categories: tuple[MeasurementCategory, ...] = Field(
        alias="measurementCategories"
    )
    "List of measurement categories defined in this graph"
    structure_relation_categories: tuple[StructureRelationCategory, ...] = Field(
        alias="structureRelationCategories"
    )
    "List of structure relation categories defined in this graph"
    natural_event_categories: tuple[NaturalEventCategory, ...] = Field(
        alias="naturalEventCategories"
    )
    "List of natural event categories defined in this graph"
    protocol_event_categories: tuple[ProtocolEventCategory, ...] = Field(
        alias="protocolEventCategories"
    )
    "List of protocol event categories defined in this graph"
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for Graph"""

        document = "fragment CategoryRef on Category {\n  id\n  key\n  label\n  ageName\n  __typename\n}\n\nfragment MediaStore on MediaStore {\n  id\n  key\n  presignedUrl\n  __typename\n}\n\nfragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment CategoryBase on Category {\n  ...CategoryRef\n  description\n  purl\n  color\n  pinned\n  image {\n    ...MediaStore\n    __typename\n  }\n  graph {\n    id\n    name\n    __typename\n  }\n  term {\n    ...TermRef\n    __typename\n  }\n  __typename\n}\n\nfragment EntityDescriptor on EntityDescriptor {\n  keys\n  ontologyTerms\n  defaultCategoryKey\n  __typename\n}\n\nfragment EventRole on EventRole {\n  key\n  role\n  descriptor {\n    ...EntityDescriptor\n    __typename\n  }\n  __typename\n}\n\nfragment PropertyDefinition on PropertyDefinition {\n  key\n  label\n  valueKind\n  unit\n  description\n  derivation\n  index\n  searchable\n  __typename\n}\n\nfragment StructureDescriptor on StructureDescriptor {\n  defaultCategoryKey\n  __typename\n}\n\nfragment EntityCategory on EntityCategory {\n  ...CategoryBase\n  instanceKind\n  positionX\n  positionY\n  width\n  height\n  propertyDefinitions {\n    ...PropertyDefinition\n    __typename\n  }\n  __typename\n}\n\nfragment GraphProjection on GraphProjection {\n  kind\n  status\n  projectedThroughSeq\n  derivedThroughSeq\n  lag\n  pending\n  schemaStale\n  schemaHash\n  derivedAt\n  rebuiltAt\n  __typename\n}\n\nfragment ListGraph on Graph {\n  id\n  name\n  description\n  ageName\n  isArchived\n  pinned\n  __typename\n}\n\nfragment MeasurementCategory on MeasurementCategory {\n  ...CategoryBase\n  sourceDescriptor {\n    ...StructureDescriptor\n    __typename\n  }\n  targetDescriptor {\n    ...EntityDescriptor\n    __typename\n  }\n  propertyDefinitions {\n    ...PropertyDefinition\n    __typename\n  }\n  __typename\n}\n\nfragment NaturalEventCategory on NaturalEventCategory {\n  ...CategoryBase\n  positionX\n  positionY\n  width\n  height\n  inputs {\n    ...EventRole\n    __typename\n  }\n  outputs {\n    ...EventRole\n    __typename\n  }\n  __typename\n}\n\nfragment ProtocolEventCategory on ProtocolEventCategory {\n  ...CategoryBase\n  positionX\n  positionY\n  width\n  height\n  inputs {\n    ...EventRole\n    __typename\n  }\n  outputs {\n    ...EventRole\n    __typename\n  }\n  __typename\n}\n\nfragment RelationCategory on RelationCategory {\n  ...CategoryBase\n  sourceDescriptor {\n    ...EntityDescriptor\n    __typename\n  }\n  targetDescriptor {\n    ...EntityDescriptor\n    __typename\n  }\n  propertyDefinitions {\n    ...PropertyDefinition\n    __typename\n  }\n  __typename\n}\n\nfragment StructureRelationCategory on StructureRelationCategory {\n  ...CategoryBase\n  sourceDescriptor {\n    ...StructureDescriptor\n    __typename\n  }\n  targetDescriptor {\n    ...StructureDescriptor\n    __typename\n  }\n  propertyDefinitions {\n    ...PropertyDefinition\n    __typename\n  }\n  __typename\n}\n\nfragment Graph on Graph {\n  ...ListGraph\n  purl\n  projection {\n    ...GraphProjection\n    __typename\n  }\n  entityCategories {\n    ...EntityCategory\n    __typename\n  }\n  relationCategories {\n    ...RelationCategory\n    __typename\n  }\n  measurementCategories {\n    ...MeasurementCategory\n    __typename\n  }\n  structureRelationCategories {\n    ...StructureRelationCategory\n    __typename\n  }\n  naturalEventCategories {\n    ...NaturalEventCategory\n    __typename\n  }\n  protocolEventCategories {\n    ...ProtocolEventCategory\n    __typename\n  }\n  __typename\n}"
        name = "Graph"
        type = "Graph"


class CreateEntityCategoryMutation(BaseModel):
    """A Category is one view's rule for a word: what it means HERE, how it is drawn, and which
    properties are derived onto it. Creating one never records a claim."""

    create_entity_category: EntityCategory = Field(alias="createEntityCategory")
    "Create a new entity category in the graph"

    class Arguments(BaseModel):
        """Arguments for CreateEntityCategory"""

        input: CreateEntityCategoryInput

    class Meta:
        """Meta class for CreateEntityCategory"""

        document = "fragment CategoryRef on Category {\n  id\n  key\n  label\n  ageName\n  __typename\n}\n\nfragment MediaStore on MediaStore {\n  id\n  key\n  presignedUrl\n  __typename\n}\n\nfragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment CategoryBase on Category {\n  ...CategoryRef\n  description\n  purl\n  color\n  pinned\n  image {\n    ...MediaStore\n    __typename\n  }\n  graph {\n    id\n    name\n    __typename\n  }\n  term {\n    ...TermRef\n    __typename\n  }\n  __typename\n}\n\nfragment PropertyDefinition on PropertyDefinition {\n  key\n  label\n  valueKind\n  unit\n  description\n  derivation\n  index\n  searchable\n  __typename\n}\n\nfragment EntityCategory on EntityCategory {\n  ...CategoryBase\n  instanceKind\n  positionX\n  positionY\n  width\n  height\n  propertyDefinitions {\n    ...PropertyDefinition\n    __typename\n  }\n  __typename\n}\n\nmutation CreateEntityCategory($input: CreateEntityCategoryInput!) {\n  createEntityCategory(input: $input) {\n    ...EntityCategory\n    __typename\n  }\n}"


class UpdateEntityCategoryMutation(BaseModel):
    """No documentation found for this operation."""

    update_entity_category: EntityCategory = Field(alias="updateEntityCategory")
    "Update an existing entity category in the graph"

    class Arguments(BaseModel):
        """Arguments for UpdateEntityCategory"""

        input: UpdateEntityCategoryInput

    class Meta:
        """Meta class for UpdateEntityCategory"""

        document = "fragment CategoryRef on Category {\n  id\n  key\n  label\n  ageName\n  __typename\n}\n\nfragment MediaStore on MediaStore {\n  id\n  key\n  presignedUrl\n  __typename\n}\n\nfragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment CategoryBase on Category {\n  ...CategoryRef\n  description\n  purl\n  color\n  pinned\n  image {\n    ...MediaStore\n    __typename\n  }\n  graph {\n    id\n    name\n    __typename\n  }\n  term {\n    ...TermRef\n    __typename\n  }\n  __typename\n}\n\nfragment PropertyDefinition on PropertyDefinition {\n  key\n  label\n  valueKind\n  unit\n  description\n  derivation\n  index\n  searchable\n  __typename\n}\n\nfragment EntityCategory on EntityCategory {\n  ...CategoryBase\n  instanceKind\n  positionX\n  positionY\n  width\n  height\n  propertyDefinitions {\n    ...PropertyDefinition\n    __typename\n  }\n  __typename\n}\n\nmutation UpdateEntityCategory($input: UpdateEntityCategoryInput!) {\n  updateEntityCategory(input: $input) {\n    ...EntityCategory\n    __typename\n  }\n}"


class DeleteEntityCategoryMutation(BaseModel):
    """No documentation found for this operation."""

    delete_entity_category: ID = Field(alias="deleteEntityCategory")
    "Delete an entity category from the graph"

    class Arguments(BaseModel):
        """Arguments for DeleteEntityCategory"""

        input: DeleteEntityCategoryInput

    class Meta:
        """Meta class for DeleteEntityCategory"""

        document = "mutation DeleteEntityCategory($input: DeleteEntityCategoryInput!) {\n  deleteEntityCategory(input: $input)\n}"


class CreateRelationCategoryMutation(BaseModel):
    """No documentation found for this operation."""

    create_relation_category: RelationCategory = Field(alias="createRelationCategory")
    "Create a new relation category in the graph"

    class Arguments(BaseModel):
        """Arguments for CreateRelationCategory"""

        input: CreateRelationCategoryInput

    class Meta:
        """Meta class for CreateRelationCategory"""

        document = "fragment CategoryRef on Category {\n  id\n  key\n  label\n  ageName\n  __typename\n}\n\nfragment MediaStore on MediaStore {\n  id\n  key\n  presignedUrl\n  __typename\n}\n\nfragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment CategoryBase on Category {\n  ...CategoryRef\n  description\n  purl\n  color\n  pinned\n  image {\n    ...MediaStore\n    __typename\n  }\n  graph {\n    id\n    name\n    __typename\n  }\n  term {\n    ...TermRef\n    __typename\n  }\n  __typename\n}\n\nfragment EntityDescriptor on EntityDescriptor {\n  keys\n  ontologyTerms\n  defaultCategoryKey\n  __typename\n}\n\nfragment PropertyDefinition on PropertyDefinition {\n  key\n  label\n  valueKind\n  unit\n  description\n  derivation\n  index\n  searchable\n  __typename\n}\n\nfragment RelationCategory on RelationCategory {\n  ...CategoryBase\n  sourceDescriptor {\n    ...EntityDescriptor\n    __typename\n  }\n  targetDescriptor {\n    ...EntityDescriptor\n    __typename\n  }\n  propertyDefinitions {\n    ...PropertyDefinition\n    __typename\n  }\n  __typename\n}\n\nmutation CreateRelationCategory($input: CreateRelationCategoryInput!) {\n  createRelationCategory(input: $input) {\n    ...RelationCategory\n    __typename\n  }\n}"


class UpdateRelationCategoryMutation(BaseModel):
    """No documentation found for this operation."""

    update_relation_category: RelationCategory = Field(alias="updateRelationCategory")
    "Update an existing relation category in the graph"

    class Arguments(BaseModel):
        """Arguments for UpdateRelationCategory"""

        input: UpdateRelationCategoryInput

    class Meta:
        """Meta class for UpdateRelationCategory"""

        document = "fragment CategoryRef on Category {\n  id\n  key\n  label\n  ageName\n  __typename\n}\n\nfragment MediaStore on MediaStore {\n  id\n  key\n  presignedUrl\n  __typename\n}\n\nfragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment CategoryBase on Category {\n  ...CategoryRef\n  description\n  purl\n  color\n  pinned\n  image {\n    ...MediaStore\n    __typename\n  }\n  graph {\n    id\n    name\n    __typename\n  }\n  term {\n    ...TermRef\n    __typename\n  }\n  __typename\n}\n\nfragment EntityDescriptor on EntityDescriptor {\n  keys\n  ontologyTerms\n  defaultCategoryKey\n  __typename\n}\n\nfragment PropertyDefinition on PropertyDefinition {\n  key\n  label\n  valueKind\n  unit\n  description\n  derivation\n  index\n  searchable\n  __typename\n}\n\nfragment RelationCategory on RelationCategory {\n  ...CategoryBase\n  sourceDescriptor {\n    ...EntityDescriptor\n    __typename\n  }\n  targetDescriptor {\n    ...EntityDescriptor\n    __typename\n  }\n  propertyDefinitions {\n    ...PropertyDefinition\n    __typename\n  }\n  __typename\n}\n\nmutation UpdateRelationCategory($input: UpdateRelationCategoryInput!) {\n  updateRelationCategory(input: $input) {\n    ...RelationCategory\n    __typename\n  }\n}"


class DeleteRelationCategoryMutation(BaseModel):
    """No documentation found for this operation."""

    delete_relation_category: ID = Field(alias="deleteRelationCategory")
    "Delete a relation category from the graph"

    class Arguments(BaseModel):
        """Arguments for DeleteRelationCategory"""

        input: DeleteRelationCategoryInput

    class Meta:
        """Meta class for DeleteRelationCategory"""

        document = "mutation DeleteRelationCategory($input: DeleteRelationCategoryInput!) {\n  deleteRelationCategory(input: $input)\n}"


class CreateMeasurementCategoryMutation(BaseModel):
    """No documentation found for this operation."""

    create_measurement_category: MeasurementCategory = Field(
        alias="createMeasurementCategory"
    )
    "Create a new measurement category in the graph"

    class Arguments(BaseModel):
        """Arguments for CreateMeasurementCategory"""

        input: CreateMeasurementCategoryInput

    class Meta:
        """Meta class for CreateMeasurementCategory"""

        document = "fragment CategoryRef on Category {\n  id\n  key\n  label\n  ageName\n  __typename\n}\n\nfragment MediaStore on MediaStore {\n  id\n  key\n  presignedUrl\n  __typename\n}\n\nfragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment CategoryBase on Category {\n  ...CategoryRef\n  description\n  purl\n  color\n  pinned\n  image {\n    ...MediaStore\n    __typename\n  }\n  graph {\n    id\n    name\n    __typename\n  }\n  term {\n    ...TermRef\n    __typename\n  }\n  __typename\n}\n\nfragment EntityDescriptor on EntityDescriptor {\n  keys\n  ontologyTerms\n  defaultCategoryKey\n  __typename\n}\n\nfragment PropertyDefinition on PropertyDefinition {\n  key\n  label\n  valueKind\n  unit\n  description\n  derivation\n  index\n  searchable\n  __typename\n}\n\nfragment StructureDescriptor on StructureDescriptor {\n  defaultCategoryKey\n  __typename\n}\n\nfragment MeasurementCategory on MeasurementCategory {\n  ...CategoryBase\n  sourceDescriptor {\n    ...StructureDescriptor\n    __typename\n  }\n  targetDescriptor {\n    ...EntityDescriptor\n    __typename\n  }\n  propertyDefinitions {\n    ...PropertyDefinition\n    __typename\n  }\n  __typename\n}\n\nmutation CreateMeasurementCategory($input: CreateMeasurementCategoryInput!) {\n  createMeasurementCategory(input: $input) {\n    ...MeasurementCategory\n    __typename\n  }\n}"


class UpdateMeasurementCategoryMutation(BaseModel):
    """No documentation found for this operation."""

    update_measurement_category: MeasurementCategory = Field(
        alias="updateMeasurementCategory"
    )
    "Update an existing measurement category in the graph"

    class Arguments(BaseModel):
        """Arguments for UpdateMeasurementCategory"""

        input: UpdateMeasurementCategoryInput

    class Meta:
        """Meta class for UpdateMeasurementCategory"""

        document = "fragment CategoryRef on Category {\n  id\n  key\n  label\n  ageName\n  __typename\n}\n\nfragment MediaStore on MediaStore {\n  id\n  key\n  presignedUrl\n  __typename\n}\n\nfragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment CategoryBase on Category {\n  ...CategoryRef\n  description\n  purl\n  color\n  pinned\n  image {\n    ...MediaStore\n    __typename\n  }\n  graph {\n    id\n    name\n    __typename\n  }\n  term {\n    ...TermRef\n    __typename\n  }\n  __typename\n}\n\nfragment EntityDescriptor on EntityDescriptor {\n  keys\n  ontologyTerms\n  defaultCategoryKey\n  __typename\n}\n\nfragment PropertyDefinition on PropertyDefinition {\n  key\n  label\n  valueKind\n  unit\n  description\n  derivation\n  index\n  searchable\n  __typename\n}\n\nfragment StructureDescriptor on StructureDescriptor {\n  defaultCategoryKey\n  __typename\n}\n\nfragment MeasurementCategory on MeasurementCategory {\n  ...CategoryBase\n  sourceDescriptor {\n    ...StructureDescriptor\n    __typename\n  }\n  targetDescriptor {\n    ...EntityDescriptor\n    __typename\n  }\n  propertyDefinitions {\n    ...PropertyDefinition\n    __typename\n  }\n  __typename\n}\n\nmutation UpdateMeasurementCategory($input: UpdateMeasurementCategoryInput!) {\n  updateMeasurementCategory(input: $input) {\n    ...MeasurementCategory\n    __typename\n  }\n}"


class DeleteMeasurementCategoryMutation(BaseModel):
    """No documentation found for this operation."""

    delete_measurement_category: ID = Field(alias="deleteMeasurementCategory")
    "Delete a measurement category from the graph"

    class Arguments(BaseModel):
        """Arguments for DeleteMeasurementCategory"""

        input: DeleteMeasurementCategoryInput

    class Meta:
        """Meta class for DeleteMeasurementCategory"""

        document = "mutation DeleteMeasurementCategory($input: DeleteMeasurementCategoryInput!) {\n  deleteMeasurementCategory(input: $input)\n}"


class CreateStructureRelationCategoryMutation(BaseModel):
    """No documentation found for this operation."""

    create_structure_relation_category: StructureRelationCategory = Field(
        alias="createStructureRelationCategory"
    )
    "Create a new structure relation category in the graph"

    class Arguments(BaseModel):
        """Arguments for CreateStructureRelationCategory"""

        input: CreateStructureRelationCategoryInput

    class Meta:
        """Meta class for CreateStructureRelationCategory"""

        document = "fragment CategoryRef on Category {\n  id\n  key\n  label\n  ageName\n  __typename\n}\n\nfragment MediaStore on MediaStore {\n  id\n  key\n  presignedUrl\n  __typename\n}\n\nfragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment CategoryBase on Category {\n  ...CategoryRef\n  description\n  purl\n  color\n  pinned\n  image {\n    ...MediaStore\n    __typename\n  }\n  graph {\n    id\n    name\n    __typename\n  }\n  term {\n    ...TermRef\n    __typename\n  }\n  __typename\n}\n\nfragment PropertyDefinition on PropertyDefinition {\n  key\n  label\n  valueKind\n  unit\n  description\n  derivation\n  index\n  searchable\n  __typename\n}\n\nfragment StructureDescriptor on StructureDescriptor {\n  defaultCategoryKey\n  __typename\n}\n\nfragment StructureRelationCategory on StructureRelationCategory {\n  ...CategoryBase\n  sourceDescriptor {\n    ...StructureDescriptor\n    __typename\n  }\n  targetDescriptor {\n    ...StructureDescriptor\n    __typename\n  }\n  propertyDefinitions {\n    ...PropertyDefinition\n    __typename\n  }\n  __typename\n}\n\nmutation CreateStructureRelationCategory($input: CreateStructureRelationCategoryInput!) {\n  createStructureRelationCategory(input: $input) {\n    ...StructureRelationCategory\n    __typename\n  }\n}"


class UpdateStructureRelationCategoryMutation(BaseModel):
    """No documentation found for this operation."""

    update_structure_relation_category: StructureRelationCategory = Field(
        alias="updateStructureRelationCategory"
    )
    "Update an existing structure relation category in the graph"

    class Arguments(BaseModel):
        """Arguments for UpdateStructureRelationCategory"""

        input: UpdateStructureRelationCategoryInput

    class Meta:
        """Meta class for UpdateStructureRelationCategory"""

        document = "fragment CategoryRef on Category {\n  id\n  key\n  label\n  ageName\n  __typename\n}\n\nfragment MediaStore on MediaStore {\n  id\n  key\n  presignedUrl\n  __typename\n}\n\nfragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment CategoryBase on Category {\n  ...CategoryRef\n  description\n  purl\n  color\n  pinned\n  image {\n    ...MediaStore\n    __typename\n  }\n  graph {\n    id\n    name\n    __typename\n  }\n  term {\n    ...TermRef\n    __typename\n  }\n  __typename\n}\n\nfragment PropertyDefinition on PropertyDefinition {\n  key\n  label\n  valueKind\n  unit\n  description\n  derivation\n  index\n  searchable\n  __typename\n}\n\nfragment StructureDescriptor on StructureDescriptor {\n  defaultCategoryKey\n  __typename\n}\n\nfragment StructureRelationCategory on StructureRelationCategory {\n  ...CategoryBase\n  sourceDescriptor {\n    ...StructureDescriptor\n    __typename\n  }\n  targetDescriptor {\n    ...StructureDescriptor\n    __typename\n  }\n  propertyDefinitions {\n    ...PropertyDefinition\n    __typename\n  }\n  __typename\n}\n\nmutation UpdateStructureRelationCategory($input: UpdateStructureRelationCategoryInput!) {\n  updateStructureRelationCategory(input: $input) {\n    ...StructureRelationCategory\n    __typename\n  }\n}"


class DeleteStructureRelationCategoryMutation(BaseModel):
    """No documentation found for this operation."""

    delete_structure_relation_category: ID = Field(
        alias="deleteStructureRelationCategory"
    )
    "Delete a structure relation category from the graph"

    class Arguments(BaseModel):
        """Arguments for DeleteStructureRelationCategory"""

        input: DeleteStructureRelationCategoryInput

    class Meta:
        """Meta class for DeleteStructureRelationCategory"""

        document = "mutation DeleteStructureRelationCategory($input: DeleteStructureRelationCategoryInput!) {\n  deleteStructureRelationCategory(input: $input)\n}"


class CreateNaturalEventCategoryMutation(BaseModel):
    """No documentation found for this operation."""

    create_natural_event_category: NaturalEventCategory = Field(
        alias="createNaturalEventCategory"
    )
    "Create a new natural event category in the graph"

    class Arguments(BaseModel):
        """Arguments for CreateNaturalEventCategory"""

        input: CreateNaturalEventCategoryInput

    class Meta:
        """Meta class for CreateNaturalEventCategory"""

        document = "fragment CategoryRef on Category {\n  id\n  key\n  label\n  ageName\n  __typename\n}\n\nfragment EntityDescriptor on EntityDescriptor {\n  keys\n  ontologyTerms\n  defaultCategoryKey\n  __typename\n}\n\nfragment MediaStore on MediaStore {\n  id\n  key\n  presignedUrl\n  __typename\n}\n\nfragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment CategoryBase on Category {\n  ...CategoryRef\n  description\n  purl\n  color\n  pinned\n  image {\n    ...MediaStore\n    __typename\n  }\n  graph {\n    id\n    name\n    __typename\n  }\n  term {\n    ...TermRef\n    __typename\n  }\n  __typename\n}\n\nfragment EventRole on EventRole {\n  key\n  role\n  descriptor {\n    ...EntityDescriptor\n    __typename\n  }\n  __typename\n}\n\nfragment NaturalEventCategory on NaturalEventCategory {\n  ...CategoryBase\n  positionX\n  positionY\n  width\n  height\n  inputs {\n    ...EventRole\n    __typename\n  }\n  outputs {\n    ...EventRole\n    __typename\n  }\n  __typename\n}\n\nmutation CreateNaturalEventCategory($input: CreateNaturalEventCategoryInput!) {\n  createNaturalEventCategory(input: $input) {\n    ...NaturalEventCategory\n    __typename\n  }\n}"


class UpdateNaturalEventCategoryMutation(BaseModel):
    """No documentation found for this operation."""

    update_natural_event_category: NaturalEventCategory = Field(
        alias="updateNaturalEventCategory"
    )
    "Update an existing natural event category in the graph"

    class Arguments(BaseModel):
        """Arguments for UpdateNaturalEventCategory"""

        input: UpdateNaturalEventCategoryInput

    class Meta:
        """Meta class for UpdateNaturalEventCategory"""

        document = "fragment CategoryRef on Category {\n  id\n  key\n  label\n  ageName\n  __typename\n}\n\nfragment EntityDescriptor on EntityDescriptor {\n  keys\n  ontologyTerms\n  defaultCategoryKey\n  __typename\n}\n\nfragment MediaStore on MediaStore {\n  id\n  key\n  presignedUrl\n  __typename\n}\n\nfragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment CategoryBase on Category {\n  ...CategoryRef\n  description\n  purl\n  color\n  pinned\n  image {\n    ...MediaStore\n    __typename\n  }\n  graph {\n    id\n    name\n    __typename\n  }\n  term {\n    ...TermRef\n    __typename\n  }\n  __typename\n}\n\nfragment EventRole on EventRole {\n  key\n  role\n  descriptor {\n    ...EntityDescriptor\n    __typename\n  }\n  __typename\n}\n\nfragment NaturalEventCategory on NaturalEventCategory {\n  ...CategoryBase\n  positionX\n  positionY\n  width\n  height\n  inputs {\n    ...EventRole\n    __typename\n  }\n  outputs {\n    ...EventRole\n    __typename\n  }\n  __typename\n}\n\nmutation UpdateNaturalEventCategory($input: UpdateNaturalEventCategoryInput!) {\n  updateNaturalEventCategory(input: $input) {\n    ...NaturalEventCategory\n    __typename\n  }\n}"


class DeleteNaturalEventCategoryMutation(BaseModel):
    """No documentation found for this operation."""

    delete_natural_event_category: ID = Field(alias="deleteNaturalEventCategory")
    "Delete a natural event category from the graph"

    class Arguments(BaseModel):
        """Arguments for DeleteNaturalEventCategory"""

        input: DeleteNaturalEventCategoryInput

    class Meta:
        """Meta class for DeleteNaturalEventCategory"""

        document = "mutation DeleteNaturalEventCategory($input: DeleteNaturalEventCategoryInput!) {\n  deleteNaturalEventCategory(input: $input)\n}"


class CreateProtocolEventCategoryMutation(BaseModel):
    """No documentation found for this operation."""

    create_protocol_event_category: ProtocolEventCategory = Field(
        alias="createProtocolEventCategory"
    )
    "Create a new protocol event category in the graph"

    class Arguments(BaseModel):
        """Arguments for CreateProtocolEventCategory"""

        input: CreateProtocolEventCategoryInput

    class Meta:
        """Meta class for CreateProtocolEventCategory"""

        document = "fragment CategoryRef on Category {\n  id\n  key\n  label\n  ageName\n  __typename\n}\n\nfragment EntityDescriptor on EntityDescriptor {\n  keys\n  ontologyTerms\n  defaultCategoryKey\n  __typename\n}\n\nfragment MediaStore on MediaStore {\n  id\n  key\n  presignedUrl\n  __typename\n}\n\nfragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment CategoryBase on Category {\n  ...CategoryRef\n  description\n  purl\n  color\n  pinned\n  image {\n    ...MediaStore\n    __typename\n  }\n  graph {\n    id\n    name\n    __typename\n  }\n  term {\n    ...TermRef\n    __typename\n  }\n  __typename\n}\n\nfragment EventRole on EventRole {\n  key\n  role\n  descriptor {\n    ...EntityDescriptor\n    __typename\n  }\n  __typename\n}\n\nfragment ProtocolEventCategory on ProtocolEventCategory {\n  ...CategoryBase\n  positionX\n  positionY\n  width\n  height\n  inputs {\n    ...EventRole\n    __typename\n  }\n  outputs {\n    ...EventRole\n    __typename\n  }\n  __typename\n}\n\nmutation CreateProtocolEventCategory($input: CreateProtocolEventCategoryInput!) {\n  createProtocolEventCategory(input: $input) {\n    ...ProtocolEventCategory\n    __typename\n  }\n}"


class UpdateProtocolEventCategoryMutation(BaseModel):
    """No documentation found for this operation."""

    update_protocol_event_category: ProtocolEventCategory = Field(
        alias="updateProtocolEventCategory"
    )
    "Update an existing protocol event category in the graph"

    class Arguments(BaseModel):
        """Arguments for UpdateProtocolEventCategory"""

        input: UpdateProtocolEventCategoryInput

    class Meta:
        """Meta class for UpdateProtocolEventCategory"""

        document = "fragment CategoryRef on Category {\n  id\n  key\n  label\n  ageName\n  __typename\n}\n\nfragment EntityDescriptor on EntityDescriptor {\n  keys\n  ontologyTerms\n  defaultCategoryKey\n  __typename\n}\n\nfragment MediaStore on MediaStore {\n  id\n  key\n  presignedUrl\n  __typename\n}\n\nfragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment CategoryBase on Category {\n  ...CategoryRef\n  description\n  purl\n  color\n  pinned\n  image {\n    ...MediaStore\n    __typename\n  }\n  graph {\n    id\n    name\n    __typename\n  }\n  term {\n    ...TermRef\n    __typename\n  }\n  __typename\n}\n\nfragment EventRole on EventRole {\n  key\n  role\n  descriptor {\n    ...EntityDescriptor\n    __typename\n  }\n  __typename\n}\n\nfragment ProtocolEventCategory on ProtocolEventCategory {\n  ...CategoryBase\n  positionX\n  positionY\n  width\n  height\n  inputs {\n    ...EventRole\n    __typename\n  }\n  outputs {\n    ...EventRole\n    __typename\n  }\n  __typename\n}\n\nmutation UpdateProtocolEventCategory($input: UpdateProtocolEventCategoryInput!) {\n  updateProtocolEventCategory(input: $input) {\n    ...ProtocolEventCategory\n    __typename\n  }\n}"


class DeleteProtocolEventCategoryMutation(BaseModel):
    """No documentation found for this operation."""

    delete_protocol_event_category: ID = Field(alias="deleteProtocolEventCategory")
    "Delete a protocol event category from the graph"

    class Arguments(BaseModel):
        """Arguments for DeleteProtocolEventCategory"""

        input: DeleteProtocolEventCategoryInput

    class Meta:
        """Meta class for DeleteProtocolEventCategory"""

        document = "mutation DeleteProtocolEventCategory($input: DeleteProtocolEventCategoryInput!) {\n  deleteProtocolEventCategory(input: $input)\n}"


class AssertEntityExistsMutation(BaseModel):
    """---- existence: instances -----------------------------------------------------------------
    A write names a WORD (`term`), never a graph and never a category id."""

    assert_entity_exists: AssertedEntity = Field(alias="assertEntityExists")
    "Claim that an entity exists, under one of the organization's words. Returns the assertion and every view that draws it — empty when no view declares the word, which is an ordinary outcome"

    class Arguments(BaseModel):
        """Arguments for AssertEntityExists"""

        input: AssertEntityExistsInput

    class Meta:
        """Meta class for AssertEntityExists"""

        document = "fragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment CategoryRef on Category {\n  id\n  key\n  label\n  ageName\n  __typename\n}\n\nfragment InstanceRef on Instance {\n  id\n  kind\n  term {\n    ...TermRef\n    __typename\n  }\n  __typename\n}\n\nfragment NodeRef on Node {\n  id\n  label\n  __typename\n}\n\nfragment Assertion on Assertion {\n  id\n  subject\n  appId\n  actionId\n  actionName\n  assertedAt\n  recordedAt\n  seq\n  __typename\n}\n\nfragment Instance on Instance {\n  ...InstanceRef\n  createdAt\n  component\n  assertion {\n    ...Assertion\n    __typename\n  }\n  __typename\n}\n\nfragment NodeDrawing on NodeDrawing {\n  graph {\n    id\n    name\n    __typename\n  }\n  category {\n    ...CategoryRef\n    __typename\n  }\n  node {\n    ...NodeRef\n    __typename\n  }\n  __typename\n}\n\nfragment AssertedEntity on AssertedEntity {\n  assertion {\n    ...Assertion\n    __typename\n  }\n  instance {\n    ...Instance\n    __typename\n  }\n  drawings {\n    ...NodeDrawing\n    __typename\n  }\n  __typename\n}\n\nmutation AssertEntityExists($input: AssertEntityExistsInput!) {\n  assertEntityExists(input: $input) {\n    ...AssertedEntity\n    __typename\n  }\n}"


class AssertNaturalEventExistsMutation(BaseModel):
    """No documentation found for this operation."""

    assert_natural_event_exists: AssertedNaturalEvent = Field(
        alias="assertNaturalEventExists"
    )
    "Claim that a natural event happened, under one of the organization's words"

    class Arguments(BaseModel):
        """Arguments for AssertNaturalEventExists"""

        input: AssertNaturalEventExistsInput

    class Meta:
        """Meta class for AssertNaturalEventExists"""

        document = "fragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment CategoryRef on Category {\n  id\n  key\n  label\n  ageName\n  __typename\n}\n\nfragment InstanceRef on Instance {\n  id\n  kind\n  term {\n    ...TermRef\n    __typename\n  }\n  __typename\n}\n\nfragment NodeRef on Node {\n  id\n  label\n  __typename\n}\n\nfragment Assertion on Assertion {\n  id\n  subject\n  appId\n  actionId\n  actionName\n  assertedAt\n  recordedAt\n  seq\n  __typename\n}\n\nfragment Instance on Instance {\n  ...InstanceRef\n  createdAt\n  component\n  assertion {\n    ...Assertion\n    __typename\n  }\n  __typename\n}\n\nfragment NodeDrawing on NodeDrawing {\n  graph {\n    id\n    name\n    __typename\n  }\n  category {\n    ...CategoryRef\n    __typename\n  }\n  node {\n    ...NodeRef\n    __typename\n  }\n  __typename\n}\n\nfragment AssertedNaturalEvent on AssertedNaturalEvent {\n  assertion {\n    ...Assertion\n    __typename\n  }\n  instance {\n    ...Instance\n    __typename\n  }\n  drawings {\n    ...NodeDrawing\n    __typename\n  }\n  __typename\n}\n\nmutation AssertNaturalEventExists($input: AssertNaturalEventExistsInput!) {\n  assertNaturalEventExists(input: $input) {\n    ...AssertedNaturalEvent\n    __typename\n  }\n}"


class AssertProtocolEventExistsMutation(BaseModel):
    """No documentation found for this operation."""

    assert_protocol_event_exists: AssertedProtocolEvent = Field(
        alias="assertProtocolEventExists"
    )
    "Claim that a protocol step happened, under one of the organization's words"

    class Arguments(BaseModel):
        """Arguments for AssertProtocolEventExists"""

        input: AssertProtocolEventExistsInput

    class Meta:
        """Meta class for AssertProtocolEventExists"""

        document = "fragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment CategoryRef on Category {\n  id\n  key\n  label\n  ageName\n  __typename\n}\n\nfragment InstanceRef on Instance {\n  id\n  kind\n  term {\n    ...TermRef\n    __typename\n  }\n  __typename\n}\n\nfragment NodeRef on Node {\n  id\n  label\n  __typename\n}\n\nfragment Assertion on Assertion {\n  id\n  subject\n  appId\n  actionId\n  actionName\n  assertedAt\n  recordedAt\n  seq\n  __typename\n}\n\nfragment Instance on Instance {\n  ...InstanceRef\n  createdAt\n  component\n  assertion {\n    ...Assertion\n    __typename\n  }\n  __typename\n}\n\nfragment NodeDrawing on NodeDrawing {\n  graph {\n    id\n    name\n    __typename\n  }\n  category {\n    ...CategoryRef\n    __typename\n  }\n  node {\n    ...NodeRef\n    __typename\n  }\n  __typename\n}\n\nfragment AssertedProtocolEvent on AssertedProtocolEvent {\n  assertion {\n    ...Assertion\n    __typename\n  }\n  instance {\n    ...Instance\n    __typename\n  }\n  drawings {\n    ...NodeDrawing\n    __typename\n  }\n  __typename\n}\n\nmutation AssertProtocolEventExists($input: AssertProtocolEventExistsInput!) {\n  assertProtocolEventExists(input: $input) {\n    ...AssertedProtocolEvent\n    __typename\n  }\n}"


class ClassifyNodesMutation(BaseModel):
    """One assertion over many (node, term) pairs — a batch is one act."""

    classify_nodes: AssertedInstances = Field(alias="classifyNodes")
    "Claim that several nodes are of a word, without displacing anyone else's claim. One act, one assertion"

    class Arguments(BaseModel):
        """Arguments for ClassifyNodes"""

        input: ClassifyNodesInput

    class Meta:
        """Meta class for ClassifyNodes"""

        document = "fragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment CategoryRef on Category {\n  id\n  key\n  label\n  ageName\n  __typename\n}\n\nfragment InstanceRef on Instance {\n  id\n  kind\n  term {\n    ...TermRef\n    __typename\n  }\n  __typename\n}\n\nfragment NodeRef on Node {\n  id\n  label\n  __typename\n}\n\nfragment Assertion on Assertion {\n  id\n  subject\n  appId\n  actionId\n  actionName\n  assertedAt\n  recordedAt\n  seq\n  __typename\n}\n\nfragment Instance on Instance {\n  ...InstanceRef\n  createdAt\n  component\n  assertion {\n    ...Assertion\n    __typename\n  }\n  __typename\n}\n\nfragment NodeDrawing on NodeDrawing {\n  graph {\n    id\n    name\n    __typename\n  }\n  category {\n    ...CategoryRef\n    __typename\n  }\n  node {\n    ...NodeRef\n    __typename\n  }\n  __typename\n}\n\nfragment AssertedInstances on AssertedInstances {\n  assertion {\n    ...Assertion\n    __typename\n  }\n  instances {\n    ...Instance\n    __typename\n  }\n  drawings {\n    ...NodeDrawing\n    __typename\n  }\n  __typename\n}\n\nmutation ClassifyNodes($input: ClassifyNodesInput!) {\n  classifyNodes(input: $input) {\n    ...AssertedInstances\n    __typename\n  }\n}"


class AssertSameInstanceMutation(BaseModel):
    """No documentation found for this operation."""

    assert_same_instance: AssertedSameness = Field(alias="assertSameInstance")
    "Claim that several already-recorded instances are one thing. An equivalence with no primary — the order of the ids carries no meaning"

    class Arguments(BaseModel):
        """Arguments for AssertSameInstance"""

        input: AssertSameInstanceInput

    class Meta:
        """Meta class for AssertSameInstance"""

        document = "fragment LinkRef on Link {\n  id\n  kind\n  sourceRef\n  targetRef\n  __typename\n}\n\nfragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment Assertion on Assertion {\n  id\n  subject\n  appId\n  actionId\n  actionName\n  assertedAt\n  recordedAt\n  seq\n  __typename\n}\n\nfragment Link on Link {\n  ...LinkRef\n  role\n  createdAt\n  term {\n    ...TermRef\n    __typename\n  }\n  assertion {\n    ...Assertion\n    __typename\n  }\n  __typename\n}\n\nfragment AssertedSameness on AssertedSameness {\n  assertion {\n    ...Assertion\n    __typename\n  }\n  links {\n    ...Link\n    __typename\n  }\n  __typename\n}\n\nmutation AssertSameInstance($input: AssertSameInstanceInput!) {\n  assertSameInstance(input: $input) {\n    ...AssertedSameness\n    __typename\n  }\n}"


class AssertStructureExistsMutation(BaseModel):
    """---- structures and metrics ---------------------------------------------------------------"""

    assert_structure_exists: AssertedStructure = Field(alias="assertStructureExists")
    "Claim that an external datum exists. Idempotent by (identifier, object): a second claim about a datum already on the record is agreement, recorded as a standing under this act (RFC 0023)"

    class Arguments(BaseModel):
        """Arguments for AssertStructureExists"""

        input: AssertStructureExistsInput

    class Meta:
        """Meta class for AssertStructureExists"""

        document = "fragment Metric on Metric {\n  id\n  kindId\n  key\n  value\n  unit\n  confidence\n  confidenceType\n  observedAt\n  assertedAt\n  __typename\n}\n\nfragment Structure on Structure {\n  id\n  identifier\n  object\n  kindId\n  __typename\n}\n\nfragment Assertion on Assertion {\n  id\n  subject\n  appId\n  actionId\n  actionName\n  assertedAt\n  recordedAt\n  seq\n  __typename\n}\n\nfragment StructureWithMetrics on Structure {\n  ...Structure\n  metrics {\n    ...Metric\n    __typename\n  }\n  __typename\n}\n\nfragment AssertedStructure on AssertedStructure {\n  assertion {\n    ...Assertion\n    __typename\n  }\n  structure {\n    ...StructureWithMetrics\n    __typename\n  }\n  __typename\n}\n\nmutation AssertStructureExists($input: AssertStructureExistsInput!) {\n  assertStructureExists(input: $input) {\n    ...AssertedStructure\n    __typename\n  }\n}"


class AssertMetricValueMutation(BaseModel):
    """No documentation found for this operation."""

    assert_metric_value: AssertedMetric = Field(alias="assertMetricValue")
    "Record a measurement, creating the structure it describes if this is its first sight. One assertion covers both"

    class Arguments(BaseModel):
        """Arguments for AssertMetricValue"""

        input: AssertMetricValueInput

    class Meta:
        """Meta class for AssertMetricValue"""

        document = "fragment Assertion on Assertion {\n  id\n  subject\n  appId\n  actionId\n  actionName\n  assertedAt\n  recordedAt\n  seq\n  __typename\n}\n\nfragment Metric on Metric {\n  id\n  kindId\n  key\n  value\n  unit\n  confidence\n  confidenceType\n  observedAt\n  assertedAt\n  __typename\n}\n\nfragment AssertedMetric on AssertedMetric {\n  assertion {\n    ...Assertion\n    __typename\n  }\n  metric {\n    ...Metric\n    __typename\n  }\n  __typename\n}\n\nmutation AssertMetricValue($input: AssertMetricValueInput!) {\n  assertMetricValue(input: $input) {\n    ...AssertedMetric\n    __typename\n  }\n}"


class AssertMetricValueForStructureMutation(BaseModel):
    """No documentation found for this operation."""

    assert_metric_value_for_structure: AssertedMetric = Field(
        alias="assertMetricValueForStructure"
    )
    "Record a measurement against a structure that already exists, named by its evidence id"

    class Arguments(BaseModel):
        """Arguments for AssertMetricValueForStructure"""

        input: AssertMetricValueForStructureInput

    class Meta:
        """Meta class for AssertMetricValueForStructure"""

        document = "fragment Assertion on Assertion {\n  id\n  subject\n  appId\n  actionId\n  actionName\n  assertedAt\n  recordedAt\n  seq\n  __typename\n}\n\nfragment Metric on Metric {\n  id\n  kindId\n  key\n  value\n  unit\n  confidence\n  confidenceType\n  observedAt\n  assertedAt\n  __typename\n}\n\nfragment AssertedMetric on AssertedMetric {\n  assertion {\n    ...Assertion\n    __typename\n  }\n  metric {\n    ...Metric\n    __typename\n  }\n  __typename\n}\n\nmutation AssertMetricValueForStructure($input: AssertMetricValueForStructureInput!) {\n  assertMetricValueForStructure(input: $input) {\n    ...AssertedMetric\n    __typename\n  }\n}"


class SupersedeMetricValueMutation(BaseModel):
    """Retracting Standing + the new Metric under ONE assertion. Returns a metric with a NEW id."""

    supersede_metric_value: AssertedMetric = Field(alias="supersedeMetricValue")
    "Correct a measurement by retracting it and asserting a new one. The returned metric has a new id: it is a new row, not an edited one"

    class Arguments(BaseModel):
        """Arguments for SupersedeMetricValue"""

        input: SupersedeMetricValueInput

    class Meta:
        """Meta class for SupersedeMetricValue"""

        document = "fragment Assertion on Assertion {\n  id\n  subject\n  appId\n  actionId\n  actionName\n  assertedAt\n  recordedAt\n  seq\n  __typename\n}\n\nfragment Metric on Metric {\n  id\n  kindId\n  key\n  value\n  unit\n  confidence\n  confidenceType\n  observedAt\n  assertedAt\n  __typename\n}\n\nfragment AssertedMetric on AssertedMetric {\n  assertion {\n    ...Assertion\n    __typename\n  }\n  metric {\n    ...Metric\n    __typename\n  }\n  __typename\n}\n\nmutation SupersedeMetricValue($input: SupersedeMetricValueInput!) {\n  supersedeMetricValue(input: $input) {\n    ...AssertedMetric\n    __typename\n  }\n}"


class AssertRelationExistsMutation(BaseModel):
    """---- links ---------------------------------------------------------------------------------"""

    assert_relation_exists: AssertedRelation = Field(alias="assertRelationExists")
    "Assert a relation between two entities, under one of the organization's words"

    class Arguments(BaseModel):
        """Arguments for AssertRelationExists"""

        input: AssertRelationExistsInput

    class Meta:
        """Meta class for AssertRelationExists"""

        document = "fragment CategoryRef on Category {\n  id\n  key\n  label\n  ageName\n  __typename\n}\n\nfragment LinkRef on Link {\n  id\n  kind\n  sourceRef\n  targetRef\n  __typename\n}\n\nfragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment Assertion on Assertion {\n  id\n  subject\n  appId\n  actionId\n  actionName\n  assertedAt\n  recordedAt\n  seq\n  __typename\n}\n\nfragment EdgeDrawing on EdgeDrawing {\n  graph {\n    id\n    name\n    __typename\n  }\n  category {\n    ...CategoryRef\n    __typename\n  }\n  __typename\n}\n\nfragment Link on Link {\n  ...LinkRef\n  role\n  createdAt\n  term {\n    ...TermRef\n    __typename\n  }\n  assertion {\n    ...Assertion\n    __typename\n  }\n  __typename\n}\n\nfragment AssertedRelation on AssertedRelation {\n  assertion {\n    ...Assertion\n    __typename\n  }\n  link {\n    ...Link\n    __typename\n  }\n  drawings {\n    ...EdgeDrawing\n    __typename\n  }\n  __typename\n}\n\nmutation AssertRelationExists($input: AssertRelationExistsInput!) {\n  assertRelationExists(input: $input) {\n    ...AssertedRelation\n    __typename\n  }\n}"


class AssertMeasurementExistsMutation(BaseModel):
    """No documentation found for this operation."""

    assert_measurement_exists: AssertedMeasurement = Field(
        alias="assertMeasurementExists"
    )
    "Assert that a structure measures an entity, under one of the organization's words. Drawings are always empty: a measurement has no AGE edge"

    class Arguments(BaseModel):
        """Arguments for AssertMeasurementExists"""

        input: AssertMeasurementExistsInput

    class Meta:
        """Meta class for AssertMeasurementExists"""

        document = "fragment LinkRef on Link {\n  id\n  kind\n  sourceRef\n  targetRef\n  __typename\n}\n\nfragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment Assertion on Assertion {\n  id\n  subject\n  appId\n  actionId\n  actionName\n  assertedAt\n  recordedAt\n  seq\n  __typename\n}\n\nfragment Link on Link {\n  ...LinkRef\n  role\n  createdAt\n  term {\n    ...TermRef\n    __typename\n  }\n  assertion {\n    ...Assertion\n    __typename\n  }\n  __typename\n}\n\nfragment AssertedMeasurement on AssertedMeasurement {\n  assertion {\n    ...Assertion\n    __typename\n  }\n  link {\n    ...Link\n    __typename\n  }\n  __typename\n}\n\nmutation AssertMeasurementExists($input: AssertMeasurementExistsInput!) {\n  assertMeasurementExists(input: $input) {\n    ...AssertedMeasurement\n    __typename\n  }\n}"


class AssertStructureRelationExistsMutation(BaseModel):
    """No documentation found for this operation."""

    assert_structure_relation_exists: AssertedStructureRelation = Field(
        alias="assertStructureRelationExists"
    )
    "Assert a relation between two structures. Drawings are always empty: neither endpoint has a vertex"

    class Arguments(BaseModel):
        """Arguments for AssertStructureRelationExists"""

        input: AssertStructureRelationExistsInput

    class Meta:
        """Meta class for AssertStructureRelationExists"""

        document = "fragment LinkRef on Link {\n  id\n  kind\n  sourceRef\n  targetRef\n  __typename\n}\n\nfragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment Assertion on Assertion {\n  id\n  subject\n  appId\n  actionId\n  actionName\n  assertedAt\n  recordedAt\n  seq\n  __typename\n}\n\nfragment Link on Link {\n  ...LinkRef\n  role\n  createdAt\n  term {\n    ...TermRef\n    __typename\n  }\n  assertion {\n    ...Assertion\n    __typename\n  }\n  __typename\n}\n\nfragment AssertedStructureRelation on AssertedStructureRelation {\n  assertion {\n    ...Assertion\n    __typename\n  }\n  link {\n    ...Link\n    __typename\n  }\n  __typename\n}\n\nmutation AssertStructureRelationExists($input: AssertStructureRelationExistsInput!) {\n  assertStructureRelationExists(input: $input) {\n    ...AssertedStructureRelation\n    __typename\n  }\n}"


class AssertParticipationMutation(BaseModel):
    """No documentation found for this operation."""

    assert_participation: AssertedParticipation = Field(alias="assertParticipation")
    "Claim that an entity took part in an event, without displacing anyone else's claim"

    class Arguments(BaseModel):
        """Arguments for AssertParticipation"""

        input: AssertParticipationInput

    class Meta:
        """Meta class for AssertParticipation"""

        document = "fragment CategoryRef on Category {\n  id\n  key\n  label\n  ageName\n  __typename\n}\n\nfragment LinkRef on Link {\n  id\n  kind\n  sourceRef\n  targetRef\n  __typename\n}\n\nfragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment Assertion on Assertion {\n  id\n  subject\n  appId\n  actionId\n  actionName\n  assertedAt\n  recordedAt\n  seq\n  __typename\n}\n\nfragment EdgeDrawing on EdgeDrawing {\n  graph {\n    id\n    name\n    __typename\n  }\n  category {\n    ...CategoryRef\n    __typename\n  }\n  __typename\n}\n\nfragment Link on Link {\n  ...LinkRef\n  role\n  createdAt\n  term {\n    ...TermRef\n    __typename\n  }\n  assertion {\n    ...Assertion\n    __typename\n  }\n  __typename\n}\n\nfragment AssertedParticipation on AssertedParticipation {\n  assertion {\n    ...Assertion\n    __typename\n  }\n  link {\n    ...Link\n    __typename\n  }\n  drawings {\n    ...EdgeDrawing\n    __typename\n  }\n  __typename\n}\n\nmutation AssertParticipation($input: AssertParticipationInput!) {\n  assertParticipation(input: $input) {\n    ...AssertedParticipation\n    __typename\n  }\n}"


class AssertParticipationsMutation(BaseModel):
    """Many participants in one event, one assertion."""

    assert_participations: AssertedLinks = Field(alias="assertParticipations")
    "Claim that several entities took part in one event, as one act and one assertion"

    class Arguments(BaseModel):
        """Arguments for AssertParticipations"""

        input: AssertParticipationsInput

    class Meta:
        """Meta class for AssertParticipations"""

        document = "fragment CategoryRef on Category {\n  id\n  key\n  label\n  ageName\n  __typename\n}\n\nfragment LinkRef on Link {\n  id\n  kind\n  sourceRef\n  targetRef\n  __typename\n}\n\nfragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment Assertion on Assertion {\n  id\n  subject\n  appId\n  actionId\n  actionName\n  assertedAt\n  recordedAt\n  seq\n  __typename\n}\n\nfragment EdgeDrawing on EdgeDrawing {\n  graph {\n    id\n    name\n    __typename\n  }\n  category {\n    ...CategoryRef\n    __typename\n  }\n  __typename\n}\n\nfragment Link on Link {\n  ...LinkRef\n  role\n  createdAt\n  term {\n    ...TermRef\n    __typename\n  }\n  assertion {\n    ...Assertion\n    __typename\n  }\n  __typename\n}\n\nfragment AssertedLinks on AssertedLinks {\n  assertion {\n    ...Assertion\n    __typename\n  }\n  links {\n    ...Link\n    __typename\n  }\n  drawings {\n    ...EdgeDrawing\n    __typename\n  }\n  __typename\n}\n\nmutation AssertParticipations($input: AssertParticipationsInput!) {\n  assertParticipations(input: $input) {\n    ...AssertedLinks\n    __typename\n  }\n}"


class CommentOnStructureMutation(BaseModel):
    """---- comments ------------------------------------------------------------------------------"""

    comment_on_structure: AssertedComment = Field(alias="commentOnStructure")
    "Record a remark about an external datum, minting its structure if this is the first sight of it. A reply names its parent and stays on the parent's thread"

    class Arguments(BaseModel):
        """Arguments for CommentOnStructure"""

        input: CommentOnStructureInput

    class Meta:
        """Meta class for CommentOnStructure"""

        document = "fragment Assertion on Assertion {\n  id\n  subject\n  appId\n  actionId\n  actionName\n  assertedAt\n  recordedAt\n  seq\n  __typename\n}\n\nfragment Comment on Comment {\n  id\n  createdAt\n  text\n  resolved\n  mentions\n  parent {\n    id\n    __typename\n  }\n  assertion {\n    ...Assertion\n    __typename\n  }\n  __typename\n}\n\nfragment AssertedComment on AssertedComment {\n  assertion {\n    ...Assertion\n    __typename\n  }\n  comment {\n    ...Comment\n    __typename\n  }\n  __typename\n}\n\nmutation CommentOnStructure($input: CommentOnStructureInput!) {\n  commentOnStructure(input: $input) {\n    ...AssertedComment\n    __typename\n  }\n}"


class CreateGraphMutation(BaseModel):
    """A Graph is a VIEW over the organization's claims, not a container. `definition.extensions`
    carries a whole ontology, so one call can declare every word this view means to draw, and
    `backfill` projects the claims those words already admit."""

    create_graph: Graph = Field(alias="createGraph")
    "Create a new graph in the graph engine"

    class Arguments(BaseModel):
        """Arguments for CreateGraph"""

        input: CreateGraphInput

    class Meta:
        """Meta class for CreateGraph"""

        document = "fragment CategoryRef on Category {\n  id\n  key\n  label\n  ageName\n  __typename\n}\n\nfragment MediaStore on MediaStore {\n  id\n  key\n  presignedUrl\n  __typename\n}\n\nfragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment CategoryBase on Category {\n  ...CategoryRef\n  description\n  purl\n  color\n  pinned\n  image {\n    ...MediaStore\n    __typename\n  }\n  graph {\n    id\n    name\n    __typename\n  }\n  term {\n    ...TermRef\n    __typename\n  }\n  __typename\n}\n\nfragment EntityDescriptor on EntityDescriptor {\n  keys\n  ontologyTerms\n  defaultCategoryKey\n  __typename\n}\n\nfragment EventRole on EventRole {\n  key\n  role\n  descriptor {\n    ...EntityDescriptor\n    __typename\n  }\n  __typename\n}\n\nfragment PropertyDefinition on PropertyDefinition {\n  key\n  label\n  valueKind\n  unit\n  description\n  derivation\n  index\n  searchable\n  __typename\n}\n\nfragment StructureDescriptor on StructureDescriptor {\n  defaultCategoryKey\n  __typename\n}\n\nfragment EntityCategory on EntityCategory {\n  ...CategoryBase\n  instanceKind\n  positionX\n  positionY\n  width\n  height\n  propertyDefinitions {\n    ...PropertyDefinition\n    __typename\n  }\n  __typename\n}\n\nfragment GraphProjection on GraphProjection {\n  kind\n  status\n  projectedThroughSeq\n  derivedThroughSeq\n  lag\n  pending\n  schemaStale\n  schemaHash\n  derivedAt\n  rebuiltAt\n  __typename\n}\n\nfragment ListGraph on Graph {\n  id\n  name\n  description\n  ageName\n  isArchived\n  pinned\n  __typename\n}\n\nfragment MeasurementCategory on MeasurementCategory {\n  ...CategoryBase\n  sourceDescriptor {\n    ...StructureDescriptor\n    __typename\n  }\n  targetDescriptor {\n    ...EntityDescriptor\n    __typename\n  }\n  propertyDefinitions {\n    ...PropertyDefinition\n    __typename\n  }\n  __typename\n}\n\nfragment NaturalEventCategory on NaturalEventCategory {\n  ...CategoryBase\n  positionX\n  positionY\n  width\n  height\n  inputs {\n    ...EventRole\n    __typename\n  }\n  outputs {\n    ...EventRole\n    __typename\n  }\n  __typename\n}\n\nfragment ProtocolEventCategory on ProtocolEventCategory {\n  ...CategoryBase\n  positionX\n  positionY\n  width\n  height\n  inputs {\n    ...EventRole\n    __typename\n  }\n  outputs {\n    ...EventRole\n    __typename\n  }\n  __typename\n}\n\nfragment RelationCategory on RelationCategory {\n  ...CategoryBase\n  sourceDescriptor {\n    ...EntityDescriptor\n    __typename\n  }\n  targetDescriptor {\n    ...EntityDescriptor\n    __typename\n  }\n  propertyDefinitions {\n    ...PropertyDefinition\n    __typename\n  }\n  __typename\n}\n\nfragment StructureRelationCategory on StructureRelationCategory {\n  ...CategoryBase\n  sourceDescriptor {\n    ...StructureDescriptor\n    __typename\n  }\n  targetDescriptor {\n    ...StructureDescriptor\n    __typename\n  }\n  propertyDefinitions {\n    ...PropertyDefinition\n    __typename\n  }\n  __typename\n}\n\nfragment Graph on Graph {\n  ...ListGraph\n  purl\n  projection {\n    ...GraphProjection\n    __typename\n  }\n  entityCategories {\n    ...EntityCategory\n    __typename\n  }\n  relationCategories {\n    ...RelationCategory\n    __typename\n  }\n  measurementCategories {\n    ...MeasurementCategory\n    __typename\n  }\n  structureRelationCategories {\n    ...StructureRelationCategory\n    __typename\n  }\n  naturalEventCategories {\n    ...NaturalEventCategory\n    __typename\n  }\n  protocolEventCategories {\n    ...ProtocolEventCategory\n    __typename\n  }\n  __typename\n}\n\nmutation CreateGraph($input: CreateGraphInput!) {\n  createGraph(input: $input) {\n    ...Graph\n    __typename\n  }\n}"


class UpdateGraphMutation(BaseModel):
    """No documentation found for this operation."""

    update_graph: Graph = Field(alias="updateGraph")
    "Update an existing graph in the graph engine"

    class Arguments(BaseModel):
        """Arguments for UpdateGraph"""

        input: UpdateGraphInput

    class Meta:
        """Meta class for UpdateGraph"""

        document = "fragment CategoryRef on Category {\n  id\n  key\n  label\n  ageName\n  __typename\n}\n\nfragment MediaStore on MediaStore {\n  id\n  key\n  presignedUrl\n  __typename\n}\n\nfragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment CategoryBase on Category {\n  ...CategoryRef\n  description\n  purl\n  color\n  pinned\n  image {\n    ...MediaStore\n    __typename\n  }\n  graph {\n    id\n    name\n    __typename\n  }\n  term {\n    ...TermRef\n    __typename\n  }\n  __typename\n}\n\nfragment EntityDescriptor on EntityDescriptor {\n  keys\n  ontologyTerms\n  defaultCategoryKey\n  __typename\n}\n\nfragment EventRole on EventRole {\n  key\n  role\n  descriptor {\n    ...EntityDescriptor\n    __typename\n  }\n  __typename\n}\n\nfragment PropertyDefinition on PropertyDefinition {\n  key\n  label\n  valueKind\n  unit\n  description\n  derivation\n  index\n  searchable\n  __typename\n}\n\nfragment StructureDescriptor on StructureDescriptor {\n  defaultCategoryKey\n  __typename\n}\n\nfragment EntityCategory on EntityCategory {\n  ...CategoryBase\n  instanceKind\n  positionX\n  positionY\n  width\n  height\n  propertyDefinitions {\n    ...PropertyDefinition\n    __typename\n  }\n  __typename\n}\n\nfragment GraphProjection on GraphProjection {\n  kind\n  status\n  projectedThroughSeq\n  derivedThroughSeq\n  lag\n  pending\n  schemaStale\n  schemaHash\n  derivedAt\n  rebuiltAt\n  __typename\n}\n\nfragment ListGraph on Graph {\n  id\n  name\n  description\n  ageName\n  isArchived\n  pinned\n  __typename\n}\n\nfragment MeasurementCategory on MeasurementCategory {\n  ...CategoryBase\n  sourceDescriptor {\n    ...StructureDescriptor\n    __typename\n  }\n  targetDescriptor {\n    ...EntityDescriptor\n    __typename\n  }\n  propertyDefinitions {\n    ...PropertyDefinition\n    __typename\n  }\n  __typename\n}\n\nfragment NaturalEventCategory on NaturalEventCategory {\n  ...CategoryBase\n  positionX\n  positionY\n  width\n  height\n  inputs {\n    ...EventRole\n    __typename\n  }\n  outputs {\n    ...EventRole\n    __typename\n  }\n  __typename\n}\n\nfragment ProtocolEventCategory on ProtocolEventCategory {\n  ...CategoryBase\n  positionX\n  positionY\n  width\n  height\n  inputs {\n    ...EventRole\n    __typename\n  }\n  outputs {\n    ...EventRole\n    __typename\n  }\n  __typename\n}\n\nfragment RelationCategory on RelationCategory {\n  ...CategoryBase\n  sourceDescriptor {\n    ...EntityDescriptor\n    __typename\n  }\n  targetDescriptor {\n    ...EntityDescriptor\n    __typename\n  }\n  propertyDefinitions {\n    ...PropertyDefinition\n    __typename\n  }\n  __typename\n}\n\nfragment StructureRelationCategory on StructureRelationCategory {\n  ...CategoryBase\n  sourceDescriptor {\n    ...StructureDescriptor\n    __typename\n  }\n  targetDescriptor {\n    ...StructureDescriptor\n    __typename\n  }\n  propertyDefinitions {\n    ...PropertyDefinition\n    __typename\n  }\n  __typename\n}\n\nfragment Graph on Graph {\n  ...ListGraph\n  purl\n  projection {\n    ...GraphProjection\n    __typename\n  }\n  entityCategories {\n    ...EntityCategory\n    __typename\n  }\n  relationCategories {\n    ...RelationCategory\n    __typename\n  }\n  measurementCategories {\n    ...MeasurementCategory\n    __typename\n  }\n  structureRelationCategories {\n    ...StructureRelationCategory\n    __typename\n  }\n  naturalEventCategories {\n    ...NaturalEventCategory\n    __typename\n  }\n  protocolEventCategories {\n    ...ProtocolEventCategory\n    __typename\n  }\n  __typename\n}\n\nmutation UpdateGraph($input: UpdateGraphInput!) {\n  updateGraph(input: $input) {\n    ...Graph\n    __typename\n  }\n}"


class UpdateGraphVisualMutation(BaseModel):
    """No documentation found for this operation."""

    update_graph_visual: Graph = Field(alias="updateGraphVisual")
    "Update the visual configuration of a graph in the graph engine"

    class Arguments(BaseModel):
        """Arguments for UpdateGraphVisual"""

        input: UpdateGraphVisualInput

    class Meta:
        """Meta class for UpdateGraphVisual"""

        document = "fragment CategoryRef on Category {\n  id\n  key\n  label\n  ageName\n  __typename\n}\n\nfragment MediaStore on MediaStore {\n  id\n  key\n  presignedUrl\n  __typename\n}\n\nfragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment CategoryBase on Category {\n  ...CategoryRef\n  description\n  purl\n  color\n  pinned\n  image {\n    ...MediaStore\n    __typename\n  }\n  graph {\n    id\n    name\n    __typename\n  }\n  term {\n    ...TermRef\n    __typename\n  }\n  __typename\n}\n\nfragment EntityDescriptor on EntityDescriptor {\n  keys\n  ontologyTerms\n  defaultCategoryKey\n  __typename\n}\n\nfragment EventRole on EventRole {\n  key\n  role\n  descriptor {\n    ...EntityDescriptor\n    __typename\n  }\n  __typename\n}\n\nfragment PropertyDefinition on PropertyDefinition {\n  key\n  label\n  valueKind\n  unit\n  description\n  derivation\n  index\n  searchable\n  __typename\n}\n\nfragment StructureDescriptor on StructureDescriptor {\n  defaultCategoryKey\n  __typename\n}\n\nfragment EntityCategory on EntityCategory {\n  ...CategoryBase\n  instanceKind\n  positionX\n  positionY\n  width\n  height\n  propertyDefinitions {\n    ...PropertyDefinition\n    __typename\n  }\n  __typename\n}\n\nfragment GraphProjection on GraphProjection {\n  kind\n  status\n  projectedThroughSeq\n  derivedThroughSeq\n  lag\n  pending\n  schemaStale\n  schemaHash\n  derivedAt\n  rebuiltAt\n  __typename\n}\n\nfragment ListGraph on Graph {\n  id\n  name\n  description\n  ageName\n  isArchived\n  pinned\n  __typename\n}\n\nfragment MeasurementCategory on MeasurementCategory {\n  ...CategoryBase\n  sourceDescriptor {\n    ...StructureDescriptor\n    __typename\n  }\n  targetDescriptor {\n    ...EntityDescriptor\n    __typename\n  }\n  propertyDefinitions {\n    ...PropertyDefinition\n    __typename\n  }\n  __typename\n}\n\nfragment NaturalEventCategory on NaturalEventCategory {\n  ...CategoryBase\n  positionX\n  positionY\n  width\n  height\n  inputs {\n    ...EventRole\n    __typename\n  }\n  outputs {\n    ...EventRole\n    __typename\n  }\n  __typename\n}\n\nfragment ProtocolEventCategory on ProtocolEventCategory {\n  ...CategoryBase\n  positionX\n  positionY\n  width\n  height\n  inputs {\n    ...EventRole\n    __typename\n  }\n  outputs {\n    ...EventRole\n    __typename\n  }\n  __typename\n}\n\nfragment RelationCategory on RelationCategory {\n  ...CategoryBase\n  sourceDescriptor {\n    ...EntityDescriptor\n    __typename\n  }\n  targetDescriptor {\n    ...EntityDescriptor\n    __typename\n  }\n  propertyDefinitions {\n    ...PropertyDefinition\n    __typename\n  }\n  __typename\n}\n\nfragment StructureRelationCategory on StructureRelationCategory {\n  ...CategoryBase\n  sourceDescriptor {\n    ...StructureDescriptor\n    __typename\n  }\n  targetDescriptor {\n    ...StructureDescriptor\n    __typename\n  }\n  propertyDefinitions {\n    ...PropertyDefinition\n    __typename\n  }\n  __typename\n}\n\nfragment Graph on Graph {\n  ...ListGraph\n  purl\n  projection {\n    ...GraphProjection\n    __typename\n  }\n  entityCategories {\n    ...EntityCategory\n    __typename\n  }\n  relationCategories {\n    ...RelationCategory\n    __typename\n  }\n  measurementCategories {\n    ...MeasurementCategory\n    __typename\n  }\n  structureRelationCategories {\n    ...StructureRelationCategory\n    __typename\n  }\n  naturalEventCategories {\n    ...NaturalEventCategory\n    __typename\n  }\n  protocolEventCategories {\n    ...ProtocolEventCategory\n    __typename\n  }\n  __typename\n}\n\nmutation UpdateGraphVisual($input: UpdateGraphVisualInput!) {\n  updateGraphVisual(input: $input) {\n    ...Graph\n    __typename\n  }\n}"


class ArchiveGraphMutation(BaseModel):
    """No documentation found for this operation."""

    archive_graph: Graph = Field(alias="archiveGraph")
    "Archive a graph in the graph engine (soft delete)"

    class Arguments(BaseModel):
        """Arguments for ArchiveGraph"""

        input: ArchiveGraphInput

    class Meta:
        """Meta class for ArchiveGraph"""

        document = "fragment CategoryRef on Category {\n  id\n  key\n  label\n  ageName\n  __typename\n}\n\nfragment MediaStore on MediaStore {\n  id\n  key\n  presignedUrl\n  __typename\n}\n\nfragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment CategoryBase on Category {\n  ...CategoryRef\n  description\n  purl\n  color\n  pinned\n  image {\n    ...MediaStore\n    __typename\n  }\n  graph {\n    id\n    name\n    __typename\n  }\n  term {\n    ...TermRef\n    __typename\n  }\n  __typename\n}\n\nfragment EntityDescriptor on EntityDescriptor {\n  keys\n  ontologyTerms\n  defaultCategoryKey\n  __typename\n}\n\nfragment EventRole on EventRole {\n  key\n  role\n  descriptor {\n    ...EntityDescriptor\n    __typename\n  }\n  __typename\n}\n\nfragment PropertyDefinition on PropertyDefinition {\n  key\n  label\n  valueKind\n  unit\n  description\n  derivation\n  index\n  searchable\n  __typename\n}\n\nfragment StructureDescriptor on StructureDescriptor {\n  defaultCategoryKey\n  __typename\n}\n\nfragment EntityCategory on EntityCategory {\n  ...CategoryBase\n  instanceKind\n  positionX\n  positionY\n  width\n  height\n  propertyDefinitions {\n    ...PropertyDefinition\n    __typename\n  }\n  __typename\n}\n\nfragment GraphProjection on GraphProjection {\n  kind\n  status\n  projectedThroughSeq\n  derivedThroughSeq\n  lag\n  pending\n  schemaStale\n  schemaHash\n  derivedAt\n  rebuiltAt\n  __typename\n}\n\nfragment ListGraph on Graph {\n  id\n  name\n  description\n  ageName\n  isArchived\n  pinned\n  __typename\n}\n\nfragment MeasurementCategory on MeasurementCategory {\n  ...CategoryBase\n  sourceDescriptor {\n    ...StructureDescriptor\n    __typename\n  }\n  targetDescriptor {\n    ...EntityDescriptor\n    __typename\n  }\n  propertyDefinitions {\n    ...PropertyDefinition\n    __typename\n  }\n  __typename\n}\n\nfragment NaturalEventCategory on NaturalEventCategory {\n  ...CategoryBase\n  positionX\n  positionY\n  width\n  height\n  inputs {\n    ...EventRole\n    __typename\n  }\n  outputs {\n    ...EventRole\n    __typename\n  }\n  __typename\n}\n\nfragment ProtocolEventCategory on ProtocolEventCategory {\n  ...CategoryBase\n  positionX\n  positionY\n  width\n  height\n  inputs {\n    ...EventRole\n    __typename\n  }\n  outputs {\n    ...EventRole\n    __typename\n  }\n  __typename\n}\n\nfragment RelationCategory on RelationCategory {\n  ...CategoryBase\n  sourceDescriptor {\n    ...EntityDescriptor\n    __typename\n  }\n  targetDescriptor {\n    ...EntityDescriptor\n    __typename\n  }\n  propertyDefinitions {\n    ...PropertyDefinition\n    __typename\n  }\n  __typename\n}\n\nfragment StructureRelationCategory on StructureRelationCategory {\n  ...CategoryBase\n  sourceDescriptor {\n    ...StructureDescriptor\n    __typename\n  }\n  targetDescriptor {\n    ...StructureDescriptor\n    __typename\n  }\n  propertyDefinitions {\n    ...PropertyDefinition\n    __typename\n  }\n  __typename\n}\n\nfragment Graph on Graph {\n  ...ListGraph\n  purl\n  projection {\n    ...GraphProjection\n    __typename\n  }\n  entityCategories {\n    ...EntityCategory\n    __typename\n  }\n  relationCategories {\n    ...RelationCategory\n    __typename\n  }\n  measurementCategories {\n    ...MeasurementCategory\n    __typename\n  }\n  structureRelationCategories {\n    ...StructureRelationCategory\n    __typename\n  }\n  naturalEventCategories {\n    ...NaturalEventCategory\n    __typename\n  }\n  protocolEventCategories {\n    ...ProtocolEventCategory\n    __typename\n  }\n  __typename\n}\n\nmutation ArchiveGraph($input: ArchiveGraphInput!) {\n  archiveGraph(input: $input) {\n    ...Graph\n    __typename\n  }\n}"


class DeleteGraphMutation(BaseModel):
    """No documentation found for this operation."""

    delete_graph: ID = Field(alias="deleteGraph")
    "Delete a graph from the graph engine"

    class Arguments(BaseModel):
        """Arguments for DeleteGraph"""

        input: DeleteGraphInput

    class Meta:
        """Meta class for DeleteGraph"""

        document = "mutation DeleteGraph($input: DeleteGraphInput!) {\n  deleteGraph(input: $input)\n}"


class AttestEntityMutation(BaseModel):
    """Standing: somebody's position on whether a claim still holds.

    `attest` records stands=True, `retract` records stands=False, and both are evidence of the
    same kind. Neither deletes: the row, its metrics and its relations all survive a retraction,
    because a derived value that dropped a contributing measurement still has to be explainable.
    There is no reinstate and no state machine — only more evidence."""

    attest_entity: AssertedEntity = Field(alias="attestEntity")
    "Claim that an entity exists, returning it to every projection whose rules admit it"

    class Arguments(BaseModel):
        """Arguments for AttestEntity"""

        input: AttestEntityInput

    class Meta:
        """Meta class for AttestEntity"""

        document = "fragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment CategoryRef on Category {\n  id\n  key\n  label\n  ageName\n  __typename\n}\n\nfragment InstanceRef on Instance {\n  id\n  kind\n  term {\n    ...TermRef\n    __typename\n  }\n  __typename\n}\n\nfragment NodeRef on Node {\n  id\n  label\n  __typename\n}\n\nfragment Assertion on Assertion {\n  id\n  subject\n  appId\n  actionId\n  actionName\n  assertedAt\n  recordedAt\n  seq\n  __typename\n}\n\nfragment Instance on Instance {\n  ...InstanceRef\n  createdAt\n  component\n  assertion {\n    ...Assertion\n    __typename\n  }\n  __typename\n}\n\nfragment NodeDrawing on NodeDrawing {\n  graph {\n    id\n    name\n    __typename\n  }\n  category {\n    ...CategoryRef\n    __typename\n  }\n  node {\n    ...NodeRef\n    __typename\n  }\n  __typename\n}\n\nfragment AssertedEntity on AssertedEntity {\n  assertion {\n    ...Assertion\n    __typename\n  }\n  instance {\n    ...Instance\n    __typename\n  }\n  drawings {\n    ...NodeDrawing\n    __typename\n  }\n  __typename\n}\n\nmutation AttestEntity($input: AttestEntityInput!) {\n  attestEntity(input: $input) {\n    ...AssertedEntity\n    __typename\n  }\n}"


class RetractEntityMutation(BaseModel):
    """No documentation found for this operation."""

    retract_entity: AssertedEntity = Field(alias="retractEntity")
    "Claim that an entity no longer stands. It leaves every projection that counts the claim; the evidence stays."

    class Arguments(BaseModel):
        """Arguments for RetractEntity"""

        input: RetractEntityInput

    class Meta:
        """Meta class for RetractEntity"""

        document = "fragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment CategoryRef on Category {\n  id\n  key\n  label\n  ageName\n  __typename\n}\n\nfragment InstanceRef on Instance {\n  id\n  kind\n  term {\n    ...TermRef\n    __typename\n  }\n  __typename\n}\n\nfragment NodeRef on Node {\n  id\n  label\n  __typename\n}\n\nfragment Assertion on Assertion {\n  id\n  subject\n  appId\n  actionId\n  actionName\n  assertedAt\n  recordedAt\n  seq\n  __typename\n}\n\nfragment Instance on Instance {\n  ...InstanceRef\n  createdAt\n  component\n  assertion {\n    ...Assertion\n    __typename\n  }\n  __typename\n}\n\nfragment NodeDrawing on NodeDrawing {\n  graph {\n    id\n    name\n    __typename\n  }\n  category {\n    ...CategoryRef\n    __typename\n  }\n  node {\n    ...NodeRef\n    __typename\n  }\n  __typename\n}\n\nfragment AssertedEntity on AssertedEntity {\n  assertion {\n    ...Assertion\n    __typename\n  }\n  instance {\n    ...Instance\n    __typename\n  }\n  drawings {\n    ...NodeDrawing\n    __typename\n  }\n  __typename\n}\n\nmutation RetractEntity($input: RetractEntityInput!) {\n  retractEntity(input: $input) {\n    ...AssertedEntity\n    __typename\n  }\n}"


class AttestNaturalEventMutation(BaseModel):
    """No documentation found for this operation."""

    attest_natural_event: AssertedNaturalEvent = Field(alias="attestNaturalEvent")
    "Claim that a natural event exists"

    class Arguments(BaseModel):
        """Arguments for AttestNaturalEvent"""

        input: AttestNaturalEventInput

    class Meta:
        """Meta class for AttestNaturalEvent"""

        document = "fragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment CategoryRef on Category {\n  id\n  key\n  label\n  ageName\n  __typename\n}\n\nfragment InstanceRef on Instance {\n  id\n  kind\n  term {\n    ...TermRef\n    __typename\n  }\n  __typename\n}\n\nfragment NodeRef on Node {\n  id\n  label\n  __typename\n}\n\nfragment Assertion on Assertion {\n  id\n  subject\n  appId\n  actionId\n  actionName\n  assertedAt\n  recordedAt\n  seq\n  __typename\n}\n\nfragment Instance on Instance {\n  ...InstanceRef\n  createdAt\n  component\n  assertion {\n    ...Assertion\n    __typename\n  }\n  __typename\n}\n\nfragment NodeDrawing on NodeDrawing {\n  graph {\n    id\n    name\n    __typename\n  }\n  category {\n    ...CategoryRef\n    __typename\n  }\n  node {\n    ...NodeRef\n    __typename\n  }\n  __typename\n}\n\nfragment AssertedNaturalEvent on AssertedNaturalEvent {\n  assertion {\n    ...Assertion\n    __typename\n  }\n  instance {\n    ...Instance\n    __typename\n  }\n  drawings {\n    ...NodeDrawing\n    __typename\n  }\n  __typename\n}\n\nmutation AttestNaturalEvent($input: AttestNaturalEventInput!) {\n  attestNaturalEvent(input: $input) {\n    ...AssertedNaturalEvent\n    __typename\n  }\n}"


class RetractNaturalEventMutation(BaseModel):
    """No documentation found for this operation."""

    retract_natural_event: AssertedNaturalEvent = Field(alias="retractNaturalEvent")
    "Claim that a natural event no longer stands"

    class Arguments(BaseModel):
        """Arguments for RetractNaturalEvent"""

        input: RetractNaturalEventInput

    class Meta:
        """Meta class for RetractNaturalEvent"""

        document = "fragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment CategoryRef on Category {\n  id\n  key\n  label\n  ageName\n  __typename\n}\n\nfragment InstanceRef on Instance {\n  id\n  kind\n  term {\n    ...TermRef\n    __typename\n  }\n  __typename\n}\n\nfragment NodeRef on Node {\n  id\n  label\n  __typename\n}\n\nfragment Assertion on Assertion {\n  id\n  subject\n  appId\n  actionId\n  actionName\n  assertedAt\n  recordedAt\n  seq\n  __typename\n}\n\nfragment Instance on Instance {\n  ...InstanceRef\n  createdAt\n  component\n  assertion {\n    ...Assertion\n    __typename\n  }\n  __typename\n}\n\nfragment NodeDrawing on NodeDrawing {\n  graph {\n    id\n    name\n    __typename\n  }\n  category {\n    ...CategoryRef\n    __typename\n  }\n  node {\n    ...NodeRef\n    __typename\n  }\n  __typename\n}\n\nfragment AssertedNaturalEvent on AssertedNaturalEvent {\n  assertion {\n    ...Assertion\n    __typename\n  }\n  instance {\n    ...Instance\n    __typename\n  }\n  drawings {\n    ...NodeDrawing\n    __typename\n  }\n  __typename\n}\n\nmutation RetractNaturalEvent($input: RetractNaturalEventInput!) {\n  retractNaturalEvent(input: $input) {\n    ...AssertedNaturalEvent\n    __typename\n  }\n}"


class AttestProtocolEventMutation(BaseModel):
    """No documentation found for this operation."""

    attest_protocol_event: AssertedProtocolEvent = Field(alias="attestProtocolEvent")
    "Claim that a protocol event exists"

    class Arguments(BaseModel):
        """Arguments for AttestProtocolEvent"""

        input: AttestProtocolEventInput

    class Meta:
        """Meta class for AttestProtocolEvent"""

        document = "fragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment CategoryRef on Category {\n  id\n  key\n  label\n  ageName\n  __typename\n}\n\nfragment InstanceRef on Instance {\n  id\n  kind\n  term {\n    ...TermRef\n    __typename\n  }\n  __typename\n}\n\nfragment NodeRef on Node {\n  id\n  label\n  __typename\n}\n\nfragment Assertion on Assertion {\n  id\n  subject\n  appId\n  actionId\n  actionName\n  assertedAt\n  recordedAt\n  seq\n  __typename\n}\n\nfragment Instance on Instance {\n  ...InstanceRef\n  createdAt\n  component\n  assertion {\n    ...Assertion\n    __typename\n  }\n  __typename\n}\n\nfragment NodeDrawing on NodeDrawing {\n  graph {\n    id\n    name\n    __typename\n  }\n  category {\n    ...CategoryRef\n    __typename\n  }\n  node {\n    ...NodeRef\n    __typename\n  }\n  __typename\n}\n\nfragment AssertedProtocolEvent on AssertedProtocolEvent {\n  assertion {\n    ...Assertion\n    __typename\n  }\n  instance {\n    ...Instance\n    __typename\n  }\n  drawings {\n    ...NodeDrawing\n    __typename\n  }\n  __typename\n}\n\nmutation AttestProtocolEvent($input: AttestProtocolEventInput!) {\n  attestProtocolEvent(input: $input) {\n    ...AssertedProtocolEvent\n    __typename\n  }\n}"


class RetractProtocolEventMutation(BaseModel):
    """No documentation found for this operation."""

    retract_protocol_event: AssertedProtocolEvent = Field(alias="retractProtocolEvent")
    "Claim that a protocol event no longer stands"

    class Arguments(BaseModel):
        """Arguments for RetractProtocolEvent"""

        input: RetractProtocolEventInput

    class Meta:
        """Meta class for RetractProtocolEvent"""

        document = "fragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment CategoryRef on Category {\n  id\n  key\n  label\n  ageName\n  __typename\n}\n\nfragment InstanceRef on Instance {\n  id\n  kind\n  term {\n    ...TermRef\n    __typename\n  }\n  __typename\n}\n\nfragment NodeRef on Node {\n  id\n  label\n  __typename\n}\n\nfragment Assertion on Assertion {\n  id\n  subject\n  appId\n  actionId\n  actionName\n  assertedAt\n  recordedAt\n  seq\n  __typename\n}\n\nfragment Instance on Instance {\n  ...InstanceRef\n  createdAt\n  component\n  assertion {\n    ...Assertion\n    __typename\n  }\n  __typename\n}\n\nfragment NodeDrawing on NodeDrawing {\n  graph {\n    id\n    name\n    __typename\n  }\n  category {\n    ...CategoryRef\n    __typename\n  }\n  node {\n    ...NodeRef\n    __typename\n  }\n  __typename\n}\n\nfragment AssertedProtocolEvent on AssertedProtocolEvent {\n  assertion {\n    ...Assertion\n    __typename\n  }\n  instance {\n    ...Instance\n    __typename\n  }\n  drawings {\n    ...NodeDrawing\n    __typename\n  }\n  __typename\n}\n\nmutation RetractProtocolEvent($input: RetractProtocolEventInput!) {\n  retractProtocolEvent(input: $input) {\n    ...AssertedProtocolEvent\n    __typename\n  }\n}"


class AttestStructureMutation(BaseModel):
    """No documentation found for this operation."""

    attest_structure: AssertedStructure = Field(alias="attestStructure")
    "Claim that a structure still stands, after somebody retracted it. New evidence, not an undo — both positions stay on the record"

    class Arguments(BaseModel):
        """Arguments for AttestStructure"""

        input: AttestStructureInput

    class Meta:
        """Meta class for AttestStructure"""

        document = "fragment Metric on Metric {\n  id\n  kindId\n  key\n  value\n  unit\n  confidence\n  confidenceType\n  observedAt\n  assertedAt\n  __typename\n}\n\nfragment Structure on Structure {\n  id\n  identifier\n  object\n  kindId\n  __typename\n}\n\nfragment Assertion on Assertion {\n  id\n  subject\n  appId\n  actionId\n  actionName\n  assertedAt\n  recordedAt\n  seq\n  __typename\n}\n\nfragment StructureWithMetrics on Structure {\n  ...Structure\n  metrics {\n    ...Metric\n    __typename\n  }\n  __typename\n}\n\nfragment AssertedStructure on AssertedStructure {\n  assertion {\n    ...Assertion\n    __typename\n  }\n  structure {\n    ...StructureWithMetrics\n    __typename\n  }\n  __typename\n}\n\nmutation AttestStructure($input: AttestStructureInput!) {\n  attestStructure(input: $input) {\n    ...AssertedStructure\n    __typename\n  }\n}"


class RetractStructureMutation(BaseModel):
    """No documentation found for this operation."""

    retract_structure: AssertedStructure = Field(alias="retractStructure")
    "Retract a datum: a Standing(stands=false) against it. Its metrics and INFORMS claims stay on the record, but stop counting for every node it informs until somebody attests it again (RFC 0023)"

    class Arguments(BaseModel):
        """Arguments for RetractStructure"""

        input: RetractStructureInput

    class Meta:
        """Meta class for RetractStructure"""

        document = "fragment Metric on Metric {\n  id\n  kindId\n  key\n  value\n  unit\n  confidence\n  confidenceType\n  observedAt\n  assertedAt\n  __typename\n}\n\nfragment Structure on Structure {\n  id\n  identifier\n  object\n  kindId\n  __typename\n}\n\nfragment Assertion on Assertion {\n  id\n  subject\n  appId\n  actionId\n  actionName\n  assertedAt\n  recordedAt\n  seq\n  __typename\n}\n\nfragment StructureWithMetrics on Structure {\n  ...Structure\n  metrics {\n    ...Metric\n    __typename\n  }\n  __typename\n}\n\nfragment AssertedStructure on AssertedStructure {\n  assertion {\n    ...Assertion\n    __typename\n  }\n  structure {\n    ...StructureWithMetrics\n    __typename\n  }\n  __typename\n}\n\nmutation RetractStructure($input: RetractStructureInput!) {\n  retractStructure(input: $input) {\n    ...AssertedStructure\n    __typename\n  }\n}"


class AttestMetricMutation(BaseModel):
    """No documentation found for this operation."""

    attest_metric: AssertedMetric = Field(alias="attestMetric")
    "Claim that a measurement still stands. The derived values that dropped it are refolded"

    class Arguments(BaseModel):
        """Arguments for AttestMetric"""

        input: AttestMetricInput

    class Meta:
        """Meta class for AttestMetric"""

        document = "fragment Assertion on Assertion {\n  id\n  subject\n  appId\n  actionId\n  actionName\n  assertedAt\n  recordedAt\n  seq\n  __typename\n}\n\nfragment Metric on Metric {\n  id\n  kindId\n  key\n  value\n  unit\n  confidence\n  confidenceType\n  observedAt\n  assertedAt\n  __typename\n}\n\nfragment AssertedMetric on AssertedMetric {\n  assertion {\n    ...Assertion\n    __typename\n  }\n  metric {\n    ...Metric\n    __typename\n  }\n  __typename\n}\n\nmutation AttestMetric($input: AttestMetricInput!) {\n  attestMetric(input: $input) {\n    ...AssertedMetric\n    __typename\n  }\n}"


class RetractMetricMutation(BaseModel):
    """No documentation found for this operation."""

    retract_metric: AssertedMetric = Field(alias="retractMetric")
    "Retract a measurement without destroying it. It stays readable, because a derived value that dropped it still has to be explainable"

    class Arguments(BaseModel):
        """Arguments for RetractMetric"""

        input: RetractMetricInput

    class Meta:
        """Meta class for RetractMetric"""

        document = "fragment Assertion on Assertion {\n  id\n  subject\n  appId\n  actionId\n  actionName\n  assertedAt\n  recordedAt\n  seq\n  __typename\n}\n\nfragment Metric on Metric {\n  id\n  kindId\n  key\n  value\n  unit\n  confidence\n  confidenceType\n  observedAt\n  assertedAt\n  __typename\n}\n\nfragment AssertedMetric on AssertedMetric {\n  assertion {\n    ...Assertion\n    __typename\n  }\n  metric {\n    ...Metric\n    __typename\n  }\n  __typename\n}\n\nmutation RetractMetric($input: RetractMetricInput!) {\n  retractMetric(input: $input) {\n    ...AssertedMetric\n    __typename\n  }\n}"


class AttestCommentMutation(BaseModel):
    """No documentation found for this operation."""

    attest_comment: AssertedComment = Field(alias="attestComment")
    "Claim a remark stands again — reopening, as new evidence rather than an undo"

    class Arguments(BaseModel):
        """Arguments for AttestComment"""

        input: AttestCommentInput

    class Meta:
        """Meta class for AttestComment"""

        document = "fragment Assertion on Assertion {\n  id\n  subject\n  appId\n  actionId\n  actionName\n  assertedAt\n  recordedAt\n  seq\n  __typename\n}\n\nfragment Comment on Comment {\n  id\n  createdAt\n  text\n  resolved\n  mentions\n  parent {\n    id\n    __typename\n  }\n  assertion {\n    ...Assertion\n    __typename\n  }\n  __typename\n}\n\nfragment AssertedComment on AssertedComment {\n  assertion {\n    ...Assertion\n    __typename\n  }\n  comment {\n    ...Comment\n    __typename\n  }\n  __typename\n}\n\nmutation AttestComment($input: AttestCommentInput!) {\n  attestComment(input: $input) {\n    ...AssertedComment\n    __typename\n  }\n}"


class RetractCommentMutation(BaseModel):
    """No documentation found for this operation."""

    retract_comment: AssertedComment = Field(alias="retractComment")
    "Claim a remark no longer stands — resolved by a reviewer or withdrawn by its author; the assertion records whose position it is. The row survives"

    class Arguments(BaseModel):
        """Arguments for RetractComment"""

        input: RetractCommentInput

    class Meta:
        """Meta class for RetractComment"""

        document = "fragment Assertion on Assertion {\n  id\n  subject\n  appId\n  actionId\n  actionName\n  assertedAt\n  recordedAt\n  seq\n  __typename\n}\n\nfragment Comment on Comment {\n  id\n  createdAt\n  text\n  resolved\n  mentions\n  parent {\n    id\n    __typename\n  }\n  assertion {\n    ...Assertion\n    __typename\n  }\n  __typename\n}\n\nfragment AssertedComment on AssertedComment {\n  assertion {\n    ...Assertion\n    __typename\n  }\n  comment {\n    ...Comment\n    __typename\n  }\n  __typename\n}\n\nmutation RetractComment($input: RetractCommentInput!) {\n  retractComment(input: $input) {\n    ...AssertedComment\n    __typename\n  }\n}"


class RetractRelationMutation(BaseModel):
    """No documentation found for this operation."""

    retract_relation: AssertedRelation = Field(alias="retractRelation")
    "Retract a relation assertion without destroying it. The edge survives wherever another live assertion still states the same proposition"

    class Arguments(BaseModel):
        """Arguments for RetractRelation"""

        input: RetractRelationInput

    class Meta:
        """Meta class for RetractRelation"""

        document = "fragment CategoryRef on Category {\n  id\n  key\n  label\n  ageName\n  __typename\n}\n\nfragment LinkRef on Link {\n  id\n  kind\n  sourceRef\n  targetRef\n  __typename\n}\n\nfragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment Assertion on Assertion {\n  id\n  subject\n  appId\n  actionId\n  actionName\n  assertedAt\n  recordedAt\n  seq\n  __typename\n}\n\nfragment EdgeDrawing on EdgeDrawing {\n  graph {\n    id\n    name\n    __typename\n  }\n  category {\n    ...CategoryRef\n    __typename\n  }\n  __typename\n}\n\nfragment Link on Link {\n  ...LinkRef\n  role\n  createdAt\n  term {\n    ...TermRef\n    __typename\n  }\n  assertion {\n    ...Assertion\n    __typename\n  }\n  __typename\n}\n\nfragment AssertedRelation on AssertedRelation {\n  assertion {\n    ...Assertion\n    __typename\n  }\n  link {\n    ...Link\n    __typename\n  }\n  drawings {\n    ...EdgeDrawing\n    __typename\n  }\n  __typename\n}\n\nmutation RetractRelation($input: RetractRelationInput!) {\n  retractRelation(input: $input) {\n    ...AssertedRelation\n    __typename\n  }\n}"


class RetractMeasurementMutation(BaseModel):
    """No documentation found for this operation."""

    retract_measurement: AssertedMeasurement = Field(alias="retractMeasurement")
    "Retract a measurement assertion without destroying it"

    class Arguments(BaseModel):
        """Arguments for RetractMeasurement"""

        input: RetractMeasurementInput

    class Meta:
        """Meta class for RetractMeasurement"""

        document = "fragment LinkRef on Link {\n  id\n  kind\n  sourceRef\n  targetRef\n  __typename\n}\n\nfragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment Assertion on Assertion {\n  id\n  subject\n  appId\n  actionId\n  actionName\n  assertedAt\n  recordedAt\n  seq\n  __typename\n}\n\nfragment Link on Link {\n  ...LinkRef\n  role\n  createdAt\n  term {\n    ...TermRef\n    __typename\n  }\n  assertion {\n    ...Assertion\n    __typename\n  }\n  __typename\n}\n\nfragment AssertedMeasurement on AssertedMeasurement {\n  assertion {\n    ...Assertion\n    __typename\n  }\n  link {\n    ...Link\n    __typename\n  }\n  __typename\n}\n\nmutation RetractMeasurement($input: RetractMeasurementInput!) {\n  retractMeasurement(input: $input) {\n    ...AssertedMeasurement\n    __typename\n  }\n}"


class RetractStructureRelationMutation(BaseModel):
    """No documentation found for this operation."""

    retract_structure_relation: AssertedStructureRelation = Field(
        alias="retractStructureRelation"
    )
    "Retract a structure relation assertion without destroying it"

    class Arguments(BaseModel):
        """Arguments for RetractStructureRelation"""

        input: RetractStructureRelationInput

    class Meta:
        """Meta class for RetractStructureRelation"""

        document = "fragment LinkRef on Link {\n  id\n  kind\n  sourceRef\n  targetRef\n  __typename\n}\n\nfragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment Assertion on Assertion {\n  id\n  subject\n  appId\n  actionId\n  actionName\n  assertedAt\n  recordedAt\n  seq\n  __typename\n}\n\nfragment Link on Link {\n  ...LinkRef\n  role\n  createdAt\n  term {\n    ...TermRef\n    __typename\n  }\n  assertion {\n    ...Assertion\n    __typename\n  }\n  __typename\n}\n\nfragment AssertedStructureRelation on AssertedStructureRelation {\n  assertion {\n    ...Assertion\n    __typename\n  }\n  link {\n    ...Link\n    __typename\n  }\n  __typename\n}\n\nmutation RetractStructureRelation($input: RetractStructureRelationInput!) {\n  retractStructureRelation(input: $input) {\n    ...AssertedStructureRelation\n    __typename\n  }\n}"


class RetractParticipationMutation(BaseModel):
    """No documentation found for this operation."""

    retract_participation: AssertedParticipation = Field(alias="retractParticipation")
    "Retract one claim that an entity took part in an event. The edge survives while another claim still states it"

    class Arguments(BaseModel):
        """Arguments for RetractParticipation"""

        input: RetractParticipationInput

    class Meta:
        """Meta class for RetractParticipation"""

        document = "fragment CategoryRef on Category {\n  id\n  key\n  label\n  ageName\n  __typename\n}\n\nfragment LinkRef on Link {\n  id\n  kind\n  sourceRef\n  targetRef\n  __typename\n}\n\nfragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment Assertion on Assertion {\n  id\n  subject\n  appId\n  actionId\n  actionName\n  assertedAt\n  recordedAt\n  seq\n  __typename\n}\n\nfragment EdgeDrawing on EdgeDrawing {\n  graph {\n    id\n    name\n    __typename\n  }\n  category {\n    ...CategoryRef\n    __typename\n  }\n  __typename\n}\n\nfragment Link on Link {\n  ...LinkRef\n  role\n  createdAt\n  term {\n    ...TermRef\n    __typename\n  }\n  assertion {\n    ...Assertion\n    __typename\n  }\n  __typename\n}\n\nfragment AssertedParticipation on AssertedParticipation {\n  assertion {\n    ...Assertion\n    __typename\n  }\n  link {\n    ...Link\n    __typename\n  }\n  drawings {\n    ...EdgeDrawing\n    __typename\n  }\n  __typename\n}\n\nmutation RetractParticipation($input: RetractParticipationInput!) {\n  retractParticipation(input: $input) {\n    ...AssertedParticipation\n    __typename\n  }\n}"


class RetractSameInstanceMutation(BaseModel):
    """No documentation found for this operation."""

    retract_same_instance: AssertedSameness = Field(alias="retractSameInstance")
    "Withdraw one sameness claim. The component it held together is rebuilt from the claims that survive, which may split it"

    class Arguments(BaseModel):
        """Arguments for RetractSameInstance"""

        input: RetractSameInstanceInput

    class Meta:
        """Meta class for RetractSameInstance"""

        document = "fragment LinkRef on Link {\n  id\n  kind\n  sourceRef\n  targetRef\n  __typename\n}\n\nfragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment Assertion on Assertion {\n  id\n  subject\n  appId\n  actionId\n  actionName\n  assertedAt\n  recordedAt\n  seq\n  __typename\n}\n\nfragment Link on Link {\n  ...LinkRef\n  role\n  createdAt\n  term {\n    ...TermRef\n    __typename\n  }\n  assertion {\n    ...Assertion\n    __typename\n  }\n  __typename\n}\n\nfragment AssertedSameness on AssertedSameness {\n  assertion {\n    ...Assertion\n    __typename\n  }\n  links {\n    ...Link\n    __typename\n  }\n  __typename\n}\n\nmutation RetractSameInstance($input: RetractSameInstanceInput!) {\n  retractSameInstance(input: $input) {\n    ...AssertedSameness\n    __typename\n  }\n}"


class AttestLinkMutation(BaseModel):
    """No documentation found for this operation."""

    attest_link: AssertedLinks = Field(alias="attestLink")
    "Claim that a link claim still stands — a relation, a classification, a participation, a measurement. One act for every kind, as `retractLinks` is"

    class Arguments(BaseModel):
        """Arguments for AttestLink"""

        input: AttestLinkInput

    class Meta:
        """Meta class for AttestLink"""

        document = "fragment CategoryRef on Category {\n  id\n  key\n  label\n  ageName\n  __typename\n}\n\nfragment LinkRef on Link {\n  id\n  kind\n  sourceRef\n  targetRef\n  __typename\n}\n\nfragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment Assertion on Assertion {\n  id\n  subject\n  appId\n  actionId\n  actionName\n  assertedAt\n  recordedAt\n  seq\n  __typename\n}\n\nfragment EdgeDrawing on EdgeDrawing {\n  graph {\n    id\n    name\n    __typename\n  }\n  category {\n    ...CategoryRef\n    __typename\n  }\n  __typename\n}\n\nfragment Link on Link {\n  ...LinkRef\n  role\n  createdAt\n  term {\n    ...TermRef\n    __typename\n  }\n  assertion {\n    ...Assertion\n    __typename\n  }\n  __typename\n}\n\nfragment AssertedLinks on AssertedLinks {\n  assertion {\n    ...Assertion\n    __typename\n  }\n  links {\n    ...Link\n    __typename\n  }\n  drawings {\n    ...EdgeDrawing\n    __typename\n  }\n  __typename\n}\n\nmutation AttestLink($input: AttestLinkInput!) {\n  attestLink(input: $input) {\n    ...AssertedLinks\n    __typename\n  }\n}"


class RetractLinksMutation(BaseModel):
    """One assertion over many link ids, of any link kind."""

    retract_links: AssertedLinks = Field(alias="retractLinks")
    "Retract several link claims as one act, by their `Link` ids — a relation, a classification, a participation, a measurement"

    class Arguments(BaseModel):
        """Arguments for RetractLinks"""

        input: RetractLinksInput

    class Meta:
        """Meta class for RetractLinks"""

        document = "fragment CategoryRef on Category {\n  id\n  key\n  label\n  ageName\n  __typename\n}\n\nfragment LinkRef on Link {\n  id\n  kind\n  sourceRef\n  targetRef\n  __typename\n}\n\nfragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment Assertion on Assertion {\n  id\n  subject\n  appId\n  actionId\n  actionName\n  assertedAt\n  recordedAt\n  seq\n  __typename\n}\n\nfragment EdgeDrawing on EdgeDrawing {\n  graph {\n    id\n    name\n    __typename\n  }\n  category {\n    ...CategoryRef\n    __typename\n  }\n  __typename\n}\n\nfragment Link on Link {\n  ...LinkRef\n  role\n  createdAt\n  term {\n    ...TermRef\n    __typename\n  }\n  assertion {\n    ...Assertion\n    __typename\n  }\n  __typename\n}\n\nfragment AssertedLinks on AssertedLinks {\n  assertion {\n    ...Assertion\n    __typename\n  }\n  links {\n    ...Link\n    __typename\n  }\n  drawings {\n    ...EdgeDrawing\n    __typename\n  }\n  __typename\n}\n\nmutation RetractLinks($input: RetractLinksInput!) {\n  retractLinks(input: $input) {\n    ...AssertedLinks\n    __typename\n  }\n}"


class CreateTermMutation(BaseModel):
    """The organization's words. Terms are minted lazily by the first claim that names one, so
    createTerm is only for declaring a word ahead of use (or giving it a label and colour).
    """

    create_term: Term = Field(alias="createTerm")
    "Declare one of the organization's words, or describe one an ingest minted bare"

    class Arguments(BaseModel):
        """Arguments for CreateTerm"""

        input: CreateTermInput

    class Meta:
        """Meta class for CreateTerm"""

        document = "fragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment Term on Term {\n  ...TermRef\n  label\n  description\n  purl\n  color\n  createdAt\n  __typename\n}\n\nmutation CreateTerm($input: CreateTermInput!) {\n  createTerm(input: $input) {\n    ...Term\n    __typename\n  }\n}"


class UpdateTermMutation(BaseModel):
    """No documentation found for this operation."""

    update_term: Term = Field(alias="updateTerm")
    "Update a term's label, description, PURL or colour. Its kind and key are its identity and cannot change."

    class Arguments(BaseModel):
        """Arguments for UpdateTerm"""

        input: UpdateTermInput

    class Meta:
        """Meta class for UpdateTerm"""

        document = "fragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment Term on Term {\n  ...TermRef\n  label\n  description\n  purl\n  color\n  createdAt\n  __typename\n}\n\nmutation UpdateTerm($input: UpdateTermInput!) {\n  updateTerm(input: $input) {\n    ...Term\n    __typename\n  }\n}"


class DeleteTermMutation(BaseModel):
    """No documentation found for this operation."""

    delete_term: ID = Field(alias="deleteTerm")
    "Retire a word nothing has been claimed under"

    class Arguments(BaseModel):
        """Arguments for DeleteTerm"""

        input: DeleteTermInput

    class Meta:
        """Meta class for DeleteTerm"""

        document = "mutation DeleteTerm($input: DeleteTermInput!) {\n  deleteTerm(input: $input)\n}"


class UpdateStructureKindMutation(BaseModel):
    """StructureKind and MetricKind are minted by the write that first needs them — there is no
    create mutation for either, only these."""

    update_structure_kind: StructureKind = Field(alias="updateStructureKind")
    "Update a structure kind's label, description or colour"

    class Arguments(BaseModel):
        """Arguments for UpdateStructureKind"""

        input: UpdateStructureKindInput

    class Meta:
        """Meta class for UpdateStructureKind"""

        document = "fragment StructureKind on StructureKind {\n  id\n  identifier\n  label\n  description\n  purl\n  color\n  createdAt\n  __typename\n}\n\nmutation UpdateStructureKind($input: UpdateStructureKindInput!) {\n  updateStructureKind(input: $input) {\n    ...StructureKind\n    __typename\n  }\n}"


class DeleteStructureKindMutation(BaseModel):
    """No documentation found for this operation."""

    delete_structure_kind: ID = Field(alias="deleteStructureKind")
    "Retire a structure kind. Refused while any structure is recorded under it — evidence is never deleted; retract the structures first"

    class Arguments(BaseModel):
        """Arguments for DeleteStructureKind"""

        input: DeleteStructureKindInput

    class Meta:
        """Meta class for DeleteStructureKind"""

        document = "mutation DeleteStructureKind($input: DeleteStructureKindInput!) {\n  deleteStructureKind(input: $input)\n}"


class UpdateMetricKindMutation(BaseModel):
    """No documentation found for this operation."""

    update_metric_kind: MetricKind = Field(alias="updateMetricKind")
    "Update a metric kind's label, description or colour"

    class Arguments(BaseModel):
        """Arguments for UpdateMetricKind"""

        input: UpdateMetricKindInput

    class Meta:
        """Meta class for UpdateMetricKind"""

        document = "fragment MetricKind on MetricKind {\n  id\n  key\n  valueKind\n  label\n  description\n  purl\n  color\n  createdAt\n  structureKind {\n    id\n    identifier\n    __typename\n  }\n  __typename\n}\n\nmutation UpdateMetricKind($input: UpdateMetricKindInput!) {\n  updateMetricKind(input: $input) {\n    ...MetricKind\n    __typename\n  }\n}"


class DeleteMetricKindMutation(BaseModel):
    """No documentation found for this operation."""

    delete_metric_kind: ID = Field(alias="deleteMetricKind")
    "Retire a metric kind. Refused while any metric is recorded under it — evidence is never deleted; retract the metrics first"

    class Arguments(BaseModel):
        """Arguments for DeleteMetricKind"""

        input: DeleteMetricKindInput

    class Meta:
        """Meta class for DeleteMetricKind"""

        document = "mutation DeleteMetricKind($input: DeleteMetricKindInput!) {\n  deleteMetricKind(input: $input)\n}"


class GetEntityCategoryQuery(BaseModel):
    """No documentation found for this operation."""

    entity_category: EntityCategory = Field(alias="entityCategory")
    "Get a single entity category by ID"

    class Arguments(BaseModel):
        """Arguments for GetEntityCategory"""

        id: ID

    class Meta:
        """Meta class for GetEntityCategory"""

        document = "fragment CategoryRef on Category {\n  id\n  key\n  label\n  ageName\n  __typename\n}\n\nfragment MediaStore on MediaStore {\n  id\n  key\n  presignedUrl\n  __typename\n}\n\nfragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment CategoryBase on Category {\n  ...CategoryRef\n  description\n  purl\n  color\n  pinned\n  image {\n    ...MediaStore\n    __typename\n  }\n  graph {\n    id\n    name\n    __typename\n  }\n  term {\n    ...TermRef\n    __typename\n  }\n  __typename\n}\n\nfragment PropertyDefinition on PropertyDefinition {\n  key\n  label\n  valueKind\n  unit\n  description\n  derivation\n  index\n  searchable\n  __typename\n}\n\nfragment EntityCategory on EntityCategory {\n  ...CategoryBase\n  instanceKind\n  positionX\n  positionY\n  width\n  height\n  propertyDefinitions {\n    ...PropertyDefinition\n    __typename\n  }\n  __typename\n}\n\nquery GetEntityCategory($id: ID!) {\n  entityCategory(id: $id) {\n    ...EntityCategory\n    __typename\n  }\n}"


class ListEntityCategoriesQuery(BaseModel):
    """No documentation found for this operation."""

    entity_categories: tuple[EntityCategory, ...] = Field(alias="entityCategories")
    "List all entity categories"

    class Arguments(BaseModel):
        """Arguments for ListEntityCategories"""

        filters: EntityCategoryFilter | None = Field(default=None)
        pagination: OffsetPaginationInput | None = Field(default=None)

    class Meta:
        """Meta class for ListEntityCategories"""

        document = "fragment CategoryRef on Category {\n  id\n  key\n  label\n  ageName\n  __typename\n}\n\nfragment MediaStore on MediaStore {\n  id\n  key\n  presignedUrl\n  __typename\n}\n\nfragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment CategoryBase on Category {\n  ...CategoryRef\n  description\n  purl\n  color\n  pinned\n  image {\n    ...MediaStore\n    __typename\n  }\n  graph {\n    id\n    name\n    __typename\n  }\n  term {\n    ...TermRef\n    __typename\n  }\n  __typename\n}\n\nfragment PropertyDefinition on PropertyDefinition {\n  key\n  label\n  valueKind\n  unit\n  description\n  derivation\n  index\n  searchable\n  __typename\n}\n\nfragment EntityCategory on EntityCategory {\n  ...CategoryBase\n  instanceKind\n  positionX\n  positionY\n  width\n  height\n  propertyDefinitions {\n    ...PropertyDefinition\n    __typename\n  }\n  __typename\n}\n\nquery ListEntityCategories($filters: EntityCategoryFilter, $pagination: OffsetPaginationInput) {\n  entityCategories(filters: $filters, pagination: $pagination) {\n    ...EntityCategory\n    __typename\n  }\n}"


class SearchEntityCategoriesQueryOptions(EntityCategoryTrait, BaseModel):
    """An entity category definition"""

    typename: Literal["EntityCategory"] = Field(
        alias="__typename", default="EntityCategory", exclude=True
    )
    value: ID
    "Database ID of the category"
    label: str
    "Label/name of the category"
    model_config = ConfigDict(frozen=True)


class SearchEntityCategoriesQuery(BaseModel):
    """No documentation found for this operation."""

    options: tuple[SearchEntityCategoriesQueryOptions, ...]
    "List all entity categories"

    class Arguments(BaseModel):
        """Arguments for SearchEntityCategories"""

        search: str | None = Field(default=None)
        values: list[ID] | None = Field(default=None)

    class Meta:
        """Meta class for SearchEntityCategories"""

        document = "query SearchEntityCategories($search: String, $values: [ID!]) {\n  options: entityCategories(\n    filters: {search: $search, ids: $values}\n    pagination: {limit: 10}\n  ) {\n    value: id\n    label: label\n    __typename\n  }\n}"


class GetRelationCategoryQuery(BaseModel):
    """No documentation found for this operation."""

    relation_category: RelationCategory = Field(alias="relationCategory")
    "Get a single relation category by ID"

    class Arguments(BaseModel):
        """Arguments for GetRelationCategory"""

        id: ID

    class Meta:
        """Meta class for GetRelationCategory"""

        document = "fragment CategoryRef on Category {\n  id\n  key\n  label\n  ageName\n  __typename\n}\n\nfragment MediaStore on MediaStore {\n  id\n  key\n  presignedUrl\n  __typename\n}\n\nfragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment CategoryBase on Category {\n  ...CategoryRef\n  description\n  purl\n  color\n  pinned\n  image {\n    ...MediaStore\n    __typename\n  }\n  graph {\n    id\n    name\n    __typename\n  }\n  term {\n    ...TermRef\n    __typename\n  }\n  __typename\n}\n\nfragment EntityDescriptor on EntityDescriptor {\n  keys\n  ontologyTerms\n  defaultCategoryKey\n  __typename\n}\n\nfragment PropertyDefinition on PropertyDefinition {\n  key\n  label\n  valueKind\n  unit\n  description\n  derivation\n  index\n  searchable\n  __typename\n}\n\nfragment RelationCategory on RelationCategory {\n  ...CategoryBase\n  sourceDescriptor {\n    ...EntityDescriptor\n    __typename\n  }\n  targetDescriptor {\n    ...EntityDescriptor\n    __typename\n  }\n  propertyDefinitions {\n    ...PropertyDefinition\n    __typename\n  }\n  __typename\n}\n\nquery GetRelationCategory($id: ID!) {\n  relationCategory(id: $id) {\n    ...RelationCategory\n    __typename\n  }\n}"


class ListRelationCategoriesQuery(BaseModel):
    """No documentation found for this operation."""

    relation_categories: tuple[RelationCategory, ...] = Field(
        alias="relationCategories"
    )
    "List all relation categories"

    class Arguments(BaseModel):
        """Arguments for ListRelationCategories"""

        filters: RelationCategoryFilter | None = Field(default=None)
        pagination: OffsetPaginationInput | None = Field(default=None)

    class Meta:
        """Meta class for ListRelationCategories"""

        document = "fragment CategoryRef on Category {\n  id\n  key\n  label\n  ageName\n  __typename\n}\n\nfragment MediaStore on MediaStore {\n  id\n  key\n  presignedUrl\n  __typename\n}\n\nfragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment CategoryBase on Category {\n  ...CategoryRef\n  description\n  purl\n  color\n  pinned\n  image {\n    ...MediaStore\n    __typename\n  }\n  graph {\n    id\n    name\n    __typename\n  }\n  term {\n    ...TermRef\n    __typename\n  }\n  __typename\n}\n\nfragment EntityDescriptor on EntityDescriptor {\n  keys\n  ontologyTerms\n  defaultCategoryKey\n  __typename\n}\n\nfragment PropertyDefinition on PropertyDefinition {\n  key\n  label\n  valueKind\n  unit\n  description\n  derivation\n  index\n  searchable\n  __typename\n}\n\nfragment RelationCategory on RelationCategory {\n  ...CategoryBase\n  sourceDescriptor {\n    ...EntityDescriptor\n    __typename\n  }\n  targetDescriptor {\n    ...EntityDescriptor\n    __typename\n  }\n  propertyDefinitions {\n    ...PropertyDefinition\n    __typename\n  }\n  __typename\n}\n\nquery ListRelationCategories($filters: RelationCategoryFilter, $pagination: OffsetPaginationInput) {\n  relationCategories(filters: $filters, pagination: $pagination) {\n    ...RelationCategory\n    __typename\n  }\n}"


class SearchRelationCategoriesQueryOptions(RelationCategoryTrait, BaseModel):
    """A relation category definition"""

    typename: Literal["RelationCategory"] = Field(
        alias="__typename", default="RelationCategory", exclude=True
    )
    value: ID
    "Database ID of the category"
    label: str
    "Label/name of the category"
    model_config = ConfigDict(frozen=True)


class SearchRelationCategoriesQuery(BaseModel):
    """No documentation found for this operation."""

    options: tuple[SearchRelationCategoriesQueryOptions, ...]
    "List all relation categories"

    class Arguments(BaseModel):
        """Arguments for SearchRelationCategories"""

        search: str | None = Field(default=None)
        values: list[ID] | None = Field(default=None)

    class Meta:
        """Meta class for SearchRelationCategories"""

        document = "query SearchRelationCategories($search: String, $values: [ID!]) {\n  options: relationCategories(\n    filters: {search: $search, ids: $values}\n    pagination: {limit: 10}\n  ) {\n    value: id\n    label: label\n    __typename\n  }\n}"


class GetMeasurementCategoryQuery(BaseModel):
    """No documentation found for this operation."""

    measurement_category: MeasurementCategory = Field(alias="measurementCategory")
    "Get a single measurement category by ID"

    class Arguments(BaseModel):
        """Arguments for GetMeasurementCategory"""

        id: ID

    class Meta:
        """Meta class for GetMeasurementCategory"""

        document = "fragment CategoryRef on Category {\n  id\n  key\n  label\n  ageName\n  __typename\n}\n\nfragment MediaStore on MediaStore {\n  id\n  key\n  presignedUrl\n  __typename\n}\n\nfragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment CategoryBase on Category {\n  ...CategoryRef\n  description\n  purl\n  color\n  pinned\n  image {\n    ...MediaStore\n    __typename\n  }\n  graph {\n    id\n    name\n    __typename\n  }\n  term {\n    ...TermRef\n    __typename\n  }\n  __typename\n}\n\nfragment EntityDescriptor on EntityDescriptor {\n  keys\n  ontologyTerms\n  defaultCategoryKey\n  __typename\n}\n\nfragment PropertyDefinition on PropertyDefinition {\n  key\n  label\n  valueKind\n  unit\n  description\n  derivation\n  index\n  searchable\n  __typename\n}\n\nfragment StructureDescriptor on StructureDescriptor {\n  defaultCategoryKey\n  __typename\n}\n\nfragment MeasurementCategory on MeasurementCategory {\n  ...CategoryBase\n  sourceDescriptor {\n    ...StructureDescriptor\n    __typename\n  }\n  targetDescriptor {\n    ...EntityDescriptor\n    __typename\n  }\n  propertyDefinitions {\n    ...PropertyDefinition\n    __typename\n  }\n  __typename\n}\n\nquery GetMeasurementCategory($id: ID!) {\n  measurementCategory(id: $id) {\n    ...MeasurementCategory\n    __typename\n  }\n}"


class ListMeasurementCategoriesQuery(BaseModel):
    """No documentation found for this operation."""

    measurement_categories: tuple[MeasurementCategory, ...] = Field(
        alias="measurementCategories"
    )
    "List all measurement categories"

    class Arguments(BaseModel):
        """Arguments for ListMeasurementCategories"""

        filters: MeasurementCategoryFilter | None = Field(default=None)
        pagination: OffsetPaginationInput | None = Field(default=None)

    class Meta:
        """Meta class for ListMeasurementCategories"""

        document = "fragment CategoryRef on Category {\n  id\n  key\n  label\n  ageName\n  __typename\n}\n\nfragment MediaStore on MediaStore {\n  id\n  key\n  presignedUrl\n  __typename\n}\n\nfragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment CategoryBase on Category {\n  ...CategoryRef\n  description\n  purl\n  color\n  pinned\n  image {\n    ...MediaStore\n    __typename\n  }\n  graph {\n    id\n    name\n    __typename\n  }\n  term {\n    ...TermRef\n    __typename\n  }\n  __typename\n}\n\nfragment EntityDescriptor on EntityDescriptor {\n  keys\n  ontologyTerms\n  defaultCategoryKey\n  __typename\n}\n\nfragment PropertyDefinition on PropertyDefinition {\n  key\n  label\n  valueKind\n  unit\n  description\n  derivation\n  index\n  searchable\n  __typename\n}\n\nfragment StructureDescriptor on StructureDescriptor {\n  defaultCategoryKey\n  __typename\n}\n\nfragment MeasurementCategory on MeasurementCategory {\n  ...CategoryBase\n  sourceDescriptor {\n    ...StructureDescriptor\n    __typename\n  }\n  targetDescriptor {\n    ...EntityDescriptor\n    __typename\n  }\n  propertyDefinitions {\n    ...PropertyDefinition\n    __typename\n  }\n  __typename\n}\n\nquery ListMeasurementCategories($filters: MeasurementCategoryFilter, $pagination: OffsetPaginationInput) {\n  measurementCategories(filters: $filters, pagination: $pagination) {\n    ...MeasurementCategory\n    __typename\n  }\n}"


class SearchMeasurementCategoriesQueryOptions(MeasurementCategoryTrait, BaseModel):
    """A measurement category definition"""

    typename: Literal["MeasurementCategory"] = Field(
        alias="__typename", default="MeasurementCategory", exclude=True
    )
    value: ID
    "Database ID of the category"
    label: str
    "Label/name of the category"
    model_config = ConfigDict(frozen=True)


class SearchMeasurementCategoriesQuery(BaseModel):
    """No documentation found for this operation."""

    options: tuple[SearchMeasurementCategoriesQueryOptions, ...]
    "List all measurement categories"

    class Arguments(BaseModel):
        """Arguments for SearchMeasurementCategories"""

        search: str | None = Field(default=None)
        values: list[ID] | None = Field(default=None)

    class Meta:
        """Meta class for SearchMeasurementCategories"""

        document = "query SearchMeasurementCategories($search: String, $values: [ID!]) {\n  options: measurementCategories(\n    filters: {search: $search, ids: $values}\n    pagination: {limit: 10}\n  ) {\n    value: id\n    label: label\n    __typename\n  }\n}"


class GetStructureRelationCategoryQuery(BaseModel):
    """No documentation found for this operation."""

    structure_relation_category: StructureRelationCategory = Field(
        alias="structureRelationCategory"
    )
    "Get a single structure relation category by ID"

    class Arguments(BaseModel):
        """Arguments for GetStructureRelationCategory"""

        id: ID

    class Meta:
        """Meta class for GetStructureRelationCategory"""

        document = "fragment CategoryRef on Category {\n  id\n  key\n  label\n  ageName\n  __typename\n}\n\nfragment MediaStore on MediaStore {\n  id\n  key\n  presignedUrl\n  __typename\n}\n\nfragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment CategoryBase on Category {\n  ...CategoryRef\n  description\n  purl\n  color\n  pinned\n  image {\n    ...MediaStore\n    __typename\n  }\n  graph {\n    id\n    name\n    __typename\n  }\n  term {\n    ...TermRef\n    __typename\n  }\n  __typename\n}\n\nfragment PropertyDefinition on PropertyDefinition {\n  key\n  label\n  valueKind\n  unit\n  description\n  derivation\n  index\n  searchable\n  __typename\n}\n\nfragment StructureDescriptor on StructureDescriptor {\n  defaultCategoryKey\n  __typename\n}\n\nfragment StructureRelationCategory on StructureRelationCategory {\n  ...CategoryBase\n  sourceDescriptor {\n    ...StructureDescriptor\n    __typename\n  }\n  targetDescriptor {\n    ...StructureDescriptor\n    __typename\n  }\n  propertyDefinitions {\n    ...PropertyDefinition\n    __typename\n  }\n  __typename\n}\n\nquery GetStructureRelationCategory($id: ID!) {\n  structureRelationCategory(id: $id) {\n    ...StructureRelationCategory\n    __typename\n  }\n}"


class ListStructureRelationCategoriesQuery(BaseModel):
    """No documentation found for this operation."""

    structure_relation_categories: tuple[StructureRelationCategory, ...] = Field(
        alias="structureRelationCategories"
    )
    "List all structure relation categories"

    class Arguments(BaseModel):
        """Arguments for ListStructureRelationCategories"""

        filters: StructureRelationCategoryFilter | None = Field(default=None)
        pagination: OffsetPaginationInput | None = Field(default=None)

    class Meta:
        """Meta class for ListStructureRelationCategories"""

        document = "fragment CategoryRef on Category {\n  id\n  key\n  label\n  ageName\n  __typename\n}\n\nfragment MediaStore on MediaStore {\n  id\n  key\n  presignedUrl\n  __typename\n}\n\nfragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment CategoryBase on Category {\n  ...CategoryRef\n  description\n  purl\n  color\n  pinned\n  image {\n    ...MediaStore\n    __typename\n  }\n  graph {\n    id\n    name\n    __typename\n  }\n  term {\n    ...TermRef\n    __typename\n  }\n  __typename\n}\n\nfragment PropertyDefinition on PropertyDefinition {\n  key\n  label\n  valueKind\n  unit\n  description\n  derivation\n  index\n  searchable\n  __typename\n}\n\nfragment StructureDescriptor on StructureDescriptor {\n  defaultCategoryKey\n  __typename\n}\n\nfragment StructureRelationCategory on StructureRelationCategory {\n  ...CategoryBase\n  sourceDescriptor {\n    ...StructureDescriptor\n    __typename\n  }\n  targetDescriptor {\n    ...StructureDescriptor\n    __typename\n  }\n  propertyDefinitions {\n    ...PropertyDefinition\n    __typename\n  }\n  __typename\n}\n\nquery ListStructureRelationCategories($filters: StructureRelationCategoryFilter, $pagination: OffsetPaginationInput) {\n  structureRelationCategories(filters: $filters, pagination: $pagination) {\n    ...StructureRelationCategory\n    __typename\n  }\n}"


class SearchStructureRelationCategoriesQueryOptions(
    StructureRelationCategoryTrait, BaseModel
):
    """A relation category definition"""

    typename: Literal["StructureRelationCategory"] = Field(
        alias="__typename", default="StructureRelationCategory", exclude=True
    )
    value: ID
    "Database ID of the category"
    label: str
    "Label/name of the category"
    model_config = ConfigDict(frozen=True)


class SearchStructureRelationCategoriesQuery(BaseModel):
    """No documentation found for this operation."""

    options: tuple[SearchStructureRelationCategoriesQueryOptions, ...]
    "List all structure relation categories"

    class Arguments(BaseModel):
        """Arguments for SearchStructureRelationCategories"""

        search: str | None = Field(default=None)
        values: list[ID] | None = Field(default=None)

    class Meta:
        """Meta class for SearchStructureRelationCategories"""

        document = "query SearchStructureRelationCategories($search: String, $values: [ID!]) {\n  options: structureRelationCategories(\n    filters: {search: $search, ids: $values}\n    pagination: {limit: 10}\n  ) {\n    value: id\n    label: label\n    __typename\n  }\n}"


class GetNaturalEventCategoryQuery(BaseModel):
    """No documentation found for this operation."""

    natural_event_category: NaturalEventCategory = Field(alias="naturalEventCategory")
    "Get a single natural event category by ID"

    class Arguments(BaseModel):
        """Arguments for GetNaturalEventCategory"""

        id: ID

    class Meta:
        """Meta class for GetNaturalEventCategory"""

        document = "fragment CategoryRef on Category {\n  id\n  key\n  label\n  ageName\n  __typename\n}\n\nfragment EntityDescriptor on EntityDescriptor {\n  keys\n  ontologyTerms\n  defaultCategoryKey\n  __typename\n}\n\nfragment MediaStore on MediaStore {\n  id\n  key\n  presignedUrl\n  __typename\n}\n\nfragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment CategoryBase on Category {\n  ...CategoryRef\n  description\n  purl\n  color\n  pinned\n  image {\n    ...MediaStore\n    __typename\n  }\n  graph {\n    id\n    name\n    __typename\n  }\n  term {\n    ...TermRef\n    __typename\n  }\n  __typename\n}\n\nfragment EventRole on EventRole {\n  key\n  role\n  descriptor {\n    ...EntityDescriptor\n    __typename\n  }\n  __typename\n}\n\nfragment NaturalEventCategory on NaturalEventCategory {\n  ...CategoryBase\n  positionX\n  positionY\n  width\n  height\n  inputs {\n    ...EventRole\n    __typename\n  }\n  outputs {\n    ...EventRole\n    __typename\n  }\n  __typename\n}\n\nquery GetNaturalEventCategory($id: ID!) {\n  naturalEventCategory(id: $id) {\n    ...NaturalEventCategory\n    __typename\n  }\n}"


class ListNaturalEventCategoriesQuery(BaseModel):
    """No documentation found for this operation."""

    natural_event_categories: tuple[NaturalEventCategory, ...] = Field(
        alias="naturalEventCategories"
    )
    "List all natural event categories"

    class Arguments(BaseModel):
        """Arguments for ListNaturalEventCategories"""

        filters: NaturalEventCategoryFilter | None = Field(default=None)
        pagination: OffsetPaginationInput | None = Field(default=None)

    class Meta:
        """Meta class for ListNaturalEventCategories"""

        document = "fragment CategoryRef on Category {\n  id\n  key\n  label\n  ageName\n  __typename\n}\n\nfragment EntityDescriptor on EntityDescriptor {\n  keys\n  ontologyTerms\n  defaultCategoryKey\n  __typename\n}\n\nfragment MediaStore on MediaStore {\n  id\n  key\n  presignedUrl\n  __typename\n}\n\nfragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment CategoryBase on Category {\n  ...CategoryRef\n  description\n  purl\n  color\n  pinned\n  image {\n    ...MediaStore\n    __typename\n  }\n  graph {\n    id\n    name\n    __typename\n  }\n  term {\n    ...TermRef\n    __typename\n  }\n  __typename\n}\n\nfragment EventRole on EventRole {\n  key\n  role\n  descriptor {\n    ...EntityDescriptor\n    __typename\n  }\n  __typename\n}\n\nfragment NaturalEventCategory on NaturalEventCategory {\n  ...CategoryBase\n  positionX\n  positionY\n  width\n  height\n  inputs {\n    ...EventRole\n    __typename\n  }\n  outputs {\n    ...EventRole\n    __typename\n  }\n  __typename\n}\n\nquery ListNaturalEventCategories($filters: NaturalEventCategoryFilter, $pagination: OffsetPaginationInput) {\n  naturalEventCategories(filters: $filters, pagination: $pagination) {\n    ...NaturalEventCategory\n    __typename\n  }\n}"


class SearchNaturalEventCategoriesQueryOptions(NaturalEventCategoryTrait, BaseModel):
    """A relation category definition"""

    typename: Literal["NaturalEventCategory"] = Field(
        alias="__typename", default="NaturalEventCategory", exclude=True
    )
    value: ID
    "Database ID of the category"
    label: str
    "Label/name of the category"
    model_config = ConfigDict(frozen=True)


class SearchNaturalEventCategoriesQuery(BaseModel):
    """No documentation found for this operation."""

    options: tuple[SearchNaturalEventCategoriesQueryOptions, ...]
    "List all natural event categories"

    class Arguments(BaseModel):
        """Arguments for SearchNaturalEventCategories"""

        search: str | None = Field(default=None)
        values: list[ID] | None = Field(default=None)

    class Meta:
        """Meta class for SearchNaturalEventCategories"""

        document = "query SearchNaturalEventCategories($search: String, $values: [ID!]) {\n  options: naturalEventCategories(\n    filters: {search: $search, ids: $values}\n    pagination: {limit: 10}\n  ) {\n    value: id\n    label: label\n    __typename\n  }\n}"


class GetProtocolEventCategoryQuery(BaseModel):
    """No documentation found for this operation."""

    protocol_event_category: ProtocolEventCategory = Field(
        alias="protocolEventCategory"
    )
    "Get a single protocol event category by ID"

    class Arguments(BaseModel):
        """Arguments for GetProtocolEventCategory"""

        id: ID

    class Meta:
        """Meta class for GetProtocolEventCategory"""

        document = "fragment CategoryRef on Category {\n  id\n  key\n  label\n  ageName\n  __typename\n}\n\nfragment EntityDescriptor on EntityDescriptor {\n  keys\n  ontologyTerms\n  defaultCategoryKey\n  __typename\n}\n\nfragment MediaStore on MediaStore {\n  id\n  key\n  presignedUrl\n  __typename\n}\n\nfragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment CategoryBase on Category {\n  ...CategoryRef\n  description\n  purl\n  color\n  pinned\n  image {\n    ...MediaStore\n    __typename\n  }\n  graph {\n    id\n    name\n    __typename\n  }\n  term {\n    ...TermRef\n    __typename\n  }\n  __typename\n}\n\nfragment EventRole on EventRole {\n  key\n  role\n  descriptor {\n    ...EntityDescriptor\n    __typename\n  }\n  __typename\n}\n\nfragment ProtocolEventCategory on ProtocolEventCategory {\n  ...CategoryBase\n  positionX\n  positionY\n  width\n  height\n  inputs {\n    ...EventRole\n    __typename\n  }\n  outputs {\n    ...EventRole\n    __typename\n  }\n  __typename\n}\n\nquery GetProtocolEventCategory($id: ID!) {\n  protocolEventCategory(id: $id) {\n    ...ProtocolEventCategory\n    __typename\n  }\n}"


class ListProtocolEventCategoriesQuery(BaseModel):
    """No documentation found for this operation."""

    protocol_event_categories: tuple[ProtocolEventCategory, ...] = Field(
        alias="protocolEventCategories"
    )
    "List all protocol event categories"

    class Arguments(BaseModel):
        """Arguments for ListProtocolEventCategories"""

        filters: ProtocolEventCategoryFilter | None = Field(default=None)
        pagination: OffsetPaginationInput | None = Field(default=None)

    class Meta:
        """Meta class for ListProtocolEventCategories"""

        document = "fragment CategoryRef on Category {\n  id\n  key\n  label\n  ageName\n  __typename\n}\n\nfragment EntityDescriptor on EntityDescriptor {\n  keys\n  ontologyTerms\n  defaultCategoryKey\n  __typename\n}\n\nfragment MediaStore on MediaStore {\n  id\n  key\n  presignedUrl\n  __typename\n}\n\nfragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment CategoryBase on Category {\n  ...CategoryRef\n  description\n  purl\n  color\n  pinned\n  image {\n    ...MediaStore\n    __typename\n  }\n  graph {\n    id\n    name\n    __typename\n  }\n  term {\n    ...TermRef\n    __typename\n  }\n  __typename\n}\n\nfragment EventRole on EventRole {\n  key\n  role\n  descriptor {\n    ...EntityDescriptor\n    __typename\n  }\n  __typename\n}\n\nfragment ProtocolEventCategory on ProtocolEventCategory {\n  ...CategoryBase\n  positionX\n  positionY\n  width\n  height\n  inputs {\n    ...EventRole\n    __typename\n  }\n  outputs {\n    ...EventRole\n    __typename\n  }\n  __typename\n}\n\nquery ListProtocolEventCategories($filters: ProtocolEventCategoryFilter, $pagination: OffsetPaginationInput) {\n  protocolEventCategories(filters: $filters, pagination: $pagination) {\n    ...ProtocolEventCategory\n    __typename\n  }\n}"


class SearchProtocolEventCategoriesQueryOptions(ProtocolEventCategoryTrait, BaseModel):
    """A relation category definition"""

    typename: Literal["ProtocolEventCategory"] = Field(
        alias="__typename", default="ProtocolEventCategory", exclude=True
    )
    value: ID
    "Database ID of the category"
    label: str
    "Label/name of the category"
    model_config = ConfigDict(frozen=True)


class SearchProtocolEventCategoriesQuery(BaseModel):
    """No documentation found for this operation."""

    options: tuple[SearchProtocolEventCategoriesQueryOptions, ...]
    "List all protocol event categories"

    class Arguments(BaseModel):
        """Arguments for SearchProtocolEventCategories"""

        search: str | None = Field(default=None)
        values: list[ID] | None = Field(default=None)

    class Meta:
        """Meta class for SearchProtocolEventCategories"""

        document = "query SearchProtocolEventCategories($search: String, $values: [ID!]) {\n  options: protocolEventCategories(\n    filters: {search: $search, ids: $values}\n    pagination: {limit: 10}\n  ) {\n    value: id\n    label: label\n    __typename\n  }\n}"


class GetInstanceQuery(BaseModel):
    """Claim-grain reads: organization scope, addressed by a bare uuid, no graph argument.
    `instance(id:)` is the fallback reader for a node no view draws."""

    instance: Instance
    "Get one claimed individual by ID, as the log has it"

    class Arguments(BaseModel):
        """Arguments for GetInstance"""

        id: ID

    class Meta:
        """Meta class for GetInstance"""

        document = "fragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment Assertion on Assertion {\n  id\n  subject\n  appId\n  actionId\n  actionName\n  assertedAt\n  recordedAt\n  seq\n  __typename\n}\n\nfragment InstanceRef on Instance {\n  id\n  kind\n  term {\n    ...TermRef\n    __typename\n  }\n  __typename\n}\n\nfragment Instance on Instance {\n  ...InstanceRef\n  createdAt\n  component\n  assertion {\n    ...Assertion\n    __typename\n  }\n  __typename\n}\n\nquery GetInstance($id: ID!) {\n  instance(id: $id) {\n    ...Instance\n    __typename\n  }\n}"


class GetLinkQuery(BaseModel):
    """No documentation found for this operation."""

    link: Link
    "Get one claim relating two things by ID, as the log has it"

    class Arguments(BaseModel):
        """Arguments for GetLink"""

        id: ID

    class Meta:
        """Meta class for GetLink"""

        document = "fragment Assertion on Assertion {\n  id\n  subject\n  appId\n  actionId\n  actionName\n  assertedAt\n  recordedAt\n  seq\n  __typename\n}\n\nfragment LinkRef on Link {\n  id\n  kind\n  sourceRef\n  targetRef\n  __typename\n}\n\nfragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment Link on Link {\n  ...LinkRef\n  role\n  createdAt\n  term {\n    ...TermRef\n    __typename\n  }\n  assertion {\n    ...Assertion\n    __typename\n  }\n  __typename\n}\n\nquery GetLink($id: ID!) {\n  link(id: $id) {\n    ...Link\n    __typename\n  }\n}"


class GetStandingsQuery(BaseModel):
    """Every position anyone has taken on a claim, newest first. An empty list means nobody has
    disputed it — silence is not dissent, and there is no folded boolean beside this."""

    standings: tuple[Standing, ...]
    "Every position anyone has taken on one claim, newest first"

    class Arguments(BaseModel):
        """Arguments for GetStandings"""

        id: ID

    class Meta:
        """Meta class for GetStandings"""

        document = "fragment Assertion on Assertion {\n  id\n  subject\n  appId\n  actionId\n  actionName\n  assertedAt\n  recordedAt\n  seq\n  __typename\n}\n\nfragment Standing on Standing {\n  id\n  stands\n  at\n  assertion {\n    ...Assertion\n    __typename\n  }\n  __typename\n}\n\nquery GetStandings($id: ID!) {\n  standings(id: $id) {\n    ...Standing\n    __typename\n  }\n}"


class GetStructureQuery(BaseModel):
    """No documentation found for this operation."""

    structure: StructureWithMetrics
    "Get a structure by ID — a bare uuid, its evidence primary key"

    class Arguments(BaseModel):
        """Arguments for GetStructure"""

        id: ID

    class Meta:
        """Meta class for GetStructure"""

        document = "fragment Metric on Metric {\n  id\n  kindId\n  key\n  value\n  unit\n  confidence\n  confidenceType\n  observedAt\n  assertedAt\n  __typename\n}\n\nfragment Structure on Structure {\n  id\n  identifier\n  object\n  kindId\n  __typename\n}\n\nfragment StructureWithMetrics on Structure {\n  ...Structure\n  metrics {\n    ...Metric\n    __typename\n  }\n  __typename\n}\n\nquery GetStructure($id: ID!) {\n  structure(id: $id) {\n    ...StructureWithMetrics\n    __typename\n  }\n}"


class GetStructureByIdentifierQuery(BaseModel):
    """No documentation found for this operation."""

    structure_by_identifier: StructureWithMetrics = Field(alias="structureByIdentifier")
    "Get a structure by identifier and object. No graph: a structure belongs to the organization and has no vertex in any projection"

    class Arguments(BaseModel):
        """Arguments for GetStructureByIdentifier"""

        identifier: StructureIdentifier
        object: StructureObject

    class Meta:
        """Meta class for GetStructureByIdentifier"""

        document = "fragment Metric on Metric {\n  id\n  kindId\n  key\n  value\n  unit\n  confidence\n  confidenceType\n  observedAt\n  assertedAt\n  __typename\n}\n\nfragment Structure on Structure {\n  id\n  identifier\n  object\n  kindId\n  __typename\n}\n\nfragment StructureWithMetrics on Structure {\n  ...Structure\n  metrics {\n    ...Metric\n    __typename\n  }\n  __typename\n}\n\nquery GetStructureByIdentifier($identifier: StructureIdentifier!, $object: StructureObject!) {\n  structureByIdentifier(identifier: $identifier, object: $object) {\n    ...StructureWithMetrics\n    __typename\n  }\n}"


class GetInformingStructuresQuery(BaseModel):
    """Resolves a naming structure back to what it names — this is how an external id is looked up
    now that `externalId` no longer exists on any write."""

    informing_structures: tuple[Structure, ...] = Field(alias="informingStructures")
    "List the structures that are evidence for an entity"

    class Arguments(BaseModel):
        """Arguments for GetInformingStructures"""

        entity_id: str = Field(
            validation_alias=AliasChoices("entity_id", "entityId"),
            serialization_alias="entityId",
        )

    class Meta:
        """Meta class for GetInformingStructures"""

        document = "fragment Structure on Structure {\n  id\n  identifier\n  object\n  kindId\n  __typename\n}\n\nquery GetInformingStructures($entityId: String!) {\n  informingStructures(entityId: $entityId) {\n    ...Structure\n    __typename\n  }\n}"


class ListStructuresQuery(BaseModel):
    """No documentation found for this operation."""

    structures: tuple[Structure, ...]
    "List structures with optional filters, ordering, and pagination"

    class Arguments(BaseModel):
        """Arguments for ListStructures"""

        structure_kind_id: ID | None = Field(
            validation_alias=AliasChoices("structure_kind_id", "structureKindId"),
            serialization_alias="structureKindId",
            default=None,
        )
        filters: StructureFilter | None = Field(default=None)
        ordering: list[StructureOrder] | None = Field(default=None)
        pagination: StructurePaginationInput | None = Field(default=None)

    class Meta:
        """Meta class for ListStructures"""

        document = "fragment Structure on Structure {\n  id\n  identifier\n  object\n  kindId\n  __typename\n}\n\nquery ListStructures($structureKindId: ID, $filters: StructureFilter, $ordering: [StructureOrder!], $pagination: StructurePaginationInput) {\n  structures(\n    structureKindId: $structureKindId\n    filters: $filters\n    ordering: $ordering\n    pagination: $pagination\n  ) {\n    ...Structure\n    __typename\n  }\n}"


class GetMetricQuery(BaseModel):
    """No documentation found for this operation."""

    metric: Metric
    "Get a metric by ID"

    class Arguments(BaseModel):
        """Arguments for GetMetric"""

        id: ID

    class Meta:
        """Meta class for GetMetric"""

        document = "fragment Metric on Metric {\n  id\n  kindId\n  key\n  value\n  unit\n  confidence\n  confidenceType\n  observedAt\n  assertedAt\n  __typename\n}\n\nquery GetMetric($id: ID!) {\n  metric(id: $id) {\n    ...Metric\n    __typename\n  }\n}"


class GetMetricsForStructureQuery(BaseModel):
    """No documentation found for this operation."""

    metrics_for_structure: tuple[Metric, ...] = Field(alias="metricsForStructure")
    "List every un-retracted metric describing a structure"

    class Arguments(BaseModel):
        """Arguments for GetMetricsForStructure"""

        structure_id: ID = Field(
            validation_alias=AliasChoices("structure_id", "structureId"),
            serialization_alias="structureId",
        )

    class Meta:
        """Meta class for GetMetricsForStructure"""

        document = "fragment Metric on Metric {\n  id\n  kindId\n  key\n  value\n  unit\n  confidence\n  confidenceType\n  observedAt\n  assertedAt\n  __typename\n}\n\nquery GetMetricsForStructure($structureId: ID!) {\n  metricsForStructure(structureId: $structureId) {\n    ...Metric\n    __typename\n  }\n}"


class GetCommentQuery(BaseModel):
    """No documentation found for this operation."""

    comment: Comment
    "Get one remark by ID, as the log has it"

    class Arguments(BaseModel):
        """Arguments for GetComment"""

        id: ID

    class Meta:
        """Meta class for GetComment"""

        document = "fragment Assertion on Assertion {\n  id\n  subject\n  appId\n  actionId\n  actionName\n  assertedAt\n  recordedAt\n  seq\n  __typename\n}\n\nfragment Comment on Comment {\n  id\n  createdAt\n  text\n  resolved\n  mentions\n  parent {\n    id\n    __typename\n  }\n  assertion {\n    ...Assertion\n    __typename\n  }\n  __typename\n}\n\nquery GetComment($id: ID!) {\n  comment(id: $id) {\n    ...Comment\n    __typename\n  }\n}"


class GetCommentsForQuery(BaseModel):
    """No documentation found for this operation."""

    comments_for: tuple[Comment, ...] = Field(alias="commentsFor")
    "Every remark about one external datum, addressed by (identifier, object), newest first — resolved ones included"

    class Arguments(BaseModel):
        """Arguments for GetCommentsFor"""

        identifier: str
        object: ID

    class Meta:
        """Meta class for GetCommentsFor"""

        document = "fragment Assertion on Assertion {\n  id\n  subject\n  appId\n  actionId\n  actionName\n  assertedAt\n  recordedAt\n  seq\n  __typename\n}\n\nfragment Comment on Comment {\n  id\n  createdAt\n  text\n  resolved\n  mentions\n  parent {\n    id\n    __typename\n  }\n  assertion {\n    ...Assertion\n    __typename\n  }\n  __typename\n}\n\nquery GetCommentsFor($identifier: String!, $object: ID!) {\n  commentsFor(identifier: $identifier, object: $object) {\n    ...Comment\n    __typename\n  }\n}"


class SearchStructuresQueryOptions(StructureTrait, BaseModel):
    """An individual with an external identity — an ROI, an image, a file. A claim about the world, never a graph node (RFC 0023)"""

    typename: Literal["Structure"] = Field(
        alias="__typename", default="Structure", exclude=True
    )
    value: ID
    "This claim's durable identity — the `Structure` primary key, a bare uuid"
    label: str
    "External object ID this structure references"
    model_config = ConfigDict(frozen=True)


class SearchStructuresQuery(BaseModel):
    """No documentation found for this operation."""

    options: tuple[SearchStructuresQueryOptions, ...]
    "List structures with optional filters, ordering, and pagination"

    class Arguments(BaseModel):
        """Arguments for SearchStructures"""

        search: str | None = Field(default=None)
        values: list[ID] | None = Field(default=None)

    class Meta:
        """Meta class for SearchStructures"""

        document = "query SearchStructures($search: String, $values: [ID!]) {\n  options: structures(\n    filters: {search: $search, ids: $values}\n    pagination: {limit: 10}\n  ) {\n    value: id\n    label: object\n    __typename\n  }\n}"


class GetGraphQuery(BaseModel):
    """No documentation found for this operation."""

    graph: Graph
    "Get a graph by ID"

    class Arguments(BaseModel):
        """Arguments for GetGraph"""

        id: ID

    class Meta:
        """Meta class for GetGraph"""

        document = "fragment CategoryRef on Category {\n  id\n  key\n  label\n  ageName\n  __typename\n}\n\nfragment MediaStore on MediaStore {\n  id\n  key\n  presignedUrl\n  __typename\n}\n\nfragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment CategoryBase on Category {\n  ...CategoryRef\n  description\n  purl\n  color\n  pinned\n  image {\n    ...MediaStore\n    __typename\n  }\n  graph {\n    id\n    name\n    __typename\n  }\n  term {\n    ...TermRef\n    __typename\n  }\n  __typename\n}\n\nfragment EntityDescriptor on EntityDescriptor {\n  keys\n  ontologyTerms\n  defaultCategoryKey\n  __typename\n}\n\nfragment EventRole on EventRole {\n  key\n  role\n  descriptor {\n    ...EntityDescriptor\n    __typename\n  }\n  __typename\n}\n\nfragment PropertyDefinition on PropertyDefinition {\n  key\n  label\n  valueKind\n  unit\n  description\n  derivation\n  index\n  searchable\n  __typename\n}\n\nfragment StructureDescriptor on StructureDescriptor {\n  defaultCategoryKey\n  __typename\n}\n\nfragment EntityCategory on EntityCategory {\n  ...CategoryBase\n  instanceKind\n  positionX\n  positionY\n  width\n  height\n  propertyDefinitions {\n    ...PropertyDefinition\n    __typename\n  }\n  __typename\n}\n\nfragment GraphProjection on GraphProjection {\n  kind\n  status\n  projectedThroughSeq\n  derivedThroughSeq\n  lag\n  pending\n  schemaStale\n  schemaHash\n  derivedAt\n  rebuiltAt\n  __typename\n}\n\nfragment ListGraph on Graph {\n  id\n  name\n  description\n  ageName\n  isArchived\n  pinned\n  __typename\n}\n\nfragment MeasurementCategory on MeasurementCategory {\n  ...CategoryBase\n  sourceDescriptor {\n    ...StructureDescriptor\n    __typename\n  }\n  targetDescriptor {\n    ...EntityDescriptor\n    __typename\n  }\n  propertyDefinitions {\n    ...PropertyDefinition\n    __typename\n  }\n  __typename\n}\n\nfragment NaturalEventCategory on NaturalEventCategory {\n  ...CategoryBase\n  positionX\n  positionY\n  width\n  height\n  inputs {\n    ...EventRole\n    __typename\n  }\n  outputs {\n    ...EventRole\n    __typename\n  }\n  __typename\n}\n\nfragment ProtocolEventCategory on ProtocolEventCategory {\n  ...CategoryBase\n  positionX\n  positionY\n  width\n  height\n  inputs {\n    ...EventRole\n    __typename\n  }\n  outputs {\n    ...EventRole\n    __typename\n  }\n  __typename\n}\n\nfragment RelationCategory on RelationCategory {\n  ...CategoryBase\n  sourceDescriptor {\n    ...EntityDescriptor\n    __typename\n  }\n  targetDescriptor {\n    ...EntityDescriptor\n    __typename\n  }\n  propertyDefinitions {\n    ...PropertyDefinition\n    __typename\n  }\n  __typename\n}\n\nfragment StructureRelationCategory on StructureRelationCategory {\n  ...CategoryBase\n  sourceDescriptor {\n    ...StructureDescriptor\n    __typename\n  }\n  targetDescriptor {\n    ...StructureDescriptor\n    __typename\n  }\n  propertyDefinitions {\n    ...PropertyDefinition\n    __typename\n  }\n  __typename\n}\n\nfragment Graph on Graph {\n  ...ListGraph\n  purl\n  projection {\n    ...GraphProjection\n    __typename\n  }\n  entityCategories {\n    ...EntityCategory\n    __typename\n  }\n  relationCategories {\n    ...RelationCategory\n    __typename\n  }\n  measurementCategories {\n    ...MeasurementCategory\n    __typename\n  }\n  structureRelationCategories {\n    ...StructureRelationCategory\n    __typename\n  }\n  naturalEventCategories {\n    ...NaturalEventCategory\n    __typename\n  }\n  protocolEventCategories {\n    ...ProtocolEventCategory\n    __typename\n  }\n  __typename\n}\n\nquery GetGraph($id: ID!) {\n  graph(id: $id) {\n    ...Graph\n    __typename\n  }\n}"


class ListGraphsQuery(BaseModel):
    """No documentation found for this operation."""

    graphs: tuple[ListGraph, ...]
    "List all graphs in the graph engine"

    class Arguments(BaseModel):
        """Arguments for ListGraphs"""

        filters: GraphFilter | None = Field(default=None)
        pagination: OffsetPaginationInput | None = Field(default=None)

    class Meta:
        """Meta class for ListGraphs"""

        document = "fragment ListGraph on Graph {\n  id\n  name\n  description\n  ageName\n  isArchived\n  pinned\n  __typename\n}\n\nquery ListGraphs($filters: GraphFilter, $pagination: OffsetPaginationInput) {\n  graphs(filters: $filters, pagination: $pagination) {\n    ...ListGraph\n    __typename\n  }\n}"


class SearchGraphsQueryOptions(GraphTrait, BaseModel):
    """One view over the organization's evidence log"""

    typename: Literal["Graph"] = Field(
        alias="__typename", default="Graph", exclude=True
    )
    value: ID
    "Database ID of the graph"
    label: str
    "Name of the graph"
    model_config = ConfigDict(frozen=True)


class SearchGraphsQuery(BaseModel):
    """No documentation found for this operation."""

    options: tuple[SearchGraphsQueryOptions, ...]
    "List all graphs in the graph engine"

    class Arguments(BaseModel):
        """Arguments for SearchGraphs"""

        search: str | None = Field(default=None)
        values: list[ID] | None = Field(default=None)

    class Meta:
        """Meta class for SearchGraphs"""

        document = "query SearchGraphs($search: String, $values: [ID!]) {\n  options: graphs(\n    filters: {search: $search, ids: $values}\n    pagination: {limit: 10}\n  ) {\n    value: id\n    label: name\n    __typename\n  }\n}"


class GetNodeQueryNodeBase(NodeTrait, BaseModel):
    """Base interface for all graph nodes"""

    model_config = ConfigDict(frozen=True)


class GetNodeQueryNodeBaseEntity(
    NodeRefEntity, GetNodeQueryNodeBase, EntityTrait, BaseModel
):
    """An entity in the knowledge graph with derived properties"""

    typename: Literal["Entity"] = Field(
        alias="__typename", default="Entity", exclude=True
    )


class GetNodeQueryNodeBaseNaturalEvent(
    NodeRefNaturalEvent, GetNodeQueryNodeBase, BaseModel
):
    """A natural event in the knowledge graph"""

    typename: Literal["NaturalEvent"] = Field(
        alias="__typename", default="NaturalEvent", exclude=True
    )


class GetNodeQueryNodeBaseProtocolEvent(
    NodeRefProtocolEvent, GetNodeQueryNodeBase, BaseModel
):
    """A protocol event in the graph"""

    typename: Literal["ProtocolEvent"] = Field(
        alias="__typename", default="ProtocolEvent", exclude=True
    )


class GetNodeQueryNodeBaseCatchAll(GetNodeQueryNodeBase, BaseModel):
    """Catch all class for GetNodeQueryNodeBase"""

    typename: str = Field(alias="__typename", exclude=True)


class GetNodeQuery(BaseModel):
    """View-grain reads: these name their view, and refuse a node the view does not admit.
    `node(id, graph)` succeeds exactly when `nodes(graph:)` could list it."""

    node: Annotated[
        GetNodeQueryNodeBaseEntity
        | GetNodeQueryNodeBaseNaturalEvent
        | GetNodeQueryNodeBaseProtocolEvent,
        Field(discriminator="typename"),
    ] | GetNodeQueryNodeBaseCatchAll
    "Get a node by ID, as the named view holds it. Refused when that view does not admit the node; the claim itself is `instance(id:)`"

    class Arguments(BaseModel):
        """Arguments for GetNode"""

        id: ID
        graph: ID

    class Meta:
        """Meta class for GetNode"""

        document = "fragment NodeRef on Node {\n  id\n  label\n  __typename\n}\n\nquery GetNode($id: ID!, $graph: ID!) {\n  node(id: $id, graph: $graph) {\n    ...NodeRef\n    __typename\n  }\n}"


class ListNodesQueryNodesBase(NodeTrait, BaseModel):
    """Base interface for all graph nodes"""

    model_config = ConfigDict(frozen=True)


class ListNodesQueryNodesBaseEntity(
    NodeRefEntity, ListNodesQueryNodesBase, EntityTrait, BaseModel
):
    """An entity in the knowledge graph with derived properties"""

    typename: Literal["Entity"] = Field(
        alias="__typename", default="Entity", exclude=True
    )


class ListNodesQueryNodesBaseNaturalEvent(
    NodeRefNaturalEvent, ListNodesQueryNodesBase, BaseModel
):
    """A natural event in the knowledge graph"""

    typename: Literal["NaturalEvent"] = Field(
        alias="__typename", default="NaturalEvent", exclude=True
    )


class ListNodesQueryNodesBaseProtocolEvent(
    NodeRefProtocolEvent, ListNodesQueryNodesBase, BaseModel
):
    """A protocol event in the graph"""

    typename: Literal["ProtocolEvent"] = Field(
        alias="__typename", default="ProtocolEvent", exclude=True
    )


class ListNodesQueryNodesBaseCatchAll(ListNodesQueryNodesBase, BaseModel):
    """Catch all class for ListNodesQueryNodesBase"""

    typename: str = Field(alias="__typename", exclude=True)


class ListNodesQuery(BaseModel):
    """No documentation found for this operation."""

    nodes: tuple[
        Annotated[
            ListNodesQueryNodesBaseEntity
            | ListNodesQueryNodesBaseNaturalEvent
            | ListNodesQueryNodesBaseProtocolEvent,
            Field(discriminator="typename"),
        ]
        | ListNodesQueryNodesBaseCatchAll,
        ...,
    ]
    "List the individuals a view holds, as it draws them — view grain: one row per individual, membership from the view's rule, properties as of the view's cursor"

    class Arguments(BaseModel):
        """Arguments for ListNodes"""

        graph: ID
        filters: NodeFilters | None = Field(default=None)
        ordering: list[NodeOrder] | None = Field(default=None)
        pagination: NodePaginationInput | None = Field(default=None)

    class Meta:
        """Meta class for ListNodes"""

        document = "fragment NodeRef on Node {\n  id\n  label\n  __typename\n}\n\nquery ListNodes($graph: ID!, $filters: NodeFilters, $ordering: [NodeOrder!], $pagination: NodePaginationInput) {\n  nodes(\n    graph: $graph\n    filters: $filters\n    ordering: $ordering\n    pagination: $pagination\n  ) {\n    ...NodeRef\n    __typename\n  }\n}"


class GetEntityQuery(BaseModel):
    """richProperties is where derived values surface — the only place a metric recorded on an
    evidence structure becomes readable as a property of the node."""

    entity: EntityView
    "Get an entity by ID, as the named view holds it — see `node`"

    class Arguments(BaseModel):
        """Arguments for GetEntity"""

        id: ID
        graph: ID

    class Meta:
        """Meta class for GetEntity"""

        document = "fragment EntityView on Entity {\n  id\n  label\n  categoryIds\n  validFrom\n  validTo\n  properties\n  richProperties {\n    key\n    value\n    nEvidence\n    spread\n    measuredFrom\n    measuredTo\n    __typename\n  }\n  __typename\n}\n\nquery GetEntity($id: ID!, $graph: ID!) {\n  entity(id: $id, graph: $graph) {\n    ...EntityView\n    __typename\n  }\n}"


class GetTermQuery(BaseModel):
    """No documentation found for this operation."""

    term: Term
    "Get one of the organization's words by ID"

    class Arguments(BaseModel):
        """Arguments for GetTerm"""

        id: ID

    class Meta:
        """Meta class for GetTerm"""

        document = "fragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment Term on Term {\n  ...TermRef\n  label\n  description\n  purl\n  color\n  createdAt\n  __typename\n}\n\nquery GetTerm($id: ID!) {\n  term(id: $id) {\n    ...Term\n    __typename\n  }\n}"


class ListTermsQuery(BaseModel):
    """No documentation found for this operation."""

    terms: tuple[Term, ...]
    "List the organization's words — its vocabulary, independent of any graph"

    class Arguments(BaseModel):
        """Arguments for ListTerms"""

        filters: TermFilter | None = Field(default=None)
        pagination: VocabularyPaginationInput | None = Field(default=None)

    class Meta:
        """Meta class for ListTerms"""

        document = "fragment TermRef on Term {\n  id\n  key\n  kind\n  __typename\n}\n\nfragment Term on Term {\n  ...TermRef\n  label\n  description\n  purl\n  color\n  createdAt\n  __typename\n}\n\nquery ListTerms($filters: TermFilter, $pagination: VocabularyPaginationInput) {\n  terms(filters: $filters, pagination: $pagination) {\n    ...Term\n    __typename\n  }\n}"


class SearchTermsQueryOptions(TermTrait, BaseModel):
    """A word this organization uses for a kind of thing"""

    typename: Literal["Term"] = Field(alias="__typename", default="Term", exclude=True)
    value: ID
    "Database ID of the term"
    label: str
    "The word itself, e.g. 'AIS'"
    model_config = ConfigDict(frozen=True)


class SearchTermsQuery(BaseModel):
    """No documentation found for this operation."""

    options: tuple[SearchTermsQueryOptions, ...]
    "List the organization's words — its vocabulary, independent of any graph"

    class Arguments(BaseModel):
        """Arguments for SearchTerms"""

        search: str | None = Field(default=None)
        values: list[ID] | None = Field(default=None)

    class Meta:
        """Meta class for SearchTerms"""

        document = "query SearchTerms($search: String, $values: [ID!]) {\n  options: terms(\n    filters: {search: $search, ids: $values}\n    pagination: {limit: 10}\n  ) {\n    value: id\n    label: key\n    __typename\n  }\n}"


class GetStructureKindQuery(BaseModel):
    """No documentation found for this operation."""

    structure_kind: StructureKind = Field(alias="structureKind")
    "Get one structure kind by ID"

    class Arguments(BaseModel):
        """Arguments for GetStructureKind"""

        id: ID

    class Meta:
        """Meta class for GetStructureKind"""

        document = "fragment StructureKind on StructureKind {\n  id\n  identifier\n  label\n  description\n  purl\n  color\n  createdAt\n  __typename\n}\n\nquery GetStructureKind($id: ID!) {\n  structureKind(id: $id) {\n    ...StructureKind\n    __typename\n  }\n}"


class ListStructureKindsQuery(BaseModel):
    """No documentation found for this operation."""

    structure_kinds: tuple[StructureKind, ...] = Field(alias="structureKinds")
    "List the organization's structure kinds"

    class Arguments(BaseModel):
        """Arguments for ListStructureKinds"""

        filters: StructureKindFilter | None = Field(default=None)
        pagination: VocabularyPaginationInput | None = Field(default=None)

    class Meta:
        """Meta class for ListStructureKinds"""

        document = "fragment StructureKind on StructureKind {\n  id\n  identifier\n  label\n  description\n  purl\n  color\n  createdAt\n  __typename\n}\n\nquery ListStructureKinds($filters: StructureKindFilter, $pagination: VocabularyPaginationInput) {\n  structureKinds(filters: $filters, pagination: $pagination) {\n    ...StructureKind\n    __typename\n  }\n}"


class SearchStructureKindsQueryOptions(StructureKindTrait, BaseModel):
    """A kind of external datum this organization knows about"""

    typename: Literal["StructureKind"] = Field(
        alias="__typename", default="StructureKind", exclude=True
    )
    value: ID
    "Database ID of the kind"
    label: str
    "The structure identifier, e.g. '@mikro/roi'"
    model_config = ConfigDict(frozen=True)


class SearchStructureKindsQuery(BaseModel):
    """No documentation found for this operation."""

    options: tuple[SearchStructureKindsQueryOptions, ...]
    "List the organization's structure kinds"

    class Arguments(BaseModel):
        """Arguments for SearchStructureKinds"""

        search: str | None = Field(default=None)
        values: list[ID] | None = Field(default=None)

    class Meta:
        """Meta class for SearchStructureKinds"""

        document = "query SearchStructureKinds($search: String, $values: [ID!]) {\n  options: structureKinds(\n    filters: {search: $search, ids: $values}\n    pagination: {limit: 10}\n  ) {\n    value: id\n    label: identifier\n    __typename\n  }\n}"


class GetMetricKindQuery(BaseModel):
    """No documentation found for this operation."""

    metric_kind: MetricKind = Field(alias="metricKind")
    "Get one metric kind by ID"

    class Arguments(BaseModel):
        """Arguments for GetMetricKind"""

        id: ID

    class Meta:
        """Meta class for GetMetricKind"""

        document = "fragment MetricKind on MetricKind {\n  id\n  key\n  valueKind\n  label\n  description\n  purl\n  color\n  createdAt\n  structureKind {\n    id\n    identifier\n    __typename\n  }\n  __typename\n}\n\nquery GetMetricKind($id: ID!) {\n  metricKind(id: $id) {\n    ...MetricKind\n    __typename\n  }\n}"


class ListMetricKindsQuery(BaseModel):
    """No documentation found for this operation."""

    metric_kinds: tuple[MetricKind, ...] = Field(alias="metricKinds")
    "List the organization's metric kinds"

    class Arguments(BaseModel):
        """Arguments for ListMetricKinds"""

        filters: MetricKindFilter | None = Field(default=None)
        pagination: VocabularyPaginationInput | None = Field(default=None)

    class Meta:
        """Meta class for ListMetricKinds"""

        document = "fragment MetricKind on MetricKind {\n  id\n  key\n  valueKind\n  label\n  description\n  purl\n  color\n  createdAt\n  structureKind {\n    id\n    identifier\n    __typename\n  }\n  __typename\n}\n\nquery ListMetricKinds($filters: MetricKindFilter, $pagination: VocabularyPaginationInput) {\n  metricKinds(filters: $filters, pagination: $pagination) {\n    ...MetricKind\n    __typename\n  }\n}"


class SearchMetricKindsQueryOptions(MetricKindTrait, BaseModel):
    """A kind of measurement that can be made about a structure kind"""

    typename: Literal["MetricKind"] = Field(
        alias="__typename", default="MetricKind", exclude=True
    )
    value: ID
    "Database ID of the kind"
    label: str
    "The measurement key, e.g. 'vector_length'"
    model_config = ConfigDict(frozen=True)


class SearchMetricKindsQuery(BaseModel):
    """No documentation found for this operation."""

    options: tuple[SearchMetricKindsQueryOptions, ...]
    "List the organization's metric kinds"

    class Arguments(BaseModel):
        """Arguments for SearchMetricKinds"""

        search: str | None = Field(default=None)
        values: list[ID] | None = Field(default=None)

    class Meta:
        """Meta class for SearchMetricKinds"""

        document = "query SearchMetricKinds($search: String, $values: [ID!]) {\n  options: metricKinds(\n    filters: {search: $search, ids: $values}\n    pagination: {limit: 10}\n  ) {\n    value: id\n    label: key\n    __typename\n  }\n}"


class KraphApi:
    """Every operation of this API as a method. Generated by turms.

    Each method hands its operation to ``execute``, ``aexecute``, ``subscribe``, ``asubscribe`` of ``self``, which the class this one is mixed into (or a base of it) provides.
    """

    async def acreate_entity_category(
        self,
        key: str,
        ontology_references: Iterable[OntologyReferenceInput],
        property_definitions: Iterable[PropertyDefinitionInput],
        graph: str,
        backfill: bool,
        description: str | None | UnsetType = UNSET,
        color: Iterable[int] | None | UnsetType = UNSET,
        image: str | None | UnsetType = UNSET,
        label: str | None | UnsetType = UNSET,
        pin: bool | None | UnsetType = UNSET,
        instance_kind: str | None | UnsetType = UNSET,
        definition: CategoryDefinitionInput | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> EntityCategory:
        """CreateEntityCategory
         A Category is one view's rule for a word: what it means HERE, how it is drawn, and which
         properties are derived onto it. Creating one never records a claim.

        Args:
            key: The label of the node participating in the event
            description: Description of this node role
            ontology_references: Ontology references for this event
            color: Optional RGBA color for this node role (e.g. [255, 0, 0, 128])
            image: Optional media store ID for an image representing this node role
            label: Optional human-readable label for this node role (defaults to 'key' if not provided)
            pin: Whether to pin this node role in the UI
            instance_kind: Optional instance kind for this entity category (e.g. 'neuron', 'synapse', 'behavior'). This is used for further categorization and filtering of entities within the graph.
            property_definitions: Property definitions
            definition: What this category *means*: a predicate over classification claims (RFC 0007). Omitted means primitive — membership is whatever was asserted under this word
            graph: The graph id this entity will belong to
            backfill: Draw the evidence this word already admits. Claims made under it before this category existed are in the organization's evidence base; with this on they are projected into the graph now, instead of waiting for the next reproject. Off by default because the work is proportional to the graph's evidence and happens before this mutation returns.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            EntityCategory"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["key"] = key
        if description is not UNSET:
            _input["description"] = description
        _input["ontologyReferences"] = ontology_references
        if color is not UNSET:
            _input["color"] = color
        if image is not UNSET:
            _input["image"] = image
        if label is not UNSET:
            _input["label"] = label
        if pin is not UNSET:
            _input["pin"] = pin
        if instance_kind is not UNSET:
            _input["instanceKind"] = instance_kind
        _input["propertyDefinitions"] = property_definitions
        if definition is not UNSET:
            _input["definition"] = definition
        _input["graph"] = graph
        _input["backfill"] = backfill
        variables["input"] = _input
        return (
            await self.aexecute(CreateEntityCategoryMutation, variables, task=task)
        ).create_entity_category

    def create_entity_category(
        self,
        key: str,
        ontology_references: Iterable[OntologyReferenceInput],
        property_definitions: Iterable[PropertyDefinitionInput],
        graph: str,
        backfill: bool,
        description: str | None | UnsetType = UNSET,
        color: Iterable[int] | None | UnsetType = UNSET,
        image: str | None | UnsetType = UNSET,
        label: str | None | UnsetType = UNSET,
        pin: bool | None | UnsetType = UNSET,
        instance_kind: str | None | UnsetType = UNSET,
        definition: CategoryDefinitionInput | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> EntityCategory:
        """CreateEntityCategory
         A Category is one view's rule for a word: what it means HERE, how it is drawn, and which
         properties are derived onto it. Creating one never records a claim.

        Args:
            key: The label of the node participating in the event
            description: Description of this node role
            ontology_references: Ontology references for this event
            color: Optional RGBA color for this node role (e.g. [255, 0, 0, 128])
            image: Optional media store ID for an image representing this node role
            label: Optional human-readable label for this node role (defaults to 'key' if not provided)
            pin: Whether to pin this node role in the UI
            instance_kind: Optional instance kind for this entity category (e.g. 'neuron', 'synapse', 'behavior'). This is used for further categorization and filtering of entities within the graph.
            property_definitions: Property definitions
            definition: What this category *means*: a predicate over classification claims (RFC 0007). Omitted means primitive — membership is whatever was asserted under this word
            graph: The graph id this entity will belong to
            backfill: Draw the evidence this word already admits. Claims made under it before this category existed are in the organization's evidence base; with this on they are projected into the graph now, instead of waiting for the next reproject. Off by default because the work is proportional to the graph's evidence and happens before this mutation returns.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            EntityCategory"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["key"] = key
        if description is not UNSET:
            _input["description"] = description
        _input["ontologyReferences"] = ontology_references
        if color is not UNSET:
            _input["color"] = color
        if image is not UNSET:
            _input["image"] = image
        if label is not UNSET:
            _input["label"] = label
        if pin is not UNSET:
            _input["pin"] = pin
        if instance_kind is not UNSET:
            _input["instanceKind"] = instance_kind
        _input["propertyDefinitions"] = property_definitions
        if definition is not UNSET:
            _input["definition"] = definition
        _input["graph"] = graph
        _input["backfill"] = backfill
        variables["input"] = _input
        return self.execute(
            CreateEntityCategoryMutation, variables, task=task
        ).create_entity_category

    async def aupdate_entity_category(
        self,
        id: IDCoercible,
        clear_definition: bool,
        key: str | None | UnsetType = UNSET,
        description: str | None | UnsetType = UNSET,
        ontology_references: Iterable[OntologyReferenceInput]
        | None
        | UnsetType = UNSET,
        color: Iterable[int] | None | UnsetType = UNSET,
        image: str | None | UnsetType = UNSET,
        label: str | None | UnsetType = UNSET,
        pin: bool | None | UnsetType = UNSET,
        instance_kind: str | None | UnsetType = UNSET,
        property_definitions: Iterable[PropertyDefinitionInput]
        | None
        | UnsetType = UNSET,
        definition: CategoryDefinitionInput | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> EntityCategory:
        """UpdateEntityCategory

        Update an existing entity category in the graph

        Args:
            id: The ID of the definition to update
            key: The label of the node participating in the event
            description: Description of this node role
            ontology_references: Ontology references for this event
            color: Optional RGBA color for this node role (e.g. [255, 0, 0, 128])
            image: Optional media store ID for an image representing this node role
            label: Optional human-readable label for this node role (defaults to 'key' if not provided)
            pin: Whether to pin this node role in the UI
            instance_kind: Optional instance kind for this entity category (e.g. 'neuron', 'synapse', 'behavior'). This is used for further categorization and filtering of entities within the graph.
            property_definitions: Property definitions
            definition: New meaning for this category (RFC 0007). Omitted means unchanged; to make the category primitive again, use clearDefinition
            clear_definition: Reset the category to primitive — membership becomes whatever was asserted under its word
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            EntityCategory"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        if key is not UNSET:
            _input["key"] = key
        if description is not UNSET:
            _input["description"] = description
        if ontology_references is not UNSET:
            _input["ontologyReferences"] = ontology_references
        if color is not UNSET:
            _input["color"] = color
        if image is not UNSET:
            _input["image"] = image
        if label is not UNSET:
            _input["label"] = label
        if pin is not UNSET:
            _input["pin"] = pin
        if instance_kind is not UNSET:
            _input["instanceKind"] = instance_kind
        if property_definitions is not UNSET:
            _input["propertyDefinitions"] = property_definitions
        if definition is not UNSET:
            _input["definition"] = definition
        _input["clearDefinition"] = clear_definition
        variables["input"] = _input
        return (
            await self.aexecute(UpdateEntityCategoryMutation, variables, task=task)
        ).update_entity_category

    def update_entity_category(
        self,
        id: IDCoercible,
        clear_definition: bool,
        key: str | None | UnsetType = UNSET,
        description: str | None | UnsetType = UNSET,
        ontology_references: Iterable[OntologyReferenceInput]
        | None
        | UnsetType = UNSET,
        color: Iterable[int] | None | UnsetType = UNSET,
        image: str | None | UnsetType = UNSET,
        label: str | None | UnsetType = UNSET,
        pin: bool | None | UnsetType = UNSET,
        instance_kind: str | None | UnsetType = UNSET,
        property_definitions: Iterable[PropertyDefinitionInput]
        | None
        | UnsetType = UNSET,
        definition: CategoryDefinitionInput | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> EntityCategory:
        """UpdateEntityCategory

        Update an existing entity category in the graph

        Args:
            id: The ID of the definition to update
            key: The label of the node participating in the event
            description: Description of this node role
            ontology_references: Ontology references for this event
            color: Optional RGBA color for this node role (e.g. [255, 0, 0, 128])
            image: Optional media store ID for an image representing this node role
            label: Optional human-readable label for this node role (defaults to 'key' if not provided)
            pin: Whether to pin this node role in the UI
            instance_kind: Optional instance kind for this entity category (e.g. 'neuron', 'synapse', 'behavior'). This is used for further categorization and filtering of entities within the graph.
            property_definitions: Property definitions
            definition: New meaning for this category (RFC 0007). Omitted means unchanged; to make the category primitive again, use clearDefinition
            clear_definition: Reset the category to primitive — membership becomes whatever was asserted under its word
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            EntityCategory"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        if key is not UNSET:
            _input["key"] = key
        if description is not UNSET:
            _input["description"] = description
        if ontology_references is not UNSET:
            _input["ontologyReferences"] = ontology_references
        if color is not UNSET:
            _input["color"] = color
        if image is not UNSET:
            _input["image"] = image
        if label is not UNSET:
            _input["label"] = label
        if pin is not UNSET:
            _input["pin"] = pin
        if instance_kind is not UNSET:
            _input["instanceKind"] = instance_kind
        if property_definitions is not UNSET:
            _input["propertyDefinitions"] = property_definitions
        if definition is not UNSET:
            _input["definition"] = definition
        _input["clearDefinition"] = clear_definition
        variables["input"] = _input
        return self.execute(
            UpdateEntityCategoryMutation, variables, task=task
        ).update_entity_category

    async def adelete_entity_category(
        self, id: IDCoercible, task: TaskLike | None = None
    ) -> ID:
        """DeleteEntityCategory

        Delete an entity category from the graph

        Args:
            id: The ID of the structure category to delete
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            ID"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        variables["input"] = _input
        return (
            await self.aexecute(DeleteEntityCategoryMutation, variables, task=task)
        ).delete_entity_category

    def delete_entity_category(
        self, id: IDCoercible, task: TaskLike | None = None
    ) -> ID:
        """DeleteEntityCategory

        Delete an entity category from the graph

        Args:
            id: The ID of the structure category to delete
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            ID"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        variables["input"] = _input
        return self.execute(
            DeleteEntityCategoryMutation, variables, task=task
        ).delete_entity_category

    async def acreate_relation_category(
        self,
        key: str,
        ontology_references: Iterable[OntologyReferenceInput],
        property_definitions: Iterable[PropertyDefinitionInput],
        graph: str,
        backfill: bool,
        description: str | None | UnsetType = UNSET,
        color: Iterable[int] | None | UnsetType = UNSET,
        image: str | None | UnsetType = UNSET,
        label: str | None | UnsetType = UNSET,
        pin: bool | None | UnsetType = UNSET,
        instance_kind: str | None | UnsetType = UNSET,
        definition: CategoryDefinitionInput | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> RelationCategory:
        """CreateRelationCategory

        Create a new relation category in the graph

        Args:
            key: The label of the node participating in the event
            description: Description of this node role
            ontology_references: Ontology references for this event
            color: Optional RGBA color for this node role (e.g. [255, 0, 0, 128])
            image: Optional media store ID for an image representing this node role
            label: Optional human-readable label for this node role (defaults to 'key' if not provided)
            pin: Whether to pin this node role in the UI
            instance_kind: Optional instance kind for this entity category (e.g. 'neuron', 'synapse', 'behavior'). This is used for further categorization and filtering of entities within the graph.
            property_definitions: Property definitions
            definition: What this category *means*: a predicate over classification claims (RFC 0007). Omitted means primitive — membership is whatever was asserted under this word
            graph: The graph id this entity will belong to
            backfill: Draw the evidence this word already admits. Claims made under it before this category existed are in the organization's evidence base; with this on they are projected into the graph now, instead of waiting for the next reproject. Off by default because the work is proportional to the graph's evidence and happens before this mutation returns.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            RelationCategory"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["key"] = key
        if description is not UNSET:
            _input["description"] = description
        _input["ontologyReferences"] = ontology_references
        if color is not UNSET:
            _input["color"] = color
        if image is not UNSET:
            _input["image"] = image
        if label is not UNSET:
            _input["label"] = label
        if pin is not UNSET:
            _input["pin"] = pin
        if instance_kind is not UNSET:
            _input["instanceKind"] = instance_kind
        _input["propertyDefinitions"] = property_definitions
        if definition is not UNSET:
            _input["definition"] = definition
        _input["graph"] = graph
        _input["backfill"] = backfill
        variables["input"] = _input
        return (
            await self.aexecute(CreateRelationCategoryMutation, variables, task=task)
        ).create_relation_category

    def create_relation_category(
        self,
        key: str,
        ontology_references: Iterable[OntologyReferenceInput],
        property_definitions: Iterable[PropertyDefinitionInput],
        graph: str,
        backfill: bool,
        description: str | None | UnsetType = UNSET,
        color: Iterable[int] | None | UnsetType = UNSET,
        image: str | None | UnsetType = UNSET,
        label: str | None | UnsetType = UNSET,
        pin: bool | None | UnsetType = UNSET,
        instance_kind: str | None | UnsetType = UNSET,
        definition: CategoryDefinitionInput | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> RelationCategory:
        """CreateRelationCategory

        Create a new relation category in the graph

        Args:
            key: The label of the node participating in the event
            description: Description of this node role
            ontology_references: Ontology references for this event
            color: Optional RGBA color for this node role (e.g. [255, 0, 0, 128])
            image: Optional media store ID for an image representing this node role
            label: Optional human-readable label for this node role (defaults to 'key' if not provided)
            pin: Whether to pin this node role in the UI
            instance_kind: Optional instance kind for this entity category (e.g. 'neuron', 'synapse', 'behavior'). This is used for further categorization and filtering of entities within the graph.
            property_definitions: Property definitions
            definition: What this category *means*: a predicate over classification claims (RFC 0007). Omitted means primitive — membership is whatever was asserted under this word
            graph: The graph id this entity will belong to
            backfill: Draw the evidence this word already admits. Claims made under it before this category existed are in the organization's evidence base; with this on they are projected into the graph now, instead of waiting for the next reproject. Off by default because the work is proportional to the graph's evidence and happens before this mutation returns.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            RelationCategory"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["key"] = key
        if description is not UNSET:
            _input["description"] = description
        _input["ontologyReferences"] = ontology_references
        if color is not UNSET:
            _input["color"] = color
        if image is not UNSET:
            _input["image"] = image
        if label is not UNSET:
            _input["label"] = label
        if pin is not UNSET:
            _input["pin"] = pin
        if instance_kind is not UNSET:
            _input["instanceKind"] = instance_kind
        _input["propertyDefinitions"] = property_definitions
        if definition is not UNSET:
            _input["definition"] = definition
        _input["graph"] = graph
        _input["backfill"] = backfill
        variables["input"] = _input
        return self.execute(
            CreateRelationCategoryMutation, variables, task=task
        ).create_relation_category

    async def aupdate_relation_category(
        self,
        id: str,
        clear_definition: bool,
        key: str | None | UnsetType = UNSET,
        description: str | None | UnsetType = UNSET,
        ontology_references: Iterable[OntologyReferenceInput]
        | None
        | UnsetType = UNSET,
        color: Iterable[int] | None | UnsetType = UNSET,
        image: str | None | UnsetType = UNSET,
        label: str | None | UnsetType = UNSET,
        pin: bool | None | UnsetType = UNSET,
        definition: CategoryDefinitionInput | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> RelationCategory:
        """UpdateRelationCategory

        Update an existing relation category in the graph

        Args:
            id: The ID of the relation category to update
            key: The label of the node participating in the event
            description: Description of this node role
            ontology_references: Ontology references for this event
            color: Optional RGBA color for this node role (e.g. [255, 0, 0, 128])
            image: Optional media store ID for an image representing this node role
            label: Optional human-readable label for this node role (defaults to 'key' if not provided)
            pin: Whether to pin this node role in the UI
            definition: New rule for this category (RFC 0009). Omitted means unchanged; to make it primitive again, use clearDefinition
            clear_definition: Reset the category to primitive — any claim naming its word counts, standings organization grain
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            RelationCategory"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        if key is not UNSET:
            _input["key"] = key
        if description is not UNSET:
            _input["description"] = description
        if ontology_references is not UNSET:
            _input["ontologyReferences"] = ontology_references
        if color is not UNSET:
            _input["color"] = color
        if image is not UNSET:
            _input["image"] = image
        if label is not UNSET:
            _input["label"] = label
        if pin is not UNSET:
            _input["pin"] = pin
        if definition is not UNSET:
            _input["definition"] = definition
        _input["clearDefinition"] = clear_definition
        variables["input"] = _input
        return (
            await self.aexecute(UpdateRelationCategoryMutation, variables, task=task)
        ).update_relation_category

    def update_relation_category(
        self,
        id: str,
        clear_definition: bool,
        key: str | None | UnsetType = UNSET,
        description: str | None | UnsetType = UNSET,
        ontology_references: Iterable[OntologyReferenceInput]
        | None
        | UnsetType = UNSET,
        color: Iterable[int] | None | UnsetType = UNSET,
        image: str | None | UnsetType = UNSET,
        label: str | None | UnsetType = UNSET,
        pin: bool | None | UnsetType = UNSET,
        definition: CategoryDefinitionInput | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> RelationCategory:
        """UpdateRelationCategory

        Update an existing relation category in the graph

        Args:
            id: The ID of the relation category to update
            key: The label of the node participating in the event
            description: Description of this node role
            ontology_references: Ontology references for this event
            color: Optional RGBA color for this node role (e.g. [255, 0, 0, 128])
            image: Optional media store ID for an image representing this node role
            label: Optional human-readable label for this node role (defaults to 'key' if not provided)
            pin: Whether to pin this node role in the UI
            definition: New rule for this category (RFC 0009). Omitted means unchanged; to make it primitive again, use clearDefinition
            clear_definition: Reset the category to primitive — any claim naming its word counts, standings organization grain
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            RelationCategory"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        if key is not UNSET:
            _input["key"] = key
        if description is not UNSET:
            _input["description"] = description
        if ontology_references is not UNSET:
            _input["ontologyReferences"] = ontology_references
        if color is not UNSET:
            _input["color"] = color
        if image is not UNSET:
            _input["image"] = image
        if label is not UNSET:
            _input["label"] = label
        if pin is not UNSET:
            _input["pin"] = pin
        if definition is not UNSET:
            _input["definition"] = definition
        _input["clearDefinition"] = clear_definition
        variables["input"] = _input
        return self.execute(
            UpdateRelationCategoryMutation, variables, task=task
        ).update_relation_category

    async def adelete_relation_category(
        self, id: str, task: TaskLike | None = None
    ) -> ID:
        """DeleteRelationCategory

        Delete a relation category from the graph

        Args:
            id: The ID of the relation category to delete
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            ID"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        variables["input"] = _input
        return (
            await self.aexecute(DeleteRelationCategoryMutation, variables, task=task)
        ).delete_relation_category

    def delete_relation_category(self, id: str, task: TaskLike | None = None) -> ID:
        """DeleteRelationCategory

        Delete a relation category from the graph

        Args:
            id: The ID of the relation category to delete
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            ID"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        variables["input"] = _input
        return self.execute(
            DeleteRelationCategoryMutation, variables, task=task
        ).delete_relation_category

    async def acreate_measurement_category(
        self,
        key: str,
        ontology_references: Iterable[OntologyReferenceInput],
        source: StructureDescriptorInput,
        target: EntityDescriptorInput,
        cardinality: Cardinality,
        properties: Iterable[PropertyDefinitionInput],
        graph: str,
        description: str | None | UnsetType = UNSET,
        color: Iterable[int] | None | UnsetType = UNSET,
        image: str | None | UnsetType = UNSET,
        label: str | None | UnsetType = UNSET,
        pin: bool | None | UnsetType = UNSET,
        definition: CategoryDefinitionInput | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> MeasurementCategory:
        """CreateMeasurementCategory

        Create a new measurement category in the graph

        Args:
            key: Relation type name/key
            description: Description of this node role
            ontology_references: Ontology references for this event
            color: Optional RGBA color for this node role (e.g. [255, 0, 0, 128])
            image: Optional media store ID for an image representing this node role
            label: Optional human-readable label for this node role (defaults to 'key' if not provided)
            pin: Whether to pin this node role in the UI
            source: Source entity type(s)
            target: Target entity type(s)
            cardinality: Relation cardinality
            properties: Derived property definitions
            definition: This measurement category's complete rule (RFC 0012): which measurement claims count and whose standings fold. Omitted means primitive
            graph: The graph id this measurement category will belong to
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            MeasurementCategory"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["key"] = key
        if description is not UNSET:
            _input["description"] = description
        _input["ontologyReferences"] = ontology_references
        if color is not UNSET:
            _input["color"] = color
        if image is not UNSET:
            _input["image"] = image
        if label is not UNSET:
            _input["label"] = label
        if pin is not UNSET:
            _input["pin"] = pin
        _input["source"] = source
        _input["target"] = target
        _input["cardinality"] = cardinality
        _input["properties"] = properties
        if definition is not UNSET:
            _input["definition"] = definition
        _input["graph"] = graph
        variables["input"] = _input
        return (
            await self.aexecute(CreateMeasurementCategoryMutation, variables, task=task)
        ).create_measurement_category

    def create_measurement_category(
        self,
        key: str,
        ontology_references: Iterable[OntologyReferenceInput],
        source: StructureDescriptorInput,
        target: EntityDescriptorInput,
        cardinality: Cardinality,
        properties: Iterable[PropertyDefinitionInput],
        graph: str,
        description: str | None | UnsetType = UNSET,
        color: Iterable[int] | None | UnsetType = UNSET,
        image: str | None | UnsetType = UNSET,
        label: str | None | UnsetType = UNSET,
        pin: bool | None | UnsetType = UNSET,
        definition: CategoryDefinitionInput | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> MeasurementCategory:
        """CreateMeasurementCategory

        Create a new measurement category in the graph

        Args:
            key: Relation type name/key
            description: Description of this node role
            ontology_references: Ontology references for this event
            color: Optional RGBA color for this node role (e.g. [255, 0, 0, 128])
            image: Optional media store ID for an image representing this node role
            label: Optional human-readable label for this node role (defaults to 'key' if not provided)
            pin: Whether to pin this node role in the UI
            source: Source entity type(s)
            target: Target entity type(s)
            cardinality: Relation cardinality
            properties: Derived property definitions
            definition: This measurement category's complete rule (RFC 0012): which measurement claims count and whose standings fold. Omitted means primitive
            graph: The graph id this measurement category will belong to
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            MeasurementCategory"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["key"] = key
        if description is not UNSET:
            _input["description"] = description
        _input["ontologyReferences"] = ontology_references
        if color is not UNSET:
            _input["color"] = color
        if image is not UNSET:
            _input["image"] = image
        if label is not UNSET:
            _input["label"] = label
        if pin is not UNSET:
            _input["pin"] = pin
        _input["source"] = source
        _input["target"] = target
        _input["cardinality"] = cardinality
        _input["properties"] = properties
        if definition is not UNSET:
            _input["definition"] = definition
        _input["graph"] = graph
        variables["input"] = _input
        return self.execute(
            CreateMeasurementCategoryMutation, variables, task=task
        ).create_measurement_category

    async def aupdate_measurement_category(
        self,
        id: str,
        clear_definition: bool,
        key: str | None | UnsetType = UNSET,
        description: str | None | UnsetType = UNSET,
        ontology_references: Iterable[OntologyReferenceInput]
        | None
        | UnsetType = UNSET,
        color: Iterable[int] | None | UnsetType = UNSET,
        image: str | None | UnsetType = UNSET,
        label: str | None | UnsetType = UNSET,
        pin: bool | None | UnsetType = UNSET,
        definition: CategoryDefinitionInput | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> MeasurementCategory:
        """UpdateMeasurementCategory

        Update an existing measurement category in the graph

        Args:
            id: The ID of the measurement category to update
            key: The label of the node participating in the event
            description: Description of this node role
            ontology_references: Ontology references for this event
            color: Optional RGBA color for this node role (e.g. [255, 0, 0, 128])
            image: Optional media store ID for an image representing this node role
            label: Optional human-readable label for this node role (defaults to 'key' if not provided)
            pin: Whether to pin this node role in the UI
            definition: New rule for this category (RFC 0012). Omitted means unchanged; to make it primitive again, use clearDefinition
            clear_definition: Reset the category to primitive — any claim naming its word counts, standings organization grain
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            MeasurementCategory"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        if key is not UNSET:
            _input["key"] = key
        if description is not UNSET:
            _input["description"] = description
        if ontology_references is not UNSET:
            _input["ontologyReferences"] = ontology_references
        if color is not UNSET:
            _input["color"] = color
        if image is not UNSET:
            _input["image"] = image
        if label is not UNSET:
            _input["label"] = label
        if pin is not UNSET:
            _input["pin"] = pin
        if definition is not UNSET:
            _input["definition"] = definition
        _input["clearDefinition"] = clear_definition
        variables["input"] = _input
        return (
            await self.aexecute(UpdateMeasurementCategoryMutation, variables, task=task)
        ).update_measurement_category

    def update_measurement_category(
        self,
        id: str,
        clear_definition: bool,
        key: str | None | UnsetType = UNSET,
        description: str | None | UnsetType = UNSET,
        ontology_references: Iterable[OntologyReferenceInput]
        | None
        | UnsetType = UNSET,
        color: Iterable[int] | None | UnsetType = UNSET,
        image: str | None | UnsetType = UNSET,
        label: str | None | UnsetType = UNSET,
        pin: bool | None | UnsetType = UNSET,
        definition: CategoryDefinitionInput | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> MeasurementCategory:
        """UpdateMeasurementCategory

        Update an existing measurement category in the graph

        Args:
            id: The ID of the measurement category to update
            key: The label of the node participating in the event
            description: Description of this node role
            ontology_references: Ontology references for this event
            color: Optional RGBA color for this node role (e.g. [255, 0, 0, 128])
            image: Optional media store ID for an image representing this node role
            label: Optional human-readable label for this node role (defaults to 'key' if not provided)
            pin: Whether to pin this node role in the UI
            definition: New rule for this category (RFC 0012). Omitted means unchanged; to make it primitive again, use clearDefinition
            clear_definition: Reset the category to primitive — any claim naming its word counts, standings organization grain
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            MeasurementCategory"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        if key is not UNSET:
            _input["key"] = key
        if description is not UNSET:
            _input["description"] = description
        if ontology_references is not UNSET:
            _input["ontologyReferences"] = ontology_references
        if color is not UNSET:
            _input["color"] = color
        if image is not UNSET:
            _input["image"] = image
        if label is not UNSET:
            _input["label"] = label
        if pin is not UNSET:
            _input["pin"] = pin
        if definition is not UNSET:
            _input["definition"] = definition
        _input["clearDefinition"] = clear_definition
        variables["input"] = _input
        return self.execute(
            UpdateMeasurementCategoryMutation, variables, task=task
        ).update_measurement_category

    async def adelete_measurement_category(
        self, id: str, task: TaskLike | None = None
    ) -> ID:
        """DeleteMeasurementCategory

        Delete a measurement category from the graph

        Args:
            id: The ID of the measurement category to delete
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            ID"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        variables["input"] = _input
        return (
            await self.aexecute(DeleteMeasurementCategoryMutation, variables, task=task)
        ).delete_measurement_category

    def delete_measurement_category(self, id: str, task: TaskLike | None = None) -> ID:
        """DeleteMeasurementCategory

        Delete a measurement category from the graph

        Args:
            id: The ID of the measurement category to delete
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            ID"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        variables["input"] = _input
        return self.execute(
            DeleteMeasurementCategoryMutation, variables, task=task
        ).delete_measurement_category

    async def acreate_structure_relation_category(
        self,
        key: str,
        ontology_references: Iterable[OntologyReferenceInput],
        properties: Iterable[PropertyDefinitionInput],
        source: StructureDescriptorInput,
        target: StructureDescriptorInput,
        cardinality: Cardinality,
        graph: str,
        description: str | None | UnsetType = UNSET,
        color: Iterable[int] | None | UnsetType = UNSET,
        image: str | None | UnsetType = UNSET,
        label: str | None | UnsetType = UNSET,
        pin: bool | None | UnsetType = UNSET,
        definition: CategoryDefinitionInput | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> StructureRelationCategory:
        """CreateStructureRelationCategory

        Create a new structure relation category in the graph

        Args:
            key: Relation type name/key
            description: Description of this node role
            ontology_references: Ontology references for this event
            color: Optional RGBA color for this node role (e.g. [255, 0, 0, 128])
            image: Optional media store ID for an image representing this node role
            label: Optional human-readable label for this node role (defaults to 'key' if not provided)
            pin: Whether to pin this node role in the UI
            properties: Derived property definitions
            source: Source entity type(s)
            target: Target entity type(s)
            cardinality: Relation cardinality
            definition: This structure-relation category's complete rule (RFC 0012): which structure-relation claims count — by word, annotator, app and window — and whose standings fold. Omitted means primitive
            graph: The graph id this entity will belong to
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            StructureRelationCategory"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["key"] = key
        if description is not UNSET:
            _input["description"] = description
        _input["ontologyReferences"] = ontology_references
        if color is not UNSET:
            _input["color"] = color
        if image is not UNSET:
            _input["image"] = image
        if label is not UNSET:
            _input["label"] = label
        if pin is not UNSET:
            _input["pin"] = pin
        _input["properties"] = properties
        _input["source"] = source
        _input["target"] = target
        _input["cardinality"] = cardinality
        if definition is not UNSET:
            _input["definition"] = definition
        _input["graph"] = graph
        variables["input"] = _input
        return (
            await self.aexecute(
                CreateStructureRelationCategoryMutation, variables, task=task
            )
        ).create_structure_relation_category

    def create_structure_relation_category(
        self,
        key: str,
        ontology_references: Iterable[OntologyReferenceInput],
        properties: Iterable[PropertyDefinitionInput],
        source: StructureDescriptorInput,
        target: StructureDescriptorInput,
        cardinality: Cardinality,
        graph: str,
        description: str | None | UnsetType = UNSET,
        color: Iterable[int] | None | UnsetType = UNSET,
        image: str | None | UnsetType = UNSET,
        label: str | None | UnsetType = UNSET,
        pin: bool | None | UnsetType = UNSET,
        definition: CategoryDefinitionInput | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> StructureRelationCategory:
        """CreateStructureRelationCategory

        Create a new structure relation category in the graph

        Args:
            key: Relation type name/key
            description: Description of this node role
            ontology_references: Ontology references for this event
            color: Optional RGBA color for this node role (e.g. [255, 0, 0, 128])
            image: Optional media store ID for an image representing this node role
            label: Optional human-readable label for this node role (defaults to 'key' if not provided)
            pin: Whether to pin this node role in the UI
            properties: Derived property definitions
            source: Source entity type(s)
            target: Target entity type(s)
            cardinality: Relation cardinality
            definition: This structure-relation category's complete rule (RFC 0012): which structure-relation claims count — by word, annotator, app and window — and whose standings fold. Omitted means primitive
            graph: The graph id this entity will belong to
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            StructureRelationCategory"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["key"] = key
        if description is not UNSET:
            _input["description"] = description
        _input["ontologyReferences"] = ontology_references
        if color is not UNSET:
            _input["color"] = color
        if image is not UNSET:
            _input["image"] = image
        if label is not UNSET:
            _input["label"] = label
        if pin is not UNSET:
            _input["pin"] = pin
        _input["properties"] = properties
        _input["source"] = source
        _input["target"] = target
        _input["cardinality"] = cardinality
        if definition is not UNSET:
            _input["definition"] = definition
        _input["graph"] = graph
        variables["input"] = _input
        return self.execute(
            CreateStructureRelationCategoryMutation, variables, task=task
        ).create_structure_relation_category

    async def aupdate_structure_relation_category(
        self,
        id: str,
        clear_definition: bool,
        key: str | None | UnsetType = UNSET,
        description: str | None | UnsetType = UNSET,
        ontology_references: Iterable[OntologyReferenceInput]
        | None
        | UnsetType = UNSET,
        color: Iterable[int] | None | UnsetType = UNSET,
        image: str | None | UnsetType = UNSET,
        label: str | None | UnsetType = UNSET,
        pin: bool | None | UnsetType = UNSET,
        definition: CategoryDefinitionInput | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> StructureRelationCategory:
        """UpdateStructureRelationCategory

        Update an existing structure relation category in the graph

        Args:
            id: The ID of the structure relation category to update
            key: The label of the node participating in the event
            description: Description of this node role
            ontology_references: Ontology references for this event
            color: Optional RGBA color for this node role (e.g. [255, 0, 0, 128])
            image: Optional media store ID for an image representing this node role
            label: Optional human-readable label for this node role (defaults to 'key' if not provided)
            pin: Whether to pin this node role in the UI
            definition: New rule for this category (RFC 0012). Omitted means unchanged; to make it primitive again, use clearDefinition
            clear_definition: Reset the category to primitive — any claim naming its word counts, standings organization grain
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            StructureRelationCategory"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        if key is not UNSET:
            _input["key"] = key
        if description is not UNSET:
            _input["description"] = description
        if ontology_references is not UNSET:
            _input["ontologyReferences"] = ontology_references
        if color is not UNSET:
            _input["color"] = color
        if image is not UNSET:
            _input["image"] = image
        if label is not UNSET:
            _input["label"] = label
        if pin is not UNSET:
            _input["pin"] = pin
        if definition is not UNSET:
            _input["definition"] = definition
        _input["clearDefinition"] = clear_definition
        variables["input"] = _input
        return (
            await self.aexecute(
                UpdateStructureRelationCategoryMutation, variables, task=task
            )
        ).update_structure_relation_category

    def update_structure_relation_category(
        self,
        id: str,
        clear_definition: bool,
        key: str | None | UnsetType = UNSET,
        description: str | None | UnsetType = UNSET,
        ontology_references: Iterable[OntologyReferenceInput]
        | None
        | UnsetType = UNSET,
        color: Iterable[int] | None | UnsetType = UNSET,
        image: str | None | UnsetType = UNSET,
        label: str | None | UnsetType = UNSET,
        pin: bool | None | UnsetType = UNSET,
        definition: CategoryDefinitionInput | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> StructureRelationCategory:
        """UpdateStructureRelationCategory

        Update an existing structure relation category in the graph

        Args:
            id: The ID of the structure relation category to update
            key: The label of the node participating in the event
            description: Description of this node role
            ontology_references: Ontology references for this event
            color: Optional RGBA color for this node role (e.g. [255, 0, 0, 128])
            image: Optional media store ID for an image representing this node role
            label: Optional human-readable label for this node role (defaults to 'key' if not provided)
            pin: Whether to pin this node role in the UI
            definition: New rule for this category (RFC 0012). Omitted means unchanged; to make it primitive again, use clearDefinition
            clear_definition: Reset the category to primitive — any claim naming its word counts, standings organization grain
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            StructureRelationCategory"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        if key is not UNSET:
            _input["key"] = key
        if description is not UNSET:
            _input["description"] = description
        if ontology_references is not UNSET:
            _input["ontologyReferences"] = ontology_references
        if color is not UNSET:
            _input["color"] = color
        if image is not UNSET:
            _input["image"] = image
        if label is not UNSET:
            _input["label"] = label
        if pin is not UNSET:
            _input["pin"] = pin
        if definition is not UNSET:
            _input["definition"] = definition
        _input["clearDefinition"] = clear_definition
        variables["input"] = _input
        return self.execute(
            UpdateStructureRelationCategoryMutation, variables, task=task
        ).update_structure_relation_category

    async def adelete_structure_relation_category(
        self, id: str, task: TaskLike | None = None
    ) -> ID:
        """DeleteStructureRelationCategory

        Delete a structure relation category from the graph

        Args:
            id: The ID of the structure relation category to delete
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            ID"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        variables["input"] = _input
        return (
            await self.aexecute(
                DeleteStructureRelationCategoryMutation, variables, task=task
            )
        ).delete_structure_relation_category

    def delete_structure_relation_category(
        self, id: str, task: TaskLike | None = None
    ) -> ID:
        """DeleteStructureRelationCategory

        Delete a structure relation category from the graph

        Args:
            id: The ID of the structure relation category to delete
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            ID"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        variables["input"] = _input
        return self.execute(
            DeleteStructureRelationCategoryMutation, variables, task=task
        ).delete_structure_relation_category

    async def acreate_natural_event_category(
        self,
        key: str,
        ontology_references: Iterable[OntologyReferenceInput],
        kind: EventKind,
        inputs: Iterable[EventRoleInput],
        outputs: Iterable[EventRoleInput],
        properties: Iterable[PropertyDefinitionInput],
        graph: str,
        backfill: bool,
        description: str | None | UnsetType = UNSET,
        color: Iterable[int] | None | UnsetType = UNSET,
        image: str | None | UnsetType = UNSET,
        label: str | None | UnsetType = UNSET,
        pin: bool | None | UnsetType = UNSET,
        definition: CategoryDefinitionInput | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> NaturalEventCategory:
        """CreateNaturalEventCategory

        Create a new natural event category in the graph

        Args:
            key: The label of the node participating in the event
            description: Description of this node role
            ontology_references: Ontology references for this event
            color: Optional RGBA color for this node role (e.g. [255, 0, 0, 128])
            image: Optional media store ID for an image representing this node role
            label: Optional human-readable label for this node role (defaults to 'key' if not provided)
            pin: Whether to pin this node role in the UI
            kind: Whether the event arises in the system itself (INTRINSIC, e.g. mitosis) or is applied from outside (EXTRINSIC, e.g. a protocol step)
            inputs: Input node roles
            outputs: Output node roles
            properties: Property definitions
            definition: This event category's complete rule (RFC 0009): which classification claims admit an event, whose existence standings count, and whose participation claims draw its edges. Omitted means primitive
            graph: The graph id this event will belong to
            backfill: Draw the evidence this word already admits. Claims made under it before this category existed are in the organization's evidence base; with this on they are projected into the graph now, instead of waiting for the next reproject. Off by default because the work is proportional to the graph's evidence and happens before this mutation returns.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            NaturalEventCategory"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["key"] = key
        if description is not UNSET:
            _input["description"] = description
        _input["ontologyReferences"] = ontology_references
        if color is not UNSET:
            _input["color"] = color
        if image is not UNSET:
            _input["image"] = image
        if label is not UNSET:
            _input["label"] = label
        if pin is not UNSET:
            _input["pin"] = pin
        _input["kind"] = kind
        _input["inputs"] = inputs
        _input["outputs"] = outputs
        _input["properties"] = properties
        if definition is not UNSET:
            _input["definition"] = definition
        _input["graph"] = graph
        _input["backfill"] = backfill
        variables["input"] = _input
        return (
            await self.aexecute(
                CreateNaturalEventCategoryMutation, variables, task=task
            )
        ).create_natural_event_category

    def create_natural_event_category(
        self,
        key: str,
        ontology_references: Iterable[OntologyReferenceInput],
        kind: EventKind,
        inputs: Iterable[EventRoleInput],
        outputs: Iterable[EventRoleInput],
        properties: Iterable[PropertyDefinitionInput],
        graph: str,
        backfill: bool,
        description: str | None | UnsetType = UNSET,
        color: Iterable[int] | None | UnsetType = UNSET,
        image: str | None | UnsetType = UNSET,
        label: str | None | UnsetType = UNSET,
        pin: bool | None | UnsetType = UNSET,
        definition: CategoryDefinitionInput | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> NaturalEventCategory:
        """CreateNaturalEventCategory

        Create a new natural event category in the graph

        Args:
            key: The label of the node participating in the event
            description: Description of this node role
            ontology_references: Ontology references for this event
            color: Optional RGBA color for this node role (e.g. [255, 0, 0, 128])
            image: Optional media store ID for an image representing this node role
            label: Optional human-readable label for this node role (defaults to 'key' if not provided)
            pin: Whether to pin this node role in the UI
            kind: Whether the event arises in the system itself (INTRINSIC, e.g. mitosis) or is applied from outside (EXTRINSIC, e.g. a protocol step)
            inputs: Input node roles
            outputs: Output node roles
            properties: Property definitions
            definition: This event category's complete rule (RFC 0009): which classification claims admit an event, whose existence standings count, and whose participation claims draw its edges. Omitted means primitive
            graph: The graph id this event will belong to
            backfill: Draw the evidence this word already admits. Claims made under it before this category existed are in the organization's evidence base; with this on they are projected into the graph now, instead of waiting for the next reproject. Off by default because the work is proportional to the graph's evidence and happens before this mutation returns.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            NaturalEventCategory"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["key"] = key
        if description is not UNSET:
            _input["description"] = description
        _input["ontologyReferences"] = ontology_references
        if color is not UNSET:
            _input["color"] = color
        if image is not UNSET:
            _input["image"] = image
        if label is not UNSET:
            _input["label"] = label
        if pin is not UNSET:
            _input["pin"] = pin
        _input["kind"] = kind
        _input["inputs"] = inputs
        _input["outputs"] = outputs
        _input["properties"] = properties
        if definition is not UNSET:
            _input["definition"] = definition
        _input["graph"] = graph
        _input["backfill"] = backfill
        variables["input"] = _input
        return self.execute(
            CreateNaturalEventCategoryMutation, variables, task=task
        ).create_natural_event_category

    async def aupdate_natural_event_category(
        self,
        id: str,
        clear_definition: bool,
        key: str | None | UnsetType = UNSET,
        description: str | None | UnsetType = UNSET,
        ontology_references: Iterable[OntologyReferenceInput]
        | None
        | UnsetType = UNSET,
        color: Iterable[int] | None | UnsetType = UNSET,
        image: str | None | UnsetType = UNSET,
        label: str | None | UnsetType = UNSET,
        pin: bool | None | UnsetType = UNSET,
        definition: CategoryDefinitionInput | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> NaturalEventCategory:
        """UpdateNaturalEventCategory

        Update an existing natural event category in the graph

        Args:
            id: The ID of the natural event category to update
            key: The label of the node participating in the event
            description: Description of this node role
            ontology_references: Ontology references for this event
            color: Optional RGBA color for this node role (e.g. [255, 0, 0, 128])
            image: Optional media store ID for an image representing this node role
            label: Optional human-readable label for this node role (defaults to 'key' if not provided)
            pin: Whether to pin this node role in the UI
            definition: New rule for this category (RFC 0009). Omitted means unchanged; to make it primitive again, use clearDefinition
            clear_definition: Reset the category to primitive — any claim naming its word counts, standings organization grain
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            NaturalEventCategory"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        if key is not UNSET:
            _input["key"] = key
        if description is not UNSET:
            _input["description"] = description
        if ontology_references is not UNSET:
            _input["ontologyReferences"] = ontology_references
        if color is not UNSET:
            _input["color"] = color
        if image is not UNSET:
            _input["image"] = image
        if label is not UNSET:
            _input["label"] = label
        if pin is not UNSET:
            _input["pin"] = pin
        if definition is not UNSET:
            _input["definition"] = definition
        _input["clearDefinition"] = clear_definition
        variables["input"] = _input
        return (
            await self.aexecute(
                UpdateNaturalEventCategoryMutation, variables, task=task
            )
        ).update_natural_event_category

    def update_natural_event_category(
        self,
        id: str,
        clear_definition: bool,
        key: str | None | UnsetType = UNSET,
        description: str | None | UnsetType = UNSET,
        ontology_references: Iterable[OntologyReferenceInput]
        | None
        | UnsetType = UNSET,
        color: Iterable[int] | None | UnsetType = UNSET,
        image: str | None | UnsetType = UNSET,
        label: str | None | UnsetType = UNSET,
        pin: bool | None | UnsetType = UNSET,
        definition: CategoryDefinitionInput | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> NaturalEventCategory:
        """UpdateNaturalEventCategory

        Update an existing natural event category in the graph

        Args:
            id: The ID of the natural event category to update
            key: The label of the node participating in the event
            description: Description of this node role
            ontology_references: Ontology references for this event
            color: Optional RGBA color for this node role (e.g. [255, 0, 0, 128])
            image: Optional media store ID for an image representing this node role
            label: Optional human-readable label for this node role (defaults to 'key' if not provided)
            pin: Whether to pin this node role in the UI
            definition: New rule for this category (RFC 0009). Omitted means unchanged; to make it primitive again, use clearDefinition
            clear_definition: Reset the category to primitive — any claim naming its word counts, standings organization grain
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            NaturalEventCategory"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        if key is not UNSET:
            _input["key"] = key
        if description is not UNSET:
            _input["description"] = description
        if ontology_references is not UNSET:
            _input["ontologyReferences"] = ontology_references
        if color is not UNSET:
            _input["color"] = color
        if image is not UNSET:
            _input["image"] = image
        if label is not UNSET:
            _input["label"] = label
        if pin is not UNSET:
            _input["pin"] = pin
        if definition is not UNSET:
            _input["definition"] = definition
        _input["clearDefinition"] = clear_definition
        variables["input"] = _input
        return self.execute(
            UpdateNaturalEventCategoryMutation, variables, task=task
        ).update_natural_event_category

    async def adelete_natural_event_category(
        self, id: str, task: TaskLike | None = None
    ) -> ID:
        """DeleteNaturalEventCategory

        Delete a natural event category from the graph

        Args:
            id: The ID of the event category to delete
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            ID"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        variables["input"] = _input
        return (
            await self.aexecute(
                DeleteNaturalEventCategoryMutation, variables, task=task
            )
        ).delete_natural_event_category

    def delete_natural_event_category(
        self, id: str, task: TaskLike | None = None
    ) -> ID:
        """DeleteNaturalEventCategory

        Delete a natural event category from the graph

        Args:
            id: The ID of the event category to delete
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            ID"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        variables["input"] = _input
        return self.execute(
            DeleteNaturalEventCategoryMutation, variables, task=task
        ).delete_natural_event_category

    async def acreate_protocol_event_category(
        self,
        key: str,
        ontology_references: Iterable[OntologyReferenceInput],
        kind: EventKind,
        inputs: Iterable[EventRoleInput],
        outputs: Iterable[EventRoleInput],
        properties: Iterable[PropertyDefinitionInput],
        protocol: str,
        graph: str,
        backfill: bool,
        description: str | None | UnsetType = UNSET,
        color: Iterable[int] | None | UnsetType = UNSET,
        image: str | None | UnsetType = UNSET,
        label: str | None | UnsetType = UNSET,
        pin: bool | None | UnsetType = UNSET,
        definition: CategoryDefinitionInput | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> ProtocolEventCategory:
        """CreateProtocolEventCategory

        Create a new protocol event category in the graph

        Args:
            key: The label of the node participating in the event
            description: Description of this node role
            ontology_references: Ontology references for this event
            color: Optional RGBA color for this node role (e.g. [255, 0, 0, 128])
            image: Optional media store ID for an image representing this node role
            label: Optional human-readable label for this node role (defaults to 'key' if not provided)
            pin: Whether to pin this node role in the UI
            kind: Whether the event arises in the system itself (INTRINSIC, e.g. mitosis) or is applied from outside (EXTRINSIC, e.g. a protocol step)
            inputs: Input node roles
            outputs: Output node roles
            properties: Property definitions
            definition: This event category's complete rule (RFC 0009): which classification claims admit an event, whose existence standings count, and whose participation claims draw its edges. Omitted means primitive
            protocol: The protocol this event definition belongs to
            graph: The graph id this event will belong to
            backfill: Draw the evidence this word already admits. Claims made under it before this category existed are in the organization's evidence base; with this on they are projected into the graph now, instead of waiting for the next reproject. Off by default because the work is proportional to the graph's evidence and happens before this mutation returns.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            ProtocolEventCategory"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["key"] = key
        if description is not UNSET:
            _input["description"] = description
        _input["ontologyReferences"] = ontology_references
        if color is not UNSET:
            _input["color"] = color
        if image is not UNSET:
            _input["image"] = image
        if label is not UNSET:
            _input["label"] = label
        if pin is not UNSET:
            _input["pin"] = pin
        _input["kind"] = kind
        _input["inputs"] = inputs
        _input["outputs"] = outputs
        _input["properties"] = properties
        if definition is not UNSET:
            _input["definition"] = definition
        _input["protocol"] = protocol
        _input["graph"] = graph
        _input["backfill"] = backfill
        variables["input"] = _input
        return (
            await self.aexecute(
                CreateProtocolEventCategoryMutation, variables, task=task
            )
        ).create_protocol_event_category

    def create_protocol_event_category(
        self,
        key: str,
        ontology_references: Iterable[OntologyReferenceInput],
        kind: EventKind,
        inputs: Iterable[EventRoleInput],
        outputs: Iterable[EventRoleInput],
        properties: Iterable[PropertyDefinitionInput],
        protocol: str,
        graph: str,
        backfill: bool,
        description: str | None | UnsetType = UNSET,
        color: Iterable[int] | None | UnsetType = UNSET,
        image: str | None | UnsetType = UNSET,
        label: str | None | UnsetType = UNSET,
        pin: bool | None | UnsetType = UNSET,
        definition: CategoryDefinitionInput | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> ProtocolEventCategory:
        """CreateProtocolEventCategory

        Create a new protocol event category in the graph

        Args:
            key: The label of the node participating in the event
            description: Description of this node role
            ontology_references: Ontology references for this event
            color: Optional RGBA color for this node role (e.g. [255, 0, 0, 128])
            image: Optional media store ID for an image representing this node role
            label: Optional human-readable label for this node role (defaults to 'key' if not provided)
            pin: Whether to pin this node role in the UI
            kind: Whether the event arises in the system itself (INTRINSIC, e.g. mitosis) or is applied from outside (EXTRINSIC, e.g. a protocol step)
            inputs: Input node roles
            outputs: Output node roles
            properties: Property definitions
            definition: This event category's complete rule (RFC 0009): which classification claims admit an event, whose existence standings count, and whose participation claims draw its edges. Omitted means primitive
            protocol: The protocol this event definition belongs to
            graph: The graph id this event will belong to
            backfill: Draw the evidence this word already admits. Claims made under it before this category existed are in the organization's evidence base; with this on they are projected into the graph now, instead of waiting for the next reproject. Off by default because the work is proportional to the graph's evidence and happens before this mutation returns.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            ProtocolEventCategory"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["key"] = key
        if description is not UNSET:
            _input["description"] = description
        _input["ontologyReferences"] = ontology_references
        if color is not UNSET:
            _input["color"] = color
        if image is not UNSET:
            _input["image"] = image
        if label is not UNSET:
            _input["label"] = label
        if pin is not UNSET:
            _input["pin"] = pin
        _input["kind"] = kind
        _input["inputs"] = inputs
        _input["outputs"] = outputs
        _input["properties"] = properties
        if definition is not UNSET:
            _input["definition"] = definition
        _input["protocol"] = protocol
        _input["graph"] = graph
        _input["backfill"] = backfill
        variables["input"] = _input
        return self.execute(
            CreateProtocolEventCategoryMutation, variables, task=task
        ).create_protocol_event_category

    async def aupdate_protocol_event_category(
        self,
        id: str,
        clear_definition: bool,
        key: str | None | UnsetType = UNSET,
        description: str | None | UnsetType = UNSET,
        ontology_references: Iterable[OntologyReferenceInput]
        | None
        | UnsetType = UNSET,
        color: Iterable[int] | None | UnsetType = UNSET,
        image: str | None | UnsetType = UNSET,
        label: str | None | UnsetType = UNSET,
        pin: bool | None | UnsetType = UNSET,
        definition: CategoryDefinitionInput | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> ProtocolEventCategory:
        """UpdateProtocolEventCategory

        Update an existing protocol event category in the graph

        Args:
            id: The ID of the protocol event category to update
            key: The label of the node participating in the event
            description: Description of this node role
            ontology_references: Ontology references for this event
            color: Optional RGBA color for this node role (e.g. [255, 0, 0, 128])
            image: Optional media store ID for an image representing this node role
            label: Optional human-readable label for this node role (defaults to 'key' if not provided)
            pin: Whether to pin this node role in the UI
            definition: New rule for this category (RFC 0012). Omitted means unchanged; to make it primitive again, use clearDefinition
            clear_definition: Reset the category to primitive — any claim naming its word counts, standings organization grain
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            ProtocolEventCategory"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        if key is not UNSET:
            _input["key"] = key
        if description is not UNSET:
            _input["description"] = description
        if ontology_references is not UNSET:
            _input["ontologyReferences"] = ontology_references
        if color is not UNSET:
            _input["color"] = color
        if image is not UNSET:
            _input["image"] = image
        if label is not UNSET:
            _input["label"] = label
        if pin is not UNSET:
            _input["pin"] = pin
        if definition is not UNSET:
            _input["definition"] = definition
        _input["clearDefinition"] = clear_definition
        variables["input"] = _input
        return (
            await self.aexecute(
                UpdateProtocolEventCategoryMutation, variables, task=task
            )
        ).update_protocol_event_category

    def update_protocol_event_category(
        self,
        id: str,
        clear_definition: bool,
        key: str | None | UnsetType = UNSET,
        description: str | None | UnsetType = UNSET,
        ontology_references: Iterable[OntologyReferenceInput]
        | None
        | UnsetType = UNSET,
        color: Iterable[int] | None | UnsetType = UNSET,
        image: str | None | UnsetType = UNSET,
        label: str | None | UnsetType = UNSET,
        pin: bool | None | UnsetType = UNSET,
        definition: CategoryDefinitionInput | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> ProtocolEventCategory:
        """UpdateProtocolEventCategory

        Update an existing protocol event category in the graph

        Args:
            id: The ID of the protocol event category to update
            key: The label of the node participating in the event
            description: Description of this node role
            ontology_references: Ontology references for this event
            color: Optional RGBA color for this node role (e.g. [255, 0, 0, 128])
            image: Optional media store ID for an image representing this node role
            label: Optional human-readable label for this node role (defaults to 'key' if not provided)
            pin: Whether to pin this node role in the UI
            definition: New rule for this category (RFC 0012). Omitted means unchanged; to make it primitive again, use clearDefinition
            clear_definition: Reset the category to primitive — any claim naming its word counts, standings organization grain
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            ProtocolEventCategory"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        if key is not UNSET:
            _input["key"] = key
        if description is not UNSET:
            _input["description"] = description
        if ontology_references is not UNSET:
            _input["ontologyReferences"] = ontology_references
        if color is not UNSET:
            _input["color"] = color
        if image is not UNSET:
            _input["image"] = image
        if label is not UNSET:
            _input["label"] = label
        if pin is not UNSET:
            _input["pin"] = pin
        if definition is not UNSET:
            _input["definition"] = definition
        _input["clearDefinition"] = clear_definition
        variables["input"] = _input
        return self.execute(
            UpdateProtocolEventCategoryMutation, variables, task=task
        ).update_protocol_event_category

    async def adelete_protocol_event_category(
        self, id: str, task: TaskLike | None = None
    ) -> ID:
        """DeleteProtocolEventCategory

        Delete a protocol event category from the graph

        Args:
            id: The ID of the event category to delete
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            ID"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        variables["input"] = _input
        return (
            await self.aexecute(
                DeleteProtocolEventCategoryMutation, variables, task=task
            )
        ).delete_protocol_event_category

    def delete_protocol_event_category(
        self, id: str, task: TaskLike | None = None
    ) -> ID:
        """DeleteProtocolEventCategory

        Delete a protocol event category from the graph

        Args:
            id: The ID of the event category to delete
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            ID"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        variables["input"] = _input
        return self.execute(
            DeleteProtocolEventCategoryMutation, variables, task=task
        ).delete_protocol_event_category

    async def aassert_entity_exists(
        self,
        term: str,
        supporting_evidence: Iterable[StructureReferenceInput],
        derived_from: Iterable[str],
        same_as: Iterable[str],
        observed_at: datetime | None | UnsetType = UNSET,
        confidence: float | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> AssertedEntity:
        """AssertEntityExists
         ---- existence: instances -----------------------------------------------------------------
         A write names a WORD (`term`), never a graph and never a category id.

        Args:
            term: The organization's word for what is being claimed — a term's `key`, e.g. 'AIS'. Not a category id and not a graph: a claim names a word, and every view that declares that word will hold what you write. The word is created if the organization has not used it before; a view that declares no category for it simply will not draw it.
            supporting_evidence: List of evidence structures with measurements
            observed_at: When the world was in this state — world time, the axis a scientist means by 'when'. Distinct from when it is claimed, which the assertion records; left unset, the two are equal. A point, not an interval: a duration is a metric.
            confidence: How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.
            derived_from: The claims this one came from — ids of instances, links, metrics or structures in your organization. Each is recorded as a DERIVED_FROM link under the same assertion as the claim itself, because "this, because of that" is one act (RFC 0017). Read back as `derivedFrom`; the cited claim lists it under `derivations`.
            same_as: Instances this new one is the same as. Saying "this is AIS 6" mints a fresh instance and claims it is the same as the one already known as AIS 6 — all under **one assertion**, because it is one act. Sameness is an equivalence with no primary, so which id you send is immaterial; entities only, never structures.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            AssertedEntity"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["term"] = term
        _input["supportingEvidence"] = supporting_evidence
        if observed_at is not UNSET:
            _input["observedAt"] = observed_at
        if confidence is not UNSET:
            _input["confidence"] = confidence
        _input["derivedFrom"] = derived_from
        _input["sameAs"] = same_as
        variables["input"] = _input
        return (
            await self.aexecute(AssertEntityExistsMutation, variables, task=task)
        ).assert_entity_exists

    def assert_entity_exists(
        self,
        term: str,
        supporting_evidence: Iterable[StructureReferenceInput],
        derived_from: Iterable[str],
        same_as: Iterable[str],
        observed_at: datetime | None | UnsetType = UNSET,
        confidence: float | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> AssertedEntity:
        """AssertEntityExists
         ---- existence: instances -----------------------------------------------------------------
         A write names a WORD (`term`), never a graph and never a category id.

        Args:
            term: The organization's word for what is being claimed — a term's `key`, e.g. 'AIS'. Not a category id and not a graph: a claim names a word, and every view that declares that word will hold what you write. The word is created if the organization has not used it before; a view that declares no category for it simply will not draw it.
            supporting_evidence: List of evidence structures with measurements
            observed_at: When the world was in this state — world time, the axis a scientist means by 'when'. Distinct from when it is claimed, which the assertion records; left unset, the two are equal. A point, not an interval: a duration is a metric.
            confidence: How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.
            derived_from: The claims this one came from — ids of instances, links, metrics or structures in your organization. Each is recorded as a DERIVED_FROM link under the same assertion as the claim itself, because "this, because of that" is one act (RFC 0017). Read back as `derivedFrom`; the cited claim lists it under `derivations`.
            same_as: Instances this new one is the same as. Saying "this is AIS 6" mints a fresh instance and claims it is the same as the one already known as AIS 6 — all under **one assertion**, because it is one act. Sameness is an equivalence with no primary, so which id you send is immaterial; entities only, never structures.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            AssertedEntity"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["term"] = term
        _input["supportingEvidence"] = supporting_evidence
        if observed_at is not UNSET:
            _input["observedAt"] = observed_at
        if confidence is not UNSET:
            _input["confidence"] = confidence
        _input["derivedFrom"] = derived_from
        _input["sameAs"] = same_as
        variables["input"] = _input
        return self.execute(
            AssertEntityExistsMutation, variables, task=task
        ).assert_entity_exists

    async def aassert_natural_event_exists(
        self,
        term: str,
        inputs: Iterable[RoleMappingInput],
        outputs: Iterable[RoleMappingInput],
        supporting_evidence: Iterable[StructureReferenceInput],
        derived_from: Iterable[str],
        observed_at: datetime | None | UnsetType = UNSET,
        confidence: float | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> AssertedNaturalEvent:
        """AssertNaturalEventExists

        Claim that a natural event happened, under one of the organization's words

        Args:
            term: The organization's word for what is being claimed — a term's `key`, e.g. 'AIS'. Not a category id and not a graph: a claim names a word, and every view that declares that word will hold what you write. The word is created if the organization has not used it before; a view that declares no category for it simply will not draw it.
            inputs: List of entity IDs that are inputs to this event
            outputs: List of entity IDs that are outputs of this event
            supporting_evidence: List of evidence structures with measurements
            observed_at: When the world was in this state — world time, the axis a scientist means by 'when'. Distinct from when it is claimed, which the assertion records; left unset, the two are equal. A point, not an interval: a duration is a metric.
            confidence: How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.
            derived_from: The claims this one came from — ids of instances, links, metrics or structures in your organization. Each is recorded as a DERIVED_FROM link under the same assertion as the claim itself, because "this, because of that" is one act (RFC 0017). Read back as `derivedFrom`; the cited claim lists it under `derivations`.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            AssertedNaturalEvent"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["term"] = term
        _input["inputs"] = inputs
        _input["outputs"] = outputs
        _input["supportingEvidence"] = supporting_evidence
        if observed_at is not UNSET:
            _input["observedAt"] = observed_at
        if confidence is not UNSET:
            _input["confidence"] = confidence
        _input["derivedFrom"] = derived_from
        variables["input"] = _input
        return (
            await self.aexecute(AssertNaturalEventExistsMutation, variables, task=task)
        ).assert_natural_event_exists

    def assert_natural_event_exists(
        self,
        term: str,
        inputs: Iterable[RoleMappingInput],
        outputs: Iterable[RoleMappingInput],
        supporting_evidence: Iterable[StructureReferenceInput],
        derived_from: Iterable[str],
        observed_at: datetime | None | UnsetType = UNSET,
        confidence: float | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> AssertedNaturalEvent:
        """AssertNaturalEventExists

        Claim that a natural event happened, under one of the organization's words

        Args:
            term: The organization's word for what is being claimed — a term's `key`, e.g. 'AIS'. Not a category id and not a graph: a claim names a word, and every view that declares that word will hold what you write. The word is created if the organization has not used it before; a view that declares no category for it simply will not draw it.
            inputs: List of entity IDs that are inputs to this event
            outputs: List of entity IDs that are outputs of this event
            supporting_evidence: List of evidence structures with measurements
            observed_at: When the world was in this state — world time, the axis a scientist means by 'when'. Distinct from when it is claimed, which the assertion records; left unset, the two are equal. A point, not an interval: a duration is a metric.
            confidence: How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.
            derived_from: The claims this one came from — ids of instances, links, metrics or structures in your organization. Each is recorded as a DERIVED_FROM link under the same assertion as the claim itself, because "this, because of that" is one act (RFC 0017). Read back as `derivedFrom`; the cited claim lists it under `derivations`.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            AssertedNaturalEvent"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["term"] = term
        _input["inputs"] = inputs
        _input["outputs"] = outputs
        _input["supportingEvidence"] = supporting_evidence
        if observed_at is not UNSET:
            _input["observedAt"] = observed_at
        if confidence is not UNSET:
            _input["confidence"] = confidence
        _input["derivedFrom"] = derived_from
        variables["input"] = _input
        return self.execute(
            AssertNaturalEventExistsMutation, variables, task=task
        ).assert_natural_event_exists

    async def aassert_protocol_event_exists(
        self,
        term: str,
        inputs: Iterable[RoleMappingInput],
        outputs: Iterable[RoleMappingInput],
        supporting_evidence: Iterable[StructureReferenceInput],
        derived_from: Iterable[str],
        observed_at: datetime | None | UnsetType = UNSET,
        confidence: float | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> AssertedProtocolEvent:
        """AssertProtocolEventExists

        Claim that a protocol step happened, under one of the organization's words

        Args:
            term: The organization's word for what is being claimed — a term's `key`, e.g. 'AIS'. Not a category id and not a graph: a claim names a word, and every view that declares that word will hold what you write. The word is created if the organization has not used it before; a view that declares no category for it simply will not draw it.
            inputs: List of entity IDs that are inputs to this event
            outputs: List of entity IDs that are outputs of this event
            supporting_evidence: List of evidence structures with measurements
            observed_at: When the world was in this state — world time, the axis a scientist means by 'when'. Distinct from when it is claimed, which the assertion records; left unset, the two are equal. A point, not an interval: a duration is a metric.
            confidence: How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.
            derived_from: The claims this one came from — ids of instances, links, metrics or structures in your organization. Each is recorded as a DERIVED_FROM link under the same assertion as the claim itself, because "this, because of that" is one act (RFC 0017). Read back as `derivedFrom`; the cited claim lists it under `derivations`.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            AssertedProtocolEvent"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["term"] = term
        _input["inputs"] = inputs
        _input["outputs"] = outputs
        _input["supportingEvidence"] = supporting_evidence
        if observed_at is not UNSET:
            _input["observedAt"] = observed_at
        if confidence is not UNSET:
            _input["confidence"] = confidence
        _input["derivedFrom"] = derived_from
        variables["input"] = _input
        return (
            await self.aexecute(AssertProtocolEventExistsMutation, variables, task=task)
        ).assert_protocol_event_exists

    def assert_protocol_event_exists(
        self,
        term: str,
        inputs: Iterable[RoleMappingInput],
        outputs: Iterable[RoleMappingInput],
        supporting_evidence: Iterable[StructureReferenceInput],
        derived_from: Iterable[str],
        observed_at: datetime | None | UnsetType = UNSET,
        confidence: float | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> AssertedProtocolEvent:
        """AssertProtocolEventExists

        Claim that a protocol step happened, under one of the organization's words

        Args:
            term: The organization's word for what is being claimed — a term's `key`, e.g. 'AIS'. Not a category id and not a graph: a claim names a word, and every view that declares that word will hold what you write. The word is created if the organization has not used it before; a view that declares no category for it simply will not draw it.
            inputs: List of entity IDs that are inputs to this event
            outputs: List of entity IDs that are outputs of this event
            supporting_evidence: List of evidence structures with measurements
            observed_at: When the world was in this state — world time, the axis a scientist means by 'when'. Distinct from when it is claimed, which the assertion records; left unset, the two are equal. A point, not an interval: a duration is a metric.
            confidence: How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.
            derived_from: The claims this one came from — ids of instances, links, metrics or structures in your organization. Each is recorded as a DERIVED_FROM link under the same assertion as the claim itself, because "this, because of that" is one act (RFC 0017). Read back as `derivedFrom`; the cited claim lists it under `derivations`.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            AssertedProtocolEvent"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["term"] = term
        _input["inputs"] = inputs
        _input["outputs"] = outputs
        _input["supportingEvidence"] = supporting_evidence
        if observed_at is not UNSET:
            _input["observedAt"] = observed_at
        if confidence is not UNSET:
            _input["confidence"] = confidence
        _input["derivedFrom"] = derived_from
        variables["input"] = _input
        return self.execute(
            AssertProtocolEventExistsMutation, variables, task=task
        ).assert_protocol_event_exists

    async def aclassify_nodes(
        self,
        classifications: Iterable[ClassificationInput],
        task: TaskLike | None = None,
    ) -> AssertedInstances:
        """ClassifyNodes
         One assertion over many (node, term) pairs — a batch is one act.

        Args:
            classifications: The claims to record
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            AssertedInstances"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["classifications"] = classifications
        variables["input"] = _input
        return (
            await self.aexecute(ClassifyNodesMutation, variables, task=task)
        ).classify_nodes

    def classify_nodes(
        self,
        classifications: Iterable[ClassificationInput],
        task: TaskLike | None = None,
    ) -> AssertedInstances:
        """ClassifyNodes
         One assertion over many (node, term) pairs — a batch is one act.

        Args:
            classifications: The claims to record
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            AssertedInstances"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["classifications"] = classifications
        variables["input"] = _input
        return self.execute(ClassifyNodesMutation, variables, task=task).classify_nodes

    async def aassert_same_instance(
        self,
        instances: Iterable[str],
        derived_from: Iterable[str],
        observed_at: datetime | None | UnsetType = UNSET,
        confidence: float | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> AssertedSameness:
        """AssertSameInstance

        Claim that several already-recorded instances are one thing. An equivalence with no primary — the order of the ids carries no meaning

        Args:
            instances: Two or more instance ids that name the same thing — entities or events alike. Every pair among them is claimed, under one assertion.
            observed_at: When the world was in this state — world time, the axis a scientist means by 'when'. Distinct from when it is claimed, which the assertion records; left unset, the two are equal. A point, not an interval: a duration is a metric.
            confidence: How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.
            derived_from: The claims this one came from — ids of instances, links, metrics or structures in your organization. Each is recorded as a DERIVED_FROM link under the same assertion as the claim itself, because "this, because of that" is one act (RFC 0017). Read back as `derivedFrom`; the cited claim lists it under `derivations`.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            AssertedSameness"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["instances"] = instances
        if observed_at is not UNSET:
            _input["observedAt"] = observed_at
        if confidence is not UNSET:
            _input["confidence"] = confidence
        _input["derivedFrom"] = derived_from
        variables["input"] = _input
        return (
            await self.aexecute(AssertSameInstanceMutation, variables, task=task)
        ).assert_same_instance

    def assert_same_instance(
        self,
        instances: Iterable[str],
        derived_from: Iterable[str],
        observed_at: datetime | None | UnsetType = UNSET,
        confidence: float | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> AssertedSameness:
        """AssertSameInstance

        Claim that several already-recorded instances are one thing. An equivalence with no primary — the order of the ids carries no meaning

        Args:
            instances: Two or more instance ids that name the same thing — entities or events alike. Every pair among them is claimed, under one assertion.
            observed_at: When the world was in this state — world time, the axis a scientist means by 'when'. Distinct from when it is claimed, which the assertion records; left unset, the two are equal. A point, not an interval: a duration is a metric.
            confidence: How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.
            derived_from: The claims this one came from — ids of instances, links, metrics or structures in your organization. Each is recorded as a DERIVED_FROM link under the same assertion as the claim itself, because "this, because of that" is one act (RFC 0017). Read back as `derivedFrom`; the cited claim lists it under `derivations`.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            AssertedSameness"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["instances"] = instances
        if observed_at is not UNSET:
            _input["observedAt"] = observed_at
        if confidence is not UNSET:
            _input["confidence"] = confidence
        _input["derivedFrom"] = derived_from
        variables["input"] = _input
        return self.execute(
            AssertSameInstanceMutation, variables, task=task
        ).assert_same_instance

    async def aassert_structure_exists(
        self,
        object: str,
        metrics: Iterable[MetricInput],
        derived_from: Iterable[str],
        identifier: str,
        observed_at: datetime | None | UnsetType = UNSET,
        confidence: float | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> AssertedStructure:
        """AssertStructureExists
         ---- structures and metrics ---------------------------------------------------------------

        Args:
            object: The unique ID of the object this structure references
            metrics: List of measurements associated with this structure
            derived_from: The claims this one came from — ids of instances, links, metrics or structures in your organization. Each is recorded as a DERIVED_FROM link under the same assertion as the claim itself, because "this, because of that" is one act (RFC 0017). Read back as `derivedFrom`; the cited claim lists it under `derivations`.
            identifier: The structure identifier, e.g. '@mikro/roi'
            observed_at: When the world was in this state — world time, the axis a scientist means by 'when'. Distinct from when it is claimed, which the assertion records; left unset, the two are equal. A point, not an interval: a duration is a metric.
            confidence: How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            AssertedStructure"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["object"] = object
        _input["metrics"] = metrics
        _input["derivedFrom"] = derived_from
        _input["identifier"] = identifier
        if observed_at is not UNSET:
            _input["observedAt"] = observed_at
        if confidence is not UNSET:
            _input["confidence"] = confidence
        variables["input"] = _input
        return (
            await self.aexecute(AssertStructureExistsMutation, variables, task=task)
        ).assert_structure_exists

    def assert_structure_exists(
        self,
        object: str,
        metrics: Iterable[MetricInput],
        derived_from: Iterable[str],
        identifier: str,
        observed_at: datetime | None | UnsetType = UNSET,
        confidence: float | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> AssertedStructure:
        """AssertStructureExists
         ---- structures and metrics ---------------------------------------------------------------

        Args:
            object: The unique ID of the object this structure references
            metrics: List of measurements associated with this structure
            derived_from: The claims this one came from — ids of instances, links, metrics or structures in your organization. Each is recorded as a DERIVED_FROM link under the same assertion as the claim itself, because "this, because of that" is one act (RFC 0017). Read back as `derivedFrom`; the cited claim lists it under `derivations`.
            identifier: The structure identifier, e.g. '@mikro/roi'
            observed_at: When the world was in this state — world time, the axis a scientist means by 'when'. Distinct from when it is claimed, which the assertion records; left unset, the two are equal. A point, not an interval: a duration is a metric.
            confidence: How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            AssertedStructure"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["object"] = object
        _input["metrics"] = metrics
        _input["derivedFrom"] = derived_from
        _input["identifier"] = identifier
        if observed_at is not UNSET:
            _input["observedAt"] = observed_at
        if confidence is not UNSET:
            _input["confidence"] = confidence
        variables["input"] = _input
        return self.execute(
            AssertStructureExistsMutation, variables, task=task
        ).assert_structure_exists

    async def aassert_metric_value(
        self,
        key: str,
        value: Any,
        value_kind: PropertyType,
        derived_from: Iterable[str],
        identifier: str,
        object: str,
        confidence: float | None | UnsetType = UNSET,
        confidence_type: str | None | UnsetType = UNSET,
        unit: str | None | UnsetType = UNSET,
        observed_at: datetime | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> AssertedMetric:
        """AssertMetricValue

        Record a measurement, creating the structure it describes if this is its first sight. One assertion covers both

        Args:
            key: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
            value: The `AnyScalar` scalar type represents an arbitrary JSON-like value (required)
            value_kind: What type of value this is. Required: it decides which column the value is stored in and which measurement term it is recorded under, and nothing infers it. Two callers may declare the same key differently — a float `confidence` and a category-label `confidence` are two terms, and both are recorded.
            confidence: How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.
            confidence_type: What kind of number `confidence` is — a method's own score, a p-value. Measurement-only
            unit: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
            observed_at: When the world was observed. Defaults to when it was claimed.
            derived_from: The claims this one came from — ids of instances, links, metrics or structures in your organization. Each is recorded as a DERIVED_FROM link under the same assertion as the claim itself, because "this, because of that" is one act (RFC 0017). Read back as `derivedFrom`; the cited claim lists it under `derivations`.
            identifier: The schema identifier for this metric (e.g. '@mikro/roi_volume')
            object: The unique ID of the object this metric references
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            AssertedMetric"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["key"] = key
        _input["value"] = value
        _input["valueKind"] = value_kind
        if confidence is not UNSET:
            _input["confidence"] = confidence
        if confidence_type is not UNSET:
            _input["confidenceType"] = confidence_type
        if unit is not UNSET:
            _input["unit"] = unit
        if observed_at is not UNSET:
            _input["observedAt"] = observed_at
        _input["derivedFrom"] = derived_from
        _input["identifier"] = identifier
        _input["object"] = object
        variables["input"] = _input
        return (
            await self.aexecute(AssertMetricValueMutation, variables, task=task)
        ).assert_metric_value

    def assert_metric_value(
        self,
        key: str,
        value: Any,
        value_kind: PropertyType,
        derived_from: Iterable[str],
        identifier: str,
        object: str,
        confidence: float | None | UnsetType = UNSET,
        confidence_type: str | None | UnsetType = UNSET,
        unit: str | None | UnsetType = UNSET,
        observed_at: datetime | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> AssertedMetric:
        """AssertMetricValue

        Record a measurement, creating the structure it describes if this is its first sight. One assertion covers both

        Args:
            key: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
            value: The `AnyScalar` scalar type represents an arbitrary JSON-like value (required)
            value_kind: What type of value this is. Required: it decides which column the value is stored in and which measurement term it is recorded under, and nothing infers it. Two callers may declare the same key differently — a float `confidence` and a category-label `confidence` are two terms, and both are recorded.
            confidence: How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.
            confidence_type: What kind of number `confidence` is — a method's own score, a p-value. Measurement-only
            unit: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
            observed_at: When the world was observed. Defaults to when it was claimed.
            derived_from: The claims this one came from — ids of instances, links, metrics or structures in your organization. Each is recorded as a DERIVED_FROM link under the same assertion as the claim itself, because "this, because of that" is one act (RFC 0017). Read back as `derivedFrom`; the cited claim lists it under `derivations`.
            identifier: The schema identifier for this metric (e.g. '@mikro/roi_volume')
            object: The unique ID of the object this metric references
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            AssertedMetric"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["key"] = key
        _input["value"] = value
        _input["valueKind"] = value_kind
        if confidence is not UNSET:
            _input["confidence"] = confidence
        if confidence_type is not UNSET:
            _input["confidenceType"] = confidence_type
        if unit is not UNSET:
            _input["unit"] = unit
        if observed_at is not UNSET:
            _input["observedAt"] = observed_at
        _input["derivedFrom"] = derived_from
        _input["identifier"] = identifier
        _input["object"] = object
        variables["input"] = _input
        return self.execute(
            AssertMetricValueMutation, variables, task=task
        ).assert_metric_value

    async def aassert_metric_value_for_structure(
        self,
        key: str,
        value: Any,
        value_kind: PropertyType,
        derived_from: Iterable[str],
        structure: IDCoercible,
        confidence: float | None | UnsetType = UNSET,
        confidence_type: str | None | UnsetType = UNSET,
        unit: str | None | UnsetType = UNSET,
        observed_at: datetime | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> AssertedMetric:
        """AssertMetricValueForStructure

        Record a measurement against a structure that already exists, named by its evidence id

        Args:
            key: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
            value: The `AnyScalar` scalar type represents an arbitrary JSON-like value (required)
            value_kind: What type of value this is. Required: it decides which column the value is stored in and which measurement term it is recorded under, and nothing infers it. Two callers may declare the same key differently — a float `confidence` and a category-label `confidence` are two terms, and both are recorded.
            confidence: How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.
            confidence_type: What kind of number `confidence` is — a method's own score, a p-value. Measurement-only
            unit: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
            observed_at: When the world was observed. Defaults to when it was claimed.
            derived_from: The claims this one came from — ids of instances, links, metrics or structures in your organization. Each is recorded as a DERIVED_FROM link under the same assertion as the claim itself, because "this, because of that" is one act (RFC 0017). Read back as `derivedFrom`; the cited claim lists it under `derivations`.
            structure: The unique ID of the structure this metric is associated with
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            AssertedMetric"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["key"] = key
        _input["value"] = value
        _input["valueKind"] = value_kind
        if confidence is not UNSET:
            _input["confidence"] = confidence
        if confidence_type is not UNSET:
            _input["confidenceType"] = confidence_type
        if unit is not UNSET:
            _input["unit"] = unit
        if observed_at is not UNSET:
            _input["observedAt"] = observed_at
        _input["derivedFrom"] = derived_from
        _input["structure"] = structure
        variables["input"] = _input
        return (
            await self.aexecute(
                AssertMetricValueForStructureMutation, variables, task=task
            )
        ).assert_metric_value_for_structure

    def assert_metric_value_for_structure(
        self,
        key: str,
        value: Any,
        value_kind: PropertyType,
        derived_from: Iterable[str],
        structure: IDCoercible,
        confidence: float | None | UnsetType = UNSET,
        confidence_type: str | None | UnsetType = UNSET,
        unit: str | None | UnsetType = UNSET,
        observed_at: datetime | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> AssertedMetric:
        """AssertMetricValueForStructure

        Record a measurement against a structure that already exists, named by its evidence id

        Args:
            key: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
            value: The `AnyScalar` scalar type represents an arbitrary JSON-like value (required)
            value_kind: What type of value this is. Required: it decides which column the value is stored in and which measurement term it is recorded under, and nothing infers it. Two callers may declare the same key differently — a float `confidence` and a category-label `confidence` are two terms, and both are recorded.
            confidence: How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.
            confidence_type: What kind of number `confidence` is — a method's own score, a p-value. Measurement-only
            unit: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
            observed_at: When the world was observed. Defaults to when it was claimed.
            derived_from: The claims this one came from — ids of instances, links, metrics or structures in your organization. Each is recorded as a DERIVED_FROM link under the same assertion as the claim itself, because "this, because of that" is one act (RFC 0017). Read back as `derivedFrom`; the cited claim lists it under `derivations`.
            structure: The unique ID of the structure this metric is associated with
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            AssertedMetric"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["key"] = key
        _input["value"] = value
        _input["valueKind"] = value_kind
        if confidence is not UNSET:
            _input["confidence"] = confidence
        if confidence_type is not UNSET:
            _input["confidenceType"] = confidence_type
        if unit is not UNSET:
            _input["unit"] = unit
        if observed_at is not UNSET:
            _input["observedAt"] = observed_at
        _input["derivedFrom"] = derived_from
        _input["structure"] = structure
        variables["input"] = _input
        return self.execute(
            AssertMetricValueForStructureMutation, variables, task=task
        ).assert_metric_value_for_structure

    async def asupersede_metric_value(
        self,
        key: str,
        value: Any,
        value_kind: PropertyType,
        derived_from: Iterable[str],
        id: str,
        confidence: float | None | UnsetType = UNSET,
        confidence_type: str | None | UnsetType = UNSET,
        unit: str | None | UnsetType = UNSET,
        observed_at: datetime | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> AssertedMetric:
        """SupersedeMetricValue
         Retracting Standing + the new Metric under ONE assertion. Returns a metric with a NEW id.

        Args:
            key: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
            value: The `AnyScalar` scalar type represents an arbitrary JSON-like value (required)
            value_kind: What type of value this is. Required: it decides which column the value is stored in and which measurement term it is recorded under, and nothing infers it. Two callers may declare the same key differently — a float `confidence` and a category-label `confidence` are two terms, and both are recorded.
            confidence: How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.
            confidence_type: What kind of number `confidence` is — a method's own score, a p-value. Measurement-only
            unit: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
            observed_at: When the world was observed. Defaults to when it was claimed.
            derived_from: The claims this one came from — ids of instances, links, metrics or structures in your organization. Each is recorded as a DERIVED_FROM link under the same assertion as the claim itself, because "this, because of that" is one act (RFC 0017). Read back as `derivedFrom`; the cited claim lists it under `derivations`.
            id: The ID of the metric to update
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            AssertedMetric"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["key"] = key
        _input["value"] = value
        _input["valueKind"] = value_kind
        if confidence is not UNSET:
            _input["confidence"] = confidence
        if confidence_type is not UNSET:
            _input["confidenceType"] = confidence_type
        if unit is not UNSET:
            _input["unit"] = unit
        if observed_at is not UNSET:
            _input["observedAt"] = observed_at
        _input["derivedFrom"] = derived_from
        _input["id"] = id
        variables["input"] = _input
        return (
            await self.aexecute(SupersedeMetricValueMutation, variables, task=task)
        ).supersede_metric_value

    def supersede_metric_value(
        self,
        key: str,
        value: Any,
        value_kind: PropertyType,
        derived_from: Iterable[str],
        id: str,
        confidence: float | None | UnsetType = UNSET,
        confidence_type: str | None | UnsetType = UNSET,
        unit: str | None | UnsetType = UNSET,
        observed_at: datetime | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> AssertedMetric:
        """SupersedeMetricValue
         Retracting Standing + the new Metric under ONE assertion. Returns a metric with a NEW id.

        Args:
            key: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
            value: The `AnyScalar` scalar type represents an arbitrary JSON-like value (required)
            value_kind: What type of value this is. Required: it decides which column the value is stored in and which measurement term it is recorded under, and nothing infers it. Two callers may declare the same key differently — a float `confidence` and a category-label `confidence` are two terms, and both are recorded.
            confidence: How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.
            confidence_type: What kind of number `confidence` is — a method's own score, a p-value. Measurement-only
            unit: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
            observed_at: When the world was observed. Defaults to when it was claimed.
            derived_from: The claims this one came from — ids of instances, links, metrics or structures in your organization. Each is recorded as a DERIVED_FROM link under the same assertion as the claim itself, because "this, because of that" is one act (RFC 0017). Read back as `derivedFrom`; the cited claim lists it under `derivations`.
            id: The ID of the metric to update
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            AssertedMetric"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["key"] = key
        _input["value"] = value
        _input["valueKind"] = value_kind
        if confidence is not UNSET:
            _input["confidence"] = confidence
        if confidence_type is not UNSET:
            _input["confidenceType"] = confidence_type
        if unit is not UNSET:
            _input["unit"] = unit
        if observed_at is not UNSET:
            _input["observedAt"] = observed_at
        _input["derivedFrom"] = derived_from
        _input["id"] = id
        variables["input"] = _input
        return self.execute(
            SupersedeMetricValueMutation, variables, task=task
        ).supersede_metric_value

    async def aassert_relation_exists(
        self,
        source_id: str,
        target_id: str,
        supporting_evidence: Iterable[StructureReferenceInput],
        derived_from: Iterable[str],
        term: str,
        observed_at: datetime | None | UnsetType = UNSET,
        confidence: float | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> AssertedRelation:
        """AssertRelationExists
         ---- links ---------------------------------------------------------------------------------

        Args:
            source_id: The ID of the source entity/structure
            target_id: The ID of the target entity/structure
            supporting_evidence: List of evidence structures with measurements
            observed_at: When the world was in this state — world time, the axis a scientist means by 'when'. Distinct from when it is claimed, which the assertion records; left unset, the two are equal. A point, not an interval: a duration is a metric.
            confidence: How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.
            derived_from: The claims this one came from — ids of instances, links, metrics or structures in your organization. Each is recorded as a DERIVED_FROM link under the same assertion as the claim itself, because "this, because of that" is one act (RFC 0017). Read back as `derivedFrom`; the cited claim lists it under `derivations`.
            term: The organization's word for what is being claimed — a term's `key`, e.g. 'AIS'. Not a category id and not a graph: a claim names a word, and every view that declares that word will hold what you write. The word is created if the organization has not used it before; a view that declares no category for it simply will not draw it.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            AssertedRelation"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["sourceId"] = source_id
        _input["targetId"] = target_id
        _input["supportingEvidence"] = supporting_evidence
        if observed_at is not UNSET:
            _input["observedAt"] = observed_at
        if confidence is not UNSET:
            _input["confidence"] = confidence
        _input["derivedFrom"] = derived_from
        _input["term"] = term
        variables["input"] = _input
        return (
            await self.aexecute(AssertRelationExistsMutation, variables, task=task)
        ).assert_relation_exists

    def assert_relation_exists(
        self,
        source_id: str,
        target_id: str,
        supporting_evidence: Iterable[StructureReferenceInput],
        derived_from: Iterable[str],
        term: str,
        observed_at: datetime | None | UnsetType = UNSET,
        confidence: float | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> AssertedRelation:
        """AssertRelationExists
         ---- links ---------------------------------------------------------------------------------

        Args:
            source_id: The ID of the source entity/structure
            target_id: The ID of the target entity/structure
            supporting_evidence: List of evidence structures with measurements
            observed_at: When the world was in this state — world time, the axis a scientist means by 'when'. Distinct from when it is claimed, which the assertion records; left unset, the two are equal. A point, not an interval: a duration is a metric.
            confidence: How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.
            derived_from: The claims this one came from — ids of instances, links, metrics or structures in your organization. Each is recorded as a DERIVED_FROM link under the same assertion as the claim itself, because "this, because of that" is one act (RFC 0017). Read back as `derivedFrom`; the cited claim lists it under `derivations`.
            term: The organization's word for what is being claimed — a term's `key`, e.g. 'AIS'. Not a category id and not a graph: a claim names a word, and every view that declares that word will hold what you write. The word is created if the organization has not used it before; a view that declares no category for it simply will not draw it.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            AssertedRelation"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["sourceId"] = source_id
        _input["targetId"] = target_id
        _input["supportingEvidence"] = supporting_evidence
        if observed_at is not UNSET:
            _input["observedAt"] = observed_at
        if confidence is not UNSET:
            _input["confidence"] = confidence
        _input["derivedFrom"] = derived_from
        _input["term"] = term
        variables["input"] = _input
        return self.execute(
            AssertRelationExistsMutation, variables, task=task
        ).assert_relation_exists

    async def aassert_measurement_exists(
        self,
        source_id: str,
        target_id: str,
        supporting_evidence: Iterable[StructureReferenceInput],
        derived_from: Iterable[str],
        term: str,
        observed_at: datetime | None | UnsetType = UNSET,
        confidence: float | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> AssertedMeasurement:
        """AssertMeasurementExists

        Assert that a structure measures an entity, under one of the organization's words. Drawings are always empty: a measurement has no AGE edge

        Args:
            source_id: The ID of the source entity/structure
            target_id: The ID of the target entity/structure
            supporting_evidence: List of evidence structures with measurements
            observed_at: When the world was in this state — world time, the axis a scientist means by 'when'. Distinct from when it is claimed, which the assertion records; left unset, the two are equal. A point, not an interval: a duration is a metric.
            confidence: How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.
            derived_from: The claims this one came from — ids of instances, links, metrics or structures in your organization. Each is recorded as a DERIVED_FROM link under the same assertion as the claim itself, because "this, because of that" is one act (RFC 0017). Read back as `derivedFrom`; the cited claim lists it under `derivations`.
            term: The organization's word for what is being claimed — a term's `key`, e.g. 'AIS'. Not a category id and not a graph: a claim names a word, and every view that declares that word will hold what you write. The word is created if the organization has not used it before; a view that declares no category for it simply will not draw it.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            AssertedMeasurement"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["sourceId"] = source_id
        _input["targetId"] = target_id
        _input["supportingEvidence"] = supporting_evidence
        if observed_at is not UNSET:
            _input["observedAt"] = observed_at
        if confidence is not UNSET:
            _input["confidence"] = confidence
        _input["derivedFrom"] = derived_from
        _input["term"] = term
        variables["input"] = _input
        return (
            await self.aexecute(AssertMeasurementExistsMutation, variables, task=task)
        ).assert_measurement_exists

    def assert_measurement_exists(
        self,
        source_id: str,
        target_id: str,
        supporting_evidence: Iterable[StructureReferenceInput],
        derived_from: Iterable[str],
        term: str,
        observed_at: datetime | None | UnsetType = UNSET,
        confidence: float | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> AssertedMeasurement:
        """AssertMeasurementExists

        Assert that a structure measures an entity, under one of the organization's words. Drawings are always empty: a measurement has no AGE edge

        Args:
            source_id: The ID of the source entity/structure
            target_id: The ID of the target entity/structure
            supporting_evidence: List of evidence structures with measurements
            observed_at: When the world was in this state — world time, the axis a scientist means by 'when'. Distinct from when it is claimed, which the assertion records; left unset, the two are equal. A point, not an interval: a duration is a metric.
            confidence: How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.
            derived_from: The claims this one came from — ids of instances, links, metrics or structures in your organization. Each is recorded as a DERIVED_FROM link under the same assertion as the claim itself, because "this, because of that" is one act (RFC 0017). Read back as `derivedFrom`; the cited claim lists it under `derivations`.
            term: The organization's word for what is being claimed — a term's `key`, e.g. 'AIS'. Not a category id and not a graph: a claim names a word, and every view that declares that word will hold what you write. The word is created if the organization has not used it before; a view that declares no category for it simply will not draw it.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            AssertedMeasurement"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["sourceId"] = source_id
        _input["targetId"] = target_id
        _input["supportingEvidence"] = supporting_evidence
        if observed_at is not UNSET:
            _input["observedAt"] = observed_at
        if confidence is not UNSET:
            _input["confidence"] = confidence
        _input["derivedFrom"] = derived_from
        _input["term"] = term
        variables["input"] = _input
        return self.execute(
            AssertMeasurementExistsMutation, variables, task=task
        ).assert_measurement_exists

    async def aassert_structure_relation_exists(
        self,
        source_id: str,
        target_id: str,
        supporting_evidence: Iterable[StructureReferenceInput],
        derived_from: Iterable[str],
        term: str,
        observed_at: datetime | None | UnsetType = UNSET,
        confidence: float | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> AssertedStructureRelation:
        """AssertStructureRelationExists

        Assert a relation between two structures. Drawings are always empty: neither endpoint has a vertex

        Args:
            source_id: The ID of the source entity/structure
            target_id: The ID of the target entity/structure
            supporting_evidence: List of evidence structures with measurements
            observed_at: When the world was in this state — world time, the axis a scientist means by 'when'. Distinct from when it is claimed, which the assertion records; left unset, the two are equal. A point, not an interval: a duration is a metric.
            confidence: How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.
            derived_from: The claims this one came from — ids of instances, links, metrics or structures in your organization. Each is recorded as a DERIVED_FROM link under the same assertion as the claim itself, because "this, because of that" is one act (RFC 0017). Read back as `derivedFrom`; the cited claim lists it under `derivations`.
            term: The organization's word for what is being claimed — a term's `key`, e.g. 'AIS'. Not a category id and not a graph: a claim names a word, and every view that declares that word will hold what you write. The word is created if the organization has not used it before; a view that declares no category for it simply will not draw it.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            AssertedStructureRelation"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["sourceId"] = source_id
        _input["targetId"] = target_id
        _input["supportingEvidence"] = supporting_evidence
        if observed_at is not UNSET:
            _input["observedAt"] = observed_at
        if confidence is not UNSET:
            _input["confidence"] = confidence
        _input["derivedFrom"] = derived_from
        _input["term"] = term
        variables["input"] = _input
        return (
            await self.aexecute(
                AssertStructureRelationExistsMutation, variables, task=task
            )
        ).assert_structure_relation_exists

    def assert_structure_relation_exists(
        self,
        source_id: str,
        target_id: str,
        supporting_evidence: Iterable[StructureReferenceInput],
        derived_from: Iterable[str],
        term: str,
        observed_at: datetime | None | UnsetType = UNSET,
        confidence: float | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> AssertedStructureRelation:
        """AssertStructureRelationExists

        Assert a relation between two structures. Drawings are always empty: neither endpoint has a vertex

        Args:
            source_id: The ID of the source entity/structure
            target_id: The ID of the target entity/structure
            supporting_evidence: List of evidence structures with measurements
            observed_at: When the world was in this state — world time, the axis a scientist means by 'when'. Distinct from when it is claimed, which the assertion records; left unset, the two are equal. A point, not an interval: a duration is a metric.
            confidence: How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.
            derived_from: The claims this one came from — ids of instances, links, metrics or structures in your organization. Each is recorded as a DERIVED_FROM link under the same assertion as the claim itself, because "this, because of that" is one act (RFC 0017). Read back as `derivedFrom`; the cited claim lists it under `derivations`.
            term: The organization's word for what is being claimed — a term's `key`, e.g. 'AIS'. Not a category id and not a graph: a claim names a word, and every view that declares that word will hold what you write. The word is created if the organization has not used it before; a view that declares no category for it simply will not draw it.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            AssertedStructureRelation"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["sourceId"] = source_id
        _input["targetId"] = target_id
        _input["supportingEvidence"] = supporting_evidence
        if observed_at is not UNSET:
            _input["observedAt"] = observed_at
        if confidence is not UNSET:
            _input["confidence"] = confidence
        _input["derivedFrom"] = derived_from
        _input["term"] = term
        variables["input"] = _input
        return self.execute(
            AssertStructureRelationExistsMutation, variables, task=task
        ).assert_structure_relation_exists

    async def aassert_participation(
        self,
        event: str,
        entity: str,
        role: str,
        is_input: bool,
        derived_from: Iterable[str],
        observed_at: datetime | None | UnsetType = UNSET,
        confidence: float | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> AssertedParticipation:
        """AssertParticipation

        Claim that an entity took part in an event, without displacing anyone else's claim

        Args:
            event: The ID of the event the entity took part in
            entity: The ID of the entity that took part
            role: Which role the entity played — the caller's own word; the write names no graph and no category
            is_input: True if the entity went into the event, False if it came out of it
            observed_at: When the world was in this state — world time, the axis a scientist means by 'when'. Distinct from when it is claimed, which the assertion records; left unset, the two are equal. A point, not an interval: a duration is a metric.
            confidence: How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.
            derived_from: The claims this one came from — ids of instances, links, metrics or structures in your organization. Each is recorded as a DERIVED_FROM link under the same assertion as the claim itself, because "this, because of that" is one act (RFC 0017). Read back as `derivedFrom`; the cited claim lists it under `derivations`.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            AssertedParticipation"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["event"] = event
        _input["entity"] = entity
        _input["role"] = role
        _input["isInput"] = is_input
        if observed_at is not UNSET:
            _input["observedAt"] = observed_at
        if confidence is not UNSET:
            _input["confidence"] = confidence
        _input["derivedFrom"] = derived_from
        variables["input"] = _input
        return (
            await self.aexecute(AssertParticipationMutation, variables, task=task)
        ).assert_participation

    def assert_participation(
        self,
        event: str,
        entity: str,
        role: str,
        is_input: bool,
        derived_from: Iterable[str],
        observed_at: datetime | None | UnsetType = UNSET,
        confidence: float | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> AssertedParticipation:
        """AssertParticipation

        Claim that an entity took part in an event, without displacing anyone else's claim

        Args:
            event: The ID of the event the entity took part in
            entity: The ID of the entity that took part
            role: Which role the entity played — the caller's own word; the write names no graph and no category
            is_input: True if the entity went into the event, False if it came out of it
            observed_at: When the world was in this state — world time, the axis a scientist means by 'when'. Distinct from when it is claimed, which the assertion records; left unset, the two are equal. A point, not an interval: a duration is a metric.
            confidence: How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.
            derived_from: The claims this one came from — ids of instances, links, metrics or structures in your organization. Each is recorded as a DERIVED_FROM link under the same assertion as the claim itself, because "this, because of that" is one act (RFC 0017). Read back as `derivedFrom`; the cited claim lists it under `derivations`.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            AssertedParticipation"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["event"] = event
        _input["entity"] = entity
        _input["role"] = role
        _input["isInput"] = is_input
        if observed_at is not UNSET:
            _input["observedAt"] = observed_at
        if confidence is not UNSET:
            _input["confidence"] = confidence
        _input["derivedFrom"] = derived_from
        variables["input"] = _input
        return self.execute(
            AssertParticipationMutation, variables, task=task
        ).assert_participation

    async def aassert_participations(
        self,
        event: str,
        participants: Iterable[ParticipantInput],
        task: TaskLike | None = None,
    ) -> AssertedLinks:
        """AssertParticipations
         Many participants in one event, one assertion.

        Args:
            event: The event the entities took part in
            participants: Everyone who took part, and how
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            AssertedLinks"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["event"] = event
        _input["participants"] = participants
        variables["input"] = _input
        return (
            await self.aexecute(AssertParticipationsMutation, variables, task=task)
        ).assert_participations

    def assert_participations(
        self,
        event: str,
        participants: Iterable[ParticipantInput],
        task: TaskLike | None = None,
    ) -> AssertedLinks:
        """AssertParticipations
         Many participants in one event, one assertion.

        Args:
            event: The event the entities took part in
            participants: Everyone who took part, and how
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            AssertedLinks"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["event"] = event
        _input["participants"] = participants
        variables["input"] = _input
        return self.execute(
            AssertParticipationsMutation, variables, task=task
        ).assert_participations

    async def acomment_on_structure(
        self,
        identifier: str,
        object: str,
        descendants: Iterable[DescendantInput],
        parent: IDCoercible | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> AssertedComment:
        """CommentOnStructure
         ---- comments ------------------------------------------------------------------------------

        Args:
            identifier: The structure identifier of the datum, e.g. '@mikro/roi'
            object: The id of the external object on its service
            descendants: The rich body of the remark — a tree of LEAF/MENTION/PARAGRAPH nodes
            parent: The comment this replies to. Must be on the same structure's thread
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            AssertedComment"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["identifier"] = identifier
        _input["object"] = object
        _input["descendants"] = descendants
        if parent is not UNSET:
            _input["parent"] = parent
        variables["input"] = _input
        return (
            await self.aexecute(CommentOnStructureMutation, variables, task=task)
        ).comment_on_structure

    def comment_on_structure(
        self,
        identifier: str,
        object: str,
        descendants: Iterable[DescendantInput],
        parent: IDCoercible | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> AssertedComment:
        """CommentOnStructure
         ---- comments ------------------------------------------------------------------------------

        Args:
            identifier: The structure identifier of the datum, e.g. '@mikro/roi'
            object: The id of the external object on its service
            descendants: The rich body of the remark — a tree of LEAF/MENTION/PARAGRAPH nodes
            parent: The comment this replies to. Must be on the same structure's thread
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            AssertedComment"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["identifier"] = identifier
        _input["object"] = object
        _input["descendants"] = descendants
        if parent is not UNSET:
            _input["parent"] = parent
        variables["input"] = _input
        return self.execute(
            CommentOnStructureMutation, variables, task=task
        ).comment_on_structure

    async def acreate_graph(
        self,
        name: str,
        backfill: bool,
        description: str | None | UnsetType = UNSET,
        definition: GraphDefinitionInput | None | UnsetType = UNSET,
        sameness_rule: SamenessRuleInput | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> Graph:
        """CreateGraph
         A Graph is a VIEW over the organization's claims, not a container. `definition.extensions`
         carries a whole ontology, so one call can declare every word this view means to draw, and
         `backfill` projects the claims those words already admit.

        Args:
            name: Name of the graph
            description: Description of the graph
            definition: The complete graph schema definition
            sameness_rule: Whose sameness claims this view counts (RFC 0024). Omitted means everyone
            backfill: Draw the evidence this graph's words already admit. A graph is a view over the organization's evidence, so a new one can be a view over history: with this on, every node and edge already claimed under a word this schema declares is projected as the graph is created. Off by default because the work is proportional to the organization's evidence and happens before this mutation returns.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            Graph"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["name"] = name
        if description is not UNSET:
            _input["description"] = description
        if definition is not UNSET:
            _input["definition"] = definition
        if sameness_rule is not UNSET:
            _input["samenessRule"] = sameness_rule
        _input["backfill"] = backfill
        variables["input"] = _input
        return (
            await self.aexecute(CreateGraphMutation, variables, task=task)
        ).create_graph

    def create_graph(
        self,
        name: str,
        backfill: bool,
        description: str | None | UnsetType = UNSET,
        definition: GraphDefinitionInput | None | UnsetType = UNSET,
        sameness_rule: SamenessRuleInput | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> Graph:
        """CreateGraph
         A Graph is a VIEW over the organization's claims, not a container. `definition.extensions`
         carries a whole ontology, so one call can declare every word this view means to draw, and
         `backfill` projects the claims those words already admit.

        Args:
            name: Name of the graph
            description: Description of the graph
            definition: The complete graph schema definition
            sameness_rule: Whose sameness claims this view counts (RFC 0024). Omitted means everyone
            backfill: Draw the evidence this graph's words already admit. A graph is a view over the organization's evidence, so a new one can be a view over history: with this on, every node and edge already claimed under a word this schema declares is projected as the graph is created. Off by default because the work is proportional to the organization's evidence and happens before this mutation returns.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            Graph"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["name"] = name
        if description is not UNSET:
            _input["description"] = description
        if definition is not UNSET:
            _input["definition"] = definition
        if sameness_rule is not UNSET:
            _input["samenessRule"] = sameness_rule
        _input["backfill"] = backfill
        variables["input"] = _input
        return self.execute(CreateGraphMutation, variables, task=task).create_graph

    async def aupdate_graph(
        self,
        id: str,
        name: str | None | UnsetType = UNSET,
        description: str | None | UnsetType = UNSET,
        archived: bool | None | UnsetType = UNSET,
        pin: bool | None | UnsetType = UNSET,
        sameness_rule: SamenessRuleInput | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> Graph:
        """UpdateGraph

        Update an existing graph in the graph engine

        Args:
            id: The ID of the graph to update
            name: New graph name
            description: New graph description
            archived: Optional archived flag update
            pin: Optional pin flag update for the user making the request
            sameness_rule: Replace whose sameness claims this view counts (RFC 0024); an empty rule list means everyone. Omitted means unchanged. Changing it refolds the view's individuals — the projection is rebuilt
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            Graph"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        if name is not UNSET:
            _input["name"] = name
        if description is not UNSET:
            _input["description"] = description
        if archived is not UNSET:
            _input["archived"] = archived
        if pin is not UNSET:
            _input["pin"] = pin
        if sameness_rule is not UNSET:
            _input["samenessRule"] = sameness_rule
        variables["input"] = _input
        return (
            await self.aexecute(UpdateGraphMutation, variables, task=task)
        ).update_graph

    def update_graph(
        self,
        id: str,
        name: str | None | UnsetType = UNSET,
        description: str | None | UnsetType = UNSET,
        archived: bool | None | UnsetType = UNSET,
        pin: bool | None | UnsetType = UNSET,
        sameness_rule: SamenessRuleInput | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> Graph:
        """UpdateGraph

        Update an existing graph in the graph engine

        Args:
            id: The ID of the graph to update
            name: New graph name
            description: New graph description
            archived: Optional archived flag update
            pin: Optional pin flag update for the user making the request
            sameness_rule: Replace whose sameness claims this view counts (RFC 0024); an empty rule list means everyone. Omitted means unchanged. Changing it refolds the view's individuals — the projection is rebuilt
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            Graph"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        if name is not UNSET:
            _input["name"] = name
        if description is not UNSET:
            _input["description"] = description
        if archived is not UNSET:
            _input["archived"] = archived
        if pin is not UNSET:
            _input["pin"] = pin
        if sameness_rule is not UNSET:
            _input["samenessRule"] = sameness_rule
        variables["input"] = _input
        return self.execute(UpdateGraphMutation, variables, task=task).update_graph

    async def aupdate_graph_visual(
        self,
        id: str,
        node_positions: Iterable[CategoryNodePositionInput],
        task: TaskLike | None = None,
    ) -> Graph:
        """UpdateGraphVisual

        Update the visual configuration of a graph in the graph engine

        Args:
            id: The ID of the graph element to update
            node_positions: List of node positions to update
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            Graph"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        _input["nodePositions"] = node_positions
        variables["input"] = _input
        return (
            await self.aexecute(UpdateGraphVisualMutation, variables, task=task)
        ).update_graph_visual

    def update_graph_visual(
        self,
        id: str,
        node_positions: Iterable[CategoryNodePositionInput],
        task: TaskLike | None = None,
    ) -> Graph:
        """UpdateGraphVisual

        Update the visual configuration of a graph in the graph engine

        Args:
            id: The ID of the graph element to update
            node_positions: List of node positions to update
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            Graph"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        _input["nodePositions"] = node_positions
        variables["input"] = _input
        return self.execute(
            UpdateGraphVisualMutation, variables, task=task
        ).update_graph_visual

    async def aarchive_graph(self, id: str, task: TaskLike | None = None) -> Graph:
        """ArchiveGraph

        Archive a graph in the graph engine (soft delete)

        Args:
            id: The ID of the graph to archive
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            Graph"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        variables["input"] = _input
        return (
            await self.aexecute(ArchiveGraphMutation, variables, task=task)
        ).archive_graph

    def archive_graph(self, id: str, task: TaskLike | None = None) -> Graph:
        """ArchiveGraph

        Archive a graph in the graph engine (soft delete)

        Args:
            id: The ID of the graph to archive
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            Graph"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        variables["input"] = _input
        return self.execute(ArchiveGraphMutation, variables, task=task).archive_graph

    async def adelete_graph(self, id: str, task: TaskLike | None = None) -> ID:
        """DeleteGraph

        Delete a graph from the graph engine

        Args:
            id: The ID of the graph to delete
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            ID"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        variables["input"] = _input
        return (
            await self.aexecute(DeleteGraphMutation, variables, task=task)
        ).delete_graph

    def delete_graph(self, id: str, task: TaskLike | None = None) -> ID:
        """DeleteGraph

        Delete a graph from the graph engine

        Args:
            id: The ID of the graph to delete
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            ID"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        variables["input"] = _input
        return self.execute(DeleteGraphMutation, variables, task=task).delete_graph

    async def aattest_entity(
        self,
        id: str,
        at: datetime | None | UnsetType = UNSET,
        confidence: float | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> AssertedEntity:
        """AttestEntity
         Standing: somebody's position on whether a claim still holds.

         `attest` records stands=True, `retract` records stands=False, and both are evidence of the
         same kind. Neither deletes: the row, its metrics and its relations all survive a retraction,
         because a derived value that dropped a contributing measurement still has to be explainable.
         There is no reinstate and no state machine — only more evidence.

        Args:
            id: The uuid of the node being attested. The same id `retract*` returns, so the two round-trip.
            at: When this position took effect — world time. Left unset, the moment of the claim. A rule bounding OBSERVED_AT on EXISTENCE reads this.
            confidence: How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            AssertedEntity"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        if at is not UNSET:
            _input["at"] = at
        if confidence is not UNSET:
            _input["confidence"] = confidence
        variables["input"] = _input
        return (
            await self.aexecute(AttestEntityMutation, variables, task=task)
        ).attest_entity

    def attest_entity(
        self,
        id: str,
        at: datetime | None | UnsetType = UNSET,
        confidence: float | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> AssertedEntity:
        """AttestEntity
         Standing: somebody's position on whether a claim still holds.

         `attest` records stands=True, `retract` records stands=False, and both are evidence of the
         same kind. Neither deletes: the row, its metrics and its relations all survive a retraction,
         because a derived value that dropped a contributing measurement still has to be explainable.
         There is no reinstate and no state machine — only more evidence.

        Args:
            id: The uuid of the node being attested. The same id `retract*` returns, so the two round-trip.
            at: When this position took effect — world time. Left unset, the moment of the claim. A rule bounding OBSERVED_AT on EXISTENCE reads this.
            confidence: How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            AssertedEntity"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        if at is not UNSET:
            _input["at"] = at
        if confidence is not UNSET:
            _input["confidence"] = confidence
        variables["input"] = _input
        return self.execute(AttestEntityMutation, variables, task=task).attest_entity

    async def aretract_entity(
        self,
        id: IDCoercible,
        at: datetime | None | UnsetType = UNSET,
        confidence: float | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> AssertedEntity:
        """RetractEntity

        Claim that an entity no longer stands. It leaves every projection that counts the claim; the evidence stays.

        Args:
            id: The ID of the entity to retract
            at: When this position took effect — world time. Left unset, the moment of the claim. A rule bounding OBSERVED_AT on EXISTENCE reads this.
            confidence: How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            AssertedEntity"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        if at is not UNSET:
            _input["at"] = at
        if confidence is not UNSET:
            _input["confidence"] = confidence
        variables["input"] = _input
        return (
            await self.aexecute(RetractEntityMutation, variables, task=task)
        ).retract_entity

    def retract_entity(
        self,
        id: IDCoercible,
        at: datetime | None | UnsetType = UNSET,
        confidence: float | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> AssertedEntity:
        """RetractEntity

        Claim that an entity no longer stands. It leaves every projection that counts the claim; the evidence stays.

        Args:
            id: The ID of the entity to retract
            at: When this position took effect — world time. Left unset, the moment of the claim. A rule bounding OBSERVED_AT on EXISTENCE reads this.
            confidence: How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            AssertedEntity"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        if at is not UNSET:
            _input["at"] = at
        if confidence is not UNSET:
            _input["confidence"] = confidence
        variables["input"] = _input
        return self.execute(RetractEntityMutation, variables, task=task).retract_entity

    async def aattest_natural_event(
        self,
        id: str,
        at: datetime | None | UnsetType = UNSET,
        confidence: float | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> AssertedNaturalEvent:
        """AttestNaturalEvent

        Claim that a natural event exists

        Args:
            id: The uuid of the node being attested. The same id `retract*` returns, so the two round-trip.
            at: When this position took effect — world time. Left unset, the moment of the claim. A rule bounding OBSERVED_AT on EXISTENCE reads this.
            confidence: How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            AssertedNaturalEvent"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        if at is not UNSET:
            _input["at"] = at
        if confidence is not UNSET:
            _input["confidence"] = confidence
        variables["input"] = _input
        return (
            await self.aexecute(AttestNaturalEventMutation, variables, task=task)
        ).attest_natural_event

    def attest_natural_event(
        self,
        id: str,
        at: datetime | None | UnsetType = UNSET,
        confidence: float | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> AssertedNaturalEvent:
        """AttestNaturalEvent

        Claim that a natural event exists

        Args:
            id: The uuid of the node being attested. The same id `retract*` returns, so the two round-trip.
            at: When this position took effect — world time. Left unset, the moment of the claim. A rule bounding OBSERVED_AT on EXISTENCE reads this.
            confidence: How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            AssertedNaturalEvent"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        if at is not UNSET:
            _input["at"] = at
        if confidence is not UNSET:
            _input["confidence"] = confidence
        variables["input"] = _input
        return self.execute(
            AttestNaturalEventMutation, variables, task=task
        ).attest_natural_event

    async def aretract_natural_event(
        self,
        id: str,
        at: datetime | None | UnsetType = UNSET,
        confidence: float | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> AssertedNaturalEvent:
        """RetractNaturalEvent

        Claim that a natural event no longer stands

        Args:
            id: The ID of the natural event to retract
            at: When this position took effect — world time. Left unset, the moment of the claim. A rule bounding OBSERVED_AT on EXISTENCE reads this.
            confidence: How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            AssertedNaturalEvent"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        if at is not UNSET:
            _input["at"] = at
        if confidence is not UNSET:
            _input["confidence"] = confidence
        variables["input"] = _input
        return (
            await self.aexecute(RetractNaturalEventMutation, variables, task=task)
        ).retract_natural_event

    def retract_natural_event(
        self,
        id: str,
        at: datetime | None | UnsetType = UNSET,
        confidence: float | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> AssertedNaturalEvent:
        """RetractNaturalEvent

        Claim that a natural event no longer stands

        Args:
            id: The ID of the natural event to retract
            at: When this position took effect — world time. Left unset, the moment of the claim. A rule bounding OBSERVED_AT on EXISTENCE reads this.
            confidence: How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            AssertedNaturalEvent"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        if at is not UNSET:
            _input["at"] = at
        if confidence is not UNSET:
            _input["confidence"] = confidence
        variables["input"] = _input
        return self.execute(
            RetractNaturalEventMutation, variables, task=task
        ).retract_natural_event

    async def aattest_protocol_event(
        self,
        id: str,
        at: datetime | None | UnsetType = UNSET,
        confidence: float | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> AssertedProtocolEvent:
        """AttestProtocolEvent

        Claim that a protocol event exists

        Args:
            id: The uuid of the node being attested. The same id `retract*` returns, so the two round-trip.
            at: When this position took effect — world time. Left unset, the moment of the claim. A rule bounding OBSERVED_AT on EXISTENCE reads this.
            confidence: How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            AssertedProtocolEvent"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        if at is not UNSET:
            _input["at"] = at
        if confidence is not UNSET:
            _input["confidence"] = confidence
        variables["input"] = _input
        return (
            await self.aexecute(AttestProtocolEventMutation, variables, task=task)
        ).attest_protocol_event

    def attest_protocol_event(
        self,
        id: str,
        at: datetime | None | UnsetType = UNSET,
        confidence: float | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> AssertedProtocolEvent:
        """AttestProtocolEvent

        Claim that a protocol event exists

        Args:
            id: The uuid of the node being attested. The same id `retract*` returns, so the two round-trip.
            at: When this position took effect — world time. Left unset, the moment of the claim. A rule bounding OBSERVED_AT on EXISTENCE reads this.
            confidence: How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            AssertedProtocolEvent"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        if at is not UNSET:
            _input["at"] = at
        if confidence is not UNSET:
            _input["confidence"] = confidence
        variables["input"] = _input
        return self.execute(
            AttestProtocolEventMutation, variables, task=task
        ).attest_protocol_event

    async def aretract_protocol_event(
        self,
        id: str,
        at: datetime | None | UnsetType = UNSET,
        confidence: float | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> AssertedProtocolEvent:
        """RetractProtocolEvent

        Claim that a protocol event no longer stands

        Args:
            id: The ID of the protocol event to retract
            at: When this position took effect — world time. Left unset, the moment of the claim. A rule bounding OBSERVED_AT on EXISTENCE reads this.
            confidence: How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            AssertedProtocolEvent"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        if at is not UNSET:
            _input["at"] = at
        if confidence is not UNSET:
            _input["confidence"] = confidence
        variables["input"] = _input
        return (
            await self.aexecute(RetractProtocolEventMutation, variables, task=task)
        ).retract_protocol_event

    def retract_protocol_event(
        self,
        id: str,
        at: datetime | None | UnsetType = UNSET,
        confidence: float | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> AssertedProtocolEvent:
        """RetractProtocolEvent

        Claim that a protocol event no longer stands

        Args:
            id: The ID of the protocol event to retract
            at: When this position took effect — world time. Left unset, the moment of the claim. A rule bounding OBSERVED_AT on EXISTENCE reads this.
            confidence: How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            AssertedProtocolEvent"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        if at is not UNSET:
            _input["at"] = at
        if confidence is not UNSET:
            _input["confidence"] = confidence
        variables["input"] = _input
        return self.execute(
            RetractProtocolEventMutation, variables, task=task
        ).retract_protocol_event

    async def aattest_structure(
        self,
        id: str,
        at: datetime | None | UnsetType = UNSET,
        confidence: float | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> AssertedStructure:
        """AttestStructure

        Claim that a structure still stands, after somebody retracted it. New evidence, not an undo — both positions stay on the record

        Args:
            id: The ID of the structure to attest — a bare uuid, its evidence primary key
            at: When this position took effect — world time. Left unset, the moment of the claim. A rule bounding OBSERVED_AT on EXISTENCE reads this.
            confidence: How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            AssertedStructure"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        if at is not UNSET:
            _input["at"] = at
        if confidence is not UNSET:
            _input["confidence"] = confidence
        variables["input"] = _input
        return (
            await self.aexecute(AttestStructureMutation, variables, task=task)
        ).attest_structure

    def attest_structure(
        self,
        id: str,
        at: datetime | None | UnsetType = UNSET,
        confidence: float | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> AssertedStructure:
        """AttestStructure

        Claim that a structure still stands, after somebody retracted it. New evidence, not an undo — both positions stay on the record

        Args:
            id: The ID of the structure to attest — a bare uuid, its evidence primary key
            at: When this position took effect — world time. Left unset, the moment of the claim. A rule bounding OBSERVED_AT on EXISTENCE reads this.
            confidence: How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            AssertedStructure"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        if at is not UNSET:
            _input["at"] = at
        if confidence is not UNSET:
            _input["confidence"] = confidence
        variables["input"] = _input
        return self.execute(
            AttestStructureMutation, variables, task=task
        ).attest_structure

    async def aretract_structure(
        self,
        id: IDCoercible,
        at: datetime | None | UnsetType = UNSET,
        confidence: float | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> AssertedStructure:
        """RetractStructure

        Retract a datum: a Standing(stands=false) against it. Its metrics and INFORMS claims stay on the record, but stop counting for every node it informs until somebody attests it again (RFC 0023)

        Args:
            id: The ID of the structure to retract — a bare uuid, its evidence primary key
            at: When this position took effect — world time. Left unset, the moment of the claim. A rule bounding OBSERVED_AT on EXISTENCE reads this.
            confidence: How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            AssertedStructure"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        if at is not UNSET:
            _input["at"] = at
        if confidence is not UNSET:
            _input["confidence"] = confidence
        variables["input"] = _input
        return (
            await self.aexecute(RetractStructureMutation, variables, task=task)
        ).retract_structure

    def retract_structure(
        self,
        id: IDCoercible,
        at: datetime | None | UnsetType = UNSET,
        confidence: float | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> AssertedStructure:
        """RetractStructure

        Retract a datum: a Standing(stands=false) against it. Its metrics and INFORMS claims stay on the record, but stop counting for every node it informs until somebody attests it again (RFC 0023)

        Args:
            id: The ID of the structure to retract — a bare uuid, its evidence primary key
            at: When this position took effect — world time. Left unset, the moment of the claim. A rule bounding OBSERVED_AT on EXISTENCE reads this.
            confidence: How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            AssertedStructure"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        if at is not UNSET:
            _input["at"] = at
        if confidence is not UNSET:
            _input["confidence"] = confidence
        variables["input"] = _input
        return self.execute(
            RetractStructureMutation, variables, task=task
        ).retract_structure

    async def aattest_metric(
        self,
        id: str,
        at: datetime | None | UnsetType = UNSET,
        confidence: float | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> AssertedMetric:
        """AttestMetric

        Claim that a measurement still stands. The derived values that dropped it are refolded

        Args:
            id: The ID of the metric to attest — a bare uuid, its evidence primary key
            at: When this position took effect — world time. Left unset, the moment of the claim. A rule bounding OBSERVED_AT on EXISTENCE reads this.
            confidence: How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            AssertedMetric"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        if at is not UNSET:
            _input["at"] = at
        if confidence is not UNSET:
            _input["confidence"] = confidence
        variables["input"] = _input
        return (
            await self.aexecute(AttestMetricMutation, variables, task=task)
        ).attest_metric

    def attest_metric(
        self,
        id: str,
        at: datetime | None | UnsetType = UNSET,
        confidence: float | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> AssertedMetric:
        """AttestMetric

        Claim that a measurement still stands. The derived values that dropped it are refolded

        Args:
            id: The ID of the metric to attest — a bare uuid, its evidence primary key
            at: When this position took effect — world time. Left unset, the moment of the claim. A rule bounding OBSERVED_AT on EXISTENCE reads this.
            confidence: How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            AssertedMetric"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        if at is not UNSET:
            _input["at"] = at
        if confidence is not UNSET:
            _input["confidence"] = confidence
        variables["input"] = _input
        return self.execute(AttestMetricMutation, variables, task=task).attest_metric

    async def aretract_metric(
        self,
        id: str,
        at: datetime | None | UnsetType = UNSET,
        confidence: float | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> AssertedMetric:
        """RetractMetric

        Retract a measurement without destroying it. It stays readable, because a derived value that dropped it still has to be explainable

        Args:
            id: The ID of the metric to retract — a bare uuid, its evidence primary key
            at: When this position took effect — world time. Left unset, the moment of the claim. A rule bounding OBSERVED_AT on EXISTENCE reads this.
            confidence: How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            AssertedMetric"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        if at is not UNSET:
            _input["at"] = at
        if confidence is not UNSET:
            _input["confidence"] = confidence
        variables["input"] = _input
        return (
            await self.aexecute(RetractMetricMutation, variables, task=task)
        ).retract_metric

    def retract_metric(
        self,
        id: str,
        at: datetime | None | UnsetType = UNSET,
        confidence: float | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> AssertedMetric:
        """RetractMetric

        Retract a measurement without destroying it. It stays readable, because a derived value that dropped it still has to be explainable

        Args:
            id: The ID of the metric to retract — a bare uuid, its evidence primary key
            at: When this position took effect — world time. Left unset, the moment of the claim. A rule bounding OBSERVED_AT on EXISTENCE reads this.
            confidence: How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            AssertedMetric"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        if at is not UNSET:
            _input["at"] = at
        if confidence is not UNSET:
            _input["confidence"] = confidence
        variables["input"] = _input
        return self.execute(RetractMetricMutation, variables, task=task).retract_metric

    async def aattest_comment(
        self,
        id: str,
        at: datetime | None | UnsetType = UNSET,
        confidence: float | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> AssertedComment:
        """AttestComment

        Claim a remark stands again — reopening, as new evidence rather than an undo

        Args:
            id: The ID of the comment to attest
            at: When this position took effect — world time. Left unset, the moment of the claim. A rule bounding OBSERVED_AT on EXISTENCE reads this.
            confidence: How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            AssertedComment"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        if at is not UNSET:
            _input["at"] = at
        if confidence is not UNSET:
            _input["confidence"] = confidence
        variables["input"] = _input
        return (
            await self.aexecute(AttestCommentMutation, variables, task=task)
        ).attest_comment

    def attest_comment(
        self,
        id: str,
        at: datetime | None | UnsetType = UNSET,
        confidence: float | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> AssertedComment:
        """AttestComment

        Claim a remark stands again — reopening, as new evidence rather than an undo

        Args:
            id: The ID of the comment to attest
            at: When this position took effect — world time. Left unset, the moment of the claim. A rule bounding OBSERVED_AT on EXISTENCE reads this.
            confidence: How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            AssertedComment"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        if at is not UNSET:
            _input["at"] = at
        if confidence is not UNSET:
            _input["confidence"] = confidence
        variables["input"] = _input
        return self.execute(AttestCommentMutation, variables, task=task).attest_comment

    async def aretract_comment(
        self,
        id: str,
        at: datetime | None | UnsetType = UNSET,
        confidence: float | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> AssertedComment:
        """RetractComment

        Claim a remark no longer stands — resolved by a reviewer or withdrawn by its author; the assertion records whose position it is. The row survives

        Args:
            id: The ID of the comment to retract
            at: When this position took effect — world time. Left unset, the moment of the claim. A rule bounding OBSERVED_AT on EXISTENCE reads this.
            confidence: How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            AssertedComment"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        if at is not UNSET:
            _input["at"] = at
        if confidence is not UNSET:
            _input["confidence"] = confidence
        variables["input"] = _input
        return (
            await self.aexecute(RetractCommentMutation, variables, task=task)
        ).retract_comment

    def retract_comment(
        self,
        id: str,
        at: datetime | None | UnsetType = UNSET,
        confidence: float | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> AssertedComment:
        """RetractComment

        Claim a remark no longer stands — resolved by a reviewer or withdrawn by its author; the assertion records whose position it is. The row survives

        Args:
            id: The ID of the comment to retract
            at: When this position took effect — world time. Left unset, the moment of the claim. A rule bounding OBSERVED_AT on EXISTENCE reads this.
            confidence: How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            AssertedComment"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        if at is not UNSET:
            _input["at"] = at
        if confidence is not UNSET:
            _input["confidence"] = confidence
        variables["input"] = _input
        return self.execute(
            RetractCommentMutation, variables, task=task
        ).retract_comment

    async def aretract_relation(
        self,
        id: IDCoercible,
        at: datetime | None | UnsetType = UNSET,
        confidence: float | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> AssertedRelation:
        """RetractRelation

        Retract a relation assertion without destroying it. The edge survives wherever another live assertion still states the same proposition

        Args:
            id: The ID of the relation claim to retract — its `Link` primary key
            at: When this position took effect — world time. Left unset, the moment of the claim. A rule bounding OBSERVED_AT on EXISTENCE reads this.
            confidence: How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            AssertedRelation"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        if at is not UNSET:
            _input["at"] = at
        if confidence is not UNSET:
            _input["confidence"] = confidence
        variables["input"] = _input
        return (
            await self.aexecute(RetractRelationMutation, variables, task=task)
        ).retract_relation

    def retract_relation(
        self,
        id: IDCoercible,
        at: datetime | None | UnsetType = UNSET,
        confidence: float | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> AssertedRelation:
        """RetractRelation

        Retract a relation assertion without destroying it. The edge survives wherever another live assertion still states the same proposition

        Args:
            id: The ID of the relation claim to retract — its `Link` primary key
            at: When this position took effect — world time. Left unset, the moment of the claim. A rule bounding OBSERVED_AT on EXISTENCE reads this.
            confidence: How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            AssertedRelation"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        if at is not UNSET:
            _input["at"] = at
        if confidence is not UNSET:
            _input["confidence"] = confidence
        variables["input"] = _input
        return self.execute(
            RetractRelationMutation, variables, task=task
        ).retract_relation

    async def aretract_measurement(
        self,
        id: str,
        at: datetime | None | UnsetType = UNSET,
        confidence: float | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> AssertedMeasurement:
        """RetractMeasurement

        Retract a measurement assertion without destroying it

        Args:
            id: The ID of the measurement claim to retract — its `Link` primary key
            at: When this position took effect — world time. Left unset, the moment of the claim. A rule bounding OBSERVED_AT on EXISTENCE reads this.
            confidence: How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            AssertedMeasurement"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        if at is not UNSET:
            _input["at"] = at
        if confidence is not UNSET:
            _input["confidence"] = confidence
        variables["input"] = _input
        return (
            await self.aexecute(RetractMeasurementMutation, variables, task=task)
        ).retract_measurement

    def retract_measurement(
        self,
        id: str,
        at: datetime | None | UnsetType = UNSET,
        confidence: float | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> AssertedMeasurement:
        """RetractMeasurement

        Retract a measurement assertion without destroying it

        Args:
            id: The ID of the measurement claim to retract — its `Link` primary key
            at: When this position took effect — world time. Left unset, the moment of the claim. A rule bounding OBSERVED_AT on EXISTENCE reads this.
            confidence: How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            AssertedMeasurement"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        if at is not UNSET:
            _input["at"] = at
        if confidence is not UNSET:
            _input["confidence"] = confidence
        variables["input"] = _input
        return self.execute(
            RetractMeasurementMutation, variables, task=task
        ).retract_measurement

    async def aretract_structure_relation(
        self,
        id: str,
        at: datetime | None | UnsetType = UNSET,
        confidence: float | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> AssertedStructureRelation:
        """RetractStructureRelation

        Retract a structure relation assertion without destroying it

        Args:
            id: The ID of the structure relation claim to retract — its `Link` primary key
            at: When this position took effect — world time. Left unset, the moment of the claim. A rule bounding OBSERVED_AT on EXISTENCE reads this.
            confidence: How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            AssertedStructureRelation"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        if at is not UNSET:
            _input["at"] = at
        if confidence is not UNSET:
            _input["confidence"] = confidence
        variables["input"] = _input
        return (
            await self.aexecute(RetractStructureRelationMutation, variables, task=task)
        ).retract_structure_relation

    def retract_structure_relation(
        self,
        id: str,
        at: datetime | None | UnsetType = UNSET,
        confidence: float | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> AssertedStructureRelation:
        """RetractStructureRelation

        Retract a structure relation assertion without destroying it

        Args:
            id: The ID of the structure relation claim to retract — its `Link` primary key
            at: When this position took effect — world time. Left unset, the moment of the claim. A rule bounding OBSERVED_AT on EXISTENCE reads this.
            confidence: How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            AssertedStructureRelation"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        if at is not UNSET:
            _input["at"] = at
        if confidence is not UNSET:
            _input["confidence"] = confidence
        variables["input"] = _input
        return self.execute(
            RetractStructureRelationMutation, variables, task=task
        ).retract_structure_relation

    async def aretract_participation(
        self,
        id: str,
        at: datetime | None | UnsetType = UNSET,
        confidence: float | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> AssertedParticipation:
        """RetractParticipation

        Retract one claim that an entity took part in an event. The edge survives while another claim still states it

        Args:
            id: The evidence ID of the participation claim to retract
            at: When this position took effect — world time. Left unset, the moment of the claim. A rule bounding OBSERVED_AT on EXISTENCE reads this.
            confidence: How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            AssertedParticipation"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        if at is not UNSET:
            _input["at"] = at
        if confidence is not UNSET:
            _input["confidence"] = confidence
        variables["input"] = _input
        return (
            await self.aexecute(RetractParticipationMutation, variables, task=task)
        ).retract_participation

    def retract_participation(
        self,
        id: str,
        at: datetime | None | UnsetType = UNSET,
        confidence: float | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> AssertedParticipation:
        """RetractParticipation

        Retract one claim that an entity took part in an event. The edge survives while another claim still states it

        Args:
            id: The evidence ID of the participation claim to retract
            at: When this position took effect — world time. Left unset, the moment of the claim. A rule bounding OBSERVED_AT on EXISTENCE reads this.
            confidence: How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            AssertedParticipation"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        if at is not UNSET:
            _input["at"] = at
        if confidence is not UNSET:
            _input["confidence"] = confidence
        variables["input"] = _input
        return self.execute(
            RetractParticipationMutation, variables, task=task
        ).retract_participation

    async def aretract_same_instance(
        self,
        id: str,
        at: datetime | None | UnsetType = UNSET,
        confidence: float | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> AssertedSameness:
        """RetractSameInstance

        Withdraw one sameness claim. The component it held together is rebuilt from the claims that survive, which may split it

        Args:
            id: The id of the sameness claim to retract
            at: When this position took effect — world time. Left unset, the moment of the claim. A rule bounding OBSERVED_AT on EXISTENCE reads this.
            confidence: How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            AssertedSameness"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        if at is not UNSET:
            _input["at"] = at
        if confidence is not UNSET:
            _input["confidence"] = confidence
        variables["input"] = _input
        return (
            await self.aexecute(RetractSameInstanceMutation, variables, task=task)
        ).retract_same_instance

    def retract_same_instance(
        self,
        id: str,
        at: datetime | None | UnsetType = UNSET,
        confidence: float | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> AssertedSameness:
        """RetractSameInstance

        Withdraw one sameness claim. The component it held together is rebuilt from the claims that survive, which may split it

        Args:
            id: The id of the sameness claim to retract
            at: When this position took effect — world time. Left unset, the moment of the claim. A rule bounding OBSERVED_AT on EXISTENCE reads this.
            confidence: How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            AssertedSameness"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        if at is not UNSET:
            _input["at"] = at
        if confidence is not UNSET:
            _input["confidence"] = confidence
        variables["input"] = _input
        return self.execute(
            RetractSameInstanceMutation, variables, task=task
        ).retract_same_instance

    async def aattest_link(
        self,
        id: str,
        at: datetime | None | UnsetType = UNSET,
        confidence: float | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> AssertedLinks:
        """AttestLink

        Claim that a link claim still stands — a relation, a classification, a participation, a measurement. One act for every kind, as `retractLinks` is

        Args:
            id: The ID of the claim to attest — its `Link` primary key
            at: When this position took effect — world time. Left unset, the moment of the claim. A rule bounding OBSERVED_AT on EXISTENCE reads this.
            confidence: How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            AssertedLinks"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        if at is not UNSET:
            _input["at"] = at
        if confidence is not UNSET:
            _input["confidence"] = confidence
        variables["input"] = _input
        return (
            await self.aexecute(AttestLinkMutation, variables, task=task)
        ).attest_link

    def attest_link(
        self,
        id: str,
        at: datetime | None | UnsetType = UNSET,
        confidence: float | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> AssertedLinks:
        """AttestLink

        Claim that a link claim still stands — a relation, a classification, a participation, a measurement. One act for every kind, as `retractLinks` is

        Args:
            id: The ID of the claim to attest — its `Link` primary key
            at: When this position took effect — world time. Left unset, the moment of the claim. A rule bounding OBSERVED_AT on EXISTENCE reads this.
            confidence: How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            AssertedLinks"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        if at is not UNSET:
            _input["at"] = at
        if confidence is not UNSET:
            _input["confidence"] = confidence
        variables["input"] = _input
        return self.execute(AttestLinkMutation, variables, task=task).attest_link

    async def aretract_links(
        self,
        ids: Iterable[str],
        at: datetime | None | UnsetType = UNSET,
        confidence: float | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> AssertedLinks:
        """RetractLinks
         One assertion over many link ids, of any link kind.

        Args:
            ids: The `Link` primary keys of the claims to retract
            at: When this position took effect — world time. Left unset, the moment of the claim. A rule bounding OBSERVED_AT on EXISTENCE reads this.
            confidence: How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            AssertedLinks"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["ids"] = ids
        if at is not UNSET:
            _input["at"] = at
        if confidence is not UNSET:
            _input["confidence"] = confidence
        variables["input"] = _input
        return (
            await self.aexecute(RetractLinksMutation, variables, task=task)
        ).retract_links

    def retract_links(
        self,
        ids: Iterable[str],
        at: datetime | None | UnsetType = UNSET,
        confidence: float | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> AssertedLinks:
        """RetractLinks
         One assertion over many link ids, of any link kind.

        Args:
            ids: The `Link` primary keys of the claims to retract
            at: When this position took effect — world time. Left unset, the moment of the claim. A rule bounding OBSERVED_AT on EXISTENCE reads this.
            confidence: How sure you are, 0 to 1. Left unset, the claim carries no number — which is neither 1.0 nor 0.0: a category rule with a CONFIDENCE condition admits only claims that carry one.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            AssertedLinks"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["ids"] = ids
        if at is not UNSET:
            _input["at"] = at
        if confidence is not UNSET:
            _input["confidence"] = confidence
        variables["input"] = _input
        return self.execute(RetractLinksMutation, variables, task=task).retract_links

    async def acreate_term(
        self,
        kind: TermKind,
        key: str,
        label: str | None | UnsetType = UNSET,
        description: str | None | UnsetType = UNSET,
        purl: str | None | UnsetType = UNSET,
        color: Iterable[int] | None | UnsetType = UNSET,
        image: str | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> Term:
        """CreateTerm
         The organization's words. Terms are minted lazily by the first claim that names one, so
         createTerm is only for declaring a word ahead of use (or giving it a label and colour).

        Args:
            kind: What sort of thing this word names. Part of its identity.
            key: The word itself, e.g. 'AIS'
            label: Human-readable name
            description: What this word means
            purl: Persistent URL, where this corresponds to a published ontology term
            color: Optional RGBA colour
            image: Optional media store ID for an illustrative image
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            Term"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["kind"] = kind
        _input["key"] = key
        if label is not UNSET:
            _input["label"] = label
        if description is not UNSET:
            _input["description"] = description
        if purl is not UNSET:
            _input["purl"] = purl
        if color is not UNSET:
            _input["color"] = color
        if image is not UNSET:
            _input["image"] = image
        variables["input"] = _input
        return (
            await self.aexecute(CreateTermMutation, variables, task=task)
        ).create_term

    def create_term(
        self,
        kind: TermKind,
        key: str,
        label: str | None | UnsetType = UNSET,
        description: str | None | UnsetType = UNSET,
        purl: str | None | UnsetType = UNSET,
        color: Iterable[int] | None | UnsetType = UNSET,
        image: str | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> Term:
        """CreateTerm
         The organization's words. Terms are minted lazily by the first claim that names one, so
         createTerm is only for declaring a word ahead of use (or giving it a label and colour).

        Args:
            kind: What sort of thing this word names. Part of its identity.
            key: The word itself, e.g. 'AIS'
            label: Human-readable name
            description: What this word means
            purl: Persistent URL, where this corresponds to a published ontology term
            color: Optional RGBA colour
            image: Optional media store ID for an illustrative image
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            Term"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["kind"] = kind
        _input["key"] = key
        if label is not UNSET:
            _input["label"] = label
        if description is not UNSET:
            _input["description"] = description
        if purl is not UNSET:
            _input["purl"] = purl
        if color is not UNSET:
            _input["color"] = color
        if image is not UNSET:
            _input["image"] = image
        variables["input"] = _input
        return self.execute(CreateTermMutation, variables, task=task).create_term

    async def aupdate_term(
        self,
        id: str,
        label: str | None | UnsetType = UNSET,
        description: str | None | UnsetType = UNSET,
        purl: str | None | UnsetType = UNSET,
        color: Iterable[int] | None | UnsetType = UNSET,
        image: str | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> Term:
        """UpdateTerm

        Update a term's label, description, PURL or colour. Its kind and key are its identity and cannot change.

        Args:
            id: The ID of the term to update
            label: Human-readable name
            description: What this word means
            purl: Persistent URL, where this corresponds to a published ontology term
            color: Optional RGBA colour
            image: Optional media store ID for an illustrative image
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            Term"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        if label is not UNSET:
            _input["label"] = label
        if description is not UNSET:
            _input["description"] = description
        if purl is not UNSET:
            _input["purl"] = purl
        if color is not UNSET:
            _input["color"] = color
        if image is not UNSET:
            _input["image"] = image
        variables["input"] = _input
        return (
            await self.aexecute(UpdateTermMutation, variables, task=task)
        ).update_term

    def update_term(
        self,
        id: str,
        label: str | None | UnsetType = UNSET,
        description: str | None | UnsetType = UNSET,
        purl: str | None | UnsetType = UNSET,
        color: Iterable[int] | None | UnsetType = UNSET,
        image: str | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> Term:
        """UpdateTerm

        Update a term's label, description, PURL or colour. Its kind and key are its identity and cannot change.

        Args:
            id: The ID of the term to update
            label: Human-readable name
            description: What this word means
            purl: Persistent URL, where this corresponds to a published ontology term
            color: Optional RGBA colour
            image: Optional media store ID for an illustrative image
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            Term"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        if label is not UNSET:
            _input["label"] = label
        if description is not UNSET:
            _input["description"] = description
        if purl is not UNSET:
            _input["purl"] = purl
        if color is not UNSET:
            _input["color"] = color
        if image is not UNSET:
            _input["image"] = image
        variables["input"] = _input
        return self.execute(UpdateTermMutation, variables, task=task).update_term

    async def adelete_term(self, id: str, task: TaskLike | None = None) -> ID:
        """DeleteTerm

        Retire a word nothing has been claimed under

        Args:
            id: The ID of the term to delete
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            ID"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        variables["input"] = _input
        return (
            await self.aexecute(DeleteTermMutation, variables, task=task)
        ).delete_term

    def delete_term(self, id: str, task: TaskLike | None = None) -> ID:
        """DeleteTerm

        Retire a word nothing has been claimed under

        Args:
            id: The ID of the term to delete
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            ID"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        variables["input"] = _input
        return self.execute(DeleteTermMutation, variables, task=task).delete_term

    async def aupdate_structure_kind(
        self,
        id: str,
        key: str | None | UnsetType = UNSET,
        description: str | None | UnsetType = UNSET,
        ontology_references: Iterable[OntologyReferenceInput]
        | None
        | UnsetType = UNSET,
        color: Iterable[int] | None | UnsetType = UNSET,
        image: str | None | UnsetType = UNSET,
        label: str | None | UnsetType = UNSET,
        pin: bool | None | UnsetType = UNSET,
        identifier: str | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> StructureKind:
        """UpdateStructureKind
         StructureKind and MetricKind are minted by the write that first needs them — there is no
         create mutation for either, only these.

        Args:
            id: The ID of the definition to update
            key: The label of the node participating in the event
            description: Description of this node role
            ontology_references: Ontology references for this event
            color: Optional RGBA color for this node role (e.g. [255, 0, 0, 128])
            image: Optional media store ID for an image representing this node role
            label: Optional human-readable label for this node role (defaults to 'key' if not provided)
            pin: Whether to pin this node role in the UI
            identifier: Read by nothing: `(organization, identifier)` is a structure kind's identity and cannot be reassigned. `update_structure_kind` writes label, description and colour only
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            StructureKind"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        if key is not UNSET:
            _input["key"] = key
        if description is not UNSET:
            _input["description"] = description
        if ontology_references is not UNSET:
            _input["ontologyReferences"] = ontology_references
        if color is not UNSET:
            _input["color"] = color
        if image is not UNSET:
            _input["image"] = image
        if label is not UNSET:
            _input["label"] = label
        if pin is not UNSET:
            _input["pin"] = pin
        if identifier is not UNSET:
            _input["identifier"] = identifier
        variables["input"] = _input
        return (
            await self.aexecute(UpdateStructureKindMutation, variables, task=task)
        ).update_structure_kind

    def update_structure_kind(
        self,
        id: str,
        key: str | None | UnsetType = UNSET,
        description: str | None | UnsetType = UNSET,
        ontology_references: Iterable[OntologyReferenceInput]
        | None
        | UnsetType = UNSET,
        color: Iterable[int] | None | UnsetType = UNSET,
        image: str | None | UnsetType = UNSET,
        label: str | None | UnsetType = UNSET,
        pin: bool | None | UnsetType = UNSET,
        identifier: str | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> StructureKind:
        """UpdateStructureKind
         StructureKind and MetricKind are minted by the write that first needs them — there is no
         create mutation for either, only these.

        Args:
            id: The ID of the definition to update
            key: The label of the node participating in the event
            description: Description of this node role
            ontology_references: Ontology references for this event
            color: Optional RGBA color for this node role (e.g. [255, 0, 0, 128])
            image: Optional media store ID for an image representing this node role
            label: Optional human-readable label for this node role (defaults to 'key' if not provided)
            pin: Whether to pin this node role in the UI
            identifier: Read by nothing: `(organization, identifier)` is a structure kind's identity and cannot be reassigned. `update_structure_kind` writes label, description and colour only
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            StructureKind"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        if key is not UNSET:
            _input["key"] = key
        if description is not UNSET:
            _input["description"] = description
        if ontology_references is not UNSET:
            _input["ontologyReferences"] = ontology_references
        if color is not UNSET:
            _input["color"] = color
        if image is not UNSET:
            _input["image"] = image
        if label is not UNSET:
            _input["label"] = label
        if pin is not UNSET:
            _input["pin"] = pin
        if identifier is not UNSET:
            _input["identifier"] = identifier
        variables["input"] = _input
        return self.execute(
            UpdateStructureKindMutation, variables, task=task
        ).update_structure_kind

    async def adelete_structure_kind(self, id: str, task: TaskLike | None = None) -> ID:
        """DeleteStructureKind

        Retire a structure kind. Refused while any structure is recorded under it — evidence is never deleted; retract the structures first

        Args:
            id: The ID of the structure kind to retire
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            ID"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        variables["input"] = _input
        return (
            await self.aexecute(DeleteStructureKindMutation, variables, task=task)
        ).delete_structure_kind

    def delete_structure_kind(self, id: str, task: TaskLike | None = None) -> ID:
        """DeleteStructureKind

        Retire a structure kind. Refused while any structure is recorded under it — evidence is never deleted; retract the structures first

        Args:
            id: The ID of the structure kind to retire
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            ID"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        variables["input"] = _input
        return self.execute(
            DeleteStructureKindMutation, variables, task=task
        ).delete_structure_kind

    async def aupdate_metric_kind(
        self,
        id: str,
        key: str | None | UnsetType = UNSET,
        description: str | None | UnsetType = UNSET,
        ontology_references: Iterable[OntologyReferenceInput]
        | None
        | UnsetType = UNSET,
        color: Iterable[int] | None | UnsetType = UNSET,
        image: str | None | UnsetType = UNSET,
        label: str | None | UnsetType = UNSET,
        pin: bool | None | UnsetType = UNSET,
        identifier: str | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> MetricKind:
        """UpdateMetricKind

        Update a metric kind's label, description or colour

        Args:
            id: The ID of the definition to update
            key: The label of the node participating in the event
            description: Description of this node role
            ontology_references: Ontology references for this event
            color: Optional RGBA color for this node role (e.g. [255, 0, 0, 128])
            image: Optional media store ID for an image representing this node role
            label: Optional human-readable label for this node role (defaults to 'key' if not provided)
            pin: Whether to pin this node role in the UI
            identifier: Read by nothing: a metric kind is identified by `(organization, structure_kind, key, value_kind)`. `update_metric_kind` writes label, description and colour only
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            MetricKind"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        if key is not UNSET:
            _input["key"] = key
        if description is not UNSET:
            _input["description"] = description
        if ontology_references is not UNSET:
            _input["ontologyReferences"] = ontology_references
        if color is not UNSET:
            _input["color"] = color
        if image is not UNSET:
            _input["image"] = image
        if label is not UNSET:
            _input["label"] = label
        if pin is not UNSET:
            _input["pin"] = pin
        if identifier is not UNSET:
            _input["identifier"] = identifier
        variables["input"] = _input
        return (
            await self.aexecute(UpdateMetricKindMutation, variables, task=task)
        ).update_metric_kind

    def update_metric_kind(
        self,
        id: str,
        key: str | None | UnsetType = UNSET,
        description: str | None | UnsetType = UNSET,
        ontology_references: Iterable[OntologyReferenceInput]
        | None
        | UnsetType = UNSET,
        color: Iterable[int] | None | UnsetType = UNSET,
        image: str | None | UnsetType = UNSET,
        label: str | None | UnsetType = UNSET,
        pin: bool | None | UnsetType = UNSET,
        identifier: str | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> MetricKind:
        """UpdateMetricKind

        Update a metric kind's label, description or colour

        Args:
            id: The ID of the definition to update
            key: The label of the node participating in the event
            description: Description of this node role
            ontology_references: Ontology references for this event
            color: Optional RGBA color for this node role (e.g. [255, 0, 0, 128])
            image: Optional media store ID for an image representing this node role
            label: Optional human-readable label for this node role (defaults to 'key' if not provided)
            pin: Whether to pin this node role in the UI
            identifier: Read by nothing: a metric kind is identified by `(organization, structure_kind, key, value_kind)`. `update_metric_kind` writes label, description and colour only
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            MetricKind"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        if key is not UNSET:
            _input["key"] = key
        if description is not UNSET:
            _input["description"] = description
        if ontology_references is not UNSET:
            _input["ontologyReferences"] = ontology_references
        if color is not UNSET:
            _input["color"] = color
        if image is not UNSET:
            _input["image"] = image
        if label is not UNSET:
            _input["label"] = label
        if pin is not UNSET:
            _input["pin"] = pin
        if identifier is not UNSET:
            _input["identifier"] = identifier
        variables["input"] = _input
        return self.execute(
            UpdateMetricKindMutation, variables, task=task
        ).update_metric_kind

    async def adelete_metric_kind(self, id: str, task: TaskLike | None = None) -> ID:
        """DeleteMetricKind

        Retire a metric kind. Refused while any metric is recorded under it — evidence is never deleted; retract the metrics first

        Args:
            id: The ID of the metric kind to retire
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            ID"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        variables["input"] = _input
        return (
            await self.aexecute(DeleteMetricKindMutation, variables, task=task)
        ).delete_metric_kind

    def delete_metric_kind(self, id: str, task: TaskLike | None = None) -> ID:
        """DeleteMetricKind

        Retire a metric kind. Refused while any metric is recorded under it — evidence is never deleted; retract the metrics first

        Args:
            id: The ID of the metric kind to retire
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            ID"""
        variables: dict[str, builtins.object] = {}
        _input: dict[str, builtins.object] = {}
        _input["id"] = id
        variables["input"] = _input
        return self.execute(
            DeleteMetricKindMutation, variables, task=task
        ).delete_metric_kind

    async def aget_entity_category(
        self, id: IDCoercible, task: TaskLike | None = None
    ) -> EntityCategory:
        """GetEntityCategory

        Get a single entity category by ID

        Args:
            id (ID): No description
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            EntityCategory"""
        variables: dict[str, builtins.object] = {}
        variables["id"] = id
        return (
            await self.aexecute(GetEntityCategoryQuery, variables, task=task)
        ).entity_category

    def get_entity_category(
        self, id: IDCoercible, task: TaskLike | None = None
    ) -> EntityCategory:
        """GetEntityCategory

        Get a single entity category by ID

        Args:
            id (ID): No description
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            EntityCategory"""
        variables: dict[str, builtins.object] = {}
        variables["id"] = id
        return self.execute(
            GetEntityCategoryQuery, variables, task=task
        ).entity_category

    async def alist_entity_categories(
        self,
        filters: EntityCategoryFilter | None | UnsetType = UNSET,
        pagination: OffsetPaginationInput | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> tuple[EntityCategory, ...]:
        """ListEntityCategories

        List all entity categories

        Args:
            filters (EntityCategoryFilter | None, optional): No description.
            pagination (OffsetPaginationInput | None, optional): No description.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            list[EntityCategory]"""
        variables: dict[str, builtins.object] = {}
        if filters is not UNSET:
            variables["filters"] = filters
        if pagination is not UNSET:
            variables["pagination"] = pagination
        return (
            await self.aexecute(ListEntityCategoriesQuery, variables, task=task)
        ).entity_categories

    def list_entity_categories(
        self,
        filters: EntityCategoryFilter | None | UnsetType = UNSET,
        pagination: OffsetPaginationInput | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> tuple[EntityCategory, ...]:
        """ListEntityCategories

        List all entity categories

        Args:
            filters (EntityCategoryFilter | None, optional): No description.
            pagination (OffsetPaginationInput | None, optional): No description.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            list[EntityCategory]"""
        variables: dict[str, builtins.object] = {}
        if filters is not UNSET:
            variables["filters"] = filters
        if pagination is not UNSET:
            variables["pagination"] = pagination
        return self.execute(
            ListEntityCategoriesQuery, variables, task=task
        ).entity_categories

    async def asearch_entity_categories(
        self,
        search: str | None | UnsetType = UNSET,
        values: list[IDCoercible] | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> tuple[SearchEntityCategoriesQueryOptions, ...]:
        """SearchEntityCategories

        List all entity categories

        Args:
            search (str | None, optional): No description.
            values (list[ID] | None, optional): No description.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            list[SearchEntityCategoriesQueryEntityCategories]"""
        variables: dict[str, builtins.object] = {}
        if search is not UNSET:
            variables["search"] = search
        if values is not UNSET:
            variables["values"] = values
        return (
            await self.aexecute(SearchEntityCategoriesQuery, variables, task=task)
        ).options

    def search_entity_categories(
        self,
        search: str | None | UnsetType = UNSET,
        values: list[IDCoercible] | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> tuple[SearchEntityCategoriesQueryOptions, ...]:
        """SearchEntityCategories

        List all entity categories

        Args:
            search (str | None, optional): No description.
            values (list[ID] | None, optional): No description.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            list[SearchEntityCategoriesQueryEntityCategories]"""
        variables: dict[str, builtins.object] = {}
        if search is not UNSET:
            variables["search"] = search
        if values is not UNSET:
            variables["values"] = values
        return self.execute(SearchEntityCategoriesQuery, variables, task=task).options

    async def aget_relation_category(
        self, id: IDCoercible, task: TaskLike | None = None
    ) -> RelationCategory:
        """GetRelationCategory

        Get a single relation category by ID

        Args:
            id (ID): No description
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            RelationCategory"""
        variables: dict[str, builtins.object] = {}
        variables["id"] = id
        return (
            await self.aexecute(GetRelationCategoryQuery, variables, task=task)
        ).relation_category

    def get_relation_category(
        self, id: IDCoercible, task: TaskLike | None = None
    ) -> RelationCategory:
        """GetRelationCategory

        Get a single relation category by ID

        Args:
            id (ID): No description
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            RelationCategory"""
        variables: dict[str, builtins.object] = {}
        variables["id"] = id
        return self.execute(
            GetRelationCategoryQuery, variables, task=task
        ).relation_category

    async def alist_relation_categories(
        self,
        filters: RelationCategoryFilter | None | UnsetType = UNSET,
        pagination: OffsetPaginationInput | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> tuple[RelationCategory, ...]:
        """ListRelationCategories

        List all relation categories

        Args:
            filters (RelationCategoryFilter | None, optional): No description.
            pagination (OffsetPaginationInput | None, optional): No description.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            list[RelationCategory]"""
        variables: dict[str, builtins.object] = {}
        if filters is not UNSET:
            variables["filters"] = filters
        if pagination is not UNSET:
            variables["pagination"] = pagination
        return (
            await self.aexecute(ListRelationCategoriesQuery, variables, task=task)
        ).relation_categories

    def list_relation_categories(
        self,
        filters: RelationCategoryFilter | None | UnsetType = UNSET,
        pagination: OffsetPaginationInput | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> tuple[RelationCategory, ...]:
        """ListRelationCategories

        List all relation categories

        Args:
            filters (RelationCategoryFilter | None, optional): No description.
            pagination (OffsetPaginationInput | None, optional): No description.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            list[RelationCategory]"""
        variables: dict[str, builtins.object] = {}
        if filters is not UNSET:
            variables["filters"] = filters
        if pagination is not UNSET:
            variables["pagination"] = pagination
        return self.execute(
            ListRelationCategoriesQuery, variables, task=task
        ).relation_categories

    async def asearch_relation_categories(
        self,
        search: str | None | UnsetType = UNSET,
        values: list[IDCoercible] | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> tuple[SearchRelationCategoriesQueryOptions, ...]:
        """SearchRelationCategories

        List all relation categories

        Args:
            search (str | None, optional): No description.
            values (list[ID] | None, optional): No description.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            list[SearchRelationCategoriesQueryRelationCategories]"""
        variables: dict[str, builtins.object] = {}
        if search is not UNSET:
            variables["search"] = search
        if values is not UNSET:
            variables["values"] = values
        return (
            await self.aexecute(SearchRelationCategoriesQuery, variables, task=task)
        ).options

    def search_relation_categories(
        self,
        search: str | None | UnsetType = UNSET,
        values: list[IDCoercible] | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> tuple[SearchRelationCategoriesQueryOptions, ...]:
        """SearchRelationCategories

        List all relation categories

        Args:
            search (str | None, optional): No description.
            values (list[ID] | None, optional): No description.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            list[SearchRelationCategoriesQueryRelationCategories]"""
        variables: dict[str, builtins.object] = {}
        if search is not UNSET:
            variables["search"] = search
        if values is not UNSET:
            variables["values"] = values
        return self.execute(SearchRelationCategoriesQuery, variables, task=task).options

    async def aget_measurement_category(
        self, id: IDCoercible, task: TaskLike | None = None
    ) -> MeasurementCategory:
        """GetMeasurementCategory

        Get a single measurement category by ID

        Args:
            id (ID): No description
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            MeasurementCategory"""
        variables: dict[str, builtins.object] = {}
        variables["id"] = id
        return (
            await self.aexecute(GetMeasurementCategoryQuery, variables, task=task)
        ).measurement_category

    def get_measurement_category(
        self, id: IDCoercible, task: TaskLike | None = None
    ) -> MeasurementCategory:
        """GetMeasurementCategory

        Get a single measurement category by ID

        Args:
            id (ID): No description
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            MeasurementCategory"""
        variables: dict[str, builtins.object] = {}
        variables["id"] = id
        return self.execute(
            GetMeasurementCategoryQuery, variables, task=task
        ).measurement_category

    async def alist_measurement_categories(
        self,
        filters: MeasurementCategoryFilter | None | UnsetType = UNSET,
        pagination: OffsetPaginationInput | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> tuple[MeasurementCategory, ...]:
        """ListMeasurementCategories

        List all measurement categories

        Args:
            filters (MeasurementCategoryFilter | None, optional): No description.
            pagination (OffsetPaginationInput | None, optional): No description.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            list[MeasurementCategory]"""
        variables: dict[str, builtins.object] = {}
        if filters is not UNSET:
            variables["filters"] = filters
        if pagination is not UNSET:
            variables["pagination"] = pagination
        return (
            await self.aexecute(ListMeasurementCategoriesQuery, variables, task=task)
        ).measurement_categories

    def list_measurement_categories(
        self,
        filters: MeasurementCategoryFilter | None | UnsetType = UNSET,
        pagination: OffsetPaginationInput | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> tuple[MeasurementCategory, ...]:
        """ListMeasurementCategories

        List all measurement categories

        Args:
            filters (MeasurementCategoryFilter | None, optional): No description.
            pagination (OffsetPaginationInput | None, optional): No description.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            list[MeasurementCategory]"""
        variables: dict[str, builtins.object] = {}
        if filters is not UNSET:
            variables["filters"] = filters
        if pagination is not UNSET:
            variables["pagination"] = pagination
        return self.execute(
            ListMeasurementCategoriesQuery, variables, task=task
        ).measurement_categories

    async def asearch_measurement_categories(
        self,
        search: str | None | UnsetType = UNSET,
        values: list[IDCoercible] | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> tuple[SearchMeasurementCategoriesQueryOptions, ...]:
        """SearchMeasurementCategories

        List all measurement categories

        Args:
            search (str | None, optional): No description.
            values (list[ID] | None, optional): No description.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            list[SearchMeasurementCategoriesQueryMeasurementCategories]"""
        variables: dict[str, builtins.object] = {}
        if search is not UNSET:
            variables["search"] = search
        if values is not UNSET:
            variables["values"] = values
        return (
            await self.aexecute(SearchMeasurementCategoriesQuery, variables, task=task)
        ).options

    def search_measurement_categories(
        self,
        search: str | None | UnsetType = UNSET,
        values: list[IDCoercible] | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> tuple[SearchMeasurementCategoriesQueryOptions, ...]:
        """SearchMeasurementCategories

        List all measurement categories

        Args:
            search (str | None, optional): No description.
            values (list[ID] | None, optional): No description.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            list[SearchMeasurementCategoriesQueryMeasurementCategories]"""
        variables: dict[str, builtins.object] = {}
        if search is not UNSET:
            variables["search"] = search
        if values is not UNSET:
            variables["values"] = values
        return self.execute(
            SearchMeasurementCategoriesQuery, variables, task=task
        ).options

    async def aget_structure_relation_category(
        self, id: IDCoercible, task: TaskLike | None = None
    ) -> StructureRelationCategory:
        """GetStructureRelationCategory

        Get a single structure relation category by ID

        Args:
            id (ID): No description
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            StructureRelationCategory"""
        variables: dict[str, builtins.object] = {}
        variables["id"] = id
        return (
            await self.aexecute(GetStructureRelationCategoryQuery, variables, task=task)
        ).structure_relation_category

    def get_structure_relation_category(
        self, id: IDCoercible, task: TaskLike | None = None
    ) -> StructureRelationCategory:
        """GetStructureRelationCategory

        Get a single structure relation category by ID

        Args:
            id (ID): No description
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            StructureRelationCategory"""
        variables: dict[str, builtins.object] = {}
        variables["id"] = id
        return self.execute(
            GetStructureRelationCategoryQuery, variables, task=task
        ).structure_relation_category

    async def alist_structure_relation_categories(
        self,
        filters: StructureRelationCategoryFilter | None | UnsetType = UNSET,
        pagination: OffsetPaginationInput | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> tuple[StructureRelationCategory, ...]:
        """ListStructureRelationCategories

        List all structure relation categories

        Args:
            filters (StructureRelationCategoryFilter | None, optional): No description.
            pagination (OffsetPaginationInput | None, optional): No description.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            list[StructureRelationCategory]"""
        variables: dict[str, builtins.object] = {}
        if filters is not UNSET:
            variables["filters"] = filters
        if pagination is not UNSET:
            variables["pagination"] = pagination
        return (
            await self.aexecute(
                ListStructureRelationCategoriesQuery, variables, task=task
            )
        ).structure_relation_categories

    def list_structure_relation_categories(
        self,
        filters: StructureRelationCategoryFilter | None | UnsetType = UNSET,
        pagination: OffsetPaginationInput | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> tuple[StructureRelationCategory, ...]:
        """ListStructureRelationCategories

        List all structure relation categories

        Args:
            filters (StructureRelationCategoryFilter | None, optional): No description.
            pagination (OffsetPaginationInput | None, optional): No description.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            list[StructureRelationCategory]"""
        variables: dict[str, builtins.object] = {}
        if filters is not UNSET:
            variables["filters"] = filters
        if pagination is not UNSET:
            variables["pagination"] = pagination
        return self.execute(
            ListStructureRelationCategoriesQuery, variables, task=task
        ).structure_relation_categories

    async def asearch_structure_relation_categories(
        self,
        search: str | None | UnsetType = UNSET,
        values: list[IDCoercible] | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> tuple[SearchStructureRelationCategoriesQueryOptions, ...]:
        """SearchStructureRelationCategories

        List all structure relation categories

        Args:
            search (str | None, optional): No description.
            values (list[ID] | None, optional): No description.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            list[SearchStructureRelationCategoriesQueryStructureRelationCategories]"""
        variables: dict[str, builtins.object] = {}
        if search is not UNSET:
            variables["search"] = search
        if values is not UNSET:
            variables["values"] = values
        return (
            await self.aexecute(
                SearchStructureRelationCategoriesQuery, variables, task=task
            )
        ).options

    def search_structure_relation_categories(
        self,
        search: str | None | UnsetType = UNSET,
        values: list[IDCoercible] | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> tuple[SearchStructureRelationCategoriesQueryOptions, ...]:
        """SearchStructureRelationCategories

        List all structure relation categories

        Args:
            search (str | None, optional): No description.
            values (list[ID] | None, optional): No description.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            list[SearchStructureRelationCategoriesQueryStructureRelationCategories]"""
        variables: dict[str, builtins.object] = {}
        if search is not UNSET:
            variables["search"] = search
        if values is not UNSET:
            variables["values"] = values
        return self.execute(
            SearchStructureRelationCategoriesQuery, variables, task=task
        ).options

    async def aget_natural_event_category(
        self, id: IDCoercible, task: TaskLike | None = None
    ) -> NaturalEventCategory:
        """GetNaturalEventCategory

        Get a single natural event category by ID

        Args:
            id (ID): No description
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            NaturalEventCategory"""
        variables: dict[str, builtins.object] = {}
        variables["id"] = id
        return (
            await self.aexecute(GetNaturalEventCategoryQuery, variables, task=task)
        ).natural_event_category

    def get_natural_event_category(
        self, id: IDCoercible, task: TaskLike | None = None
    ) -> NaturalEventCategory:
        """GetNaturalEventCategory

        Get a single natural event category by ID

        Args:
            id (ID): No description
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            NaturalEventCategory"""
        variables: dict[str, builtins.object] = {}
        variables["id"] = id
        return self.execute(
            GetNaturalEventCategoryQuery, variables, task=task
        ).natural_event_category

    async def alist_natural_event_categories(
        self,
        filters: NaturalEventCategoryFilter | None | UnsetType = UNSET,
        pagination: OffsetPaginationInput | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> tuple[NaturalEventCategory, ...]:
        """ListNaturalEventCategories

        List all natural event categories

        Args:
            filters (NaturalEventCategoryFilter | None, optional): No description.
            pagination (OffsetPaginationInput | None, optional): No description.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            list[NaturalEventCategory]"""
        variables: dict[str, builtins.object] = {}
        if filters is not UNSET:
            variables["filters"] = filters
        if pagination is not UNSET:
            variables["pagination"] = pagination
        return (
            await self.aexecute(ListNaturalEventCategoriesQuery, variables, task=task)
        ).natural_event_categories

    def list_natural_event_categories(
        self,
        filters: NaturalEventCategoryFilter | None | UnsetType = UNSET,
        pagination: OffsetPaginationInput | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> tuple[NaturalEventCategory, ...]:
        """ListNaturalEventCategories

        List all natural event categories

        Args:
            filters (NaturalEventCategoryFilter | None, optional): No description.
            pagination (OffsetPaginationInput | None, optional): No description.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            list[NaturalEventCategory]"""
        variables: dict[str, builtins.object] = {}
        if filters is not UNSET:
            variables["filters"] = filters
        if pagination is not UNSET:
            variables["pagination"] = pagination
        return self.execute(
            ListNaturalEventCategoriesQuery, variables, task=task
        ).natural_event_categories

    async def asearch_natural_event_categories(
        self,
        search: str | None | UnsetType = UNSET,
        values: list[IDCoercible] | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> tuple[SearchNaturalEventCategoriesQueryOptions, ...]:
        """SearchNaturalEventCategories

        List all natural event categories

        Args:
            search (str | None, optional): No description.
            values (list[ID] | None, optional): No description.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            list[SearchNaturalEventCategoriesQueryNaturalEventCategories]"""
        variables: dict[str, builtins.object] = {}
        if search is not UNSET:
            variables["search"] = search
        if values is not UNSET:
            variables["values"] = values
        return (
            await self.aexecute(SearchNaturalEventCategoriesQuery, variables, task=task)
        ).options

    def search_natural_event_categories(
        self,
        search: str | None | UnsetType = UNSET,
        values: list[IDCoercible] | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> tuple[SearchNaturalEventCategoriesQueryOptions, ...]:
        """SearchNaturalEventCategories

        List all natural event categories

        Args:
            search (str | None, optional): No description.
            values (list[ID] | None, optional): No description.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            list[SearchNaturalEventCategoriesQueryNaturalEventCategories]"""
        variables: dict[str, builtins.object] = {}
        if search is not UNSET:
            variables["search"] = search
        if values is not UNSET:
            variables["values"] = values
        return self.execute(
            SearchNaturalEventCategoriesQuery, variables, task=task
        ).options

    async def aget_protocol_event_category(
        self, id: IDCoercible, task: TaskLike | None = None
    ) -> ProtocolEventCategory:
        """GetProtocolEventCategory

        Get a single protocol event category by ID

        Args:
            id (ID): No description
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            ProtocolEventCategory"""
        variables: dict[str, builtins.object] = {}
        variables["id"] = id
        return (
            await self.aexecute(GetProtocolEventCategoryQuery, variables, task=task)
        ).protocol_event_category

    def get_protocol_event_category(
        self, id: IDCoercible, task: TaskLike | None = None
    ) -> ProtocolEventCategory:
        """GetProtocolEventCategory

        Get a single protocol event category by ID

        Args:
            id (ID): No description
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            ProtocolEventCategory"""
        variables: dict[str, builtins.object] = {}
        variables["id"] = id
        return self.execute(
            GetProtocolEventCategoryQuery, variables, task=task
        ).protocol_event_category

    async def alist_protocol_event_categories(
        self,
        filters: ProtocolEventCategoryFilter | None | UnsetType = UNSET,
        pagination: OffsetPaginationInput | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> tuple[ProtocolEventCategory, ...]:
        """ListProtocolEventCategories

        List all protocol event categories

        Args:
            filters (ProtocolEventCategoryFilter | None, optional): No description.
            pagination (OffsetPaginationInput | None, optional): No description.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            list[ProtocolEventCategory]"""
        variables: dict[str, builtins.object] = {}
        if filters is not UNSET:
            variables["filters"] = filters
        if pagination is not UNSET:
            variables["pagination"] = pagination
        return (
            await self.aexecute(ListProtocolEventCategoriesQuery, variables, task=task)
        ).protocol_event_categories

    def list_protocol_event_categories(
        self,
        filters: ProtocolEventCategoryFilter | None | UnsetType = UNSET,
        pagination: OffsetPaginationInput | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> tuple[ProtocolEventCategory, ...]:
        """ListProtocolEventCategories

        List all protocol event categories

        Args:
            filters (ProtocolEventCategoryFilter | None, optional): No description.
            pagination (OffsetPaginationInput | None, optional): No description.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            list[ProtocolEventCategory]"""
        variables: dict[str, builtins.object] = {}
        if filters is not UNSET:
            variables["filters"] = filters
        if pagination is not UNSET:
            variables["pagination"] = pagination
        return self.execute(
            ListProtocolEventCategoriesQuery, variables, task=task
        ).protocol_event_categories

    async def asearch_protocol_event_categories(
        self,
        search: str | None | UnsetType = UNSET,
        values: list[IDCoercible] | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> tuple[SearchProtocolEventCategoriesQueryOptions, ...]:
        """SearchProtocolEventCategories

        List all protocol event categories

        Args:
            search (str | None, optional): No description.
            values (list[ID] | None, optional): No description.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            list[SearchProtocolEventCategoriesQueryProtocolEventCategories]"""
        variables: dict[str, builtins.object] = {}
        if search is not UNSET:
            variables["search"] = search
        if values is not UNSET:
            variables["values"] = values
        return (
            await self.aexecute(
                SearchProtocolEventCategoriesQuery, variables, task=task
            )
        ).options

    def search_protocol_event_categories(
        self,
        search: str | None | UnsetType = UNSET,
        values: list[IDCoercible] | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> tuple[SearchProtocolEventCategoriesQueryOptions, ...]:
        """SearchProtocolEventCategories

        List all protocol event categories

        Args:
            search (str | None, optional): No description.
            values (list[ID] | None, optional): No description.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            list[SearchProtocolEventCategoriesQueryProtocolEventCategories]"""
        variables: dict[str, builtins.object] = {}
        if search is not UNSET:
            variables["search"] = search
        if values is not UNSET:
            variables["values"] = values
        return self.execute(
            SearchProtocolEventCategoriesQuery, variables, task=task
        ).options

    async def aget_instance(
        self, id: IDCoercible, task: TaskLike | None = None
    ) -> Instance:
        """GetInstance
         Claim-grain reads: organization scope, addressed by a bare uuid, no graph argument.
         `instance(id:)` is the fallback reader for a node no view draws.

        Args:
            id (ID): No description
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            Instance"""
        variables: dict[str, builtins.object] = {}
        variables["id"] = id
        return (await self.aexecute(GetInstanceQuery, variables, task=task)).instance

    def get_instance(self, id: IDCoercible, task: TaskLike | None = None) -> Instance:
        """GetInstance
         Claim-grain reads: organization scope, addressed by a bare uuid, no graph argument.
         `instance(id:)` is the fallback reader for a node no view draws.

        Args:
            id (ID): No description
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            Instance"""
        variables: dict[str, builtins.object] = {}
        variables["id"] = id
        return self.execute(GetInstanceQuery, variables, task=task).instance

    async def aget_link(self, id: IDCoercible, task: TaskLike | None = None) -> Link:
        """GetLink

        Get one claim relating two things by ID, as the log has it

        Args:
            id (ID): No description
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            Link"""
        variables: dict[str, builtins.object] = {}
        variables["id"] = id
        return (await self.aexecute(GetLinkQuery, variables, task=task)).link

    def get_link(self, id: IDCoercible, task: TaskLike | None = None) -> Link:
        """GetLink

        Get one claim relating two things by ID, as the log has it

        Args:
            id (ID): No description
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            Link"""
        variables: dict[str, builtins.object] = {}
        variables["id"] = id
        return self.execute(GetLinkQuery, variables, task=task).link

    async def aget_standings(
        self, id: IDCoercible, task: TaskLike | None = None
    ) -> tuple[Standing, ...]:
        """GetStandings
         Every position anyone has taken on a claim, newest first. An empty list means nobody has
         disputed it — silence is not dissent, and there is no folded boolean beside this.

        Args:
            id (ID): No description
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            list[Standing]"""
        variables: dict[str, builtins.object] = {}
        variables["id"] = id
        return (await self.aexecute(GetStandingsQuery, variables, task=task)).standings

    def get_standings(
        self, id: IDCoercible, task: TaskLike | None = None
    ) -> tuple[Standing, ...]:
        """GetStandings
         Every position anyone has taken on a claim, newest first. An empty list means nobody has
         disputed it — silence is not dissent, and there is no folded boolean beside this.

        Args:
            id (ID): No description
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            list[Standing]"""
        variables: dict[str, builtins.object] = {}
        variables["id"] = id
        return self.execute(GetStandingsQuery, variables, task=task).standings

    async def aget_structure(
        self, id: IDCoercible, task: TaskLike | None = None
    ) -> StructureWithMetrics:
        """GetStructure

        Get a structure by ID — a bare uuid, its evidence primary key

        Args:
            id (ID): No description
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            StructureWithMetrics"""
        variables: dict[str, builtins.object] = {}
        variables["id"] = id
        return (await self.aexecute(GetStructureQuery, variables, task=task)).structure

    def get_structure(
        self, id: IDCoercible, task: TaskLike | None = None
    ) -> StructureWithMetrics:
        """GetStructure

        Get a structure by ID — a bare uuid, its evidence primary key

        Args:
            id (ID): No description
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            StructureWithMetrics"""
        variables: dict[str, builtins.object] = {}
        variables["id"] = id
        return self.execute(GetStructureQuery, variables, task=task).structure

    async def aget_structure_by_identifier(
        self,
        identifier: StructureIdentifierCoercible,
        object: StructureObjectCoercible,
        task: TaskLike | None = None,
    ) -> StructureWithMetrics:
        """GetStructureByIdentifier

        Get a structure by identifier and object. No graph: a structure belongs to the organization and has no vertex in any projection

        Args:
            identifier (StructureIdentifier): No description
            object (StructureObject): No description
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            StructureWithMetrics"""
        variables: dict[str, builtins.object] = {}
        variables["identifier"] = identifier
        variables["object"] = object
        return (
            await self.aexecute(GetStructureByIdentifierQuery, variables, task=task)
        ).structure_by_identifier

    def get_structure_by_identifier(
        self,
        identifier: StructureIdentifierCoercible,
        object: StructureObjectCoercible,
        task: TaskLike | None = None,
    ) -> StructureWithMetrics:
        """GetStructureByIdentifier

        Get a structure by identifier and object. No graph: a structure belongs to the organization and has no vertex in any projection

        Args:
            identifier (StructureIdentifier): No description
            object (StructureObject): No description
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            StructureWithMetrics"""
        variables: dict[str, builtins.object] = {}
        variables["identifier"] = identifier
        variables["object"] = object
        return self.execute(
            GetStructureByIdentifierQuery, variables, task=task
        ).structure_by_identifier

    async def aget_informing_structures(
        self, entity_id: str, task: TaskLike | None = None
    ) -> tuple[Structure, ...]:
        """GetInformingStructures
         Resolves a naming structure back to what it names — this is how an external id is looked up
         now that `externalId` no longer exists on any write.

        Args:
            entity_id (str): No description
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            list[Structure]"""
        variables: dict[str, builtins.object] = {}
        variables["entityId"] = entity_id
        return (
            await self.aexecute(GetInformingStructuresQuery, variables, task=task)
        ).informing_structures

    def get_informing_structures(
        self, entity_id: str, task: TaskLike | None = None
    ) -> tuple[Structure, ...]:
        """GetInformingStructures
         Resolves a naming structure back to what it names — this is how an external id is looked up
         now that `externalId` no longer exists on any write.

        Args:
            entity_id (str): No description
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            list[Structure]"""
        variables: dict[str, builtins.object] = {}
        variables["entityId"] = entity_id
        return self.execute(
            GetInformingStructuresQuery, variables, task=task
        ).informing_structures

    async def alist_structures(
        self,
        structure_kind_id: IDCoercible | None | UnsetType = UNSET,
        filters: StructureFilter | None | UnsetType = UNSET,
        ordering: list[StructureOrder] | None | UnsetType = UNSET,
        pagination: StructurePaginationInput | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> tuple[Structure, ...]:
        """ListStructures

        List structures with optional filters, ordering, and pagination

        Args:
            structure_kind_id (ID | None, optional): No description.
            filters (StructureFilter | None, optional): No description.
            ordering (list[StructureOrder] | None, optional): No description.
            pagination (StructurePaginationInput | None, optional): No description.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            list[Structure]"""
        variables: dict[str, builtins.object] = {}
        if structure_kind_id is not UNSET:
            variables["structureKindId"] = structure_kind_id
        if filters is not UNSET:
            variables["filters"] = filters
        if ordering is not UNSET:
            variables["ordering"] = ordering
        if pagination is not UNSET:
            variables["pagination"] = pagination
        return (
            await self.aexecute(ListStructuresQuery, variables, task=task)
        ).structures

    def list_structures(
        self,
        structure_kind_id: IDCoercible | None | UnsetType = UNSET,
        filters: StructureFilter | None | UnsetType = UNSET,
        ordering: list[StructureOrder] | None | UnsetType = UNSET,
        pagination: StructurePaginationInput | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> tuple[Structure, ...]:
        """ListStructures

        List structures with optional filters, ordering, and pagination

        Args:
            structure_kind_id (ID | None, optional): No description.
            filters (StructureFilter | None, optional): No description.
            ordering (list[StructureOrder] | None, optional): No description.
            pagination (StructurePaginationInput | None, optional): No description.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            list[Structure]"""
        variables: dict[str, builtins.object] = {}
        if structure_kind_id is not UNSET:
            variables["structureKindId"] = structure_kind_id
        if filters is not UNSET:
            variables["filters"] = filters
        if ordering is not UNSET:
            variables["ordering"] = ordering
        if pagination is not UNSET:
            variables["pagination"] = pagination
        return self.execute(ListStructuresQuery, variables, task=task).structures

    async def aget_metric(
        self, id: IDCoercible, task: TaskLike | None = None
    ) -> Metric:
        """GetMetric

        Get a metric by ID

        Args:
            id (ID): No description
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            Metric"""
        variables: dict[str, builtins.object] = {}
        variables["id"] = id
        return (await self.aexecute(GetMetricQuery, variables, task=task)).metric

    def get_metric(self, id: IDCoercible, task: TaskLike | None = None) -> Metric:
        """GetMetric

        Get a metric by ID

        Args:
            id (ID): No description
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            Metric"""
        variables: dict[str, builtins.object] = {}
        variables["id"] = id
        return self.execute(GetMetricQuery, variables, task=task).metric

    async def aget_metrics_for_structure(
        self, structure_id: IDCoercible, task: TaskLike | None = None
    ) -> tuple[Metric, ...]:
        """GetMetricsForStructure

        List every un-retracted metric describing a structure

        Args:
            structure_id (ID): No description
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            list[Metric]"""
        variables: dict[str, builtins.object] = {}
        variables["structureId"] = structure_id
        return (
            await self.aexecute(GetMetricsForStructureQuery, variables, task=task)
        ).metrics_for_structure

    def get_metrics_for_structure(
        self, structure_id: IDCoercible, task: TaskLike | None = None
    ) -> tuple[Metric, ...]:
        """GetMetricsForStructure

        List every un-retracted metric describing a structure

        Args:
            structure_id (ID): No description
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            list[Metric]"""
        variables: dict[str, builtins.object] = {}
        variables["structureId"] = structure_id
        return self.execute(
            GetMetricsForStructureQuery, variables, task=task
        ).metrics_for_structure

    async def aget_comment(
        self, id: IDCoercible, task: TaskLike | None = None
    ) -> Comment:
        """GetComment

        Get one remark by ID, as the log has it

        Args:
            id (ID): No description
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            Comment"""
        variables: dict[str, builtins.object] = {}
        variables["id"] = id
        return (await self.aexecute(GetCommentQuery, variables, task=task)).comment

    def get_comment(self, id: IDCoercible, task: TaskLike | None = None) -> Comment:
        """GetComment

        Get one remark by ID, as the log has it

        Args:
            id (ID): No description
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            Comment"""
        variables: dict[str, builtins.object] = {}
        variables["id"] = id
        return self.execute(GetCommentQuery, variables, task=task).comment

    async def aget_comments_for(
        self, identifier: str, object: IDCoercible, task: TaskLike | None = None
    ) -> tuple[Comment, ...]:
        """GetCommentsFor

        Every remark about one external datum, addressed by (identifier, object), newest first — resolved ones included

        Args:
            identifier (str): No description
            object (ID): No description
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            list[Comment]"""
        variables: dict[str, builtins.object] = {}
        variables["identifier"] = identifier
        variables["object"] = object
        return (
            await self.aexecute(GetCommentsForQuery, variables, task=task)
        ).comments_for

    def get_comments_for(
        self, identifier: str, object: IDCoercible, task: TaskLike | None = None
    ) -> tuple[Comment, ...]:
        """GetCommentsFor

        Every remark about one external datum, addressed by (identifier, object), newest first — resolved ones included

        Args:
            identifier (str): No description
            object (ID): No description
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            list[Comment]"""
        variables: dict[str, builtins.object] = {}
        variables["identifier"] = identifier
        variables["object"] = object
        return self.execute(GetCommentsForQuery, variables, task=task).comments_for

    async def asearch_structures(
        self,
        search: str | None | UnsetType = UNSET,
        values: list[IDCoercible] | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> tuple[SearchStructuresQueryOptions, ...]:
        """SearchStructures

        List structures with optional filters, ordering, and pagination

        Args:
            search (str | None, optional): No description.
            values (list[ID] | None, optional): No description.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            list[SearchStructuresQueryStructures]"""
        variables: dict[str, builtins.object] = {}
        if search is not UNSET:
            variables["search"] = search
        if values is not UNSET:
            variables["values"] = values
        return (
            await self.aexecute(SearchStructuresQuery, variables, task=task)
        ).options

    def search_structures(
        self,
        search: str | None | UnsetType = UNSET,
        values: list[IDCoercible] | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> tuple[SearchStructuresQueryOptions, ...]:
        """SearchStructures

        List structures with optional filters, ordering, and pagination

        Args:
            search (str | None, optional): No description.
            values (list[ID] | None, optional): No description.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            list[SearchStructuresQueryStructures]"""
        variables: dict[str, builtins.object] = {}
        if search is not UNSET:
            variables["search"] = search
        if values is not UNSET:
            variables["values"] = values
        return self.execute(SearchStructuresQuery, variables, task=task).options

    async def aget_graph(self, id: IDCoercible, task: TaskLike | None = None) -> Graph:
        """GetGraph

        Get a graph by ID

        Args:
            id (ID): No description
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            Graph"""
        variables: dict[str, builtins.object] = {}
        variables["id"] = id
        return (await self.aexecute(GetGraphQuery, variables, task=task)).graph

    def get_graph(self, id: IDCoercible, task: TaskLike | None = None) -> Graph:
        """GetGraph

        Get a graph by ID

        Args:
            id (ID): No description
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            Graph"""
        variables: dict[str, builtins.object] = {}
        variables["id"] = id
        return self.execute(GetGraphQuery, variables, task=task).graph

    async def alist_graphs(
        self,
        filters: GraphFilter | None | UnsetType = UNSET,
        pagination: OffsetPaginationInput | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> tuple[ListGraph, ...]:
        """ListGraphs

        List all graphs in the graph engine

        Args:
            filters (GraphFilter | None, optional): No description.
            pagination (OffsetPaginationInput | None, optional): No description.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            list[ListGraph]"""
        variables: dict[str, builtins.object] = {}
        if filters is not UNSET:
            variables["filters"] = filters
        if pagination is not UNSET:
            variables["pagination"] = pagination
        return (await self.aexecute(ListGraphsQuery, variables, task=task)).graphs

    def list_graphs(
        self,
        filters: GraphFilter | None | UnsetType = UNSET,
        pagination: OffsetPaginationInput | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> tuple[ListGraph, ...]:
        """ListGraphs

        List all graphs in the graph engine

        Args:
            filters (GraphFilter | None, optional): No description.
            pagination (OffsetPaginationInput | None, optional): No description.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            list[ListGraph]"""
        variables: dict[str, builtins.object] = {}
        if filters is not UNSET:
            variables["filters"] = filters
        if pagination is not UNSET:
            variables["pagination"] = pagination
        return self.execute(ListGraphsQuery, variables, task=task).graphs

    async def asearch_graphs(
        self,
        search: str | None | UnsetType = UNSET,
        values: list[IDCoercible] | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> tuple[SearchGraphsQueryOptions, ...]:
        """SearchGraphs

        List all graphs in the graph engine

        Args:
            search (str | None, optional): No description.
            values (list[ID] | None, optional): No description.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            list[SearchGraphsQueryGraphs]"""
        variables: dict[str, builtins.object] = {}
        if search is not UNSET:
            variables["search"] = search
        if values is not UNSET:
            variables["values"] = values
        return (await self.aexecute(SearchGraphsQuery, variables, task=task)).options

    def search_graphs(
        self,
        search: str | None | UnsetType = UNSET,
        values: list[IDCoercible] | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> tuple[SearchGraphsQueryOptions, ...]:
        """SearchGraphs

        List all graphs in the graph engine

        Args:
            search (str | None, optional): No description.
            values (list[ID] | None, optional): No description.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            list[SearchGraphsQueryGraphs]"""
        variables: dict[str, builtins.object] = {}
        if search is not UNSET:
            variables["search"] = search
        if values is not UNSET:
            variables["values"] = values
        return self.execute(SearchGraphsQuery, variables, task=task).options

    async def aget_node(
        self, id: IDCoercible, graph: IDCoercible, task: TaskLike | None = None
    ) -> Annotated[
        GetNodeQueryNodeBaseEntity
        | GetNodeQueryNodeBaseNaturalEvent
        | GetNodeQueryNodeBaseProtocolEvent,
        Field(discriminator="typename"),
    ] | GetNodeQueryNodeBaseCatchAll:
        """GetNode
         View-grain reads: these name their view, and refuse a node the view does not admit.
         `node(id, graph)` succeeds exactly when `nodes(graph:)` could list it.

        Args:
            id (ID): No description
            graph (ID): No description
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            NodeRef"""
        variables: dict[str, builtins.object] = {}
        variables["id"] = id
        variables["graph"] = graph
        return (await self.aexecute(GetNodeQuery, variables, task=task)).node

    def get_node(
        self, id: IDCoercible, graph: IDCoercible, task: TaskLike | None = None
    ) -> (
        Annotated[
            GetNodeQueryNodeBaseEntity
            | GetNodeQueryNodeBaseNaturalEvent
            | GetNodeQueryNodeBaseProtocolEvent,
            Field(discriminator="typename"),
        ]
        | GetNodeQueryNodeBaseCatchAll
    ):
        """GetNode
         View-grain reads: these name their view, and refuse a node the view does not admit.
         `node(id, graph)` succeeds exactly when `nodes(graph:)` could list it.

        Args:
            id (ID): No description
            graph (ID): No description
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            NodeRef"""
        variables: dict[str, builtins.object] = {}
        variables["id"] = id
        variables["graph"] = graph
        return self.execute(GetNodeQuery, variables, task=task).node

    async def alist_nodes(
        self,
        graph: IDCoercible,
        filters: NodeFilters | None | UnsetType = UNSET,
        ordering: list[NodeOrder] | None | UnsetType = UNSET,
        pagination: NodePaginationInput | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> tuple[
        Annotated[
            ListNodesQueryNodesBaseEntity
            | ListNodesQueryNodesBaseNaturalEvent
            | ListNodesQueryNodesBaseProtocolEvent,
            Field(discriminator="typename"),
        ]
        | ListNodesQueryNodesBaseCatchAll,
        ...,
    ]:
        """ListNodes

        List the individuals a view holds, as it draws them — view grain: one row per individual, membership from the view's rule, properties as of the view's cursor

        Args:
            graph (ID): No description
            filters (NodeFilters | None, optional): No description.
            ordering (list[NodeOrder] | None, optional): No description.
            pagination (NodePaginationInput | None, optional): No description.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            list[NodeRef]"""
        variables: dict[str, builtins.object] = {}
        variables["graph"] = graph
        if filters is not UNSET:
            variables["filters"] = filters
        if ordering is not UNSET:
            variables["ordering"] = ordering
        if pagination is not UNSET:
            variables["pagination"] = pagination
        return (await self.aexecute(ListNodesQuery, variables, task=task)).nodes

    def list_nodes(
        self,
        graph: IDCoercible,
        filters: NodeFilters | None | UnsetType = UNSET,
        ordering: list[NodeOrder] | None | UnsetType = UNSET,
        pagination: NodePaginationInput | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> tuple[
        Annotated[
            ListNodesQueryNodesBaseEntity
            | ListNodesQueryNodesBaseNaturalEvent
            | ListNodesQueryNodesBaseProtocolEvent,
            Field(discriminator="typename"),
        ]
        | ListNodesQueryNodesBaseCatchAll,
        ...,
    ]:
        """ListNodes

        List the individuals a view holds, as it draws them — view grain: one row per individual, membership from the view's rule, properties as of the view's cursor

        Args:
            graph (ID): No description
            filters (NodeFilters | None, optional): No description.
            ordering (list[NodeOrder] | None, optional): No description.
            pagination (NodePaginationInput | None, optional): No description.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            list[NodeRef]"""
        variables: dict[str, builtins.object] = {}
        variables["graph"] = graph
        if filters is not UNSET:
            variables["filters"] = filters
        if ordering is not UNSET:
            variables["ordering"] = ordering
        if pagination is not UNSET:
            variables["pagination"] = pagination
        return self.execute(ListNodesQuery, variables, task=task).nodes

    async def aget_entity(
        self, id: IDCoercible, graph: IDCoercible, task: TaskLike | None = None
    ) -> EntityView:
        """GetEntity
         richProperties is where derived values surface — the only place a metric recorded on an
         evidence structure becomes readable as a property of the node.

        Args:
            id (ID): No description
            graph (ID): No description
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            EntityView"""
        variables: dict[str, builtins.object] = {}
        variables["id"] = id
        variables["graph"] = graph
        return (await self.aexecute(GetEntityQuery, variables, task=task)).entity

    def get_entity(
        self, id: IDCoercible, graph: IDCoercible, task: TaskLike | None = None
    ) -> EntityView:
        """GetEntity
         richProperties is where derived values surface — the only place a metric recorded on an
         evidence structure becomes readable as a property of the node.

        Args:
            id (ID): No description
            graph (ID): No description
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            EntityView"""
        variables: dict[str, builtins.object] = {}
        variables["id"] = id
        variables["graph"] = graph
        return self.execute(GetEntityQuery, variables, task=task).entity

    async def aget_term(self, id: IDCoercible, task: TaskLike | None = None) -> Term:
        """GetTerm

        Get one of the organization's words by ID

        Args:
            id (ID): No description
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            Term"""
        variables: dict[str, builtins.object] = {}
        variables["id"] = id
        return (await self.aexecute(GetTermQuery, variables, task=task)).term

    def get_term(self, id: IDCoercible, task: TaskLike | None = None) -> Term:
        """GetTerm

        Get one of the organization's words by ID

        Args:
            id (ID): No description
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            Term"""
        variables: dict[str, builtins.object] = {}
        variables["id"] = id
        return self.execute(GetTermQuery, variables, task=task).term

    async def alist_terms(
        self,
        filters: TermFilter | None | UnsetType = UNSET,
        pagination: VocabularyPaginationInput | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> tuple[Term, ...]:
        """ListTerms

        List the organization's words — its vocabulary, independent of any graph

        Args:
            filters (TermFilter | None, optional): No description.
            pagination (VocabularyPaginationInput | None, optional): No description.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            list[Term]"""
        variables: dict[str, builtins.object] = {}
        if filters is not UNSET:
            variables["filters"] = filters
        if pagination is not UNSET:
            variables["pagination"] = pagination
        return (await self.aexecute(ListTermsQuery, variables, task=task)).terms

    def list_terms(
        self,
        filters: TermFilter | None | UnsetType = UNSET,
        pagination: VocabularyPaginationInput | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> tuple[Term, ...]:
        """ListTerms

        List the organization's words — its vocabulary, independent of any graph

        Args:
            filters (TermFilter | None, optional): No description.
            pagination (VocabularyPaginationInput | None, optional): No description.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            list[Term]"""
        variables: dict[str, builtins.object] = {}
        if filters is not UNSET:
            variables["filters"] = filters
        if pagination is not UNSET:
            variables["pagination"] = pagination
        return self.execute(ListTermsQuery, variables, task=task).terms

    async def asearch_terms(
        self,
        search: str | None | UnsetType = UNSET,
        values: list[IDCoercible] | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> tuple[SearchTermsQueryOptions, ...]:
        """SearchTerms

        List the organization's words — its vocabulary, independent of any graph

        Args:
            search (str | None, optional): No description.
            values (list[ID] | None, optional): No description.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            list[SearchTermsQueryTerms]"""
        variables: dict[str, builtins.object] = {}
        if search is not UNSET:
            variables["search"] = search
        if values is not UNSET:
            variables["values"] = values
        return (await self.aexecute(SearchTermsQuery, variables, task=task)).options

    def search_terms(
        self,
        search: str | None | UnsetType = UNSET,
        values: list[IDCoercible] | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> tuple[SearchTermsQueryOptions, ...]:
        """SearchTerms

        List the organization's words — its vocabulary, independent of any graph

        Args:
            search (str | None, optional): No description.
            values (list[ID] | None, optional): No description.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            list[SearchTermsQueryTerms]"""
        variables: dict[str, builtins.object] = {}
        if search is not UNSET:
            variables["search"] = search
        if values is not UNSET:
            variables["values"] = values
        return self.execute(SearchTermsQuery, variables, task=task).options

    async def aget_structure_kind(
        self, id: IDCoercible, task: TaskLike | None = None
    ) -> StructureKind:
        """GetStructureKind

        Get one structure kind by ID

        Args:
            id (ID): No description
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            StructureKind"""
        variables: dict[str, builtins.object] = {}
        variables["id"] = id
        return (
            await self.aexecute(GetStructureKindQuery, variables, task=task)
        ).structure_kind

    def get_structure_kind(
        self, id: IDCoercible, task: TaskLike | None = None
    ) -> StructureKind:
        """GetStructureKind

        Get one structure kind by ID

        Args:
            id (ID): No description
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            StructureKind"""
        variables: dict[str, builtins.object] = {}
        variables["id"] = id
        return self.execute(GetStructureKindQuery, variables, task=task).structure_kind

    async def alist_structure_kinds(
        self,
        filters: StructureKindFilter | None | UnsetType = UNSET,
        pagination: VocabularyPaginationInput | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> tuple[StructureKind, ...]:
        """ListStructureKinds

        List the organization's structure kinds

        Args:
            filters (StructureKindFilter | None, optional): No description.
            pagination (VocabularyPaginationInput | None, optional): No description.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            list[StructureKind]"""
        variables: dict[str, builtins.object] = {}
        if filters is not UNSET:
            variables["filters"] = filters
        if pagination is not UNSET:
            variables["pagination"] = pagination
        return (
            await self.aexecute(ListStructureKindsQuery, variables, task=task)
        ).structure_kinds

    def list_structure_kinds(
        self,
        filters: StructureKindFilter | None | UnsetType = UNSET,
        pagination: VocabularyPaginationInput | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> tuple[StructureKind, ...]:
        """ListStructureKinds

        List the organization's structure kinds

        Args:
            filters (StructureKindFilter | None, optional): No description.
            pagination (VocabularyPaginationInput | None, optional): No description.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            list[StructureKind]"""
        variables: dict[str, builtins.object] = {}
        if filters is not UNSET:
            variables["filters"] = filters
        if pagination is not UNSET:
            variables["pagination"] = pagination
        return self.execute(
            ListStructureKindsQuery, variables, task=task
        ).structure_kinds

    async def asearch_structure_kinds(
        self,
        search: str | None | UnsetType = UNSET,
        values: list[IDCoercible] | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> tuple[SearchStructureKindsQueryOptions, ...]:
        """SearchStructureKinds

        List the organization's structure kinds

        Args:
            search (str | None, optional): No description.
            values (list[ID] | None, optional): No description.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            list[SearchStructureKindsQueryStructureKinds]"""
        variables: dict[str, builtins.object] = {}
        if search is not UNSET:
            variables["search"] = search
        if values is not UNSET:
            variables["values"] = values
        return (
            await self.aexecute(SearchStructureKindsQuery, variables, task=task)
        ).options

    def search_structure_kinds(
        self,
        search: str | None | UnsetType = UNSET,
        values: list[IDCoercible] | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> tuple[SearchStructureKindsQueryOptions, ...]:
        """SearchStructureKinds

        List the organization's structure kinds

        Args:
            search (str | None, optional): No description.
            values (list[ID] | None, optional): No description.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            list[SearchStructureKindsQueryStructureKinds]"""
        variables: dict[str, builtins.object] = {}
        if search is not UNSET:
            variables["search"] = search
        if values is not UNSET:
            variables["values"] = values
        return self.execute(SearchStructureKindsQuery, variables, task=task).options

    async def aget_metric_kind(
        self, id: IDCoercible, task: TaskLike | None = None
    ) -> MetricKind:
        """GetMetricKind

        Get one metric kind by ID

        Args:
            id (ID): No description
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            MetricKind"""
        variables: dict[str, builtins.object] = {}
        variables["id"] = id
        return (
            await self.aexecute(GetMetricKindQuery, variables, task=task)
        ).metric_kind

    def get_metric_kind(
        self, id: IDCoercible, task: TaskLike | None = None
    ) -> MetricKind:
        """GetMetricKind

        Get one metric kind by ID

        Args:
            id (ID): No description
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            MetricKind"""
        variables: dict[str, builtins.object] = {}
        variables["id"] = id
        return self.execute(GetMetricKindQuery, variables, task=task).metric_kind

    async def alist_metric_kinds(
        self,
        filters: MetricKindFilter | None | UnsetType = UNSET,
        pagination: VocabularyPaginationInput | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> tuple[MetricKind, ...]:
        """ListMetricKinds

        List the organization's metric kinds

        Args:
            filters (MetricKindFilter | None, optional): No description.
            pagination (VocabularyPaginationInput | None, optional): No description.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            list[MetricKind]"""
        variables: dict[str, builtins.object] = {}
        if filters is not UNSET:
            variables["filters"] = filters
        if pagination is not UNSET:
            variables["pagination"] = pagination
        return (
            await self.aexecute(ListMetricKindsQuery, variables, task=task)
        ).metric_kinds

    def list_metric_kinds(
        self,
        filters: MetricKindFilter | None | UnsetType = UNSET,
        pagination: VocabularyPaginationInput | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> tuple[MetricKind, ...]:
        """ListMetricKinds

        List the organization's metric kinds

        Args:
            filters (MetricKindFilter | None, optional): No description.
            pagination (VocabularyPaginationInput | None, optional): No description.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            list[MetricKind]"""
        variables: dict[str, builtins.object] = {}
        if filters is not UNSET:
            variables["filters"] = filters
        if pagination is not UNSET:
            variables["pagination"] = pagination
        return self.execute(ListMetricKindsQuery, variables, task=task).metric_kinds

    async def asearch_metric_kinds(
        self,
        search: str | None | UnsetType = UNSET,
        values: list[IDCoercible] | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> tuple[SearchMetricKindsQueryOptions, ...]:
        """SearchMetricKinds

        List the organization's metric kinds

        Args:
            search (str | None, optional): No description.
            values (list[ID] | None, optional): No description.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            list[SearchMetricKindsQueryMetricKinds]"""
        variables: dict[str, builtins.object] = {}
        if search is not UNSET:
            variables["search"] = search
        if values is not UNSET:
            variables["values"] = values
        return (
            await self.aexecute(SearchMetricKindsQuery, variables, task=task)
        ).options

    def search_metric_kinds(
        self,
        search: str | None | UnsetType = UNSET,
        values: list[IDCoercible] | None | UnsetType = UNSET,
        task: TaskLike | None = None,
    ) -> tuple[SearchMetricKindsQueryOptions, ...]:
        """SearchMetricKinds

        List the organization's metric kinds

        Args:
            search (str | None, optional): No description.
            values (list[ID] | None, optional): No description.
            task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

        Returns:
            list[SearchMetricKindsQueryMetricKinds]"""
        variables: dict[str, builtins.object] = {}
        if search is not UNSET:
            variables["search"] = search
        if values is not UNSET:
            variables["values"] = values
        return self.execute(SearchMetricKindsQuery, variables, task=task).options


AssertEntityExistsInput.model_rebuild()
AssertMeasurementExistsInput.model_rebuild()
AssertNaturalEventExistsInput.model_rebuild()
AssertParticipationsInput.model_rebuild()
AssertProtocolEventExistsInput.model_rebuild()
AssertRelationExistsInput.model_rebuild()
AssertStructureExistsInput.model_rebuild()
AssertStructureRelationExistsInput.model_rebuild()
CategoryDefinitionInput.model_rebuild()
ClaimConditionGroupInput.model_rebuild()
CommentOnStructureInput.model_rebuild()
CreateEntityCategoryInput.model_rebuild()
CreateGraphInput.model_rebuild()
CreateMeasurementCategoryInput.model_rebuild()
CreateNaturalEventCategoryInput.model_rebuild()
CreateProtocolEventCategoryInput.model_rebuild()
CreateRelationCategoryInput.model_rebuild()
CreateStructureRelationCategoryInput.model_rebuild()
DerivationRuleInput.model_rebuild()
DescendantInput.model_rebuild()
EntityCategoryFilter.model_rebuild()
EntityDefinitionInput.model_rebuild()
EventDefinitionInput.model_rebuild()
EventRoleInput.model_rebuild()
GraphDefinitionInput.model_rebuild()
GraphExtensionsInput.model_rebuild()
GraphFilter.model_rebuild()
MeasurementCategoryFilter.model_rebuild()
MeasurementDefinitionInput.model_rebuild()
MetricKindFilter.model_rebuild()
NaturalEventCategoryFilter.model_rebuild()
ProtocolEventCategoryFilter.model_rebuild()
RelationCategoryFilter.model_rebuild()
StructureKindFilter.model_rebuild()
StructureRelationCategoryFilter.model_rebuild()
TermFilter.model_rebuild()
