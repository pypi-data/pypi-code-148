from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Optional, cast

from Crypto.Cipher import AES
from Crypto.Cipher._mode_gcm import GcmMode
from Crypto.Hash import SHA512
from Crypto.Protocol.KDF import PBKDF2

from dcclog import b2str, from_json, str2b, to_json

LOG_VER = 1
LOG_TYPE = "AES"


@dataclass
class AESMessage:
    nonce: bytes
    tag: bytes
    ciphertext: bytes
    extra: bytes

    def encode(self) -> str:
        d = {k: b2str(v) for k, v in asdict(self).items()}
        return b2str(to_json(d))

    @classmethod
    def decode(cls, s: str) -> AESMessage:
        decoded_message = from_json(str2b(s))
        if isinstance(decoded_message, dict):
            d: dict[str, bytes] = {}
            for k, v in decoded_message.items():
                if not (isinstance(k, str) and isinstance(v, str)):
                    raise ValueError("Invalid ciphertext.")
                d[k] = str2b(v)
            return cls(**d)
        raise ValueError("Invalid ciphertext.")


class AESEncryption:
    KEYSIZE = 32
    ITER_COUNT = 100000

    def __init__(self, password: str, salt: Optional[bytes] = None) -> None:
        if salt is None:
            salt = SHA512.new(password.encode()).digest()
        self._key = PBKDF2(
            password=password,
            salt=salt,
            dkLen=self.KEYSIZE,
            count=self.ITER_COUNT,
            hmac_hash_module=SHA512,
        )
        self._salt = salt

    def encrypt(self, plaintext: str, level: str) -> str:
        result = self.encrypt_data(
            self._key, plaintext.encode(), level.encode()
        )

        return f"{level: <8} ::{LOG_TYPE}-{LOG_VER}:: {result.encode()}"

    def decrypt(self, ciphertext: str) -> str:
        try:
            parts = ciphertext.split("::")
            if len(parts) != 3:
                raise ValueError
            encoded_message = parts[2].strip()
            log_type, log_version = parts[1].split("-")
            if log_type != LOG_TYPE or int(log_version) > LOG_VER:
                raise ValueError
        except Exception as exc:
            raise ValueError("Invalid log format.") from exc
        else:
            try:
                message = AESMessage.decode(encoded_message)
                return self.decrypt_data(self._key, message).decode()
            except (ValueError, KeyError) as key_error:
                raise ValueError(
                    "Invalid ciphertext or password."
                ) from key_error

    @staticmethod
    def encrypt_data(key: bytes, data: bytes, extra: bytes) -> AESMessage:
        cipher = cast(GcmMode, AES.new(key, AES.MODE_GCM))
        cipher.update(extra)
        ciphertext, tag = cipher.encrypt_and_digest(data)
        return AESMessage(
            nonce=cipher.nonce, tag=tag, ciphertext=ciphertext, extra=extra
        )

    @staticmethod
    def decrypt_data(key: bytes, data: AESMessage) -> bytes:
        cipher = cast(GcmMode, AES.new(key, AES.MODE_GCM, nonce=data.nonce))
        cipher.update(data.extra)
        return cipher.decrypt_and_verify(data.ciphertext, data.tag)
