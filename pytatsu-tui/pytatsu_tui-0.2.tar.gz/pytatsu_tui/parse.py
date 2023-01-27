import shutil
from typing import Any

import attrs
import httpx
from remotezip import RemoteZip

from .api import TIMEOUT
from .config import ERROR, bm_dir, wait_to_exit


@attrs.define
class DeviceInfo:
    """
    Put information for the selected device into a class object
    """

    number: int
    model: str
    board: str
    ecid: int
    generator: str
    apnonce: str
    name: str | None = attrs.field(init=False)


@attrs.define
class AllDevices:
    """
    Parse info from devices.json
    """

    devices: list[dict[str, str]]

    def check(self, model: str, board: str) -> str | None:
        """
        Returns the iOS device name if given arguments is a valid model/board combination

        Example::

            if (model, board) == ("iPhone12,5", "D431AP"):
                return "iPhone 11 Pro Max"
        """

        return next(
            (
                device["name"]
                for device in self.devices
                if (model.lower(), board.lower())
                == (device["identifier"], device["board"])
            ),
            None,
        )


@attrs.define
class Firmwares:
    """
    Parse info from firmwares.json
    """

    firmwares: list[dict[str, Any]]

    def dissect(self, version: str) -> list[str] | list[None]:
        """
        Returns::

            [version name, base version number, version build id] or [None, None, None]

        `version` can be the name or build identifier of an iOS version

        Example::

            if version == "15.6 beta" or version == "19G5027e":
                return ["15.6 beta", "15.6", "19G5027e"]
        """

        for entry in self.firmwares:
            if version.lower() in (entry["name"].lower(), entry["build"].lower()):
                return [entry["name"], entry["base"], entry["build"]]

        return [None for _ in range(3)]

    def signing_status(self, version: str) -> bool | None:
        """
        Returns the signing status of a given version

        `version` can be the name or build identifier of an iOS version

        Example::

            if version == "15.6 beta" or version == "19G5027e":
                return True | False
        """

        return next(
            (
                entry["signed"]
                for entry in self.firmwares
                if version.lower() in (entry["name"].lower(), entry["build"].lower())
            ),
            None,
        )

    @property
    def all_signed(self) -> list[tuple[str, str]]:
        """
        Lists all signed iOS version names with their corresponding build identifiers
        """

        signed_names: list[str] = [
            *filter(self.signing_status, [entry["name"] for entry in self.firmwares])
        ]

        signed_builds: list[str] = [
            *filter(self.signing_status, [entry["build"] for entry in self.firmwares])
        ]

        # if the RC becomes the GM
        duplicates = {
            build for build in signed_builds if signed_builds.count(build) > 1
        }

        for dupe in duplicates:
            vers, build = self.dissect(dupe)[::2]
            signed_names.remove(vers)
            signed_builds.remove(build)

        return sorted(zip(signed_names, signed_builds))

    async def download_manifest(
        self,
        device: DeviceInfo,
        *,
        version: str,
        build: str,
        indicate: bool = True,
    ) -> None:
        """
        Extracts the BuildManifest.plist from an Apple IPSW link

        `version` must be the base iOS version number

        `build` must be the iOS version's build identifier

        `indicate` is to optionally print a dowloading indicator
        """

        if (bm_dir() / f"{version}-{build}-{device.board}.plist").is_file():
            return

        if indicate:
            print("\nDownloading BuildManifest...")

        for entry in self.firmwares:
            if build == entry["build"]:
                ipsw_url = entry["ipsw"]
                bm_url = entry["buildmanifest"]

        try:
            async with httpx.AsyncClient(timeout=TIMEOUT) as client:
                bm_request = await client.get(bm_url)

        except httpx.ConnectError:
            wait_to_exit(
                f"{ERROR} Please check your internet connection and try again later.",
                clear=True,
            )

        except (httpx.ConnectTimeout, httpx.ReadTimeout):
            wait_to_exit(
                f"{ERROR} Timed out while receiving data from api get request.",
                "\n\nPlease try again later.",
                clear=True,
            )

        if bm_request.status_code == 200:
            (bm_dir() / f"{version}-{build}-{device.board}.plist").write_bytes(
                bm_request.content
            )

        else:
            with RemoteZip(ipsw_url) as ipsw_file:
                ipsw_file.extract("BuildManifest.plist")

            shutil.move(
                "./BuildManifest.plist",
                bm_dir() / f"{version}-{build}-{device.board}.plist",
            )
