import argparse

from .worker import Worker


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--app",
        "-a",
        required=True,
        help="The Aipo app instance. Formatted as module:object.",
    )
    parser.add_argument(
        "--loop",
        "-l",
        default=None,
        help="The event loop to use. Defaults to asyncio.get_event_loop().",
    )
    args = parser.parse_args()

    worker = Worker(app=args.app, loop_name=args.loop)
    worker.exec_from_cmd()


if __name__ == "__main__":
    main()
