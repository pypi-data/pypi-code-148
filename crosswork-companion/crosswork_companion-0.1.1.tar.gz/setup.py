# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['crosswork_companion']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=22.1.0,<23.0.0',
 'aiohttp>=3.8.3,<4.0.0',
 'jinja2>=3.1.2,<4.0.0',
 'pyyaml>=6.0,<7.0',
 'requests>=2.28.2,<3.0.0',
 'rich-click>=1.6.1,<2.0.0']

entry_points = \
{'console_scripts': ['crosswork_companion = crosswork_companion.script:run']}

setup_kwargs = {
    'name': 'crosswork-companion',
    'version': '0.1.1',
    'description': 'Business ready documents from Cisco Crosswork',
    'long_description': '# Crosswork Companion\n\nBusiness Ready Documents for Cisco Crosswork\n\n## Current API Coverage\n\nHealth Insights KPI Management Query\n\n    pulse_cpu_utilization\n\n    pulse_cpu_threshold\n\n    pulse_cef_drops\n\n    pulse_device_uptime\n\n    pulse_ethernet_port_error_counters\n\n    pulse_ethernet_port_packet_size_distribution\n\n    pulse_interface_packet_counters\n\n    pulse_interface_qos_egress\n\n    pulse_interface_qos_ingress\n\n    pulse_interface_rate_counters\n\n    pulse_memory_utilization\n\nNCA YANG Modules\n\n\n## Installation\n\n```console\n$ python3 -m venv crosswork\n$ source crosswork/bin/activate\n(crosswork) $ pip install crosswork_companion\n```\n\n## Usage - Help\n\n```console\n(crosswork) $ crosswork_companion --help\n```\n\n![Help](/images/help.png)\n\n## Usage - In-line\n\n```console\n(crossswork) $ crosswork_companion --url <url to Crosswork> --username <crosswork username> --password <crosswork password>\n```\n\n## Usage - Interactive\n\n```console\n(crosswork) $ crosswork_companion\nCrosswork URL: <URL to Crosswork>\nCrosswork Username: <Crosswork Username>\nCrosswork Password: <Crosswork Password>\n```\n\n## Usage - Environment Variables\n\n```console\n(crosswork) $ export URL=<URL to Crosswork>\n(crosswork) $ export USERNAME=<Crosswork Username>\n(crosswork) $ export PASSWORD=<Crosswork Password>\n```\n\n## Recommended VS Code Extensions\n\nExcel Viewer - CSV Files\n\nMarkdown Preview - Markdown Files\n\nMarkmap - Mindmap Files\n\nOpen in Default Browser - HTML Files\n\n## Contact\n\nPlease contact John Capobianco if you need any assistance\n',
    'author': 'John Capobianco',
    'author_email': 'ptcapo@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
