import os
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from sw_product_lib.client.platform import API, Operation
from sw_product_lib.errors.error import StrangeworksError


@dataclass
class Job:
    id: str
    child_jobs: Optional[List]
    external_identifier: Optional[str]
    slug: Optional[str]
    resource: Optional[Dict[str, Any]]
    status: Optional[str]
    is_terminal_state: Optional[str]
    remote_status: Optional[str] = None
    job_data_schema: Optional[str] = None
    job_data: Optional[Dict[str, Any]] = None

    def as_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @staticmethod
    def from_dict(res: dict):
        child_jobs: List[Job] = []
        if "childJobs" in res:
            for _, child_job in res["childJobs"]:
                child_jobs.append(Job.from_dict(child_job))

        return Job(
            id=res["id"],
            external_identifier=res["externalIdentifier"],
            slug=res["slug"],
            resource=res["resource"] if "resource" in res else None,
            status=res["status"],
            is_terminal_state=res["isTerminalState"]
            if "isTerminalState" in res
            else None,
            remote_status=res["remoteStatus"] if "remoteStatus" in res else None,
            job_data_schema=res["jobDataSchema"] if "jobDataSchema" in res else None,
            job_data=res["jobData"] if "jobData" in res else None,
            child_jobs=child_jobs,
        )


@dataclass
class File:
    id: str
    slug: Optional[str] = None
    label: Optional[str] = None
    file_name: Optional[str] = None
    url: Optional[str] = None

    @classmethod
    def from_dict(cls, d: dict):
        return File(
            id=d["id"],
            slug=d["slug"],
            label=d["label"],
            url=d["url"],
            file_name=d["fileName"],
        )


create_request = Operation(
    query="""
        mutation jobCreate(
            $resource_slug: String!,
            $workspace_member_slug: String!,
            $parent_job_slug: String,
            $external_identifier: String,
            $status: JobStatus,
            $remote_status: String,
            $job_data_schema: String,
            $job_data: JSON) {
            jobCreate(input: {
                resourceSlug: $resource_slug,
                workspaceMemberSlug: $workspace_member_slug,
                parentJobSlug: $parent_job_slug,
                externalIdentifier: $external_identifier,
                status: $status,
                remoteStatus: $remote_status,
                jobDataSchema: $job_data_schema,
                jobData: $job_data,
            }) {
                job {
                id
                externalIdentifier
                slug
                status
                isTerminalState
                remoteStatus
                jobDataSchema
                jobData
                }
            }
        }
        """,
)


def create(
    api: API,
    resource_slug: str,
    workspace_member_slug: str,
    parent_job_slug: Optional[str] = None,
    external_identifier: Optional[str] = None,
    status: Optional[str] = None,
    remote_status: Optional[str] = None,
    job_data_schema: Optional[str] = None,
    job_data: Optional[str] = None,
) -> Job:
    """Create a job entry

    Parameters
    ----------
    api: API
        provides access to the platform API.
    resource_slug: str
        used as identifier for the resource.
    workspaceMemberSlug: str
        used to map workspace and user.
    parentJobSlug: Optional[str]
        slug of the job which created this job.
    external_identifier: Optional[str]
        id typically generated as a result of making a request to an external system.
    status: {Optionapstr
        status of the job. Refer to the  platform for possible values.
    remoteStatus: Optional[str]
        status of job that was initiated on an  external (non-Strangeworks) system.
    jobDataSchema: Optional[str]
        link to the json schema describing job output.
    jobData: Optional[str]
        job output.

    Returns
    -------
    : Job
        The ``Job`` object
    """
    platform_result = api.execute(
        op=create_request,
        **locals(),
    )

    return Job.from_dict(platform_result["jobCreate"]["job"])


update_request = Operation(
    query="""
        mutation jobUpdate(
            $resource_slug: String!,
            $job_slug: String!,
            $parent_job_slug: String,
            $external_identifier: String,
            $status: JobStatus,
            $remote_status: String,
            $job_data_schema: String,
            $job_data: JSON) {
            jobUpdate(input: {
                resourceSlug: $resource_slug,
                jobSlug: $job_slug,
                parentJobSlug: $parent_job_slug,
                externalIdentifier: $external_identifier,
                status: $status,
                remoteStatus: $remote_status,
                jobDataSchema: $job_data_schema,
                jobData: $job_data,
            }) {
                job {
                id
                externalIdentifier
                slug
                status
                isTerminalState
                remoteStatus
                jobDataSchema
                jobData
                }
            }
        }
        """,
)


def update(
    api: API,
    resource_slug: str,
    job_slug: str,
    parent_job_slug: Optional[str] = None,
    external_identifier: Optional[str] = None,
    status: Optional[str] = None,
    remote_status: Optional[str] = None,
    job_data_schema: Optional[str] = None,
    job_data: Optional[str] = None,
) -> Job:
    """Make an update to a job entry.

    Parameters
    ----------
    api: API
        provides access to the platform API.
    resource_slug: str
        used as identifier for the resource.
    job_slug: str
        identifier used to retrieve the job.
    parent_job_slug: Optional[str]
        slug of the job which created this job.
    external_identifier: Optional[str]
        id typically generated as a result of making a request to an external system.
    status: {Optionapstr
        status of the job. Refer to the  platform for possible values.
    remote_status: Optional[str]
        status of job that was initiated on an  external (non-Strangeworks) system.
    job_data_schema: Optional[str]
        link to the json schema describing job output.
    job_data: Optional[str]
        job output.

    Returns
    -------
    : Job
        The ``Job`` object
    """
    platform_result = api.execute(
        op=update_request,
        **locals(),
    )
    return Job.from_dict(platform_result["jobUpdate"]["job"])


def get_job_request(query: str, job_param_name: str) -> Operation:
    return Operation(
        query=f"""
        query {query} (
            $resource_slug: String!,
            $id: String!) {{
            {query}(
                resourceSlug: $resource_slug,
                {job_param_name}: $id
            )
            {{
                id
                childJobs {{
                    id
                }}
                externalIdentifier
                slug
                status
                isTerminalState
                remoteStatus
                jobDataSchema
                jobData
            }}
        }}
        """
    )


def get(
    api: API,
    resource_slug: str,
    id: str,
) -> Job:
    """Retrieve job info

    Parameters
    ----------
    api: API
        provides access to the platform API.
    resource_slug: str
        identifier for the resource.
    id: str
        the job_slug identifier used to retrieve the job.

    Returns
    -------
    Job
        The ``Job`` object identified by the slug.
    """
    platform_result = api.execute(
        op=get_job_request("job", "jobSlug"),
        **locals(),
    )
    return Job.from_dict(platform_result["job"])


get_jobs_request = Operation(
    query="""
        query jobs(
            $external_identifier: String,
            $resource_slug: String,
            $parent_job_slug: String,
        ) {
            jobs(
                externalIdentifier: $external_identifier,
                resourceSlug: $resource_slug,
                parentJobSlug: $parent_job_slug
            ) {
                edges {
                    node {
                        id
                        slug
                        status
                        resource {
                            slug
                        }
                        externalIdentifier
                        isTerminalState
                        remoteStatus
                        dateJobCreated
                        dateJobCompleted
                    }
                }
            }
        }
""",
)


def get_by_external_identifier(
    api: API,
    id: str,
) -> Optional[Job]:
    """Retrieve job info

    Parameters
    ----------
    api: API
        provides access to the platform API.
    id: str
        the external_identifier used to retrieve the job.

    Returns
    -------
    Job
        The ``Job`` object identified by id or None.
    """
    platform_result = api.execute(
        op=get_jobs_request,
        external_identifier=id,
    )
    if "jobs" not in platform_result:
        raise StrangeworksError(
            message="Missing field ('jobs') in response to jobs query", status_code=400
        )
    if "edges" not in platform_result["jobs"]:
        raise StrangeworksError(
            message="Missing field ('edges') in response to jobs query", status_code=400
        )

    if len(platform_result["jobs"]["edges"]) == 0:
        return None

    if len(platform_result["jobs"]["edges"]) > 1:
        raise StrangeworksError(
            message="More than one job returned for product identifier", status_code=400
        )

    if "node" not in platform_result["jobs"]["edges"][0]:
        raise StrangeworksError(
            message="Missing field ('node') in response to jobs query", status_code=400
        )

    val = platform_result["jobs"]["edges"][0]["node"]
    return Job.from_dict(val)


upload_file_request = Operation(
    query="""
        mutation jobUploadFile(
            $resource_slug: String!,
            $job_slug: String!,
            $override_existing: Boolean!,
            $file_name: String!,
            $json_schema: String,
            $is_hidden: Boolean!,
            $sort_weight: Int!,
            $label: String,
            $content_type: String!,
            $meta_file_type: String,
            $meta_file_size: Int,
            $meta_file_create_date: Time,
            $meta_file_modified_date: Time,
            $is_public: Boolean! = false,
        ){
            jobUploadFile(
                input: {
                    resourceSlug: $resource_slug,
                    jobSlug: $job_slug,
                    shouldOverrideExistingFile: $override_existing,
                    fileName: $file_name,
                    jsonSchema: $json_schema,
                    isHidden: $is_hidden,
                    sortWeight: $sort_weight,
                    label: $label,
                    contentType: $content_type,
                    metaFileType: $meta_file_type,
                    metaFileSize: $meta_file_size,
                    metaFileCreateDate: $meta_file_create_date,
                    metaFileModifiedDate: $meta_file_modified_date,
                    isPublic: $is_public,
                }
            ){
                signedURL
                file {
                    id
                    slug
                    label
                    fileName
                    url
                    metaFileType
                    metaDateCreated
                    metaDateModified
                    metaSizeBytes
                    jsonSchema
                    dateCreated
                    dateUpdated
                }
            }
        }
        """,
)


def upload_file(
    api: API,
    resource_slug: str,
    job_slug: str,
    file_path: str,
    override_existing: bool = False,
    is_hidden: bool = False,
    is_public: bool = False,
    sort_weight: int = 0,
    file_name: Optional[str] = None,
    json_schema: Optional[str] = None,
    label: Optional[str] = None,
    content_type: Optional[str] = None,
) -> Tuple[File, str]:
    """Upload a file associated with a job.

    Parameters
    ----------
    api: API
        provides access to the platform API.
    resource_slug: str
        identifier for the resource.
    job_slug: str
        the strangeworks identefier of the job.
    file_path: str
        fully qualified path to the file.
    override_existing: bool
        If True, any existing file with the same name owned by this `Job`
          will be replaced with this file.
    is_hidden: bool
        If true, this file will not be displayed in the portal.
        This can be useful for supporting files that should be saved against the job,
          but typically would be referenced by URL in other contexts.
        (i.e.: an image file which is referenced in a JSON model.)
        This does **not*** prevent a user from accessing this file
          in other contexts, such as job archives.
    is_public: bool
        If True, this file may be accessed by the URL with no authentication.
        In general, most files should NOT be public.
    sort_weight: int
        This is the primary sorting instruction for JobFiles
         when returned to the client.
        The default is 0.
        Files with a higher sort order will be returned first.
        This allows you to control the order of files in the portal if desired.
    file_name: Optional[str]
        the name given to the file.
        This takes precedence over the name in file_path. Must be unique per Job.
    json_schema: Optional[str]
        A full URL to a JSON Schema document which will be used to
         label and validate the content of this file.
        If set, the system will assume the file contains JSON data.
        Please refer to documentation for common platform schemas.
    label: Optional[str]
        An optional label that will be displayed to users in the portal
         instead of the file name "Results 01", etc.
    content_type: Optional[str]
        Used to indicate the original media type of what is going to be uploaded.
        Defaults to `application/x-www-form-urlencoded`.

    Returns
    -------
    File
        The ``File`` object that contains platform information about the file.
    str
        A signed url where the file can be uploaded to.

    """
    p = Path(file_path)
    stats = p.stat()
    meta_size = stats.st_size
    meta_create_date = datetime.fromtimestamp(
        stats.st_ctime, tz=timezone.utc
    ).isoformat()
    meta_modified_date = datetime.fromtimestamp(
        stats.st_mtime, tz=timezone.utc
    ).isoformat()
    meta_type = p.suffix[1:]  # suffix without the .
    if meta_type == "" and file_name:
        # could be the case that p.suffix is coming from a temporary file
        # the temporary file can be without an extension
        # the user could have correctly named the file with an extension
        # so as a final attempt we try to pull the extension from the user file name
        _, ext = os.path.splitext(file_name)
        meta_type = ext[1:]  # again, without the .
    name = file_name or p.name
    ct = content_type or "application/x-www-form-urlencoded"
    res = api.execute(
        op=upload_file_request,
        resource_slug=resource_slug,
        job_slug=job_slug,
        file_name=name,
        override_existing=override_existing,
        json_schema=json_schema,
        is_hidden=is_hidden,
        sort_weight=sort_weight,
        label=label,
        is_public=is_public,
        content_type=ct,
        meta_file_type=meta_type,
        meta_file_size=meta_size,
        meta_file_create_date=meta_create_date,
        meta_file_modified_date=meta_modified_date,
    ).get("jobUploadFile")
    if not res:
        raise StrangeworksError(message="unable to get valid response from platform")

    if "error" in res:
        raise StrangeworksError(message=res.get("error"))
    f = res.get("file")
    signedUrl = res.get("signedURL")
    if not f or not signedUrl:
        raise StrangeworksError(
            message="unable to obtain file details or a place to upload the file"
        )
    return (File.from_dict(f), signedUrl)
