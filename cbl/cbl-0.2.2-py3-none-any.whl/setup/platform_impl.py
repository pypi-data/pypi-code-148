# (C) 2023 A. Voß setup@codebasedlearning.dev, a.voss@fh-aachen.de

import platform
import dataclasses


@dataclasses.dataclass
class PlatformInfo:
    platform: str
    machine: str
    processor: str


def about_platform() -> PlatformInfo:
    return PlatformInfo(platform.platform(), platform.machine(), platform.processor())


if __name__ == "__main__":
    print(f"About Platform: '{about_platform()}'")

