# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xontrib_cd']

package_data = \
{'': ['*']}

install_requires = \
['xonsh>=0.12.5']

entry_points = \
{'xonsh.xontribs': ['cd = xontrib_cd.main']}

setup_kwargs = {
    'name': 'xontrib-cd',
    'version': '0.2.1',
    'description': 'cd to any path without escaping in xonsh shell: cd ~/[te] st',
    'long_description': '<p align="center">\n<code>cd</code> to any path without escaping in <a href="https://xon.sh">xonsh shell</a>.\n<br/>\nReplaces <code>cd </code> at the start of a line with a <a href="https://xon.sh/tutorial_macros.html#subprocess-macros">subprocess macro</a> <code>cd! </code> \n</p>\n\n<p align="center">  \nIf you like the idea click ⭐ on the repo and stay tuned.\n</p>\n\n\n## Installation\n\nTo install use pip:\n\n```bash\nxpip install xontrib-cd\n# or: xpip install -U git+https://github.com/eugenesvk/xontrib-cd\n```\n\nThis xontrib will get loaded automatically for interactive sessions; to stop this, set\n\n```xonsh\n$XONTRIBS_AUTOLOAD_DISABLED = {"cd", }\n```\n\n## Usage\n\nUse `cd` as usual, but without the fear of copying&pasting arbitrary paths (e.g. `.../space separated/` or `.../[bracketed]/`)\n\n```bash\nxontrib load cd\ncd ~/[Path] With Spaces\t# equivalent to \'cd! ~/[Path] With Spaces\'\ncd C:/Program Files    \t# equivalent to \'cd! C:/Program Files\'\ncd -P ~/SymlinkTo      \t# follow symlinks, equivalent to \'cd -P! ~/SymlinkTo\'\n```\n\nSet the following environment variables in your profile to enable __extra options__ (disabled by default):\n\n  - `$XONTRIB_CD_ALTSYMLINKFLAG = True` to pass `-p`, `-f`, or `-s` flags (in addition to `-P`) to follow symlinks\n  - `$XONTRIB_CD_ALTSYMLINKFUNC = True` to use `cdp`, `cdf`, or `cds` (in addition to `cd -P`) to follow symlinks\n  - `$XONTRIB_CD_SYMLINKAlWAYSON = True` to make `cd` always follow symlinks (always pass `-P`)\n\n## Known issues\n\nTo be discovered...\n\n## Credits\n\nThis package was created with [xontrib cookiecutter template](https://github.com/xonsh/xontrib-cookiecutter) based on the idea of hooking into the command line input as implemented in [xontrib-sh](https://github.com/anki-code/xontrib-sh)\n',
    'author': 'Evgeny',
    'author_email': 'es.bugzilla@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/eugenesvk/xontrib-cd',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
