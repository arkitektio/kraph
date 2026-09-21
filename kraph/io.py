from typing import TYPE_CHECKING

import aiohttp
from koil import unkoil

if TYPE_CHECKING:
    from kraph.datalayer import DataLayer


async def adownload_file(datalayer: "DataLayer", presigned_url: str, file_name: str) -> str:
    """Download a presigned url from ``datalayer`` into ``file_name``."""
    endpoint_url = await datalayer.get_endpoint_url()

    async with aiohttp.ClientSession() as session:
        async with session.get(endpoint_url + presigned_url) as response:
            with open(file_name, "wb") as file:
                while True:
                    chunk = await response.content.read(
                        1024
                    )  # read the response by chunks of 1024 bytes
                    if not chunk:
                        break
                    file.write(chunk)

    return file_name


def download_file(datalayer: "DataLayer", presigned_url: str, file_name: str) -> str:
    """Blocking :func:`adownload_file`."""
    return unkoil(adownload_file, datalayer, presigned_url, file_name)
