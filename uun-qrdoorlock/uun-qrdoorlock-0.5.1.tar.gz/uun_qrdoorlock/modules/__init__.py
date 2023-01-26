from .QrLock import QrLock
def init(config, uuclient):

    gconfig = config["gateway"]

    def cmd_get_public_key():
        # will be replaced by placing the publicKey directly into main configuration by server
        try:
            uucmd = config['uuApp']['uuCmdList']['getPublicKey']
            return uuclient.get_request(uucmd)
        except KeyError:
            return None

    def cmd_send_used_qr(storage):
        failed = []
        try:
            # testing
            uucmd = config["uuApp"]['uuCmdList']['qrcodeLog']
        except:
            return []
        for stuple in storage:
            (keycode, timestamp) = stuple
            dto_in = {
                "keyCode": keycode,
                "usageTs": timestamp
            }
            response = uuclient.post_request(uucmd, dto_in)
            if response.status_code < 200 or response.status_code >= 300:
                failed.append(stuple)
        
        return failed

    def cmd_send_doormonitor(storage):
        uucmd = "TODO"

        
    ret = [
            QrLock(gconfig, (cmd_send_used_qr, cmd_get_public_key))
        ]
    # DoorMonitor is totally disabled in virtual mode
    if not gconfig["virtualMode"]:
        from .DoorMonitor import DoorMonitor
        ret.append(
            DoorMonitor(gconfig, cmd_send_doormonitor)
        )

    return ret
