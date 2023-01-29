import json
from datetime import datetime

SEPARATOR = " :: "

class LogginMixin():
    def __init__(self, debug=False, session_file_path=None):
        self.print_logs = False
        self.session = ""
        self.save_session_file = False
        if debug:
            self.print_logs = True

        if session_file_path != None and session_file_path != "":
            self.save_session_file = True
            self.sessions_file = session_file_path

    def print(self, *args):
        return True

    def debug(self, msg, jsonObj=None):
        current = str(datetime.now()) + SEPARATOR + msg + "\n"
        if jsonObj:
            current += "==============JSON Conf==============\n\n"
            current += json.dumps(jsonObj,indent=2)
            current += "\n\n============================\n"

        self.session += current
        # print (current)

    def save_session(self):
        if self.print_logs:
            print ("\n\n Printing session logs ..........")
            print (self.session)
            print ("\nSession logs end\n")
        self.session = ""
        return True
