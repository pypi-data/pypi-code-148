#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup_args = dict(
    name='space_wrap',
    version='0.0.1',
    description='Automated Spacy wrapper to turn plain text into Spacy doc objects',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY,
    license='MIT',
    packages=find_packages(),
    py_modules=['space_wrap'],
    author='Evan Anthony',
    author_email='anthonyevanm@gmail.com',
    keywords=['Spacy', 'tokenizer', 'NLP'],
    url='https://github.com/eanthony1224',
    download_url='https://pypi.org/project/space_wrap/'
)

install_requires = [
   'pandas',
    'spacy'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)

