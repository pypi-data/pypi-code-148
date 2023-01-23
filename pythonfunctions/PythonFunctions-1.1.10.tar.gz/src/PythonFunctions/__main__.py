import argparse
import json
import os

from . import Version


def parserFunc():
    parser = argparse.ArgumentParser(
        prog="PythonFunctions.__main__", description="Some stuff"
    )
    parser.add_argument(
        "-v",
        "--version",
        action="store_const",
        const=True,
        help="Print the module version",
    )
    parser.add_argument(
        "-s",
        "--settings",
        action="store_const",
        const=True,
        help="Generate the settings",
    )
    return parser.parse_args()


def GenerateSettings():
    with open(f"{os.getcwd()}/PyFuncSet.json", "w", encoding="utf-8") as f:
        data = {"Mute": False}
        json.dump(data, f)
    return "Generated setting file"


def GetVersion():
    return Version.ReadLocal()


def main():
    result = parserFunc()
    if result.version:
        print(f"Version: {GetVersion()}")
        return
    if result.settings:
        GenerateSettings()
        return

    print("Please add `--help` on the end to view the arguments")


main()
