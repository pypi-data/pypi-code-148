"""
Contains the install functions for the various components
"""

# pylint: disable=missing-function-docstring,consider-using-with,disable=invalid-name,subprocess-run-check,line-too-long

import os
import shutil
import sys
from download import download  # type: ignore

from pyflutterinstall.resources import (
    ANDROID_SDK_URL,
    CMDLINE_TOOLS,
    INSTALL_DIR,
    DOWNLOAD_DIR,
    ANDROID_SDK,
)

from pyflutterinstall.util import (
    execute,
    make_title,
)

from pyflutterinstall.setenv import add_env_path, set_env_var


def install_android_sdk() -> int:
    make_title("Installing Android SDK")
    print(
        f"Install Android commandline-tools SDK from {ANDROID_SDK_URL} to {INSTALL_DIR}"
    )
    # sdk\Android\tools\bin\sdkmanager.bat
    path = download(ANDROID_SDK_URL, DOWNLOAD_DIR / os.path.basename(ANDROID_SDK_URL))
    print(f"Unpacking {path} to {INSTALL_DIR}")
    shutil.unpack_archive(path, ANDROID_SDK / "cmdline-tools" / "tools")
    sdkmanager_name = "sdkmanager.bat" if os.name == "nt" else "sdkmanager"
    sdkmanager_path = (
        ANDROID_SDK
        / "cmdline-tools"
        / "tools"
        / "cmdline-tools"
        / "bin"
        / sdkmanager_name
    )
    # add_system_path(sdkmanager_path.parent)
    if not os.path.exists(sdkmanager_path):
        raise FileNotFoundError(f"Could not find {sdkmanager_path}")
    os.chmod(sdkmanager_path, 0o755)
    print("About to install Android SDK tools")
    # install latest
    execute(
        f'{sdkmanager_path} --sdk_root="{ANDROID_SDK}" --install "platform-tools"',
        send_confirmation="y\n",
        ignore_errors=False,
    )
    set_env_var("ANDROID_SDK_ROOT", ANDROID_SDK)
    set_env_var("ANDROID_HOME", ANDROID_SDK)
    # update tools
    print(f"Updating Android SDK with {sdkmanager_path}")
    execute(
        f'{sdkmanager_path} --sdk_root="{ANDROID_SDK}" --update',
        send_confirmation="y\n",
        ignore_errors=False,
    )
    tools_to_install = [f'"{tool}"' for tool in CMDLINE_TOOLS]
    for tool in tools_to_install:
        execute(
            f'{sdkmanager_path} --sdk_root="{ANDROID_SDK}" --install {tool}',
            send_confirmation="y\n",
            ignore_errors=False,
        )
    # send_confirmation = "y\ny\ny\ny\ny\ny\ny\nn\n"
    send_confirmation = "y\ny\ny\ny\ny\ny\ny\ny\ny\ny\ny\ny\ny\nn\n"
    execute(
        f'{sdkmanager_path} --licenses --sdk_root="{ANDROID_SDK}"',
        send_confirmation=send_confirmation,
        ignore_errors=False,
    )
    add_env_path(ANDROID_SDK / "cmdline-tools" / "latest" / "bin")
    return 0


def main() -> int:
    install_android_sdk()
    return 0


if __name__ == "__main__":
    sys.exit(main())
