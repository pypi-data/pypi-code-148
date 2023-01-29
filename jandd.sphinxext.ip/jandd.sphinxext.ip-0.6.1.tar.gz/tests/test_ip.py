# -*- coding: utf-8 -*-
import shutil
import unittest
from io import StringIO

from .util import SphinxTestApplication, test_root

IP4_ADDRESSES = ["127.0.0.1", "192.168.0.1"]
IP6_ADDRESSES = ["::1", "2001:dead:beef::1"]
IP4_RANGES = ["172.16.0.0/24", "192.168.0.0/24"]
IP6_RANGES = ["2001:dead:beef::/64", "2001:dada:b001::/64"]


class TestIPExtension(unittest.TestCase):
    def setUp(self):
        if not (test_root / "_static").exists():
            (test_root / "_static").mkdir()
        self.feed_warnfile = StringIO()
        self.app = SphinxTestApplication(
            buildername="html", warning=self.feed_warnfile, cleanenv=True
        )
        self.app.build(force_all=True, filenames=[])

    def tearDown(self):
        self.app.cleanup()
        shutil.rmtree((test_root / "_build"))

    def test_ip_domaindata(self):
        self.assertIn("ip", self.app.env.domaindata)
        ipdomdata = self.app.env.domaindata["ip"]
        self.assertIn("ip_refs", ipdomdata)
        self.assertIn("range_refs", ipdomdata)
        self.assertIn("range_nodes", ipdomdata)
        self.assertIn("ranges", ipdomdata)
        self.assertIn("ip_dict", ipdomdata)

    def find_in_index(self, entry):
        indexentries = self.app.env.get_domain("index").entries
        for index in indexentries:
            for value in indexentries[index]:
                if value[1] == entry:
                    return
        self.fail("%s not found in index" % entry)

    def test_ip4_addresses(self):
        ips = self.app.env.domaindata["ip"]["ip_refs"]
        for ip in IP4_ADDRESSES:
            self.assertIn(ip, ips)
            self.find_in_index("IPv4 address; %s" % ip)
            self.find_in_index("%s; Test page 2" % ip)

    def test_ip6_addresses(self):
        ips = self.app.env.domaindata["ip"]["ip_refs"]
        for ip in IP6_ADDRESSES:
            self.assertIn(ip, ips)
            self.find_in_index("IPv6 address; %s" % ip)
            self.find_in_index("%s; Test page 2" % ip)
