import asyncio
import json
import os
import platform
import plistlib
import shutil
import subprocess
import sys
from collections.abc import Generator
from contextlib import contextmanager
from io import TextIOWrapper
from pathlib import Path
from time import sleep
from typing import NoReturn

import click
from pyimg4 import IM4M
from pytatsu.tss import TSS
from send2trash import send2trash
from termcolor import colored

from .api import devices_file, firmwares_file
from .config import (
    ERROR,
    SUCCESS,
    add_device,
    blob_dir,
    bm_dir,
    clear_terminal,
    config_file,
    create_config,
    path_txt,
    rm_device,
    strtobool,
    wait_to_cont,
    wait_to_exit,
)
from .devices import device_selection, get_device_info
from .parse import AllDevices, DeviceInfo, Firmwares


def save_blobs(device: DeviceInfo, firmwares: Firmwares) -> None:
    """
    Save blobs for the given device
    """

    clear_terminal()

    print(
        "Continuing to save blobs!",
        f"\n\nEnter {colored('A', 'green', attrs=['bold'])} to save blobs",
        f"for {colored('all', attrs=['underline'])} signed iOS versions",
        f"\n\nEnter {colored('M', 'yellow', attrs=['bold'])} to save blobs",
        f"for a {colored('singular', attrs=['underline'])} iOS version",
    )

    all_or_one = input("\n: ").lower().strip()

    if all_or_one == "":
        return

    elif all_or_one not in ("a", "m"):
        wait_to_cont(
            f'"{colored(all_or_one, "red")}" is not a valid option.',
            clear=True,
        )
        return

    elif all_or_one == "a":
        clear_terminal()

        if list_signed_vers(device, firmwares):
            print("\nPlease wait", end="")

            for ios_versions in firmwares.all_signed:
                version_num, version_build = firmwares.dissect(ios_versions[0])[1:]

                asyncio.run(
                    firmwares.download_manifest(
                        device,
                        version=version_num,
                        build=version_build,
                        indicate=False,
                    )
                )

                tss_request(device, version=version_num, build=version_build)

                print(".", end="", flush=True)

            wait_to_cont(
                f"\n\n{SUCCESS} saved blobs of all signed iOS versions",
                f"for DEVICE {device.number}!",
            )

        else:
            wait_to_cont()

    elif all_or_one == "m":
        clear_terminal()

        manual_version = input(
            "Please enter an iOS version name or build identifier\n\n: "
        )

        if manual_version.strip() == "":
            return

        version_name, version_num, version_build = firmwares.dissect(manual_version)

        if version_name is None:
            wait_to_cont(
                f'"{colored(manual_version, "red")}"',
                f"is not a valid iOS version/build identifier for the {device.name}.",
                clear=True,
            )
            return

        elif firmwares.signing_status(version_name):
            clear_terminal()

            print(
                f"Signing status of iOS {version_name} ({version_build})",
                f"for the {device.name}: {colored('TRUE', 'green')}",
            )

            asyncio.run(
                firmwares.download_manifest(
                    device,
                    version=version_num,
                    build=version_build,
                )
            )

            tss_request(device, version=version_num, build=version_build)

            wait_to_cont(f"\n{SUCCESS} saved blobs for DEVICE {device.number}!")

        else:
            wait_to_cont(
                f"Signing status of iOS {version_name} ({version_build})",
                f"for the {device.name}: {colored('FALSE', 'red')}",
                f"\n\n{colored('Unable', 'red')} to save blobs for DEVICE {device.number}.",
                clear=True,
            )


def view_blob_info(device: DeviceInfo, firmwares: Firmwares) -> None:
    """
    View blob information for the given device using pyimg4/img4tool
    """

    clear_terminal()

    print(
        "Continuing to view blob information!",
        "\n\nPlease enter an iOS version name or build identifier",
    )

    manual_version = input("\n: ")

    if manual_version.strip() == "":
        return

    version_name, version_num, version_build = firmwares.dissect(manual_version)

    if version_name is None:
        wait_to_cont(
            f'"{colored(manual_version, "red")}"',
            f"is not a valid iOS version/build identifier for the {device.name}.",
            clear=True,
        )
        return

    for file in os.listdir(blob_dir(device.number)):
        if (
            file.startswith(f"{device.ecid}")
            and file.find(f"{version_num}-{version_build}") != -1
            and file.endswith(".shsh2")
        ) or file == f"{version_num}-{version_build}.shsh2":

            blob_file = file
            break

    else:
        wait_to_cont(
            f"{ERROR} Cannot find saved blobs of iOS {version_name} ({version_build})",
            f"for DEVICE {device.number}",
            "\n\nTry saving it first.",
            clear=True,
        )
        return

    asyncio.run(
        firmwares.download_manifest(
            device,
            version=version_num,
            build=version_build,
        )
    )

    img4tool_output = subprocess.run(
        [
            Path(f"./bins/{platform.system()}").resolve() / "img4tool",
            "-s",
            blob_dir(device.number) / blob_file,
            "-v",
            bm_dir() / f"{version_num}-{version_build}-{device.board}.plist",
        ],
        capture_output=True,
        check=True,
        text=True,
    )

    lines = len(img4tool_output.stdout.split("\n"))

    blob_info = img4tool_output.stdout.split("\n")[lines - 11 : lines - 2]  # noqa

    with (blob_dir(device.number) / blob_file).open("rb") as shsh_file:

        data = plistlib.load(shsh_file)

        shsh_info = IM4M(data["ApImg4Ticket"])

    clear_terminal()

    print(f"DEVICE : {device.number} [{device.name}]")

    for text in blob_info[:3]:
        print(
            text.replace(
                f"BuildNumber : {version_build}",
                f"iOS Vers. : {colored(version_name, 'yellow')} ({colored(version_build, 'yellow')})",
            )
        )

    print(
        f"ECID (Hex) : {shsh_info.ecid:X}",
        f"\nECID (Decimal) : {shsh_info.ecid}",
        f"\nGenerator : {data['generator']}",
        f"\nApNonce : {shsh_info.apnonce.hex()}",
    )

    for text in blob_info[3:-1]:
        print(text)

    wait_to_cont(
        blob_info[-1]
        .replace(
            "GOOD",
            colored("GOOD", "green", attrs=["bold"]),
        )
        .replace(
            "BAD",
            colored("BAD", "red", attrs=["bold"]),
        ),
    )


# Rename blobs saved with tsschecker
def rename_blobs(device: DeviceInfo) -> None:
    """
    Renames all blobs for the given device

    From::

        "ecid - model - board - version - build - apnonce.shsh2"

    To::

        "version - build.shsh2"
    """

    clear_terminal()

    blobs_to_be_renamed = []

    for file in os.listdir(blob_dir(device.number)):
        if (
            file.endswith(".shsh2")
            and file.lower().find(f"{device.ecid}_{device.model.lower()}") != -1
        ):
            blobs_to_be_renamed.append(file)

            blob_name, shsh2 = os.path.splitext(file)

            vers_build = blob_name.split("_")[3]

            shutil.move(
                blob_dir(device.number) / file,
                blob_dir(device.number) / f"{vers_build}{shsh2}",
            )

    wait_to_cont(
        f"{SUCCESS} renamed {len(blobs_to_be_renamed)} blob(s)",
        f"for DEVICE {device.number}!",
    )


def list_saved_blobs(device: DeviceInfo, firmwares: Firmwares) -> None:
    """
    List the number of saved blobs for the given device
    """

    clear_terminal()

    saved_blobs = set()

    for file in os.listdir(blob_dir(device.number)):
        if file.endswith(".shsh2"):
            blob_1st_half, blob_2nd_half = file.split("-")

            # saved with tsschecker
            if (
                blob_1st_half.lower().find(f"{device.ecid}_{device.model.lower()}")
                != -1
            ):
                build = blob_2nd_half.split("_")[0]

            # pytatsu
            else:
                build = os.path.splitext(blob_2nd_half)[0]

            version_name, version_build = firmwares.dissect(build)[::2]

            # For the iOS versions that aren't scraped (yet)
            if version_name is None:

                # saved with tsschecker
                if (
                    blob_1st_half.lower().find(f"{device.ecid}_{device.model.lower()}")
                    != -1
                ):
                    version_name = blob_1st_half.split("_")[3]
                    version_build = blob_2nd_half.split("_")[0]

                # pytatsu
                else:
                    version_name = blob_1st_half
                    version_build = blob_2nd_half.split(".")[0]

            saved_blobs.add(f"iOS {version_name} ({version_build})")

    if (len_blobs := len(saved_blobs)) >= 1:
        if len_blobs == 1:
            print(
                f"You have {colored('1', 'green')} blob saved",
                f"for DEVICE {device.number} [{device.name}]:\n",
            )

        else:
            print(
                f"You have {colored(len_blobs, 'green')} blobs saved",
                f"for DEVICE {device.number} [{device.name}]:\n",
            )

        for blob in sorted(saved_blobs):
            print(blob)

    else:
        print(
            f"There are {colored('NO', 'red')} blobs saved",
            f"for DEVICE {device.number} [{device.name}]",
        )

    wait_to_cont()


def list_signed_vers(device: DeviceInfo, firmwares: Firmwares) -> bool:
    """
    List all signed iOS versions for the given device

    Returns `True` if there is one or more signed iOS version(s)

    Returns `False` otherwise
    """

    clear_terminal()

    if (len_signed := len([*firmwares.all_signed])) >= 1:
        if len_signed == 1:
            print(
                f"There is only {colored('1', 'yellow')}",
                f"signed iOS version for the {device.name}:\n",
            )

        else:
            print(
                f"There are {colored(len_signed, 'green')}",
                f"signed iOS versions for the {device.name}:\n",
            )

        for version_name, version_build in firmwares.all_signed:
            print(f"iOS {version_name} ({version_build})")

        return True

    print(
        f"There are {colored('NO', 'red')}",
        f"signed iOS versions for the {device.name}",
    )

    return False


def delete_manifests(device_number: int, board: str) -> None:
    """
    Delete all BuildManifest.plist files for the given device number
    """

    clear_terminal()

    print(
        f"By proceeding, all BuildManifests for DEVICE {device_number}",
        f"will be {colored('deleted', 'red', attrs=['underline'])}",
    )

    i = input("\nAre you sure you want to continue?\n\n[Y/N]: ")

    if i.strip() == "":
        return

    elif strtobool(i):
        send2trash(
            plists := [plist for plist in bm_dir().iterdir() if board in f"{plist}"],
        )

        wait_to_cont(
            f"{SUCCESS} deleted {len(plists)} BuildManifest files for DEVICE {device_number}!",
            clear=True,
        )

    else:
        wait_to_cont(
            "Aborting...",
            clear=True,
        )


@contextmanager
def hide_prints() -> Generator[TextIOWrapper, None, None]:
    """
    Hide all print calls within a context manager
    """

    og_stdout = sys.stdout

    try:
        sys.stdout = open(os.devnull, "w", encoding="utf-8")
        yield sys.stdout
    finally:
        sys.stdout.close()
        sys.stdout = og_stdout


def tss_request(device: DeviceInfo, *, version: str, build: str) -> None:
    """
    Send a post request to Apple's TSS for the given device

    `version` must be the base iOS version number

    `build` must be the iOS version's build identifier
    """

    blob = Path("./blob.shsh2")

    tss = TSS(
        board=device.board,
        ecid=device.ecid,
        generator=device.generator,
        apnonce=device.apnonce,
        build_manifest_path=str(bm_dir() / f"{version}-{build}-{device.board}.plist"),
    )

    with hide_prints():
        tss.send_request()

    if blob.is_file():
        shutil.move(
            blob,
            blob_dir(device.number) / f"{version}-{build}.shsh2",
        )


@click.command()
@click.option(
    "-u",
    "--unset",
    is_flag=True,
)
def main(unset: bool) -> NoReturn:
    """
    Display list of options
    """

    if unset and path_txt.exists():
        old_directory = path_txt.read_text(encoding="utf-8").strip()

        path_txt.unlink()

        print(f'Unset saved directory: "{old_directory}"')

        return

    device = DeviceInfo(*get_device_info(device_selection()))

    while True:
        clear_terminal()

        with (
            firmwares_file.open(encoding="utf-8") as device_firmwares_file,
            devices_file.open(encoding="utf-8") as device_info_file,
        ):
            ios_firmware_data = json.load(device_firmwares_file)
            apple_firmwares = Firmwares(**ios_firmware_data)

            ios_device_data = json.load(device_info_file)
            apple_devices = AllDevices(**ios_device_data)

        device.name = apple_devices.check(device.model, device.board)

        if device.name is None:
            wait_to_exit(
                f"{ERROR} Invalid BOARD for DEVICE {device.number}",
                f'\n\nThe board configuration for "{device.model}" is NOT "{device.board}"'
                f"\n\nPlease edit {config_file()} before continuing.",
            )

        device.name = colored(device.name, "cyan")

        device.board = device.board.lower()

        print(f"DEVICE: {device.number} [{device.name}]")

        print(
            "\n1) Save blobs",
            "\n2) View blob info",
            "\n3) Rename blobs",
            "\n4) List all saved blobs",
            "\n5) List all signed firmwares",
            "\n6) Change current device",
            "\n7) Add new device(s)",
            "\n8) Remove device(s)",
            "\n9) Delete BuildManifests",
            "\nElse) Exit",
        )

        options = input("\n: ")

        match options:
            case "1":
                save_blobs(device, apple_firmwares)

            case "2":
                view_blob_info(device, apple_firmwares)

            case "3":
                rename_blobs(device)

            case "4":
                list_saved_blobs(device, apple_firmwares)

            case "5":
                list_signed_vers(device, apple_firmwares)

                wait_to_cont()

            case "6":
                main()

            case "7":
                add_device()

            case "8":
                if rm_device():
                    create_config()
                    main(device_selection())

            case "9":
                delete_manifests(device.number, device.board)

            case _:
                print("\nExiting...")
                sleep(1)
                clear_terminal()
                raise SystemExit
