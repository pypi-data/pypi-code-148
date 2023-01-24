from setuptools import setup, find_packages

packages = \
['Genetic_Algorithm_VEDA']

package_data = \
{'': ['*']}

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'  
]

setup(
    name='Genetic_Algorithm_VEDA',
    version='0.0.3',
    description='Algoritmo Genético para estudo da evolução de circuitos lógicos combinacionais na presença de falhas.',
    long_description=open('README.txt').read(),
    url='',
    author='Humberto Távora',
    author_email='humbertocct@hotmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='Genetic Algorithm',
    packages=find_packages(),
    install_requires = ['']
)