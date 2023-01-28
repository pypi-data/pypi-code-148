# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['allin']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=22.1.0,<23.0.0',
 'autoroutes>=0.3.5,<0.4.0',
 'biscuits>=0.3.0,<0.4.0',
 'fast-query-parsers>=0.3.0,<0.4.0',
 'jetblack-asgi-typing>=0.4.0,<0.5.0',
 'msgspec>=0.12.0,<0.13.0',
 'python-multipart>=0.0.5,<0.0.6',
 'typing-extensions>=4.2.0,<5.0.0']

setup_kwargs = {
    'name': 'allin',
    'version': '0.1.1a0',
    'description': 'Allin is an experimental asynchronous web framework.',
    'long_description': '# allin\n\nAllin is an experimental asynchronous web framework.\n\nTable of Contents:\n\n* [:raised_eyebrow: Why ?](#🤨-why)\n* [:books: Roadmap](#📚-roadmap)\n* [:star_struck: Features](#🤩-features)\n* [:love_you_gesture: Quick Start](#🤟-quick-start)\n* [:sunglasses: Installation](#😎-installation)\n\n    * [From source](#install-from-source)\n    * [With `pip`](#install-with-pip)\n\n`Allin` is heavily inspired by [Flask](https://flask.palletsprojects.com/en/2.2.x/), [Starlette](https://www.starlette.io/) & [Falcon](https://falconframework.org/).\n\n## :raised_eyebrow: Why ?\n\n> I\'m just curious :monocle_face:\n\n[ASGI]: https://asgi.readthedocs.io/en/latest\n\nYup, I\'m curious about how a web application based on [ASGI] works.\n\nIt may not yet fully comply with the [ASGI] application specifications as documented. But, for the main features like route mapping, HTTP responses, error handling, parsing the request body it\'s there.\n\n...and I want to build my own framework from scratch so I know how the application works.\n\nLiterally, the "framework parts" weren\'t built from scratch as I also used third party modules and some "parts from other sources" were used as references.\n\n> _This is part of the journey_\n\n## :books: Roadmap\n\n- [x] ASGI Lifespan Support\n- [x] HTTP Support\n\n    - [x] Parse HTTP Headers\n    - [x] Parse HTTP Request\n        - [x] Request Body Stream (Useful for dealing with large data)\n        - [x] JSON Body Support\n        - [x] MessagePack Body Support\n        - [x] Form Data Support\n        - [x] Cookies\n        - [x] Query Parameters\n\n    - [x] HTTP Responses\n        - [x] JSONResponse\n        - [x] MessagePackResponse\n\n    - [ ] HTTP Middleware\n        - [ ] Before HTTP Request\n        - [ ] After HTTP Request\n\n    - [x] Routing\n\n        - [x] Decorator shortcuts such as `@get`, `@post`, `@put`, etc. are available.\n        - [x] Nesting routers\n\n- [ ] Websocket Support\n\n## :star_struck: Features\n\n- [x] Global variables. (It means, you can access the `app` and `request` object instances globally)\n- [x] Error handling\n- [x] `JSON` and `MessagePack` requests are supported out of the box (thanks to [msgspec](https://github.com/jcrist/msgspec))\n- [x] Form Data Support (`application/x-www-form-urlencoded` or `multipart/form-data`)\n- [x] Decorator shortcuts such as `@get`, `@post`, `@put`, etc. are available.\n- [x] Nesting routers\n\n## :love_you_gesture: Quick Start\n\nHere is an example application based on the `Allin` framework and I\'m sure you are familiar with it.\n\n```python\nfrom allin import Allin, JSONResponse\n\napp = Allin()\n\n@app.route("/")\nasync def index():\n    return JSONResponse({"message": "Hello World!"})\n```\n\n<details>\n<summary>:point_down: Explanation</summary>\n\n* The `app` variable is the ASGI application instance.\n* And we create an endpoint with the route `/` on the line `app.route(...)`\n* Then we add the `index()` function to handle the `/` route.\n* And the handler function will return a JSON response with the content `{"message": "Hello World!"}`\n\n</details>\n\nThat\'s it! looks familiar right?\n\nWant more? check out other [sample projects here](https://github.com/aprilahijriyan/allin/tree/main/examples)\n\n## :sunglasses: Installation\n\n### Install from source\n\n```\ngit clone --depth 1 https://github.com/aprilahijriyan/allin.git\ncd allin\n```\n\nNeed https://python-poetry.org/ installed on your device\n\n```\npoetry build\npip install ./dist/*.whl\n```\n\n### Install with `pip`\n\nCurrently I just published the pre-release version `v0.1.1a0`. So, maybe you need to install it with the `--pre` option. Example:\n\n```\npip install --pre allin\n```\n',
    'author': 'Aprila Hijriyan',
    'author_email': 'hijriyan23@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/aprilahijriyan/allin',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
