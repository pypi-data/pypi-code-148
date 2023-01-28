# (C) 2023 A. Voß setup@codebasedlearning.dev, a.voss@fh-aachen.de

import platform
import sys
import dataclasses


@dataclasses.dataclass
class PythonInfo:
    executable: str
    version: str
    implementation: str


def about_python() -> PythonInfo:
    return PythonInfo(sys.executable, platform.python_version(), platform.python_implementation())


if __name__ == "__main__":
    print(f"About Python: '{about_python()}'")
