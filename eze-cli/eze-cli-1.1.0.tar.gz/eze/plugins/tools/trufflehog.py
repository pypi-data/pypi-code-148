"""TruffleHog v3 Python tool class"""
import json
import re
import shlex
import time

from pydash import py_

from eze.utils.vo.findings import SecretVO
from eze.utils.vo.enums import ToolType, SourceType
from eze.utils.vo.findings import ScanVO
from eze.core.tool import (
    ToolMeta,
)
from eze.utils.cli.run import run_async_cli_command, CompletedProcess
from eze.utils.io.file import (
    write_json,
)
from eze.utils.log import log

from eze.utils.io.file_scanner import cache_workspace_into_tmp, cache_production_workspace_into_tmp
from eze.utils.cli.exe import exe_variable_interpolation_single
from eze.utils.git import get_compiled_gitignore_regexes, is_file_gitignored
from typing import List


def extract_leading_number(value: str) -> str:
    """Take output and check for common version patterns"""
    leading_number_regex = re.compile("^[0-9.]+")
    leading_number = re.search(leading_number_regex, value)
    if leading_number:
        return value[leading_number.start() : leading_number.end()]
    return ""


class TruffleHogTool(ToolMeta):
    """TruffleHog v3 Python tool class"""

    MAX_REASON_SIZE: int = 1000

    TOOL_NAME: str = "trufflehog-v3"
    TOOL_URL: str = "https://trufflesecurity.com/"
    TOOL_TYPE: ToolType = ToolType.SECRET
    SOURCE_SUPPORT: list = [SourceType.ALL]
    SHORT_DESCRIPTION: str = "Opensource secret scanner"
    INSTALL_HELP: str = """Only needs docker
https://hub.docker.com/r/trufflesecurity/trufflehog/

Local GO exe can be installed, instructions on github
https://github.com/trufflesecurity/trufflehog
"""
    MORE_INFO: str = """https://github.com/trufflesecurity/trufflehog/

Tips
===============================
- false positives can be individually omitted with post fixing line with "# nosecret" and "// nosecret"
"""

    LICENSE: str = """GPL"""

    EZE_CONFIG: dict = {
        "SOURCE": {
            "type": list,
            "default": ".",
            "required": True,
            "help_text": """TruffleHog v3 list of source folders to scan for secrets""",
        },
        "USE_GIT_IGNORE": {
            "type": bool,
            "default": True,
            "help_text": """.gitignore ignore files specified added to EXCLUDE""",
        },
        "INCLUDE_FULL_REASON": {
            "type": bool,
            "default": False,
            "help_text": """Optional include the full reason in report
Warning: on production might want to set this to False to prevent found Secrets appearing in reports""",
        },
        "EXCLUDE": {
            "type": list,
            "default": [],
            "help_text": """Array of regex str of folders/files to exclude from scan for secrets in .gitignore format
eze will automatically normalise folder separator "/" to os specific versions, "/" for unix, "\\\\" for windows""",
            "help_example": ["PATH-TO-EXCLUDED-FOLDER/**", ".secret"],
        },
        "INCLUDE_TEST": {
            "type": bool,
            "default": False,
            "help_text": "Include test assets in scan",
        },
    }

    VERSION_CHECK: dict = {
        "FROM_EXE": "trufflehog --version",
        "FROM_DOCKER": {
            "DOCKER_COMMAND": {"IMAGE_NAME": "trufflesecurity/trufflehog:3.21.0", "BASE_COMMAND": "--version"}
        },
        # #104 - TRUFFLEHOG outputs version string into stderr
        "COMBINE_STD_OUT_ERR": True,
    }
    TOOL_CLI_CONFIG = {
        "CMD_CONFIG": {
            # tool command prefix.
            "BASE_COMMAND": shlex.split("trufflehog filesystem --directory=__CACHED_WORKSPACE__ --json"),
            "DOCKER_COMMAND": {
                "FOLDERS": {"/tmp/cached_workspace": "__CACHED_WORKSPACE__"},
                "FOLDER_NAME": "/src",
                "WORKING_FOLDER": "/tmp/cached_workspace",
                "IMAGE_NAME": "trufflesecurity/trufflehog:3.21.0",
                "BASE_COMMAND": "filesystem --directory=__CACHED_WORKSPACE__ --json",
            },
            # eze config fields -> flags
        }
    }

    async def run_scan(self) -> ScanVO:
        """
        Run scan using tool

        typical steps
        1) setup config
        2) run tool
        3) parse tool report & normalise into common format

        :raises EzeError
        """
        self.config["REPORT_FILE"] = "__EZE_CONFIG_FOLDER__/raw/_truffleHog-v3-report.json"

        tic = time.perf_counter()

        scan_config = self.config.copy()
        cwd: str = cache_workspace_into_tmp() if self.config["INCLUDE_TEST"] else cache_production_workspace_into_tmp()
        completed_process: CompletedProcess = await run_async_cli_command(
            self.TOOL_CLI_CONFIG["CMD_CONFIG"], scan_config, self.TOOL_NAME, cwd=cwd
        )

        toc = time.perf_counter()
        total_time = toc - tic
        if total_time > 10:
            log(
                f"trufflehog v3 scan took a long time ({total_time:0.2f}s), "
                f"you can often speed up trufflehog significantly by excluding dependency or binary folders like node_modules or sbin"
            )

        report_local_filepath: str = exe_variable_interpolation_single(self.config["REPORT_FILE"])
        parsed_json: list = self._convert_json_lines_into_json_list(completed_process.stdout)
        write_json(report_local_filepath, parsed_json)
        report: ScanVO = self.parse_report(parsed_json)
        if completed_process.stderr:
            report.warnings.append(completed_process.stderr)

        return report

    def _convert_json_lines_into_json_list(self, json_strings_textblock: str) -> list:
        """given string of jsons on newlines, convert into python list of json objects"""
        return json.loads("[" + ",\n".join(json_strings_textblock.strip().split("\n")) + "]")

    def parse_report(self, parsed_json: list) -> ScanVO:
        """convert report json into ScanVO"""
        report_events = parsed_json
        secrets_list: list[SecretVO] = []
        for report_event in report_events:
            if report_event != {}:
                secrets = self._trufflehog_line(report_event)
                secrets_list.append(secrets)
        secrets_list = self._remove_excluded_secrets(secrets_list)
        report: ScanVO = ScanVO(
            {
                "tool": self.TOOL_NAME,
                "secrets": secrets_list,
                "warnings": [],
            }
        )
        return report

    def _trufflehog_line(self, report_event) -> SecretVO:
        """trufflehog format parse support"""
        path: str = py_.get(report_event, "SourceMetadata.Data.Git.file")
        if not path:
            path = py_.get(report_event, "SourceMetadata.Data.Filesystem.file", "unknown")
        # normalise paths to be relative
        if path:
            local_cached_path: str = cache_workspace_into_tmp()
            path = path.replace(str(local_cached_path), "")
            docker_cached_path: str = "/tmp/cached_workspace/"
            path = path.replace(docker_cached_path, "")
        line: str = py_.get(report_event, "SourceMetadata.Data.Git.line") or "1"
        location_str: str = path if line is None else path + ":" + str(line)
        detector_name: str = py_.get(report_event, "DetectorName", "")

        name = f"'{detector_name}' Hardcoded Secret Pattern"
        summary = f"Detected '{detector_name}' Hardcoded Secret Pattern in {path}"
        recommendation = (
            f"Investigate '{location_str}' for '{detector_name}' strings. (add '# nosecret' to line if false positive)"
        )
        # only include full reason if include_full_reason true
        if self.config["INCLUDE_FULL_REASON"]:
            line_containing_secret = report_event["Redacted"]
            if len(line_containing_secret) > self.MAX_REASON_SIZE:
                recommendation += f" Full Match: <on long line ({len(line_containing_secret)} characters)>"
            else:
                recommendation += " Full Match: " + line_containing_secret

        return SecretVO(
            {
                "name": name,
                "overview": summary,
                "recommendation": recommendation,
                "language": "file",
                "identifiers": {},
                "metadata": None,
                "file_location": {"path": path, "line": line},
            }
        )

    def _remove_excluded_secrets(self, vulnerabilities_list: List[SecretVO]) -> List[SecretVO]:
        exclude_config: tuple = None
        if self.config["USE_GIT_IGNORE"]:
            exclude_config = get_compiled_gitignore_regexes(extra_paths=self.config["EXCLUDE"])

        def _is_secret_excluded(secret: SecretVO) -> bool:
            filepath: str = py_.get(secret, "file_location.path")
            if self.config["USE_GIT_IGNORE"] and filepath:
                if is_file_gitignored(filepath, exclude_config):
                    return False
            return True

        return list(filter(_is_secret_excluded, vulnerabilities_list))
