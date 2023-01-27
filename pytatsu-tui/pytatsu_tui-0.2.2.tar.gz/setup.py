# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytatsu_tui']

package_data = \
{'': ['*'], 'pytatsu_tui': ['bins/Darwin/*', 'bins/Linux/*', 'bins/Windows/*']}

install_requires = \
['attrs==22.2.0',
 'click==8.1.3',
 'colorama==0.4.6',
 'httpx==0.23.3',
 'nest-asyncio==1.5.6',
 'pyimg4==0.7',
 'pytatsu==0.1.4',
 'remotezip==0.9.4',
 'send2trash==1.8.0',
 'termcolor==2.2.0']

entry_points = \
{'console_scripts': ['tatsu-tui = pytatsu_tui.__main__:main']}

setup_kwargs = {
    'name': 'pytatsu-tui',
    'version': '0.2.2',
    'description': 'A way to save/manage *OS blobs using pytatsu',
    'long_description': "## What is this?\n\nA way to save/manage \\*OS blobs using [pytatsu](https://github.com/Cryptiiiic/Tatsu)\n\n## Prerequisites\n\n- Windows/Linux/macOS\n- [Python](https://www.python.org/downloads/) (**>= 3.10**)\n  - [Tkinter](https://tkdocs.com/tutorial/install.html)\n\n## Usage\n\n```sh\n$ python3 -m pip install pytatsu-tui --upgrade\n\n$ tatsu-tui\n\n$ tatsu-tui -u/--unset # Unset the saved config directory\n```\n\nFor every device you have, you'll be asked to provide the following information:\n\n- [Device Model and Board Configuration](https://github.com/doms9/tatsumanager/blob/default/apple_devices.md)\n- [Exclusive Chip Identification](https://www.theiphonewiki.com/wiki/ECID#Getting_the_ECID) (Decimal and Hex formats supported)\n- [ApNonce](https://gist.github.com/m1stadev/5464ea557c2b999cb9324639c777cd09#getting-a-generator-apnonce-pair-jailbroken) (Required for A12+)\n  - This **<ins>DOES NOT</ins>** freeze your ApNonce if your device isn't jailbroken, do that beforehand.\n- [Generator](https://www.idownloadblog.com/2021/03/08/futurerestore-guide-1-generator/) (Required for A12+)\n  - (Eg. 0x1111111111111111 for [unc0ver](https://unc0ver.dev/), 0xbd34a880be0b53f3 for [Electra](https://coolstar.org/electra/)/[Chimera](https://chimera.coolstar.org/)/[Odyssey](https://theodyssey.dev/)/[Taurine](https://taurine.app/)/[Cheyote](https://www.cheyote.io/))\n\n## Preview\n\n![](https://github.com/doms9/tatsu-tui/blob/default/preview.gif)\n\n---\n\n###### [API used for Apple's Stable Firmwares](https://ipswdownloads.docs.apiary.io/#)\n\n###### [API used for Apple's Beta Firmwares](https://github.com/m1stadev/ios-beta-api)\n\n###### [Cryptiiiic's Pytatsu](https://github.com/Cryptiiiic/Tatsu)\n",
    'author': 'doms9',
    'author_email': 'domsenueve@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/doms9/tatsumanager',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
