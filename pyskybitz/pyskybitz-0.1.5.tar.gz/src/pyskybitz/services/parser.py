"""Parser class to parse data coming from APIs."""
import os
import re
import sys

from lxml import etree as etree_

from pyskybitz.models.base import SkyBitz

TagPattern = re.compile(r"({.*})?(.*)")
CDATAPattern = re.compile(r"<!\[CDATA\[.*?\]\]>", re.DOTALL)
GDSClassesMapping = {}
TagNamePrefix = ""
SaveElementTreeNode = True
GenerateDSNamespaceDefs = {}
GenerateDSNamespaceTypePrefixes = {}


class GdsCollector:
    """GdsCollector class, obviously."""

    def __init__(self, messages=None):
        """Initialize Gds Collector instance."""
        if messages is None:
            self.messages = []
        else:
            self.messages = messages

    def add_message(self, msg):
        """Add new message."""
        self.messages.append(msg)

    def get_messages(self):
        """Get all messages."""
        return self.messages

    def clear_messages(self):
        """Empty the list containing all messages."""
        self.messages = []

    def print_messages(self):
        """Print out all messages."""
        for msg in self.messages:
            print("Warning: {}".format(msg))

    def write_messages(self, outstream):
        """Write all messages to source."""
        for msg in self.messages:
            outstream.write("Warning: {}\n".format(msg))


class Parser:
    """Parser class to execute all parsing actions."""

    @staticmethod
    def parse_xml(infile, parser=None, **kwargs):
        """Parse the given XML file."""
        if parser is None:
            # Use the lxml ElementTree compatible parser so that, e.g.,
            #   we ignore comments.
            try:
                parser = etree_.ETCompatXMLParser()
            except AttributeError:
                # fallback to xml.etree
                parser = etree_.XMLParser()
        try:
            if isinstance(infile, os.PathLike):
                infile = os.path.join(infile)
        except AttributeError:
            pass
        doc = etree_.parse(infile, parser=parser, **kwargs)
        return doc

    @staticmethod
    def parse_xml_string(in_string, parser=None, **kwargs):
        """Parse the given XML string."""
        if parser is None:
            # Use the lxml ElementTree compatible parser so that, e.g.,
            #   we ignore comments.
            try:
                parser = etree_.ETCompatXMLParser()
            except AttributeError:
                # fallback to xml.etree
                parser = etree_.XMLParser()
        element = etree_.fromstring(in_string, parser=parser, **kwargs)
        return element

    @staticmethod
    def get_root_tag(node):
        """Get the root tag."""
        tag = TagPattern.match(node.tag).groups()[-1]
        prefix_tag = TagNamePrefix + tag
        root_class = GDSClassesMapping.get(prefix_tag)
        if root_class is None:
            root_class = globals().get(prefix_tag)
        return tag, root_class

    @staticmethod
    def get_required_ns_prefix_defs(root_node):
        """
        Get all name space prefix definitions required in this XML doc.

        :param root_node: Root node.
        :return: A dictionary of definitions and a char string of definitions.
        """
        ns_map = {
            prefix: uri
            for node in root_node.iter()
            for (prefix, uri) in node.nsmap.items()
            if prefix is not None
        }
        namespace_defs = " ".join(
            ['xmlns:{}="{}"'.format(prefix, uri) for prefix, uri in ns_map.items()]
        )
        return ns_map, namespace_defs

    def parse(self, in_file_name, silence=False, print_warnings=True):
        """Parse the given file."""
        global CapturedNsMap
        gds_collector = GdsCollector()
        parser = None
        doc = self.parse_xml(in_file_name, parser)
        root_node = doc.getroot()
        root_tag, root_class = self.get_root_tag(root_node)
        if root_class is None:
            root_tag = "skybitz"
            root_class = SkyBitz
        root_obj = root_class.factory()
        root_obj.build(root_node, gds_collector_=gds_collector)
        CapturedNsMap, namespace_defs = self.get_required_ns_prefix_defs(root_node)
        if not silence:
            sys.stdout.write('<?xml version="1.0" ?>\n')
            root_obj.export(
                sys.stdout,
                0,
                name_=root_tag,
                namespacedef_=namespace_defs,
                pretty_print=True,
            )
        if print_warnings and len(gds_collector.get_messages()) > 0:
            separator = ("-" * 50) + "\n"
            sys.stderr.write(separator)
            sys.stderr.write(
                "----- Warnings -- count: {} -----\n".format(
                    len(gds_collector.get_messages()),
                )
            )
            gds_collector.write_messages(sys.stderr)
            sys.stderr.write(separator)
        return root_obj

    def parse_etree(
        self,
        in_file_name,
        silence=False,
        print_warnings=True,
        mapping=None,
        reverse_mapping=None,
        nsmap=None,
    ):
        """Parse the given file and return tuple of root_obj, root_element, mapping, reverse_node_mapping."""
        parser = None
        doc = self.parse_xml(in_file_name, parser)
        gds_collector = GdsCollector()
        root_node = doc.getroot()
        root_tag, root_class = self.get_root_tag(root_node)
        if root_class is None:
            root_tag = "skybitz"
            root_class = SkyBitz
        root_obj = root_class.factory()
        root_obj.build(root_node, gds_collector_=gds_collector)
        if mapping is None:
            mapping = {}
        if reverse_mapping is None:
            reverse_mapping = {}
        root_element = root_obj.to_etree(
            None,
            name_=root_tag,
            mapping_=mapping,
            reverse_mapping_=reverse_mapping,
            nsmap_=nsmap,
        )
        reverse_node_mapping = root_obj.gds_reverse_node_mapping(mapping)
        # Enable Python to collect the space used by the DOM.
        if not SaveElementTreeNode:
            doc = None
            root_node = None
        if not silence:
            content = etree_.tostring(
                root_element, pretty_print=True, xml_declaration=True, encoding="utf-8"
            )
            sys.stdout.write(str(content))
            sys.stdout.write("\n")
        if print_warnings and len(gds_collector.get_messages()) > 0:
            separator = ("-" * 50) + "\n"
            sys.stderr.write(separator)
            sys.stderr.write(
                "----- Warnings -- count: {} -----\n".format(
                    len(gds_collector.get_messages()),
                )
            )
            gds_collector.write_messages(sys.stderr)
            sys.stderr.write(separator)
        return root_obj, root_element, mapping, reverse_node_mapping

    def parse_string(self, in_string, silence=False, print_warnings=True):
        """
        Parse a string, create the object tree, and export it.

        :param in_string:A string. This XML fragment should not start with an XML declaration containing an encoding.
        :param silence: A boolean. If False, export the object.
        :return: The root object in the tree.
        """
        if isinstance(in_string, str):
            in_string = in_string.encode("utf8")
        parser = None
        root_node = self.parse_xml_string(in_string, parser)
        gds_collector = GdsCollector()
        root_tag, root_class = self.get_root_tag(root_node)
        if root_class is None:
            root_tag = "skybitz"
            root_class = SkyBitz
        root_obj = root_class.factory()
        root_obj.build(root_node, gds_collector_=gds_collector)
        if not silence:
            sys.stdout.write('<?xml version="1.0" ?>\n')
            root_obj.export(
                sys.stdout,
                0,
                name_=root_tag,
                namespacedef_='xmlns:t="http://www.w3.org/namespace/"',
            )
        if print_warnings and len(gds_collector.get_messages()) > 0:
            separator = ("-" * 50) + "\n"
            sys.stderr.write(separator)
            sys.stderr.write(
                "----- Warnings -- count: {} -----\n".format(
                    len(gds_collector.get_messages()),
                )
            )
            gds_collector.write_messages(sys.stderr)
            sys.stderr.write(separator)
        return root_obj

    def parse_literal(self, in_file_name, silence=False, print_warnings=True):
        """Parse the given file."""
        parser = None
        doc = self.parse_xml(in_file_name, parser)
        gds_collector = GdsCollector()
        root_node = doc.getroot()
        root_tag, root_class = self.get_root_tag(root_node)
        if root_class is None:
            root_tag = "skybitz"
            root_class = SkyBitz
        root_obj = root_class.factory()
        root_obj.build(root_node, gds_collector_=gds_collector)
        # Enable Python to collect the space used by the DOM.
        if not SaveElementTreeNode:
            doc = None
            root_node = None
        if not silence:
            sys.stdout.write("#from models import *\n\n")
            sys.stdout.write("import models as model_\n\n")
            sys.stdout.write("rootObj = model_.rootClass(\n")
            root_obj.exportLiteral(sys.stdout, 0, name_=root_tag)
            sys.stdout.write(")\n")
        if print_warnings and len(gds_collector.get_messages()) > 0:
            separator = ("-" * 50) + "\n"
            sys.stderr.write(separator)
            sys.stderr.write(
                "----- Warnings -- count: {} -----\n".format(
                    len(gds_collector.get_messages()),
                )
            )
            gds_collector.write_messages(sys.stderr)
            sys.stderr.write(separator)
        return root_obj
