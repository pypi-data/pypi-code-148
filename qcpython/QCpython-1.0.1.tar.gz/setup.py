from setuptools import setup, Extension
from distutils.core import setup
from pathlib import Path
dir = Path(__file__).parent
setup(
    name = 'QCpython',
    packages = ['QCpy'],
    version = '1.0.1',
    description = 'QCpy is a lightweight quantum circuit simulator and visualization of quantum computing.',
    long_description = (dir / "README.md").read_text(),
    long_description_content_type='text/markdown',
    author = 'Brennan Freeze, Paris Osuch, Aundre Barras, Soren Richenberg, Suzanne Rivoire',
    author_email = 'freezebrennan@gmail.com, osuch@sonoma.edu, barras@sonoma.edu, richenbe@sonoma.edu, rivoire@sonoma.edu',
    url = 'https://github.com/QCpython/QCpy',
    keywords = ['quantum computing', 'physics', 'visualization', 'quantum circuit'],
    classifiers = [],
)