# WTFPL

import subprocess
import shlex
import shutil
import os
import re
import signal
import sys


class MonitoredApp:
    def __init__(self,name,options):
        self.name = name
        self.options = options
        if "shell" in options and options["shell"]:
            self.cmd_tokens = options["cmd"]
        else:
            self.cmd_tokens = shlex.split(options["cmd"])
        self.persist = options["persist"] if "persist" in options else False
        self.proc = None
        self.returnValue = None

    @staticmethod
    def get(name, options):
        if "acquire" in options and options["acquire"]:
            aa = AcquiredApp(name,options)
            if aa.getpid():
                return aa
            #else
            aa.terminateIfNonpersistent()
        return OwnApp(name,options)

    def terminateIfNonpersistent(self):
        if not self.persist:
            self.terminate()

    def isAquired(self):
        return False

class OwnApp(MonitoredApp):
    def __init__(self,name,options):
        MonitoredApp.__init__(self,name,options)

    def launch(self):
        if not self.proc or not self.running():
            options = {}
            if "cwd" in self.options:
                options["cwd"] = self.options["cwd"]
            if "shell" in self.options and self.options["shell"]:
                options["shell"] = True
                options["executable"] = "/bin/bash"
            if "detach" in self.options and self.options["detach"]:
                options["preexec_fn"]=os.setpgrp

            self.proc = subprocess.Popen(self.cmd_tokens, **options)
            return self

    def terminate(self):
        if self.proc:
            self.proc.terminate()
            try:
                self.proc.wait(1)
            except subprocess.TimeoutExpired as ex:
                print("do not terminate, killing")
                self.proc.kill()
                self.proc.wait(1)
            self.returnValue = self.proc.poll()
            self.proc = None

    def running(self):
        if not self.proc:
            return False
        else:
            return self.proc.poll() is None

    def poll(self):
        return self.proc.poll() if self.proc else self.returnValue


class AcquiredApp(MonitoredApp):
    def __init__(self,name,options):
        MonitoredApp.__init__(self,name,options)
        self.pid = self.getpid()
        if shutil.which("strace") is None:
            print("acquire flag require strace to be installed.")
            sys.exit(-1)

        strace_cmd = "strace -e none -e exit_group -p "+str(self.pid)
        self.strace = subprocess.Popen(shlex.split(strace_cmd),stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
        self.straceOut = None
        self.straceEnded = False
    def isAquired(self):
        return True

    def getpid(self):
        return self.getPidBasedOnGrepCmd()

    def getPidBasedOnGrepCmd(self):
        grepCommand = """ps -eo pid,cmd |egrep "^ *[0-9]* """ \
                + self.options["cmd"] + """$" --color|awk '{print $1;}'"""
        output = subprocess.check_output(grepCommand, shell=True)
        lines = output.decode("utf8").strip().split("\n")
        if len(lines) >1:
            print("warning: multiple pid found")
        if len(lines) == 1 and len(lines[0]) >0:
            return int(lines[0])
        else:
            return None

    def launch(self):
        if self.straceEnded:
            oa = OwnApp(self.name,self.options)
            oa.launch()
            return oa
        else:
            return self

    def running(self):
        return self.strace.poll() is None

    def poll(self):
        if self.running():
            return None
        else:
            if not self.straceEnded:
                #first poll after strace ended
                self.straceEnded = True
                outs = self.strace.stdout.read()
                # print("read outs:"+str(outs))
                errs = self.strace.stderr.read()
                # print("read errs:"+str(errs))
                match = re.search(r"\+\+\+ exited with (\d+) \+\+\+",errs)
                if match:
                    self.straceOut = int(match.group(1))
                else:
                    self.straceOut = -1
            return self.straceOut


    def terminate(self):
        if not(self.straceEnded):
            os.kill(self.pid, signal.SIGTERM)
            self.strace.wait(.5)
            self.poll()

    def terminateIfNonpersistent(self):
        super().terminateIfNonpersistent()
        if self.strace.poll() is None:
            self.strace.terminate()