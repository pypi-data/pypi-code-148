# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ha_mqtt']

package_data = \
{'': ['*']}

install_requires = \
['paho-mqtt>=1.6,<2.0']

setup_kwargs = {
    'name': 'homeassistant-mqtt-binding',
    'version': '2.0.2',
    'description': 'Bindings to implement arbitrary homeassistant devices in python using mqtt as interface',
    'long_description': "# Homeassistant MQTT Binding for python\n\nThis package enables you to implement arbitrary devices in python supported in homeassistant. The communication with\nhomeassistant is handled by MQTT. For example you could write an simple program running on a raspberry pi controlling an\nLED. By exposing this configuration to homeassistant you can easily control the LED via HA.\n\nThe base class handles the following things automatically:\n\n* registering devices in homeassistant through the mqtt discovery protocol\n* setting the device as available once fully setup\n* setting the device unavailable when quitting the application\n\n### Installation\n\n`python3 -m pip install homeassistant-mqtt-binding`\nthe dependencies should be installed automatically\n\n### Usage\n\n1. create an paho mqtt Client instance connected to your mqtt server\n2. instantiate your desired device and pass the Client instance to the constructor\n3. when your program closes make sure to call the `close()` function of each device for cleanup\n\n### Examples\n\nThe following examples require an already running stack of homeassistant and an MQTT server.  \nSee the [examples](https://gitlab.com/anphi/homeassistant-mqtt-binding/HaMqtt/examples) folder for all demo scripts.\n\n* switch.py:\n  simple switch device that can be toggled by homeassistant\n\n### Expanding the application\n\nSince I don't use all devices I haven't implemented them yet. You can easily implement any missing device:\n\n1. create an empty class subclassing any of the devices (normally you would subclass `MQTTDevice` or `MQTTSensor`).\n2. implement the `pre_discovery()` if necessary:  \n   It gets called before sending out the discovery payload to the broker. This is the right place to place custom config\n   options for the config\n   dictionary via `add_config_option()`\n3. implement the `post_discovery()` if necessary:  \n   It gets called right after sending out the discovery payload to the broker. Use it to send initial values to HA, if\n   it is necessary that\n   HA knows about the device beforehand.\n4. Implement any callbacks that might be necessary for all devices that can receive data. (commands for switches for\n   example).\n5. If your device needs more topics than state, configuration and set, feel free to implement them additionally.",
    'author': 'Andreas Philipp',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab.com/anphi/homeassistant-mqtt-binding',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
