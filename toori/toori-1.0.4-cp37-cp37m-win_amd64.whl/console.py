import argparse

from toori.main import start


def main():
    parser = argparse.ArgumentParser(description="Toori")
    parser.add_argument("addr", type=str)
    parser.add_argument("-f", "--filter", type=str, required=False)

    parser.add_argument("-nd", "--nodns", action="store_true")

    args = parser.parse_args()

    start(args.addr, args.filter, args.nodns)


if __name__ == "__main__":
    main()
