"""Checkmarx Kics Container tool class"""
import re
import shlex
import os

from eze.utils.log import log_debug
from pydash import py_

from eze.utils.vo.findings import SmellVO
from eze.utils.vo.enums import ToolType, SourceType, SmellSeverityEnum
from eze.utils.vo.findings import ScanVO
from eze.core.tool import (
    ToolMeta,
)
from eze.utils.cli.run import run_async_cli_command, CompletedProcess
from eze.utils.io.file import load_json
from eze.utils.io.file_scanner import cache_production_workspace_into_tmp
from eze.utils.error import EzeError
from eze.utils.cli.exe import exe_variable_interpolation_single

# TODO: IMPROVEMENT: speed up docker by mount the "cache_workspace_into_tmp" for scanning


class KicsTool(ToolMeta):
    """SAST Container Kics tool class"""

    TOOL_NAME: str = "container-kics"
    TOOL_URL: str = "https://github.com/Checkmarx/kics"
    TOOL_TYPE: ToolType = ToolType.SAST
    SOURCE_SUPPORT: list = [SourceType.CONTAINER]
    SHORT_DESCRIPTION: str = "Opensource Infrastructure as a Code (IaC) scanner"
    INSTALL_HELP: str = """Only availbale via docker

You can run/install it locally with kics but it's very difficult

you need to extract the executable from the docker image, not recommended
"""
    MORE_INFO: str = """"""
    # https://github.com/Checkmarx/kics/blob/master/LICENSE
    LICENSE: str = """Apache-2.0"""
    EZE_CONFIG: dict = {
        "SOURCE": {
            "type": str,
            "default": ".",
            "help_text": """source folders to scan for IAC files, paths comma-separated""",
        },
        "CONFIG_FILE": {"type": str, "default": None, "help_text": "Optional file input to customise scan command"},
        "EXCLUDE": {
            "type": list,
            "default": [],
            "help_text": """array of regex str of folders/files to exclude from scan,
eze will automatically normalise folder separator "/" to os specific versions, "/" for unix, "\\\\" for windows""",
            "help_example": ["PATH-TO-EXCLUDED-FOLDER/.*", "PATH-TO-EXCLUDED-FILE.js", ".*\\.jpeg"],
        },
        "INCLUDE_FULL_REASON": {
            "type": bool,
            "default": True,
            "help_text": """Optional inclusion of full reason in report
Warning: on production might want to set this to False to prevent found Secrets appearing in reports""",
        },
        "DISABLE_SECRET_SCANNING": {
            "type": bool,
            "default": False,
            "help_text": """Optional disable of kics's secret scanning
enables --disable-secrets flag""",
        },
    }
    VERSION_CHECK: dict = {
        "FROM_EXE": "kics version",
        "FROM_DOCKER": {"DOCKER_COMMAND": {"IMAGE_NAME": "checkmarx/kics:v1.6.6", "BASE_COMMAND": "version"}},
    }
    TOOL_CLI_CONFIG = {
        "CMD_CONFIG": {
            # tool command prefix
            "BASE_COMMAND": shlex.split("kics scan --ci --bom --exclude-gitignore --report-formats 'json' -p"),
            "DOCKER_COMMAND": {
                "FOLDER_NAME": "/path",
                "IMAGE_NAME": "checkmarx/kics:v1.6.6",
                "BASE_COMMAND": "scan --ci --bom --exclude-gitignore --report-formats 'json' -p /path -o '/path/'",
            },
            # eze config fields -> arguments
            "ARGUMENTS": ["SOURCE"],
            # eze config fields -> flags
            "FLAGS": {
                "REPORT_PATH": "--output-path=",
                "REPORT_FILENAME": "--output-name=",
                "CONFIG_FILE": "--config=",
            },
            "SHORT_FLAGS": {"DISABLE_SECRET_SCANNING": "--disable-secrets"},
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
        self.config["REPORT_FILE"] = "__EZE_CONFIG_FOLDER__/raw/_kics-report.json"
        scan_config = self.config.copy()
        # convert REPORT_FILE to separated REPORT_PATH/REPORT_FILENAME arguments to fit the plugin
        scan_config["REPORT_FILENAME"] = os.path.basename(scan_config["REPORT_FILE"])
        scan_config["REPORT_PATH"] = re.sub(scan_config["REPORT_FILENAME"], "", scan_config["REPORT_FILE"]) or "."
        cwd: str = cache_production_workspace_into_tmp()

        completed_process: CompletedProcess = await run_async_cli_command(
            self.TOOL_CLI_CONFIG["CMD_CONFIG"], scan_config, self.TOOL_NAME, cwd=cwd
        )
        report_local_filepath: str = exe_variable_interpolation_single(self.config["REPORT_FILE"])
        report_events = load_json(report_local_filepath)
        report: ScanVO = self.parse_report(report_events)

        if """ERR Failed to run application error="download not supported for scheme""" in completed_process.stderr:
            raise EzeError(
                f"""[{self.TOOL_NAME}] (#97) crashed while running, this is likely because kics docker doesn't work in git-bash
please try again in cmd or powershell
https://pitman.io/posts/tips-for-using-docker-from-git-bash-on-windows/
https://gist.github.com/borekb/cb1536a3685ca6fc0ad9a028e6a959e3"""
            )

        if completed_process.stderr:
            report.warnings.append(completed_process.stderr)

        return report

    def parse_report(self, parsed_json: list) -> ScanVO:
        """convert report json into ScanVO"""
        report_events = py_.get(parsed_json, "queries", [])

        smells_list: list[SmellVO] = []
        if report_events:
            for report_event in report_events:
                if report_event["files"]:
                    files: list[str] = report_event["files"]
                    for file in files:
                        reason: str = report_event["description"]
                        path: str = file["file_name"]
                        # WORKAROUND: clean up docker path, remove '../../path/' prefix
                        path = re.sub("^../../path/", "", path)
                        line: str = file["line"]
                        identifier: str = file["issue_type"]
                        name: str = report_event["query_name"]
                        summary: str = f"{file['actual_value']} ({identifier}) on {report_event['platform']}"
                        recommendation: str = (
                            f"Investigate '{path}' on line {line} for '{reason}'. Expected '{file['expected_value']}'. "
                        )

                        # only include full reason if include_full_reason true
                        if self.config["INCLUDE_FULL_REASON"]:
                            recommendation += f"Full Match: {file['search_key']}."

                        smells_list.append(
                            SmellVO(
                                {
                                    "name": name,
                                    "overview": summary,
                                    "recommendation": recommendation,
                                    "severity": convert_kics_to_smell_severity(report_event["severity"]),
                                    "identifiers": identifier,
                                    "references": report_event["query_url"],
                                    "file_location": {"path": path, "line": line},
                                }
                            )
                        )

        report_sboms = py_.get(parsed_json, "bill_of_materials", [])
        sboms: dict = {}
        if report_sboms:
            for report_sbom in report_sboms:
                platform = report_sbom["platform"]
                if platform not in sboms:
                    sboms[platform] = {"components": []}

                component = {}
                component["name"] = report_sbom["query_name"]
                component["type"] = "resource"
                component["purl"] = report_sbom["platform"] + " - " + report_sbom["query_name"]
                component["version"] = "N/A"
                component["description"] = report_sbom["description"]

                sboms[platform]["components"].append(component)

        report: ScanVO = ScanVO(
            {
                "tool": self.TOOL_NAME,
                "sboms": sboms,
                "smells": smells_list,
            }
        )
        return report

    def _parse_config(self, eze_config: dict) -> dict:
        """take raw config dict and normalise values"""
        parsed_config = super()._parse_config(eze_config)

        # ADDITION PARSING: EXCLUDE FLAGS
        # convert list into comma condensed list
        parsed_config["EXCLUDE"] = ",".join(parsed_config["EXCLUDE"])

        return parsed_config


def convert_kics_to_smell_severity(kics_severity: str) -> str:
    """normalise the severity from kics into the standard eze severity"""
    if kics_severity == "HIGH":
        return SmellSeverityEnum.error.name
    elif kics_severity == "MEDIUM":
        return SmellSeverityEnum.warning.name
    elif kics_severity == "LOW":
        return SmellSeverityEnum.warning.name
    elif kics_severity == "INFO":
        return SmellSeverityEnum.note.name
    elif kics_severity == "TRACE":
        return SmellSeverityEnum.note.name
    log_debug(f"Unknown kics severity: {kics_severity}")
    return SmellSeverityEnum.warning.name
