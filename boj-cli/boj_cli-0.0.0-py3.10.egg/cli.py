from boj.utils import input
from boj.utils import output

def login(args):
    print(args)

command_dict = {
    "login": login,
}

def exec(args):
    command_dict[args.command](args)


def run():
    try:
        args = input.parse_args()
        exec(args)
    except Exception as e:
        print(e)
        output.print_usage()
        raise SystemExit(1)
