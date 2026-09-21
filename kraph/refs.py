"""Turning Python objects into the references the write path speaks.

Every claim addresses things by one of two shapes:

* an **instance or link** — a bare uuid, the evidence row's primary key;
* a **structure** — an ``(identifier, object)`` pair naming an external datum.

The old client resolved these inline in half a dozen places and encoded a structure as a single
``identifier:object`` string. The schema now takes the two halves separately, so the resolution
lives here, once. A bare object maps to its identifier only through a structure registry;
passing explicit pairs needs none.
"""

from typing import Any, Union

from pydantic import BaseModel
from rath.turms.utils import get_attributes_or_error

from kraph.errors import UnregisteredStructure

StructureRef = Union[str, tuple, BaseModel]
NodeRef = Union[str, BaseModel]


def identifier_for_cls(cls: type, registry: Any = None) -> str:  # noqa: ANN401
    """The structure identifier a Python class is registered under in ``registry``.

    There is no current registry to ask: a class maps to an identifier only through
    the registry of an app that declared it (``rekuest.structure_registry``).
    Without one, pass the identifier yourself.
    """
    if registry is None:
        raise UnregisteredStructure(
            f"Which structure is a {cls.__name__}? Nothing here knows without a "
            "structure registry. Pass an explicit (identifier, object) pair, or the "
            "'@ns/name' identifier."
        )
    identifier = registry.get_identifier_for_cls(cls)
    if identifier is None:
        raise UnregisteredStructure(
            f"{cls.__name__} is not registered in the given structure registry. "
            f"Pass an explicit (identifier, object) pair instead."
        )
    return identifier


def as_node_id(x: NodeRef) -> str:
    """The bare uuid of an instance, however it was handed to us.

    Accepts a uuid string, an ``Instance``/``Node``, or any ``Asserted*`` write result — so the
    result of one call can be passed straight into the next.
    """
    if isinstance(x, str):
        return x
    for attr in ("instance", "claim"):
        inner = getattr(x, attr, None)
        if inner is not None and not isinstance(inner, list):
            return str(get_attributes_or_error(inner, "id"))
    return str(get_attributes_or_error(x, "id"))


def as_link_id(x: NodeRef) -> str:
    """The bare uuid of a link claim."""
    if isinstance(x, str):
        return x
    inner = getattr(x, "link", None)
    if inner is not None:
        return str(get_attributes_or_error(inner, "id"))
    return str(get_attributes_or_error(x, "id"))


def as_structure_ref(x: StructureRef) -> tuple[str, str]:
    """The ``(identifier, object)`` pair addressing an external datum.

    Accepts an explicit pair, a legacy ``"@ns/name:123"`` string, a kraph ``Structure`` (or an
    ``AssertedStructure``), or any pydantic model registered with the rekuest structure registry
    — which is how a foreign object such as a mikro ``ROI`` or ``Image`` enters the graph.
    """
    if isinstance(x, tuple):
        if len(x) != 2:
            raise TypeError(f"A structure reference is a 2-tuple, got {len(x)} items")
        return str(x[0]), str(x[1])

    if isinstance(x, str):
        if x.count(":") != 1:
            raise TypeError(
                f"{x!r} is not a structure reference; pass ('@ns/name', 'object') instead"
            )
        identifier, _, object_id = x.partition(":")
        return identifier, object_id

    structure = getattr(x, "structure", None)
    if structure is not None:
        x = structure

    identifier = getattr(x, "identifier", None)
    if identifier is not None:
        return str(identifier), str(get_attributes_or_error(x, "object"))

    if isinstance(x, BaseModel):
        return (
            identifier_for_cls(type(x)),
            str(get_attributes_or_error(x, "id")),
        )

    raise TypeError(f"Cannot read a structure reference out of {type(x).__name__}")


def as_term(x: Any) -> str:
    """The word a claim is stated in — a ``Term.key``, never a category id."""
    if isinstance(x, str):
        return x
    key = getattr(x, "key", None)
    if key is not None:
        return str(key)
    raise TypeError(f"Cannot read a term key out of {type(x).__name__}")
