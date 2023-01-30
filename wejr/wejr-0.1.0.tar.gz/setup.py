# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wejr', 'wejr.jsonrpc', 'wejr.utils']

package_data = \
{'': ['*']}

install_requires = \
['channels>=4.0.0,<5.0.0']

extras_require = \
{'channel-layer': ['channels-redis>=4.0.0,<5.0.0']}

setup_kwargs = {
    'name': 'wejr',
    'version': '0.1.0',
    'description': 'Communication via websocket in JSON-RPC way',
    'long_description': '# [WIP] Websocket by JSON-RPC protocol for Django Channels\n\nLibrary for using websocket in django(with channels) in jsonrpc way\n\n### JSON-RPC specification\nhttps://www.jsonrpc.org/specification\n\n## Installing\nWIP\n\n## Usage example\n\n\nAdd wejr to django INSTALLED_APPS before your apps\n```python\nINSTALLED_APPS = [\n    ...\n    "wejr",\n    ...\n]\n```\n    \n\nConfigure channel layer via Redis PubSub\n```python\nCHANNEL_LAYERS = {\n    "default": {\n        "BACKEND": "channels_redis.pubsub.RedisPubSubChannelLayer",\n        "CONFIG": {\n            "hosts": [("localhost", 6379)],\n        },\n    },\n}\n```\n\nDefine routers, methods, params schemas\n```python\nfrom dataclasses import dataclass, asdict\nfrom wejr.router import Router\n\n@dataclass\nclass ChatId:\n    id: int\n\n@dataclass\nclass MessageCreated:\n    author_id: int\n    content: str\n    chat_id: int\n\nclient = Router()\nchat = Router()\n\n@client.method\nasync def chat_by_id(consumer, request, params: ChatId):\n    chat = get_chat_data(params.id)\n    consumer.send_result(request, chat)\n\n@chat.method\nasync def message_created(consumer, request, params: MessageCreated):\n    consumer.send_notification("", asdict(params))\n```\n\n\nDefine consumer\n```python\nfrom wejr.consumers import AsyncBaseJsonRpcConsumer\nfrom myproject.app.routers import client, chat\n\nclass MyConsumer(AsyncBaseJsonRpcConsumer):\n    client_router = client\n    group_routers = {\n        "chat": chat,\n    }\n```\n\nDefine urls\n```python\nurlpatterns = [\n    re_path(r"v1/ws", MyConsumer.as_asgi()),\n]\n```\n\nExtend asgi with websocket\n```python\nfrom channels.routing import ProtocolTypeRouter, URLRouter\nfrom django.core.asgi import get_asgi_application\n\nfrom djangochatws.apps.threadws import urls as ws_urls\n\napplication = ProtocolTypeRouter(\n    {\n        "http": get_asgi_application(),\n        "websocket": AuthMiddlewareStack(\n            URLRouter(ws_urls.urlpatterns)\n        )\n    }\n)\n```\n',
    'author': 'Wasth',
    'author_email': 'riasta@yandex.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
