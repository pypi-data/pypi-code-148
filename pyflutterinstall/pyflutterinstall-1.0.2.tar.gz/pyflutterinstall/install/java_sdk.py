"""
Contains the install functions for the various components
"""

# pylint: disable=missing-function-docstring,consider-using-with,disable=invalid-name,subprocess-run-check,line-too-long,R0801

import os
import sys
from pathlib import Path
import shutil
import subprocess
from download import download  # type: ignore

from pyflutterinstall.resources import (
    JAVA_SDK_URL,
    INSTALL_DIR,
    DOWNLOAD_DIR,
    JAVA_DIR,
)

from pyflutterinstall.util import make_title

from pyflutterinstall.setenv import add_env_path, set_env_var


def install_java_sdk() -> int:
    make_title("Installing Java SDK")
    print(f"Install Java SDK from {JAVA_SDK_URL} to {INSTALL_DIR}")
    java_sdk_zip_file = Path(
        download(JAVA_SDK_URL, DOWNLOAD_DIR / os.path.basename(JAVA_SDK_URL))
    )
    if os.path.exists(JAVA_DIR):
        print(f"Removing existing Java SDK at {JAVA_DIR}")
        shutil.rmtree(JAVA_DIR)
    print(f"Unpacking {java_sdk_zip_file} to {JAVA_DIR}")
    shutil.unpack_archive(java_sdk_zip_file, JAVA_DIR)
    base_java_dir = JAVA_DIR / os.listdir(JAVA_DIR)[0]
    print(base_java_dir)
    if sys.platform == "darwin":
        java_bin_dir = base_java_dir / "Contents" / "Home" / "bin"
    else:
        java_bin_dir = base_java_dir / "bin"
    # check that java is in the path
    print(java_bin_dir)
    java_exe = "java.exe" if os.name == "nt" else "java"
    assert java_exe in os.listdir(java_bin_dir), "java not found in java bin dir"
    add_env_path(java_bin_dir)
    if sys.platform == "darwin":
        set_env_var("JAVA_HOME", str(base_java_dir / "Contents" / "Home"))
    else:
        set_env_var("JAVA_HOME", str(base_java_dir))
    found_java_path = shutil.which("java")
    assert found_java_path is not None, "No java path found"
    assert (
        str(java_bin_dir) in found_java_path
    ), f"java installed not in expected path, instead it's {found_java_path}"
    java_version = subprocess.check_output(
        "java -version", shell=True, universal_newlines=True, stderr=subprocess.STDOUT
    )
    print(f"Java SDK installed: {java_version}\n")
    return 0


def main():
    install_java_sdk()


if __name__ == "__main__":
    main()
