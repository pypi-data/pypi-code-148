# info@codebasedlearning.dev, a.voss@fh-aachen.de

import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))  # enables relative local imports

#import __version__
#import package

def semver_of(major: int, minor: int, patch: int, stage: str = "") -> str:
    """Example package function. Create semantic version with stage (if given)."""
    return f"{major}.{minor}.{patch}{f'-{stage}' if stage else ''}"


#def package_semver_of(stage: str = "") -> str:
#    """Example package function. Combine package version with stage (if given)."""
#    return f"{__version__}{f'-{stage}' if stage else ''}"


if __name__ == "__main__":
    print(f"case 1: '{semver_of(1, 2, 3)}'")
    print(f"case 2: '{semver_of(2, 3, 4, 'a.1')}'")
    #print(f"case 3: '{package_semver_of()}'")
    #print(f"case 4: '{package_semver_of('rc.3')}'")
