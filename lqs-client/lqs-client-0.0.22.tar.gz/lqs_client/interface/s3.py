from uuid import UUID
from enum import Enum
from typing import Optional, Union, List

import requests
import xmltodict


class S3Method(str, Enum):
    abort_multipart_upload = "abort_multipart_upload"
    complete_multipart_upload = "complete_multipart_upload"
    create_multipart_upload = "create_multipart_upload"
    delete_object = "delete_object"
    get_object = "get_object"
    head_object = "head_object"
    list_multipart_uploads = "list_multipart_uploads"
    list_object_versions = "list_object_versions"
    list_objects_v2 = "list_objects_v2"
    list_parts = "list_parts"
    put_object = "put_object"
    restore_object = "restore_object"
    upload_part = "upload_part"


class S3Resource(str, Enum):
    extraction = "extraction"
    ingestion = "ingestion"
    log = "log"
    record = "record"
    topic = "topic"


class S3:
    def __init__(self, creator):
        self._creator = creator

    def generate_presigned_url(
        self,
        method: S3Method,
        resource: S3Resource,
        params: dict,
        resource_id: UUID = None,
        timestamp: Optional[float] = None,
    ):
        if resource == "extraction":
            presigned_url = self._creator.extraction_presigned_url(
                extraction_id=resource_id, method=method, params=params
            )
        elif resource == "ingestion":
            presigned_url = self._creator.ingestion_presigned_url(
                ingestion_id=resource_id, method=method, params=params
            )
        elif resource == "log":
            presigned_url = self._creator.log_presigned_url(
                log_id=resource_id, method=method, params=params
            )
        elif resource == "record":
            if timestamp is None:
                raise ValueError("timestamp is required.")
            presigned_url = self._creator.record_presigned_url(
                topic_id=resource_id, timestamp=timestamp, method=method, params=params
            )
        elif resource == "topic":
            presigned_url = self._creator.topic_presigned_url(
                topic_id=resource_id, method=method, params=params
            )
        else:
            raise ValueError(f"Unknown resource {resource}.")
        url = presigned_url["url"]
        used_params = presigned_url["params"]
        return url, used_params

    def abort_multi_part_upload(
        self,
        resource: S3Resource,
        resource_id: Union[str, dict],
        key: str,
        upload_id: str,
    ):
        if resource in ["record"]:
            if (
                isinstance(resource_id, str)
                or "topic_id" not in resource_id
                or "timestamp" not in resource_id
            ):
                raise ValueError(
                    "When resource is 'record', resource_id must be a dict with values 'topic_id' and 'timestamp'."
                )
            timestamp = resource_id["timestamp"]
            resource_id = resource_id["topic_id"]
        else:
            timestamp = None
        params = {
            "Key": key,
            "UploadId": upload_id,
        }
        url, used_params = self.generate_presigned_url(
            method="abort_multipart_upload",
            resource=resource,
            params=params,
            resource_id=resource_id,
            timestamp=timestamp,
        )
        r = requests.delete(url)
        return r.headers, used_params, None

    def complete_multipart_upload(
        self,
        resource: S3Resource,
        resource_id: Union[str, dict],
        key: str,
        upload_id: str,
        parts: List[dict],
        convert_to_dict: bool = True,
    ):
        if resource in ["record"]:
            if (
                isinstance(resource_id, str)
                or "topic_id" not in resource_id
                or "timestamp" not in resource_id
            ):
                raise ValueError(
                    "When resource is 'record', resource_id must be a dict with values 'topic_id' and 'timestamp'."
                )
            timestamp = resource_id["timestamp"]
            resource_id = resource_id["topic_id"]
        else:
            timestamp = None
        params = {
            "Key": key,
            "UploadId": upload_id,
        }
        url, used_params = self.generate_presigned_url(
            method="complete_multipart_upload",
            resource=resource,
            params=params,
            resource_id=resource_id,
            timestamp=timestamp,
        )
        complete_multipart_payload = "<CompleteMultipartUpload>"
        for part in parts:
            if "ETag" not in part or "PartNumber" not in part:
                raise ValueError("Part must contain 'ETag' and 'PartNumber'.")
            part["ETag"] = part["ETag"].strip('"')
            complete_multipart_payload += f"""
            <Part>
                <PartNumber>{part["PartNumber"]}</PartNumber>
                <ETag>{part["ETag"]}</ETag>
            </Part>
            """
        complete_multipart_payload += "</CompleteMultipartUpload>"

        r = requests.post(url, data=complete_multipart_payload)
        response_content = xmltodict.parse(r.text) if convert_to_dict else r.text
        return r.headers, used_params, response_content

    def create_multipart_upload(
        self,
        resource: S3Resource,
        resource_id: Union[str, dict],
        key: str,
        convert_to_dict: bool = True,
    ):
        if resource in ["record"]:
            if (
                isinstance(resource_id, str)
                or "topic_id" not in resource_id
                or "timestamp" not in resource_id
            ):
                raise ValueError(
                    "When resource is 'record', resource_id must be a dict with values 'topic_id' and 'timestamp'."
                )
            timestamp = resource_id["timestamp"]
            resource_id = resource_id["topic_id"]
        else:
            timestamp = None
        params = {"Key": key}
        url, used_params = self.generate_presigned_url(
            method="create_multipart_upload",
            resource=resource,
            params=params,
            resource_id=resource_id,
            timestamp=timestamp,
        )
        r = requests.post(url)
        response_content = xmltodict.parse(r.text) if convert_to_dict else r.text
        return r.headers, used_params, response_content

    def delete_object(
        self,
        resource: S3Resource,
        resource_id: Union[str, dict],
        key: str,
        version_id: Optional[str] = None,
    ):
        if resource in ["record"]:
            if (
                isinstance(resource_id, str)
                or "topic_id" not in resource_id
                or "timestamp" not in resource_id
            ):
                raise ValueError(
                    "When resource is 'record', resource_id must be a dict with values 'topic_id' and 'timestamp'."
                )
            timestamp = resource_id["timestamp"]
            resource_id = resource_id["topic_id"]
        else:
            timestamp = None
        params = {"Key": key}
        if version_id is not None:
            params["VersionId"] = version_id
        url, used_params = self.generate_presigned_url(
            method="delete_object",
            resource=resource,
            params=params,
            resource_id=resource_id,
            timestamp=timestamp,
        )
        r = requests.delete(url)
        return r.headers, used_params, None

    def get_object(
        self,
        resource: S3Resource,
        resource_id: Union[str, dict],
        key: str,
        part_number: Optional[int] = None,
    ):
        if resource in ["record"]:
            if (
                isinstance(resource_id, str)
                or "topic_id" not in resource_id
                or "timestamp" not in resource_id
            ):
                raise ValueError(
                    "When resource is 'record', resource_id must be a dict with values 'topic_id' and 'timestamp'."
                )
            timestamp = resource_id["timestamp"]
            resource_id = resource_id["topic_id"]
        else:
            timestamp = None
        params = {"Key": key}
        if part_number is not None:
            params["PartNumber"] = part_number
        url, used_params = self.generate_presigned_url(
            method="get_object",
            resource=resource,
            params=params,
            resource_id=resource_id,
            timestamp=timestamp,
        )
        r = requests.get(url)
        return r.headers, used_params, r.content

    def head_object(
        self,
        resource: S3Resource,
        resource_id: Union[str, dict],
        key: str,
        part_number: Optional[int] = None,
        version_id: Optional[str] = None,
    ):
        if resource in ["record"]:
            if (
                isinstance(resource_id, str)
                or "topic_id" not in resource_id
                or "timestamp" not in resource_id
            ):
                raise ValueError(
                    "When resource is 'record', resource_id must be a dict with values 'topic_id' and 'timestamp'."
                )
            timestamp = resource_id["timestamp"]
            resource_id = resource_id["topic_id"]
        else:
            timestamp = None
        params = {"Key": key}
        if part_number is not None:
            params["PartNumber"] = part_number
        if version_id is not None:
            params["VersionId"] = version_id
        url, used_params = self.generate_presigned_url(
            method="head_object",
            resource=resource,
            params=params,
            resource_id=resource_id,
            timestamp=timestamp,
        )
        r = requests.head(url)
        return r.headers, used_params, None

    def list_multipart_uploads(
        self,
        resource: S3Resource,
        resource_id: Union[str, dict],
        convert_to_dict: bool = True,
    ):
        if resource in ["record"]:
            if (
                isinstance(resource_id, str)
                or "topic_id" not in resource_id
                or "timestamp" not in resource_id
            ):
                raise ValueError(
                    "When resource is 'record', resource_id must be a dict with values 'topic_id' and 'timestamp'."
                )
            timestamp = resource_id["timestamp"]
            resource_id = resource_id["topic_id"]
        else:
            timestamp = None
        params = {}
        url, used_params = self.generate_presigned_url(
            method="list_multipart_uploads",
            resource=resource,
            params=params,
            resource_id=resource_id,
            timestamp=timestamp,
        )
        r = requests.get(url)
        response_content = xmltodict.parse(r.text) if convert_to_dict else r.text
        return r.headers, used_params, response_content

    def list_object_versions(
        self,
        resource: S3Resource,
        resource_id: Union[str, dict],
        convert_to_dict: bool = True,
    ):
        if resource in ["record"]:
            if (
                isinstance(resource_id, str)
                or "topic_id" not in resource_id
                or "timestamp" not in resource_id
            ):
                raise ValueError(
                    "When resource is 'record', resource_id must be a dict with values 'topic_id' and 'timestamp'."
                )
            timestamp = resource_id["timestamp"]
            resource_id = resource_id["topic_id"]
        else:
            timestamp = None
        params = {}
        url, used_params = self.generate_presigned_url(
            method="list_object_versions",
            resource=resource,
            params=params,
            resource_id=resource_id,
            timestamp=timestamp,
        )
        r = requests.get(url)
        response_content = xmltodict.parse(r.text) if convert_to_dict else r.text
        return r.headers, used_params, response_content

    def list_objects_v2(
        self,
        resource: S3Resource,
        resource_id: Union[str, dict],
        continuation_token: Optional[str] = None,
        convert_to_dict: bool = True,
    ):
        if resource in ["record"]:
            if (
                isinstance(resource_id, str)
                or "topic_id" not in resource_id
                or "timestamp" not in resource_id
            ):
                raise ValueError(
                    "When resource is 'record', resource_id must be a dict with values 'topic_id' and 'timestamp'."
                )
            timestamp = resource_id["timestamp"]
            resource_id = resource_id["topic_id"]
        else:
            timestamp = None
        params = {}
        if continuation_token is not None:
            params["ContinuationToken"] = continuation_token
        url, used_params = self.generate_presigned_url(
            method="list_objects_v2",
            resource=resource,
            params=params,
            resource_id=resource_id,
            timestamp=timestamp,
        )
        r = requests.get(url)
        response_content = xmltodict.parse(r.text) if convert_to_dict else r.text
        return r.headers, used_params, response_content

    def list_parts(
        self,
        resource: S3Resource,
        resource_id: Union[str, dict],
        key: str,
        upload_id: str,
        part_number_marker: Optional[int] = None,
        convert_to_dict: bool = True,
    ):
        if resource in ["record"]:
            if (
                isinstance(resource_id, str)
                or "topic_id" not in resource_id
                or "timestamp" not in resource_id
            ):
                raise ValueError(
                    "When resource is 'record', resource_id must be a dict with values 'topic_id' and 'timestamp'."
                )
            timestamp = resource_id["timestamp"]
            resource_id = resource_id["topic_id"]
        else:
            timestamp = None
        params = {"Key": key, "UploadId": upload_id}
        if part_number_marker is not None:
            params["PartNumberMarker"] = part_number_marker
        url, used_params = self.generate_presigned_url(
            method="list_parts",
            resource=resource,
            params=params,
            resource_id=resource_id,
            timestamp=timestamp,
        )
        r = requests.get(url)
        response_content = xmltodict.parse(r.text) if convert_to_dict else r.text
        return r.headers, used_params, response_content

    def put_object(
        self, resource: S3Resource, resource_id: Union[str, dict], key: str, body: bytes
    ):
        if resource in ["record"]:
            if (
                isinstance(resource_id, str)
                or "topic_id" not in resource_id
                or "timestamp" not in resource_id
            ):
                raise ValueError(
                    "When resource is 'record', resource_id must be a dict with values 'topic_id' and 'timestamp'."
                )
            timestamp = resource_id["timestamp"]
            resource_id = resource_id["topic_id"]
        else:
            timestamp = None
        params = {"Key": key}
        url, used_params = self.generate_presigned_url(
            method="put_object",
            resource=resource,
            params=params,
            resource_id=resource_id,
            timestamp=timestamp,
        )
        r = requests.put(url, data=body)
        return r.headers, used_params, None

    def restore_object(self):
        raise NotImplementedError("Restore object is not implemented yet.")

    def upload_part(
        self,
        resource: S3Resource,
        resource_id: Union[str, dict],
        key: str,
        body: bytes,
        part_number: int,
        upload_id: str,
    ):
        if resource in ["record"]:
            if (
                isinstance(resource_id, str)
                or "topic_id" not in resource_id
                or "timestamp" not in resource_id
            ):
                raise ValueError(
                    "When resource is 'record', resource_id must be a dict with values 'topic_id' and 'timestamp'."
                )
            timestamp = resource_id["timestamp"]
            resource_id = resource_id["topic_id"]
        else:
            timestamp = None
        params = {"Key": key, "PartNumber": part_number, "UploadId": upload_id}
        url, used_params = self.generate_presigned_url(
            method="upload_part",
            resource=resource,
            params=params,
            resource_id=resource_id,
            timestamp=timestamp,
        )
        r = requests.put(url, data=body)
        return r.headers, used_params, None
