from pysnmp.hlapi import *

from portmanager.switches.general_switch import GeneralSwitch
from portmanager.switches.interface import Interface
from portmanager.switches.vlan import Vlan
from portmanager.switches.utils import *

from typing import List

import re


RESULT = List[Dict[str, str]]

class CiscoSwitch(GeneralSwitch):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def load_vlans_real(self) -> None:
        snmp_results=snmp_walk(
            fqdn=self.fqdn,
            credentials=self.community_string,
            oids={
                self.NAME_OID_DICT["vtpVlanName"]: str
            }
        )
        for index, vlan_desc in snmp_results[self.NAME_OID_DICT["vtpVlanName"]].items():
            self.load_object(Vlan, index, self.vlans, {"vlan_index": int(index), "vlan_description": vlan_desc})

        self._filter_vlans()

    def load_vlan_interface_macs(self, vlan_id: str, if_index: str):
        results = []
        snmp_results_vlan_macs = snmp_walk(
            fqdn=self.fqdn,
            credentials=f"{self.community_string}@{vlan_id}",
            oids={
                self.NAME_OID_DICT["dot1dTpFdbPort"]: str,
                self.NAME_OID_DICT["dot1dTpFdbAddress"]: str
            },
            node_count=6
        )

        snmp_results_indices = snmp_walk(
            fqdn=self.fqdn,
            credentials=f"{self.community_string}@{vlan_id}",
            oids={
                self.NAME_OID_DICT["dot1dBasePortIfIndex"]: str,
            },
        )

        snmp_results_names = snmp_walk(
            fqdn=self.fqdn,
            credentials=self.community_string,
            oids={
                self.NAME_OID_DICT["ifName"]: str,
            },
        )

        for index, mac in snmp_results_vlan_macs[self.NAME_OID_DICT["dot1dTpFdbAddress"]].items():

            port_id = snmp_results_vlan_macs[self.NAME_OID_DICT["dot1dTpFdbPort"]][index]
            index = snmp_results_indices[self.NAME_OID_DICT["dot1dBasePortIfIndex"]].get(port_id)
            if index == if_index:
                splitted_mac = mac.upper()[2:]
                results.append(":".join([splitted_mac[i:i+2] for i in range(0, len(splitted_mac), 2)]))

        return results, snmp_results_names[self.NAME_OID_DICT["ifName"]].get(if_index)


    def load_interfaces_real(self) -> None:
        oids = {
            self.NAME_OID_DICT["ifName"]       : str, 
            self.NAME_OID_DICT["ifType"]       : int, 
            self.NAME_OID_DICT["ifAlias"]      : str,
            self.NAME_OID_DICT["ifAdminStatus"]: int, 
            self.NAME_OID_DICT["ifOperStatus"] : int, 
            self.NAME_OID_DICT["vmVlan"]       : int, 
            self.NAME_OID_DICT["cpsIfMaxSecureMacAddr"]  : int, 
            self.NAME_OID_DICT["cpsIfPortSecurityEnable"]: int, 
            self.NAME_OID_DICT["ifTrunk"]: int,
        }

        snmp_results = snmp_walk(
            fqdn=self.fqdn,
            credentials=self.community_string,
            oids=oids
        )
        snmp_results_poe = snmp_walk(
            fqdn=self.fqdn,
            credentials=self.community_string,
            oids={
                self.NAME_OID_DICT["cpeExtPsePortEntry"]: int
            }, 
            node_count=2
        )
        snmp_results.update(snmp_results_poe)

        for if_index, if_name in snmp_results[self.NAME_OID_DICT["ifName"]].items():
            port_label = if_name.split("/")
            poe = ""
            if len(port_label) == 3:
                fst, second = port_label[0][2:], port_label[-1]
                poe = snmp_results[self.NAME_OID_DICT["cpeExtPsePortEntry"]].get(f"{fst}.{second}", "")

            obj_kwargs = {
                "if_index": if_index,
                "if_name": if_name,
                "if_vlan": snmp_results[self.NAME_OID_DICT["ifType"]].get(if_index),
                "if_description": snmp_results[self.NAME_OID_DICT["ifAlias"]].get(if_index),
                "if_admin_status": snmp_results[self.NAME_OID_DICT["ifAdminStatus"]].get(if_index),
                "if_oper_status": snmp_results[self.NAME_OID_DICT["ifOperStatus"]].get(if_index),
                "if_vlan": snmp_results[self.NAME_OID_DICT["vmVlan"]].get(if_index),
                "if_trunk": snmp_results[self.NAME_OID_DICT["ifTrunk"]].get(if_index),
                "if_type": snmp_results[self.NAME_OID_DICT["ifType"]].get(if_index),
                "if_ps_enable": snmp_results[self.NAME_OID_DICT["cpsIfPortSecurityEnable"]].get(if_index),
                "if_ps_max": snmp_results[self.NAME_OID_DICT["cpsIfMaxSecureMacAddr"]].get(if_index),
                "if_poe": poe,
            }
            self.load_object(Interface, if_index, self.interfaces, obj_kwargs)
        
        self._filter_interfaces()

    def load_interfaces_changes(self, data: Dict[str, List[str]]) -> Tuple[List[str], List[str]]:
        if not self.check_interfaces_data(data):
            raise RuntimeError("Data integrity error.")

        success: List[Dict[str, str]] = []
        errors: List[Dict[str, str]] = []
        changes: List[Dict[str, str]] = []

        for index, if_index in enumerate(data["if_index"]):
            interface = self.interfaces.get(if_index)
            if interface is None or interface.if_enabled is False:
                continue

            change_vlan = data["if_vlan"][index]
            if change_vlan != "" and change_vlan.isdigit() and int(change_vlan) != interface.if_vlan:
                if change_vlan not in self.vlans or not self.vlans[change_vlan].vlan_enabled:
                    errors.append({"interface": interface.if_name, "component": "vlan", "before": interface.if_vlan, "after": change_vlan})
                else:
                    changes.append((if_index, "if_vlan", "vlan", interface.if_vlan, self.NAME_OID_DICT["vmVlan"], int(change_vlan)))

            change_description = data["if_description"][index]
            if change_description != interface.if_description and change_description != "":
                if not bool(re.search(r'^[\x00-\x7F]+$', change_description)):
                    errors.append({"interface": interface.if_name, "component": "description", "before": interface.if_description, "after": change_description})
                else:
                    changes.append((if_index, "if_description", "description", interface.if_description, self.NAME_OID_DICT["ifAlias"], change_description))

            change_admin_status = data["if_admin_status"][index]
            if change_admin_status != "" and change_admin_status.isdigit() and int(change_admin_status) != interface.if_admin_status:
                if change_admin_status not in ["1", "2"]:
                    errors.append({"interface": interface.if_name, "component": "admin status", "before": interface.if_admin_status, "after": change_admin_status})
                else:
                    changes.append((if_index, "if_admin_status", "admin status", interface.if_admin_status, self.NAME_OID_DICT["ifAdminStatus"], int(change_admin_status)))

            change_if_ps_max = str(data["if_ps_max"][index])
            if change_if_ps_max != "" and change_if_ps_max.isdigit() and int(change_if_ps_max) != interface.if_ps_max:
                if interface.if_ps_enable == 2 or not change_if_ps_max.isdigit() or int(change_if_ps_max) > self.portsec_max:
                    errors.append({"interface": interface.if_name, "component": "portsec", "before": interface.if_ps_max, "after": change_if_ps_max})
                else:
                    changes.append((if_index, "if_ps_max", "portsec max", interface.if_ps_max, self.NAME_OID_DICT["cpsIfMaxSecureMacAddr"], int(change_if_ps_max)))

        self.set_changes(changes, success, errors)
        if len(success) > 0:
            self.save_running_config(success, errors)
        return success, errors

    def set_changes(self, changes: List[Dict[str, str]], success: RESULT, errors: RESULT) -> None:
        
        for if_index, if_attr, if_verbose, if_value_before, oid_root, value in changes:
            oid = f"{oid_root}.{if_index}"
            change = {
                    "interface": self.interfaces[if_index].if_name,
                    "component": if_verbose,
                    "before": if_value_before,
                    "after": value
                }
            try:
                response = snmp_set(
                    fqdn=self.fqdn,
                    oid=oid,
                    value=value,
                    credentials=self.community_string,
                )
                self.interfaces[if_index].__setattr__(if_attr, value)
                success.append(change)
            except RuntimeError:
                errors.append(change)

    def save_running_config(self, success: RESULT, errors: RESULT) -> None:
        change = {
                "interface": "",
                "component": "save running config",
                "before": "",
                "after": ""
            }
        try :
            response = snmp_set(
                fqdn=self.fqdn,
                credentials=self.community_string,
                value=1,
                oid=self.NAME_OID_DICT["writeMem"]
            )
            success.append(change)
        except RuntimeError:
            errors.append(change)
        