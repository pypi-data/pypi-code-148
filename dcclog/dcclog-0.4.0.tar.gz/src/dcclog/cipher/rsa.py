from typing import Optional

from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA512
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes

from dcclog.cipher.aes import AESEncryption, AESMessage

LOG_VER = 1
LOG_TYPE = "RSA"


class RSAEncryption:
    MINIMUM_KEYSIZE = 2048
    KEYSIZE = 32

    def __init__(self, keyfile: str, password: Optional[str] = None) -> None:
        with open(keyfile, "rb") as f:
            rsa_key = RSA.import_key(
                f.read(),
                passphrase=password,
            )
        if rsa_key.size_in_bits() < self.MINIMUM_KEYSIZE:
            raise ValueError("Key size is very short.")

        self._rsa_cipher = PKCS1_OAEP.new(rsa_key, hashAlgo=SHA512)

        self._key = get_random_bytes(self.KEYSIZE)
        self._enc_key = self._rsa_cipher.encrypt(self._key)

    def encrypt(self, plaintext: str, level: str) -> str:
        result = AESEncryption.encrypt_data(
            self._key, plaintext.encode(), self._enc_key
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
                session_key = self._rsa_cipher.decrypt(message.extra)
                return AESEncryption.decrypt_data(
                    session_key, message
                ).decode()
            except (ValueError, KeyError) as key_error:
                raise ValueError(
                    "Invalid ciphertext or keyfile."
                ) from key_error
