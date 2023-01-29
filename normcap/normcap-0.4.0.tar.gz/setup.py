# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['normcap',
 'normcap.clipboard',
 'normcap.gui',
 'normcap.ocr',
 'normcap.ocr.magics',
 'normcap.resources',
 'normcap.screengrab']

package_data = \
{'': ['*'], 'normcap.resources': ['icons/*', 'tessdata/*']}

install_requires = \
['PySide6-Essentials>=6.4.1,<7.0.0',
 'certifi>=2022.12.7,<2023.0.0',
 'jeepney>=0.8.0,<0.9.0',
 'pytesseract>=0.3.10']

entry_points = \
{'console_scripts': ['normcap = normcap.app:main']}

setup_kwargs = {
    'name': 'normcap',
    'version': '0.4.0',
    'description': 'OCR-powered screen-capture tool to capture information instead of images.',
    'long_description': '<!-- markdownlint-disable MD013 MD026 MD033 -->\n\n# NormCap\n\n**_OCR powered screen-capture tool to capture information instead of images. For Linux,\nmacOS and Windows._**\n\n[![Build](https://img.shields.io/github/actions/workflow/status/dynobo/normcap/python.yaml?branch=main)](https://github.com/dynobo/normcap/releases)\n[![Coverage Status](https://img.shields.io/coverallsCoverage/github/dynobo/normcap?label=Test%20coverage&branch=main)](https://coveralls.io/github/dynobo/normcap)\n[![CodeQL](https://img.shields.io/github/actions/workflow/status/dynobo/normcap/codeql-analysis.yml?branch=main&label=CodeQL)](https://github.com/dynobo/normcap/actions/workflows/codeql-analysis.yml)\n\n[![GitHub](https://img.shields.io/github/downloads/dynobo/normcap/total?label=Github%20downloads&color=blue)](https://github.com/dynobo/normcap/releases)\n[![PyPi](https://img.shields.io/pypi/dm/normcap?label=PyPi%20downloads&color=blue)](https://pypi.org/project/normcap)\n[![Flathub](https://img.shields.io/flathub/downloads/com.github.dynobo.normcap?label=Flathub%20downloads&color=blue)](https://flathub.org/apps/details/com.github.dynobo.normcap)\n[![AUR](https://img.shields.io/aur/votes/normcap?label=AUR%20votes&color=blue)](https://aur.archlinux.org/packages/normcap)\n\n**Links:** [Source Code](https://github.com/dynobo/normcap) |\n[Documentation](https://dynobo.github.io/normcap/) |\n[FAQs](https://dynobo.github.io/normcap/#faqs) |\n[Releases](https://github.com/dynobo/normcap/releases) |\n[Changelog](https://github.com/dynobo/normcap/blob/main/CHANGELOG.md)\n\n[![Screencast](https://user-images.githubusercontent.com/11071876/189767585-8bc45c18-8392-411d-84dc-cef1cb5dbc47.gif)](https://raw.githubusercontent.com/dynobo/normcap/main/assets/normcap.gif)\n\n## Quickstart\n\nInstall a prebuilt release:\n\n- **Windows**:\n  [NormCap-0.4.0-x86_64-Windows.msi](https://github.com/dynobo/normcap/releases/download/v0.4.0/NormCap-0.4.0-x86_64-Windows.msi)\n- **Linux**:\n  [NormCap-0.4.0-x86_64.AppImage](https://github.com/dynobo/normcap/releases/download/v0.4.0/NormCap-0.4.0-x86_64.AppImage)\n- **macOS** (x86) ¹:\n  [NormCap-0.4.0-x86_64-macOS.dmg](https://github.com/dynobo/normcap/releases/download/v0.4.0/NormCap-0.4.0-x86_64-macOS.dmg)\n- **macOS** (M1) ¹·²:\n  [NormCap-0.4.0-arm64-macOS.dmg](https://github.com/dynobo/normcap/releases/download/v0.4.0/NormCap-0.4.0-arm64-macOS.dmg)\n  \\\n  <sub>1: On macOS, allow the unsigned application on first start: "System\n  Preferences" → "Security & Privacy" → "General" → "Open anyway". You might also need\n  to allow NormCap to take screenshots.\n  [#135](https://github.com/dynobo/normcap/issues/135)<br> 2: Might be available a bit\n  delayed, as it is currently build manually. (Thx,\n  [@Takrin](https://github.com/Takrin)!)</sub>\n\nInstall from repositories:\n\n- **Arch / Manjaro**: Install the\n  [`normcap`](https://aur.archlinux.org/packages/normcap) package from AUR.\n- **FlatPak (Linux)**: Install\n  [com.github.dynobo.normcap](https://flathub.org/apps/details/com.github.dynobo.normcap)\n  from FlatHub.\n\nIf you experience issues please look at the\n[FAQs](https://dynobo.github.io/normcap/#faqs) or\n[open an issue](https://github.com/dynobo/normcap/issues).\n\n## Python package\n\nAs an _alternative_ to a prebuilt package you can install the\n[NormCap Python package](https://pypi.org/project/normcap/) for **Python >=3.9**:\n\n#### On Linux\n\n```sh\n# Install dependencies (Ubuntu/Debian)\nsudo apt install build-essential tesseract-ocr tesseract-ocr-eng libtesseract-dev libleptonica-dev wl-clipboard\n\n## Install dependencies (Arch)\nsudo pacman -S tesseract tesseract-data-eng wl-clipboard\n\n## Install dependencies (Fedora)\nsudo dnf install tesseract wl-clipboard\n\n## Install dependencies (openSUSE)\nsudo zypper install python3-devel tesseract-ocr tesseract-ocr-devel wl-clipboard\n\n# Install normcap\npip install normcap\n\n# Run\n./normcap\n```\n\n#### On macOS\n\n```sh\n# Install dependencies\nbrew install tesseract tesseract-lang\n\n# Install normcap\npip install normcap\n\n# Run\n./normcap\n```\n\n#### On Windows\n\n1\\. Install `Tesseract 5` by using the\n[installer provided by UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki).\n\n2\\. Adjust environment variables:\n\n- Create an environment variable `TESSDATA_PREFIX` and set it to Tesseract\'s data\n  folder, e.g.:\n\n  ```cmd\n  setx TESSDATA_PREFIX "C:\\Program Files\\Tesseract-OCR\\tessdata"\n  ```\n\n- Append Tesseract\'s location to the environment variable `Path`, e.g.:\n\n  ```cmd\n  setx Path "%Path%;C:\\Program Files\\Tesseract-OCR"\n  ```\n\n- Make sure to close and reopen your current terminal window to apply the new variables.\n  Test it by running:\n\n  ```cmd\n  tesseract --list-langs\n  ```\n\n3\\. Install and run NormCap:\n\n```bash\n# Install normcap\npip install normcap\n\n# Run\nnormcap\n```\n\n## Why "NormCap"?\n\nSee [XKCD](https://xkcd.com):\n\n[![Comic](https://imgs.xkcd.com/comics/norm_normal_file_format.png)](https://xkcd.com/2116/)\n\n## Development\n\nPrerequisites for setting up a development environment are: **Python >=3.9**,\n**Poetry>=1.3.2** and **Tesseract** (incl. **language data**).\n\n```sh\n# Clone repository\ngit clone https://github.com/dynobo/normcap.git\n\n# Change into project directory\ncd normcap\n\n# Create virtual env and install dependencies\npoetry install\n\n# Register pre-commit hook\npoetry run pre-commit install\n\n# Run NormCap in virtual env\npoetry run python -m normcap\n```\n\n## Credits\n\nThis project uses the following non-standard libraries:\n\n- [pyside6](https://pypi.org/project/PySide6/) _- bindings for Qt UI Framework_\n- [pytesseract](https://pypi.org/project/pytesseract/) _- wrapper for tesseract\'s API_\n- [jeepney](https://pypi.org/project/jeepney/) _- DBUS client_\n\nAnd it depends on external software:\n\n- [tesseract](https://github.com/tesseract-ocr/tesseract) - _OCR engine_\n- [wl-clipboard](https://github.com/bugaevc/wl-clipboard) - _Wayland clipboard\n  utilities_\n\nPackaging is done with:\n\n- [briefcase](https://pypi.org/project/briefcase/) _- converting Python projects into_\n  _standalone apps_\n\nThanks to the maintainers of those nice tools!\n\n## Similar open source tools\n\nIf NormCap doesn\'t fit your needs, try those alternatives (no particular order):\n\n- [TextSnatcher](https://github.com/RajSolai/TextSnatcher) (Linux)\n- [GreenShot](https://getgreenshot.org/) (Linux, macOS)\n- [TextShot](https://github.com/ianzhao05/textshot) (Windows)\n- [gImageReader](https://github.com/manisandro/gImageReader) (Linux, Windows)\n- [Capture2Text](https://sourceforge.net/projects/capture2text) (Windows)\n- [Frog](https://github.com/TenderOwl/Frog) (Linux)\n- [Textinator](https://github.com/RhetTbull/textinator) (macOS)\n\n## Certification\n\n![WOMM](https://raw.githubusercontent.com/dynobo/lmdiag/master/badge.png)\n',
    'author': 'dynobo',
    'author_email': 'dynobo@mailbox.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://dynobo.github.io/normcap/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.12',
}


setup(**setup_kwargs)
