"""A kraph call goes through the client it is made on, and nothing else.

No server: the rath is a fake returning canned data. Nothing is ever current: a
client is passed (or an object remembers the one that fetched it).
"""

from types import SimpleNamespace
from typing import Any, AsyncIterator, Optional

import pytest
from koil import Koil
from pydantic import BaseModel, ConfigDict
from rath.links.testing.mock import AsyncMockLink
from rath.origin import get_origin, origin_context

from kraph.datalayer import DataLayer
from kraph.errors import NoKraphFound
from kraph.kraph import TASK_HEADER, Kraph
from kraph.rath import KraphRath
from kraph.traits import GraphTrait, HasPresignedDownloadAccessor, StructureTrait


class FakeRath:
    """Answers every query with the same canned store, and remembers what was sent."""

    def __init__(self) -> None:
        self.sent: list[dict[str, Any]] = []
        self.headers: list[Any] = []

    def _answer(self, variables: dict[str, Any], headers: Any) -> Any:
        self.sent.append(variables)
        self.headers.append(headers)
        return SimpleNamespace(
            data={"store": {"id": "store-1", "presigned_url": "/media/file.bin", "key": "file.bin"}}
        )

    async def aquery(self, document: str, variables: dict[str, Any], headers: Any = None) -> Any:
        return self._answer(variables, headers)

    async def asubscribe(
        self, document: str, variables: dict[str, Any], headers: Any = None
    ) -> AsyncIterator[Any]:
        yield self._answer(variables, headers)


def client(name: str = "a") -> Kraph:
    """A real client over a fake rath, built without validating the rath's type."""
    return Kraph.model_construct(
        rath=FakeRath(),
        datalayer=DataLayer(endpoint_url=f"http://{name}.invalid"),
    )


class Store(HasPresignedDownloadAccessor):
    model_config = ConfigDict(frozen=True)
    id: str
    presigned_url: str
    key: str


class GetStore(BaseModel):
    """Shaped like a generated operation."""

    store: Store

    class Arguments(BaseModel):
        id: str
        note: Optional[str] = None

    class Meta:
        document = "query GetStore($id: ID!) { store(id: $id) { id presignedUrl key } }"


# --------------------------------------------------------------------------- #
# The client's execute/aexecute/subscribe/asubscribe
# --------------------------------------------------------------------------- #


@pytest.mark.asyncio
async def test_aexecute_goes_through_the_client_and_results_remember_it() -> None:
    mine, other = client("a"), client("b")

    result = await mine.aexecute(GetStore, {"id": "store-1"})

    assert (len(mine.rath.sent), len(other.rath.sent)) == (1, 0)
    origin = get_origin(result.store)
    assert origin is not None and origin.client is mine and origin.rath is mine.rath
    assert origin.clients["datalayer"] is mine.datalayer


def test_execute_goes_through_the_client() -> None:
    mine = client()
    with Koil():
        result = mine.execute(GetStore, {"id": "store-1"})
    assert result.store.id == "store-1"
    assert len(mine.rath.sent) == 1
    assert get_origin(result.store).client is mine


@pytest.mark.asyncio
async def test_asubscribe_goes_through_the_client() -> None:
    mine = client()
    events = [e async for e in mine.asubscribe(GetStore, {"id": "store-1"})]
    assert [e.store.id for e in events] == ["store-1"]
    assert get_origin(events[0].store).client is mine


@pytest.mark.asyncio
async def test_none_arguments_are_omitted() -> None:
    """kraph's wire behaviour, kept through the rewrite: exclude_none (see kraph.kraph)."""
    mine = client()
    await mine.aexecute(GetStore, {"id": "store-1"})
    await mine.aexecute(GetStore, {"id": "store-1", "note": None})
    await mine.aexecute(GetStore, {"id": "store-1", "note": "x"})
    assert mine.rath.sent == [{"id": "store-1"}, {"id": "store-1"}, {"id": "store-1", "note": "x"}]




@pytest.mark.asyncio
async def test_the_ambient_task_is_stamped_without_a_view() -> None:
    """One shared client attributes each call to whatever task is running."""
    from types import SimpleNamespace

    from rath.task import task_scope

    shared = client()
    await shared.aexecute(GetStore, {"id": "store-1"})
    with task_scope(SimpleNamespace(token="tok")):
        await shared.aexecute(GetStore, {"id": "store-1"})
    await shared.aexecute(GetStore, {"id": "store-1"})

    assert shared.rath.headers == [None, {TASK_HEADER: "tok"}, None]
    assert "task_token" not in Kraph.model_fields, "no per-task copy exists"


@pytest.mark.asyncio
async def test_a_task_named_at_the_call_beats_the_ambient_one() -> None:
    from types import SimpleNamespace

    from rath.task import task_scope

    shared = client()
    with task_scope(SimpleNamespace(token="ambient")):
        await shared.aexecute(
            GetStore, {"id": "store-1"}, task=SimpleNamespace(token="explicit")
        )

    assert shared.rath.headers == [{TASK_HEADER: "explicit"}]


# --------------------------------------------------------------------------- #
# The client
# --------------------------------------------------------------------------- #


def real_client(name: str) -> Kraph:
    return Kraph(rath=KraphRath(link=AsyncMockLink()), datalayer=DataLayer(endpoint_url=name))


def test_every_operation_is_a_method_of_the_client() -> None:
    kraph = real_client("self")

    assert callable(kraph.create_graph) and callable(kraph.aget_graph)
    assert set(Kraph.model_fields) == {"datalayer", "rath"}


@pytest.mark.asyncio
async def test_a_generated_method_calls_through_its_own_client(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    seen: list[Any] = []

    async def fake_aexecute(
        self: Any, operation: Any, variables: Any, task: Any = None
    ) -> Any:
        # Every generated method forwards `task=`, so the delegate takes it.
        seen.append(self)
        return SimpleNamespace(graph="the graph")

    monkeypatch.setattr(Kraph, "aexecute", fake_aexecute)
    kraph = real_client("self")

    assert await kraph.aget_graph(id="1") == "the graph"
    assert seen == [kraph]




# --------------------------------------------------------------------------- #
# What an object fetches later
# --------------------------------------------------------------------------- #


@pytest.fixture()
def downloaded(monkeypatch: pytest.MonkeyPatch) -> list[dict[str, Any]]:
    """Record which datalayer a download reaches for, without any I/O."""
    seen: list[dict[str, Any]] = []

    def fake_unkoil(function: Any, datalayer: Any, url: str, file_name: str) -> str:
        seen.append({"url": url, "datalayer": datalayer})
        return file_name

    monkeypatch.setattr("kraph.io.unkoil", fake_unkoil)
    return seen


def test_object_downloads_through_the_client_that_fetched_it(
    downloaded: list[dict[str, Any]],
) -> None:
    a, b = real_client("a"), real_client("b")
    store = Store.model_validate(
        {"id": "s", "presigned_url": "/media/file.bin", "key": "file.bin"},
        context=origin_context(client=a, rath=a.rath, datalayer=a.datalayer),
    )

    assert store.download() == "file.bin"
    store.download("elsewhere.bin", kraph=b)

    assert downloaded == [
        {"url": "/media/file.bin", "datalayer": a.datalayer},
        {"url": "/media/file.bin", "datalayer": b.datalayer},
    ]


def test_an_unfetched_object_needs_a_client(downloaded: list[dict[str, Any]]) -> None:
    store = Store(id="s", presigned_url="/media/file.bin", key="file.bin")

    with pytest.raises(NoKraphFound, match="kraph="):
        store.download()
    assert downloaded == []


def test_graph_polls_its_projection_through_its_own_client() -> None:
    asked: list[str] = []

    def fake(name: str) -> Any:
        def get_graph(id: str) -> Any:
            asked.append(name)
            return SimpleNamespace(projection=SimpleNamespace(projected_through_seq=7))

        return SimpleNamespace(get_graph=get_graph)

    class View(GraphTrait):
        id: str

    # Only a Kraph counts as a fetching client, so the origin carries a real one
    # whose method is swapped out; an explicit client may be anything shaped like one.
    a = real_client("a")
    object.__setattr__(a, "get_graph", fake("a").get_graph)
    view = View.model_validate({"id": "1"}, context=origin_context(client=a, rath=a.rath))

    assert view.wait_until_projected(7).projected_through_seq == 7
    assert View(id="2").wait_until_projected(7, kraph=fake("b")).projected_through_seq == 7
    assert asked == ["a", "b"]
    with pytest.raises(NoKraphFound):
        View(id="3").wait_until_projected(7)


def test_structure_resolves_through_the_registry_it_is_given(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class Pointer(StructureTrait):
        identifier: str
        object: str

    async def expand(id: str) -> str:
        return f"expanded {id}"

    registry = SimpleNamespace(
        get_fullfilled_structure=lambda identifier: SimpleNamespace(expand=expand)
    )
    pointer = Pointer(identifier="@mikro/image", object="5")

    with Koil():
        assert pointer.resolve(registry) == "expanded 5"  # type: ignore[arg-type]
