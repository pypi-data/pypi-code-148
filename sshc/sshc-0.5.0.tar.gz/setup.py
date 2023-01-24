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
    'version': '0.5.0',
    'description': 'SSH Config and Ansible Inventory Generator.',
    'long_description': '# sshc - SSH Configuration Management Tool with Ansible Inventory Generation\nThe purpose of this tool is to help you manage ssh config files with hosts as well as ansible inventory file management.\n\n#### Structure\n\n1. Insert host information to a JSON file as a DB.\n2. Generate SSH Config file and an Ansible Inventory file.\n\n#### Technology Stack\n1. python\n2. json\n3. openssh\n4. ansible\n\n### Dependency\n\n#### Runtime\n- Python3.7+\n- Linux\n\n#### Development\n- Poetry\n\n## Installation\n\n```bash\n% pip3 install sshc --upgrade\n```\n\n## Usage\n\n### Step 1: Need the DB to be initiated for the first time\n\n```bash\n% sshc init\n```\n\n### Step 2: Insert host information to the Database\n\n```bash\n% sshc insert --name Google --host 8.8.8.8 --port 22 --user groot --identityfile /home/fahad/fahad.pem --comment "This is the server where you are not authorized to have access." --configfile /home/fahad/.ssh/config --groups google, fun\n```\n\n### Step 3: Generate ssh config and as well as ansible inventory file\n\n```bash\n% python3 sshc.py generate\n```\nThis command will read all the entries in the DB and generate\n1. SSH config file in your preferred directory or default one(i.e. $HOME/.ssh/config).\n2. Ansible Inventory file will be created at your preferred directory or in default one.\n\nIf you do not change default directory, then you will be able to use the SSH configs immediately. But Ansible inventory \nwill not be created in its default directory. You need to choose the inventory file or create link file.\n\nFor SSH,\n```bash\n% ssh -F <DIR>/config\n```\n\nFor Ansible,\n```bash\n% ansible -i <DIR>/hosts.json all --list-host\n```\n\n### Others\nHelp message of the tool\n```bash\n% sshc --help\n```\n\n```bash\nusage: sshc [-h] [--version] [--destination DESTINATION] [--identityfile IDENTITYFILE] [--configfile CONFIGFILE] [--dbfile DBFILE] [--inventoryfile INVENTORYFILE]\n            {init,insert,delete,read,generate} ...\n\nSSH Config and Ansible Inventory Generator !\n\noptions:\n  -h, --help            show this help message and exit\n  --version             show program\'s version number and exit\n  --destination DESTINATION\n                        Config HOME?\n  --identityfile IDENTITYFILE\n                        SSH Default Identity File Location. i.e. id_rsa\n  --configfile CONFIGFILE\n                        SSH Config File.\n  --dbfile DBFILE       SSHC DB File.\n  --inventoryfile INVENTORYFILE\n                        Ansible Inventory File.\n\nsubcommands:\n  The main command of this CLI tool.\n\n  {init,insert,delete,read,generate}\n                        The main commands have their own arguments.\n    init                Initiate Host DB !\n    insert              Insert host information !\n    delete              Delete host information !\n    read                Read Database !\n    generate            Generate necessary config files !\n```\n\n### Delete Inserted Data\n\n```bash\n% sshc delete --hostname <HOSTNAME>\n```\n\n### Read DB Data\n\n```bash\n% sshc read\n```\n\nYou can pass verbose too\n\n```bash\n% sshc read --verbose yes\n```\n\n## Known issues or Limitations\n\n- Tested in Ubuntu 22.04\n- Windows is not tested\n\n## Getting help\nIf you have questions, concerns, bug reports and others, please file an issue in this repository\'s Issue Tracker.\n\n## Getting involved\nIf you want to contribute to this tool, feel free to fork the repo and create Pull request with your changes.\nKeep in mind to\n- include better comment to understand.\n- create PR to **development** branch.\n\n---\n## Author\n- [Fahad Ahammed - DevOps Enthusiast - Dhaka, Bangladesh](https://github.com/fahadahammed)',
    'author': 'fahadahammed',
    'author_email': 'iamfahadahammed@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/fahadahammed/sshc',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
