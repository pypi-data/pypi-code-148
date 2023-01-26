from setuptools import find_packages, setup

with open('README.md') as readme_file:
    README = readme_file.read()

setup_args = {
    "name": 'shopcloud_organize',
    "version": '1.0.0',
    "description": 'CLI tool for task management @talk-point',
    "long_description_content_type": "text/markdown",
    "long_description": README,
    "license": 'MIT',
    "packages": find_packages(),
    "author": 'Konstantin Stoldt',
    "author_email": 'konstantin.stoldt@talk-point.de',
    "keywords": ['CLI'],
    "url": 'https://github.com/Talk-Point/shopcloud-organize',
    "scripts": ['./scripts/organize'],
}

install_requires = [
    'pyyaml',
    'requests',
    'shopcloud-secrethub',
    'tqdm',
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
