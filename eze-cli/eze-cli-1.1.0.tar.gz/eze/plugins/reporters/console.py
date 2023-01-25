"""Console reporter class implementation"""
import re

from pydash import py_
from pydash import trim

from eze.utils.vo.findings import FindingVO
from eze.core.reporter import ReporterMeta
from eze.utils.vo.findings import ScanVO
from eze.utils.log import log
from eze.utils.scan_result import (
    vulnerabilities_short_summary,
    bom_short_summary,
    name_and_time_summary,
    has_sbom_data,
    has_vulnerability_data,
    convert_into_summaries,
    group_scans,
)
from eze.utils.io.print import pretty_print_table
from eze.core.license import annotated_sbom_table


def condense_md(text: str, indent: str) -> str:
    texts: list[str] = text.split("\n")
    text = "\n".join(list(map(lambda i: indent + trim(i), texts)))
    text = re.sub(f"([\n]{indent})+", f"\n{indent}", text)
    return text


class ConsoleReporter(ReporterMeta):
    """Python report class for echoing all output into the console"""

    REPORTER_NAME: str = "console"
    SHORT_DESCRIPTION: str = "Standard command line reporter"
    INSTALL_HELP: str = """inbuilt"""
    MORE_INFO: str = """inbuilt"""
    LICENSE: str = """inbuilt"""
    VERSION_CHECK: dict = {"FROM_EZE": True}
    EZE_CONFIG: dict = {
        "PRINT_SUMMARY_ONLY": {
            "type": bool,
            "default": False,
            "help_text": """Whether or not to only print the summary (not bom or vulnerabilities)
defaults to false""",
        },
        "PRINT_IGNORED": {
            "type": bool,
            "default": False,
            "environment_variable": "PRINT_IGNORED",
            "help_text": """Whether or not to print out ignored vulnerabilities
defaults to false""",
        },
        "PRINT_TRANSITIVE_PACKAGES": {
            "type": bool,
            "default": False,
            "environment_variable": "PRINT_TRANSITIVE_PACKAGES",
            "help_text": """Print out non top level packages""",
        },
    }

    async def run_report(self, scan_results: list):
        """Method for taking scans and turning then into report output"""
        log("Eze report results:\n")
        self.print_scan_summary_table(scan_results)

        if self.config["PRINT_SUMMARY_ONLY"]:
            return
        (
            scan_results_with_vulnerabilities,
            scan_results_with_secrets,
            scan_results_with_smells,
            scan_results_with_license_risks,
            scan_results_with_sboms,
            scan_results_with_warnings,
            scan_results_with_errors,
        ) = group_scans(scan_results)

        self._print_scan_report_errors(scan_results_with_errors)
        self._print_scan_report_warnings(scan_results_with_warnings)
        self._print_scan_report_findings("Vulnerabilities", "vulnerabilities", scan_results_with_vulnerabilities)
        self._print_scan_report_findings("Secrets", "secrets", scan_results_with_secrets)
        self._print_scan_report_findings("Code Smells", "smells", scan_results_with_smells)
        self._print_scan_report_findings("Licensing Risks", "license_risks", scan_results_with_license_risks)
        self._print_scan_report_sbom(scan_results_with_sboms)

    def print_scan_summary_table(self, scan_results: list):
        """Print scan summary as table"""
        (total_summary, total_totals, summaries, sbom_scans) = convert_into_summaries(scan_results)
        printable_summaries: list = summaries[:]
        printable_summaries.append(total_summary)
        pretty_print_table(printable_summaries, False)
        for sbom_scan in sbom_scans:
            tool_name: str = py_.get(sbom_scan, "run_details.tool_name", "unknown")
            duration_sec = py_.get(sbom_scan, "run_details.duration_sec", 0)
            log(f"BILL OF MATERIALS: {tool_name} (duration: {'{:.1f}s'.format(duration_sec)})")
            log(f"    {bom_short_summary(sbom_scan, '    ', self.config['PRINT_TRANSITIVE_PACKAGES'])}")

    def print_scan_summary_title(self, scan_result: ScanVO, prefix: str = "") -> str:
        """Title of scan summary title"""

        scan_summary = f"""{prefix}TOOL REPORT: {name_and_time_summary(scan_result, "")}\n"""

        # bom count if exists
        if has_sbom_data(scan_result):
            scan_summary += bom_short_summary(scan_result, prefix + "    ", self.config["PRINT_TRANSITIVE_PACKAGES"])

        # if bom only scan, do not print vulnerability count
        if has_vulnerability_data(scan_result):
            scan_summary += vulnerabilities_short_summary(scan_result, prefix + "    ")
        log(scan_summary)

    def _print_scan_report_findings(self, title: str, finding_key: str, scan_results_with_secrets: list[ScanVO]):
        """Method for taking scan vulnerabilities and printing them"""

        if len(scan_results_with_secrets) <= 0:
            return
        log(
            f"""
{title}
================================="""
        )
        count = 0
        for scan_result in scan_results_with_secrets:
            run_details = scan_result.run_details
            tool_name = py_.get(run_details, "tool_name", "unknown")
            indent = "  "

            findings: list[FindingVO] = scan_result.__dict__[finding_key]
            finding: FindingVO = None
            for finding in findings:
                # INFO: By Default ignore "ignored vulnerabilities"
                if finding.is_ignored:
                    if not self.config["PRINT_IGNORED"]:
                        continue
                count += 1
                log(
                    condense_md(
                        finding.to_markdown(indent=indent, escape_md=False, count=count, tool_name=tool_name), indent
                    )
                )
                log("")

    def _print_scan_report_sbom(self, scan_results_with_sboms: list):
        """print scan sbom"""
        if len(scan_results_with_sboms) <= 0:
            return
        log(
            """
Bill of Materials
================================="""
        )
        for scan_result in scan_results_with_sboms:
            run_details = scan_result.run_details
            tool_name = py_.get(run_details, "tool_name", "unknown")
            run_type = f":{run_details['run_type']}" if "run_type" in run_details and run_details["run_type"] else ""
            for project_name in scan_result.sboms:
                cyclonedx_bom = scan_result.sboms[project_name]
                log(
                    f"""
[{tool_name}{run_type}] {project_name} SBOM
================================="""
                )
                sboms = annotated_sbom_table(cyclonedx_bom, self.config["PRINT_TRANSITIVE_PACKAGES"])
                pretty_print_table(sboms)

    def _print_scan_report_warnings(self, scan_results_with_warnings: list):
        """print scan warnings"""
        if len(scan_results_with_warnings) <= 0:
            return

        log(
            """
Warnings
================================="""
        )
        for scan_result in scan_results_with_warnings:
            run_details = scan_result.run_details
            tool_name = py_.get(run_details, "tool_name", "unknown")
            run_type = f":{run_details['run_type']}" if "run_type" in run_details and run_details["run_type"] else ""
            small_indent = "    "
            indent = "        "
            log(
                f"""
{small_indent}[{tool_name}{run_type}] Warnings
{small_indent}================================="""
            )
            for warning in scan_result.warnings:
                log(f"""{indent}{warning}""")

    def _print_scan_report_errors(self, scan_results_with_errors: list):
        """print scan errors"""
        if len(scan_results_with_errors) <= 0:
            return

        log(
            """
Errors
================================="""
        )
        for scan_result in scan_results_with_errors:
            run_details = scan_result.run_details
            tool_name = py_.get(run_details, "tool_name", "unknown")
            run_type = f":{run_details['run_type']}" if "run_type" in run_details and run_details["run_type"] else ""
            small_indent = "    "
            indent = "        "
            log(
                f"""
{small_indent}[{tool_name}{run_type}] Errors
{small_indent}================================="""
            )
            for fatal_error in scan_result.fatal_errors:
                log(f"""{indent}{fatal_error}""")
