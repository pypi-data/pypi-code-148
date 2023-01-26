from dateutil.parser import isoparse
from docker import DockerClient
from docker.models.images import Image as DockerImage
from docker.models.containers import Container as DockerContainer
from docker.errors import APIError
from .models import ContainerRuntimeInfo, Image, Container, Port
from .errors import ContainerRuntimeAPIError, ModelMappingError

required_info_keys = [
    "NCPU",
    "Architecture",
    "KernelVersion",
    "Name",
    "OperatingSystem",
    "OSType",
    "OSVersion",
    "ServerVersion",
]


def _find_missing_keys(required, actual):
    missing_fields = list(set(required).difference(actual))
    return sorted(missing_fields)


def get_runtime_info() -> ContainerRuntimeInfo:
    try:
        client = DockerClient.from_env()
        raw_data = client.info()

        missing = _find_missing_keys(required_info_keys, raw_data)
        if len(missing) > 0:
            missing_formated = ", ".join(missing)
            raise ModelMappingError(
                "Error mapping from Docker API response."
                f" Missing expected fields: {missing_formated}"
            )

        return ContainerRuntimeInfo(
            cpu_count=int(raw_data["NCPU"]),
            cpu_architecture=raw_data["Architecture"],
            kernel_version=raw_data["KernelVersion"],
            name=raw_data["Name"],
            os=raw_data["OperatingSystem"],
            os_type=raw_data["OSType"],
            os_version=raw_data["OSVersion"],
            server_version=raw_data["ServerVersion"],
        )
    except APIError as ex:
        raise ContainerRuntimeAPIError(
            "Error while pulling runtime information from Docker API", ex
        )


def get_images() -> list[Image]:
    try:
        client = DockerClient.from_env()
        raw_image_list = client.images.list()
        return list(map(_map_image, raw_image_list))
    except APIError as ex:
        raise ContainerRuntimeAPIError(
            "Error while pulling list of images from Docker API", ex
        )


def get_containers() -> list[Container]:
    try:
        client = DockerClient.from_env()
        raw_container_list = client.containers.list()
        return list(map(_map_container, raw_container_list))
    except APIError as ex:
        raise ContainerRuntimeAPIError(
            "Error while pulling list of containers from Docker API", ex
        )


def _map_image(raw_image: DockerImage) -> Image:
    repo_tags = raw_image.attrs.get("RepoTags")[0].split(":")
    image_id = "".join(raw_image.short_id.split(":")[-1:])
    return Image(
        name=repo_tags[0],
        tag=repo_tags[1],
        image_id=image_id,
        created=isoparse(raw_image.attrs.get("Created")),
        size_bytes=raw_image.attrs.get("Size"),
    )


def _map_container(raw_container: DockerContainer) -> Container:
    image = " ".join(raw_container.image.tags)
    return Container(
        id=raw_container.short_id,
        name=raw_container.name,
        status=raw_container.status,
        image=image,
        command=raw_container.attrs["Path"],
        ports=[
            Port(container=key, host=value)
            for key, value in raw_container.ports.items()
        ],
    )
