import ipaddress as ipaddr
from typing import Dict, List

from schema import And, Optional, Or, Regex, Schema, SchemaError, Use

import spyctl.resources.fingerprints as spyctl_fprints
import spyctl.config.configs as cfgs
import spyctl.spyctl_lib as lib


class PortsSchema(Schema):
    def validate(self, data, **kwargs):
        val_schema = Schema(
            self.schema,
            self._error,
            self._ignore_extra_keys,
            self._name,
            self._description,
            self.as_reference,
        )
        rv = val_schema.validate(data, **kwargs)
        e = self._error
        for port in data:
            endport = port.get(lib.ENDPORT_FIELD)
            if endport is not None:
                if endport < port[lib.PORT_FIELD]:
                    message = (
                        f"{lib.ENDPORT_FIELD} {endport} should be greater than"
                        f" or equal to {lib.PORT_FIELD} {port[lib.PORT_FIELD]}"
                    )
                    raise SchemaError(message, e.format(port) if e else None)
        return rv


class IP_Block_Schema(Schema):
    def validate(self, data, **kwargs):
        val_schema = Schema(
            self.schema,
            self._error,
            self._ignore_extra_keys,
            self._name,
            self._description,
            self.as_reference,
        )
        rv = val_schema.validate(data, **kwargs)
        e = self._error
        if lib.EXCEPT_FIELD not in data[lib.IP_BLOCK_FIELD]:
            return rv
        cidr = data[lib.IP_BLOCK_FIELD][lib.CIDR_FIELD]
        try:
            network = ipaddr.IPv4Network(cidr)
        except ipaddr.AddressValueError:
            network = ipaddr.IPv6Network(cidr)

        for except_cidr in data[lib.IP_BLOCK_FIELD][lib.EXCEPT_FIELD]:
            try:
                except_net = ipaddr.IPv4Address(except_cidr)
            except ipaddr.AddressValueError:
                except_net = ipaddr.IPv6Address(except_cidr)
            try:
                if not network.supernet_of(except_net):
                    message = (
                        f"Except CIDR {except_cidr} must be a subnet of {cidr}"
                    )
                    raise SchemaError(message, e.format(data) if e else None)
            except TypeError:
                message = (
                    f"{except_cidr} and {cidr} must be the same IP version"
                )
                raise SchemaError(message, e.format(data) if e else None)
        return rv


class Spec_Schema(Schema):
    process_ids = set()

    def validate(self, data, **kwargs):
        val_schema = Schema(
            self.schema,
            self._error,
            self._ignore_extra_keys,
            self._name,
            self._description,
            self.as_reference,
        )
        rv = val_schema.validate(data, **kwargs)
        process_list = data.get(lib.PROC_POLICY_FIELD)
        self.__validate_unique_ids(process_list)
        ingress_list = data.get(lib.INGRESS_FIELD)
        self.__validate_network_processes(ingress_list)
        egress_list = data.get(lib.EGRESS_FIELD)
        self.__validate_network_processes(egress_list)
        return rv

    def __validate_unique_ids(self, process_list: List[Dict]):
        e = self._error
        for process_node in process_list:
            id = process_node[lib.ID_FIELD]
            if id in self.process_ids:
                message = (
                    f"Duplicate process ID detected {id}. All ids in"
                    f" the {lib.PROC_POLICY_FIELD} must be unique"
                )
                raise SchemaError(
                    message, e.format(process_list) if e else None
                )
            else:
                self.process_ids.add(id)
                if lib.CHILDREN_FIELD in process_node:
                    self.__validate_unique_ids(
                        process_node[lib.CHILDREN_FIELD]
                    )

    def __validate_network_processes(self, net_node_list: List[Dict]):
        e = self._error
        for net_node in net_node_list:
            processes = net_node[lib.PROCESSES_FIELD]
            for proc_id in processes:
                if proc_id not in self.process_ids:
                    message = (
                        f"Process id {proc_id} in {lib.NET_POLICY_FIELD} not"
                        f" found in {lib.PROC_POLICY_FIELD}."
                    )
                    raise SchemaError(
                        message, e.format(net_node) if e else None
                    )


class SpyderbatObjSchema(Schema):
    """A base schema class for fingerprints, baselines, and policies"""

    def validate(self, data, **kwargs):
        e = self._error
        val_schema = Schema(
            self.schema,
            self._error,
            self._ignore_extra_keys,
            self._name,
            self._description,
            self.as_reference,
        )
        rv = val_schema.validate(data, **kwargs)
        type = data[lib.METADATA_FIELD][lib.METADATA_TYPE_FIELD]
        spec = data[lib.SPEC_FIELD]
        if type == lib.POL_TYPE_CONT and lib.CONT_SELECTOR_FIELD not in spec:
            message = (
                f"Missing {lib.CONT_SELECTOR_FIELD} in {lib.SPEC_FIELD} field"
            )
            raise SchemaError(message, e.format(spec) if e else None)
        elif type == lib.POL_TYPE_SVC and lib.SVC_SELECTOR_FIELD not in spec:
            message = (
                f"Missing {lib.SVC_SELECTOR_FIELD} in {lib.SPEC_FIELD} field"
            )
            raise SchemaError(message, e.format(spec) if e else None)
        return rv


config_schema = Schema(
    {
        lib.API_FIELD: lib.API_VERSION,
        lib.KIND_FIELD: cfgs.CONFIG_KIND,
        cfgs.CONTEXTS_FIELD: [],
        cfgs.CURR_CONTEXT_FIELD: str,
    }
)

context_schema = Schema(
    {
        cfgs.CONTEXT_NAME_FIELD: str,
        cfgs.SECRET_FIELD: str,
        cfgs.CONTEXT_FIELD: {
            cfgs.ORG_FIELD: str,
            Optional(cfgs.CLUSTER_FIELD): Or(str, [str]),
            Optional(cfgs.MACHINES_FIELD): Or(str, [str]),
            Optional(cfgs.POD_FIELD): Or(str, [str]),
            Optional(cfgs.NAMESPACE_FIELD): Or(str, [str]),
            Optional(cfgs.CGROUP_FIELD): Or(str, [str]),
            Optional(cfgs.CONTAINER_NAME_FIELD): Or(str, [str]),
            Optional(cfgs.CONT_ID_FIELD): Or(str, [str]),
            Optional(cfgs.IMG_FIELD): Or(str, [str]),
            Optional(cfgs.IMGID_FIELD): Or(str, [str]),
        },
    }
)

ports_schema = PortsSchema(
    [
        {
            lib.PORT_FIELD: And(Use(int), lambda n: 0 <= n <= 65535),
            lib.PROTO_FIELD: And(
                "TCP", error="Only TCP ports are supported at this time"
            ),
            Optional(lib.ENDPORT_FIELD): And(
                Use(int), lambda n: 0 <= n <= 65535
            ),
        }
    ]
)


def validate_process_schema(data: list):
    return child_processes_schema.validate(data)


child_processes_schema = Schema(
    [
        {
            lib.NAME_FIELD: And(str, lambda x: len(x) > 0),
            lib.EXE_FIELD: [And(str, lambda x: len(x) > 0)],
            lib.ID_FIELD: And(str, lambda x: len(x) > 0),
            Optional(lib.EUSER_FIELD): And([str], lambda x: len(x) > 0),
            Optional(lib.LISTENING_SOCKETS): ports_schema,
            Optional(lib.CHILDREN_FIELD): validate_process_schema,
        }
    ]
)

process_policy_schema = Schema(
    [
        {
            lib.NAME_FIELD: And(str, lambda x: len(x) > 0),
            lib.EXE_FIELD: [And(str, lambda x: len(x) > 0)],
            lib.ID_FIELD: And(str, lambda x: len(x) > 0),
            lib.EUSER_FIELD: [And(str, lambda x: len(x) > 0)],
            Optional(lib.LISTENING_SOCKETS): ports_schema,
            Optional(lib.CHILDREN_FIELD): child_processes_schema,
        }
    ]
)

ip_block_schema = IP_Block_Schema(
    {
        lib.IP_BLOCK_FIELD: {
            lib.CIDR_FIELD: Or(ipaddr.IPv4Network, ipaddr.IPv6Network),
            Optional(lib.EXCEPT_FIELD): [
                Or(ipaddr.IPv4Network, ipaddr.IPv6Network)
            ],
        }
    }
)

dns_schema = Schema({lib.DNS_SELECTOR_FIELD: [And(str, lambda x: len(x) > 0)]})

ingress_schema = Schema(
    [
        {
            lib.TO_FIELD: [Or(dns_schema, ip_block_schema)],
            lib.PROCESSES_FIELD: [And(str, lambda x: len(x) > 0)],
            lib.PORTS_FIELD: ports_schema,
        }
    ]
)

egress_schema = Schema(
    [
        {
            lib.FROM_FIELD: [Or(dns_schema, ip_block_schema)],
            lib.PROCESSES_FIELD: [And(str, lambda x: len(x) > 0)],
            lib.PORTS_FIELD: ports_schema,
        }
    ]
)

svc_selector_schema = Schema(
    {lib.CGROUP_FIELD: And(str, lambda x: len(x) > 0)}
)

container_selector_schema = Schema(
    And(
        {
            Optional(lib.IMAGE_FIELD): And(str, lambda x: len(x) > 0),
            Optional(lib.IMAGEID_FIELD): And(str, lambda x: len(x) > 0),
            Optional(lib.CONT_NAME_FIELD): And(str, lambda x: len(x) > 0),
            Optional(lib.CONT_ID_FIELD): And(str, lambda x: len(x) > 0),
        },
        lambda d: len(d) > 0,
    )
)

# TODO: Update machine selector
machine_selector_schema = Schema({}, ignore_extra_keys=True)

match_labels_schema = Schema({lib.MATCH_LABELS_FIELD: {str: str}})

pod_selector_schema = match_labels_schema
namespace_selector_schema = match_labels_schema

baseline_spec_schema = Schema(
    {
        Optional(lib.ENABLED_FIELD): bool,
        Optional(lib.CONT_SELECTOR_FIELD): container_selector_schema,
        Optional(lib.SVC_SELECTOR_FIELD): svc_selector_schema,
        Optional(lib.MACHINE_SELECTOR_FIELD): machine_selector_schema,
        Optional(lib.POD_SELECTOR_FIELD): pod_selector_schema,
        Optional(lib.NAMESPACE_SELECTOR_FIELD): namespace_selector_schema,
        lib.PROC_POLICY_FIELD: process_policy_schema,
        lib.NET_POLICY_FIELD: {
            lib.INGRESS_FIELD: ingress_schema,
            lib.EGRESS_FIELD: egress_schema,
        },
    }
)

# TODO: Update response actions format
# TODO: Create schemas for various response actions
policy_spec_schema = Schema(
    {
        Optional(lib.ENABLED_FIELD): bool,
        Optional(lib.CONT_SELECTOR_FIELD): container_selector_schema,
        Optional(lib.SVC_SELECTOR_FIELD): svc_selector_schema,
        Optional(lib.MACHINE_SELECTOR_FIELD): machine_selector_schema,
        Optional(lib.POD_SELECTOR_FIELD): pod_selector_schema,
        Optional(lib.NAMESPACE_SELECTOR_FIELD): namespace_selector_schema,
        lib.PROC_POLICY_FIELD: process_policy_schema,
        lib.NET_POLICY_FIELD: {
            lib.INGRESS_FIELD: ingress_schema,
            lib.EGRESS_FIELD: egress_schema,
        },
        lib.RESPONSE_FIELD: {
            lib.RESP_DEFAULT_FIELD: Or([{str: str}], {str: str}),
            lib.RESP_ACTIONS_FIELD: [{str: str}],
        },
    }
)

# TODO: Add type to fingerprint group metadata
fprint_group_metadata_schema = Schema(
    {
        Optional(lib.IMAGE_FIELD): str,
        Optional(lib.IMAGEID_FIELD): str,
        Optional(lib.CGROUP_FIELD): str,
        Optional(lib.FIRST_TIMESTAMP_FIELD): Or(int, float),
        Optional(lib.LATEST_TIMESTAMP_FIELD): Or(int, float),
    },
    ignore_extra_keys=True,
)

fprint_metadata_schema = Schema(
    {
        lib.METADATA_NAME_FIELD: And(str, lambda x: len(x) > 0),
        lib.METADATA_TYPE_FIELD: Or(
            lib.POL_TYPE_CONT,
            lib.POL_TYPE_SVC,
            error=(
                f"Fingerprint type must be {lib.POL_TYPE_CONT} or"
                f" {lib.POL_TYPE_SVC}"
            ),
        ),
        Optional(lib.FIRST_TIMESTAMP_FIELD): Or(int, float),
        Optional(lib.LATEST_TIMESTAMP_FIELD): Or(
            int, float, spyctl_fprints.NOT_AVAILABLE
        ),
    },
    ignore_extra_keys=True,
)

baseline_metadata_schema = Schema(
    {
        lib.METADATA_NAME_FIELD: And(str, lambda x: len(x) > 0),
        lib.METADATA_TYPE_FIELD: Or(
            lib.POL_TYPE_CONT,
            lib.POL_TYPE_SVC,
            error=(
                f"Fingerprint type must be {lib.POL_TYPE_CONT} or"
                f" {lib.POL_TYPE_SVC}"
            ),
        ),
        Optional(lib.LATEST_TIMESTAMP_FIELD): Or(
            int, float, spyctl_fprints.NOT_AVAILABLE
        ),
    },
)

policy_metadata_schema = Schema(
    {
        lib.METADATA_NAME_FIELD: And(str, lambda x: len(x) > 0),
        lib.METADATA_TYPE_FIELD: Or(
            lib.POL_TYPE_CONT,
            lib.POL_TYPE_SVC,
            error=(
                f"Fingerprint type must be {lib.POL_TYPE_CONT} or"
                f" {lib.POL_TYPE_SVC}"
            ),
        ),
        Optional(lib.METADATA_CREATE_TIME): Or(str, int, float),
        Optional(lib.LATEST_TIMESTAMP_FIELD): Or(
            int, float, spyctl_fprints.NOT_AVAILABLE
        ),
        Optional(lib.METADATA_UID_FIELD): str,
    },
)

fprint_schema = SpyderbatObjSchema(
    {
        lib.API_FIELD: lib.API_VERSION,
        lib.KIND_FIELD: lib.FPRINT_KIND,
        lib.METADATA_FIELD: fprint_group_metadata_schema,
    }
)

fprint_group_schema = Schema({})
