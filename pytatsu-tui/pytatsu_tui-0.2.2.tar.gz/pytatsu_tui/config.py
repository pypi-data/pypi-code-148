import platform
import shutil
import subprocess
from configparser import ConfigParser
from pathlib import Path
from typing import NoReturn

from send2trash import send2trash
from termcolor import colored

# sourcery skip: raise-from-previous-error
try:
    from tkinter import Tk, filedialog
except ImportError:
    print(
        "Please install tkinter before continuing.",
        "\nGuide: https://tkdocs.com/tutorial/install.html",
    )
    raise SystemExit(1)


config_prsr = ConfigParser()

ERROR = colored("ERROR:", "red", attrs=["bold"])

SUCCESS = colored("Successfully", "green")

path_txt = Path("./path.txt").resolve()


def clear_terminal() -> int:
    """
    Clear the terminal
    """

    return subprocess.call(
        "cls" if platform.system() == "Windows" else "clear",
        shell=True,
    )


def strtobool(value: str) -> bool:
    """Convert a string value into a boolean.

    Example::

        if value in ("y", "yes", "t", "true", "on", "1"):
            return True
        else:
            return False
    """

    return value.lower().strip() in {"y", "yes", "t", "true", "on", "1"}


def wait_to_cont(*args, clear: bool = False) -> None:
    """
    Print a message then wait for user input to continue

    `clear` is to optionally clear the terminal beforehand
    """

    if clear:
        clear_terminal()

    if args:
        print(*args)

    input("\nEnter any key to continue\n\n: ")


def wait_to_exit(*args, clear: bool = False) -> NoReturn:
    """
    Print a message then wait for user input to exit

    `clear` is to optionally clear the terminal beforehand
    """

    if clear:
        clear_terminal()

    if args:
        print(*args)

    input("\nEnter any key to exit\n\n: ")

    raise SystemExit


def get_cfg_path() -> Path:
    """
    Create path.txt if it doesn't exist
    """

    clear_terminal()

    print("Please select a directory to save your blobs.\n")

    Tk().withdraw()

    try:
        directory = Path(
            filedialog.askdirectory(
                initialdir=Path.home(),
                title="Choose a directory for your blobs",
            )
        )

        path_txt.write_text(f"{directory}", encoding="utf-8")

        (directory / "permissionchecking12345").mkdir()

        (directory / "permissionchecking12345").rmdir()

    except PermissionError:
        path_txt.unlink()

        wait_to_exit(
            "Please select a directory where you have read and write permissions.",
            clear=True,
        )

    except TypeError:
        wait_to_exit(
            "Please make sure to select a directory.",
            clear=True,
        )

    return directory.resolve()


def config_dir() -> Path:
    """
    Path to where the config file, blobs, and buildmanifests are saved
    """

    if not path_txt.exists():
        return get_cfg_path()

    try:
        directory = Path(path_txt.read_text(encoding="utf-8").strip())

        (directory / "permissionchecking12345").mkdir()

        (directory / "permissionchecking12345").rmdir()

    except PermissionError:
        path_txt.unlink()

        wait_to_exit(
            "Please select a new directory where you have read and write permissions.",
            clear=True,
        )

    except OSError:
        path_txt.unlink()

        wait_to_exit(
            "Please select a new directory to save your config file.",
            clear=True,
        )

    return directory.resolve()


def create_config() -> None:
    """
    Create a config file if it doesn't exist
    """
    # sourcery skip: raise-from-previous-error

    if config_file().is_file():
        return

    clear_terminal()

    print("Config not found, creating a new one...\n")

    amount_of_devices = input("How many devices would you like to add?\n\n: ")

    try:
        devices = int(amount_of_devices)
    except ValueError:
        if amount_of_devices.strip() == "":
            raise SystemExit

        wait_to_exit(
            "Please enter the number of devices as an integer, not a string/float.",
            clear=True,
        )

    for i in range(1, devices + 1):
        config_entries(
            number=i,
        )

    wait_to_cont(
        f"{SUCCESS} added {devices} device(s) to the config!",
        clear=True,
    )


def add_device() -> None:
    """
    Add device(s) to the config
    """

    clear_terminal()

    total_devices = num_of_devices()[-1]

    amount_of_devices = input("How many new devices would you like to add?\n\n: ")

    try:
        devices = int(amount_of_devices)
    except ValueError:
        if amount_of_devices.strip() == "":
            return

        wait_to_cont(
            "Please enter the number of new devices as an integer.",
            clear=True,
        )
        return

    for i in range(1, devices + 1):
        config_entries(
            number=i,
            total=total_devices,
            cfg_exists=True,
        )

    wait_to_cont(
        f"{SUCCESS} added {devices} device(s) to the config!",
        clear=True,
    )


def config_entries(
    number: int,
    total: int = 0,
    cfg_exists: bool = False,
) -> None:
    """
    Input entries into the config file
    """
    # sourcery skip: merge-dict-assign

    if cfg_exists:
        number += total

    clear_terminal()

    print(
        "ENTERING INFORMATION FOR",
        f"{colored(f'DEVICE {number}', attrs=['underline'])}",
    )

    config_prsr[f"DEVICE {number}"] = {}

    config_prsr[f"DEVICE {number}"]["model"] = input("\nDevice Identifier?\n\n: ")

    config_prsr[f"DEVICE {number}"]["board"] = input("\nBoard Configuration?\n\n: ")

    config_prsr[f"DEVICE {number}"]["ecid"] = input(
        "\nExclusive Chip Identification (ECID)?\n\n: "
    )

    config_prsr[f"DEVICE {number}"]["generator"] = input(
        "\nGenerator? (Required for A12+)\n\n: "
    )

    config_prsr[f"DEVICE {number}"]["apnonce"] = input(
        "\nApNonce? (Required for A12+)\n\n: "
    )

    with config_file().open("w", encoding="utf-8") as f:
        config_prsr.write(f)


def config_file() -> Path:
    """
    Path to the config file
    """

    return config_dir() / "tatsu.ini"


def bm_dir() -> Path:
    """
    Path to the buildmanifests' directory
    """

    return config_dir() / "BuildManifests"


def blob_dir(device_number: int) -> Path:
    """
    Path to the directory where blobs are saved for the given device
    """

    return config_dir() / "Blobs" / f"DEVICE {device_number}"


def num_of_devices() -> list[int]:
    """
    Return the numbers of devices in the config
    """

    config_prsr.read(config_file())

    return [devices[0] for devices in enumerate(config_prsr.sections(), start=1)]


def rm_device() -> bool | None:
    """
    Remove device(s) from the config

    Returns `True` if a device was removed

    Returns `False/None` otherwise
    """

    clear_terminal()

    print("Which device would you like to remove?\n")

    for num in num_of_devices():
        model = config_prsr[f"DEVICE {num}"]["model"]
        print(f"{num}) DEVICE {num} ({colored(model, 'cyan')})")

    selected_device = input("\n: ")

    try:
        device = int(selected_device)
    except ValueError:
        if selected_device.strip() == "":
            return

        wait_to_cont(
            "Please enter an integer from the list of devices.",
            clear=True,
        )
        return

    if device in num_of_devices():
        clear_terminal()

        print(
            f"By proceeding, all saved blobs for DEVICE {device}",
            f"will be {colored('deleted', 'red', attrs=['underline'])}\n",
        )

        confirm = input("Are you sure you want to continue?\n\n[Y/N]: ")

        if confirm.strip() == "":
            return

        elif confirmed := strtobool(confirm):
            delete_blob_dirs(device)

            wait_to_cont(
                f"{SUCCESS} deleted DEVICE {device}!",
                clear=True,
            )

        else:
            wait_to_cont(
                "Aborting...",
                clear=True,
            )

        return confirmed

    else:
        wait_to_cont(
            f"DEVICE {colored(device, 'red')} does not exist.",
            clear=True,
        )


def delete_blob_dirs(device: int) -> None:
    """
    Delete the blob directory for the given device
    """

    if len(num_of_devices()) == device == 1:
        send2trash(config_file())

        if blob_dir(1).exists():
            send2trash(blob_dir(1))

        return

    if blob_dir(device).exists():
        send2trash(blob_dir(device))

    if device == 1:
        for existing in num_of_devices()[1:]:
            if (blob_dir(existing)).is_dir():
                shutil.move(
                    blob_dir(existing),
                    blob_dir(existing - 1),
                )
    else:
        for existing in num_of_devices()[device - 1 :]:  # noqa
            if (blob_dir(existing)).is_dir():
                shutil.move(
                    blob_dir(existing),
                    blob_dir(existing - 1),
                )

    update_config(device, num_of_devices()[-1])


def update_config(
    selected_device: int,
    total_devices: int,
) -> None:

    """
    Update the config after removing a device
    """

    config_prsr.read(config_file())

    config_prsr.remove_section(f"DEVICE {selected_device}")

    if selected_device != total_devices:
        for device in range(selected_device, total_devices + 1):
            if device != selected_device:
                items = config_prsr.items(f"DEVICE {device}")

                config_prsr.remove_section(f"DEVICE {device}")

                config_prsr.add_section(f"DEVICE {device - 1}")

                for key, val in items:
                    config_prsr.set(f"DEVICE {device - 1}", key, val)

    with config_file().open("w", encoding="utf-8") as a:
        config_prsr.write(a)
