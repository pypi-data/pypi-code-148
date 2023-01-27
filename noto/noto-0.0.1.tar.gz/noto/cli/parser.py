import argparse
import sys
from noto.cli.output import print_notes

from noto.note.read import read
from noto.note.write import write
from noto.note.update import update
from noto.note.delete import delete

from noto.cli import interactive


def parse(config: object):

    parser = argparse.ArgumentParser(
        prog="noto", description="Probably non-deterministic note box"
    )
    parser.set_defaults(func=lambda *_: parser.print_help())
    subparsers = parser.add_subparsers()

    read_parser = subparsers.add_parser("read", help="Read posted notes")
    read_parser.add_argument(
        "-n",
        "--amount",
        type=int,
        dest="amount",
        default=1,
        help="The amount of notes you want to receive",
    )
    read_parser.add_argument(
        "-m",
        "--min_priority",
        type=int,
        dest="min_priority",
        default=None,
        help="The minimum priority of received notes",
    )
    read_parser.add_argument(
        "-M",
        "--max_priority",
        type=int,
        dest="max_priority",
        default=None,
        help="The maximum priority of received notes",
    )
    read_parser.add_argument(
        "-r",
        "--random",
        dest="random",
        action="store_true",
        help="Whether to sample a random note within the given limits. If not set, the highest priority ones will be returned",
    )
    read_parser.add_argument(
        "-t",
        "--tag",
        dest="tags",
        action="append",
        help="Tag that returned notes must be tagged with",
    )

    read_parser.set_defaults(func=read)

    write_parser = subparsers.add_parser("write", help="Write new note")
    write_parser.add_argument("text", type=str, help="The text you want to submit")
    write_parser.add_argument(
        "-p",
        "--priority",
        type=int,
        dest="priority",
        required=False,
        default=0,
        help="A priority to assign (default = 0)",
    )
    write_parser.add_argument(
        "-t",
        "--tag",
        type=str,
        dest="tags",
        action="append",
        help="A tag to assign to the note (can be used multiple times)",
    )
    write_parser.set_defaults(func=write)

    update_parser = subparsers.add_parser("update", help="Update existing note")
    update_parser.add_argument(
        "id", type=int, help="The id of the note you want to modify"
    )
    update_parser.add_argument("-m", "--text", type=str, help="New note text")
    update_parser.add_argument(
        "-p", "--priority", type=int, help="New priority to assign"
    )
    update_parser.add_argument(
        "-T",
        "--add_tag",
        type=str,
        dest="add_tags",
        action="append",
        help="Tags to remove from note",
    )
    update_parser.add_argument(
        "-t",
        "--remove_tag",
        type=str,
        dest="remove_tags",
        action="append",
        help="Tags to add to note",
    )
    update_parser.set_defaults(func=update)

    delete_parser = subparsers.add_parser("delete", help="Delete existing note")
    delete_parser.add_argument(
        "--id", type=int, required=True, help="The id of the note you want to delete"
    )
    delete_parser.set_defaults(func=delete)

    # use interactive mode on default
    if len(sys.argv) < 2:
        interactive.run(config)
    else:
        args = parser.parse_args()
        func = args.func

        del args.func
        print_notes(func(**vars(args)))
