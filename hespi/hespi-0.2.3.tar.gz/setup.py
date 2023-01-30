# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hespi', 'hespi.data']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0',
 'pytesseract>=0.3.10,<0.4.0',
 'rich>=10.16.1,<11.0.0',
 'torchapp>=0.2.0,<0.3.0',
 'transformers>=4.21.3,<5.0.0',
 'typer>=0.4.0,<0.5.0',
 'yolov5>=6.1.8,<7.0.0']

entry_points = \
{'console_scripts': ['hespi = hespi.main:app']}

setup_kwargs = {
    'name': 'hespi',
    'version': '0.2.3',
    'description': 'HErbarium Specimen sheet PIpeline',
    'long_description': "================================================================\nhespi\n================================================================\n\n.. image:: https://raw.githubusercontent.com/rbturnbull/hespi/main/docs/images/hespi-banner.svg\n\n.. start-badges\n\n|testing badge| |coverage badge| |docs badge| |black badge|\n\n.. |testing badge| image:: https://github.com/rbturnbull/hespi/actions/workflows/testing.yml/badge.svg\n    :target: https://github.com/rbturnbull/hespi/actions\n\n.. |docs badge| image:: https://github.com/rbturnbull/hespi/actions/workflows/docs.yml/badge.svg\n    :target: https://rbturnbull.github.io/hespi\n    \n.. |black badge| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/psf/black\n    \n.. |coverage badge| image:: https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/rbturnbull/f31036b00473b6d0af3a160ea681903b/raw/coverage-badge.json\n    :target: https://rbturnbull.github.io/hespi/coverage/\n    \n.. end-badges\n\nHErbarium Specimen sheet PIpeline\n\n.. start-quickstart\n\nHespi takes images of specimen sheets from herbaria and first detects the various components of the sheet. These components include:\n\n- small database label\n- handwritten data\n- stamp\n- annotation label\n- scale\n- swing tag\n- full database label\n- database label\n- swatch\n- institutional label\n- number\n\nThen it takes any `institutional label` and detects the following fields from it:\n\n- 'genus',\n- 'species',\n- 'year',\n- 'month',\n- 'day',\n- 'family',\n- 'collector',\n- 'authority',\n- 'locality',\n- 'geolocation',\n- 'collector_number',\n- 'infrasp taxon'\n\nThese text fields are then run through the OCR program Tesseract.\n\nInstallation\n==================================\n\nInstall hespi using pip:\n\n.. code-block:: bash\n\n    pip install hespi\n\nThe first time it runs, it will download the required model weights from the internet.\n\nIt is recommended that you also install `Tesseract <https://tesseract-ocr.github.io/tessdoc/Home.html>`_ so that this can be used in the text recognition part of the pipeline.\n\nUsage\n==================================\n\nTo run the pipeline, use the executable ``hespi`` and give it any number of images:\n\n.. code-block:: bash\n\n    hespi image1.jpg image2.jpg\n\nThis will prompt you to specify an output directory. You can set the output directory with the command with the ``--output-dir`` argument:\n\n.. code-block:: bash\n\n    hespi images/*.tif --output-dir ./hespi-output\n\nThe detected components and text fields will be cropped and stored in the output directory. There will also be a CSV file with the text recognition results for any institutional labels found.\n\n.. end-quickstart\n\nCredits\n==================================\n\n.. start-credits\n\nRobert Turnbull, Karen Thompson, Emily Fitzgerald, Jo Birch.\n\nPublication and citation details to follow.\n\nThis pipeline depends on `YOLOv5 <https://github.com/ultralytics/yolov5>`_, \n`torchapp <https://github.com/rbturnbull/torchapp>`_,\nMicrosoft's `TrOCR <https://www.microsoft.com/en-us/research/publication/trocr-transformer-based-optical-character-recognition-with-pre-trained-models/>`_.\n\nLogo derived from artwork by `ka reemov <https://thenounproject.com/icon/plant-1386076/>`_.\n\n.. end-credits\n",
    'author': 'Robert Turnbull',
    'author_email': 'robert.turnbull@unimelb.edu.au',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://rbturnbull.github.io/hespi/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
