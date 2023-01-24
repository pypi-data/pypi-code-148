# _*_ coding:utf-8 _*_

'''
@name: provider
@author: caimmy@hotmail.com
@date: 2022-12-03
@version: 1.0
@desc: 企业微信服务商相关能力封装
'''
import time
import tempfile
import os
import pickle
import json
from random import randint
from urllib.parse import quote

import requests
from .WXBizMsgCrypt import (
    WXBizMsgCrypt, 
    SHA1
)
from .helper import (
    QywxXMLParser
)
from ..helpers.char_helper import ensureString
from .base import (
    _QywxBase,
    QywxClient
)
from ..helpers.logger_helper import LoggerTimedRotating

logger = LoggerTimedRotating.getInstance("/tmp/dev.log")

class ProviderClient(_QywxBase):
    """
    服务商企业微信代理对象
    """
    def __init__(self, corpid: str, provider_secret: str):
        self._corpid = corpid
        self._corpsecret = provider_secret
        self._provider_access_token = ""
        self._provider_access_token_exptm = 0
        self.BaseClient = QywxClient(corpid, provider_secret)
        self.getProviderToken()
        

    def _refreshProviderToken(self):
        _req_url = "https://qyapi.weixin.qq.com/cgi-bin/service/get_provider_token"
        _, _token_result = self.BaseClient.postRequest(_req_url, {
            "corpid": self._corpid,
            "provider_secret": self._corpsecret
        })
        if isinstance(_token_result, dict) and "provider_access_token" in _token_result:
            _access_token = _token_result.get("provider_access_token")
            _expires_in = _token_result.get("expires_in")
            # 设置过期时间，比正常时间提前5分钟
            _exp_timestamp = int(
                time.time()) + (_expires_in - 300 if _expires_in > 300 else _expires_in)
            return {
                "exptm": _exp_timestamp,
                "access_token": _access_token
            }
        return None
    
    def getProviderToken(self) -> str:
        """
        获取服务商的access_token
        """
        ret_token = None
        ret_expiretm = 0
        _tmppath = tempfile.gettempdir()
        if not os.path.isdir(_tmppath):
            raise Exception("template path is invalid")
        _cache_token_file = os.path.join(_tmppath, f"{self._corpid}_{self._corpsecret}.bin")
        if os.path.isfile(_cache_token_file):
            with open(_cache_token_file, "rb") as f:
                _catched_data = pickle.load(f)
                if isinstance(_catched_data, dict) and "exptm" in _catched_data and _catched_data.get("exptm") > int(time.time()):
                    self._provider_access_token = ret_token = _catched_data.get("access_token")
                    self._provider_access_token_exptm = ret_expiretm = _catched_data.get("exptm")
        if not ret_token or ret_expiretm < int(time.time()):
            # 没有从缓存文件中成功加载token，重新刷新token
            _refresh_data = self._refreshProviderToken()
            if isinstance(_refresh_data, dict):
                self._provider_access_token = ret_token = _refresh_data.get("access_token")
                self._provider_access_token_exptm = ret_expiretm = _refresh_data.get("exptm")
                # 将刷新后的token写入缓存文件
                with open(_cache_token_file, "wb") as wf:
                    pickle.dump(_refresh_data, wf)
        return ret_token

    def postRequest(self, url: str, params: dict):
        _url = f"{url}?access_token={self.getProviderToken()}"
        try:
            _response = requests.post(_url, bytes(
                json.dumps(params, ensure_ascii=False), "utf-8"))
            if _response.ok:
                ret_data = _response.json()
                return self._checkReponse(ret_data)
        except Exception as e:
            return False, str(e)

    def getRequest(self, url: str, params: dict):
        _url = f"{url}?access_token={self.getProviderToken()}"
        try:
            _response = requests.get(_url, params=params)
            if _response.ok:
                ret_data = _response.json()
                return self._checkReponse(ret_data)
        except Exception as e:
            return False, str(e)

    def CallbackEchoStr(self, token: str, aeskey: str, msg_signature: str, timestamp: str, nonce: str, echostr: str, receiveid: str=None) -> str:
        """
        设置回调时解密响应口令
        在设置应用回调地址时使用
        @return str
        """
        if not receiveid: receiveid = self._corpid
        wxcpt = WXBizMsgCrypt(token, aeskey, receiveid)
        ret, sEchoStr = wxcpt.VerifyURL(
            msg_signature, timestamp, nonce, echostr)
        return sEchoStr if 0 == ret else None

    def CallbackEchoStrWithGetParams(self, token: str, aeskey: str, getparams: dict, receiveid: str=None):
        """
        回调时从dict获取解密参数
        """
        return self.CallbackEchoStr(token, aeskey, ensureString(getparams.get("msg_signature")),
                                    ensureString(getparams.get("timestamp")), ensureString(getparams.get("nonce")), ensureString(getparams.get("echostr")), receiveid)
    
    def ProxyParseUploadMessage(self, token: str, aeskey: str, params: dict, msgbody: str):
        """
        解析微信上行到应用服务器的消息
        适用于第三方开发或服务商代开应用
        @params: dict 验证参数 msg_signature, timestamp, nonce
        @msgbody: str 待解密消息体 echostr, 
        """
        ret_msg_struct = None
        sha1helper = SHA1()
        origin_encrypt_msg = QywxXMLParser.parseOriginEncryptMsg(msgbody)
        ret, check_sig = sha1helper.getSHA1(token, params.get(
            "timestamp"), params.get("nonce"), origin_encrypt_msg.Encrypt)
        if 0 == ret and check_sig == params.get("msg_signature"):
            # 提取加密数据字段
            str_callbackmsg = self.CallbackEchoStr(token, aeskey, params.get(
                "msg_signature"), params.get("timestamp"), params.get("nonce"), origin_encrypt_msg.Encrypt, origin_encrypt_msg.ToUserName)
            if str_callbackmsg:
                ret_msg_struct = QywxXMLParser.parseNormalCallbackData(
                    str_callbackmsg)
        return ret_msg_struct



class ProxySuiteUnit:
    """
    第三方代开发套件单元
    封装第三方代理开发应用相关的逻辑和api
    """
    def __init__(self, provider_id: str, provider_secret: str, corp_id: str, secret: str,  suite_id: str, suite_secret: str, token: str, aeskey: str):
        """
        :param provider_id: 服务商编号
        :param provider_secret: 服务商密钥
        :param corp_id: 使用企业的编号
        :param secret: 使用企业的永久性授权码
        :param suite_id: 代开模板（套件）编号
        :param suite_secret: 代开模板（套件）密钥
        :param token: 回调口令
        :param aeskey: 回调密钥
        """
        self._provider_client = ProviderClient(provider_id, provider_secret)
        self._corp_id = corp_id
        self._secret = secret
        self._suite_id = suite_id
        self._suite_secret = suite_secret
        self._suite_access_token = ""
        self._token = token
        self._aeskey = aeskey

    @classmethod
    def fromConfigure(cls, conf_params: dict):
        """
        从传入参数构造第三方代开发套件单元对象
        """
        _match_construct_condition = True
        for _k in ("provider_id", "provider_secret", "corp_id", "secret", "suite_id", "suite_secret", "token", "aeskey"):
            if not _k in conf_params:
                _match_construct_condition = False
                break
        if _match_construct_condition:
            return cls(
                provider_id = conf_params["provider_id"],
                provider_secret = conf_params["provider_secret"],
                corp_id = conf_params["corp_id"],
                secret = conf_params["secret"],
                suite_id = conf_params["suite_id"],
                suite_secret = conf_params["suite_secret"],
                token = conf_params["token"],
                aeskey = conf_params["aeskey"]
            )
        return None

    def postRequest(self, url: str, params: dict):
        try:
            _response = requests.post(url, bytes(
                json.dumps(params, ensure_ascii=False), "utf-8"))
            if _response.ok:
                return self._parseRequestResponse(_response.json())
        except Exception as e:
            return False, str(e)

    def getRequest(self, url: str, params: dict):
        try:
            _response = requests.get(url, params=params)
            if _response.ok:
                return self._parseRequestResponse(_response.json())
        except Exception as e:
            return False, str(e)

    def CallbackEchoStrWithGetParams(self, getparams: dict, receiveid: str=None):
        """
        回调时从dict获取解密参数
        """
        return self._provider_client.CallbackEchoStrWithGetParams(self._token, self._aeskey, getparams, receiveid)

    def ProxyParseUploadMessage(self, params: dict, msgbody: str):
        payload_package = self._provider_client.ProxyParseUploadMessage(self._token, self._aeskey, params, msgbody)
        logger.debug("payload_package")
        logger.debug(payload_package._data)
        # 处理suite_ticket回调消息，立刻更新suite_access_token
        _package_info_type = payload_package._data.get("InfoType", "")
        if _package_info_type == "suite_ticket":
            if self._suite_id == payload_package._data.get("SuiteId", ""):
                # 缓存最近一次suite_ticket
                self._storeSuiteAccessTicket(payload_package._data.get("SuiteTicket"), payload_package._data.get("TimeStamp", 0))

        return payload_package

    def getAuthPermanentCode(self, suite_id: str, auth_code: str):
        """
        接收到企业授权安装消息后调用，获取企业永久授权码及授权企业信息
        :param auth_code str 企业授权码
        """
        if suite_id == self._suite_id:
            _url = f"https://qyapi.weixin.qq.com/cgi-bin/service/get_permanent_code?suite_access_token={self.getSuiteAccessToken()}&"
            logger.debug(f"permanent_code: {_url} \n auth_code: {auth_code}")
            _, result = self._provider_client.postRequest(_url, {
                "auth_code": auth_code,
            })
            logger.debug(result)
            return result
        return None

    def _refreshSuiteAccessToken(self):
        """
        获取开发套件的访问凭据
        """
        _req_url = "https://qyapi.weixin.qq.com/cgi-bin/service/get_suite_token"
        _, _token_result = self._provider_client.postRequest(_req_url, {
            "suite_id": self._suite_id,
            "suite_secret": self._suite_secret, 
            "suite_ticket": self._retrieveSuiteAccessTicket()
        })
        if isinstance(_token_result, dict) and "suite_access_token" in _token_result:
            _access_token = _token_result.get("suite_access_token")
            _expires_in = _token_result.get("expires_in")
            # 设置过期时间，比正常时间提前5分钟
            _exp_timestamp = int(
                time.time()) + (_expires_in - 300 if _expires_in > 300 else _expires_in)
            return {
                "exptm": _exp_timestamp,
                "suite_access_token": _access_token
            }
        return None

    def _refreshProxyAccessToken(self, corp_id: str, secret: str):
        """
        获取开发套件的访问凭据
        """
        _req_url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corp_id}&corpsecret={secret}"
        _req_result = requests.get(_req_url)
        
        _token_result = _req_result.json() if _req_result.ok else None
        
        if isinstance(_token_result, dict) and "access_token" in _token_result:
            _access_token = _token_result.get("access_token")
            _expires_in = _token_result.get("expires_in")
            # 设置过期时间，比正常时间提前5分钟
            _exp_timestamp = int(
                time.time()) + (_expires_in - 300 if _expires_in > 300 else _expires_in)
            return {
                "exptm": _exp_timestamp,
                "suite_access_token": _access_token
            }
        return None

    def getAccessToken(self) -> str:
        """
        获取待开发授权应用的access_token
        """
        ret_token = None
        ret_expiretm = 0
        _tmppath = tempfile.gettempdir()
        if not os.path.isdir(_tmppath):
            raise Exception("template path is invalid")
        _cache_token_file = os.path.join(_tmppath, f"access_token_{self._corp_id}_{self._suite_id}.bin")
        if os.path.isfile(_cache_token_file):
            with open(_cache_token_file, "rb") as f:
                logger.debug("load access_token from cache file")
                _catched_data = pickle.load(f)
                logger.debug(_catched_data)
                if isinstance(_catched_data, dict) and "exptm" in _catched_data and _catched_data.get("exptm") > int(time.time()):
                    self._suite_access_token = ret_token = _catched_data.get("suite_access_token", "")
                    ret_expiretm = _catched_data.get("exptm")
        if not ret_token or ret_expiretm < int(time.time()):
            # 没有从缓存文件中成功加载token，重新刷新token
            _refresh_data = self._refreshProxyAccessToken(self._corp_id, self._secret)
            logger.debug("get suite_access_token from cache file")
            logger.debug(_refresh_data)
            if isinstance(_refresh_data, dict):
                self._suite_access_token = ret_token = _refresh_data.get("suite_access_token")
                # 将刷新后的token写入缓存文件
                with open(_cache_token_file, "wb") as wf:
                    pickle.dump(_refresh_data, wf)
        return ret_token

    def getSuiteAccessToken(self) -> str:
        """
        获取开发套件的访问凭据（启用本地缓存机制）
        """
        ret_token = None
        ret_expiretm = 0
        _tmppath = tempfile.gettempdir()
        if not os.path.isdir(_tmppath):
            raise Exception("template path is invalid")
        _cache_token_file = os.path.join(_tmppath, f"suite_token_{self._suite_id}.bin")
        if os.path.isfile(_cache_token_file):
            with open(_cache_token_file, "rb") as f:
                logger.debug("load access_token from cache file")
                _catched_data = pickle.load(f)
                logger.debug(_catched_data)
                if isinstance(_catched_data, dict) and "exptm" in _catched_data and _catched_data.get("exptm") > int(time.time()):
                    self._suite_access_token = ret_token = _catched_data.get("suite_access_token", "")
                    ret_expiretm = _catched_data.get("exptm")
        if not ret_token or ret_expiretm < int(time.time()):
            # 没有从缓存文件中成功加载token，重新刷新token
            _refresh_data = self._refreshSuiteAccessToken()
            logger.debug("get suite_access_token from cache file")
            logger.debug(_refresh_data)
            if isinstance(_refresh_data, dict):
                self._suite_access_token = ret_token = _refresh_data.get("suite_access_token")
                # 将刷新后的token写入缓存文件
                with open(_cache_token_file, "wb") as wf:
                    pickle.dump(_refresh_data, wf)
        return ret_token

    def _storeSuiteAccessTicket(self, ticket: str, timestamp: int):
        """
        暂存开发套件的访问ticket
        """
        _tmppath = tempfile.gettempdir()
        if not os.path.isdir(_tmppath):
            raise Exception("template path is invalid")
        _cache_token_file = os.path.join(_tmppath, f"suite_ticket_{self._suite_id}.bin")
        with open(_cache_token_file, "wb") as wf:
            pickle.dump({
                "suite_id": self._suite_id,
                "suite_ticket": ticket,
                "timestamp": timestamp
            }, wf)
        return True

    def _retrieveSuiteAccessTicket(self):
        """
        取回暂存的开发套件ticket
        """
        _tmppath = tempfile.gettempdir()
        if not os.path.isdir(_tmppath):
            raise Exception("template path is invalid")
        _cache_token_file = os.path.join(_tmppath, f"suite_ticket_{self._suite_id}.bin")
        with open(_cache_token_file, "rb") as rf:
            _catched_data = pickle.load(rf)
            return _catched_data.get("suite_ticket")

    def _parseRequestResponse(self, respjson: dict):
        ret_check = False
        
        if isinstance(respjson, dict) and "errcode" in respjson and respjson["errcode"] == 0:
            ret_check = True
                
        return ret_check, respjson

    def _loadSendmsgParams(self, agentid: str, msgtype: str, args: dict) -> dict:
        """
        针对发送消息请求，构造基本请求参数
        """
        touser = args.get("touser") if "touser" in args else []
        toparty = args.get("toparty") if "toparty" in args else []
        totag = args.get("totag") if "totag" in args else []
        safe = args.get("safe") if "safe" in args else 0
        _params = {
            "touser": "|".join(touser),
            "toparty": "|".join(toparty),
            "totag": "|".join(totag),
            "msgtype": msgtype,
            "agentid": agentid,
            "safe": safe,
            "enable_id_trans": 0,
            "enable_duplicate_check": 0,
            "duplicate_check_interval": 1800
        }
        return _params

    def getCorpAuthInfo(self):
        """
        获取授权企业信息
        :param corpid str 企业编号
        :param secret str 企业永久授权码 permanent_code
        """
        _url = f"https://qyapi.weixin.qq.com/cgi-bin/service/get_auth_info?suite_access_token={self.getSuiteAccessToken()}"
        return self.postRequest(_url, {
            "auth_corpid": self._corp_id,
            "permanent_code": self._secret
        })

    def code2UserId(self, code: str):
        """
        从oauth2认证码转用户编号
        :param code str oauth2登录认证码
        """
        _url = f"https://qyapi.weixin.qq.com/cgi-bin/auth/getuserinfo?access_token={self.getAccessToken()}&code={code}"
        logger.debug(_url)
        return self.getRequest(_url, {})

    def getOauth2RedirectUrl(self, url: str, agentid: str, state: str=None):
        """
        构造oauth2认证跳转连接
        :param url: 实际的业务地址
        :param state: 登录状态码
        """
        if not state: state = randint(100, 1000000)
        _redirectUrl = quote(url)
        return f"https://open.weixin.qq.com/connect/oauth2/authorize?appid={self._corp_id}&redirect_uri={_redirectUrl}&response_type=code&scope=snsapi_base&state={state}&agentid={agentid}#wechat_redirect"

    def getOrganization(self):
        """
        获取组织架构
        """
        _url = f"https://qyapi.weixin.qq.com/cgi-bin/department/list?access_token={self.getAccessToken()}"
        _ret, _orgnization_tree = self.getRequest(_url, {})
        _department_tree = []
        if _ret:
            # 解析全量组织架构
            logger.info(_department_tree)
            _origin_department_list = _orgnization_tree.get("department")
            _origin_dep_array = {}
            for _dep in _origin_department_list:
                _cur_parent_id = _dep["parentid"]
                if not _cur_parent_id in _origin_dep_array:
                    _origin_dep_array[_cur_parent_id] = []
                _origin_dep_array[_cur_parent_id].append(_dep)
            return True, self._make_orgnization_tree(0, _origin_dep_array)
        else:
            return False, _orgnization_tree
        
    def _make_orgnization_tree(self, parentid: int, dep_tree: dict):
        """
        在内存中构造组织架构树
        """
        if parentid in dep_tree:
            dep_tree[parentid] = sorted(dep_tree[parentid], key=lambda x: x["order"], reverse=True)
            _level_nodes = []
            for _dep in dep_tree[parentid]:
                _dep["children"] = self._make_orgnization_tree(_dep["id"], dep_tree)
                _level_nodes.append(_dep)
            return _level_nodes
        else:
            return []


    def getFullDepartmentTree(self):
        """
        获取完整的组织架构树
        该方法存在循环调用接口的机制，效率极低。
        """
        _ret, _dep_tree = self.getDepartmentSimpleList()
        _department_tree = []
        if _ret:
            for _dep_node in _dep_tree["department_id"]:
                _chk, _depinfor = self.getDepartmentInfor(_dep_node["id"])
                if _chk:
                    _department_tree.append(_depinfor["department"])
        return _department_tree

    def getDepartmentSimpleList(self, depid: int=0):
        """
        获取部门的编号及上下级信息
        """
        _url = f"https://qyapi.weixin.qq.com/cgi-bin/department/simplelist?access_token={self.getAccessToken()}"
        logger.debug(_url)
        if depid:
            _url += f"&id={depid}"
        return self.getRequest(_url, {})

    def getDepartmentInfor(self, depid: int):
        """
        获取部门详细信息
        :param depid int 部门编号
        """
        _url = f"https://qyapi.weixin.qq.com/cgi-bin/department/get?access_token={self.getAccessToken()}&id={depid}"
        return self.getRequest(_url, {})

    def getDepartmentUsers(self, depid: int):
        """
        获取指定部门下所有用户的信息
        """
        _url = f"https://qyapi.weixin.qq.com/cgi-bin/user/list?access_token={self.getAccessToken()}&department_id={depid}"
        return self.getRequest(_url, {})

    def getUserInfor(self, user_id: str):
        """
        获取企业用户信息
        :param user_id str 用户编号（openid）
        """
        _url = f"https://qyapi.weixin.qq.com/cgi-bin/user/get?access_token={self.getAccessToken()}&userid={user_id}"
        return self.getRequest(_url, {})

    def mobile2UserId(self, mobile: str):
        """
        通过手机号码获取用户账号
        :param mobile: str 手机号码
        """
        _url = f"https://qyapi.weixin.qq.com/cgi-bin/user/getuserid?access_token={self.getAccessToken()}"
        return self.postRequest(_url, {
            "mobile": mobile
        })

    def MsgSendText(self, agentid: int, content: str, **kwargs):
        """
        发送文本消息
        """
        _params = self._loadSendmsgParams(agentid, "text", kwargs)
        _params["text"] = {
            "content": content
        }

        return self.postRequest(f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={self.getAccessToken()}", params=_params)

    def MsgSendImage(self, agentid: int, img_content, **kwargs):
        """
        发送图片消息
        首先调用 [上传临时素材接口] 获取图片的media_id，
        然后再发送消息
        """
        media_id = self.UploadTempMedia("image", content=img_content)
        if media_id:
            _params = self._loadSendmsgParams(agentid, "image", kwargs)
            _params["image"] = {
                "media_id": media_id
            }
            return self.postRequest(f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={self.getAccessToken()}", params=_params)
        else:
            return {
                "errcode": -1,
                "errmsg": "没有获取到有效的media_id"
            }

    def MsgSendTextCard(self, agentid: int, title: str, description: str, url: str, btntxt: str = "更多", **kwargs):
        """
        发送文本卡片消息
        """
        _params = self._loadSendmsgParams(agentid, "textcard", kwargs)
        _params["textcard"] = {
            "title": title,
            "description": description,
            "url": url,
            "btntxt": btntxt
        }
        return self.postRequest(f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={self.getAccessToken()}", params=_params)

    def MsgSendMarkdown(self, agentid: int, markdown: str, **kwargs):
        """
        发送markdown消息
        """
        _params = self._loadSendmsgParams(agentid, "markdown", kwargs)
        _params["markdown"] = {
            "content": markdown
        }

        return self.postRequest(f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={self.getAccessToken()}", params=_params)