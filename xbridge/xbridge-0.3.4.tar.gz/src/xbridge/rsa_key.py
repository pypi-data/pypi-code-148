

import hashlib
import os
from typing import Optional

from Crypto.Cipher import PKCS1_OAEP as rsa_cipher
# from Crypto.Cipher import PKCS1_v1_5 as rsa_cipher
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA1
# from Crypto.Signature import pss as sig
from Crypto.Signature import pkcs1_15 as sig

class RSAKey:

    prikey_filename = 'prikey.pem'
    pubkey_filename = 'pubkey.pem'

    prikey: Optional[any]
    pubkey: any


    def __init__(self, prikey: Optional[any], pubkey: any):
        self.pubkey = pubkey
        self.prikey = prikey
        # print('pub', pubkey)
        # print('pri', prikey)

    @classmethod
    def fromBytes(cls, pri_bytes: Optional[bytes], pub_bytes: bytes):
        if pri_bytes:
            prikey = RSA.import_key(pri_bytes)
            # .PrivateKey.load_pkcs1(pri_bytes)
        else:
            prikey = None
        pubkey = RSA.import_key(pub_bytes)
        return RSAKey(prikey, pubkey)

    @classmethod
    def new(cls, dir):
        print('create new rsa keys')
        pri = RSA.generate(2048)
        pub = pri.public_key()
        ins = RSAKey(pri, pub)
        ins.save(dir)
        return ins

    @classmethod
    def load(cls, dir):
        print('load rsa keys from %s' % dir)
        prikey_file = os.path.join(dir, RSAKey.prikey_filename)
        pubkey_file = os.path.join(dir, RSAKey.pubkey_filename)
        if os.path.isfile(prikey_file) and os.path.isfile(pubkey_file):
            with open(prikey_file, mode='rb') as privatefile:
                pri_keydata = privatefile.read()
                # prikey = rsa.PrivateKey.load_pkcs1(pri_keydata)
            with open(pubkey_file, mode='rb') as pubfile:
                pub_keydata = pubfile.read()
                # pubkey = rsa.PublicKey.load_pkcs1(pub_keydata)

            return RSAKey.fromBytes(pri_keydata, pub_keydata)

        else:
            return RSAKey.new(dir)

    def save(self, dir):
        print('save rsa keys to %s' % dir)
        pubkey_file = os.path.join(dir, RSAKey.pubkey_filename)
        os.makedirs(os.path.dirname(pubkey_file), 0o755, exist_ok=True)
        with open(pubkey_file, mode='wb+') as file:
            file.write(self.pubkey_bytes)

        prikey_file = os.path.join(dir, RSAKey.prikey_filename)
        os.makedirs(os.path.dirname(prikey_file), 0o755, exist_ok=True)
        with open(prikey_file, mode='wb+') as file:
            file.write(self.prikey_bytes)

    @property
    def pubkey_hash(self) -> str:
        return hashlib.sha1(self.pubkey_bytes).hexdigest()
        
    @property
    def pubkey_bytes(self) -> bytes:
        return self.pubkey.export_key('PEM')

    @property
    def prikey_bytes(self) -> bytes:
        return self.prikey.export_key('PEM')

    @property
    def pubkey_hex(self):
        return self.pubkey_bytes.hex()

    def encrypt(self, data: bytes) -> bytes:
        # print('data=', data)
        # print('pubkey', self.pubkey)
        cipher = rsa_cipher.new(self.pubkey, SHA1)
        return cipher.encrypt(data)

    def encryptAsHex(self, data: bytes) -> str:
        return self.encrypt(data).hex()

    def decrypt(self, data: bytes) -> bytes:
        # return rsa.decrypt(data, self.prikey)
        cipher = rsa_cipher.new(self.prikey, SHA1)
        print("decrypt data length=", len(data))
        return cipher.decrypt(data)


    def sign(self, data: bytes) ->  bytes:
        h = SHA1.new(data)
        return sig.new(self.prikey).sign(h)
        # return rsa.sign(data, self.prikey, 'SHA-1')

        # ok = self.verify(data, signature)
        # print("sign result: ", ok)
        # return signature

    def verify(self, data: bytes, signature: bytes) -> bool:
        h = SHA1.new(data)
        verifier = sig.new(self.pubkey)
        try:
            verifier.verify(h, signature)
            return True
        except (ValueError, TypeError):
            print("The signature is not authentic.")
        # try:
        #     algo = rsa.verify(data, signature, self.pubkey)
        #     if algo == 'SHA-1':
        #         return True
        # except rsa.pkcs1.VerificationError as e:
        #     print("VerificationError:", e)
        #     return False
        
        return False