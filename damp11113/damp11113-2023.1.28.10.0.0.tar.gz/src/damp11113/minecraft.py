from mcstatus import JavaServer
import json
import requests
from base64 import b64decode as base64decode
import subprocess
from mcrcon import MCRcon

class mcstatus_exception(Exception):
    pass

class uuid2name_exception(Exception):
    pass

class server_exeption(Exception):
    pass

class install_exception(Exception):
    pass

class rcon_exception(Exception):
    pass

#------------------------server------------------------------
class mcserver:
    def __init__(self, server='server.jar', java='java', ramuse='1024', nogui=True, noguipp=False):
        self.serverf = server
        self.java = java
        self.ramuse = ramuse
        self.nogui = nogui
        self.noguipp = noguipp

    def start(self):
        if self.nogui:
            if self.noguipp:
                self.s = subprocess.Popen(f'{self.java} -Xms{self.ramuse}M -Xmx{self.ramuse}M -jar {self.serverf} --nogui', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            else:
                self.s = subprocess.Popen(f'{self.java} -Xms{self.ramuse}M -Xmx{self.ramuse}M -jar {self.serverf} nogui', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)        
        else:
            self.s = subprocess.Popen(f'{self.java} -Xms{self.ramuse}M -Xmx{self.ramuse}M -jar {self.serverf}', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def stop(self):
        self.command('stop')
        self.s.communicate()

    def command(self, command):
        self.s.stdin.write(command + '\n')

    def log(self):
        return self.s.stdout.read()
        
#------------------get-uuid2name------------------

class uuid2name:
    def __init__(self) -> None:
        pass

    def getmcuuid(self, player_name):
        try:
            r = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{player_name}")
            if r.text == '':
                raise uuid2name_exception(f"{player_name} not found")
            else:
                return json.loads(r.text)['id']
        except Exception as e:
            raise uuid2name_exception(e)

    def getmcname(self, player_uuid):
        try:
            r = requests.get(f"https://api.mojang.com/user/profiles/{player_uuid}/names")
        except Exception as e:
            raise uuid2name_exception(e)
        try:
            o = json.loads(r.text)[0]['name']
            return o
        except KeyError:
            raise uuid2name_exception(f"player not found")

    def getmcnamejson(self, player_uuid):
        try:
            return requests.get(f"https://api.mojang.com/user/profiles/{player_uuid}/names").text
        except Exception as e:
            raise uuid2name_exception(f"get mc name error: {e}")

    def getmcuuidjson(self, player_name):
        try:
            return requests.get(f"https://api.mojang.com/users/profiles/minecraft/{player_name}").text
        except Exception as e:
            raise uuid2name_exception(f"get mc uuid error: {e}")

#----------------other api------------------

def skin_url(uuid):
    try:
        r = requests.get(f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}")
        base = json.loads(r.text)['properties'][0]['value']
        # base64 to json
        js = base64decode(base)
        # json to dict
        d = json.loads(js)
        # get skin url
        return d['textures']['SKIN']['url']
    except Exception as e:
        raise uuid2name_exception(f"skin url error: {e}")

def mctimestamp(uuid):
    try:
        r = requests.get(f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}")
        base = json.loads(r.text)['properties'][0]['value']
        # base64 to json
        js = base64decode(base)
        # json to dict
        d = json.loads(js)
        # get skin url
        return d['timestamp']
    except Exception as e:
        raise uuid2name_exception(f"error: {e}")


#----------------------mcstatus------------------------

class mcstatus():
    def __init__(self, ip):
        self.server = JavaServer.lookup(ip)

    def raw(self):
        try:
            return self.server.status().raw
        except Exception as e:
            raise mcstatus_exception(f"raw mc status error: {e}")

    def players(self):
        try:
            return self.server.status().players
        except Exception as e:
            raise mcstatus_exception(f"players mc status error: {e}")

    def favicon(self):
        try:
            return self.server.status().favicon
        except Exception as e:
            raise mcstatus_exception(f"favicon mc status error: {e}")

    def description(self):
        try:
            return self.server.status().description
        except Exception as e:
            raise mcstatus_exception(f"description mc status error: {e}")

    def version(self):
        try:
            return self.server.status().version
        except Exception as e:
            raise mcstatus_exception(f"version mc status error: {e}")

    def ping(self):
        try:
            return self.server.ping()
        except Exception as e:
            raise mcstatus_exception(f"ping mc status error: {e}")

    def query_raw(self):
        try:
            return self.server.query().raw
        except Exception as e:
            raise mcstatus_exception(f"query raw mc status error: {e}")

    def query_players(self):
        try:
            return self.server.query().players
        except Exception as e:
            raise mcstatus_exception(f"query players mc status error: {e}")

    def query_map(self):
        try:
            return self.server.query().map
        except Exception as e:
            raise mcstatus_exception(f"query map mc status error: {e}")

    def query_motd(self):
        try:
            return self.server.query().motd
        except Exception as e:
            raise mcstatus_exception(f"query motd mc status error: {e}")

    def query_software(self):
        try:
            return self.server.query().software
        except Exception as e:
            raise mcstatus_exception(f"query software mc status error: {e}")

#----------------------Rcon------------------------

class Rcon:
    def __init__(self, ip, password, port=25575, tls=0, timeout=5):
        self.ip = ip
        self.port = port
        self.password = password
        self.rcon = MCRcon(host=ip, port=port, password=password, tlsmode=tls, timeout=timeout)

    def connect(self):
        try:
            self.rcon.connect()
        except Exception as e:
            raise rcon_exception(f"rcon connect error: {e}")

    def send(self, command):
        try:
            return self.rcon.command(command)
        except Exception as e:
            raise rcon_exception(f"rcon send error: {e}")

    def disconnect(self):
        try:
            self.rcon.disconnect()
        except Exception as e:
            raise rcon_exception(f"rcon disconnect error: {e}")