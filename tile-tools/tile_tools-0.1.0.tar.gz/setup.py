# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tile_tools', 'tile_tools.common', 'tile_tools.cover', 'tile_tools.tilebelt']

package_data = \
{'': ['*']}

install_requires = \
['geojson>=2.5.0,<3.0.0', 'mercantile>=1.2.1,<2.0.0']

setup_kwargs = {
    'name': 'tile-tools',
    'version': '0.1.0',
    'description': 'A collection of tools for navigating Mapbox tiles.',
    'long_description': "# Tile Tools\n\n[![Python Tests](https://github.com/biglocalnews/tile-tools/actions/workflows/pytest.yaml/badge.svg)](https://github.com/biglocalnews/tile-tools/actions/workflows/pytest.yaml)\n[![Python Lint](https://github.com/biglocalnews/tile-tools/actions/workflows/pylint.yaml/badge.svg)](https://github.com/biglocalnews/tile-tools/actions/workflows/pylint.yaml)\n\nCollection of tools useful for navigating Mapbox (and similar) tiles.\n\nMost of these tools were written by Mapbox in JavaScript. I've ported them into Python with minimal modification.\n\n\n## Contents\n\n### `tilebelt`\n\nUtility functions for working with tiles.\n\nThis is a complete Python port of Mapbox's [@mapbox/tilebelt](https://github.com/mapbox/tilebelt/).\n\nThere are some minor differences in the API.\nSee the [submodule readme](tile_tools/tilebelt/README.md) for more details.\n\n### `cover`\n\nGiven a GeoJSON Geometry and a zoom level, generate the minimal set of Mapbox `(x, y, zoom)` tiles that cover this geometry.\n\nThis is a re-implementation of Mapbox's [`@mapbox/tile-cover`](https://github.com/mapbox/tile-cover/).\nThe implementation started out as a port, however the originally library is not passing all of its own tests.\nThe API has been re-implemented here with a slightly different approach, and all of the equivalent tests are now passing.\n\nSee [submodule readme](tile_tools/cover/README.md) for details.\n\n### `coords`\n\n#### `coords.tilecoords2lnglat`\n\nTransform Mapbox's relative tile `(x, y)` coordinates into longitude/latitude degrees.\n\n\n### `distance`\n\n#### `distance.haversine`\n\nCompute the distance between two points on the globe using the haversine formula.\n\n\n## Development\n\nSet up the environment with `poetry`:\n\n```zsh\npoetry install --with dev\npoetry run pre-commit install\n```\n",
    'author': 'Joe Nudell',
    'author_email': 'jnu@stanford.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
