"""sbom data value objects"""
from eze.utils.config import get_config_key


class Component:
    """Wrapper around raw dict to provide easy code typing, for annotated cyclonedx sbom components"""

    def __init__(self, vo: dict):
        """constructor"""
        self.type: str = get_config_key(vo, "type", str, "")
        self.name: str = get_config_key(vo, "name", str, "")
        self.version: str = get_config_key(vo, "version", str, "")
        self.description: str = get_config_key(vo, "description", str, "")
        self.is_transitive = get_config_key(vo, "is_transitive", bool, False)
        self.license: str = get_config_key(vo, "license", str, "unknown")
        self.license_type: str = get_config_key(vo, "license_type", str, "unknown")
        self.license_is_professional: str = get_config_key(vo, "license_is_professional", bool, None)
        self.license_is_osi_approved: str = get_config_key(vo, "license_is_osi_approved", bool, None)
        self.license_is_fsf_libre: str = get_config_key(vo, "license_is_fsf_libre", bool, None)
        self.license_is_deprecated: str = get_config_key(vo, "license_is_deprecated", bool, None)
