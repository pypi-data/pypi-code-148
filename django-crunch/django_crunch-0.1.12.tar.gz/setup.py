# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['crunch',
 'crunch.client',
 'crunch.django',
 'crunch.django.app',
 'crunch.django.proj',
 'crunch.management.commands',
 'crunch.migrations',
 'crunch.templatetags']

package_data = \
{'': ['*'], 'crunch': ['templates/*', 'templates/crunch/*']}

install_requires = \
['Django>=3.2,<4.0',
 'anytree>=2.8.0,<3.0.0',
 'django-cms>=3.9.0,<4.0.0',
 'django-extensions>=3.1.5,<4.0.0',
 'django-mptt>=0.13.4,<0.14.0',
 'django-next-prev>=1.1.0,<2.0.0',
 'django-polymorphic-tree>=2.1,<3.0',
 'django-polymorphic>=2,<3.1',
 'django-storages[boto3]>=1.12.2,<2.0.0',
 'djangocms-admin-style>=2.0.2,<3.0.0',
 'djangocms-attributes-field>=2.0.0,<3.0.0',
 'djangocms-bootstrap4>=2.0.0,<3.0.0',
 'djangocms-bootstrap>=1.1.2,<2.0.0',
 'djangocms-file>=3.0.0,<4.0.0',
 'djangocms-googlemap>=2.0.0,<3.0.0',
 'djangocms-link>=3.0.0,<4.0.0',
 'djangocms-page-meta>=1.0.1,<2.0.0',
 'djangocms-picture>=3.0.0,<4.0.0',
 'djangocms-snippet>=3.0.0,<4.0.0',
 'djangocms-style>=3.0.0,<4.0.0',
 'djangocms-text-ckeditor>=4.0.0,<5.0.0',
 'djangocms-themata>=0.1.0,<0.2.0',
 'djangocms-video>=3.0.0,<4.0.0',
 'djangorestframework>=3.13.1,<4.0.0',
 'humanize>=4.0.0,<5.0.0',
 'ipykernel>=6.9.1,<7.0.0',
 'pandas>=1.4.4,<2.0.0',
 'pydeck>=0.7.1,<0.8.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'requests>=2.27.1,<3.0.0',
 'rich>=11.1.0,<12.0.0',
 'setuptools>=65.3.0,<66.0.0',
 'snakemake>=6.15.5,<7.0.0',
 'toml>=0.10.2,<0.11.0',
 'typer[all]>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['crunch = crunch.client.main:app',
                     'crunchsite = crunch.django.proj.manage:main']}

setup_kwargs = {
    'name': 'django-crunch',
    'version': '0.1.12',
    'description': 'A data processing orcestration tool.',
    'long_description': '================================================================\ndjango-crunch\n================================================================\n\n.. image:: https://raw.githubusercontent.com/rbturnbull/django-crunch/main/docs/images/crunch-banner.svg\n\n.. start-badges\n\n|testing badge| |coverage badge| |docs badge| |black badge|\n\n.. |testing badge| image:: https://github.com/rbturnbull/django-crunch/actions/workflows/testing.yml/badge.svg\n    :target: https://github.com/rbturnbull/django-crunch/actions\n\n.. |docs badge| image:: https://github.com/rbturnbull/django-crunch/actions/workflows/docs.yml/badge.svg\n    :target: https://rbturnbull.github.io/django-crunch\n    \n.. |black badge| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/psf/black\n    \n.. |coverage badge| image:: https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/rbturnbull/d83b00666fad82df59a814083a09d1c1/raw/coverage-badge.json\n    :target: https://rbturnbull.github.io/django-crunch/coverage/\n    \n.. end-badges\n\n\n.. start-quickstart\n\nA data processing orcestration tool.\nCrunch allows you to visualize the datasets, orchestrate and manage the processing online and present the results to the world.\n\nDescription\n===========\n\nCrunch coordinates three components. First there is a web application in the cloud. \nCrunch includes a Django app which can be included in a website built using the Django framework for building database driven websites. \nThe website allows users to create what we call ``datasets``. \nEach dataset corresponds to one collection of files and metadata which is designed to be run through the workflow. \nEach dataset has its own page on the website which displays all the information about it.\n\nThe second component is data storage. \nThe main use-case for crunch is when your datasets are so many and so large that you cannott fit them all on to the disk where you are doing your computation. \nWith crunch, the data can be stored in any of the media storage options available with Django. \nThese can be Amazon S3, Google Cloud or many other storage options. \n\nThe third component is the client which runs at the place where you are performing the computation. \nThis could be in a high-performance computing environment, or it could be on a virtual machine in the cloud or it could be just on your own laptop. \nThe user just runs the crunch command line tool. \nThe command line tool communicates with the website to find out which dataset should be processed next, \nthen it copies it from storage and saves it locally. \nThen it processes the dataset using a pre-defined workflow provided by the user. \nWhen it is finished, it copies back the data to the storage with the resulting files. \nAt each stage the user can see the status on the website interface. \nIf you run the `crunch loop`` command then the client continually loops through the datasets until they are completely finished. \nYou can run as many clients in parallel as you have computing resources.\n\nOnce each dataset is processed, the resulting files can be accessed via the website. \nThe permissions for the website can be set dynamically so that users can restrict access \nto just the team for while the data is being processed and once the results are ready for the world then you can allow access to the public.\n\n\nInstallation\n==================================\n\nThe crunch app for a Django website and the command-line client are installed with pip:\n\n.. code-block:: bash\n\n    pip install git+https://github.com/rbturnbull/django-crunch\n\n\nInstall the crunch app to the Djanco website project by adding it to the settings:\n\n.. code-block:: python\n\n    INSTALLED_APPS += [\n        "crunch",\n    ]\n\nThen add the urls to your main urls.py:\n\n.. code-block:: python\n\n    urlpatterns += [\n        path(\'crunch/\', include(\'crunch.django.app.urls\'))),    \n    ]\n\nThe path ``crunch/`` can be changed to be whatever you choose.\n\nUsage\n==================================\n\nCreate projects, datasets, items and attributes on the website using the HTML interface, the crunch command-line client or the Python API.\n\nUpload initial data for each dataset as needed to the storage using the Crunch HTML interface or direct to the folder for each dataset on the storage.\n\nThen process each dataset at the location where you are performing your compute with the crunch client. All datasets can be processed with the single command:\n\n.. code-block:: bash\n\n    crunch loop\n\n.. end-quickstart\n\nCredits\n==================================\n\n.. start-credits\n\nRobert Turnbull, Mar Quiroga and Simon Mutch from the Melbourne Data Analytics Platform.\n\nPublication and citation details to follow.\n\n.. end-credits\n',
    'author': 'Robert Turnbull, Mar Quiroga and Simon Mutch',
    'author_email': 'robert.turnbull@unimelb.edu.au',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/rbturnbull/django-crunch',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<=3.11',
}


setup(**setup_kwargs)
