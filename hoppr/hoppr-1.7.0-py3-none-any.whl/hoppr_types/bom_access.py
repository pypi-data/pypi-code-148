"""
Enumeration to indicate how a plugin may change a BOM
"""
import enum

from typing import Any

from hoppr_cyclonedx_models.cyclonedx_1_4 import Component
from hoppr_cyclonedx_models.cyclonedx_1_4 import CyclonedxSoftwareBillOfMaterialsStandard as Bom  # type: ignore


class BomAccess(enum.IntEnum):
    """
    Enumeration to indicate how a plugin may change a BOM
    """

    NO_ACCESS = 0
    COMPONENT_ACCESS = 1
    FULL_ACCESS = 2

    def has_access_to(self, obj: Any) -> bool:
        """
        Determine whether the specified value allows updates to an object
        """
        match self:
            case BomAccess.NO_ACCESS:
                return obj is None
            case BomAccess.COMPONENT_ACCESS:
                return isinstance(obj, Component)
            case BomAccess.FULL_ACCESS:
                return isinstance(obj, Bom)
