import os
from pathlib import Path
from setuptools import setup, find_packages


setup(
    name='webex-integration',
    version=os.getenv('CI_COMMIT_TAG'),
    author='Deutsche Telekom IT GmbH',
    description='integrate Webex to your python project',
    long_description_content_type='text/markdown',
    long_description=Path('README.md', encoding='utf-8').read_text(),
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests'
    ],
    license="Apache Software License (Apache 2.0)",
    keywords=[
        'python', 'webex', 'logging', 'chat', 'cisco'
    ],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        'Development Status :: 4 - Beta',
    ]
)