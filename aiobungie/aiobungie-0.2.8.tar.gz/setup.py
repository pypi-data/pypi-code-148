# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiobungie', 'aiobungie.crates', 'aiobungie.interfaces', 'aiobungie.internal']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp==3.8.3', 'attrs==22.2.0', 'python-dateutil==2.8.2']

setup_kwargs = {
    'name': 'aiobungie',
    'version': '0.2.8',
    'description': 'A Python and Asyncio API for Bungie.',
    'long_description': '# aiobungie\nA statically typed API wrapper for the Bungie\'s REST API written in Python3 and Asyncio.\n\n# Installing\n\nPyPI stable release.\n\n```sh\n$ pip install aiobungie\n```\n\nDevelopment\n```sh\n$ pip install git+https://github.com/nxtlo/aiobungie@master\n```\n\n## Quick Example\n\nSee [Examples for advance usage.](https://github.com/nxtlo/aiobungie/tree/master/examples)\n\n```python\nimport aiobungie\n\nclient = aiobungie.Client(\'YOUR_API_KEY\')\n\nasync def main() -> None:\n\n    # Fetch a charatcer with all its components.\n    # This includes Equimpents, Inventory, Records, etc.\n    async with client.rest:\n        my_warlock = await client.fetch_character(\n            membership_id,\n            aiobungie.MembershipType.STEAM,\n            character_id,\n            components=[aiobungie.Component.ALL_CHARACTERS]\n        )\n\n        for activity in my_warlock.activities:\n            # Check if activity is a raid.\n            if activity.current_mode and activity.current_mode is aiobungie.GameMode.RAID:\n                print(activity.avaliable_activities) # All raids for this character.\n\n# You can either run it using the client or just asyncio.run(main())\nclient.run(main())\n```\n\n## RESTful clients\nAlternatively, You can use `RESTClient` which\'s designed to only make HTTP requests and return JSON objects.\nand to interact with the manifest.\n\n### Example\n```py\nimport aiobungie\nimport asyncio\n\n# Single REST client connection.\nclient = aiobungie.RESTClient("...")\n\nasync def main() -> None:\n    async with client:\n        # SQLite manifest.\n        await client.download_manifest()\n\n        # OAuth2 API.\n        tokens = await client.fetch_oauth2_tokens(\'code\')\n\nasyncio.run(main())\n```\n\n### Requirements\n* Python 3.9 or higher\n* aiohttp\n* attrs\n\n## Contributing\nPlease read this [manual](https://github.com/nxtlo/aiobungie/blob/master/CONTRIBUTING.md)\n\n### Getting Help\n* Discord: `Fate 怒#0008` | `350750086357057537`\n* Docs: [Here](https://nxtlo.github.io/aiobungie/).\n',
    'author': 'nxtlo',
    'author_email': 'dhmony-99@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nxtlo/aiobungie',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
