"""Initialize modules."""
from .Heartbeat import Heartbeat
from .BaseHealthCheck import BaseHealthCheck

def init(config, uuclient):

    def cmd_heartbeat(dto_in):
        uucmd = config["uuApp"]['uuCmdList']['gatewayHeartbeat']
        return uuclient.post_request(uucmd, dto_in)

    gateway_config = config["gateway"]

    return [Heartbeat(cmd_heartbeat)]

