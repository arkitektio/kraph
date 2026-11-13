"""Pairing two data under a structure-relation word, holding them to the word's pins first.

A structure-relation category may pin descriptors on its ends ("the source has three
space axes"). kraph stores those pins but cannot evaluate them: the descriptors live
with the service that hosts the datum (mikro's ``stored_descriptors``). So the pins are
checked here, before the claim is made, by asking that service, through ``check``.

``check(end, requires)`` is handed the ``(identifier, object)`` of one end and that
end's constraints, and says whether the datum satisfies all of them. It must use the
hosting service's strict semantics, where a key the datum does not carry fails. With
mikro, a search that offers the lens only when every constraint holds::

    def check(end, requires):
        identifier, object_id = end
        found = mikro.search_array_lenses(values=[object_id], requires=[c.model_dump() for c in requires])
        return len(found) == 1

Never ``arkitekt_spec.declare.descriptors.unfulfilled``: it skips a key the object
lacks, so a pin on ``@mikro/value_kind`` would pass for every lens.
"""

from collections.abc import Callable, Sequence
from datetime import datetime
from typing import TYPE_CHECKING, Any

from rath.turms.utils import get_attributes_or_error

from kraph.client import client_of
from kraph.refs import StructureRef, as_structure_ref

if TYPE_CHECKING:
    from kraph.kraph import Kraph

#: Says whether the datum at ``(identifier, object)`` satisfies every constraint.
Check = Callable[[tuple[str, str], Sequence[Any]], bool]


class PinRefused(ValueError):
    """A datum does not satisfy what the word pins on its end of the pair."""


def _end(descriptor: Any) -> tuple[list[str], list[Any]]:  # noqa: ANN401
    """The identifiers and the pinned constraints of one end of a category."""
    if descriptor is None:
        return [], []
    return list(getattr(descriptor, "identifiers", None) or []), list(getattr(descriptor, "requires", None) or [])


def _hold(name: str, end: tuple[str, str], descriptor: Any, check: Check | None) -> None:  # noqa: ANN401
    identifiers, requires = _end(descriptor)
    if identifiers and end[0] not in identifiers:
        raise PinRefused(f"The {name} is a {end[0]}, but this word pairs {', '.join(identifiers)} there")
    if not requires:
        return
    if check is None:
        raise PinRefused(f"This word pins {len(requires)} descriptor(s) on its {name}, and only the datum's own service can say whether they hold: pass check=")
    if not check(end, requires):
        pinned = ", ".join(f"{c.key} {getattr(c.operator, 'value', c.operator)} {c.value!r}" for c in requires)
        raise PinRefused(f"The {name} {end[0]}:{end[1]} does not satisfy what this word pins there: {pinned}")


def _word(category: Any) -> str:  # noqa: ANN401
    """The word a claim under this category names: its term's key, as the server reads it."""
    term = getattr(category, "term", None)
    key = getattr(term, "key", None) if term is not None else None
    return str(key) if key else str(get_attributes_or_error(category, "key"))


def pair(
    source: StructureRef,
    target: StructureRef,
    category: Any,  # noqa: ANN401
    *,
    check: Check | None = None,
    confidence: float | None = None,
    observed_at: datetime | None = None,
    kraph: "Kraph | None" = None,
) -> Any:  # noqa: ANN401
    """Claim that ``source`` and ``target`` are a pair under ``category``'s word.

    Both ends are held to the category's ends first (identifiers, then pinned descriptors
    through ``check``), and refused with :class:`PinRefused` before anything is written.
    Then each end is made a structure (idempotent per datum) and the relation is asserted
    under the category's word. The claim names the word, never the category: every view
    declaring the same word reads it.

    Returns the ``AssertedStructureRelation`` the write returned.
    """
    client = client_of(category, kraph)
    source_end, target_end = as_structure_ref(source), as_structure_ref(target)
    _hold("source", source_end, getattr(category, "source_descriptor", None), check)
    _hold("target", target_end, getattr(category, "target_descriptor", None), check)

    structures = [
        client.assert_structure_exists(identifier=identifier, object=object_id).structure
        for identifier, object_id in (source_end, target_end)
    ]
    return client.assert_structure_relation_exists(
        source_id=str(get_attributes_or_error(structures[0], "id")),
        target_id=str(get_attributes_or_error(structures[1], "id")),
        term=_word(category),
        confidence=confidence,
        observed_at=observed_at,
    )
