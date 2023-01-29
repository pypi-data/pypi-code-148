# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_mqtt']

package_data = \
{'': ['*']}

install_requires = \
['fastapi<1.0.0',
 'gmqtt>=0.6.11,<0.7.0',
 'pydantic>=1.9.0,<2.0.0',
 'uvicorn>=0.19.0']

setup_kwargs = {
    'name': 'fastapi-mqtt',
    'version': '1.7',
    'description': 'fastapi-mqtt is extension for MQTT protocol',
    'long_description': '# fastapi-mqtt\n\nMQTT is a lightweight publish/subscribe messaging protocol designed for M2M (machine to machine) telemetry in low bandwidth environments.\nFastapi-mqtt is the client for working with MQTT.\n\nFor more information about MQTT, please refer to here: [MQTT](MQTT.md)\n\nFatapi-mqtt wraps around [gmqtt](https://github.com/wialon/gmqtt) module. Gmqtt Python async client for MQTT client implementation.\nModule has support of MQTT version 5.0 protocol\n\n[![MIT licensed](https://img.shields.io/github/license/sabuhish/fastapi-mqtt)](https://raw.githubusercontent.com/sabuhish/fastapi-mqtt/master/LICENSE)\n[![GitHub stars](https://img.shields.io/github/stars/sabuhish/fastapi-mqtt.svg)](https://github.com/sabuhish/fastapi-mqtt/stargazers)\n[![GitHub forks](https://img.shields.io/github/forks/sabuhish/fastapi-mqtt.svg)](https://github.com/sabuhish/fastapi-mqtt/network)\n[![GitHub issues](https://img.shields.io/github/issues-raw/sabuhish/fastapi-mqtt)](https://github.com/sabuhish/fastapi-mqtt/issues)\n[![Downloads](https://pepy.tech/badge/fastapi-mqtt)](https://pepy.tech/project/fastapi-mqtt)\n\n---\n\n## **Documentation**: [FastApi-MQTT](https://sabuhish.github.io/fastapi-mqtt/)\n\nThe key feature are:\n\nMQTT specification avaliable with help decarator methods using callbacks:\n\n- on_connect()\n- on_disconnect()\n- on_subscribe()\n- on_message()\n- subscribe(topic)\n\n- Base Settings available with `pydantic` class\n- Authetication to broker with credentials\n- unsubscribe certain topics and publish to certain topics\n\n### 🔨 Installation\n\n```sh\n $ pip install fastapi-mqtt\n```\n\n### 🕹 Guide\n\n```python\nfrom fastapi import FastAPI\nfrom fastapi_mqtt import FastMQTT, MQTTConfig\n\napp = FastAPI()\n\nmqtt_config = MQTTConfig()\n\nmqtt = FastMQTT(\n    config=mqtt_config\n)\n\nmqtt.init_app(app)\n\n\n\n@mqtt.on_connect()\ndef connect(client, flags, rc, properties):\n    mqtt.client.subscribe("/mqtt") #subscribing mqtt topic\n    print("Connected: ", client, flags, rc, properties)\n\n@mqtt.on_message()\nasync def message(client, topic, payload, qos, properties):\n    print("Received message: ",topic, payload.decode(), qos, properties)\n\n@mqtt.subscribe("my/mqtt/topic/#")\nasync def message_to_topic(client, topic, payload, qos, properties):\n    print("Received message to specific topic: ", topic, payload.decode(), qos, properties)\n\n@mqtt.on_disconnect()\ndef disconnect(client, packet, exc=None):\n    print("Disconnected")\n\n@mqtt.on_subscribe()\ndef subscribe(client, mid, qos, properties):\n    print("subscribed", client, mid, qos, properties)\n\n```\n\nPublish method:\n\n```python\nasync def func():\n    mqtt.publish("/mqtt", "Hello from Fastapi") #publishing mqtt topic\n\n    return {"result": True,"message":"Published" }\n\n\n```\n\nSubscribe method:\n\n```python\n\n@mqtt.on_connect()\ndef connect(client, flags, rc, properties):\n    mqtt.client.subscribe("/mqtt") #subscribing mqtt topic\n    print("Connected: ", client, flags, rc, properties)\n\n```\n\nChanging connection params\n\n```python\nmqtt_config = MQTTConfig(host = "mqtt.mosquito.org",\n    port= 1883,\n    keepalive = 60,\n    username="username",\n    password="strong_password")\n\n\nmqtt = FastMQTT(\n    config=mqtt_config)\n\n```\n\n# Contributing\n\nFell free to open issue and send pull request.\n\nThanks To [Contributors](https://github.com/sabuhish/fastapi-mqtt/graphs/contributors).\nContributions of any kind are welcome!\n\nBefore you start please read [CONTRIBUTING](https://github.com/sabuhish/fastapi-mqtt/blob/master/CONTRIBUTING.md)\n',
    'author': 'sabuhish',
    'author_email': 'sabuhi.shukurov@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/sabuhish/fastapi-mqtt',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
