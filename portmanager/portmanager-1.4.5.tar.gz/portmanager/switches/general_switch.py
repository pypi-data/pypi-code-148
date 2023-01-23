from typing import Dict, List, Tuple, Any

from pysnmp.hlapi import *

from portmanager.switches.interface import Interface
from portmanager.switches.vlan import Vlan, VLANInterval

import re


class GeneralSwitch():
    NAME_OID_DICT = {
        'sysDescr': '1.3.6.1.2.1.1.1.0',
        'ifAdminStatus': '1.3.6.1.2.1.2.2.1.7',
        'ifDescr': '1.3.6.1.2.1.2.2.1.2',
        'ifIndex': '1.3.6.1.2.1.2.2.1.1',
        'dot1dTpFdbPort': '1.3.6.1.2.1.17.4.3.1.2',
        'dot1dTpFdbAddress': '1.3.6.1.2.1.17.4.3.1.1',
        'vmVlan': '1.3.6.1.4.1.9.9.68.1.2.2.1.2',
        'ifAlias': '1.3.6.1.2.1.31.1.1.1.18',
        'ifPhysAddress': '1.3.6.1.2.1.2.2.1.6',
        'vtpVlanName': '1.3.6.1.4.1.9.9.46.1.3.1.1.4.1',
        'dot1qVlanStaticName': '1.3.6.1.2.1.17.7.1.4.3.1.1',
        'dot1qVlanStaticPort': '1.3.6.1.4.1.207.1.4.167.116.7.1.4.5.1.1',
        'dot1qVlanStaticForbidPorts': '1.3.6.1.2.1.17.7.1.4.3.1.3',
        'dot1qVlanStaticEgressPorts': '1.3.6.1.2.1.17.7.1.4.3.1.2',
        'dot1qVlanStaticUntaggedPorts': '1.3.6.1.2.1.17.7.1.4.3.1.4',
        'dot1qVlanStaticTable': '1.3.6.1.2.1.17.7.1.4.3.1.4',
        'dot1dBasePortIfIndex': '1.3.6.1.2.1.17.1.4.1.2',
        'dot3StatsIndex': '1.3.6.1.2.1.10.7.2.1.1',
        'h3cvlanlist': '1.3.6.1.4.1.2011.2.23.1.2.1.1.1.1',
        'ifTrunk': '1.3.6.1.4.1.9.9.46.1.6.1.1.14',
        'ifOperStatus': '1.3.6.1.2.1.2.2.1.8',
        'ipNetToMediaPhysAddress': '1.3.6.1.2.1.4.22.1.2',
        'ipNetToMedia': '1.3.6.1.2.1.4.35',
        'vlanTrunkPortVlansEnabled': '1.3.6.1.4.1.9.9.46.1.6.1.1.4',
        'cpsIfPortSecurityEnable': '1.3.6.1.4.1.9.9.315.1.2.1.1.1',
        'cpsIfMaxSecureMacAddr': '1.3.6.1.4.1.9.9.315.1.2.1.1.3',
        'vtpRevNum': '1.3.6.1.4.1.9.9.46.1.2.1.1.4.1',
        'ifName': '1.3.6.1.2.1.31.1.1.1.1',
        'ifType': '1.3.6.1.2.1.2.2.1.3',
        'cpeExtPsePortEntry': '1.3.6.1.4.1.9.9.402.1.2.1.9',
        'writeMem': '1.3.6.1.4.1.9.2.1.54.0'
    }
    
    OID_NAME_DICT = {oid: name for name, oid in NAME_OID_DICT.items()}

    def __init__(
        self, 
        fqdn: str, 
        community_string: str, 
        interval_string: str = "[]", 
        portsec_max: int = 16384
    ) -> None:
        self.fqdn = fqdn
        self.community_string = community_string
        self.portsec_max = portsec_max
        self.vlan_interval = VLANInterval(interval_string)

        self.interfaces: Dict[str, Interface] = {}
        self.vlans: Dict[str, Vlan] = {}

    def _filter_vlans(self) -> None:
        for vlan in self.vlans.values():
            if self.vlan_interval.check_boundaries(vlan):
                vlan.vlan_enabled = True

    def _filter_interfaces(self) -> None:
        filtered_interfaces = {}
        for if_index, interface in self.interfaces.items():
            if interface.if_type == 6 and \
                interface.if_ps_enable is not None and \
                interface.if_ps_max is not None:

                if interface.if_trunk == 1 or interface.if_vlan is None:
                    interface.if_enabled = False
                    interface.if_comment = "No access. Port is TRUNK."
                elif interface.if_ps_enable == 2:
                    interface.if_enabled = False
                    interface.if_comment = "No access. Port has not setup 'mode access' or 'port-security'."

                filtered_interfaces[if_index] = interface
        self.interfaces = filtered_interfaces

    @staticmethod
    def check_interfaces_data(data: Dict[str, List[str]]) -> bool:
        wanted_keys = set(["if_index", "if_admin_status", "if_ps_max", "if_description", "if_vlan"])
        if wanted_keys != set(data.keys()):
            return False 
        if not (len(data["if_index"]) \
            == len(data["if_admin_status"]) \
            == len(data["if_ps_max"]) \
            == len(data["if_description"]) \
            == len(data["if_vlan"])
        ):
            return False
        return True

    

    def get_interfaces(self) -> List[Dict[str, str]]:
        return [interface.get_table_info() for interface in self.interfaces.values()]

    def get_vlans(self) -> List[Tuple[str, str]]:
        return {str(vlan.vlan_index): vlan.get_table_info() for vlan in self.vlans.values()}

    @staticmethod
    def load_object(obj: Any, key: str, collector: Dict[str, Dict[str, str]], obj_kwargs: Dict[str, str]) -> None:
        collector[key] = obj(**obj_kwargs)
