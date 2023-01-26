# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pelican', 'pelican.plugins.feed_filter']

package_data = \
{'': ['*']}

install_requires = \
['pelican>=4.5,<5.0']

extras_require = \
{'markdown': ['markdown>=3.2,<4.0']}

setup_kwargs = {
    'name': 'pelican-feed-filter',
    'version': '1.1.0',
    'description': 'Filter elements from feeds according to custom rules',
    'long_description': '# Feed Filter\n\n[![Build Status](https://img.shields.io/github/actions/workflow/status/pelican-plugins/feed-filter/main.yml?branch=master)](https://github.com/pelican-plugins/feed-filter/actions)\n[![PyPI Version](https://img.shields.io/pypi/v/pelican-feed-filter)](https://pypi.org/project/pelican-feed-filter/)\n\nFeed Filter is a Pelican plugin that filters elements from feeds.\n\nInstallation\n------------\n\nThis plugin can be installed via:\n\n    python -m pip install pelican-feed-filter\n\nUsage\n-----\n\nThis plugin is configured through your Pelican configuration file, by setting the following variable:\n\n`FEED_FILTER = {}`\n\nDefine feed paths and include/exclude filters to apply to matching feeds. Both feed paths and filters are matched using [Unix shell-stye wildcards][1].\n\nFilters are defined as:\n* `include.item attribute`\n* `exclude.item_attribute`\n\nwhere `item_attribute` can be any [feed item attribute][2], ie. `title`, `link`, `author_name`, `categories`, ...\n\nYou can also match `pubdate` and `updateddate` item attributes as strings formatted with the following format: `%a, %d %b %Y %H:%M:%S` (e.g. \'Thu, 28 Jun 2001 14:17:15\')\n\n**Filter priorities**\n\nIf an inclusion filter is defined, only feed elements that match the filter will be included in the feed.\n\nIf an exclusion filter is defined, all feed elements except those which match the filter will be included in the feed.\n\nIf both include and exclude filters are defined, all feed elements except those which match some exclusion filter but no inclusion filter, will be included in the feed.\n\nIf multiple inclusion/exclusion filters are defined for the same feed path, a single match is enough to include the item in the feed.\n\nUsage examples\n--------------\n\n* Include only posts in some categories into the global feed:\n```\nFEED_ATOM = \'feed/atom\'\nFEED_RSS = \'feed/rss\'\nFEED_FILTER = {\n    \'feed/*\': {\n        \'include.categories\': [\'software-*\', \'programming\']\n    }\n}\n```\n\n* Exclude an author from a category feed:\n```\nCATEGORY_FEED_ATOM = \'feed/{slug}.atom\'\nCATEGORY_FEED_RSS = \'feed/{slug}.rss\'\nFEED_FILTER = {\n    \'feed/a-category-slug.*\': {\n        \'exclude.author_name\': \'An Author name\'\n    }\n}\n```\n\n* Exclude an author from all category feeds:\n```\nCATEGORY_FEED_ATOM = \'feed/{slug}.atom\'\nCATEGORY_FEED_RSS = \'feed/{slug}.rss\'\nFEED_FILTER = {\n    \'feed/*.*\': {\n        \'exclude.author_name\': \'An Author name\'\n    }\n}\n```\n\n* In the global feed, exclude all posts in a category, except if written by a given author:\n```\nFEED_ATOM = \'feed/atom\'\nFEED_RSS = \'feed/rss\'\nFEED_FILTER = {\n    \'feed/*\': {\n        \'include.author_name\': \'An Author name\',\n        \'exclude.category\': \'software-development\'\n    }\n}\n```\n\n* In the global feed, exclude all posts whose title starts with "Review":\n```\nFEED_ATOM = \'feed/atom\'\nFEED_RSS = \'feed/rss\'\nFEED_FILTER = {\n    \'feed/*\': {\n        \'exclude.title\': \'Review*\'\n    }\n}\n```\n\n* In the global feed, include all posts written by a given author OR in a certain category, except if the title starts with "Review":\n```\nFEED_ATOM = \'feed/atom\'\nFEED_RSS = \'feed/rss\'\nFEED_FILTER = {\n    \'feed/*\': {\n        \'include.author_name\': \'An Author name\',\n        \'include.category\': \'software-development\'\n        \'exclude.title\': \'Review*\'\n    }\n}\n```\n\nContributing\n------------\n\nContributions are welcome and much appreciated. Every little bit helps. You can contribute by improving the documentation, adding missing features, and fixing bugs. You can also help out by reviewing and commenting on [existing issues][].\n\nTo start contributing to this plugin, review the [Contributing to Pelican][] documentation, beginning with the **Contributing Code** section.\n\n[1]: https://docs.python.org/3/library/fnmatch.html "Fnmatch Python module"\n[2]: https://github.com/getpelican/feedgenerator/blob/master/feedgenerator/django/utils/feedgenerator.py#L132 "Feed item attributes"\n[existing issues]: https://github.com/pelican-plugins/feed-filter/issues\n[Contributing to Pelican]: https://docs.getpelican.com/en/latest/contribute.html\n',
    'author': 'David Alfonso',
    'author_email': 'developer@davidalfonso.es',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/pelican-plugins/feed-filter',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
