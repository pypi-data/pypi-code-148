############################################################################################################
#                                     Helper Functions                                                     #
from os import environ, path, getcwd
from subprocess import run, CalledProcessError
from contextlib import suppress
from re import search

def check_debugger() -> bool:
    with suppress(Exception):
        return any([search("vsc", environ.get("TERM_PROGRAM")), search("pycharm", environ.get("TERM_PROGRAM"))])

def orjson_exists() -> bool:
    env_path = path.join(getcwd(), ".env")

    try:
        from orjson import dumps
        return True
    except ImportError:
        pass

    if path.exists(env_path):
        with open(env_path) as env_file:
            if 'ORJSON_NOT_AVAILABLE' in env_file.read():
                return False

    if environ.get("OS") != "Windows_NT":
        return False

    try:
        run(["pip", "install", "orjson"], check=True)
        from orjson import dumps
        run("cls" if environ.get("OS") == "Windows_NT" else "clear", shell=True)
        return True
    except CalledProcessError:
        with open(env_path, "w") as env_file:
            env_file.write("ORJSON_NOT_AVAILABLE=1")
        return False

############################################################################################################
