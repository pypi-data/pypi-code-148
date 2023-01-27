# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['longeval',
 'longeval.linkage',
 'longeval.linkage.longchecker',
 'longeval.linkage.similarity',
 'longeval.linkage.summac']

package_data = \
{'': ['*'], 'longeval.linkage.similarity': ['sim/.gitkeep']}

install_requires = \
['bert-score>=0.3.12,<0.4.0',
 'nltk>=3.8.1,<4.0.0',
 'pandas==1.1',
 'pytorch-lightning==1.2.1',
 'rank-bm25>=0.2.2,<0.3.0',
 'rouge-score>=0.1.2,<0.2.0',
 'sentencepiece>=0.1.97,<0.2.0',
 'spacy>=3.5.0,<4.0.0',
 'torch>=1.13.1,<2.0.0',
 'tqdm>=4.64.1,<5.0.0',
 'transformers>=4.26.0,<5.0.0']

setup_kwargs = {
    'name': 'longeval',
    'version': '0.1.0',
    'description': 'Prepare your summarization data in a format compatible with the longeval guidelines for human evaluation.',
    'long_description': '## LongEval: Guidelines for Human Evaluation of Faithfulness in Long-form Summarization\n\nThis is the official repository for our EACL 2023 paper, LongEval: Guidelines for Human Evaluation of Faithfulness in Long-form Summarization. LongEval is a set of three guidelines to help manually evaluate factuality of long summaries. This repository provides the annotation data we collected, along with a command-line tool to prepare data in a format compatible with our annotation guidelines.\n\n### Setup\n\n```\n# from PyPI\n\npython3.7 -m virtualenv longeval-venv\nsource longeval-venv/bin/activate\npip install longeval\npython -m spacy download en_core_web_lg\n\n# from source\n\npython3.7 -m virtualenv longeval-venv\nsource longeval-venv/bin/activate\ngit clone https://github.com/martiansideofthemoon/longeval-summarization\ncd longeval-summarization\npip install --editable .\npython -m spacy download en_core_web_lg\n```\n\n**Other setup**\n\nDownload the SIM model from [here](https://drive.google.com/drive/folders/1lBN2nbzxtpqbPUyeURtzt0k1kBY6u6Mj?usp=share_link) if you are interested in using the non-default linker from [Wieting et al. 2019](https://aclanthology.org/P19-1427/). Place both files in `longeval/linkage/similarity/sim`.\n\n### Crowdsourcing Templates\n\nOur FINE-grained crowdsourcing interface can be found in [`templates/fine_sandbox_interface.html`](templates/fine_sandbox_interface.html). To use this interface, login to [AMT Sandbox](https://requestersandbox.mturk.com) and create a new project. Add this HTML code to the "Design Layout" tab. We also used this short instruction [video](https://youtu.be/LbZPo0AmXYI) to familiarize our FINE-grained annotators with the interface. Instructions to Upworkers for COARSE-grained evaluations on PubMed are provided in [`templates/coarse_instructions.md`](templates/coarse_instructions.md).\n\nNote that while we used AMT Sandbox to host our annotation interface, all our annotators were hired on Upwork only - no MTurk crowdworkers were used in our experiments. We provided Upwork annotations with the AMT Sandbox URL, and requested them to make an account on the interface. All payments were processed through Upwork only.\n\n### Preprocessing data\n\nTo get your summarization data in a format compatible with our templates,\n\n```\n\n```\n\n### Citation\n\nIf you found our paper or repository useful, please cite us using:\n\n```\n@inproceedings{longeval23,\nauthor={Kalpesh Krishna and Erin Bransom and Bailey Kuehl and Mohit Iyyer and Pradeep Dasigi and Arman Cohan and Kyle Lo},\nbooktitle = {European Chapter of the Association for Computational Linguistics},\nYear = "2023",\nTitle={LongEval: Guidelines for Human Evaluation of Faithfulness in Long-form Summarization},\n}\n```',
    'author': 'Kalpesh Krishna',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
