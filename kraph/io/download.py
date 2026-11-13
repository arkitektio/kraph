"""Reading a big file back: an access grant for its store, then its one object, streamed to disk.

Both clients are the ones the object was fetched with (``client_of``): the kraph that asks
for the grant, and its datalayer, which says where the store is. Nothing is looked up.
"""

from pathlib import Path
from typing import TYPE_CHECKING, Any

import obstore

from kraph.io.obstore import create_s3_store

if TYPE_CHECKING:
    from kraph.kraph import Kraph


def _target(file_name: str) -> str:
    Path(file_name).expanduser().resolve().parent.mkdir(parents=True, exist_ok=True)
    return file_name


def download_bigfile(store_id: str, file_name: str, kraph: "Kraph") -> str:
    """Stream the big file in ``store_id`` to ``file_name``. Returns the path written."""
    from kraph.api.schema import RequestBigFileAccessInput

    grant = kraph.request_bigfile_access(input=RequestBigFileAccessInput(store_id=store_id))
    store = create_s3_store(kraph.datalayer.endpoint_url, grant, proxy=kraph.datalayer.proxy)
    response = obstore.get(store, grant.key)
    with open(_target(file_name), "wb") as file:
        for chunk in response.stream():
            file.write(chunk)
    return file_name


async def adownload_bigfile(store_id: str, file_name: str, kraph: "Kraph") -> str:
    """Stream the big file in ``store_id`` to ``file_name``. Returns the path written."""
    from kraph.api.schema import RequestBigFileAccessInput

    grant = await kraph.arequest_bigfile_access(input=RequestBigFileAccessInput(store_id=store_id))
    store = create_s3_store(await kraph.datalayer.get_endpoint_url(), grant, proxy=kraph.datalayer.proxy)
    response = await obstore.get_async(store, grant.key)
    with open(_target(file_name), "wb") as file:
        async for chunk in response.stream():
            file.write(chunk)
    return file_name


def file_name_of(store: Any, file_name: str | None) -> str:  # noqa: ANN401
    """Where a download lands: the name asked for, else the uploaded file's own name, else its key's last part."""
    return file_name or getattr(store, "original_file_name", None) or str(store.key).rsplit("/", 1)[-1]
