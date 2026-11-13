"""Pairs on the client: a port typed for one kind of pair (a pairs query or a run), and a pair held to its word's pins.

Nothing here needs a server. The port typing compiles to the two `Requires` the server's
descriptors answer, and `pair` refuses a datum the word's pins do not fit before it writes
anything: the server stores pins but cannot evaluate them.
"""

from types import SimpleNamespace
from collections.abc import Sequence
from typing import Annotated, Any, get_args, get_origin

import pytest

pytest.importorskip("arkitekt_spec")

from kraph.api.schema import GraphPairsQuery, PairsQueryRun  # noqa: E402
from kraph.pairs import PinRefused, pair  # noqa: E402

IMAGE = "@mikro/arraylens"


class ArrayLens:
    """Stands in for mikro's generated model, which carries the structure it travels as."""

    __identifier__ = IMAGE

    def __init__(self, id: str) -> None:
        """A lens is addressed by its id."""
        self.id = id


def _requires(annotated: object) -> list[tuple[str, str, object]]:
    assert get_origin(annotated) is Annotated
    _, *markers = get_args(annotated)
    return [(m.key, getattr(m.operator, "value", m.operator), m.value) for m in markers]


def test_a_port_typed_for_image_pairs_requires_both_identifiers() -> None:
    """Strings and stamped classes compile to the same two `Requires` on the identifier descriptors."""
    by_name = PairsQueryRun[IMAGE, IMAGE]
    assert get_args(by_name)[0] is PairsQueryRun
    assert _requires(by_name) == [("@kraph/source_identifier", "EQUALS", IMAGE), ("@kraph/target_identifier", "EQUALS", IMAGE)]
    assert _requires(PairsQueryRun[ArrayLens, ArrayLens]) == _requires(by_name), "a stamped class names itself"
    assert _requires(GraphPairsQuery[IMAGE, IMAGE]) == _requires(by_name), "a query is typed the way its runs are"
    assert get_args(GraphPairsQuery[IMAGE, IMAGE])[0] is GraphPairsQuery

    # The runtime's check skips a key the object lacks, so a mixed dataset carries the key as null.
    from arkitekt_spec.declare.descriptors import unfulfilled

    markers = get_args(by_name)[1:]
    mixed = {"@kraph/source_identifier": IMAGE, "@kraph/target_identifier": None, "@kraph/n_pairs": 2}
    assert unfulfilled(markers, mixed), "a dataset pairing images with tables fails an image-pair port"
    assert not unfulfilled(markers, {**mixed, "@kraph/target_identifier": IMAGE})


def test_a_pair_is_held_to_its_words_pins_before_anything_is_written() -> None:
    """Missing check, failing pin and wrong identifier are refused with nothing written; a fitting pair is claimed."""
    written: list[tuple[str, dict]] = []

    class Kraph:
        def assert_structure_exists(self, **kwargs: Any) -> SimpleNamespace:  # noqa: ANN401
            written.append(("structure", kwargs))
            return SimpleNamespace(structure=SimpleNamespace(id=f"s-{kwargs['object']}"))

        def assert_structure_relation_exists(self, **kwargs: Any) -> dict:  # noqa: ANN401
            written.append(("relation", kwargs))
            return kwargs

    pin = SimpleNamespace(key="@mikro/n_space_axes", operator="EQUALS", value=3)
    end = SimpleNamespace(identifiers=[IMAGE], requires=[pin])
    category = SimpleNamespace(key="GROUND_TRUTH_OF", source_descriptor=end, target_descriptor=end)
    volumes = {"noisy", "clean"}

    def check(datum: tuple[str, str], requires: Sequence[Any]) -> bool:
        return datum[1] in volumes

    with pytest.raises(PinRefused, match="pass check="):
        pair(ArrayLens("noisy"), ArrayLens("clean"), category, kraph=Kraph())
    with pytest.raises(PinRefused, match="does not satisfy"):
        pair(ArrayLens("noisy"), ArrayLens("a-plane"), category, kraph=Kraph(), check=check)
    with pytest.raises(PinRefused, match="pairs @mikro/arraylens"):
        pair(ArrayLens("noisy"), ("@mikro/table", "t1"), category, kraph=Kraph(), check=check)
    assert written == [], "a refused pair writes nothing"

    claim = pair(ArrayLens("noisy"), ArrayLens("clean"), category, kraph=Kraph(), check=check, confidence=0.9)
    assert claim == {"source_id": "s-noisy", "target_id": "s-clean", "term": "GROUND_TRUTH_OF", "confidence": 0.9, "observed_at": None}


def test_what_a_client_fetches_reaches_that_client() -> None:
    """A fetched model, its weights' store and the run it was trained on find the client they came from.

    `download()`, `read_entries()` and `run()` call through `client_of`, which reads the origin
    only a `ContextBound` model keeps; a trait on a plain `BaseModel` would raise `NoKraphFound`.
    """
    from rath.origin import origin_context

    from kraph.api.schema import Model
    from kraph.client import client_of
    from kraph.kraph import Kraph

    client = Kraph.model_construct()
    payload = {
        "id": "1",
        "name": "care",
        "description": None,
        "framework": "care",
        "parameters": None,
        "descriptors": {},
        "createdAt": "2026-11-08T00:00:00Z",
        "trainedOn": {
            "id": "r1",
            "name": "first",
            "description": None,
            "auto": True,
            "asOfSeq": 7,
            "nPairs": 2,
            "schemaHash": None,
            "sourceIdentifier": IMAGE,
            "targetIdentifier": IMAGE,
            "queryId": "q1",
            "graphId": "g1",
            "descriptors": {},
            "createdAt": "2026-11-08T00:00:00Z",
        },
        "store": {"id": "s1", "key": "k", "bucket": "b", "path": "s3://b/k", "originalFileName": "w.zip", "sizeBytes": 3},
    }
    model = Model.model_validate(payload, context=origin_context(client=client))

    assert client_of(model) is client
    assert client_of(model.store) is client, "the nested store downloads through the same client"
    assert client_of(model.trained_on) is client, "the run it cites reads its entries through the same client"
