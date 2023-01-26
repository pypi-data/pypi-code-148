# coding: utf-8
from pathlib import Path

from setuptools import find_packages, setup


setup(
    name='camunda-adapter',
    url='https://stash.bars-open.ru/projects/M3/repos/camunda-adapter',
    license='MIT',
    author='BARS Group',
    description='Адаптер для BPMN-движка Camunda',
    author_email='bars@bars-open.ru',
    package_dir={'': 'src'},
    packages=find_packages('src', exclude=('testapp', 'testapp.*',)),
    long_description=(Path(__file__).parent / 'README.md').open('r').read(),
    long_description_content_type='text/markdown',
    include_package_data=True,
    package_data = {
        '': ['LICENSE', 'README.md5', 'RELEASE']
    },
    classifiers=[
        'Intended Audience :: Developers',
        'Environment :: Web Environment',
        'Natural Language :: Russian',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Development Status :: 5 - Production/Stable',
    ],
    install_requires=(
        'pydantic',
        'requests'
    ),
    dependency_links=(
        'http://pypi.bars-open.ru/simple/m3-builder',
    ),
    setup_requires=(
        'm3-builder>=1.2,<2',
    ),
    python_requires='>=3.7',
    set_build_info=Path(__file__).parent.as_posix(),
)
