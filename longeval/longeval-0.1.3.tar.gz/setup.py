# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['longeval',
 'longeval.linkage',
 'longeval.linkage.longchecker',
 'longeval.linkage.similarity',
 'longeval.linkage.summac',
 'longeval.metrics']

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
 'spacy==3.0.0',
 'statsmodels>=0.13.5,<0.14.0',
 'torch>=1.13.1,<2.0.0',
 'tqdm>=4.64.1,<5.0.0',
 'transformers>=4.26.0,<5.0.0']

setup_kwargs = {
    'name': 'longeval',
    'version': '0.1.3',
    'description': 'Prepare your summarization data in a format compatible with the longeval guidelines for human evaluation.',
    'long_description': '## LongEval: Guidelines for Human Evaluation of Faithfulness in Long-form Summarization\n\n[![made-with-python](https://img.shields.io/badge/Made%20with-Python-red.svg)](#python)\n[![PyPI version longeval](https://badge.fury.io/py/longeval.svg)](https://pypi.python.org/pypi/longeval/) [![License: Apache 2.0](https://img.shields.io/badge/License-Apache--2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)\n[![Downloads](https://pepy.tech/badge/longeval)](https://pepy.tech/project/longeval)\n\nThis is the official repository for our EACL 2023 paper, [LongEval: Guidelines for Human Evaluation of Faithfulness in Long-form Summarization](https://martiansideofthemoon.github.io/assets/longeval.pdf). LongEval is a set of three guidelines to help manually evaluate factuality of long summaries. This repository provides the annotation data we collected, along with a command-line tool to prepare data in a format compatible with our annotation guidelines.\n\n### Setup\n\n```\n# from PyPI\n\npython3.7 -m virtualenv longeval-venv\nsource longeval-venv/bin/activate\npip install longeval\npython -m spacy download en_core_web_lg\n\n# from source\n\npython3.7 -m virtualenv longeval-venv\nsource longeval-venv/bin/activate\ngit clone https://github.com/martiansideofthemoon/longeval-summarization\ncd longeval-summarization\npip install --editable .\npython -m spacy download en_core_web_lg\n```\n\nAdditionally, download the SIM model from [here](https://drive.google.com/drive/folders/1lBN2nbzxtpqbPUyeURtzt0k1kBY6u6Mj?usp=share_link) if you are interested in using the non-default linker from [Wieting et al. 2019](https://aclanthology.org/P19-1427/). Place both files in `longeval/linkage/similarity/sim`.\n\nTo test the implementation works correctly, run the experiment to evaluate SuperPAL\'s linking abilities (Table 4 in Section 3.3):\n\n```\npython -m longeval.evaluate_linkers --linking_algorithm superpal\n\n# Expected output (takes 5-6 min to run)\nBest match:\nRecall@3 = 0.6080 (76 / 125)\nRecall@5 = 0.6800 (85 / 125)\nRecall@10 = 0.7680 (96 / 125)\n```\n\n### Crowdsourcing Templates\n\nOur FINE-grained crowdsourcing interface can be found in [`templates/fine_sandbox_interface.html`](templates/fine_sandbox_interface.html). To use this interface, login to [AMT Sandbox](https://requestersandbox.mturk.com) and create a new project. Add this HTML code to the "Design Layout" tab. We also used this short instruction [video](https://youtu.be/LbZPo0AmXYI) to familiarize our FINE-grained annotators with the interface. Instructions to Upworkers for COARSE-grained evaluations on PubMed are provided in [`templates/coarse_instructions.md`](templates/coarse_instructions.md).\n\nNote that while we used AMT Sandbox to host our annotation interface, all our annotators were hired on Upwork only - no MTurk crowdworkers were used in our experiments. We provided Upwork annotations with the AMT Sandbox URL, and requested them to make an account on the interface. All payments were processed through Upwork only.\n\n### Preprocessing data\n\nTo get your summarization data in a format compatible with our templates,\n\n```\npython -m longeval.prepare_summaries \\\n    --src_file data/pubmed_summaries/beam_3.jsonl \\\n    --scu_fraction 0.5 \\\n    --num_articles 3 \\\n    --num_truncate_splits 3 \\\n    --linking_algorithm superpal \\\n    --output_dir outputs/pubmed_beam_3 \\\n    --included_models "bigbird_pegasus;longt5;human"\n```\n\nEach source article produces a different file containing all the summaries for that particular article. Make sure the input file is a JSONL file, with the `"article"` key representing the source document and one key for each model\'s summary. See [`data/pubmed_summaries/beam_3.jsonl`](data/pubmed_summaries/beam_3.jsonl) for an example.\n\n### Annotated Data\n\n**FINE/COARSE annotations**\n\nAll the annotations can be found in this [Google Drive link](https://drive.google.com/drive/folders/1nLVmPQMmX_XOHrc_0I7oJBJfl6EMRqeK?usp=share_link). After downloading the data, place it in `data`. The annotations follow the AMT / LabelStudio formats, which may appear a bit complex. Functions to read-in the data are provided in [`longeval/metrics_corr_confidence_pubmed.py`](metrics_corr_confidence_pubmed.py).\n\nRunning metric correlation scripts on this data (Figure 2) needs a few additional setup steps which we haven\'t included in the PyPI package due to dependency issues.\n\n1. Setup BLEURT using the instructions here: https://github.com/google-research/bleurt\n\n2. Setup SacreROUGE: https://github.com/danieldeutsch/sacrerouge, or simply run `pip install sacrerouge`\n\n3. Upgrade HuggingFace Hub since SacreROUGE downgrades it to an incompatible version.\n\n```\npip install --upgrade huggingface-hub\n```\n\nAfter this setup simply run the following to reproduce Figure 2:\n\n```\npython -m longeval.metrics_corr_confidence_squality\npython -m longeval.metrics_corr_confidence_pubmed\n```\n\n**SQuALITY source-summary alignments**\n\nFinally, our hand-annotated source-summary alignment data in SQuALITY can be found in [`data/squality_alignment/data.json`](data/squality_alignment/data.json). To test linking algorithms on this run:\n\n```\npython -m longeval.evaluate_linkers --linking_algorithm superpal\n```\n\nYou can set `--linking_algorithm` to any of the algorithms in the `get_linking_fn` function written in [`longeval/linkage/utils.py`](longeval/linkage/utils.py).\n\n### Citation\n\nIf you found our paper or repository useful, please cite us using:\n\n```\n@inproceedings{longeval23,\nauthor={Kalpesh Krishna and Erin Bransom and Bailey Kuehl and Mohit Iyyer and Pradeep Dasigi and Arman Cohan and Kyle Lo},\nbooktitle = {European Chapter of the Association for Computational Linguistics},\nYear = "2023",\nTitle={LongEval: Guidelines for Human Evaluation of Faithfulness in Long-form Summarization},\n}\n```',
    'author': 'Kalpesh Krishna, Erin Bransom, Bailey Kuehl, Mohit Iyyer, Pradeep Dasigi, Arman Cohan, Kyle Lo',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/martiansideofthemoon/longeval-summarization',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
