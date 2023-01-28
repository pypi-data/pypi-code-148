# WTFPL

import subprocess

class MonitoredApp:
    def __init__(self,name,options):
        self.name = name
        self.options = options
        self.cmd_tokens = options["cmd"].split(" ")
        self.proc = None

    def launch(self):
        if not self.proc or not self.running():
            self.proc = subprocess.Popen(self.cmd_tokens)
    def terminate(self):
        if self.proc:
            self.proc.terminate()
            try:
                self.proc.wait(1)
            except subprocess.TimeoutExpired as ex:
                print("do not terminate, killing")
                self.proc.kill()
                self.proc.wait(1)
            self.proc = None

    def running(self):
        if not self.proc:
            return False
        else:
            return self.proc.poll() is None
