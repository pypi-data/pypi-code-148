# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['kapak', 'kapak.cli']

package_data = \
{'': ['*']}

install_requires = \
['cryptography>=39.0.0,<40.0.0']

entry_points = \
{'console_scripts': ['kapak = kapak.cli.__main__:main']}

setup_kwargs = {
    'name': 'kapak',
    'version': '4.0.0rc2',
    'description': 'A simple-to-use file encryption script',
    'long_description': '<p align="center">\n  <img src="https://user-images.githubusercontent.com/24605263/214285260-80aed843-17e6-4a2f-98bf-bfb21f900dff.png">\n</p>\n\n[![tests](https://github.com/amis-shokoohi/kapak/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/amis-shokoohi/kapak/actions/workflows/test.yml)\n[![codecov](https://codecov.io/gh/amis-shokoohi/kapak/branch/main/graph/badge.svg?token=6W2V3QOZKP)](https://codecov.io/gh/amis-shokoohi/kapak)\n![GitHub](https://img.shields.io/github/license/amis-shokoohi/kapak)\n![GitHub last commit (branch)](https://img.shields.io/github/last-commit/amis-shokoohi/kapak/main)\n![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/amis-shokoohi/kapak)\n![GitHub Repo stars](https://img.shields.io/github/stars/amis-shokoohi/kapak)\n![GitHub forks](https://img.shields.io/github/forks/amis-shokoohi/kapak)\n\n# kapak: A simple-to-use file encryption script\n\n- [Description](#description)\n- [Installation](#installation)\n- [CLI Usage](#cli-usage)\n  - [Encrypt file](#cli-usage-encrypt-file)\n  - [Encrypt stdin](#cli-usage-encrypt-stdin)\n  - [Password file](#cli-usage-password-file)\n- [Integration](#integration)\n  - [Encrypt file](#integration-encrypt-file)\n  - [Encrypt stdin](#integration-encrypt-stdin)\n\n<span id="description"></span>\n\n## Description\n\nKapak is a simple-to-use **file encryption** script.<br>\nIt uses `AES_256_CBC` as its encryption cipher and <br>\n`scrypt` key derivation algorithm to generate a 256 bit key.\n\n> If you are wondering what _kapak_ means, it means _mold_.\n\n<span id="installation"></span>\n\n## Installation\n\n```\npip install kapak\n```\n\n<span id="cli-usage"></span>\n\n## CLI Usage\n\n```\nkapak [global options] [command] [command options] [input]\nkapak [encrypt | e] [options] [input]\nkapak [decrypt | d] [options] [input]\n```\n\n<span id="cli-usage-encrypt-file"></span>\n\n### Encrypt file\n\n```\n$ kapak encrypt -o ./image.jpg.kpk ./image.jpg\nEnter password:\nConfirm password:\n■■■■■■■■■■ 100%\n```\n\n```\n$ kapak decrypt -o ./image.jpg ./image.jpg.kpk\nEnter password:\n■■■■■■■■■■ 100%\n```\n\n<span id="cli-usage-encrypt-stdin"></span>\n\n### Encrypt stdin\n\n```\n$ echo \'secret stuff\' | kapak encrypt | base64\nEnter password:\nConfirm password:\nAAAAbWth...t/ILJW/v\n```\n\n```\n$ echo \'AAAAbWth...t/ILJW/v\' | base64 --decode | kapak decrypt\nEnter password:\nsecret stuff\n```\n\n```\n$ cat ./text.txt | kapak encrypt -b 1024 > ./text.txt.kpk\nEnter password:\nConfirm password:\n```\n\n```\n$ kapak decrypt -b 1024 ./text.txt.kpk > ./text.txt\nEnter password:\n```\n\n<span id="cli-usage-password-file"></span>\n\n### Password file\n\n```\n$ echo \'P@ssw0rd\' > ./password.txt\n$ kapak encrypt -p ./password.txt -o ./image.jpg.kpk ./image.jpg\n■■■■■■■■■■ 100%\n```\n\n```\n$ kapak decrypt -p ./password.txt -o ./image.jpg ./image.jpg.kpk\n■■■■■■■■■■ 100%\n```\n\n<span id="integration"></span>\n\n## Integration\n\n<span id="integration-encrypt-file"></span>\n\n### Encrypt file\n\n```py\nfrom pathlib import Path\nfrom kapak.aes import encrypt\n\ninput_file = Path("image.jpg")\noutput_file = Path("image.jpg.kpk")\n\nwith input_file.open("rb") as src, output_file.open("wb") as dst:\n    total_len = input_file.stat().st_size\n    progress = 0\n    for chunk_len in encrypt(src, dst, "P@ssw0rd"):\n        progress += chunk_len\n        print(f"{progress}/{total_len}")\n```\n\n> `kapak.aes.encrypt` is a generator. It yields the length of encrypted data on every iteration.\n\n```py\nfrom pathlib import Path\nfrom itertools import accumulate\nfrom kapak.aes import decrypt\n\ninput_file = Path("image.jpg.kpk")\noutput_file = Path("image.jpg")\n\nwith input_file.open("rb") as src, output_file.open("wb") as dst:\n    total_len = input_file.stat().st_size\n    for progress in accumulate(decrypt(src, dst, "P@ssw0rd")):\n        print(f"{progress}/{total_len}")\n```\n\n> `kapak.aes.decrypt` is a generator. It yields the length of decrypted data on every iteration.\n\n<span id="integration-encrypt-stdin"></span>\n\n### Encrypt stdin\n\n```py\nimport io\nimport sys\nimport base64\nfrom kapak.aes import encrypt\n\nwith io.BytesIO() as dst:\n    for _ in encrypt(\n        src=sys.stdin.buffer,\n        dst=dst,\n        password="P@ssw0rd",\n        buffer_size=1024\n    ):\n        pass\n    encrypted_data = dst.getvalue()\n    encrypted_data_base64 = base64.standard_b64encode(encrypted_data)\n    print(encrypted_data_base64.decode("utf-8"))\n```\n',
    'author': 'Amis Shokoohi',
    'author_email': 'amisshokoohi@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/amis-shokoohi/kapak',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
