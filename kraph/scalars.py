"""Custom scalars the kraph schema names.

The evidence-log schema declares nine scalars, of which only these need Python behaviour;
``AnyScalar``, ``JSON``, ``UnixMilliseconds`` and ``_Any`` map to plain builtins in
``graphql.config.yaml``, and ``DateTime`` is a turms built-in.

Note that a structure is addressed by **two** fields now — ``identifier`` and ``object`` — rather
than by a single ``identifier:object`` string. The old ``StructureString`` scalar is gone with
it, and the job of turning a Python object into that pair belongs to
:func:`kraph.refs.as_structure_ref`, not to a scalar validator.
"""

import io
import os
import uuid
from typing import IO, Any

from pydantic import BaseModel, GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema

StructureIdentifierCoercible = str
"""What may be passed where a StructureIdentifier is wanted."""

StructureObjectCoercible = str
"""What may be passed where a StructureObject is wanted."""

CypherLiteralCoercible = str
"""What may be passed where a CypherLiteral is wanted."""

UUIDCoercible = str | uuid.UUID
"""What may be passed where a UUID is wanted."""


class UUID(str):
    """A uuid, held as its text so that a request's variables can be sent as JSON."""

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source_type: Any,  # noqa: ANN401
        handler: GetCoreSchemaHandler,  # noqa: ANN401
    ) -> CoreSchema:
        """Get the pydantic core schema for the validator function"""
        return core_schema.no_info_before_validator_function(cls.validate, handler(str))

    @classmethod
    def validate(cls: type["UUID"], v: UUIDCoercible, *info: Any) -> "UUID":
        """Accept a uuid or its text, and refuse anything else."""
        return cls(str(uuid.UUID(str(v))))


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
        cls: type["StructureIdentifier"], v: StructureIdentifierCoercible, *info: Any
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
        cls: type["StructureObject"], v: StructureObjectCoercible, *info: Any
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


BigFileLikeCoercible = str | IO[bytes]
"""What may be passed where a ``BigFileLike`` is wanted: a path (opened in binary mode on
validation) or an already-open binary file."""


class BigFile:
    """A file to upload as a big file: what an input typed ``BigFileLike`` takes.

    The client's upload middleware (:mod:`kraph.middleware.upload`) finds it in a request's
    variables, uploads it through kraph's datalayer (request a grant, write, finish) and sends
    the finished store's id in its place: the same protocol every service's files use.
    """

    def __init__(self, value: IO[bytes], file_name: str = "") -> None:
        """Wrap an open binary file and the name it is uploaded under."""
        self.value = value
        self.file_name = file_name or str(getattr(value, "name", "") or "upload")

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source_type: Any,  # noqa: ANN401
        handler: GetCoreSchemaHandler,
    ) -> CoreSchema:
        """Validate with :meth:`validate`; the instance travels to the middleware as itself."""
        return core_schema.no_info_after_validator_function(cls.validate, handler(object))

    @classmethod
    def validate(cls, v: "BigFileLikeCoercible | BigFile") -> "BigFile":
        """Open a path, or take an open binary file; refuse anything else."""
        if isinstance(v, cls):
            return v
        if isinstance(v, (str, os.PathLike)):
            return cls(open(v, "rb"), file_name=os.path.basename(os.fspath(v)))  # noqa: SIM115 - read by the upload, closed with it
        if not isinstance(v, io.IOBase):
            raise ValueError(f"A big file is a path or an open binary file, not {type(v).__name__}")
        return cls(v)

    def __repr__(self) -> str:
        """Name the file, never its contents."""
        return f"BigFile({self.file_name!r})"
