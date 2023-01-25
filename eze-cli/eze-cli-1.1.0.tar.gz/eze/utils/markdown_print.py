"""Print as markdown helpers
"""

from eze.utils.vo.findings import FindingVO
from eze.utils.vo.findings import ScanVO
from eze.utils.io.print import generate_markdown_table, generate_markdown_list, generate_markdown_header
from eze.utils.scan_result import (
    bom_short_summary,
    name_and_time_summary,
    vulnerabilities_short_summary,
    has_vulnerability_data,
    has_sbom_data,
    convert_into_summaries,
    group_scans,
)
from pydash import py_
from eze.core.license import annotated_sbom_table


def scan_results_as_markdown(scan_results: list, print_transitive: bool = False) -> str:
    """Method for taking scans and turning then into report output"""

    (total_summary, total_totals, summaries, sbom_scans) = convert_into_summaries(scan_results)
    (
        scan_results_with_vulnerabilities,
        scan_results_with_secrets,
        scan_results_with_smells,
        scan_results_with_license_risks,
        scan_results_with_sboms,
        scan_results_with_warnings,
        scan_results_with_errors,
    ) = group_scans(scan_results)

    # TOOL SUMMARIES
    printable_summaries: list = summaries[:]
    printable_summaries.append(total_summary)

    # GIT BRANCH SUMMARIES
    git_branch = (
        "unknown"
        if len(scan_results) == 0
        else py_.get(scan_results[0].run_details, "git_branch", "Git Repo Not Detected")
    )

    return f"""{generate_markdown_header("Eze Report Results", 1)}
{generate_markdown_header(
    f"Summary  ![tools](https://img.shields.io/static/v1?style=plastic&label=Tools&message={len(scan_results)}&color=blue)",
    2,
)}

---

![critical](https://img.shields.io/static/v1?style=plastic&label=critical&message={total_totals["critical"]}&color=red)
![high](https://img.shields.io/static/v1?style=plastic&label=high&message={total_totals["high"]}&color=orange)
![medium](https://img.shields.io/static/v1?style=plastic&label=medium&message={total_totals["medium"]}&color=yellow)
![low](https://img.shields.io/static/v1?style=plastic&label=low&message={total_totals["low"]}&color=lightgrey)
![secrets](https://img.shields.io/static/v1?style=plastic&label=secrets&message={total_summary["Secrets"]}&color=red)

{generate_markdown_table(printable_summaries, False)}

f"<b>Branch tested:</b>&nbsp;{git_branch}"

{_print_errors_from_scan_results(scan_results_with_errors)}
{_print_findings_from_scan_results('Vulnerabilities', 'vulnerabilities', scan_results_with_vulnerabilities)}
{_print_findings_from_scan_results('Secrets', 'secrets', scan_results_with_secrets)}
{_print_findings_from_scan_results('Code Smells', 'smells', scan_results_with_smells)}
{_print_findings_from_scan_results('Licensing Risks', 'license_risks', scan_results_with_license_risks)}
{_print_sboms_from_scan_results(scan_results_with_sboms, print_transitive)}
{_print_warnings_from_scan_results(scan_results_with_warnings)}
"""


def _print_errors_from_scan_results(scan_results: list) -> str:
    """print errors from scan_results"""

    if len(scan_results) <= 0:
        return ""

    str_buffer: list[str] = []
    for scan_result in scan_results:
        run_details = scan_result.run_details
        tool_name = py_.get(run_details, "tool_name", "unknown")
        run_type = f":{run_details['run_type']}" if "run_type" in run_details and run_details["run_type"] else ""
        run_type_concat = ":" + run_type if run_type != "" else run_type

        str_buffer.append(generate_markdown_header(f"[{tool_name}{run_type_concat}] Errors", 3))
        for fatal_error in scan_result.fatal_errors:
            str_buffer.append(f"""{fatal_error}""")
    errors_str: str = "\n".join(str_buffer)
    return f"""{generate_markdown_header("Errors", 2)}
---
{errors_str}"""


def _print_findings_from_scan_results(
    title: str, finding_key: str, scan_results_with_vulnerabilities: list[ScanVO]
) -> str:
    """Method for taking scan vulnerabilities and printing them"""

    str_buffer = []

    if len(scan_results_with_vulnerabilities) <= 0:
        return ""

    str_buffer.append(generate_markdown_header(title, 2))
    str_buffer.append("""---""")
    for scan_result in scan_results_with_vulnerabilities:
        run_details = scan_result.run_details
        tool_name = py_.get(run_details, "tool_name", "unknown")
        run_type = f":{run_details['run_type']}" if "run_type" in run_details and run_details["run_type"] else ""

        str_buffer.append(generate_markdown_header(f"[{tool_name}{run_type}] {title}", 3))
        _print_scan_summary_title(scan_result, "    ")
        findings: list[FindingVO] = scan_result.__dict__[finding_key]
        finding: FindingVO = None
        for finding in findings:
            str_buffer.append(finding.to_markdown(escape_md=True))

    return "\n".join(str_buffer)


def _print_scan_summary_title(scan_result: ScanVO, prefix: str = "") -> str:
    """Title of scan summary title"""

    scan_summary = f"""{prefix}TOOL REPORT: {name_and_time_summary(scan_result, "")}\n"""

    # bom count if exists
    if has_sbom_data(scan_result):
        scan_summary += bom_short_summary(scan_result, prefix + "    ")

    # if bom only scan, do not print vulnerability count
    if has_vulnerability_data(scan_result):
        scan_summary += vulnerabilities_short_summary(scan_result, prefix + "    ")

    return scan_summary


def _print_sboms_from_scan_results(scan_results: list, print_transitive: bool = False) -> str:
    """print scan sbom"""

    str_buffer = []
    if len(scan_results) <= 0:
        return ""
    str_buffer.append(generate_markdown_header("Bill of Materials", 2))
    str_buffer.append("""---""")

    str_buffer.append("")

    for scan_result in scan_results:
        run_details = scan_result.run_details
        tool_name = py_.get(run_details, "tool_name", "unknown")
        run_type = f":{run_details['run_type']}" if "run_type" in run_details and run_details["run_type"] else ""
        for project_name in scan_result.sboms:
            cyclonedx_bom: dict = scan_result.sboms[project_name]
            sboms: list = annotated_sbom_table(cyclonedx_bom, print_transitive)
            str_buffer.append(
                f"""{generate_markdown_header(f"[{tool_name}{run_type}] {project_name} SBOM", 3)}

![components](https://img.shields.io/static/v1?style=plastic&label=components&message={len(sboms)}&color=blue)

{generate_markdown_table(sboms)}
"""
            )

    return "\n".join(str_buffer)


def _print_warnings_from_scan_results(scan_results: list) -> str:
    """print warnings from scan_results"""

    str_buffer = []
    if len(scan_results) <= 0:
        return ""

    str_buffer.append(generate_markdown_header("Warnings", 2))
    str_buffer.append("---")
    for scan_result in scan_results:
        run_details = scan_result.run_details
        tool_name = py_.get(run_details, "tool_name", "unknown")
        run_type = f":{run_details['run_type']}" if "run_type" in run_details and run_details["run_type"] else ""
        if len(scan_result.warnings) > 0:
            str_buffer.append(generate_markdown_header(f"[{tool_name}{run_type}] Warnings", 3))
            str_buffer.append(generate_markdown_list(scan_result.warnings))

    return "\n".join(str_buffer)
