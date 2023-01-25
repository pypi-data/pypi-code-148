from setuptools import setup

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(name='kopeechka',
      version='5.2',
      description='This code is a representation of the kopeechka.store API in Python',
      long_description = long_description,
      long_description_content_type='text/markdown',
      packages=['kopeechka', 'kopeechka.async_methods', "kopeechka.methods", "kopeechka.errors", "kopeechka.types_kopeechka", "kopeechka.utils"],
      install_requires=["requests", "aiohttp"],
      author_email='rem.game.on@gmail.com'
      )