from pysnmp import hlapi
from pysnmp.hlapi import OctetString, Integer
from typing import Dict, Union, Tuple

SNMPValue = Union[str, int]


def snmp_get(fqdn: str, 
    oid: Tuple[str, SNMPValue], 
    credentials: str, 
    port: int=161,
    engine=hlapi.SnmpEngine(), 
    context=hlapi.ContextData(),
    node_count: int=1
) -> Tuple[str, SNMPValue]:
    handler = hlapi.getCmd(
        engine,
        hlapi.CommunityData(credentials),
        hlapi.UdpTransportTarget((fqdn, port), timeout=5, retries=3),
        context,
        hlapi.ObjectType(hlapi.ObjectIdentity(oid)),
        lookupMib=False,
        lexicographicMode=False
    )
    try:
        error_indication, error_status, error_index, var_binds = next(handler)
    except StopIteration:
        raise RuntimeError("Got SNMP error: No Value.")

    if error_indication or error_status or error_index:
        raise RuntimeError(f"Got SNMP error ({oid}): {error_indication or error_status or error_index}")

    for var_bind in var_binds:
        oid, value = [x.prettyPrint() for x in var_bind]
        splitted_oid = oid.split(".")
        snmp_root = ".".join(splitted_oid[:-node_count])
        snmp_node = ".".join(splitted_oid[-node_count:])
        return snmp_root, snmp_node, value

    raise RuntimeError(f"Got SNMP error ({oid}): No Value.")


def snmp_walk(
    fqdn: str, 
    oids: Dict[str, SNMPValue], 
    credentials: str, 
    port: int=161,
    engine=hlapi.SnmpEngine(), 
    context=hlapi.ContextData(),
    node_count: int=1
) -> Dict[str, Dict[str, SNMPValue]]:
    handler = hlapi.nextCmd(
        engine,
        hlapi.CommunityData(credentials),
        hlapi.UdpTransportTarget((fqdn, port), timeout=5, retries=3),
        context,
        *[hlapi.ObjectType(hlapi.ObjectIdentity(oid)) for oid in oids],
        lookupMib=False,
        lexicographicMode=False
    )

    snmp_result = {oid: {} for oid in oids}
    for error_indication, error_status, error_index, var_binds in handler:
        if error_indication or error_status or error_index:
            raise RuntimeError(f"Got SNMP error (walk): {error_indication or error_status or error_index}")
            
        for var_bind in var_binds:
            oid, value = [x.prettyPrint() for x in var_bind]
            if value == "No more variables left in this MIB View":
                continue
            splitted_oid = oid.split(".")
            snmp_root = ".".join(splitted_oid[:-node_count])
            snmp_node = ".".join(splitted_oid[-node_count:])
            snmp_result[snmp_root][snmp_node] = oids[snmp_root](value)
    
    return snmp_result


def snmp_set(
    fqdn: str, 
    oid: str,
    value: SNMPValue,
    credentials: str, 
    port: int=161,
    engine=hlapi.SnmpEngine(), 
    context=hlapi.ContextData(),
    node_count: int=1
) -> None:
    value = Integer(value) if isinstance(value, int) else OctetString(value)
    handler = hlapi.setCmd(
        engine,
        hlapi.CommunityData(credentials),
        hlapi.UdpTransportTarget((fqdn, port), timeout=5, retries=3),
        context,
        hlapi.ObjectType(hlapi.ObjectIdentity(oid), value),
        lookupMib=False
    )
    try:
        error_indication, error_status, error_index, var_binds = next(handler)
    except StopIteration:
        raise RuntimeError("Got SNMP error: No value.")

    if error_indication or error_status or error_index:
        raise RuntimeError(f"Got SNMP error: {error_indication or error_status or error_index}")
    
    for var_bind in var_binds:
        oid, value = [x.prettyPrint() for x in var_bind]
        splitted_oid = oid.split(".")
        snmp_root = ".".join(splitted_oid[:-node_count])
        snmp_node = ".".join(splitted_oid[-node_count:])
        return snmp_root, snmp_node, value

    raise RuntimeError("Got SNMP error: No Value.")
