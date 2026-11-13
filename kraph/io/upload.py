"""Writing a big file under a grant: the one write the upload middleware drives.

Requesting the grant and finishing the upload are the middleware's
(:class:`kraph.middleware.upload.UploadMiddleware`); this only puts the bytes where the grant
says, through a store whose credentials renew themselves while it runs.
"""

import logging
from typing import TYPE_CHECKING

import obstore

from kraph.errors import UploadError
from kraph.io.obstore import create_s3_store
from kraph.scalars import BigFile

if TYPE_CHECKING:
    from kraph.api.schema import BigFileUploadGrant
    from kraph.datalayer import DataLayer

logger = logging.getLogger(__name__)


def upload_bigfile(file: BigFile, credentials: "BigFileUploadGrant", datalayer: "DataLayer") -> str:
    """Write ``file`` to the object its grant names, synchronously. Returns the store id."""
    store = create_s3_store(datalayer.endpoint_url, credentials, proxy=datalayer.proxy)
    try:
        obstore.put(store, credentials.key, file.value)
    except Exception as e:
        raise UploadError(f"Error while uploading to s3://{credentials.bucket}/{credentials.key} on {datalayer.endpoint_url}") from e
    logger.info("Uploaded %s to s3://%s/%s", file.file_name, credentials.bucket, credentials.key)
    return credentials.store


async def aupload_bigfile(file: BigFile, credentials: "BigFileUploadGrant", datalayer: "DataLayer") -> str:
    """Write ``file`` to the object its grant names. Returns the store id."""
    endpoint_url = await datalayer.get_endpoint_url()
    store = create_s3_store(endpoint_url, credentials, proxy=datalayer.proxy)
    try:
        await obstore.put_async(store, credentials.key, file.value)
    except Exception as e:
        raise UploadError(f"Error while uploading to s3://{credentials.bucket}/{credentials.key} on {endpoint_url}") from e
    logger.info("Uploaded %s to s3://%s/%s", file.file_name, credentials.bucket, credentials.key)
    return credentials.store
