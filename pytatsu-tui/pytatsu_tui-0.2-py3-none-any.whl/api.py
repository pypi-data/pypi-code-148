import asyncio
import json
import re
from pathlib import Path

import httpx

from .config import ERROR, wait_to_exit

firmwares_file = Path("./firmwares.json")

devices_file = Path("./devices.json")

TIMEOUT = httpx.Timeout(15.0)


def request_apis(model: str) -> asyncio.Future[tuple[None, None]]:
    """
    Run get requests in parallel
    """

    return asyncio.gather(
        __ios_firmwares(model),
        __ios_devices(),
    )


async def __ios_firmwares(model: str) -> None:
    """
    Create a json file containing data of all stable/beta firmwares for the given device model
    """

    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            stable_api = await client.get(
                f"https://api.ipsw.me/v4/device/{model}",
                params={"type": "ipsw"},
            )

            beta_api = await client.get(
                f"https://api.m1sta.xyz/betas/{model}",
            )

    except httpx.ConnectError:
        wait_to_exit(
            f"{ERROR} Please check your internet connection and try again.",
            clear=True,
        )

    except (httpx.ConnectTimeout, httpx.ReadTimeout):
        wait_to_exit(
            f"{ERROR} Timed out while receiving data from get requests.",
            "\n\nPlease try again later.",
            clear=True,
        )

    with firmwares_file.open("w", encoding="utf-8") as a:
        json.dump({"firmwares": []}, a, indent=2)

    with firmwares_file.open(encoding="utf-8") as b:
        data = json.load(b)

    if stable_api.status_code == beta_api.status_code == 200:
        for x in stable_api.json()["firmwares"]:
            data["firmwares"].append(x)

        for y in beta_api.json():
            if y != "detail":
                data["firmwares"].append(y)

        for z in data["firmwares"]:
            z["name"] = z.pop("version").replace("[", "").replace("]", "")
            z["base"] = re.sub(r"[^0-9.]\s*[a-zA-Z]*\d*", "", z["name"])
            z["build"] = z.pop("buildid")
            z["ipsw"] = z.pop("url")
            z["buildmanifest"] = (
                re.sub(r"[^/]*$", "", z["ipsw"]) + "BuildManifest.plist"
            )

        with firmwares_file.open("w", encoding="utf-8") as c:
            json.dump(data, c, indent=2)

    else:
        wait_to_exit(
            f"{ERROR} Stable ({stable_api.status_code})/Beta ({beta_api.status_code})",
            "API returned a status code other than 200.",
            f'\n\n"{model}" may not be a valid Apple device.'
            "\n\nPlease edit this or try again later.",
            clear=True,
        )


async def __ios_devices() -> None:
    """
    Create a json file containing information for all Apple devices
    """

    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            device_info = await client.get("https://api.ipsw.me/v4/devices")

    except httpx.ConnectError:
        wait_to_exit(
            f"{ERROR} Please check your internet connection and try again.",
            clear=True,
        )

    except (httpx.ConnectTimeout, httpx.ReadTimeout):
        wait_to_exit(
            f"{ERROR} Timed out while receiving data from get requests.",
            "\n\nPlease try again later.",
            clear=True,
        )

    if device_info.status_code == 200:
        devices = device_info.json()

        with devices_file.open("w", encoding="utf-8") as a:
            json.dump({"devices": []}, a, indent=2)

        entry = {}

        for device in devices:
            for x in device["boards"]:
                entry["name"] = (
                    device["name"].replace("+", " Plus").replace("generation", "gen.")
                )
                entry["identifier"] = device["identifier"].lower()
                entry["board"] = x["boardconfig"].lower()

                with devices_file.open(encoding="utf-8") as b:
                    data = json.load(b)
                    data["devices"].append(entry)

                with devices_file.open("w", encoding="utf-8") as c:
                    json.dump(data, c, indent=2)

    else:
        wait_to_exit(
            f"{ERROR} Stable API returned status code {device_info.status_code}",
            "\n\nPlease try again later.",
            clear=True,
        )
