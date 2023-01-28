# encoding: utf-8
"""
-------------------------------------------------
@author: haohe
@email: haohe@nocode.com
@software: PyCharm
@file: __init__.py
@time: 2023/1/28 14:16
@description:
-------------------------------------------------
"""
from nocode_utils.http_utils import http_post
from functools import wraps
import json
import inspect
from datetime import datetime

info_template = {
    "config": {
        "wide_screen_mode": True
    },
    "header": {
        "title": {
            "tag": "plain_text",
            "content": "通知"
        },
        "template": "blue"
    },
    "elements": [{
        "tag": "markdown",
        "content": ""
    }]
}

alert_template = {
    "config": {
        "wide_screen_mode": True
    },
    "header": {
        "title": {
            "tag": "plain_text",
            "content": "警报"
        },
        "template": "red"
    },
    "elements": [{
        "tag": "div",
        "fields": [
            {
                "is_short": False,
                "text": {
                    "tag": "lark_md",
                    "content": "**函数路径：**\n"
                }
            },
            {
                "is_short": False,
                "text": {
                    "tag": "lark_md",
                    "content": ""
                }
            },
            {
                "is_short": True,
                "text": {
                    "tag": "lark_md",
                    "content": "**函数名称：**\n"
                }
            },
            {
                "is_short": True,
                "text": {
                    "tag": "lark_md",
                    "content": "**时间：**\n"
                }
            },
            {
                "is_short": False,
                "text": {
                    "tag": "lark_md",
                    "content": ""
                }
            },
            {
                "is_short": False,
                "text": {
                    "tag": "lark_md",
                    "content": "**警报信息**\n"
                }
            }
        ]
    }]
}


def get_tenant_access_token(app_id, app_secret):
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    data = {
        "app_id": app_id,
        "app_secret": app_secret
    }
    tenant_access_token = http_post(url, data=data)['tenant_access_token']
    return tenant_access_token


def get_user_openid(emails, tenant_access_token):
    url = "https://open.feishu.cn/open-apis/contact/v3/users/batch_get_id?user_id_type=open_id"
    headers = {
        "Authorization": "Bearer " + tenant_access_token,
    }
    data = {"emails": emails}
    re = http_post(url, data, headers=headers)

    user_openids = []
    for user in re['data']['user_list']:
        user_openids.append(user['user_id'])
    return user_openids


def send_message(open_id, tenant_access_token, msg):
    url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id"
    headers = {
        "Authorization": "Bearer " + tenant_access_token,
    }
    data = {
        "receive_id": open_id,
        "msg_type": "interactive",
        "content": json.dumps(msg),
    }
    _ = http_post(url, data, headers)


def feishubot_alert(app_id, app_secret, emails, content):
    """
    用于发送飞书机器人警报，警报会包括文件和函数信息
    :param app_id:
    :param app_secret:
    :param emails: 用户邮箱列表
    :param content:
    :return:
    """
    tenant_access_token = get_tenant_access_token(app_id, app_secret)
    r = get_user_openid(emails, tenant_access_token)

    stack = inspect.stack()
    # 获取调用b函数的函数信息
    caller_frame = stack[1]
    frame_info = inspect.getframeinfo(caller_frame[0])
    path = frame_info.filename
    function_name = frame_info.function
    line_number = frame_info.lineno

    msg = alert_template
    # 文件路径
    msg['elements'][0]['fields'][0]['text']['content'] += path
    # 函数名称
    msg['elements'][0]['fields'][2]['text']['content'] += function_name + ":" + str(line_number)
    # 时间
    msg['elements'][0]['fields'][3]['text']['content'] += datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    # 信息
    msg['elements'][0]['fields'][5]['text']['content'] += str(content)

    for open_id in r:
        send_message(open_id, tenant_access_token, msg)


def feishubot_info(app_id, app_secret, emails, content):
    """
    用于发送飞书机器人消息
    :param app_id:
    :param app_secret:
    :param emails: 用户邮箱列表
    :param content:
    :return:
    """
    tenant_access_token = get_tenant_access_token(app_id, app_secret)
    r = get_user_openid(emails, tenant_access_token)

    msg = info_template
    msg['elements'][0]['content'] = str(content)

    for open_id in r:
        send_message(open_id, tenant_access_token, msg)


if __name__ == "__main__":
    app_id = "cli_a33507c352b9900d"
    app_secret = "4skVjTVX0PQUssK8FVbBhYBpy5F6qeat"


    def test_func():
        try:
            a = 1 / 0
            return a
        except Exception as e:
            feishubot_alert(app_id, app_secret, ["haohe@nocode.com"], e)
            return 0


    print("res: ", test_func())
