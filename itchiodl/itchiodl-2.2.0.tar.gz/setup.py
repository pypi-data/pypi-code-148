# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['itchiodl', 'itchiodl.bundle_tool', 'itchiodl.downloader']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.10.0,<5.0.0',
 'clint>=0.5.1,<0.6.0',
 'requests>=2.28.1,<3.0.0']

entry_points = \
{'console_scripts': ['itch-download = itchiodl.downloader.__main__:main',
                     'itch-load-bundle = itchiodl.bundle_tool.__main__:main']}

setup_kwargs = {
    'name': 'itchiodl',
    'version': '2.2.0',
    'description': 'Python Scripts for downloading / archiving your itchio library',
    'long_description': '## IMPORTANT NOTICE: up until 2022-03-09, the package was called itchio, it is now called itchiodl (to avoid pypi conflicts)\n\n# Itchio Downloader Tool\n## Install\n```bash\npip install itchiodl\n```\n## Download All Games in library from account\n**Please Note:** Having too many jobs may cause rate-limiting from some testing 8 works fine but 10 starts giving errors.\n\n```bash\n# via python\npython -m itchiodl.downloader\n\n# via setup-tools entry point\nitch-download\n```\n\nThis uses the same API the itchio app uses to download the files. If you have 2FA enabled, generate an API key [here](https://itch.io/user/settings/api-keys) and run the following instead\n\n```bash\n# via python (with 4 concurrent downloads)\npython -m itchiodl.downloader --api-key=KEYHERE --jobs=4\n\n# via setup-tools entry point\nitch-download -k KEYHERE\n\n# download with multiple threads\nitch-download -k KEYHERE -j 4\n\n# only download osx or cross platform downloads\nitch-download -p osx\n```\n\n## Add All Games in a bundle to your library\n\n```bash\n# via python\npython -m itchiodl.bundle_tool\n\n# via setup-tools entry point\nitch-load-bundle\n```\n\nThis is a bit of a bodge, but it works. It essentially goes through and clicks the "Download" link on every item on the bundle\'s page, which adds it to your itchio library. It does not download any files. You will need the download page\'s URL (this will be in the bundle\'s email, and possibly your purchase history). It will not work with 2FA, and I\'m unlikely to be able to fix it without making it far more complicated\n\n\n## Errors\nif a download fails it will be reported in ```errors.txt``` in the same directory as your downloads\n\nAn example of which could look something like this:\n```Cannot download game/asset: <Game Name>\nPublisher Name: <Publisher Name>\nOutput File: <Publisher Name>/<Game Name>/<Specific Item>\nRequest URL: <Some URL>\nRequest Response Code: 404\nError Reason: Not Found\nThis game/asset has been skipped please download manually\n---------------------------------------------------------\n```\n\nThis is not a perfect solution but does prevent the whole process from crashing\n',
    'author': 'Peter Taylor',
    'author_email': 'me@et1.uk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
