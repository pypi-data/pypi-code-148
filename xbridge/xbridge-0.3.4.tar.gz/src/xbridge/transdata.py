


from enum import Enum
import json

from xbridge.transmsg import CompleteMsg, ConnectMsg, HelloMsg, NormalMsg


class DataType(Enum):
    hello = 0
    connect = 1
    encrypted = 2
    file = 3
    complete = 4


class TransData:

    type: DataType
    msg: bytes

    def __init__(self, type: DataType, msg: bytes) -> None:
        self.type = type
        self.msg = msg

    @classmethod
    def hello(cls, pubkey_hex: str, random: bytes):
        msg = HelloMsg(pubkey_hex, random)
        return TransData(DataType.hello, msg.toBytes())

    @classmethod
    def connect(cls,
                key: str = None, iv: str = None, sign: str = None, empty = False):
        msg = ConnectMsg(key, iv, sign, empty)
        return TransData(DataType.connect, msg.toBytes())

    @classmethod
    def refuse(cls, reason):
        msg = {
            "reason": reason,
        }
        return TransData(DataType.refuse,
                         bytes(json.dumps(msg), encoding='UTF-8'))

    @classmethod
    def complete(cls, reason: str = ''):
        msg = CompleteMsg(reason)
        return TransData(DataType.complete, msg.toBytes())

    @classmethod
    def encrypted(cls, msg: NormalMsg, cipher):
        return TransData(DataType.encrypted,
                         cipher.encrypt(msg.toBytes()))

    @classmethod
    def encrypted_bin(cls, bin: bytes, cipher):
        return TransData(DataType.file,
                         cipher.encrypt(bin))

    @classmethod
    def fromBytes(cls, data: bytes):
        # print("transdata[%d]" % len(data), data)
        try:
            data_type = int.from_bytes(data[:4], 'little', signed=False)
            # print('data type = ', data_type)
            return TransData(DataType(data_type), data[4:])
        except Exception as e:
            print(e)
            print('data: ', data)
            raise Exception("data format error")

    def toBytes(self) -> bytes:
        data_type: int = self.type.value
        return data_type.to_bytes(4, 'little', signed=False) + self.msg

    def resolveMsg(self, cipher=None):
        # print('data type = ', self.type.value)
        if self.type == DataType.connect:
            return ConnectMsg.fromBytes(self.msg)
        if self.type == DataType.hello:
            return HelloMsg.fromBytes(self.msg)
        if self.type == DataType.complete:
            return CompleteMsg.fromBytes(self.msg)

        decrypted_msg: bytes = cipher.decrypt(self.msg)
        if self.type == DataType.file:
            return decrypted_msg

        return NormalMsg.fromBytes(decrypted_msg)

