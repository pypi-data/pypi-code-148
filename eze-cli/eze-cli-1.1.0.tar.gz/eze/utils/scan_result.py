"""Utilities for cyclone dx SBOM"""
from eze.utils.vo.enums import ToolType
from pydash import py_

from eze.core.tool import ToolMeta
from eze.utils.vo.findings import ScanVO
from eze.core.license import get_bom_license, check_licenses


def convert_sbom_into_scan_result(tool: ToolMeta, cyclonedx_bom: dict, project: str = "project"):
    """convert sbom into scan_result"""
    (license_risks, code_smells, warnings) = check_licenses(
        cyclonedx_bom,
        tool.config["LICENSE_CHECK"],
        tool.config["LICENSE_ALLOWLIST"],
        tool.config["LICENSE_DENYLIST"],
        project,
    )
    return ScanVO(
        {
            "tool": tool.TOOL_NAME,
            # bom is deprecated will be removed soon
            "bom": cyclonedx_bom,
            "sboms": {project: cyclonedx_bom},
            "license_risks": license_risks,
            "smells": code_smells,
            "warnings": warnings,
        }
    )


def convert_multi_sbom_into_scan_result(tool: ToolMeta, cyclonedx_boms: dict):
    """convert sbom into scan_result"""
    first_bom = None
    license_risks_list: list = []
    code_smells_list: list = []
    warnings_list: list = []
    for project_name in cyclonedx_boms:
        cyclonedx_bom = cyclonedx_boms[project_name]
        first_bom = cyclonedx_bom

        (license_risks, code_smells, warnings) = check_licenses(
            cyclonedx_bom,
            tool.config["LICENSE_CHECK"],
            tool.config["LICENSE_ALLOWLIST"],
            tool.config["LICENSE_DENYLIST"],
            project_name,
        )
        license_risks_list.extend(license_risks)
        code_smells_list.extend(code_smells)
        warnings_list.extend(warnings)

    return ScanVO(
        {
            "tool": tool.TOOL_NAME,
            # bom is deprecated will be removed soon
            "bom": first_bom,
            "sboms": cyclonedx_boms,
            "license_risks": license_risks_list,
            "code_smells": code_smells_list,
            "warnings": warnings_list,
        }
    )


def name_and_time_summary(scan_result: ScanVO, indent: str = "    ") -> str:
    """convert scan_result into one line summary"""
    run_details = scan_result.run_details
    #
    tool_name = py_.get(run_details, "tool_name", "unknown")
    run_type = f":{run_details['run_type']}" if "run_type" in run_details and run_details["run_type"] else ""
    scan_type = f"[{run_details['scan_type']}] " if "scan_type" in run_details and run_details["scan_type"] else ""
    duration_sec = py_.get(run_details, "duration_sec", "unknown")
    return f"""{indent}{scan_type}{tool_name}{run_type} (scan duration: {duration_sec:0.1f} seconds)"""


def bom_short_summary(scan_result: ScanVO, indent: str = "    ", print_transitive: bool = False) -> str:
    """convert bom into one line summary"""
    if not has_sbom_data(scan_result):
        return ""
    if len(scan_result.fatal_errors) > 0:
        return "ERROR when creating SBOM"
    totals_txts = []
    for project_name in scan_result.sboms:
        cyclonedx_bom = scan_result.sboms[project_name]
        license_counts = {}

        # extract non transitive if desired
        valid_components = []
        for component in py_.get(cyclonedx_bom, "components", []):
            is_transitive = py_.get(component, "properties.transitive", False)
            if not print_transitive and is_transitive:
                continue
            valid_components.append(component)

        component_count = len(valid_components)
        totals_txt = f"""{indent}{project_name} components: {component_count}"""
        if component_count > 0:
            totals_txt += " ("
            breakdowns = []
            for component in valid_components:
                licenses = component.get("licenses", [])
                if len(licenses) == 0:
                    license_counts["unknown"] = license_counts.get("unknown", 0) + 1
                for license_dict in licenses:
                    license_name = get_bom_license(license_dict)
                    if license_name:
                        license_counts[license_name] = license_counts.get(license_name, 0) + 1
            for license_name in license_counts:
                license_count = license_counts[license_name]
                breakdowns.append(f"{license_name}:{license_count}")
            totals_txt += ", ".join(breakdowns)
            totals_txt += ")"
            totals_txts.append(totals_txt)
    return "\n".join(totals_txts) + "\n"


def vulnerabilities_short_summary(scan_result: ScanVO, indent: str = "    ") -> str:
    """convert bom into one line summary"""
    summary_totals = scan_result.summary["totals"]
    summary_ignored = scan_result.summary["ignored"]
    return (
        f"""{indent}{_get_scan_summary_totals(summary_totals, "total", scan_result.warnings)}
{indent}{_get_scan_summary_totals(summary_ignored, "ignored", scan_result.warnings)}"""
        + "\n"
    )


def _get_scan_summary_totals(summary_totals: dict, title: str, warnings: list) -> str:
    """get text summary of summary dict"""
    totals_txt = f"{title}: {summary_totals['total']} "
    if summary_totals["total"] > 0:
        totals_txt += "("
        breakdowns = []
        for key in ["critical", "high", "medium", "low", "none", "na"]:
            if summary_totals[key] > 0:
                breakdowns.append(f"{key}:{summary_totals[key]}")

        if len(warnings) > 0:
            breakdowns.append("warnings:true")

        totals_txt += ", ".join(breakdowns)
        totals_txt += ")"
    return totals_txt


def has_sbom_data(scan_result: ScanVO) -> bool:
    """if scanresult has sbom data"""
    return bool(scan_result.sboms and len(scan_result.sboms) > 0)


def has_vulnerability_data(scan_result: ScanVO) -> bool:
    """if scanresult has vulnerability or has no sbom data (meaning vulnerabilities are zero)"""
    tool_type: str = py_.get(scan_result, "run_details.tool_type", "")
    return len(scan_result.vulnerabilities) > 0 or tool_type == ToolType.SCA


def has_secret_data(scan_result: ScanVO) -> bool:
    """if scanresult has vulnerability or has no sbom data (meaning vulnerabilities are zero)"""
    tool_type: str = py_.get(scan_result, "run_details.tool_type", "")
    return len(scan_result.secrets) > 0 or tool_type == ToolType.SECRET


def has_smell_data(scan_result: ScanVO) -> bool:
    """if scanresult has vulnerability or has no sbom data (meaning vulnerabilities are zero)"""
    tool_type: str = py_.get(scan_result, "run_details.tool_type", "")
    return len(scan_result.smells) > 0 or tool_type == ToolType.SAST


def convert_into_summaries(scans: list[ScanVO]) -> tuple:
    """create a simple summary of all tool results"""
    total_totals = {
        "critical": 0,
        "high": 0,
        "medium": 0,
        "low": 0,
        "total": 0,
        "smells": 0,
        "smell_errors": 0,
        "smell_warnings": 0,
        "smell_notes": 0,
    }
    total_summary: dict = {
        "Name": "All Tools",
        "Type": "ALL",
        "Vulnerabilities": 0,
        "Secrets": 0,
        "Smells": 0,
        "LRisks": 0,
        "Ignored": 0,
        "Warnings": "False",
        "Time": 0,
    }
    sbom_scans = []
    summaries = []
    has_vulnerabilities: bool = False
    has_secrets: bool = False
    has_smells: bool = False
    has_license_risks: bool = False

    def create_smell_summary(totals: dict) -> str:
        summary: str = ""
        if totals["smells"] == 0:
            return "None Found"
        if totals["smell_errors"]:
            summary += " Errors:" + str(totals["smell_errors"])
        if totals["smell_warnings"]:
            summary += " Warnings:" + str(totals["smell_warnings"])
        if totals["smell_notes"]:
            summary += " Notes:" + str(totals["smell_notes"])
        return summary

    def create_vulnerabilty_summary(totals: dict) -> str:
        summary: str = ""
        if totals["total"] == 0:
            return "None Found"
        if totals["critical"]:
            summary += " Critical:" + str(totals["critical"])
        if totals["high"]:
            summary += " High:" + str(totals["high"])
        if totals["medium"]:
            summary += " Medium:" + str(totals["medium"])
        if totals["low"]:
            summary += " Low:" + str(totals["low"])
        return summary

    for scan_result in scans:
        run_details = scan_result.run_details
        tool_name = py_.get(run_details, "tool_name", "unknown")
        run_type = f":{run_details['run_type']}" if "run_type" in run_details and run_details["run_type"] else ""
        scan_type = run_details["tool_type"] if "tool_type" in run_details and run_details["tool_type"] else "unknown"
        duration_sec = py_.get(run_details, "duration_sec", "unknown")

        if has_sbom_data(scan_result):
            sbom_scans.append(scan_result)

        entry: dict = {
            "Name": tool_name + run_type,
            "Type": scan_type,
            "Vulnerabilities": "-",
            "Secrets": "-",
            "Smells": "-",
            "LRisks": "-",
            "Ignored": "-",
            "Warnings": str(len(scan_result.warnings) > 0) or len(scan_result.fatal_errors) > 0,
            "Time": "{:.1f}s".format(duration_sec),
        }
        if entry["Warnings"] == "True":
            total_summary["Warnings"] = "True"
        total_summary["Time"] += duration_sec

        if len(scan_result.fatal_errors) > 0:
            entry["Ignored"] = "Error"
            entry["Vulnerabilities"] = "Error"
            entry["Secrets"] = "Error"
            entry["Smells"] = "Error"
            entry["Ignored"] = "Error"
        else:
            if len(scan_result.vulnerabilities) > 0 or scan_type == ToolType.SCA:
                entry["Vulnerabilities"] = create_vulnerabilty_summary(scan_result.summary["totals"])
                total_summary["Ignored"] += int(scan_result.summary["ignored"]["total"])
                total_totals["critical"] += int(scan_result.summary["totals"]["critical"])
                total_totals["high"] += int(scan_result.summary["totals"]["high"])
                total_totals["medium"] += int(scan_result.summary["totals"]["medium"])
                total_totals["low"] += int(scan_result.summary["totals"]["low"])
                total_totals["total"] += int(scan_result.summary["totals"]["total"])
                has_vulnerabilities = True
            if len(scan_result.secrets) > 0 or scan_type == ToolType.SECRET:
                entry["Secrets"] = str(scan_result.summary["totals"]["secrets"])
                entry["Ignored"] = str(scan_result.summary["ignored"]["secrets"])
                total_summary["Ignored"] += int(scan_result.summary["ignored"]["secrets"])
                total_summary["Secrets"] += int(scan_result.summary["totals"]["secrets"])
                has_secrets = True
            if len(scan_result.smells) > 0 or scan_type == ToolType.SAST:
                entry["Smells"] = create_smell_summary(scan_result.summary["totals"])
                entry["Ignored"] = str(scan_result.summary["ignored"]["smells"])
                total_summary["Ignored"] += int(scan_result.summary["ignored"]["smells"])
                total_totals["smells"] += int(scan_result.summary["totals"]["smells"])
                total_totals["smell_errors"] += int(scan_result.summary["totals"]["smell_errors"])
                total_totals["smell_warnings"] += int(scan_result.summary["totals"]["smell_warnings"])
                total_totals["smell_notes"] += int(scan_result.summary["totals"]["smell_notes"])
                has_smells = True
            if len(scan_result.license_risks) > 0:
                entry["LRisks"] = str(scan_result.summary["totals"]["license_risks"])
                entry["Ignored"] = str(scan_result.summary["ignored"]["license_risks"])
                total_summary["Ignored"] += int(scan_result.summary["ignored"]["license_risks"])
                total_summary["LRisks"] += int(scan_result.summary["totals"]["license_risks"])
                has_license_risks = True
        summaries.append(entry)
    # Normalise into str
    total_summary["Vulnerabilities"] = create_vulnerabilty_summary(total_totals) if has_vulnerabilities else "-"
    total_summary["Secrets"] = str(total_summary["Secrets"] if has_secrets else "-")
    total_summary["Smells"] = create_smell_summary(total_totals) if has_smells else "-"
    total_summary["LRisks"] = str(total_summary["LRisks"] if has_license_risks else "-")
    total_summary["Ignored"] = str(total_summary["Ignored"])
    total_summary["Time"] = "{:.1f}s".format(total_summary["Time"])
    #
    return (total_summary, total_totals, summaries, sbom_scans)


def group_scans(scans: list[ScanVO]) -> tuple:
    """create a simple grouping of all tool results"""
    scan_results_with_vulnerabilities: list = []
    scan_results_with_secrets: list = []
    scan_results_with_smells: list = []
    scan_results_with_license_risks: list = []
    scan_results_with_sboms: list = []
    scan_results_with_warnings: list = []
    scan_results_with_errors: list = []
    for scan_result in scans:
        if has_vulnerability_data(scan_result):
            scan_results_with_vulnerabilities.append(scan_result)
        if has_secret_data(scan_result):
            scan_results_with_secrets.append(scan_result)
        if has_smell_data(scan_result):
            scan_results_with_smells.append(scan_result)
        if has_sbom_data(scan_result):
            scan_results_with_sboms.append(scan_result)
        if len(scan_result.license_risks) > 0:
            scan_results_with_license_risks.append(scan_result)
        if len(scan_result.warnings) > 0:
            scan_results_with_warnings.append(scan_result)
        if len(scan_result.fatal_errors) > 0:
            scan_results_with_errors.append(scan_result)
    return (
        scan_results_with_vulnerabilities,
        scan_results_with_secrets,
        scan_results_with_smells,
        scan_results_with_license_risks,
        scan_results_with_sboms,
        scan_results_with_warnings,
        scan_results_with_errors,
    )
