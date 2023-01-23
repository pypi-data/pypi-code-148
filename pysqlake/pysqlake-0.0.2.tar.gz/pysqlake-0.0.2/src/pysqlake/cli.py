import json
import subprocess

def run(cmd,token):
                        
    proc1 = subprocess.run(["upsolver","execute","-t", token,"-c", cmd],
    capture_output=True)

    proc2 = subprocess.run(['jq', '-s'],
    input=proc1.stdout,
    capture_output=True)

    output, err = json.loads(proc2.stdout),proc1.stderr.decode("utf-8")
    if err == '':
        return True,output
    else:
        return False,err
