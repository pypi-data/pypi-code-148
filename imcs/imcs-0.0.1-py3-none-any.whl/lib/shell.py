"""
  shell utilities for imcs
"""

import shlex
import subprocess
import sys

class ShellError(Exception):
    """"
    Raised when shell commands were not successful
    Attributes:
       message - the error message
    """
    def __init__(self, message):
        self.message = message

def shell(cmd, shell=False, split=True, return_errorcode=False):
    """
    @input: 
     - a call string to transfer to the shell
     - shell (True/False) - a bool to indicate the shell flag to Popen, defaults to False
     - split (True/False) - whether or not the command string shall be split with shlex
     - return_errorcode - defaults to false, when set to True, no exception will be raised,
       but the error handling is left to the client
    @output: the result
    """
    if split:
        cmd = shlex.split(cmd)
    process = subprocess.Popen(
        cmd, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    out, err = process.communicate()
    out = out.decode(sys.stdout.encoding)
    err = err.decode(sys.stderr.encoding)
    # have we been successful?
    if return_errorcode:
        return out, err, process.returncode
    elif process.returncode == 0:
        return out, err, process.returncode
    raise ShellError(err)
