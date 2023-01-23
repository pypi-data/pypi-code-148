from setuptools import setup
from os import path
from codecs import open
import io
import re


#https://www.karakaram.com/how-to-create-python-cli-package/
#https://qiita.com/shinichi-takii/items/6d1063e0aa3f79e599f0

package_name = "pdivas"
root_dir = path.abspath(path.dirname(__file__))

def _requirements():
    return [name.rstrip() for name in open(path.join(root_dir, 'requirements.txt')).readlines()]

with open(path.join(root_dir, package_name, '__init__.py')) as f:
    init_text = f.read()
    author = re.search(r'__author__\s*=\s*[\'\"](.+?)[\'\"]', init_text).group(1)
    author_email = re.search(r'__author_email__\s*=\s*[\'\"](.+?)[\'\"]', init_text).group(1)
    url = re.search(r'__url__\s*=\s*[\'\"](.+?)[\'\"]', init_text).group(1)

assert license
assert author
assert author_email
assert url

setup(name='pdivas',
      description='PDIVAS: Pathogenicity predictor of Deep-Intronic Variants causing Aberrant Splicing',
      long_description=io.open('README.md', encoding='utf-8').read(),
      long_description_content_type='text/markdown',
      version='0.5.5',
      author=author,
      author_email=author_email,
      license='',
      url=url,
      packages=['pdivas'],
      install_requires=_requirements(),
      package_data={'pdivas': ['model/PDIVAS.sav']},
      entry_points={'console_scripts': ['pdivas=pdivas.__main__:main']},
      test_suite='tests')



