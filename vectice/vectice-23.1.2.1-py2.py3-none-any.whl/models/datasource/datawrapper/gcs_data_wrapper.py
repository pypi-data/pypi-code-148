from __future__ import annotations

from typing import TYPE_CHECKING

from vectice.models.datasource.datawrapper.data_wrapper import DataWrapper
from vectice.models.datasource.datawrapper.metadata import DatasetSourceUsage, File, FilesMetadata, SourceOrigin

if TYPE_CHECKING:
    from google.cloud.storage import Blob, Bucket, Client


class GcsDataWrapper(DataWrapper):
    """Wrap columnar data and its metadata in GCS."""

    def __init__(
        self,
        gcs_client: Client,
        bucket_name: str,
        resource_paths: str | list[str],
        name: str,
        usage: DatasetSourceUsage | None = None,
        inputs: list[int] | None = None,
    ):
        """Initialize a GCS data wrapper.

        Parameters:
            gcs_client: The `google.cloud.storage.Client` used
                to interact with Google Cloud Storage.
            bucket_name: The name of the bucket to get data from.
            resource_paths: The paths of the resources to get.
            usage: The usage of the dataset.
            name: The name of the dataWrapper.
            inputs: The list of dataset ids to create a new dataset from.
        """
        self.bucket_name = bucket_name
        self.resource_paths = resource_paths if isinstance(resource_paths, list) else [resource_paths]
        self.gcs_client = gcs_client
        super(GcsDataWrapper, self).__init__(name, usage, inputs)

    def _fetch_data(self) -> dict[str, bytes]:
        datas = {}
        for path in self.resource_paths:
            blob = self._get_blob(path)
            datas[f"{self.bucket_name}/{path}"] = blob.download_as_bytes()
        return datas

    def _build_metadata(self) -> FilesMetadata:
        files = []
        size = 0
        for path in self.resource_paths:
            blob = self._get_blob(path)
            blob_file = self._build_file_from_blob(blob)
            files.append(blob_file)
            size += blob_file.size
        metadata = FilesMetadata(
            size=size,
            origin=SourceOrigin.GCS,
            files=files,
            files_count=len(files),
            usage=self.usage,
        )
        return metadata

    def _get_blob(self, path: str) -> Blob:
        from google.cloud import storage

        bucket: Bucket = storage.Bucket(self.gcs_client, name=self.bucket_name)
        blob = bucket.get_blob(blob_name=path)
        if blob is None:
            raise NoSuchGcsResourceError(self.bucket_name, path)
        blob.reload()
        return blob

    def _build_file_from_blob(self, blob: Blob) -> File:
        return File(
            name=blob.name,
            size=blob.size,
            fingerprint=blob.md5_hash,
            created_date=blob.time_created.isoformat(),
            updated_date=blob.updated.isoformat(),
            uri=f"gs://{self.bucket_name}/{blob.name}",
        )


class NoSuchGcsResourceError(Exception):
    def __init__(self, bucket: str, resource: str):
        self.message = f"{resource} does not exist in the GCS bucket {bucket}."
        super().__init__(self.message)

    def __str__(self):
        return self.message
