# Module update checker, based off the github file
import json
import os


def LocalSettings():
    """Check if muted

    Returns:
        bool: Muted or not
    """
    path = os.getcwd() + "/PyFuncSet.json"
    if os.path.exists(path):
        data = {}
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return not data.get("Mute")

    return True


muted = LocalSettings()
if muted:
    canReadGlobal = True
    try:
        import requests
    except ModuleNotFoundError:
        print(
            "Requests is not installed. Can not check for a new PythonFunction update!"
        )
        canReadGlobal = False


def ReadLocal():
    """Get the module version

    Returns:
        str: Module version
    """
    return "1.2.6"


def ReadGlobal():
    """Get the version on the server"""
    if canReadGlobal:
        url = "https://raw.githubusercontent.com/FunAndHelpfulDragon/python-Functions/main/Version.txt"
        r = requests.get(url, timeout=60)
        return r.text


def Compare():
    current = ReadLocal()
    server = ReadGlobal()

    if server > current:
        print("*" * os.get_terminal_size().columns)
        print(
            f"""Notice: A newer version of PythonFunctions is alvalible.
Current Version: {current}. New version: {server}
Make the file PyFuncSet.json to mute this"""
        )
        print("*" * os.get_terminal_size().columns)


if __name__ == "__main__":
    if canReadGlobal and muted:
        ReadGlobal()
