# (C) 2023 A. Voß setup@codebasedlearning.dev, a.voss@fh-aachen.de

import platform
import sys
import dataclasses
import importlib.metadata


@dataclasses.dataclass
class PackageInfo:
    name: str
    version: str
    summary: str


_raw_cbl = importlib.metadata.metadata('cbl')


def about_package() -> PackageInfo:
    return PackageInfo(_raw_cbl['Name'], _raw_cbl['Version'], _raw_cbl['Summary'])


if __name__ == "__main__":
    print(f"About Package: '{about_package()}'")
