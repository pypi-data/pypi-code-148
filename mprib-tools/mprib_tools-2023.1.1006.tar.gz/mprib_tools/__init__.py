"""Top-level package for basic_template_repo."""

__package_name__ = "mprib_tools"
__version__ = "v2023.01.1006"

__author__ = """Skelly FreeMoCap"""
__email__ = "info@freemocap.org"
__repo_owner_github_user_name__ = "freemocap"
__repo_url__ = f"https://github.com/{__repo_owner_github_user_name__}/{__package_name__}/"
__repo_issues_url__ = f"{__repo_url__}issues"

import sys
from pathlib import Path

print(f"Thank you for using {__package_name__}!")
print(f"This is printing from: {__file__}")
print(f"Source code for this package is available at: {__repo_url__}")

from mprib_tools.system.default_paths import get_log_file_path
from mprib_tools.system.logging_configuration import configure_logging


configure_logging(log_file_path=get_log_file_path())