# pylint: disable=invalid-name

"""Eze's core enums module"""
from enum import Enum


class SmellSeverityEnum(Enum):
    """
    Enum for smell
    Error, Warning, Note
    @see https://docs.github.com/en/code-security/code-scanning/automatically-scanning-your-code-for-vulnerabilities-and-errors/about-code-scanning-alerts
    """

    error = 0
    warning = 1
    note = 2

    @staticmethod
    def normalise_name(value: str, default="na") -> str:
        """Normalise the name of the enum"""
        if hasattr(VulnerabilitySeverityEnum, value):
            return value
        return default


class VulnerabilitySeverityEnum(Enum):
    """
    Enum for severity

    @see https://nvd.nist.gov/vuln-metrics/cvss
    """

    critical = 0
    high = 1
    medium = 2
    low = 3
    none = 4
    na = 5

    @staticmethod
    def normalise_name(value: str, default="na") -> str:
        """Normalise the name of the enum"""
        if hasattr(VulnerabilitySeverityEnum, value):
            return value
        return default


class ToolType(Enum):
    """Enum for Tool Type"""

    SBOM = "SBOM"  # Bill of Materials Tool
    SCA = "SCA"  # Software Composition Analysis
    SAST = "SAST"  # Insecure Code Scanners
    SECRET = "SECRET"  # Secrets Scanner
    MISC = "MISC"  # Other type of Scanner


class SourceType(Enum):
    """Enum for Source Type"""

    ALL = "ALL"  # Generic supports all source type
    PYTHON = "PYTHON"  # Python project
    BASH = "BASH"  # Bash files
    NODE = "NODE"  # Node project
    DOTNET = "DOTNET"  # C# and Dot Net project
    JAVA = "JAVA"  # Java Maven project
    GRADLE = "GRADLE"  # Java Gradle project
    SBT = "SBT"  # Java / Scala SBT project
    RUBY = "RUBY"  # Ruby project
    GO = "GO"  # Golang project
    PHP = "PHP"  # PHP project
    CONTAINER = "CONTAINER"  # Dockerfile / Container project


class LicenseScanType(Enum):
    """Enum for License Scan Type"""

    PROPRIETARY = "PROPRIETARY"  # for commercial projects, check for non-commercial, strong-copyleft, and source-available licenses
    PERMISSIVE = "PERMISSIVE"  # for permissive open source projects (aka MIT, LGPL), check for strong-copyleft licenses
    OPENSOURCE = (
        "OPENSOURCE"  # for copyleft open source projects (aka GPL), check for non-OSI or FsfLibre certified licenses
    )
    OFF = "OFF"  # no license checks
