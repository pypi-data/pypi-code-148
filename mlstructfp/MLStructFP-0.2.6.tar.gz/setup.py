"""
MLSTRUCTFP - SETUP

Setup distribution.
"""

# Library imports
from setuptools import setup, find_packages
import MLStructFP

# Load readme
with open('README.rst') as f:
    long_description = f.read()

# Load requirements
requirements = [
    'matplotlib == 3.5.3',
    'numpy == 1.18.5',
    'opencv-python == 4.5.1.48',
    'Pillow == 9.4.0',
    'plotly == 5.11.0',
    'requests == 2.28.1',
    'six == 1.16.0'
]

requirements_tests = requirements.copy()
requirements_tests.extend([
    'codecov',
    'nose2'
])

# Setup library
setup(
    author=MLStructFP.__author__,
    author_email=MLStructFP.__email__,
    classifiers=[
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Image Recognition',
        'Topic :: Scientific/Engineering :: Visualization'
    ],
    description=MLStructFP.__description__,
    long_description=long_description,
    include_package_data=True,
    install_requires=requirements,
    extras_require={
        'test': requirements_tests
    },
    keywords=MLStructFP.__keywords__,
    name='MLStructFP',
    packages=find_packages(exclude=[
        '.idea',
        '.ipynb_checkpoints',
        'test'
    ]),
    platforms=['any'],
    project_urls={
        'Bug Tracker': MLStructFP.__url_bug_tracker__,
        'Documentation': MLStructFP.__url_documentation__,
        'Source Code': MLStructFP.__url_source_code__
    },
    python_requires='>=3.8',
    url=MLStructFP.__url__,
    version=MLStructFP.__version__
)
