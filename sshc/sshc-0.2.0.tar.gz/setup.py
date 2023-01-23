# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['src']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['sshc = src.sshc:__main__']}

setup_kwargs = {
    'name': 'sshc',
    'version': '0.2.0',
    'description': 'SSH Config and Ansible Inventory Generator.',
    'long_description': '# ssh-config-ansible-inventory-generator\nThis tool should help you manage ssh config file with hosts as well as ansible hosts or inventory file.\n\n## Usage\n\n### help\n\n```bash\n% python3 sshc.py --help\n```\n\n```bash\nusage: sshc [-h] [--version] [--destination DESTINATION] [--identityfile IDENTITYFILE] [--configfile CONFIGFILE] [--dbfile DBFILE] [--inventoryfile INVENTORYFILE]\n            {init,insert,delete,read,generate} ...\n\nSSH Config and Ansible Inventory Generator !\n\noptions:\n  -h, --help            show this help message and exit\n  --version             show program\'s version number and exit\n  --destination DESTINATION\n                        Config HOME?\n  --identityfile IDENTITYFILE\n                        SSH Default Identity File Location. i.e. id_rsa\n  --configfile CONFIGFILE\n                        SSH Config File.\n  --dbfile DBFILE       SSHC DB File.\n  --inventoryfile INVENTORYFILE\n                        Ansible Inventory File.\n\nsubcommands:\n  The main command of this CLI tool.\n\n  {init,insert,delete,read,generate}\n                        The main commands have their own arguments.\n    init                Initiate Host DB !\n    insert              Insert host information !\n    delete              Delete host information !\n    read                Read Database !\n    generate            Generate necessary config files !\n```\n\n### Need the DB to be initiated for the first time\n\n```bash\n% sshc init\n```\n\n### How to insert host information to the Database?\n\n```bash\n% sshc insert --name Google --host 8.8.8.8 --port 22 --user groot --identityfile /home/fahad/fahad.pem --comment "This is the server where you are not authorized to have access." --configfile /home/fahad/.ssh/config --groups google, fun\n```\n\n### How to generate ssh config and as well as ansible inventory file\n\n```bash\n% python3 sshc.py generate\n```',
    'author': 'fahadahammed',
    'author_email': 'iamfahadahammed@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://sshc.fahadahammed.com/',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
