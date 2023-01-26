# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['imap_mailbox']
setup_kwargs = {
    'name': 'imap-mailbox',
    'version': '0.2.0',
    'description': 'mailbox over IMAP',
    'long_description': '*Please note that `imap_mailbox` is still under active development and will be subject to significant changes.*\n\n```python\nimport imap_mailbox\n\n# connect to the IMAP server\nwith imap_mailbox.IMAPMailbox(\'imap.example.com\', \'username\', \'password\') as mailbox:\n    \n    # search messages from vip@example.com\n    uids = mailbox.search(\'FROM\', \'vip@example.com\')\n    \n    # move the messages to the \'VIP\' folder\n    mailbox.move(uids, \'VIP\')\n```\n\nThis module provides a subclass of `mailbox.Mailbox` that allows you to interact with an IMAP server. It is designed to be a drop-in replacement for the standard library `mailbox` module.\n\n# Installation\n\nInstall the latest stable version from PyPI:\n\n```bash\npip install imap-mailbox\n```\n\nInstall the latest version from GitHub:\n\n```bash\npip install https://github.com/medecau/imap_mailbox/archive/refs/heads/main.zip\n```\n\n# Examples\n\n## Iterate over messages in a folder\n\n```python\nimport imap_mailbox\n\n# connect to the IMAP server\nwith imap_mailbox.IMAPMailbox(\'imap.example.com\', \'username\', \'password\') as mailbox:\n    \n    # select the INBOX folder\n    mailbox.select(\'INBOX\')\n    \n    # iterate over messages in the folder\n    for message in mailbox:\n        print(f"From: {message[\'From\']}")\n        print(f"Subject: {message[\'Subject\']}")\n```\n\n## Connect to a Proton Mail account\n\n```python\nimport imap_mailbox\n\n# connect to the local IMAP bridge\nwith imap_mailbox.IMAPMailbox(\n    \'127.0.0.1\', \'username\', \'password\'\n    port=1143, security=\'STARTTLS\'\n    ) as mailbox:\n    \n    # search messages from your friend\n    uids = mailbox.search(\'FROM\', \'handler@proton.me\')\n\n    # erase the evidence\n    mailbox.delete(uids)\n    \n```\n_this is a joke; don\'t use proton for crimes – stay safe_\n\n## Delete messages from a noisy sender\n\n```python\nimport imap_mailbox\n\nwith imap_mailbox.IMAPMailbox(\'imap.example.com\', \'username\', \'password\') as mailbox:\n    \n    # search messages from\n    uids = mailbox.search(\'FROM\', \'spammer@example.com\')\n\n    # delete the messages\n    mailbox.delete(uids)\n```\n\n## Delete GitHub messages older than two years\n\n```python\nimport imap_mailbox\n\nwith imap_mailbox.IMAPMailbox(\'imap.example.com\', \'username\', \'password\') as mailbox:\n    \n    # search messages older than two years from github.com\n    uids = mailbox.search(\'NOT PAST2YEARS FROM github.com\')\n    \n    # delete the messages\n    mailbox.delete(uids)\n```\n\n# Contribution\n\nHelp improve imap_mailbox by reporting any issues or suggestions on our issue tracker at [github.com/medecau/imap_mailbox/issues](https://github.com/medecau/imap_mailbox/issues).\n\nGet involved with the development, check out the source code at [github.com/medecau/imap_mailbox](https://github.com/medecau/imap_mailbox).\n',
    'author': 'Pedro Rodrigues',
    'author_email': 'medecau@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://medecau.github.io/imap_mailbox/',
    'py_modules': modules,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
