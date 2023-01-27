# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['epoa_tools', 'epoa_tools.data']

package_data = \
{'': ['*']}

install_requires = \
['fdfgen',
 'mdpdf',
 'pdf-redactor',
 'pypdf>=3.3.0,<4.0.0',
 'python-slugify',
 'reportlab']

entry_points = \
{'console_scripts': ['epoa-job-ad = epoa_tools.job_ad:main']}

setup_kwargs = {
    'name': 'epoa-tools',
    'version': '0.0.1',
    'description': 'EPOA pay transparency tools',
    'long_description': '# epoa-tools: WA EPOA pay transparency tools\n\n[![Build](https://img.shields.io/github/checks-status/smkent/epoa-tools/main?label=build)][gh-actions]\n[![codecov](https://codecov.io/gh/smkent/epoa-tools/branch/main/graph/badge.svg)][codecov]\n[![GitHub stars](https://img.shields.io/github/stars/smkent/epoa-tools?style=social)][repo]\n\n[Washington state\'s Equal Pay and Opportunities Act][li-epoa] requires pay\nranges to be included on job ads ([RCW 49.58.110][rcw]). WA L&I provides a [PDF\ncomplaint form][li-complaint-form] for violations. `epoa-tools` automates some\nof the toil around this form, such as filling out basic information, checking\nthe right boxes, and optionally including additional PDF files as evidence (e.g.\nthe related job posting without pay range information).\n\nThe output is a single PDF which can be dropped into [WA L&I\'s secure file\nupload][li-file-upload].\n\n## Prerequisites\n\n`epoa-tools` depends on `pdftk` for filling out forms and joining pages.\n\nOn Debian / Ubuntu, install with:\n\n```shell\nsudo apt install pdftk-java\n```\n\n## Installation\n\n```\npip install epoa-tools\n```\n\n## Usage\n\nSave a PDF file with evidence of the violation (e.g. job ad or recruiter email).\nBrowsers can print or save web pages as PDFs.\n\nThen, use `epoa-job-ad` to complete the complaint form, attaching your evidence\nfile:\n\n```shell\nepoa-job-ad \\\n    --name "John Q. Public" --email john.q.public@example.com \\\n    "ACME Anti-Pay Ranges, Inc." \\\n    saved_job_ad.pdf\n```\n\nTo file anonymously, omit the `--name` argument. The complainant name on the\nform will be listed as `Anonymous` and the signature line will contain\n`Anonymous (your.email.address@example.com)`:\n\n```shell\nepoa-job-ad \\\n    --email anon.e.mouse@example.com \\\n    "ACME Anti-Pay Ranges, Inc." \\\n    saved_job_ad.pdf\n```\n\nOptionally include additional information text about your complaint with the\n`-i` / `--addinfo` / `--additional-information` option:\n\n```shell\nepoa-job-ad \\\n    --email anon.e.mouse@example.com \\\n    "ACME Anti-Pay Ranges, Inc." \\\n    saved_job_ad.pdf \\\n    -i "This job ad is public, contains specific job requirements for a job in WA, but lists no pay range"\n```\n\nWord(s) can be redacted from evidence file attachments on a best effort basis:\n```shell\nepoa-job-ad \\\n    --email anon.e.mouse@example.com \\\n    "ACME Anti-Pay Ranges, Inc." \\\n    saved_job_ad.pdf \\\n    -r remove_this_word -r also_remove_this_word\n```\n\nEach of these examples creates a file such as\n`john-q-public-acme-anti-pay-ranges-inc-20230101-pay-transparency-complaint.pdf`\nwhich can then be [uploaded to WA L&I][li-file-upload].\n\n## Development\n\n### [Poetry][poetry] installation\n\nVia [`pipx`][pipx]:\n\n```console\npip install pipx\npipx install poetry\npipx inject poetry poetry-dynamic-versioning poetry-pre-commit-plugin\n```\n\nVia `pip`:\n\n```console\npip install poetry\npoetry self add poetry-dynamic-versioning poetry-pre-commit-plugin\n```\n\n### Development tasks\n\n* Setup: `poetry install`\n* Run static checks: `poetry run poe lint` or\n  `poetry run pre-commit run --all-files`\n* Run static checks and tests: `poetry run poe test`\n\n---\n\nCreated from [smkent/cookie-python][cookie-python] using\n[cookiecutter][cookiecutter]\n\n[codecov]: https://codecov.io/gh/smkent/epoa-tools\n[cookie-python]: https://github.com/smkent/cookie-python\n[cookiecutter]: https://github.com/cookiecutter/cookiecutter\n[gh-actions]: https://github.com/smkent/epoa-tools/actions?query=branch%3Amain\n[li-complaint-form]: https://www.lni.wa.gov/forms-publications/F700-200-000.pdf\n[li-epoa]: https://www.lni.wa.gov/workers-rights/wages/equal-pay-opportunities-act/\n[li-file-upload]: https://lni.app.box.com/f/81096b771d1243c0aab00fea150f8c6a\n[pipx]: https://pypa.github.io/pipx/\n[poetry]: https://python-poetry.org/docs/#installation\n[rcw]: https://app.leg.wa.gov/RCW/default.aspx?cite=49.58.110\n[repo]: https://github.com/smkent/epoa-tools\n',
    'author': 'Stephen Kent',
    'author_email': 'smkent@smkent.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/smkent/epoa-tools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
