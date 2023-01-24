from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from strangeworks.core.client.platform import API, Operation


@dataclass
class File:
    """Class representing a file."""

    id: str
    slug: str
    label: Optional[str] = None
    file_name: Optional[str] = None
    url: Optional[str] = None

    @classmethod
    def from_dict(cls, d: dict):
        """Generate a File object from a dictionary."""
        return File(
            id=d.get("id"),
            slug=d.get("slug"),
            label=d.get("label", None),
            file_name=d.get("fileName", None),
            url=d.get("url", None),
        )


_upload_file = Operation(
    query="""
    mutation uploadWorkspaceFile($workspace_slug: String!, $file: Upload!) {
	  workspaceUploadFile(input: { workspaceSlug: $workspace_slug, file: $file }) {
		file {
			id
			slug
			label
			fileName
			url
		}
      }
    }
    """,
    upload_files=True,
)


def upload(client: API, workspace_slug: str, file_path: str) -> File:
    """Upload a file to the associated workspace."""
    with open(file_path, "rb") as fd:
        platform_result = client.execute(
            op=_upload_file, workspace_slug=workspace_slug, file=fd
        )
        return File.from_dict(platform_result["workspaceUploadFile"]["file"])
