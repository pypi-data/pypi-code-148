import json
import subprocess

def run(cmd,token):
                
        proc1 = subprocess.run(["upsolver","execute","-t", token,"-c", cmd],
        capture_output=True)

        proc2 = subprocess.run(['jq', '-s'],
        input=proc1.stdout,
        capture_output=True)

        try:
            output = json.loads(proc2.stdout)
        except:
            output = proc1.stdout.decode("utf-8")
        
        err = proc1.stderr.decode("utf-8")

        if err == '':
            return True,output
        else:
            return False,err


