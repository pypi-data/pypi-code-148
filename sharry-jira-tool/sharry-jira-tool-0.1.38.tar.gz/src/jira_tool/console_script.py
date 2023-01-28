# -*- coding: utf-8 -*-
"""
This module is used to provide the console program.
"""
import os
import pathlib
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser, Namespace
from datetime import datetime
from importlib.resources import files
from pathlib import Path

from .excel_definition import ExcelDefinition
from .excel_operation import output_to_excel_file, process_excel_file

__all__ = ["sort_excel_file", "generate_template"]


def get_args_for_sort_excel_file() -> Namespace:
    parser = ArgumentParser(
        description="Jira tool: Used to sort stories",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "input_file", metavar="input_file", type=pathlib.Path, help="Source Excel file."
    )
    parser.add_argument(
        "-o",
        "--output_folder",
        metavar="",
        type=pathlib.Path,
        required=False,
        help="Output folder.",
    )
    parser.add_argument(
        "--excel_definition_file",
        metavar="",
        type=pathlib.Path,
        required=False,
        help="Excel definition JSON file.",
    )
    parser.add_argument(
        "--sprint_schedule_file",
        metavar="",
        type=pathlib.Path,
        required=False,
        help="Milestone priority JSON file.",
    )
    parser.add_argument(
        "--over_write",
        metavar="",
        type=bool,
        required=False,
        help="Whether or not to over write existing file.",
    )

    args = parser.parse_args()

    return args


# TODO:
# 1. Create new script to generate excel (empty)
# 2. Create new script to generate json templates.


def sort_excel_file() -> None:
    try:
        args = get_args_for_sort_excel_file()

        # Pre-Process input file
        input_file_absolute_path: pathlib.Path = (
            pathlib.Path.cwd() / args.input_file.as_posix()
        ).resolve()

        if input_file_absolute_path.suffix.lower() != ".xlsx":
            print(f"Please provide an Excel file. File: {input_file_absolute_path}.")
            quit(1)

        if not os.path.exists(input_file_absolute_path):
            print(f"Input file is not exist. File: {input_file_absolute_path}.")
            quit(1)

        input_file_name_without_extension = input_file_absolute_path.stem

        # Pre-Process output file
        output_folder_absolute_path: pathlib.Path = (
            input_file_absolute_path.parent.absolute()
        )

        if args.output_folder is not None:
            temp = pathlib.Path(args.output_folder).resolve()
            if temp.is_dir():
                output_folder_absolute_path = temp.absolute()
            else:
                output_folder_absolute_path = temp.parent.absolute()

        if not output_folder_absolute_path.exists():
            output_folder_absolute_path.mkdir(parents=True, exist_ok=True)

        output_file_absolute_path: pathlib.Path = (
            output_folder_absolute_path
            / f"{input_file_name_without_extension}_sorted.xlsx"
        ).resolve()

        # Fix duplicate output file issue.
        test_output_file_absolute_path = pathlib.Path(
            output_file_absolute_path
        ).resolve()

        copy_count = 1
        while test_output_file_absolute_path.exists():
            test_output_file_absolute_path = (
                output_folder_absolute_path
                / f"{ output_file_absolute_path.stem }_{copy_count}.xlsx"
            )
            copy_count += 1

        output_file_absolute_path = pathlib.Path(
            test_output_file_absolute_path
        ).resolve()

        excel_definition_file_absolute_path = None

        if args.excel_definition_file is not None:
            excel_definition_file_absolute_path = pathlib.Path(
                args.excel_definition_file
            ).resolve()

            if excel_definition_file_absolute_path.suffix.lower() != ".json":
                print(
                    f"Please provide an JSON file for Excel definition. File: {excel_definition_file_absolute_path}."
                )
                quit(1)

        sprint_schedule_file_absolute_path = None

        if args.sprint_schedule_file is not None:
            sprint_schedule_file_absolute_path = pathlib.Path(
                args.sprint_schedule_file
            ).resolve()

            if sprint_schedule_file_absolute_path.suffix.lower() != ".json":
                print(
                    f"Please provide an JSON file for sprint schedule. File: {sprint_schedule_file_absolute_path}."
                )
                quit(1)

        # Over write parameter.
        over_write = True
        if args.over_write is not None:
            over_write = args.over_write

        process_excel_file(
            input_file_absolute_path,
            output_file_absolute_path,
            excel_definition_file_absolute_path,
            sprint_schedule_file_absolute_path,
            over_write,
        )

        quit(0)
    except Exception as e:
        print(e)
        quit(1)


def get_args_for_generate_template() -> Namespace:
    parser = ArgumentParser(
        description="Jira tool: Used to generate templates",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "template_type",
        metavar="template_type",
        type=str,
        help="What kind of file template you want to generate.",
        choices=["excel", "excel-definition", "sprint-schedule", "jira-status-mapping"],
    )

    return parser.parse_args()


HERE = pathlib.Path(__file__).resolve().parent
SRC_ASSETS = HERE / "assets"

from shutil import copyfile


def generate_template():
    try:
        args = get_args_for_generate_template()

        template_type: str = str(args.template_type).lower()

        result: Path | None = None
        if template_type == "excel":
            result = _generate_excel_template(
                _generate_timestamp_filename("excel-template", ".xlsx")
            )
        elif template_type == "excel-definition":
            result = copyfile(
                SRC_ASSETS / "excel_definition.json",
                _generate_timestamp_filename("excel-definition-template", ".json"),
            )
        elif template_type == "sprint-schedule":
            result = copyfile(
                SRC_ASSETS / "sprint_schedule.json",
                _generate_timestamp_filename("sprint_schedule-template", ".json"),
            )
        else:
            result = copyfile(
                SRC_ASSETS / "jira_status_mapping.json",
                _generate_timestamp_filename("jira_status_mapping-template", ".json"),
            )

        if result is not None and result.is_file():
            print(f"Generate success! Template type: {template_type}.")
            quit(0)
        else:
            print(f"Generate failed! Template type: {template_type}.")
            quit(1)
    except Exception as e:
        print(e)
        quit(1)


def _generate_timestamp_filename(prefix: str, extension: str) -> "Path":
    return (
        Path.cwd()
        / f'{prefix}-{datetime.now().strftime("%y-%m-%d-%H-%M-%S")}{extension}'
    ).resolve()


def _generate_excel_template(output_file: "Path") -> "Path | None":
    try:
        excel_definition = ExcelDefinition().load(
            files("jira_tool.assets").joinpath("excel_definition.json").read_text()
        )
        output_to_excel_file(output_file, [], excel_definition)
        return output_file
    except Exception as e:
        print(e)
        return None
