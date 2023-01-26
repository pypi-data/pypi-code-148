# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['helyos_agent_sdk']

package_data = \
{'': ['*']}

install_requires = \
['dataclasses-json>=0.5.7,<0.6.0',
 'pika>=1.3.1,<2.0.0',
 'pycryptodome>=3.15.0,<4.0.0']

setup_kwargs = {
    'name': 'helyos-agent-sdk',
    'version': '0.1.5',
    'description': '',
    'long_description': '<div id="top"></div>\n\n<!-- PROJECT LOGO -->\n<br />\n<div align="center">\n  <a href="https://github.com/">\n    <img src="helyos_logo.png" alt="Logo"  height="80">\n    <img src="truck.png" alt="Logo"  height="80">\n  </a>\n\n  <h3 align="center">helyOS Agent SDK</h3>\n\n  <p align="center">\n    Methods and data strrctures to connect autonomous vehicles to helyOS.\n    <br />\n    <a href="https://fraunhoferivi.github.io/helyOS-agent-sdk/"><strong>Explore the docs »</strong></a>\n    <br />\n    <br />\n    <a href="https://github.com/">View Demo</a>\n    ·\n    <a href="https://github.com/FraunhoferIVI/helyOS-agent-sdk/issues">Report Bug</a>\n    ·\n    <a href="https://github.com/FraunhoferIVI/helyOS-agent-sdk/issues">Request Feature</a>\n  </p>\n</div>\n\n## About The Project\n\nThe helyos-agent-sdk python package encloses methods and data structures definitions that facilitate the connection to helyOS core through rabbitMQ.\n\n### List of features\n\n*   RabbitMQ client to communicate with helyOS. \n*   Check-in method.\n*   Agent and assignment status definitions. \n*   Easy access to helyOS assignments via callbacks. \n*   Application-level encryption.\n\n### Install\n\n```\npip install helyos_agent_sdk\n\n```\n### Usage\n\n```python\nos.environ[\'AGENTS_UL_EXCHANGE\'] = "xchange_helyos.agents.ul"\nos.environ[\'AGENTS_DL_EXCHANGE\'] = "xchange_helyos.agents.dl"\nos.environ[\'AGENT_ANONYMOUS_EXCHANGE\'] = "xchange_helyos.agents.anonymous"\nfrom helyos_agent_sdk import HelyOSClient, AgentConnector\n\n# Check in\nhelyOS_client = HelyOSClient(rabbitmq_host, rabbitmq_port, uuid=AGENT_UID)\nhelyOS_client.perform_checkin(yard_uid=\'1\', agent_data=agent_data, status="free")\nhelyOS_client.get_checkin_result()\n\n\n# Communication\nagent_connector = AgentConnector(helyOS_client)\nagent_connector.publish_sensors(x=-30167, y=3000, z=0, orientations=[1500, 0], sensor= {"my_sensor": 12})\n\n# ... #\n\nagentConnector.publish_state(status, resources, assignment_status)\n\n# ... #\n\nagentConnector.consume_instant_action_messages(my_reserve_callback, my_release_callback, my_cancel_assignm_callback, any_other_callback)\nagentConnector.consume_assignment_messages(my_assignment_callback)\nagentConnector.start_consuming()\n\n\n```\n\n\n### Contributing\n\nKeep it simple. Keep it minimal.\n\n### Authors \n\n*   Carlos E. Viol Barbosa\n*   ...\n\n### License\n\nThis project is licensed under the MIT License',
    'author': 'Carlos Viol Barbosa',
    'author_email': 'you@example.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://helyos.ivi.fraunhofer.de',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
