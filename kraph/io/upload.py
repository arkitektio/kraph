"""Writing a big file under a grant: the one write the upload middleware drives.

Requesting the grant and finishing the upload are the middleware's
(:class:`kraph.middleware.upload.UploadMiddleware`); this only puts the bytes where the grant
says, through a store whose credentials renew themselves while it runs.
"""

import io
import logging
import os
from typing import TYPE_CHECKING, cast

import obstore

from kraph.errors import UploadError
from kraph.io.obstore import create_s3_store
from kraph.scalars import BigFile

if TYPE_CHECKING:
    from kraph.api.schema import BigFileUploadGrant
    from kraph.datalayer import DataLayer

logger = logging.getLogger(__name__)


#: Sent with every request and part of a big-file upload, so the object store verifies it.
BIGFILE_CHECKSUM = "SHA256"


def part_size_for(size: int) -> int:
    """The part size the server's digest of a ``size``-byte file is cut at (``arkitekt_datalayer.digest``).

    8 MiB, doubled until the parts fit S3's 10,000. Computed here, not read off the grant, so
    an upload to a hub that does not advertise it still has its digest verified on arrival.
    """
    part = 8 * 1024 * 1024
    while size > part * 10_000:
        part *= 2
    return part


def _remaining_bytes(value: object) -> int:
    """How many bytes a write will send: a buffer's length, a path's size, or a file object's rest, left where it was."""
    if isinstance(value, (bytes, bytearray, memoryview)):
        return len(value)
    if isinstance(value, (str, os.PathLike)):
        return os.path.getsize(value)
    stream = cast("io.IOBase", value)
    position = stream.tell()
    end = stream.seek(0, io.SEEK_END)
    stream.seek(position)
    return end - position


def upload_bigfile(
    file: BigFile, credentials: "BigFileUploadGrant", datalayer: "DataLayer"
) -> str:
    """Write ``file`` to the object its grant names, synchronously. Returns the store id."""
    store = create_s3_store(
        datalayer.endpoint_url,
        credentials,
        proxy=datalayer.proxy,
        certificates=datalayer.certificates,
        checksum_algorithm=BIGFILE_CHECKSUM,
    )
    try:
        obstore.put(
            store,
            credentials.key,
            file.value,
            chunk_size=part_size_for(_remaining_bytes(file.value)),
        )
    except Exception as e:
        raise UploadError(
            f"Error while uploading to s3://{credentials.bucket}/{credentials.key} on {datalayer.endpoint_url}"
        ) from e
    logger.info(
        "Uploaded %s to s3://%s/%s", file.file_name, credentials.bucket, credentials.key
    )
    return credentials.store


async def aupload_bigfile(
    file: BigFile, credentials: "BigFileUploadGrant", datalayer: "DataLayer"
) -> str:
    """Write ``file`` to the object its grant names. Returns the store id."""
    endpoint_url = await datalayer.get_endpoint_url()
    store = create_s3_store(
        endpoint_url,
        credentials,
        proxy=datalayer.proxy,
        certificates=datalayer.certificates,
        checksum_algorithm=BIGFILE_CHECKSUM,
    )
    try:
        await obstore.put_async(
            store,
            credentials.key,
            file.value,
            chunk_size=part_size_for(_remaining_bytes(file.value)),
        )
    except Exception as e:
        raise UploadError(
            f"Error while uploading to s3://{credentials.bucket}/{credentials.key} on {endpoint_url}"
        ) from e
    logger.info(
        "Uploaded %s to s3://%s/%s", file.file_name, credentials.bucket, credentials.key
    )
    return credentials.store
