import sys, argparse

def parse():
    if len(sys.argv) < 2:
        raise Exception("No command selected")

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-f", "--file", dest="file", action="store"
    )

    args = parser.parse_args()

    return sys.argv[1], args
