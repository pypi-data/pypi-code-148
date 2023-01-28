from setuptools import setup

setup(
    name='jtokengen',
    version='0.0.2',
    description='Easier command token generator.',
    url='https://github.com/jumichica/tokengen',
    author='Edwin Ariza',
    author_email='me@edwinariza.com',
    license='MIT',
    scripts=['bin/jtokengen'],
    packages=['jtokengen'],
    install_requires=[],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)