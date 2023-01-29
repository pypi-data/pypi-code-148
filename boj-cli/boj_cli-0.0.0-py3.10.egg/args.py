import argparse
import os


def init_parser():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest="command")  # this line changed

    # Login command parser
    login_args_parser = subparsers.add_parser(
        "login",
        help="logs in to BOJ",
    )
    login_args_parser.add_argument(
        "-u",
        "--user",
        help="username",
    )
    login_args_parser.add_argument(
        "-t",
        "--token",
        help="login token from the cookies",
    )

    # Submit command parser
    submit_args_parser = subparsers.add_parser("submit", help="submits your code")
    submit_args_parser.add_argument(
        "file",
        metavar="FILE",
        type=validate_file,
        help="the file path of the sorce code",
    )
    submit_args_parser.add_argument(
        "-l",
        "--lang",
        help="the language to submit your source code as",
    )

    problem_args_parser = subparsers.add_parser(
        "problem", help="shows the problem in terminal"
    )
    problem_args_parser.add_argument(
        "id",
        metavar="PROBLEM_ID",
        type=int,
        help="the problem id",
    )

    run_args_parser = subparsers.add_parser("run", help="run testcases")
    run_args_parser.add_argument(
        "file",
        metavar="FILE",
        type=validate_file,
        help="the file path of the source code",
    )
    run_args_parser.add_argument(
        "-v",
        "--verbose",
        action='store_true',
        help="show detailed output",
    )

    init_args_parser = subparsers.add_parser("init", help="init testcases")
    init_args_parser.add_argument(
        "problem_id",
        metavar="PROBLEM_ID",
        type=int,
        help="problem id",
    )

    return parser


def validate_file(file):
    if os.path.isfile(file):
        return file
    else:
        raise argparse.ArgumentTypeError(f"'{file}' No such file.")
