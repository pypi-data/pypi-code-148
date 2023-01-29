# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['osint_tools',
 'osint_tools.api',
 'osint_tools.api.email',
 'osint_tools.api.email.gmail',
 'osint_tools.api.four_chan',
 'osint_tools.api.rss',
 'osint_tools.api.translator',
 'osint_tools.api.translator.schema',
 'osint_tools.api.utube',
 'osint_tools.db',
 'osint_tools.db.deta_db',
 'osint_tools.db.mongo_db',
 'osint_tools.schemas',
 'osint_tools.schemas.rss',
 'osint_tools.utils']

package_data = \
{'': ['*']}

install_requires = \
['chardet==4.0.0',
 'deep-translator==1.8.3',
 'feedparser>=6.0.8,<7.0.0',
 'motor>=3.0.0,<4.0.0',
 'opencv-python==4.5.5.64',
 'pillow==9.1.0',
 'pydantic>=1.10.1,<2.0.0',
 'pytesseract==0.3.9',
 'python-jose>=3.3.0,<4.0.0',
 'python-multipart>=0.0.5,<0.0.6',
 'requests>=2.11',
 'strawberry-graphql[debug-server,fastapi]>=0.139.0,<0.140.0',
 'werkzeug>=2.2.2,<3.0.0']

setup_kwargs = {
    'name': 'osint-tools',
    'version': '0.2.8',
    'description': '',
    'long_description': '\nTools for working with data.\n\n\n```\ncython\nfastapi==0.74.1\nrequired for web3?\nrequests>=2.11\npython-multipart==0.0.5\npydantic[email,dotenv]==1.9.0\n\nstrawberry-graphql[debug-server,fastapi]\nuvicorn==0.17.5\nuvicorn[standard]\n\ngunicorn==20.1.0\ngunicorn[gthread]\n\npython-jose[cryptography]==3.3.0\npasslib[bcrypt]==1.7.4\npyserum\nsolana\nweb3==4.2.1\nmotor==2.5.1\nredis==4.3.4\ndeep-translator==1.8.3\nfeedparser==6.0.8\nPillow==9.1.0\npytesseract==0.3.9\nchardet==4.0.0\nopencv-python==4.5.5.64\n```',
    'author': 'Alexander Slessor',
    'author_email': 'alexjslessor@gmail.com.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
