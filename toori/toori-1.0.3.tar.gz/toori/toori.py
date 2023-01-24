import argparse

from toori.main import start

def main():
    parser = argparse.ArgumentParser(description="Toori")
    parser.add_argument("addr", type=str)

    args = parser.parse_args()

    start(args.addr)


if __name__ == "__main__":
    main()
