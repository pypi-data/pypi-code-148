

from enum import Enum
import json
from typing import List, Optional


VERSION = 2

class MsgType(Enum):
    GetInfo = 'get_info'

    # base
    Request = 'request'
    Resume = 'resume'
    
    Reply = 'reply'
    Done = "done"
    Later = 'later'

    GetFile = 'get_file'
    SendFileCipher = 'send_file_cipher'
    SendFileInfo = 'send_file_info'
    # SendDirInfo = 'send_dir_info'
    SendFileEnd = 'send_file_end'

    # Requirements = "requirements"



class MsgTypeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Enum):
            return obj.value
        # if obj is None:
        #     return None
        return json.JSONEncoder.default(self, obj)


class Codable:

    def toDict(self) -> dict:
        return {}

    def toString(self) -> str:
        # obj = self.toDict()
        # print("obj=", obj)
        return json.dumps(self.toDict(), cls=MsgTypeEncoder, )

    def toPrettyString(self) -> str:
        # obj = self.toDict()
        # print("obj=", obj)
        return json.dumps(self.toDict(), cls=MsgTypeEncoder, indent='    ')

    def toBytes(self) -> bytes:
        return self.toString().encode(encoding='utf8', errors='strict')

class ParamType(Enum):
    FileOrDir = "any-file-or-dir"
    FileOrDirList = "any-file-or-dir-list"
    File = "any-file"
    FileList = "any-file-list"
    Dir = "any-dir"
    DirList = "any-dir-list"
    Text = "any-text"
    TextList = "any-text-list"
    Selectable = "selectable"
    SelectableList = "selectable-list"


class ParamSelection(Codable):
    select: str
    localized: Optional[str]
    
    def __init__(self, select, localized = None):
        self.select = select
        self.localized = localized

    @classmethod
    def fromDict(cls, obj: bytes):
        try:
            # string = data.decode(encoding='utf8', errors='strict')
            # obj = json.loads(string)
            # print("obj", obj)
            return ParamSelection(obj['select'], obj.get('localized'))
        except Exception as e:
            print(e)
            raise Exception("data format error")

    def toDict(self) -> dict:
        # print("param selection toDict")

        return {
            'select': self.select,
            'localized': self.localized,
        }


class ParamRequire(Codable):
    param: str
    localized: Optional[str]
    type: ParamType
    selections: Optional[List[ParamSelection]]

    def __init__(self, param, type: ParamType, localized = None, selections = None):
        self.param = param
        self.localized = localized
        self.type = type
        self.selections = selections

    @classmethod
    def fromDict(cls, obj):
        try:
            # string = data.decode(encoding='utf8', errors='strict')
            # obj = json.loads(string)
            # print("obj", obj)
            selections = obj.get("selections")
            return ParamRequire(obj['param'], ParamType(obj['type']), obj.get('localized'),
                list(map(ParamSelection.fromDict, selections)) if selections else None)
        except Exception as e:
            print(e)
            raise Exception("data format error")

    def toDict(self) -> dict:
        # print("param require toDict")
        return {
            'param': self.param,
            'localized': self.localized,
            'type': self.type,
            'selections': list(map(ParamSelection.toDict, self.selections)) if self.selections else None,
        }

class NormalMsg(Codable):

    type: MsgType
    sessionid: Optional[str]

    app: Optional[str]
    action: str
    params: List[str]
    files: Optional[List[str]]
    require_params: Optional[List[ParamRequire]]

    def __init__(self, type: MsgType, 
                sessionid: Optional[str] = None,
                app: Optional[str] = None,
                action: str = "",
                params:  List[str] = [],
                files:  Optional[List[str]] = None,
                requires: Optional[ParamRequire] = None) -> None:
        self.type = type
        self.app = app
        self.action = action
        self.params = params
        self.files = files
        self.require_params = requires
        self.sessionid = sessionid

    @classmethod
    def request(cls, app=None, action=None, params=None, files=None):
        return NormalMsg(MsgType.Request, None, app, action, params, files)

    @classmethod
    def reply(cls, app=None, action=None,  params=None, files=None):
        return NormalMsg(MsgType.Reply, None, app, action, params, files)

    # @classmethod
    # def requires(cls, action: str, requires: List[ParamRequire]):
    #     return NormalMsg(MsgType.Reply, action=action, requires=requires)

    @classmethod
    def fromBytes(cls, data: bytes):
        try:
            string = data.decode(encoding='utf8', errors='strict')
            # print("string:", string)
            obj = json.loads(string)
            # print("NormalMsg fromBytes: obj: ", obj)
            return NormalMsg.fromDict(obj)
        except Exception as e:
            print("data format error:", e)
            raise e

    def toDict(self) -> dict:
        print("normal msg toDict")
        return {
            'type': self.type,
            'sessionid': self.sessionid,
            'app': self.app,
            'action': self.action,
            'params': self.params,
            'files': self.files,
            "requires": list(map(ParamRequire.toDict, self.require_params)) if self.require_params else None
        }

    @classmethod
    def fromDict(cls, obj):
        try:
            if obj is None:
                return None
            requires = obj.get('requires')
            # if requires:
            #     return NormalMsg(MsgType(obj['type']), action= )
            sessionid: str = obj.get('sessionid', None)
            if sessionid is not None:
                sessionid = sessionid.lower()
            return NormalMsg(MsgType(obj['type']), sessionid, obj.get('app'),  obj.get('action'), obj.get('params'), obj.get('files'), 
                list(map(ParamRequire.fromDict, requires)) if requires else None
            )
        except Exception as e:
            print(e)
            raise Exception("data format error")


class HelloMsg(Codable):
    version: int
    pubkey: str  # pubkey.pem hex
    random: bytes

    def __init__(self, pubkey: str, random: bytes, version: int = VERSION) -> None:
        self.pubkey = pubkey
        self.version = version
        self.random = random

    @classmethod
    def fromBytes(cls, data: bytes):
        # print("hello msg from bytes...")
        string = data.decode(encoding='utf8', errors='strict')
        obj = json.loads(string)
        return HelloMsg(obj['pubkey'], bytes.fromhex(obj['random']), obj['version'])

    def toDict(self) -> dict:
        return {
            'pubkey': self.pubkey,
            'random': self.random.hex(),
            'version': self.version,
        }

  

class ConnectMsg(Codable):
    key: str
    iv: str
    sign: str
    empty: bool

    def __init__(self, key: str = None, iv: str = None, sign: str = None, empty = False) -> None:
        self.key = key
        self.iv = iv
        self.sign = sign
        self.empty = empty

    @classmethod
    def fromBytes(cls, data: bytes):
        # print("connect msg from bytes...")
        # try:
        string = data.decode(encoding='utf8', errors='strict')
        obj = json.loads(string)
        # print("get connect msg: ", obj)
        if obj.get('aes'):
            return  ConnectMsg(
                obj['aes']['key'],
                obj['aes']['iv'],
                obj['aes']['sign'])
        return ConnectMsg(empty=True)

        # except Exception as e:
        #     print(e)
        #     raise Exception("data format error")

    def toDict(self) -> dict:
        if self.empty :
            return {}
        
        return {
            'aes': {
                'key': self.key,
                'iv': self.iv,
                'sign': self.sign,
            },
        }



class CompleteMsg(Codable):
    reason: str

    def __init__(self, reason: str) -> None:
        self.reason = reason

    @classmethod
    def fromBytes(cls, data: bytes):
        # print("hello msg from bytes...")
        string = data.decode(encoding='utf8', errors='strict')
        obj = json.loads(string)
        return CompleteMsg(obj['reason'])

    def toDict(self) -> dict:
        return {
            'reason': self.reason,
        }


class RefuseMsg(Codable):
    reason: str

    def __init__(self, reason: str) -> None:
        self.reason = reason

    @classmethod
    def fromBytes(cls, data: bytes):
        # try:
        string = data.decode(encoding='utf8', errors='strict')
        obj = json.loads(string)
        # print('obj', obj)
        return RefuseMsg(obj['reason'])
        # except Exception as e:
        #     print(e)
        #     raise Exception("data format error")

    def toDict(self) -> dict:
        return {
            'reason': self.reason,
        }

  

# HandleReplyCallable = Optional[Callable[[Msg, List[str]], None]]
