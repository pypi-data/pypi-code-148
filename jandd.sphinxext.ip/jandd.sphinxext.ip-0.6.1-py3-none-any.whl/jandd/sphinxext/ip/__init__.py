# -*- coding: utf-8 -*-
"""
    jandd.sphinxext.ip
    ~~~~~~~~~~~~~~~~~~

    The IP domain.

    :copyright: Copyright (c) Jan Dittberner
    :license: GPLv3+, see COPYING file for details.
"""
__version__ = "0.6.1"

import ipaddress
from collections import defaultdict
from typing import Iterable, List, Optional, Tuple, Any, cast

from docutils import nodes
from docutils.nodes import Element
from sphinx import addnodes
from sphinx.addnodes import desc_signature, pending_xref
from sphinx.application import Sphinx
from sphinx.builders import Builder
from sphinx.directives import ObjectDescription, T
from sphinx.domains import Domain, ObjType
from sphinx.environment import BuildEnvironment
from sphinx.errors import NoUri
from sphinx.locale import _
from sphinx.roles import XRefRole
from sphinx.util import logging
from sphinx.util.nodes import make_refnode

logger = logging.getLogger(__name__)


class ip_range(nodes.General, nodes.Element):
    pass


class IPRangeDirective(ObjectDescription):
    """A custom directive that describes an IP address range."""

    has_content = True
    required_arguments = 1
    title_prefix: str = ""
    range_spec: str = ""

    def get_title_prefix(self) -> str:
        return self.title_prefix

    def handle_signature(self, sig: str, sig_node: desc_signature) -> str:
        sig_node += addnodes.desc_name(
            text="{} {}".format(self.get_title_prefix(), sig)
        )
        self.range_spec = sig
        return sig

    def transform_content(self, content_node: addnodes.desc_content) -> None:
        ip_range_node = ip_range()
        ip_range_node["range_spec"] = self.range_spec
        content_node += ip_range_node


class IPV4RangeDirective(IPRangeDirective):
    title_prefix = _("IPv4 range")

    def add_target_and_index(self, name: T, sig: str, sig_node: desc_signature) -> None:
        anchor = "ip-ipv4range-{0}".format(sig)
        sig_node["ids"].append(anchor)
        ips = cast(IPDomain, self.env.get_domain("ip"))
        ips.add_ip4_range(sig)
        idx_text = "{}; {}".format(self.title_prefix, name)
        self.indexnode["entries"] = [
            ("single", idx_text, anchor, "", None),
        ]


class IPV6RangeDirective(IPRangeDirective):
    title_prefix = _("IPv6 range")

    def add_target_and_index(self, name: T, sig: str, signode: desc_signature) -> None:
        anchor = "ip-ipv6range-{0}".format(sig)
        signode["ids"].append(anchor)
        ips = cast(IPDomain, self.env.get_domain("ip"))
        ips.add_ip6_range(sig)
        idx_text = "{}; {}".format(self.title_prefix, name)
        self.indexnode["entries"] = [
            ("single", idx_text, anchor, "", None),
        ]


class IPXRefRole(XRefRole):
    def __init__(self, index_type):
        self.index_type = index_type
        super().__init__()

    def process_link(
        self,
        env: BuildEnvironment,
        refnode: nodes.Element,
        has_explicit_title: bool,
        title: str,
        target: str,
    ) -> Tuple[str, str]:
        refnode.attributes.update(env.ref_context)

        ips = cast(IPDomain, env.get_domain("ip"))
        if refnode["reftype"] == "v4":
            ips.add_ip4_address_reference(target)
        elif refnode["reftype"] == "v6":
            ips.add_ip6_address_reference(target)
        elif refnode["reftype"] == "v4range":
            ips.add_ip4_range_reference(target)
        elif refnode["reftype"] == "v6range":
            ips.add_ip6_range_reference(target)

        return title, target

    def result_nodes(
        self,
        document: nodes.document,
        env: BuildEnvironment,
        node: nodes.Element,
        is_ref: bool,
    ) -> Tuple[List[nodes.Node], List[nodes.system_message]]:
        node_list, message = super().result_nodes(document, env, node, is_ref)

        ip = cast(IPDomain, env.get_domain("ip"))
        if self.reftype in ["v4", "v6"] and self.target not in ip.data["ip_dict"]:
            return node_list, message
        if (
            self.reftype in ["v4range", "v6range"]
            and self.target not in ip.data["ranges"]
        ):
            return node_list, message

        index_node = addnodes.index()
        target_id = "ip-{}-{}".format(self.reftype, env.new_serialno("index"))

        if self.reftype in ["v4", "v6"]:
            ip.add_ip_address_anchor(self.target, env.docname, target_id)

        target_node = nodes.target("", "", ids=[target_id])
        doc_title = next(d for d in document.findall(nodes.title)).astext()

        node_text = node.astext()

        idx_text = "{}; {}".format(node_text, doc_title)
        idx_text_2 = "{}; {}".format(self.index_type, node.astext())
        index_node["entries"] = [
            ("single", idx_text, target_id, "", None),
            ("single", idx_text_2, target_id, "", None),
        ]

        node_list.insert(0, target_node)
        node_list.insert(0, index_node)
        return node_list, message


class IPDomain(Domain):
    """Custom domain for IP addresses and ranges."""

    def merge_domaindata(self, docnames: list[str], otherdata: dict) -> None:
        # TODO: implement merge_domaindata
        print(
            f"merge_domaindata called for docnames: {docnames} with otherdata: {otherdata}"
        )

    def resolve_any_xref(
        self,
        env: BuildEnvironment,
        fromdocname: str,
        builder: Builder,
        target: str,
        node: pending_xref,
        contnode: Element,
    ) -> list[tuple[str, Element]]:
        # TODO: implement resolve_any_xref
        print("resolve_any_xref called")
        return []

    name = "ip"
    label = "IP addresses and ranges."

    object_types = {
        "v4": ObjType(_("v4"), "v4", "obj"),
        "v6": ObjType(_("v6"), "v6", "obj"),
        "v4range": ObjType(_("v4range"), "v4range", "obj"),
        "v6range": ObjType(_("v6range"), "v6range", "obj"),
    }

    directives = {
        "v4range": IPV4RangeDirective,
        "v6range": IPV6RangeDirective,
    }

    roles = {
        "v4": IPXRefRole("IPv4 address"),
        "v6": IPXRefRole("IPv6 address"),
        "v4range": IPXRefRole("IPv4 range"),
        "v6range": IPXRefRole("IPv6 range"),
    }

    initial_data = {
        "range_nodes": [],
        "ip_refs": defaultdict(list),
        "range_refs": [],
        "ranges": defaultdict(list),
        "ip_dict": {},
    }

    def get_full_qualified_name(self, node: nodes.Element) -> Optional[str]:
        return "{}.{}".format("ip", node)

    def get_objects(self) -> Iterable[Tuple[str, str, str, str, str, int]]:
        for obj in self.data["range_nodes"]:
            yield obj

    def add_ip4_range(self, sig: str):
        logger.debug("add_ip4_range: %s", sig)
        self._add_ip_range("v4", sig)

    def add_ip6_range(self, sig: str):
        logger.debug("add_ip6_range: %s", sig)
        self._add_ip_range("v6", sig)

    def _add_ip_range(self, family: str, sig: str):
        name = "ip{}range.{}".format(family, sig)
        anchor = "ip-ip{}range-{}".format(family, sig)
        try:
            new_ip_range = ipaddress.ip_network(sig)
            self.data["range_nodes"].append(
                (name, family, sig, self.env.docname, anchor, 0)
            )
            self.data["ranges"][sig].append((new_ip_range, self.env.docname, anchor))
        except ValueError as e:
            logger.error("invalid ip range address '%s': %s", sig, e)

    def add_ip4_address_reference(self, ip_address: str):
        logger.debug("add_ip4_address_reference")
        self._add_ip_address_reference("v4", ip_address)

    def add_ip6_address_reference(self, ip_address: str):
        logger.debug("add_ip4_address_reference")
        self._add_ip_address_reference("v6", ip_address)

    def _add_ip_address_reference(self, family, sig):
        try:
            self.data["ip_dict"][sig] = ipaddress.ip_address(sig)
        except ValueError as e:
            logger.error("invalid ip address '%s': %s", sig, e)

    def add_ip_address_anchor(self, sig, docname, anchor):
        try:
            ip = ipaddress.ip_address(sig)
            self.data["ip_refs"][sig].append((ip, docname, anchor))
        except ValueError as e:
            logger.error("invalid ip address '%s': %s", sig, e)

    def add_ip4_range_reference(self, ip_range: str):
        logger.debug("add_ip4_range_reference")
        self._add_ip_range_reference("v4", ip_range)

    def add_ip6_range_reference(self, ip_range: str):
        logger.debug("add_ip6_address_reference")
        self._add_ip_range_reference("v6", ip_range)

    def _add_ip_range_reference(self, family, sig):
        name = "iprange{}.{}".format(family, sig)
        anchor = "ip-iprange{}-{}".format(family, sig)
        try:
            ip_range = ipaddress.ip_network(sig)
            self.data["range_refs"].append(
                (
                    name,
                    sig,
                    "IP{} range".format(family),
                    str(ip_range),
                    self.env.docname,
                    anchor,
                    0,
                )
            )
        except ValueError as e:
            logger.error("invalid ip range '%s': %s", sig, e)

    def resolve_xref(
        self,
        env: BuildEnvironment,
        fromdocname: str,
        builder: Builder,
        typ: str,
        target: str,
        node: pending_xref,
        contnode: nodes.Element,
    ) -> Optional[nodes.Element]:
        match = []

        def address_tuple(docname, anchor, ip_range: Any) -> Tuple[str, str, str]:
            return (
                docname,
                anchor,
                _("IPv{0} range {1}".format(ip_range.version, ip_range.compressed)),
            )

        if typ in ("v4", "v6"):
            # reference to IP range
            if target not in self.data["ip_dict"]:
                # invalid ip address
                raise NoUri(target)
            match = [
                address_tuple(docname, anchor, ip_range)
                for ip_range, docname, anchor in [
                    r
                    for range_nodes in self.data["ranges"].values()
                    for r in range_nodes
                ]
                if self.data["ip_dict"][target] in ip_range
            ]
        elif typ in ("v4range", "v6range"):
            if target in self.data["ranges"]:
                match = [
                    address_tuple(docname, anchor, ip_range)
                    for ip_range, docname, anchor in [
                        range_nodes for range_nodes in self.data["ranges"][target]
                    ]
                ]
        if len(match) > 0:
            todocname = match[0][0]
            targ = match[0][1]
            title = match[0][2]

            return make_refnode(builder, fromdocname, todocname, targ, contnode, title)
        else:
            logger.error("found no link target for %s", target)
        return None


def process_ip_nodes(app: Sphinx, doctree: nodes.Node, fromdocname: str):
    env = app.builder.env
    ips = env.get_domain(IPDomain.name)

    header = (_("IP address"), _("Used by"))
    column_widths = (2, 5)

    for node in doctree.findall(ip_range):
        content = []
        net = ipaddress.ip_network(node["range_spec"], strict=False)
        addresses = defaultdict(list)
        for ip_address_sig, refs in ips.data["ip_refs"].items():
            for ip_address, to_doc_name, anchor in refs:
                if ip_address in net:
                    addresses[ip_address_sig].append((ip_address, to_doc_name, anchor))
                    logger.debug(
                        "found %s in network %s on %s",
                        ip_address_sig,
                        net.compressed,
                        to_doc_name,
                    )
        if addresses:
            table = nodes.table()
            table.attributes["classes"].append("indextable")
            table.attributes["align"] = "left"

            tgroup = nodes.tgroup(cols=len(header))
            table += tgroup
            for column_width in column_widths:
                tgroup += nodes.colspec(colwidth=column_width)

            thead = nodes.thead()
            tgroup += thead
            thead += create_table_row([nodes.paragraph(text=label) for label in header])

            tbody = nodes.tbody()
            tgroup += tbody

            for ip_address_sig, ip_info in [
                (key, addresses[key]) for key in sorted(addresses, key=sort_by_ip)
            ]:
                para = nodes.paragraph()
                para += nodes.literal("", ip_info[0][0].compressed)

                ref_node = nodes.paragraph()
                ref_nodes = []
                referenced_docs = set()

                for item in ip_info:
                    ip_address, to_doc_name, anchor = item
                    if to_doc_name in referenced_docs:
                        continue
                    referenced_docs.add(to_doc_name)

                    title = env.titles[to_doc_name]
                    inner_node = nodes.Text(title.astext())
                    new_node = make_refnode(
                        app.builder,
                        fromdocname,
                        to_doc_name,
                        anchor,
                        inner_node,
                        title.astext(),
                    )

                    ref_nodes.append(new_node)
                for count in range(len(ref_nodes)):
                    ref_node.append(ref_nodes[count])
                    if count < len(ref_nodes) - 1:
                        ref_node.append(nodes.Text(", "))
                tbody += create_table_row([para, ref_node])
            content.append(table)
        else:
            para = nodes.paragraph(_("No IP addresses in this range"))
            content.append(para)

        node.replace_self(content)


def create_table_row(rowdata):
    row = nodes.row()
    for cell in rowdata:
        entry = nodes.entry()
        row += entry
        entry += cell
    return row


def sort_by_ip(item):
    return ipaddress.ip_address(item)


def setup(app: Sphinx):
    app.add_domain(IPDomain)
    app.connect("doctree-resolved", process_ip_nodes)
    return {
        "version": __version__,
        "env_version": 4,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
