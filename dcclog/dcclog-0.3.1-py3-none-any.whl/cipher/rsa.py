from typing import Optional

from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA512
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes

from dcclog.cipher.aes import AESEncryption, AESMessage


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

        return f"{level: <8} :: {result.encode()}"

    def decrypt(self, ciphertext: str) -> str:
        parts = ciphertext.split(" :: ")
        if len(parts) != 2:
            raise ValueError("Invalid ciphertext.")
        encoded_message = parts[1].rstrip()
        try:
            message = AESMessage.decode(encoded_message)
            session_key = self._rsa_cipher.decrypt(message.extra)
            return AESEncryption.decrypt_data(session_key, message).decode()
        except (ValueError, KeyError) as key_error:
            raise ValueError("Invalid ciphertext or keyfile.") from key_error
