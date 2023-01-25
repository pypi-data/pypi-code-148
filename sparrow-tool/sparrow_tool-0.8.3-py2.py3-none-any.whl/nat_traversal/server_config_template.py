from sparrow.nat_traversal.install import Installer
import os


def gen_frps_ini():
    content = """\
[common]
bind_port = 7000
vhost_http_port = 8080
"""



