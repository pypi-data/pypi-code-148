

from enum import Enum
import json
import os
import shutil
from typing import List, Optional
from xbridge.config import Config

from xbridge.transmsg import Codable, NormalMsg

class SessionState(Enum):
    Initial = 'initial'

    # RequestWillSend = 'request_will_send'
    RequestTransferring = 'request_transferring'
    RequestReceived = 'request_received'

    # ReplyWillSend = 'reply_will_send'
    ReplyTransferring = 'reply_transferring'

    Done = "done"
    # Cancelled = "cancelled"

    def isDone(self): 
        if self == SessionState.Done or self == SessionState.Initial:
            return True
        return False

class SessionRole(Enum):
    Unknown = 'unknown'
    Initiator = 'initiator'
    Handler = 'handler'

class Session(Codable):

    userid: str
    id: str

    file: str
    dir: str

    role: SessionRole
    state: SessionState

    request: Optional[NormalMsg] = None
    reply: Optional[NormalMsg] = None

    files_provided: List[str] = []
    files_accessable: List[str] = []

    def dump(self):
        print("🐟 Session Role: %s, state: %s, in: %s" % (self.role.value, self.state.value, self.dir))

    def __del__(self):
        print("[-] Session state: %s" % self.state)
        if self.state.isDone():
            shutil.rmtree(self.dir, ignore_errors=True)
            print('delete session_dir of : %s' % self.dir)
        else:
            self.save()

    def __init__(self, id: str, userid: str, role: SessionRole = SessionRole.Unknown) -> None:
        print("[+] Session")
        self.role = role
        self.userid = userid
        self.state = SessionState.Initial
        self.id = id
        self.dir = os.path.join(Config.config_dir, 'sessions', userid, id)
        self.file = os.path.join(self.dir, "session.json")

        if role == SessionRole.Unknown:
            # session already exist, load
            # if not os.path.isfile(self.file):
            #     raise Exception("Session NOT exist!")

            try:
                with open(self.file, 'rb') as file:
                    string = file.read().decode(encoding='utf8', errors='strict')
                    obj = json.loads(string)
                    self.role = SessionRole(obj["role"])
                    self.state = SessionState(obj["state"])
                    self.request = NormalMsg.fromDict(obj.get("request", None))  
                    self.reply = NormalMsg.fromDict(obj.get("reply", None))
                    self.files_provided = obj.get("files_provided", [])
                    self.files_accessable = obj.get("files_accessable", [])
            except Exception as e:
                 raise Exception("Session NOT exist!")
        else:
            # new session
            self.state = SessionState.Initial
            os.makedirs(self.dir, 0o755)
            print('create session_dir: %s' % self.dir)
            # self.save()

    def save(self):
        try:
            with open(self.file, 'wb') as file:
                data = self.toBytes()
                print("save session: ", self.id)
                print(data)
                file.write(data)
        except FileNotFoundError:
            print("save session failed")

    def toDict(self):
        reqdict = None
        replyDict = None
        if self.request:
            reqdict = self.request.toDict()
        if self.reply:
            replyDict = self.reply.toDict()
        return {
            'role': self.role,
            'state': self.state,
            "request": reqdict,
            "reply": replyDict,
            'files_provided': self.files_provided,
            'files_accessable': self.files_accessable,
        }
        
