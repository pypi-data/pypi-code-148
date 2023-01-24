# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['amqp_client_python',
 'amqp_client_python.domain.models',
 'amqp_client_python.event',
 'amqp_client_python.exceptions',
 'amqp_client_python.rabbitmq',
 'amqp_client_python.utils']

package_data = \
{'': ['*']}

install_requires = \
['pika>=1.3.0,<2.0.0']

setup_kwargs = {
    'name': 'amqp-client-python',
    'version': '0.1.4',
    'description': '',
    'long_description': '# AMQP Client Python\n\n[![License][license-image]][license-url]\n<a href="https://pypi.org/project/amqp-client-python" target="_blank">\n    <img src="https://img.shields.io/pypi/v/amqp-client-python?color=%2334D058&label=pypi%20package" alt="Package version">\n</a><a href="https://pypi.org/project/amqp-client-python" target="_blank">\n    <img src="https://img.shields.io/pypi/pyversions/amqp-client-python.svg?color=%2334D058" alt="Supported Python versions">\n</a>\n[![Downloads](https://static.pepy.tech/personalized-badge/amqp-client-python?period=month&units=international_system&left_color=black&right_color=orange&left_text=PyPI%20downloads%20per%20month)](https://pepy.tech/project/amqp-client-python)\n[![Vulnerabilities][known-vulnerabilities-image]][known-vulnerabilities-url]  [![Releases][releases-image]][releases-url] \n\n\n\n\n--------\nClient with high level of abstraction for manipulation of messages in the event bus RabbitMQ.\n\n### Features:\n- Automatic creation and management of queues, exchanges and channels;\n- Support for **direct**, **topic** and **fanout** exchanges;\n- Publish;\n- Subscribe;\n- Support for a Remote procedure call _(RPC)_.\n\n\n[//]: # (These are reference links used in the body of this note.)\n[license-image]: https://img.shields.io/badge/license-Apache%202-blue.svg\n[license-url]: https://github.com/nutes-uepb/amqp-client-python/blob/master/LICENSE\n[npm-image]: https://img.shields.io/npm/v/amqp-client-python.svg?color=red&logo=npm\n[npm-url]: https://npmjs.org/package/amqp-client-python\n[downloads-image]: https://img.shields.io/npm/dt/amqp-client-python.svg?logo=npm\n[travis-url]: https://travis-ci.org/nutes-uepb/amqp-client-python\n[coverage-image]: https://coveralls.io/repos/github/nutes-uepb/amqp-client-python/badge.svg\n[coverage-url]: https://coveralls.io/github/nutes-uepb/amqp-client-python?branch=master\n[known-vulnerabilities-image]: https://snyk.io/test/github/nutes-uepb/amqp-client-python/badge.svg?targetFile=requirements.txt\n[known-vulnerabilities-url]: https://snyk.io/test/github/nutes-uepb/amqp-client-python?targetFile=requirements.txt\n[releases-image]: https://img.shields.io/github/release-date/nutes-uepb/amqp-client-python.svg\n[releases-url]: https://github.com/nutes-uepb/amqp-client-python/releases\n\n### Examples:\n- basic usage\n    ```Python\n    # basic configuration\n    from amqp_client_python import (\n        AsyncEventbusRabbitMQ,\n        Config, Options\n    )\n    from amqp_client_python.event import IntegrationEvent, IntegrationEventHandler\n    config = Config(Options("queue", "rpc_queue", "rpc_exchange"))\n    eventbus = AsyncEventbusRabbitMQ(config)\n    # publish\n    class ExampleEvent(IntegrationEvent):\n        EVENT_NAME: str = "ExampleEvent"\n        def __init__(self, event_type: str, message = []) -> None:\n            super().__init__(self.EVENT_NAME, event_type)\n            self.message = message\n\n    publish_event = ExampleEvent(rpc_exchange, ["message"])\n    eventbus.publish(publish_event, rpc_routing_key, "direct")\n    # subscribe\n    class ExampleEventHandler(IntegrationEventHandler):\n        def handle(self, body) -> None:\n            print(body) # handle messages\n    await eventbus.subscribe(subscribe_event, subscribe_event_handle, rpc_routing_key)\n    # rpc_publish\n    response = await eventbus.rpc_client(rpc_exchange, "user.find", ["content_message"])\n    # provider\n    async def handle2(*body) -> bytes:\n        print(f"body: {body}")\n        return b"content"\n    await eventbus.provide_resource("user.find", handle)\n    ```\n',
    'author': 'NUTES UEPB',
    'author_email': 'dev.seniorsaudemovel@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
