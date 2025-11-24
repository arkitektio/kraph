from calendar import c
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum
from re import search
import re
import types
from typing import Any, Union, Optional, get_origin, get_args
import inspect
from fieldz import fields, asdict
from graphql import SchemaDefinitionNode
from kraph.api.schema import (
    EntityCategory,
    EntityCategoryInput,
    MeasurementCategorySchemaInput,
    OptionInput,
    RelationCategoryInput,
    RelationCategorySchemaInput,
    RelationCategorySourcedefinition,
    RelationCategoryTargetdefinition,
    SchemaInput,
    VariableDefinitionInput,
    PropertyDefinitionInput,
    MetricKind,
    SchemaDefinitionInput,
    EntityCategorySchemaInput,
    create_entity,
    DescriptorInput,
)
from .vars import current_graph
from inflection import titleize


def property(
    *,
    description: str | None = None,
    searchable: bool = False,
    label: str | None = None,
    options: list[Union[str, OptionInput]] = None,
):
    """Helper to define a variable with description metadata."""

    if options:
        options = [
            OptionInput(value=opt, label=opt)
            if not isinstance(opt, OptionInput)
            else opt
            for opt in options
        ]

    return field(
        metadata={
            "description": description,
            "options": options,
            "searchable": searchable,
            "label": label,
        }
    )


def measurement(
    *,
    description: str | None = None,
):
    """Helper to define a measurement variable with description metadata."""

    return field(
        metadata={
            "description": description,
            "is_measurement": True,
        }
    )


def relation_property(
    *,
    description: str | None = None,
    tags: list[str] | None = None,
):
    """Helper to define a relation property with description metadata."""

    return field(
        metadata={
            "description": description,
            "tags": tags,
        }
    )


def unwrap_optional(field_type):
    """Unwrap Optional/Union types to get the actual type"""
    # Check if it's Optional (Union with None)
    if get_origin(field_type) in (Union, Optional):
        args = get_args(field_type)
        # Filter out NoneType
        non_none_args = [arg for arg in args if arg is not type(None)]
        if len(non_none_args) == 1:
            return non_none_args[0]
        elif len(non_none_args) > 1:
            # Still a Union, return the first non-None type
            return non_none_args[0]
    return field_type


def field_type_to_metric_kind(field_type: type) -> MetricKind:
    """Convert a field type to a MetricKind

    Handles edge cases:
    - Unwraps Optional/Union types
    - Checks bool BEFORE int (bool is subclass of int)
    - Excludes Enum types
    - Uses inspect.isclass() for proper type checking
    """
    # Unwrap Optional/Union types first
    field_type = unwrap_optional(field_type)

    # Check if it's actually a class
    if not inspect.isclass(field_type):
        return MetricKind.STRING

    # Check bool BEFORE int (bool is subclass of int)
    if not issubclass(field_type, Enum) and issubclass(field_type, bool):
        return MetricKind.BOOLEAN

    # Check int (excluding bool)
    if not issubclass(field_type, Enum) and issubclass(field_type, int):
        return MetricKind.INT

    # Check float
    if not issubclass(field_type, Enum) and issubclass(field_type, float):
        return MetricKind.FLOAT

    # Check datetime
    if not issubclass(field_type, Enum) and issubclass(field_type, datetime):
        return MetricKind.DATETIME

    # Check str
    if not issubclass(field_type, Enum) and issubclass(field_type, str):
        return MetricKind.STRING

    # Default to STRING for everything else (including Enums)
    return MetricKind.STRING


def cast_value_to_metric_kind(value, metric_kind: MetricKind):
    """Cast a value to the correct type based on MetricKind"""
    if value is None:
        return None

    if metric_kind == MetricKind.INT:
        return int(value)
    elif metric_kind == MetricKind.FLOAT:
        return float(value)
    elif metric_kind == MetricKind.STRING:
        return str(value)
    elif metric_kind == MetricKind.BOOLEAN:
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ("true", "1", "yes")
        return bool(value)
    elif metric_kind == MetricKind.DATETIME:
        if isinstance(value, datetime):
            return value.isoformat()
        elif isinstance(value, str):
            return value
        else:
            return str(value)
    else:
        return value


def serialize_kwargs(kwargs, entity_category: EntityCategory):
    """Serialize kwargs based on entity category property definitions"""
    serialized = {}
    prop_defs = {pd.key: pd for pd in entity_category.property_definitions}

    for key, value in kwargs.items():
        if key in prop_defs:
            metric_kind = prop_defs[key].value_kind
            serialized[key] = cast_value_to_metric_kind(value, metric_kind)
        else:
            serialized[key] = value  # No casting if property definition not found

    return serialized


def create(cls, original_init, def_map):
    def __init__(self, *args, **kwargs):
        original_init(self, *args, **kwargs)
        graph = current_graph.get()
        graph.register_instance(self)

    return __init__


def create_relation(cls, original_init, def_map):
    def __init__(self, *args, **kwargs):
        original_init(self, *args, **kwargs)
        graph = current_graph.get()
        graph.register_relation(self)

    return __init__


def create_serialized_properties(cls, def_map):
    from kraph.api.schema import NodeImport

    def serialized_properties(self):
        dict = asdict(self)
        serialized_properties = {}
        for key, var_def in def_map.items():
            if key in dict:
                value = dict[key]
                metric_kind = var_def.value_kind
                serialized_properties[key] = cast_value_to_metric_kind(
                    value, metric_kind
                )

        return serialized_properties

    return serialized_properties


def create_serialized_measurements(cls, def_map):
    from kraph.api.schema import NodeImport

    def serialized_properties(self):
        dict = asdict(self)
        serialized_properties = {}
        for key, var_def in def_map.items():
            if key in dict:
                value = dict[key]
                metric_kind = var_def.value_kind
                serialized_properties[key] = cast_value_to_metric_kind(
                    value, metric_kind
                )

        return serialized_properties

    return serialized_properties


def is_measurement_field(field_obj) -> bool:
    """Check if a field is marked as a measurement"""
    return field_obj.metadata.get("is_measurement", False)


def cls_to_entity_category_input(
    cls, tags=None, descriptors=None
) -> EntityCategoryInput:
    var_defs = []

    try:
        fields(cls)
    except Exception:
        cls = dataclass(cls)

    def_map = {}
    # inspect fields and create variable definitions
    for field_obj in fields(cls):
        # create variable definition

        print("Processing field:", field_obj.name, "of type", field_obj.annotated_type)
        type = field_obj.annotated_type or field_obj.type
        var_def = PropertyDefinitionInput(
            key=field_obj.name,
            value_kind=field_type_to_metric_kind(type),
            description=field_obj.metadata.get("description", ""),
            label=field_obj.metadata.get("label", titleize(field_obj.name)),
            options=field_obj.metadata.get("options", None),
            searchable=field_obj.metadata.get("searchable", False),
        )
        print("Adding variable definition:", var_def)
        def_map[field_obj.name] = var_def
        var_defs.append(var_def)

    cls.__init__ = create(cls, cls.__init__, def_map)
    cls.serialized_properties = create_serialized_properties(cls, def_map)

    return EntityCategorySchemaInput(
        label=cls.__name__,
        description=cls.__doc__ or "",
        tags=tags or [],
        property_definitions=var_defs,
    )


def get_field_tags(field_obj):
    """Get source and target tags from a relation property field"""
    source_tags = field_obj.metadata.get("tags", None)
    return source_tags


def get_field_description(field_obj):
    """Get description from a field object"""
    description = field_obj.metadata.get("description", "")
    return description


def field_to_definition(field_obj) -> SchemaDefinitionInput:
    type = field_obj.annotated_type or field_obj.type

    tags = get_field_tags(field_obj)

    # check if is union
    origin = get_origin(type)
    print("Origin of field", field_obj.name, "is", origin)
    if origin is Any:
        var_def = SchemaDefinitionInput(
            labels=[],
            tags=tags,
        )
        return var_def

    if origin in (Union, types.UnionType):
        print("Processing union type for field:", field_obj.name)
        args = get_args(type)
        # handle union types
        # get class names of all types in union
        class_names = [arg.__name__ for arg in args if inspect.isclass(arg)]

        var_def = SchemaDefinitionInput(
            labels=class_names,
            tags=tags,
        )
    else:
        class_names = [type.__name__] if inspect.isclass(type) else []

        var_def = SchemaDefinitionInput(
            labels=class_names,
            tags=tags,
        )

    return var_def


def field_to_structure_definition(field_obj) -> SchemaDefinitionInput:
    type = field_obj.annotated_type or field_obj.type

    tags = get_field_tags(field_obj)

    # check if is union
    origin = get_origin(type)
    print("Origin of field", field_obj.name, "is", origin)
    if origin is Any:
        var_def = SchemaDefinitionInput(
            labels=[],
            tags=tags,
        )
        return var_def

    if origin in (Union, types.UnionType):
        print("Processing union type for field:", field_obj.name)
        args = get_args(type)
        # handle union types
        # get class names of all types in union
        class_names = [arg.__name__ for arg in args if inspect.isclass(arg)]

        var_def = SchemaDefinitionInput(
            labels=class_names,
            tags=tags,
        )
    else:
        class_names = [type.__name__] if inspect.isclass(type) else []

        var_def = SchemaDefinitionInput(
            labels=class_names,
            tags=tags,
        )

    return var_def


def cls_to_relation_category_input(cls, tags=None) -> RelationCategorySchemaInput:
    var_defs = []

    try:
        fields(cls)
    except Exception:
        cls = dataclass(cls)

    def_map = {}

    class_fields = fields(cls)

    source = next(f for f in class_fields if f.name == "source")
    target = next(f for f in class_fields if f.name == "target")

    source_definition = field_to_definition(source)
    target_definition = field_to_definition(target)

    # inspect fields and create variable definitions
    for field_obj in class_fields:
        if field_obj.name in ("source", "target"):
            continue
        # create variable definition
        print("Processing field:", field_obj.name, "of type", field_obj.annotated_type)
        type = field_obj.annotated_type or field_obj.type
        var_def = PropertyDefinitionInput(
            key=field_obj.name,
            value_kind=field_type_to_metric_kind(type),
            description=field_obj.metadata.get("description", ""),
            label=field_obj.metadata.get("label", titleize(field_obj.name)),
            options=field_obj.metadata.get("options", None),
            searchable=field_obj.metadata.get("searchable", False),
        )
        print("Adding variable definition:", var_def)
        def_map[field_obj.name] = var_def
        var_defs.append(var_def)

    cls.__init__ = create_relation(cls, cls.__init__, def_map)
    cls.serialized_properties = create_serialized_properties(cls, def_map)

    return RelationCategorySchemaInput(
        label=cls.__name__,
        description=cls.__doc__ or "",
        tags=tags or [],
        property_definitions=var_defs,
        sourceDefinition=source_definition,
        targetDefinition=target_definition,
    )


def cls_to_measurement_category_input(cls, tags=None) -> MeasurementCategorySchemaInput:
    var_defs = []

    try:
        fields(cls)
    except Exception:
        cls = dataclass(cls)

    def_map = {}

    class_fields = fields(cls)

    source = next(f for f in class_fields if f.name == "source")
    target = next(f for f in class_fields if f.name == "target")

    source_definition = field_to_definition(source)
    target_definition = field_to_definition(target)

    # inspect fields and create variable definitions
    for field_obj in class_fields:
        if field_obj.name in ("source", "target"):
            continue
        # create variable definition
        print("Processing field:", field_obj.name, "of type", field_obj.annotated_type)
        type = field_obj.annotated_type or field_obj.type
        var_def = PropertyDefinitionInput(
            key=field_obj.name,
            value_kind=field_type_to_metric_kind(type),
            description=field_obj.metadata.get("description", ""),
            label=field_obj.metadata.get("label", titleize(field_obj.name)),
            options=field_obj.metadata.get("options", None),
            searchable=field_obj.metadata.get("searchable", False),
        )
        print("Adding variable definition:", var_def)
        def_map[field_obj.name] = var_def
        var_defs.append(var_def)

    cls.__init__ = create_relation(cls, cls.__init__, def_map)
    cls.serialized_properties = create_serialized_properties(cls, def_map)

    return RelationCategorySchemaInput(
        label=cls.__name__,
        description=cls.__doc__ or "",
        tags=tags or [],
        property_definitions=var_defs,
        sourceDefinition=source_definition,
        targetDefinition=target_definition,
    )


class SchemaEntity:
    """Base class for schema entities."""

    __entity_category: EntityCategory | None = None

    def __init__(self, **kwargs):
        self.variables = kwargs

    def create_entity(
        self, name: str = None, external_id: str = None, pinned: bool = None
    ):
        """Create the entity in the current graph with properly cast variables."""
        if not self.__entity_category:
            raise ValueError(
                "Entity category not set. Did you register this class with @schema.entity()?"
            )

        # Get field definitions to determine metric kinds
        cls = self.__class__
        try:
            field_list = fields(cls)
        except Exception:
            field_list = []

        # Build field_name -> metric_kind mapping
        field_kinds = {}
        for f in field_list:
            metric_kind = field_type_to_metric_kind(f.annotated_type)
            field_kinds[f.name] = metric_kind

        # Cast all variables to their correct types
        casted_variables = {}
        for key, value in self.variables.items():
            if key in field_kinds:
                casted_variables[key] = cast_value_to_metric_kind(
                    value, field_kinds[key]
                )
            else:
                casted_variables[key] = value

        # Create the entity with casted variables
        return create_entity(
            entity_category=self.__entity_category.id,
            name=name,
            external_id=external_id,
            pinned=pinned,
            variables=casted_variables,
            rath=current_graph.get().rath if current_graph.get() else None,
        )


class Schema:
    """
    Trait for building schema input objects from class definitions.

    This trait provides a method to convert class definitions
    """

    def __init__(self):
        self.entity_schemas = []
        self.as_measurements = []
        self.relation_schemas = []

    def as_graph(self, name: str):
        """Create a graph with this schema in the current context."""
        from kraph.api.schema import create_graph

        return create_graph(name=name, schema=self.build())

    def entity(
        self, *cls, tags: list[str] = None, descriptors: list[DescriptorInput] = None
    ):
        if len(cls) == 0:

            def wrapper(inner_cls):
                entity_category_input = cls_to_entity_category_input(
                    inner_cls, tags=tags or [], descriptors=descriptors or []
                )
                self.entity_schemas = [*self.entity_schemas, entity_category_input]
                return inner_cls

            return wrapper

        else:
            assert len(cls) == 1, (
                "entity() decorator accepts only a single class at a time."
            )
            entity_category_input = cls_to_entity_category_input(
                cls[0], tags=tags or []
            )
            self.entity_schemas = [*self.entity_schemas, entity_category_input]
            return cls

    def relate(self, *cls, tags=None):
        if len(cls) == 0:

            def wrapper(inner_cls):
                entity_category_input = cls_to_relation_category_input(
                    inner_cls, tags=tags or []
                )
                self.relation_schemas = [*self.relation_schemas, entity_category_input]
                return inner_cls

            return wrapper

        else:
            assert len(cls) == 1, (
                "entity() decorator accepts only a single class at a time."
            )
            entity_category_input = cls_to_relation_category_input(
                cls[0], tags=tags or []
            )
            self.relation_schemas = [*self.relation_schemas, entity_category_input]
            return cls

    def measurement(self, *cls, tags=None):
        if len(cls) == 0:

            def wrapper(inner_cls):
                entity_category_input = cls_to_relation_category_input(
                    inner_cls, tags=tags or []
                )
                self.relation_schemas = [*self.relation_schemas, entity_category_input]
                return inner_cls

            return wrapper

        else:
            assert len(cls) == 1, (
                "entity() decorator accepts only a single class at a time."
            )
            entity_category_input = cls_to_relation_category_input(
                cls[0], tags=tags or []
            )
            self.relation_schemas = [*self.relation_schemas, entity_category_input]
            return cls

    def build(self):
        return SchemaInput(
            entitySchemas=self.entity_schemas,
            measurementSchemas=self.as_measurements,
            relationSchemas=self.relation_schemas,
        )

    def json(self, indent: int = None) -> str:
        return self.build().model_dump_json(indent=indent)
