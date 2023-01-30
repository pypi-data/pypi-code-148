# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import abc
import base64
import hashlib
import hmac
import json
import random
import time

import pyDes
import rsa
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5


class Encrypt(abc.ABC):
    @abc.abstractmethod
    def encrypt(self, data):
        return NotImplemented

    @abc.abstractmethod
    def sign(self, mess, timestamp, data):
        return NotImplemented

    @abc.abstractmethod
    def encrypt_type(self):
        return NotImplemented


def decrypt(des3key, data):
    data = bytes(data, encoding="utf8")
    key = bytes(des3key[0:8], encoding="utf8")
    return pyDes.triple_des(des3key, pyDes.CBC, key, pad=None, padmode=pyDes.PAD_PKCS5).decrypt(base64.b64decode(data))


def verify_sign_rsa(public_key, app_key, data, mess, timestamp, signature):
    sign_pairs = "data=" + data + "&mess=" + mess + "&timestamp=" + timestamp + "&key=" + app_key
    rsa.verify(sign_pairs, signature, public_key)


def verify_sign_hmac(des3key, app_key, data, mess, timestamp, signature):
    sign_pairs = "data=%s&mess=%s&timestamp=%d&key=%s" % (data, mess, timestamp, app_key)
    return hmac.new(app_key.encode('utf-8'), msg=sign_pairs, digestmod=hashlib.sha256).hexdigest() == signature


def gen_key():
    x = RSA.generate(2048)
    s_key = x.export_key()  # 私钥
    g_key = x.publickey().export_key()  # 公钥
    public_key = g_key.decode("utf-8")
    private_key = s_key.decode("utf-8")
    return public_key, private_key


class EncryptHmac(Encrypt):
    def __init__(self, app_key, des3key):
        self.__app_key = app_key
        self.__des3key = des3key

    def encrypt_type(self):
        return "sha256"

    def encrypt(self, data):
        data = bytes(data, encoding="utf8")
        key = bytes(self.__des3key[0:8], encoding="utf8")
        return base64.b64encode(
            pyDes.triple_des(self.__des3key, pyDes.CBC, key, pad=None, padmode=pyDes.PAD_PKCS5).encrypt(data))

    def sign(self, mess, timestamp, encrypt_data):
        signPairs = "data=%s&mess=%s&timestamp=%d&key=%s" % (
            str(encrypt_data, encoding="utf-8"), mess, timestamp, self.__app_key)
        app_key = bytes(self.__app_key, encoding="utf8")
        signPairs = bytes(signPairs, encoding="utf8")
        return hmac.new(app_key, msg=signPairs, digestmod=hashlib.sha256).hexdigest()


class EncryptRsa(Encrypt):
    def __init__(self, app_key, public_key, private_key, des3key):
        self.__public_key = RSA.importKey(public_key)
        self.__private_key = RSA.importKey(private_key)
        self.__app_key = app_key
        self.__des3key = des3key

    def encrypt_type(self):
        return "rsa"

    def encrypt(self, data):
        data = bytes(data, encoding="utf8")
        key = bytes(self.__des3key[0:8], encoding="utf8")
        return base64.b64encode(
            pyDes.triple_des(self.__des3key, pyDes.CBC, key, pad=None, padmode=pyDes.PAD_PKCS5).encrypt(data))

    def sign(self, mess, timestamp, encrypt_data):
        sign_pairs = "data=%s&mess=%s&timestamp=%d&key=%s" % (
            bytes.decode(encrypt_data), mess, timestamp, self.__app_key)
        signer = Signature_pkcs1_v1_5.new(self.__private_key)
        digest = SHA256.new()
        digest.update(sign_pairs.encode("utf8"))
        sign = signer.sign(digest)
        return base64.b64encode(sign)


class ReqMessage(object):
    """
    ReqMessage 请求消息体
    """

    def __init__(self, encrypt, data):
        """
        :param encrypt: 加密方式
        :type data: {} 请求信息
        :param data: 请求信息
        """
        self.__encrypt = encrypt
        self.data = None
        if data is not None:
            self.data = json.dumps(data, ensure_ascii=False)

    def pack(self):
        if self.data is None:
            return None
        timestamp = int(time.time())
        mess = ''.join(random.sample('1234567890abcdefghijklmnopqrstuvwxy', 10))
        encrypt_data = self.__encrypt.encrypt(self.data)
        return {
            "data": encrypt_data,
            "mess": mess,
            'timestamp': timestamp,
            "sign": self.__encrypt.sign(mess, timestamp, encrypt_data),
            "sign_type": self.__encrypt.encrypt_type()
        }


class RespMessage(object):
    """
    RespMessage 返回信息
    """

    def __init__(self, des3key, content, req_data, req_param, headers):
        self.__des3key = des3key
        self.__content = content
        dic = json.loads(content)
        self.__req_param = req_param
        self.__req_data = req_data
        self.__code = dic['code'] if 'code' in dic else None
        self.__message = dic['message'] if 'message' in dic else None
        self.__data = dic['data'] if 'data' in dic else None
        self.__request_id = headers['request-id']

    def decrypt(self):
        if self.__data is None:
            return self

        if self.__des3key is not None and self.__req_param is not None \
                and 'data_type' in self.__req_param and \
                self.__req_param['data_type'] == 'encryption':
            self.__data = json.loads(decrypt(self.__des3key, self.__data))
        return self

    @property
    def code(self):
        return self.__code

    @property
    def message(self):
        return self.__message

    @property
    def data(self):
        return self.__data

    @property
    def content(self):
        return self.__content

    @property
    def request_id(self):
        return self.__request_id
