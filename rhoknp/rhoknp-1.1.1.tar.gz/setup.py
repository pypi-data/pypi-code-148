# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['rhoknp',
 'rhoknp.cli',
 'rhoknp.cohesion',
 'rhoknp.processors',
 'rhoknp.props',
 'rhoknp.units',
 'rhoknp.utils']

package_data = \
{'': ['*']}

extras_require = \
{':python_version < "3.8"': ['cached-property>=1.5,<2.0',
                             'importlib-metadata>=5.2,<6.0']}

entry_points = \
{'console_scripts': ['rhoknp = rhoknp.cli.cli:app']}

setup_kwargs = {
    'name': 'rhoknp',
    'version': '1.1.1',
    'description': 'Yet another Python binding for Juman++/KNP/KWJA',
    'long_description': '# rhoknp: Yet another Python binding for Juman++/KNP/KWJA\n\n[![Test](https://img.shields.io/github/actions/workflow/status/ku-nlp/rhoknp/test.yml?branch=main&logo=github&label=test&style=flat-square)](https://github.com/ku-nlp/rhoknp/actions/workflows/test.yml)\n[![Codecov](https://img.shields.io/codecov/c/github/ku-nlp/rhoknp?logo=codecov&style=flat-square)](https://codecov.io/gh/ku-nlp/rhoknp)\n[![CodeFactor](https://img.shields.io/codefactor/grade/github/ku-nlp/rhoknp?style=flat-square)](https://www.codefactor.io/repository/github/ku-nlp/rhoknp)\n[![PyPI](https://img.shields.io/pypi/v/rhoknp?style=flat-square)](https://pypi.org/project/rhoknp/)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/rhoknp?style=flat-square)\n[![Documentation](https://img.shields.io/readthedocs/rhoknp?style=flat-square)](https://rhoknp.readthedocs.io/en/latest/?badge=latest)\n[![Code style - black](https://img.shields.io/badge/code%20style-black-222222?style=flat-square)](https://github.com/psf/black)\n\n*rhoknp* is a Python binding for [Juman++](https://github.com/ku-nlp/jumanpp), [KNP](https://github.com/ku-nlp/knp), and [KWJA](https://github.com/ku-nlp/kwja).\n\n```python\nimport rhoknp\n\n# Perform language analysis by Juman++\njumanpp = rhoknp.Jumanpp()\nsentence = jumanpp.apply_to_sentence(\n    "電気抵抗率は電気の通しにくさを表す物性値である。"\n)\n\n# Access to the result\nfor morpheme in sentence.morphemes:  # a.k.a. keitai-so\n    ...\n\n# Save language analysis by Juman++\nwith open("result.jumanpp", "wt") as f:\n    f.write(sentence.to_jumanpp())\n\n# Load language analysis by Juman++\nwith open("result.jumanpp", "rt") as f:\n    sentence = rhoknp.Sentence.from_jumanpp(f.read())\n```\n\n## Requirements\n\n- Python 3.7+\n\n## Optional requirements for language analysis\n\n- [Juman++](https://github.com/ku-nlp/jumanpp) v2.0.0-rc3+\n- [KNP](https://github.com/ku-nlp/knp) 5.0+\n- [KWJA](https://github.com/ku-nlp/kwja) 1.0.0+\n\n## Installation\n\n```shell\npip install rhoknp\n```\n\n## Documentation\n\n[https://rhoknp.readthedocs.io/en/latest/](https://rhoknp.readthedocs.io/en/latest/)\n\n## Quick tour\n\nLet\'s start with using Juman++ with *rhoknp*.\nHere is a simple example of using Juman++ to analyze a sentence.\n\n```python\n# Perform language analysis by Juman++\njumanpp = rhoknp.Jumanpp()\nsentence = jumanpp.apply_to_sentence("電気抵抗率は電気の通しにくさを表す物性値である。")\n```\n\nYou can easily access the morphemes that make up the sentence.\n\n```python\nfor morpheme in sentence.morphemes:  # a.k.a. keitai-so\n    ...\n```\n\nSentence objects can be saved in the JUMAN format.\n\n```python\n# Save the sentence in the JUMAN format\nwith open("sentence.jumanpp", "wt") as f:\n    f.write(sentence.to_jumanpp())\n\n# Load the sentence\nwith open("sentence.jumanpp", "rt") as f:\n    sentence = rhoknp.Sentence.from_jumanpp(f.read())\n```\n\nAlmost the same APIs are available for KNP.\n\n```python\n# Perform language analysis by KNP\nknp = rhoknp.KNP()\nsentence = knp.apply_to_sentence("電気抵抗率は電気の通しにくさを表す物性値である。")\n```\n\nKNP performs language analysis at multiple levels.\n\n```python\nfor clause in sentence.clauses:  # a.k.a., setsu\n    ...\nfor phrase in sentence.phrases:  # a.k.a. bunsetsu\n    ...\nfor base_phrase in sentence.base_phrases:  # a.k.a. kihon-ku\n    ...\nfor morpheme in sentence.morphemes:  # a.k.a. keitai-so\n    ...\n```\n\nSentence objects can be saved in the KNP format.\n\n```python\n# Save the sentence in the KNP format\nwith open("sentence.knp", "wt") as f:\n    f.write(sentence.to_knp())\n\n# Load the sentence\nwith open("sentence.knp", "rt") as f:\n    sentence = rhoknp.Sentence.from_knp(f.read())\n```\n\n*rhoknp* also provides APIs for document-level language analysis.\n\n```python\ndocument = rhoknp.Document.from_raw_text(\n    "電気抵抗率は電気の通しにくさを表す物性値である。単に抵抗率とも呼ばれる。"\n)\n# If you know sentence boundaries, you can use `Document.from_sentences` instead.\ndocument = rhoknp.Document.from_sentences(\n    [\n        "電気抵抗率は電気の通しにくさを表す物性値である。",\n        "単に抵抗率とも呼ばれる。",\n    ]\n)\n```\n\nDocument objects can be handled in almost the same way as Sentence objects.\n\n```python\n# Perform language analysis by Juman++\ndocument = jumanpp.apply_to_document(document)\n\n# Access language units in the document\nfor sentence in document.sentences:\n    ...\nfor morpheme in document.morphemes:\n    ...\n\n# Save language analysis by Juman++\nwith open("document.jumanpp", "wt") as f:\n    f.write(document.to_jumanpp())\n\n# Load language analysis by Juman++\nwith open("document.jumanpp", "rt") as f:\n    document = rhoknp.Document.from_jumanpp(f.read())\n```\n\nFor more information, explore the [examples](./examples) and [documentation](https://rhoknp.readthedocs.io/en/latest/).\n\n## Main differences from [pyknp](https://github.com/ku-nlp/pyknp/)\n\n[*pyknp*](https://pypi.org/project/pyknp/) has been developed as the official Python binding for Juman++ and KNP.\nIn *rhoknp*, we redesigned the API from the top-down, taking into account the current use cases of *pyknp*.\nThe main differences are as follows:\n\n- **Support for document-level language analysis**: *rhoknp* can load and instantiate the result of document-level language analysis (i.e., cohesion analysis and discourse relation analysis).\n- **Strictly type-aware**: *rhoknp* is thoroughly annotated with type annotations.\n- **Extensive test suite**: *rhoknp* is tested with an extensive test suite. See the code coverage at [Codecov](https://app.codecov.io/gh/ku-nlp/rhoknp).\n\n## License\n\nMIT\n\n## Contributing\n\nWe welcome contributions to *rhoknp*.\nYou can get started by reading the [contribution guide](https://rhoknp.readthedocs.io/en/latest/contributing/index.html).\n\n## Reference\n\n- [KNP FORMAT](http://cr.fvcrc.i.nagoya-u.ac.jp/~sasano/knp/format.html)\n- [KNP - KUROHASHI-CHU-MURAWAKI LAB](https://nlp.ist.i.kyoto-u.ac.jp/?KNP)\n',
    'author': 'Hirokazu Kiyomaru',
    'author_email': 'h.kiyomaru@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ku-nlp/rhoknp',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.12',
}


setup(**setup_kwargs)
