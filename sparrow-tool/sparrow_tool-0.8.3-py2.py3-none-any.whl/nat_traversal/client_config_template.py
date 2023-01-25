
def gen_frpc_ini():
    content = """\
[common]
server_addr = x.x.x.x
server_port = 7000

[web]
type = http
local_port = 80
custom_domains = www.yourdomain.com

[web2]
type = http
local_port = 8080
custom_domains = www.yourdomain2.com
"""