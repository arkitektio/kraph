"""A file in a request goes to kraph's datalayer first, the way every service's client sends one.

The middleware requests a grant declaring the file's size, writes under it, finishes the
upload and sends the store id in the file's place; a write that fails is reported with
``valid=False`` and its error raised. Nothing here touches a server or an object store.
"""

import asyncio
import io
from types import SimpleNamespace
from typing import Any

import pytest

from kraph.datalayer import DataLayer
from kraph.middleware import upload as upload_module
from kraph.middleware.upload import UploadMiddleware
from kraph.scalars import BigFile

GRANT = {"accessKey": "a", "secretKey": "s", "sessionToken": "t", "path": "s3://b/k", "key": "k", "bucket": "b", "expiresIn": 3600, "store": "store-1"}
STORE = {"id": "store-1", "key": "k", "bucket": "b", "path": "s3://b/k", "originalFileName": "weights.zip", "sizeBytes": 3}


class Rath:
    """Answers the three datalayer mutations and records what was asked."""

    def __init__(self) -> None:
        """Nothing asked yet."""
        self.asked: list[tuple[str, dict]] = []

    async def aquery(self, document: str, variables: dict[str, Any]) -> SimpleNamespace:
        """Answer by the mutation's name, as the server would."""
        name = document.split("mutation ", 1)[1].split("(", 1)[0]
        self.asked.append((name, variables["input"]))
        answer = {"RequestBigfileUpload": {"requestBigfileUpload": GRANT}, "FinishBigfileUpload": {"finishBigfileUpload": STORE}}[name]
        return SimpleNamespace(data=answer)


def _run(middleware: UploadMiddleware, rath: Rath, variables: dict) -> dict:
    return asyncio.run(middleware.aprocess_variables(variables, None, rath))  # type: ignore[arg-type]


def test_a_file_is_uploaded_finished_and_sent_as_its_store(monkeypatch: pytest.MonkeyPatch) -> None:
    """Grant (declaring the size), write, finish: then the store id travels instead of the bytes."""

    async def write(file: BigFile, grant: Any, datalayer: DataLayer) -> str:  # noqa: ANN401
        assert (grant.key, grant.bucket) == ("k", "b"), "the write goes where the grant says"
        return grant.store

    monkeypatch.setattr(upload_module, "aupload_bigfile", write)
    rath = Rath()
    weights = BigFile(io.BytesIO(b"abc"), file_name="weights.zip")

    sent = _run(UploadMiddleware(datalayer=DataLayer()), rath, {"input": {"name": "care", "store": weights}})

    assert sent == {"input": {"name": "care", "store": "store-1"}}
    assert rath.asked == [
        ("RequestBigfileUpload", {"originalFileName": "weights.zip", "fileSize": 3}),
        ("FinishBigfileUpload", {"storeId": "store-1", "valid": True}),
    ]


def test_a_failed_write_is_reported_and_raised(monkeypatch: pytest.MonkeyPatch) -> None:
    """The server ends the upload at once (valid=False); the write's own error is what the caller sees."""

    async def write(file: BigFile, grant: Any, datalayer: DataLayer) -> str:  # noqa: ANN401
        raise ConnectionError("the store went away")

    monkeypatch.setattr(upload_module, "aupload_bigfile", write)
    rath = Rath()

    with pytest.raises(ConnectionError, match="went away"):
        _run(UploadMiddleware(datalayer=DataLayer()), rath, {"input": {"store": BigFile(io.BytesIO(b"abc"), file_name="w.zip")}})
    assert rath.asked[-1] == ("FinishBigfileUpload", {"storeId": "store-1", "valid": False})
