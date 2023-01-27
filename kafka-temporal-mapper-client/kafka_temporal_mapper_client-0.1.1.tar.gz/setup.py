# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.', 'common': './common'}

packages = \
['client', 'common']

package_data = \
{'': ['*']}

install_requires = \
['dacite>=1.7.0,<2.0.0',
 'dataclasses-json>=0.5.7,<0.6.0',
 'kafka-python>=2.0.2,<3.0.0']

setup_kwargs = {
    'name': 'kafka-temporal-mapper-client',
    'version': '0.1.1',
    'description': 'A client library to send subscribe and notify workflow events to the kafka-temporal-mapper server.',
    'long_description': '# Kafka-Temporal Mapper Client\n\nKafka-Temporal mapper client facilitates the interaction between the workflows and the Kafka-Temporal mapper server.\nThis library is used by the workflows and provides methods for publishing of the workflow and mapping events. \n\nThe client provides two methods:\n- **subscribe**: used to subscribe a workflow to the execution of another workflow.   \n- **notify**: used by a workflow to notify the termination of its execution.  \n\n### Installation\n```bash\npip install kafka_temporal_mapper_client\n```\n\n### Usage\nTo use this library for notifying or subscribing:\n```python\nfrom kafka_temporal_mapper.client import KafkaTemporalClient\n\nktc = KafkaTemporalClient()\n\n# subscribe workflow B to workflow A using a part of A\'s results as argument (@b.c)\nktc.subscribe(\'WorkflowB\', [{\'name\':\'WorkflowA\', \'args\': {"a":"hello", "b":"@b.c"}}]) \n\n# notify workflow A execution and its results\nktc.notify(\'WorkflowA\', {"a":"hello", "b": {"c": "world"}})\n```\n',
    'author': 'gtato',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
