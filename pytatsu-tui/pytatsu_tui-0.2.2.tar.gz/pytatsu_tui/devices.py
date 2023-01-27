import asyncio
import re
import string

from termcolor import colored

from .api import request_apis
from .config import (
    ERROR,
    blob_dir,
    clear_terminal,
    config_dir,
    config_file,
    config_prsr,
    num_of_devices,
    wait_to_cont,
    wait_to_exit,
)


def device_selection() -> int:
    """
    Select a device from the config
    """
    # sourcery skip: raise-from-previous-error

    while True:
        config_prsr.read(config_file())

        clear_terminal()

        print(f"Config directory: {config_dir()}\n")

        print("Please select a device\n")

        for num in num_of_devices():
            model = config_prsr[f"DEVICE {num}"]["model"]
            print(f"{num}) DEVICE {num} ({colored(model, 'cyan')})")

        selected_device = input("\n: ")

        try:
            device = int(selected_device)
        except ValueError:
            if selected_device.strip() == "":
                raise SystemExit

            wait_to_cont(
                "Please enter a number from the list of devices.",
                clear=True,
            )
            continue

        if device not in num_of_devices():
            wait_to_cont(
                f"DEVICE {colored(device, 'red')} does not exist.",
                clear=True,
            )
            continue

        blob_dir(device).mkdir(0o755, parents=True, exist_ok=True)

        return device


def isdex(value: str) -> bool:
    """
    Determine if value is a decimal/hex string
    """

    return all(
        charctrs in set(string.hexdigits) for charctrs in value.removeprefix("0x")
    )


def get_device_info(device: int) -> tuple[int, str, str, int, str, str]:
    """
    Returns the stored values for the given device in the config
    """

    config_prsr.read(config_file())

    if (
        re.search(
            r"(ipod|iphone|ipad|appletv)[0-9]{1,2},[0-9]{1,2}",
            config_prsr[f"DEVICE {device}"]["model"].lower(),
        )
        is None
    ):
        wait_to_exit(
            f"{ERROR} Invalid MODEL for DEVICE {device}",
            f'\n\n"{config_prsr[f"DEVICE {device}"]["model"]}" is not a valid device model.',
            "\n\nThis script supports iPods, iPhones, iPads, and Apple TVs.",
            f"\n\nPlease edit {config_file()} before continuing.",
            clear=True,
        )

    for key, value in config_prsr.items(f"DEVICE {device}"):
        value = value.strip()

        if value == "" and key not in ("apnonce", "generator"):
            wait_to_exit(
                f"{ERROR} Missing the value of {key.upper()} for DEVICE {device}",
                f"\n\nPlease edit {config_file()} before continuing.",
                clear=True,
            )

        elif not value.isalnum() and key != "model":
            if key not in ("apnonce", "generator") and len(value) != 0:
                wait_to_exit(
                    f"{ERROR} Do not use any spaces/special characters",
                    f"in the {key.upper()} of DEVICE {device}",
                    f"\n\nPlease edit {config_file()} before continuing.",
                    clear=True,
                )

        elif not isdex(value) and key in (
            "ecid",
            "apnonce",
        ):
            if key == "ecid":
                wait_to_exit(
                    f"{ERROR} Invalid ECID for DEVICE {device}",
                    "\n\nCurrent value is neither decimal or hexadecimal.",
                    f"\n\nPlease edit {config_file()} before continuing.",
                    clear=True,
                )

            wait_to_exit(
                f"{ERROR} Invalid APNONCE for DEVICE {device}",
                "\n\nCurrent value is not a valid hexadecimal string."
                f"\n\nPlease edit {config_file()} before continuing.",
                clear=True,
            )

        elif ((1 <= len(value) < 18) or (len(value) > 18)) and key == "generator":

            wait_to_exit(
                f"{ERROR} Invalid GENERATOR for DEVICE {device}",
                f"\n\nCurrent length: {len(value)}\nAccepted length: 18",
                f"\n\nPlease edit {config_file()} before continuing.",
                clear=True,
            )

    model = config_prsr[f"DEVICE {device}"]["model"].strip()
    board = config_prsr[f"DEVICE {device}"]["board"].strip()
    ecid = config_prsr[f"DEVICE {device}"]["ecid"].strip()
    generator = config_prsr[f"DEVICE {device}"]["generator"].strip()
    apnonce = config_prsr[f"DEVICE {device}"]["apnonce"].strip()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(request_apis(model))

    return (
        device,
        model,
        board,
        int(ecid) if ecid.isdecimal() else int(ecid, 16),
        generator,
        apnonce,
    )
