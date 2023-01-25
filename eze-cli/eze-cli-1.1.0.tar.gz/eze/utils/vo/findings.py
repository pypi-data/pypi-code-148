"""Eze's finding value object module"""
from eze.utils.io.print import (
    escape_markdown_text,
    non_escape_text,
)

from eze.utils.vo.enums import VulnerabilitySeverityEnum, SmellSeverityEnum
from eze.utils.config import get_config_key
from pydash import py_

from eze.utils.io.file import normalise_linux_file_path


class FindingVO:
    """finding from security tool"""

    def __init__(self, vo: dict):
        """constructor"""
        # package name for SCA / file name for SAST
        self.name: str = get_config_key(vo, "name", str, "")
        # description of issue for SCA/SAST
        self.overview: str = get_config_key(vo, "overview", str, "")
        # [optional] mitigation recommendations for SCA/SAST
        self.recommendation: str = get_config_key(vo, "recommendation", str, "")
        self.is_ignored: bool = get_config_key(vo, "is_ignored", bool, False)
        self.is_excluded: bool = get_config_key(vo, "is_excluded", bool, False)
        # [optional] containers cve/cwe info
        self.identifiers: dict = get_config_key(vo, "identifiers", dict, {})
        # [optional] pair of File/Line
        self.file_location: dict = get_config_key(vo, "file_location", dict, None)
        # [optional] list of reference urls
        self.references: list = get_config_key(vo, "references", list, [])
        # misc container
        self.metadata: dict = get_config_key(vo, "metadata", dict, None)

    def update_ignored(self, tool_config: dict) -> bool:
        """detect if vulnerability is to be ignored"""
        # TODO: move function to util
        if self.is_ignored:
            self.is_ignored = True
            return True
        if self.name in tool_config["IGNORED_VULNERABILITIES"]:
            self.is_ignored = True
            return True
        for identifier_key in self.identifiers:
            identifier_value = self.identifiers[identifier_key]
            if identifier_value in tool_config["IGNORED_VULNERABILITIES"]:
                self.is_ignored = True
                return True
        file_location = py_.get(self, "file_location.path", False)
        if file_location:
            file_location = normalise_linux_file_path(file_location)
            for ignored_path in tool_config["IGNORED_FILES"]:
                if file_location.startswith(ignored_path):
                    self.is_ignored = True
                    return True
        self.is_ignored = False
        return False

    def update_excluded(self, tool_config: dict) -> bool:
        """detect if vulnerability is to be excluded"""
        # TODO: move function to util
        if self.is_excluded:
            self.is_excluded = True
            return True

        file_location = py_.get(self, "file_location.path", False)
        if file_location:
            file_location = normalise_linux_file_path(file_location)
            for excluded_path in tool_config["EXCLUDE"]:
                if file_location.startswith(excluded_path):
                    self.is_excluded = True
                    return True

        self.is_excluded = False
        return False

    def to_markdown(self, *, indent: str = "", escape_md: bool = True, count: int = None, tool_name: str = None) -> str:
        """simple to markdown representation of vulnerability finding"""
        esc = escape_markdown_text if escape_md else non_escape_text

        def identifier_table(identifiers):
            if len(identifiers) == 0:
                return ""
            vulnerability_identifier: str = "\n"
            for identifier_key in identifiers:
                identifier_value = identifiers[identifier_key]
                vulnerability_identifier += f" - {indent}**{esc(identifier_key)}**: {esc(identifier_value)}\n"
            return vulnerability_identifier + f"\n{indent}\n"

        return f"""{indent}**{esc(str(count)) + ') ' if count else ""}{esc(tool_name) + ': ' if tool_name else ""}{esc(self.name)}{" (ignored)" if self.is_ignored else ''}**
{f"{indent}**file**: {esc(py_.get(self, 'file_location.path', '-'))} (line {esc(py_.get(self, 'file_location.line', '-'))}" if self.file_location else ""}
{indent}**overview**: {esc(self.overview)}
{identifier_table(self.identifiers)}
{indent}**recommendation**: {f"{esc(self.recommendation.strip())}" if self.recommendation else "none"}
{indent}
"""


class SecretVO(FindingVO):
    """Hard coded secret finding from SAST Secret tool"""

    pass


class SmellVO(FindingVO):
    """Security code smell finding from SAST tool"""

    def __init__(self, vo: dict):
        """constructor"""
        # Smell severity level
        self.severity: str = get_config_key(vo, "severity", str, "").lower()
        super().__init__(vo)

    def to_markdown(self, *, indent: str = "", escape_md: bool = True, count: int = None, tool_name: str = None) -> str:
        """simple to markdown representation of vulnerability finding"""
        esc = escape_markdown_text if escape_md else non_escape_text

        def identifier_table(identifiers):
            if len(identifiers) == 0:
                return ""
            vulnerability_identifier: str = "\n"
            for identifier_key in identifiers:
                identifier_value = identifiers[identifier_key]
                vulnerability_identifier += f" - {indent}**{esc(identifier_key)}**: {esc(identifier_value)}\n"
            return vulnerability_identifier + f"\n{indent}\n"

        return f"""{indent}**{esc(str(count)) + ') ' if count else ""}{esc(tool_name) + ': ' if tool_name else ""}{esc(self.severity)} : {esc(self.name)}{" (ignored)" if self.is_ignored else ''}**
{f"{indent}**file**: {esc(py_.get(self, 'file_location.path', '-'))} (line {esc(py_.get(self, 'file_location.line', '-'))})" if self.file_location else ""}
{indent}**overview**: {esc(self.overview)}
{identifier_table(self.identifiers)}
{indent}**recommendation**: {esc(self.recommendation.strip()) if self.recommendation else "none"}
{indent}
"""


class LicenseRiskVO(FindingVO):
    """License risk finding from license scan tool"""

    pass


class VulnerabilityVO(FindingVO):
    """Vulnerability finding from SCA Secret tool"""

    def __init__(self, vo: dict):
        """constructor"""
        # CVE severity level
        self.severity: str = get_config_key(vo, "severity", str, "").lower()
        # [optional] version of dependency under test
        self.version: str = get_config_key(vo, "version", str, "")
        super().__init__(vo)

    def update_ignored(self, tool_config: dict) -> bool:
        """update ignored flag in VO"""
        if super().update_ignored(tool_config):
            return True
        severity_level = VulnerabilitySeverityEnum[self.severity].value
        if severity_level > tool_config["IGNORE_BELOW_SEVERITY_INT"]:
            self.is_ignored = True
            return True
        self.is_ignored = False
        return False

    def to_markdown(self, *, indent: str = "", escape_md: bool = True, count: int = None, tool_name: str = None) -> str:
        """simple to markdown representation of vulnerability finding"""
        esc = escape_markdown_text if escape_md else non_escape_text

        def identifier_table(identifiers):
            if len(identifiers) == 0:
                return ""
            vulnerability_identifier: str = "\n"
            for identifier_key in identifiers:
                identifier_value = identifiers[identifier_key]
                vulnerability_identifier += f" - {indent}**{esc(identifier_key)}**: {esc(identifier_value)}\n"
            return vulnerability_identifier + f"\n{indent}\n"

        return f"""{indent}**{esc(str(count)) + ') ' if count else ""}{esc(tool_name) + ': ' if tool_name else ""}{esc(self.severity)} : {esc(self.name)}{f" ({esc(self.version)})" if self.version else ""}{" (ignored)" if self.is_ignored else ''}**
{f"{indent}**file**: {esc(py_.get(self, 'file_location.path', '-'))} (line {esc(py_.get(self, 'file_location.line', '-'))})" if self.file_location else ""}
{indent}**overview**: {esc(self.overview)}
{identifier_table(self.identifiers)}
{indent}**recommendation**: {f"{esc(self.recommendation.strip())}" if self.recommendation else "none"}
{indent}
"""


class ScanVO:
    """
    VO for Tool Scan Results, contains the findings from tools

    # Data
    - tool
    - sboms
    - license_risks
    - vulnerabilities
    - secrets
    - smells

    # Meta Data
    - summary
    - run_details
    - warnings
    - fatal_errors
    """

    def __init__(self, vo: dict):
        """constructor"""
        # Data
        self.tool: str = get_config_key(vo, "tool", str, None)

        # bom and boms in Cyclonedx format
        # https://cyclonedx.org/
        self.sboms: dict = get_config_key(vo, "sboms", dict, None)

        raw_vulnerabilities = get_config_key(vo, "vulnerabilities", list, [])
        self._rehydrate(raw_vulnerabilities, VulnerabilityVO)
        self.vulnerabilities: list[VulnerabilityVO] = raw_vulnerabilities

        raw_secrets = get_config_key(vo, "secrets", list, [])
        self._rehydrate(raw_secrets, SecretVO)
        self.secrets: list[SecretVO] = raw_secrets

        raw_smells = get_config_key(vo, "smells", list, [])
        self._rehydrate(raw_smells, SmellVO)
        self.smells: list[SmellVO] = raw_smells

        raw_license_risks = get_config_key(vo, "license_risks", list, [])
        self._rehydrate(raw_license_risks, LicenseRiskVO)
        self.license_risks: list[LicenseRiskVO] = raw_license_risks

        # Meta Data
        self.summary: dict = get_config_key(vo, "summary", dict, {})
        self.run_details: dict = get_config_key(vo, "run_details", dict, {})

        # String list of Warnings from Tooling
        self.warnings: list = get_config_key(vo, "warnings", list, [])

        # String list of Fatal Errors from Tooling
        # one or more occurrences will
        self.fatal_errors: list = get_config_key(vo, "fatal_errors", list, [])

    @staticmethod
    def _rehydrate(vos: list[FindingVO], vo_class_type):
        """helper to rehydrate VOs if not VO Class but raw dict"""
        for i, vulnerability in enumerate(vos):
            if isinstance(vulnerability, vo_class_type):
                continue
            if isinstance(vulnerability, dict):
                vos[i] = vo_class_type(vulnerability)
                continue
            # WARNING: unable to rehydrate poor data

    def finalise(self, tool_config: dict):
        """count vulnerabilities and create summary"""
        summary: dict = {
            "ignored": {
                "total": 0,
                "critical": 0,
                "high": 0,
                "medium": 0,
                "low": 0,
                "none": 0,
                "na": 0,
                "secrets": 0,
                "smells": 0,
                "smell_errors": 0,
                "smell_warnings": 0,
                "smell_notes": 0,
            },
            "totals": {
                "total": 0,
                "critical": 0,
                "high": 0,
                "medium": 0,
                "low": 0,
                "none": 0,
                "na": 0,
                "secrets": 0,
                "smells": 0,
                "smell_errors": 0,
                "smell_warnings": 0,
                "smell_notes": 0,
                "license_risks": 0,
            },
        }
        # normalise vulnerabilities list
        self.vulnerabilities = self._normalise_vulnerabilities(tool_config)
        # sort by severity and ignored status
        self.vulnerabilities = sorted(self.vulnerabilities, key=self._vulnerability_sort_heuristic)
        self.smells = sorted(self.smells, key=self._smell_sort_heuristic)
        # count summary
        for vulnerability in self.vulnerabilities:
            # increment counters
            if vulnerability.is_ignored:
                summary["ignored"]["total"] += 1
                summary["ignored"][vulnerability.severity] += 1
            else:
                summary["totals"]["total"] += 1
                summary["totals"][vulnerability.severity] += 1
        for secret in self.secrets:
            # increment counters
            if secret.is_ignored:
                summary["ignored"]["secrets"] += 1
            else:
                summary["totals"]["secrets"] += 1
        for smell in self.smells:
            # increment counters
            if smell.is_ignored:
                summary["ignored"]["smells"] += 1
                summary["ignored"]["smell_" + smell.severity + "s"] += 1
            else:
                summary["totals"]["smells"] += 1
                summary["totals"]["smell_" + smell.severity + "s"] += 1
        for license_risk in self.license_risks:
            # increment counters
            if license_risk.is_ignored:
                summary["ignored"]["license_risks"] += 1
            else:
                license_risk["totals"]["license_risks"] += 1
        self.summary = summary

    def _normalise_vulnerabilities(self, tool_config: dict) -> list[VulnerabilityVO]:
        """sort and normalise any corrupted values in vulnerabilities"""
        vulnerabilities: list[VulnerabilityVO] = self.vulnerabilities
        # normalise any corrupted values
        for vulnerability in vulnerabilities:
            vulnerability.severity = self._get_severity(vulnerability, tool_config)
            vulnerability.update_ignored(tool_config)
            vulnerability.update_excluded(tool_config)
        vulnerabilities = [x for x in vulnerabilities if not x.is_excluded]
        return vulnerabilities

    @staticmethod
    def _vulnerability_sort_heuristic(vulnerability: VulnerabilityVO):
        """sort heuristic function"""
        sort_key: str = "b_" if vulnerability.is_ignored else "a_"
        sort_key += str(VulnerabilitySeverityEnum[vulnerability.severity].value) + "_"
        sort_key += str(vulnerability.name) + "_" + str(vulnerability.overview)
        return sort_key

    @staticmethod
    def _smell_sort_heuristic(smell: SmellVO) -> list:
        """sort heuristic function"""
        sort_key: str = "b_" if smell.is_ignored else "a_"
        sort_key += str(SmellSeverityEnum[smell.severity].value) + "_"
        sort_key += str(smell.name) + "_" + str(smell.overview)
        return sort_key

    def _get_severity(self, vulnerability: VulnerabilityVO, tool_config: dict) -> str:
        """detect severity of vulnerability"""
        severity = (vulnerability.severity or "").lower()
        if hasattr(VulnerabilitySeverityEnum, severity):
            return severity
        return tool_config["DEFAULT_SEVERITY"]
