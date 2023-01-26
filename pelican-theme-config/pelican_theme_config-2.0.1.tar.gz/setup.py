# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pelican', 'pelican.plugins.theme_config']

package_data = \
{'': ['*']}

install_requires = \
['pelican>=4.5']

extras_require = \
{'markdown': ['markdown>=3.2']}

setup_kwargs = {
    'name': 'pelican-theme-config',
    'version': '2.0.1',
    'description': 'Pelican plugin to add footnotes to articles and pages',
    'long_description': 'Theme Configuration: A Plugin for Pelican\n==========================================\n\n[![Build Status](https://img.shields.io/github/actions/workflow/status/pelican-plugins/theme-config/main.yml?branch=main)](https://github.com/pelican-plugins/theme-config/actions)\n[![PyPI Version](https://img.shields.io/pypi/v/pelican-theme-config)](https://pypi.org/project/pelican-theme-config/)\n\nThis package provides a plugin for the Pelican static website generator and\nadds support for themes to adjust Pelican\'s configuration using the\n`themeconf.py` file located in the root directory of the theme.\n\nInstallation\n------------\n\nThis plugin can be installed via:\n\n    python -m pip install pelican-theme-config\n\nUsage\n-----\n\nAdd `theme_config` to the list of plugins in the `pelicanconf.py` file, e.g.\n\n    PLUGINS = [ "theme_config" ]\n\nFrom that point on, Pelican will try to load the `themeconf.py` from theme\'s\ndirectory.\n\nOverview\n--------\n\nThis plugin allows theme authors to create more self-contained themes since\neverything that a theme requires can be configured within the theme itself:\n\n  * themes can be shipped with their own plugins\n  * themes can provide their static content (e.g. a theme that implements\n    Google\'s PWA can provide `manifest.json` that should be put into the\n    root of the website)\n  * basically, authors could do almost anything :) since with this plugin\n    theme gets control\n\nThe code is hooked up early in Pelican\'s start-up sequence leveraging the\n"initialized" Pelican event, so almost every configuration option can be\nsafely redefined and would take effect.\n\nHowever, since the plugin hooks up after the sanity checks on the provided\nconfiguration were done by Pelican this gives some opportunities and risks.\nBasically, theme authors should be careful to adhere to Pelican\'s conventions\non the configuration directives, otherwise they may confuse their users.\n\nThis plugin protects the following configuration options from being modified\nby the theme:\n\n  - BIND\n  - CACHE_PATH\n  - PATH\n  - PELICAN_CLASS\n  - OUTPUT_PATH\n  - SITEURL\n  - THEME\n  - THEME_CONFIG\n  - THEME_CONFIG_PROTECTED\n  - PORT\n\nThis list can be configured by the end user in `pelicanconf.py` if they want\nto restrict it even further or make it more relaxed.  The goal is to give the\nuser the ability to define the expected behaviour for their configuration.\n\nThe plugin introduces the following configuration options one can specify in\nthe primary Pelican configuration file:\n\n    # The name of the file to lookup in theme\'s directory\n    THEME_CONFIG = "themeconf.py"\n\n    # The list of configuration options to be protected from modification\n    THEME_CONFIG_PROTECTED = ["PATH","OUTPUT_PATH"]\n\nContributing\n------------\n\nContributions are welcome and much appreciated. Every little bit helps. You can\ncontribute by improving the documentation, adding missing features, and fixing\nbugs. You can also help out by reviewing and commenting on [existing issues][].\n\nTo start contributing to this plugin, review the [Contributing to Pelican][]\ndocumentation, beginning with the **Contributing Code** section.\n\nCredits\n-------\n\nAuthored by [Dmitry Khlebnikov](https://dmitry.khlebnikov.net/).\n\n[existing issues]: https://github.com/pelican-plugins/theme-config/issues\n[Contributing to Pelican]: https://docs.getpelican.com/en/latest/contribute.html\n',
    'author': '(GalaxyMaster)',
    'author_email': 'galaxy4public+pypi@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/pelican-plugins/theme-config',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
