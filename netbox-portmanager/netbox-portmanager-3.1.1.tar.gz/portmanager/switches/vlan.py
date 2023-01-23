from typing import Tuple, List
import re


class Vlan:
    def __init__(
        self,
        vlan_index: int,
        vlan_description: str,
        vlan_enabled: bool=False,
    ) -> None:
        self.vlan_index = vlan_index
        self.vlan_description = vlan_description
        self.vlan_enabled = vlan_enabled
    
    def get_table_info(self) -> Tuple[str, str]:
        return {
            "vlan_index": self.vlan_index,
            "vlan_description": self.vlan_description,
            "vlan_enabled": self.vlan_enabled
        }


class VLANInterval:
    SYNTAX_PATTERN = "^\[(|\d+|\d+-\d+)(,\d+|,\d+-\d+)*\]$"
    def __init__(self, interval_string: str) -> None:
        self.intervals: List[Tuple[int, int]] = []
        if not self.check_and_build(interval_string=interval_string):
            raise RuntimeError("Method VLANInterval.check_and_build returned False.")

    def get_intervals(self) -> List[Tuple[int, int]]:
        return self.intervals

    @staticmethod
    def check_syntax(interval_string: str) -> bool:
        return re.search(VLANInterval.SYNTAX_PATTERN, interval_string) is not None

    def check_and_build(self, interval_string: str) -> bool:
        if not self.check_syntax(interval_string):
            return False

        interval_string = interval_string[1:-1]
        if len(interval_string) == 0:
            return True
        for vlan_id in interval_string.split(","):
            if "-" in vlan_id:
                min_id, max_id = vlan_id.split("-")
            else:
                min_id = max_id = int(vlan_id)
            self.intervals.append((int(min_id), int(max_id)))
        return True

    def check_boundaries(self, vlan: 'Vlan') -> bool:
        for interval in self.intervals:
            if interval[0] <= int(vlan.vlan_index) <= interval[1]:
                return True
        return False
