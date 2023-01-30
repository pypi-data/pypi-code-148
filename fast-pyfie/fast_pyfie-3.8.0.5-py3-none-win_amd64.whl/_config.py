import json
import os

from pyfie import _util


def _create_config():
    def detect_platform(config, target_platform):
        config = config.copy()
        # "platform" ブロックを取り除き...
        platform_config = config.pop("platform", {})
        # 指定プラットフォーム部分を追加.
        config.update(platform_config.get(target_platform, {}))
        return config

    CONFIG_FILE_NAME = "pyfie_config.json"

    DEFAULT_CONFIG = {
        "DEBUG": False,

        "auto_init": True,

        "lib_decl_file": "./pyfie_decl.json",

        "patches": {
            "patch_arm_vfp_cprc": True
        },

        "platform": {
            "Windows": {
                "lib_bin_path": [
                    "%WIL3_0_0X64%/fvalgmt.x64.3.0.0.dll",
                    "%WIL3_0_0X64%/fvalg_oss_mt.x64.3.0.0.dll",
                    "%WIL3_0_0X64%/fvalg_camcalib_mt.x64.3.0.0.dll"
                ]
            },

            "Linux": {
                "lib_bin_path": [
                    "./libfvalg.so",
                    "./libfvalg_oss.so",
                    "./libfvalg_camcalib.so"
                ]
            }
        }
    }

    DEFAULT_PLATFORM = "Windows"
    my_platform = _util.get_platform(default=DEFAULT_PLATFORM)

    config = detect_platform(DEFAULT_CONFIG, my_platform)

    # 規定のコンフィグファイルがあればそれで上書き ...
    REGULAR_CONFIG_FILE = _util.resolve_path(CONFIG_FILE_NAME)

    if os.path.exists(REGULAR_CONFIG_FILE):
        with open(REGULAR_CONFIG_FILE, 'r') as jf:
            regular_config = json.load(jf)

        config.update(
            detect_platform(regular_config, my_platform)
        )

    # ユーザーディレクトリにコンフィグファイルがあれば更に上書き ...
    USER_CONFIG_FILE = _util.resolve_path(
        os.path.expanduser("~/" + CONFIG_FILE_NAME))

    if os.path.exists(USER_CONFIG_FILE):
        with open(USER_CONFIG_FILE, 'r') as jf:
            user_config = json.load(jf)

        config.update(
            detect_platform(user_config, my_platform)
        )

    return config


_config = _create_config()

DEBUG = _config["DEBUG"]
auto_init = _config["auto_init"]
lib_decl_file = _config["lib_decl_file"]
patches = _config["patches"]
lib_bin_path = _config["lib_bin_path"]
