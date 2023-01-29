from setuptools import setup, find_packages

setup(
    name='DomiKnowS',
    version= 0,
    description='A tutorial for creating pip packages.',

    url='https://github.com/HLR/DomiKnowS',
    author='Andrzej Uszok',
    author_email='auszok@ihmc.org',

    packages=find_packages(include=['regr.*']),

    classifiers=[
        'Intended Audience :: Developers',

        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)