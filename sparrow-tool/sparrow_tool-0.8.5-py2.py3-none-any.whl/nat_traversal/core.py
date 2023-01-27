# 前置条件 服务端上已安装 systemd, 安装示例 `apt install systemd`
from sparrow.nat_traversal.install import Installer
from sparrow.nat_traversal.server_config_template import *
import os


class Manager:
    def __init__(self):
        self.installer = Installer()

    def install_frp(self):
        self.installer.install()

    def write_systemd(self):
        write_frps_to_systemd()



def write_frps_to_systemd():
    # vim /etc/systemd/system/frps.service
    installer = Installer()
    frps_path = os.path.join(installer.frp_unpack_file_dir, "frps")
    frps_ini_path = os.path.join(installer.frp_unpack_file_dir, "frps.ini")
    content = f"""\
[Unit]
# 服务名称，可自定义
Description = frp server
After = network.target syslog.target
Wants = network.target

[Service]
Type = simple
# 启动frps的命令，需修改为您的frps的安装路径
ExecStart = {frps_path} -c {frps_ini_path}

[Install]
WantedBy = multi-user.target
"""
    frp_systemd_file = "/etc/systemd/system/frps.service"
    try:
        with open(frp_systemd_file, 'w') as f:
            f.write(content)
    except Exception as e:
        print(e)
        print(f"Write to {frp_systemd_file} failed! Please write the following content into it manually.")
        print(content)


def start_server():
    os.system("systemctl start frps")


def stop_server():
    os.system("systemctl stop frps")


def restart_server():
    os.system("systemctl restart frps")


def enable_server():
    """开机自启"""
    os.system("systemctl enable frps")
