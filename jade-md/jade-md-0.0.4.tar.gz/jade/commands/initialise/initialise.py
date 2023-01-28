"""Initialise the project directory with the required files."""
from __future__ import annotations

import jade.path as path
from jade.commands.initialise.files import FILES


def initialise():
    """Initialise the project directory with the required files."""
    for raw in FILES:
        file = path.path(raw)
        if path.exists(file):
            print(f"File already exists: {file}\nAborting...")
            exit(1)

        else:
            if not path.exists(file.parent):
                file.parent.mkdir()

            with open(path.path(file), "w") as f:
                f.write(FILES[raw].removeprefix("\n"))

    print("Done!")
    exit(0)
