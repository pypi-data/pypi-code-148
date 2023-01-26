# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rpc_call']

package_data = \
{'': ['*']}

install_requires = \
['aio-pika>=8.3.0,<9.0.0',
 'loguru>=0.6.0,<0.7.0',
 'orjson>=3.8.5,<4.0.0',
 'pika>=1.3.1,<2.0.0',
 'pydantic>=1.10.4,<2.0.0',
 'simplejson>=3.18.1,<4.0.0']

entry_points = \
{'console_scripts': ['client = tests.simple_client:run',
                     'server = tests.simple_server:run']}

setup_kwargs = {
    'name': 'rpc-call',
    'version': '0.1.1',
    'description': '',
    'long_description': '> **Note**\n> TThe main idea of the project is based on RabbitMQ RPC, so RabbitMQ must be installed. Keep it mind.\n\n### Get started\n-------------\n#### *Simple RPC client using FastAPI*\n\n\n#### **`server.py`**\n\n```python\nimport asyncio\nfrom fastapi import FastAPI, Depends, status\nfrom rpc_call.async_client import RPCClient\nfrom rpc_call.types import Task, TaskResult\n\napp = FastAPI()\n\nasync def rpc_connection() -> RPCClient:\n    return await RPCClient(\n        amqp_dsn = "<amqp://login:password@host:port/vhost>",\n        queue_name = "<RabbitMQQueueName>"\n    ).connect()\n\n@app.post("/RPCEndpoint", response_model=TaskResult)\nasync def read_users(task: Task, rpc_conn: RPCClient = Depends(rpc_connection)) -> TaskResult:\n    task_result = await rpc_conn.call(task)\n    return task_result\n```\n\n```shell\n$ python server.py\n```\n\n-------------\n#### *Simple RPC server*\n\n#### **`client.py`**\n\n```python\nfrom rpc_call.server import RPCServer\n\nclass CallbackHandler:\n    def test_func(self, arg1: str) -> str:\n        return "test_func rpc result"\n\nif __name__ == "__main__":\n    RPCServer(\n        amqp_dsn = "<amqp://login:password@host:port/vhost>",\n        queue_name = "<RabbitMQQueueName>",\n        callback_handler = CallbackHandler\n    )\n```\n\n```bash\n$ uvicorn client:app --host 0.0.0.0 --port 8000 --reload\n```\n',
    'author': 'Artyom Syssolov',
    'author_email': 'artyom.syssolov1@homecredit.kz',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
