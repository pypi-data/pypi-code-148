# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xontrib_homebrew']

package_data = \
{'': ['*']}

install_requires = \
['xonsh>=0.12.5']

entry_points = \
{'xonsh.xontribs': ['homebrew = xontrib_homebrew.main']}

setup_kwargs = {
    'name': 'xontrib-homebrew',
    'version': '0.2.1',
    'description': "Add Homebrew's shell environment to xonsh on macOS/Linux",
    'long_description': '<p align="center">\nAdd <a href="https://brew.sh"><b>Homebrew</b></a>\'s shell environment to <a href="https://xon.sh"><b>xonsh</b></a> shell on <b>macOS</b>/<b>Linux</b>\n<br/>\n(alternative to <a href="https://docs.brew.sh/Homebrew-on-Linux">shellenv</a>).\n</p>\n\n<p align="center">  \nIf you like the idea click ⭐ on the repo and <a href="https://twitter.com/intent/tweet?text=Nice%20xontrib%20for%20the%20xonsh%20shell!&url=https://github.com/eugenesvk/xontrib-homebrew" target="_blank">tweet</a>. This might also accelerate adding <a href="https://github.com/Homebrew/brew/pull/10757#issuecomment-791381047">xonsh support to Homebrew</a>.\n</p>\n\n\n## Introduction\n\n__Homebrew__ has a `shellenv` command to add __its environment__ to your shell: it adds a few\nenvironment variables (`HOMEBREW_` `PREFIX`/`CELLAR`/`REPOSITORY`) and updates a few paths (`MAN`/`INFO`/ `PATH`).\n\nThis xontrib automatically translates the default __bash__ export statements of `shellenv` into __xonsh__.\n\n## Installation\n\nTo install use pip:\n\n```bash\nxpip install xontrib-homebrew\n# or: xpip install -U git+https://github.com/eugenesvk/xontrib-homebrew\n```\n\nThis xontrib will get loaded automatically for interactive sessions; to stop this, set\n\n```xonsh\n$XONTRIBS_AUTOLOAD_DISABLED = {"homebrew", }\n```\n\n## Usage\n\nAdd this to your xonsh run control file (`~/.xonshrc` or `~/.config/rc.xsh`):\n```bash\nxontrib load homebrew\n```\n\nSet custom Homebrew installation path via `$XONTRIB_HOMEBREW_PATHBREW` to `/full/path/to/bin/brew` if it\'s not installed at these default paths (which always take precedence):\n\n| macOS                   \t| Linux                                \t|\n|:------------------------\t|:-------------------------------------\t|\n| `/usr/local/bin/brew`   \t| `/home/linuxbrew/.linuxbrew/bin/brew`\t|\n| `/opt/homebrew/bin/brew`\t| `~/.linuxbrew/bin/brew`              \t|\n\nSet the level of verbosity via `$XONTRIB_HOMEBREW_LOGLEVEL` to __0–3__ (default __1__):\n\n  - 0 print nothing (fail silently)\n  - __1__ print errors (e.g. can\'t find `brew` at default locations)\n  - 2 print warnings (e.g issues when parsing `shellenv`)\n  - 3 print more verbose messages\n\n## Known issues\n\n- Xontrib autoload currently can\'t be disabled due to a [xonsh bug](https://github.com/xonsh/xonsh/issues/5020), so if you need precise control over when your environment variables are set (e.g., whether `/path/to/homebrew/bin` is at the top of `PATH`), try installing from a `deauto` branch:</br>\n  `xpip install -U git+https://github.com/eugenesvk/xontrib-homebrew@deauto`\n- Likely due to the same bug your `$XONTRIB_HOMEBREW_PATHBREW` and `$XONTRIB_HOMEBREW_LOGLEVEL` env vars might be ignored in the autoloaded version, so install the `@deauto` version mentioned above\n\n## Credits\n\nThis package was created with [xontrib cookiecutter template](https://github.com/xonsh/xontrib-cookiecutter).\n',
    'author': 'Evgeny',
    'author_email': 'es.bugzilla@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/eugenesvk/xontrib-homebrew',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
