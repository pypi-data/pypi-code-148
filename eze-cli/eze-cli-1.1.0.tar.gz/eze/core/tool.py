"""Eze's Scan Tools module"""
from __future__ import annotations

import asyncio
import os
import time
import math
from abc import abstractmethod
from typing import Callable

from copy import deepcopy

from eze.core.reporter import ReporterManager
from eze.core.config import EzeConfig, PluginMeta
from eze.utils.vo.findings import VulnerabilityVO
from eze.utils.vo.enums import VulnerabilitySeverityEnum, ToolType
from eze.utils.git import get_active_branch_name, get_active_branch_uri
from eze.utils.cli.run import EzeExecutableNotFoundError
from eze.utils.io.file import normalise_file_paths, create_folder, delete_file
from eze.utils.io.print import pretty_print_table
from eze.utils.config import (
    get_config_key,
    get_config_keys,
    create_config_help,
    extract_embedded_run_type,
)
from eze.utils.error import EzeError, EzeConfigError
from eze.utils.log import log, log_debug, log_error, status_message, clear_status_message
from eze.utils.io.file_scanner import IGNORED_FOLDERS
from eze.utils.cli.exe import exe_variable_interpolation_single
from eze.utils.vo.findings import ScanVO


class ToolMeta(PluginMeta):
    """Base class for all scanner implementations"""

    TOOL_NAME: str = "AbstractTool"
    TOOL_URL: str = ""
    TOOL_TYPE: ToolType = ToolType.MISC
    SOURCE_SUPPORT: list = []
    COMMON_EZE_CONFIG: dict = {
        "ADDITIONAL_ARGUMENTS": {
            "type": str,
            "default": "",
            "help_text": """common field that can be used to postfix arbitrary arguments onto any plugin cli tooling""",
        },
        "IGNORE_BELOW_SEVERITY": {
            "type": str,
            "help_text": """vulnerabilities severities to ignore, by CVE severity level
aka if set to medium, would ignore medium/low/none/na
available levels: critical, high, medium, low, none, na""",
        },
        "IGNORED_VULNERABILITIES": {
            "type": list,
            "help_text": """vulnerabilities to ignore, by CVE code or by name
feature only for use when vulnerability mitigated or on track to be fixed""",
        },
        "IGNORED_FILES": {
            "type": list,
            "help_text": """vulnerabilities in files or prefix folders to ignore
feature only for use when vulnerability mitigated or on track to be fixed""",
        },
        "DEFAULT_SEVERITY": {
            "type": str,
            "help_text": """Severity to set vulnerabilities, when tool doesn't provide a severity, defaults to na
available levels: critical, high, medium, low, none, na""",
        },
        "EXCLUDE": {
            "type": list,
            "default": [],
            "help_text": """files or prefix folders to exclude in the scanning process""",
        },
    }

    DEFAULT_IGNORED_LOCATIONS: list = IGNORED_FOLDERS

    def _parse_config(self, eze_config: dict) -> dict:
        """take raw config dict and normalise values based off "EZE_CONFIG" config,
        can be overridden for advanced behaviours"""
        parsed_config = super()._parse_config(eze_config)
        parsed_config = get_config_keys(eze_config, deepcopy(self.COMMON_EZE_CONFIG), parsed_config)
        return parsed_config

    @classmethod
    def tool_type(cls) -> str:
        """Returns tool type"""
        return cls.TOOL_TYPE

    @classmethod
    def source_support(cls) -> str:
        """Returns the sources supported by tool"""
        return cls.SOURCE_SUPPORT

    @classmethod
    def config_help(cls) -> str:
        """Returns self help instructions how to configure the tool"""
        return create_config_help(cls.TOOL_NAME, cls.EZE_CONFIG.copy(), cls.COMMON_EZE_CONFIG.copy())

    @abstractmethod
    async def run_scan(self) -> ScanVO:
        """
        Run scan using tool

        typical steps
        1) setup config
        2) run tool
        3) parse tool report & normalise into common format

        :raises EzeError
        """

    def prepare_folder(self) -> None:
        """Create a reports folder for the plugin report if it does not exist"""
        report_local_filepath = exe_variable_interpolation_single(self.config.get("REPORT_FILE", None))
        if report_local_filepath:
            create_folder(report_local_filepath, False)
            delete_file(report_local_filepath)


class ToolManager:
    """Singleton Class for accessing all available Tools"""

    _instance = None

    @staticmethod
    def get_instance() -> ToolManager:
        """Get previously set tools config"""
        if ToolManager._instance is None:
            log_error("ToolManager unable to get config before it is setup")
        return ToolManager._instance

    @staticmethod
    def set_instance(plugins: dict) -> ToolManager:
        """Set the global tools config"""
        ToolManager._instance = ToolManager(plugins)
        return ToolManager._instance

    @staticmethod
    def reset_instance():
        """Reset the global tools config"""
        ToolManager._instance = None

    def __init__(self, plugins: dict = None):
        """takes list of config files, and merges them together, dicts can also be passed instead of pathlib.Path"""
        if plugins is None:
            plugins = {}
        #
        self.tools = {}
        for plugin_name in plugins:
            plugin = plugins[plugin_name]
            if not hasattr(plugin, "get_tools") or not isinstance(plugin.get_tools, Callable):
                log_debug(f"'get_tools' function missing from plugin '{plugin_name}'")
                continue
            plugin_tools = plugin.get_tools()
            self._add_tools(plugin_tools)

    async def run_tool(self, tool_name: str, scan_type: str = None, run_type: str = None) -> ScanVO:
        """
        Runs a instance of a tool, populated with it's configuration

        :raises EzeConfigError
        """
        tic = time.perf_counter()
        [tool_name, run_type] = extract_embedded_run_type(tool_name, run_type)
        tool_instance = self.get_tool(tool_name, scan_type, run_type)
        tool_instance.prepare_folder()
        try:
            process = {"scan_result": None}

            async def run_counter(what: str, delay: int = 1):
                status_message(what)
                while True:
                    toc = time.perf_counter()
                    status_message(what + " (" + str(math.ceil(toc - tic)) + " secs)")
                    await asyncio.sleep(delay)

            run_counter_task = asyncio.create_task(run_counter(f"running tool '{tool_name}'"))

            async def run_process():
                try:
                    process["scan_result"] = await tool_instance.run_scan()
                finally:
                    run_counter_task.cancel()

            task_run_process = asyncio.create_task(run_process())
            try:
                await asyncio.gather(run_counter_task, task_run_process)
            except RuntimeError:
                pass
            except asyncio.exceptions.CancelledError:
                pass
            scan_result: ScanVO = process["scan_result"]
        except EzeExecutableNotFoundError as error:
            # Special Case:
            # If executable not installed print "install help"
            # to help user fix error
            tool_class = self.tools[tool_name]
            is_installed = tool_class.check_installed()
            if not is_installed:
                log_error(
                    f"""[{tool_name}] {error}

Looks like {tool_name} is not installed

{tool_name} Install Help:
============================
{tool_class.install_help()}
"""
                )
            scan_result: ScanVO = ScanVO(
                {
                    "tool": tool_instance.TOOL_NAME,
                    "fatal_errors": [f"{error}"],
                }
            )
        except EzeError as error:
            scan_result: ScanVO = ScanVO(
                {
                    "tool": tool_instance.TOOL_NAME,
                    "fatal_errors": [f"{error}"],
                }
            )

        toc = time.perf_counter()
        # annotation raw scan result
        if not scan_result:
            scan_result = ScanVO(
                {
                    "tool": tool_instance.TOOL_NAME,
                    "fatal_errors": ["Not scan result received"],
                }
            )
        if not scan_result.tool:
            scan_result.tool = tool_instance.TOOL_NAME

        git_dir = os.getcwd()
        git_repo = get_active_branch_uri(git_dir)
        git_branch = get_active_branch_name(git_dir)
        scan_result.run_details = {
            "tool_name": tool_name,
            "tool_url": tool_instance.TOOL_URL,
            "tool_type": tool_instance.TOOL_TYPE.value,
            "scan_type": scan_type,
            "run_type": run_type,
            "duration_sec": toc - tic,
            "date": tic,
            "git_repo": git_repo,
            "git_branch": git_branch,
        }
        # get tool config for ignore list
        tool_config: dict = self._get_tool_config(tool_name, scan_type, run_type)
        # create counts of findings
        scan_result.finalise(tool_config)
        return scan_result

    def get_tool_class(self, tool_name: str) -> ToolMeta:
        """
        Gets a instance of a tool class

        :raises EzeConfigError
        """
        if tool_name not in self.tools:
            raise EzeConfigError(f"tool id: {tool_name} does not exist")
        tool_class = self.tools[tool_name]
        return tool_class

    def get_tool(self, tool_name: str, scan_type: str = None, run_type: str = None) -> ToolMeta:
        """
        Gets a instance of a tool, populated with it's configuration

        :raises EzeConfigError
        """

        [tool_name, run_type] = extract_embedded_run_type(tool_name, run_type)

        tool_config: dict = self._get_tool_config(tool_name, scan_type, run_type)
        tool_class = self.get_tool_class(tool_name)
        tool_instance = tool_class(tool_config)
        return tool_instance

    def print_tools_list(
        self,
        tool_type: str = None,
        source_type: str = None,
        include_source_type: bool = None,
        include_version: bool = None,
    ):
        """list available tools"""
        if include_version:
            log(
                """Please note that obtaining the version information for the tools may take several minutes, as all required Docker images must be obtained for version detection to occur."""
            )
        log(
            """Available Tools are:
======================="""
        )
        tools = []
        tools_counter = 0
        tools_length = len(self.tools)
        for current_tool_name in self.tools:
            tools_counter += 1
            current_tool_class = self.get_tool_class(current_tool_name)
            current_tool_type = current_tool_class.tool_type().name
            current_source_support = current_tool_class.source_support()
            current_source_support_strs = list(map(lambda source: source.name, current_source_support))
            current_source_support_str = ",".join(current_source_support_strs)
            current_tool_license = current_tool_class.license()
            current_tool_description = current_tool_class.short_description()
            if tool_type and tool_type != current_tool_type:
                continue
            if (
                source_type
                and source_type not in current_source_support_strs
                and "ALL" not in current_source_support_strs
            ):
                continue
            # WARNING: order of dict keys important, determines table column order
            tool_entry: dict = {"Type": current_tool_type, "Name": current_tool_name}
            if include_version:
                status_message(f"({tools_counter}/{tools_length}) obtaining '{current_tool_name}' tool version")
                current_tool_version = current_tool_class.check_installed() or "Not Installed"
                tool_entry["Version"] = current_tool_version
            tool_entry["License"] = current_tool_license
            if include_source_type:
                tool_entry["Sources"] = current_source_support_str
            tool_entry["Description"] = current_tool_description
            tools.append(tool_entry)

        clear_status_message()
        pretty_print_table(tools)

    def print_tools_help(self, tool_type: str = None, source_type: str = None, include_source_type: bool = None):
        """print help for all tools"""
        log(
            """Available Tools Help:
======================="""
        )
        for current_tool_name in self.tools:
            current_tool_class = self.get_tool_class(current_tool_name)
            current_tool_type = current_tool_class.tool_type().name
            current_source_support = current_tool_class.source_support()
            current_source_support_strs = list(map(lambda source: source.name, current_source_support))
            if tool_type and tool_type != current_tool_type:
                continue
            if (
                source_type
                and source_type not in current_source_support_strs
                and "ALL" not in current_source_support_strs
            ):
                continue
            self.print_tool_help(current_tool_name)

    def print_tool_help(self, tool_id: str):
        """print out tool help"""
        tool_class: ToolMeta = self.get_tool_class(tool_id)
        tool_description = tool_class.short_description()
        log(
            f"""
=================================
Tool '{tool_id}' Help
{tool_description}
================================="""
        )
        tool_license = tool_class.license()
        log(f"License: {tool_license}")
        tool_version = tool_class.check_installed()
        if tool_version:
            log(f"Version: {tool_version} Installed\n")
        else:
            log(
                """Tool Install Instructions:
---------------------------------"""
            )
            log(tool_class.install_help())
            log("")
        log(
            """Tool Configuration Instructions:
---------------------------------"""
        )
        log(tool_class.config_help())

        log(
            """Tool More Info:
---------------------------------"""
        )
        log(tool_class.more_info())

    def _add_tools(self, tools: dict):
        """adds new tools to tools registry"""
        for tool_name in tools:
            tool = tools[tool_name]
            if issubclass(tool, ToolMeta):
                if not hasattr(self.tools, tool_name):
                    log_debug(f"-- installing tool '{tool_name}'")
                    self.tools[tool_name] = tool
                else:
                    log_debug(f"-- skipping '{tool_name}' already defined")
                    continue
            # TODO: else check public functions
            else:
                log_error(f"-- skipping invalid tool '{tool_name}'")
                continue

    def _get_tool_config(self, tool_name: str, scan_type: str = None, run_type: str = None) -> dict:
        """
        Get Tool Config, handle default config parameters

        :raises EzeConfigError
        """
        eze_config = EzeConfig.get_instance()
        tool_config = eze_config.get_plugin_config(tool_name, scan_type, run_type)

        # Warnings for corrupted config
        if tool_name not in self.tools:
            error_message = f"[{tool_name}] The ./ezerc config references unknown tool plugin '{tool_name}', run 'eze tools list' to see available tools"
            raise EzeConfigError(error_message)

        tool_class = self.get_tool_class(tool_name)
        default_severity = VulnerabilitySeverityEnum.na.name
        if hasattr(tool_class, "DEFAULT_SEVERITY"):
            default_severity = tool_class.DEFAULT_SEVERITY

        tool_config["DEFAULT_SEVERITY"] = get_config_key(tool_config, "DEFAULT_SEVERITY", str, default_severity)
        if not hasattr(VulnerabilitySeverityEnum, tool_config["DEFAULT_SEVERITY"]):
            log_error(
                f"{tool_name} configured with invalid DEFAULT_SEVERITY='{tool_config['DEFAULT_SEVERITY']}', defaulting to na"
            )
            tool_config["DEFAULT_SEVERITY"] = VulnerabilitySeverityEnum.na.name
        tool_config["IGNORED_VULNERABILITIES"] = get_config_key(tool_config, "IGNORED_VULNERABILITIES", list, [])

        raw_ignored_files = get_config_key(tool_config, "IGNORED_FILES", list, [])
        tool_config["IGNORED_FILES"] = normalise_file_paths(raw_ignored_files)

        raw_excluded_files = get_config_key(tool_config, "EXCLUDE", list, [])
        raw_excluded_files.extend(self.find_tool_output_files(scan_type, run_type))
        raw_excluded_files.extend(self.find_reporter_files(scan_type, run_type))
        tool_config["EXCLUDE"] = normalise_file_paths(raw_excluded_files)

        ignore_below_severity_name = get_config_key(
            tool_config, "IGNORE_BELOW_SEVERITY", str, VulnerabilitySeverityEnum.na.name
        )
        if not hasattr(VulnerabilitySeverityEnum, ignore_below_severity_name):
            log_error(f"invalid IGNORE_BELOW_SEVERITY value '{ignore_below_severity_name}' given, defaulting to na")
            ignore_below_severity_name = VulnerabilitySeverityEnum.na.name
        tool_config["IGNORE_BELOW_SEVERITY_INT"] = VulnerabilitySeverityEnum[ignore_below_severity_name].value
        return tool_config

    def find_tool_output_files(self, scan_type: str, run_type: str):
        """Get Tool Config, handle default config parameters"""
        eze_config = EzeConfig.get_instance()
        report_files = []
        for tool_name in self.tools:
            tool_config = eze_config.get_plugin_config(tool_name, scan_type, run_type)
            report_local_filepath = exe_variable_interpolation_single(tool_config.get("REPORT_FILE", None))
            report_files.append(report_local_filepath)
        return [rf for rf in report_files if rf]

    def find_reporter_files(self, scan_type: str, run_type: str):
        """Get Tool Config, handle default config parameters"""
        reporters = []
        try:
            reporters = EzeConfig.get_instance().get_scan_config(scan_type).get("reporters", [])
        except Exception:
            pass
        reporter_manager = ReporterManager.get_instance()
        report_files = []
        for reporter_name in reporters:
            reporter_config = reporter_manager.get_reporter(reporter_name, scan_type, run_type).config
            report_local_filepath = exe_variable_interpolation_single(reporter_config.get("REPORT_FILE", None))
            report_files.append(report_local_filepath)
        return [rf for rf in report_files if rf]
