

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad

import random

class Cipher:

    key: bytes # 16B
    iv: bytes  # 16B

    aes_for_en: any
    aes_for_de: any

    def __init__(self, key: bytes, iv: bytes):
        # print('create a cipher')
        # print('key:', key)
        # print('iv:', iv)
        self.key = key
        self.iv = iv

        self.aes_for_en = AES.new(key, AES.MODE_CBC, iv)
        self.aes_for_de = AES.new(key, AES.MODE_CBC, iv)
        pass

    @classmethod
    def new(cls):
        key = Cipher.random()
        iv = Cipher.random()
        return Cipher(key, iv)

    @classmethod
    def random(cls) -> bytes:
        keyarr = [0] * 16
        for i in range(16):
            keyarr[i] = random.randint(0, 255) 
        return bytes(keyarr)

    def encrypt(self, data) -> bytes:
        return self.aes_for_en.encrypt(pad(data, 16, 'pkcs7'))
        # return data

    def decrypt(self, data) -> bytes:
        # print('data[%d]:' % len(data), data)
        return unpad(self.aes_for_de.decrypt(data), 16, 'pkcs7')
        # return data


    @property
    def key_hex(self):
        return self.key.hex()

    @property
    def iv_hex(self):
        return self.iv.hex()