"""
Enumeration of supported purl types
"""

from enum import Enum


class PurlType(Enum):
    """
    Enumeration of supported purl types
    """

    DEB = "deb"
    DOCKER = "docker"
    GENERIC = "generic"
    GIT = "git"
    GITHUB = "github"
    GITLAB = "gitlab"
    GOLANG = "golang"
    HELM = "helm"
    MAVEN = "maven"
    NPM = "npm"
    PYPI = "pypi"
    RPM = "rpm"

    def __str__(self) -> str:
        return self.value
