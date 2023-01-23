from typing import Dict, Optional


class Interface():
    def __init__(self, 
        if_index: int,
        if_name: Optional[int], 
        if_type: Optional[int], 
        if_description: Optional[str], 
        if_vlan: Optional[int], 
        if_trunk: Optional[int], 
        if_admin_status: Optional[int], 
        if_oper_status: Optional[int], 
        if_poe: Optional[int],
        if_ps_enable: Optional[int],
        if_ps_max: Optional[int],
        if_enabled: bool = True,
        if_comment: str = ""
    ) -> None:
        self.if_index = if_index
        self.if_name = if_name
        self.if_type = if_type
        self.if_description = if_description
        self.if_vlan = if_vlan
        self.if_trunk = if_trunk
        self.if_admin_status = if_admin_status
        self.if_oper_status = if_oper_status
        self.if_poe = if_poe
        self.if_ps_enable = if_ps_enable
        self.if_ps_max = if_ps_max
        self.if_enabled = if_enabled
        self.if_comment = if_comment

    def get_table_info(self) -> Dict[str, str]:
        return {
            "if_index": self.if_index,
            "if_name": self.if_name,
            "if_vlan": self.if_vlan,
            "if_description": self.if_description,
            "if_portsec": None if self.if_ps_enable == 2 else self.if_ps_max,
            "if_ps_enable": self.if_ps_enable,
            "if_ps_max": self.if_ps_max,
            "if_admin_status": self.if_admin_status,
            "if_oper_status": self.if_oper_status,
            "if_poe": self.if_poe / 1000 if isinstance(self.if_poe, int) else self.if_poe,
            "if_enabled": self.if_enabled,
            "if_comment": self.if_comment,
        }

    def __repr__(self) -> str:
        return "{\n" +\
               f"    if_index = {self.if_index}\n" +\
               f"    if_name = {self.if_name}\n" +\
               f"    if_type = {self.if_type}\n" +\
               f"    if_description = {self.if_description}\n" +\
               f"    if_vlan = {self.if_vlan}\n" +\
               f"    if_trunk = {self.if_trunk}\n" +\
               f"    if_admin_status = {self.if_admin_status}\n" +\
               f"    if_oper_status = {self.if_oper_status}\n" +\
               f"    if_poe = {self.if_poe}\n" +\
               f"    if_ps_enable = {self.if_ps_enable}\n" +\
               f"    if_ps_max = {self.if_ps_max}\n" +\
               f"    if_enabled = {self.if_enabled}\n" +\
               f"    if_comment = {self.if_comment}\n" +\
               "}\n" 



