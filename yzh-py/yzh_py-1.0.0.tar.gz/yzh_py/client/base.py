import platform
import uuid

import requests

from .. import __version__
from ..message import *


class BaseClient(object):
    def __init__(self, config, timeout=30):
        """
        :type config: Config
        :param config: 配置信息

        :type timeout: int
        :param timeout: 非必填
        """

        encrypt_type = config.sign_type
        if encrypt_type != "sha256" and encrypt_type != "rsa":
            raise ValueError('wrong encrypt type')

        self.__des3key = config.des3key
        self.__encrypt = None
        if encrypt_type == "sha256":
            self.__encrypt = EncryptHmac(
                config.app_key, config.des3key)
        if encrypt_type == "rsa":
            self.__encrypt = EncryptRsa(
                config.app_key, config.public_key, config.private_key, config.des3key)

        self.__dealer_id = config.dealer_id
        self.__base_url = config.host
        self.__timeout = timeout

    def __header(self, request_id):
        if type(request_id) is not str or request_id == "":
            request_id = str(int(time.time()))
        return {
            'dealer-id': self.__dealer_id,
            'request-id': request_id,
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "yunzhanghu-sdk-python/%s/%s/%s" % (
                __version__, platform.platform(), platform.python_version()),
        }

    def __request(self, method, url, **kwargs):
        data = kwargs['data'] if 'data' in kwargs else None
        param = kwargs['param'] if 'param' in kwargs else None
        headers = self.__header(kwargs['request_id'])
        return self.__handle_resp(
            data, param, headers,
            requests.request(method=method,
                             url=self.__base_url + url,
                             headers=headers,
                             data=ReqMessage(self.__encrypt, data).pack(),
                             params=ReqMessage(self.__encrypt, param).pack(),
                             timeout=self.__timeout))

    def _post(self, url, request_id, data):
        kwargs = {'data': data, 'request_id': request_id}
        return self.__request(method='POST', url=url, **kwargs)

    def _get(self, url, request_id, param):
        kwargs = {'param': param, 'request_id': request_id}
        return self.__request(method='GET', url=url, **kwargs)

    def __handle_resp(self, req_data, req_param, headers, resp):
        if resp is None:
            raise ValueError('resp is None')

        # 抛出status异常
        resp.raise_for_status()
        return RespMessage(self.__des3key, resp.text, req_data,
                           req_param, headers).decrypt()


class BaseRequest(object):
    def __init__(self):
        self.__request_id = uuid.uuid1()

    @property
    def request_id(self):
        """ Get 请求ID

        :return: str, dealer_id
        """
        if self.__request_id is None or self.__request_id == "":
            self.__request_id = uuid.uuid1()
        return self.__request_id.__str__()

    @request_id.setter
    def request_id(self, request_id):
        """ Set 请求ID

        :type request_id: str
        :param request_id: 请求ID
        """
        self.__request_id = request_id
