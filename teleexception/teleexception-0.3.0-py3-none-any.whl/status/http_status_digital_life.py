# -*- coding =utf-8 -*-
import logging
from enum import Enum

logger = logging.getLogger(__name__)


class HTTPStatusDigitalLife(Enum):
    """HTTP status codes and reason phrases
    Status codes from the following RFCs are all observed =
        * RFC 7231 = Hypertext Transfer Protocol (HTTP/1.1), obsoletes 2616
        * RFC 6585 = Additional HTTP Status Codes
        * RFC 3229 = Delta encoding in HTTP
        * RFC 4918 = HTTP Extensions for WebDAV, obsoletes 2518
        * RFC 5842 = Binding Extensions to WebDAV
        * RFC 7238 = Permanent Redirect
        * RFC 2295 = Transparent Content Negotiation in HTTP
        * RFC 2774 = An HTTP Extension Framework
    """
    def __new__(cls, value, phrase, description=''):
        obj = object.__new__(cls)
        obj._value_ = obj
        obj.code = value
        obj.phrase = phrase
        obj.description = description
        return obj

    @property
    def value(self):
        return self.code

    # 0 请求成功
    SUCCESS = (0, '请求成功', '请求成功')

    # 1001 参数错误
    PARAM_FORMAT_ERR = (1001, '参数错误', '参数错误')

    # 1002 请求异常
    REQUEST_ERR = (1002, "请求异常", "请求异常")

    # 1003 内部服务异常
    IMTERNAL_SERVICE_ERR = (1003, "内部服务异常", "内部服务异常")

    # 400004 请求体内容为空
    BODY_JSON_ERR = (400004, "请求体非 json 格式", "请求体内容需要符合 json 要求")

    # 1004 获取刷新地址异常
    REFRESH_SOURCE_URL_ERR = (1004, "获取刷新地址异常", "获取刷新地址异常")

    # 1005 上传文件异常
    UPLOAD_FILE_ERR = (1005, "上传文件异常", "上传文件异常")
    
    # 1006 图像等资源异常
    SOURCE_ERR = (1006, "图像等资源异常", "图像等资源异常")

    # 1007 流文件不合法
    STREAM_ILLEGAL_ERR = (1007, "流文件不合法", "流文件不合法")
    
    # 1008 算法编码错误
    ALGORITHM_CODE_ERR = (1008, "算法编码错误", "算法编码错误")
