"""NpmAudit tool class"""
import shlex
from pathlib import Path

from eze.utils.cli.exe import exe_variable_interpolation_single
from pydash import py_

from eze.utils.vo.findings import SmellVO
from eze.utils.vo.enums import VulnerabilitySeverityEnum, ToolType, SourceType, SmellSeverityEnum
from eze.core.tool import (
    ToolMeta,
)
from eze.utils.vo.findings import ScanVO
from eze.utils.log import log_debug
from eze.utils.cli.run import run_async_cli_command, CompletedProcess
from eze.utils.io.file import write_text, parse_json
from eze.utils.semvar import get_severity, get_recommendation
from eze.utils.language.node import install_npm_in_path, get_npm_projects, NPM_DOCKER_IMAGE


class NpmOutdatedTool(ToolMeta):
    """NpmOutdated Node tool class"""

    TOOL_NAME: str = "node-npmoutdated"
    TOOL_URL: str = "https://docs.npmjs.com/cli/v6/commands/npm-outdated"
    TOOL_TYPE: ToolType = ToolType.SAST
    SOURCE_SUPPORT: list = [SourceType.NODE]
    SHORT_DESCRIPTION: str = "Opensource tool for scanning Node.js projects and identifying outdated dependencies"
    INSTALL_HELP: str = """In most cases all that is required to install node and npm (version 6+)
npm --version"""
    MORE_INFO: str = """https://docs.npmjs.com/cli/v6/commands/npm-outdated
https://docs.npmjs.com/downloading-and-installing-node-js-and-npm
"""
    EZE_CONFIG: dict = {
        "NEWER_MAJOR_SEMVERSION_SEVERITY": {
            "type": str,
            "default": SmellSeverityEnum.warning.name,
            "help_text": """severity of vulnerabilty to raise, if new major version available of a package""",
        },
        "NEWER_MINOR_SEMVERSION_SEVERITY": {
            "type": str,
            "default": SmellSeverityEnum.warning.name,
            "help_text": """severity of vulnerabilty to raise, if new minor version available of a package""",
        },
        "NEWER_PATCH_SEMVERSION_SEVERITY": {
            "type": str,
            "default": SmellSeverityEnum.note.name,
            "help_text": """severity of vulnerabilty to raise, if new patch version available of a package""",
        },
    }
    # https://github.com/npm/cli/blob/latest/LICENSE
    LICENSE: str = """NPM"""
    # TODO: improve with FROM_NPM ?
    VERSION_CHECK: dict = {
        "FROM_EXE": "npm --version",
        "FROM_DOCKER": {"DOCKER_COMMAND": {"IMAGE_NAME": NPM_DOCKER_IMAGE, "BASE_COMMAND": "npm --version"}},
        "CONDITION": ">=6",
    }
    DEFAULT_SEVERITY = VulnerabilitySeverityEnum.high.name
    TOOL_CLI_CONFIG = {
        "CMD_CONFIG": {
            "BASE_COMMAND": shlex.split("npm outdated --json"),
            "DOCKER_COMMAND": {
                "FOLDER_NAME": "/src",
                "WORKING_FOLDER": "/src",
                "IMAGE_NAME": NPM_DOCKER_IMAGE,
                "BASE_COMMAND": "npm outdated --json",
            },
            # eze config fields -> flags
            "FLAGS": {},
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
        self.config["REPORT_FILE"] = "__EZE_CONFIG_FOLDER__/raw/_npmoutdated-report.json"
        npm_package_jsons = get_npm_projects()
        smells_list: list = []
        warnings_list: list = []
        for npm_package in npm_package_jsons:
            log_debug(f"run 'npm outdated' on {npm_package}")
            npm_project = Path(npm_package).parent
            npm_project_fullpath = Path.joinpath(Path.cwd(), npm_project)
            await install_npm_in_path(npm_project)
            self.config["__THROW_ERROR_ON_STDERR"] = True
            completed_process: CompletedProcess = await run_async_cli_command(
                self.TOOL_CLI_CONFIG["CMD_CONFIG"], self.config, self.TOOL_NAME, cwd=npm_project_fullpath
            )

            report_text = completed_process.stdout
            report_local_filepath: str = exe_variable_interpolation_single(self.config["REPORT_FILE"])
            write_text(report_local_filepath, report_text)
            parsed_json = parse_json(report_text)
            [smells, warnings] = self.parse_report(parsed_json, npm_package)
            smells_list.extend(smells)
            warnings_list.extend(warnings)
        report: ScanVO = ScanVO(
            {
                "tool": self.TOOL_NAME,
                "smells": smells_list,
                "warnings": warnings_list,
            }
        )
        return report

    def parse_report(self, parsed_json: list, npm_package: str = None) -> tuple:
        """convert report json into ScanVO"""

        warnings = []
        smells_list: list[SmellVO] = []
        for outdated_package in parsed_json:
            outdated_module: str = parsed_json[outdated_package]
            current_installed_version: str = py_.get(outdated_module, "current")
            if not current_installed_version:
                warnings.append(
                    f"{outdated_package}: package not locally installed, detecting outdated status from wanted version, fix with `npm install`"
                )
            installed_version: str = current_installed_version or outdated_module["wanted"]
            latest_version: str = outdated_module["latest"]
            smells_list.append(
                SmellVO(
                    {
                        "name": outdated_package,
                        "overview": f"{outdated_package} (current version={installed_version}, newest={latest_version})",
                        "recommendation": get_recommendation(outdated_package, installed_version, latest_version),
                        "severity": get_severity(installed_version, latest_version, self.config),
                        "file_location": {"path": npm_package, "line": 1},
                    }
                )
            )

        return [smells_list, warnings]
