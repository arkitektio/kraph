"""Custom scalars the kraph schema names.

The evidence-log schema declares eight scalars, of which only these need Python behaviour;
``AnyScalar``, ``JSON``, ``UnixMilliseconds`` and ``_Any`` map to plain builtins in
``graphql.config.yaml``, and ``DateTime`` is a turms built-in.

Note that a structure is addressed by **two** fields now — ``identifier`` and ``object`` — rather
than by a single ``identifier:object`` string. The old ``StructureString`` scalar is gone with
it, and the job of turning a Python object into that pair belongs to
:func:`kraph.refs.as_structure_ref`, not to a scalar validator.
"""

from typing import Any, Type

from pydantic import BaseModel, GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema

StructureIdentifierCoercible = str
"""What may be passed where a StructureIdentifier is wanted."""

StructureObjectCoercible = str
"""What may be passed where a StructureObject is wanted."""

CypherLiteralCoercible = str
"""What may be passed where a CypherLiteral is wanted."""


class StructureIdentifier(str):
    """Names a kind of external datum, e.g. ``@mikro/roi``.

    Accepts a registered Python class directly, resolving it through the rekuest structure
    registry, so ``Structures([ROI])`` and ``"@mikro/roi"`` mean the same thing.
    """

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source_type: Any,  # noqa: ANN401
        handler: GetCoreSchemaHandler,  # noqa: ANN401
    ) -> CoreSchema:
        """Get the pydantic core schema for the validator function"""
        return core_schema.no_info_before_validator_function(cls.validate, handler(str))

    @classmethod
    def validate(
        cls: Type["StructureIdentifier"], v: StructureIdentifierCoercible, *info: Any
    ) -> "StructureIdentifier":
        if isinstance(v, BaseModel) or isinstance(v, type) and issubclass(v, BaseModel):
            from kraph.refs import identifier_for_cls

            target = v if isinstance(v, type) else type(v)
            return cls(identifier_for_cls(target))

        if isinstance(v, str):
            assert "@" in v, f"{v!r} is not a valid structure identifier (expected '@ns/name')"
            return cls(v)

        raise TypeError(
            "A structure identifier must be a '@ns/name' string or a registered structure class"
        )


class StructureObject(str):
    """Names the particular external datum, within its identifier's namespace."""

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source_type: Any,  # noqa: ANN401
        handler: GetCoreSchemaHandler,  # noqa: ANN401
    ) -> CoreSchema:
        """Get the pydantic core schema for the validator function"""
        return core_schema.no_info_before_validator_function(cls.validate, handler(str))

    @classmethod
    def validate(
        cls: Type["StructureObject"], v: StructureObjectCoercible, *info: Any
    ) -> "StructureObject":
        if isinstance(v, BaseModel):
            from rath.turms.utils import get_attributes_or_error

            return cls(str(get_attributes_or_error(v, "id")))
        if isinstance(v, (str, int)):
            return cls(str(v))
        raise TypeError("A structure object must be a string, an int, or a model with an id")


class CypherLiteral(str):
    """A literal fragment of Cypher, used only by the deprecated saved-query surface."""

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source_type: Any,  # noqa: ANN401
        handler: GetCoreSchemaHandler,  # noqa: ANN401
    ) -> CoreSchema:
        """Get the pydantic core schema for the validator function"""
        return core_schema.no_info_before_validator_function(cls.validate, handler(str))

    @classmethod
    def validate(cls, v: CypherLiteralCoercible, *info: Any) -> "CypherLiteral":
        if isinstance(v, str):
            return cls(v)
        raise TypeError("A CypherLiteral must be a string")
