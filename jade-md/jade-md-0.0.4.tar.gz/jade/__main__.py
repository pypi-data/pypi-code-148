"""Initialise a new Jade project."""
from __future__ import annotations

import sys

import jade.commands


def main():
    """Run the Jade CLI."""
    commands = {
        "init": jade.commands.initialise,
    }

    try:
        command = sys.argv[1]
    except IndexError:
        print("Welcome to Jade.")
        print("Available commands: " + ", ".join(commands.keys()) + ".")
        exit(0)

    if command in commands:
        commands[command]()

    else:
        print(f"Unknown command: {command}")
        print("Available commands: " + ", ".join(commands.keys()) + ".")
        exit(1)


if __name__ == "__main__":
    main()
