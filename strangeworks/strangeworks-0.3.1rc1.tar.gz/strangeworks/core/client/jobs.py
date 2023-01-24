"""jobs.py."""
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from strangeworks.core.client.platform import API, Operation
from strangeworks.core.client.resource import Resource
from strangeworks.core.errors.error import StrangeworksError
from strangeworks.core.client.file import File


@dataclass
class Job:
    """Object representing a Strangeworks platform job entry."""

    slug: str
    child_jobs: Optional[List]
    external_identifier: Optional[str]
    resource: Optional[Dict[str, Any]]
    status: Optional[str]
    is_terminal_state: Optional[str]
    remote_status: Optional[str] = None
    job_data_schema: Optional[str] = None
    job_data: Optional[Dict[str, Any]] = None
    files: Optional[List[File]] = None

    @staticmethod
    def from_dict(res: Dict[str, Any]):
        """Generate a Job object from dictionary."""
        child_jobs: List[Job] = []
        if "childJobs" in res:
            for _, child_job in res["childJobs"]:
                child_jobs.append(Job.from_dict(child_job))

        files: List[File] = []
        if "files" in res:
            for _, f in res["files"]:
                files.append(File.from_dict(f))

        resource = Resource.from_dict(res.get("resource"))
        return Job(
            external_identifier=res.get("externalIdentifier"),
            slug=res.get("slug"),
            resource=resource,
            status=res.get("status"),
            is_terminal_state=res.get("isTerminalState"),
            remote_status=res.get("remoteStatus"),
            job_data_schema=res.get("jobDataSchema"),
            job_data=res.get("jobData"),
            child_jobs=child_jobs,
            files=files,
        )

    def is_complete(self) -> bool:
        """Check if job is in terminal state.

        deprecated method, kept to limit number of changes
        required for extension SDKs
        """
        return self.is_terminal_state


_get_jobs = Operation(
    query="""
     query sdk_get_jobs(
        $job_slug: String,
        $resource_slugs: [String!],
        $product_slugs: [String!],
        $statuses: [JobStatus!]
    ){
        workspace {
            jobs(
                jobSlug: $job_slug,
                resourceSlugs: $resource_slugs,
                productSlugs: $product_slugs,
                jobStatuses: $statuses
            ) {
                edges {
                    node {
                        slug
                        externalIdentifier
                        status
                        resource {
                            slug
                            isDeleted
                            product {
                                slug
                                name
                            }
                        }
                    }
                }
            }
        }
    }
    """
)


def get(
    client: API,
    job_slug: Optional[str] = None,
    resource_slugs: Optional[List[str]] = None,
    product_slugs: Optional[List[str]] = None,
    statuses: Optional[List[str]] = None,
) -> Optional[List[Job]]:
    """Return list of jobs associated with the current workspace.

    If no parameters (other than client) are specified, the function will return all
    jobs associated with the current workspace account.Caller can filter results
    through specifying parameters. The filters are cumulative, meaning only jobs
    matching all specified criteria will be returned.

    Parameters
    ----------
    client: StrangeworksGQLClient
        client to access the sdk api on the platform.
    job_slub: Optional[str]
        Filter to retrieve only the job whose slug matches. Defaults to None.
    resource_slugs: Optional[List[str]]
        List of resource identifiers. Only jobs with matching resource will be returned.
        Defaults to None.
    product_slugs: Optional[List[str]]
        List of product identifiers called slugs. Only jobs for matching products will
        be retuned. Defaults to None.
    statuses: Optional[List[str]]
        List of job statuses. Only jobs whose statuses match will be returned. Defaults
        to None.

    Return
    ------
    Optional[List[Job]]
        List of Job objects that match the given criteria.
    """
    workspace = client.execute(op=_get_jobs, **locals()).get("workspace")

    if not workspace:
        raise StrangeworksError(
            message="unable to retrieve jobs information (no workspace returned"
        )
    jobs = workspace.get("jobs")
    return (
        list(map(lambda x: Job.from_dict(x.get("node")), jobs.get("edges")))
        if jobs
        else None
    )
