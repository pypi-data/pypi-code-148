import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='musibatln',
    version='0.2.1',
    author='Shahzain Khan',
    author_email='asifjamali83@hotmail.com',
    description='Team Musibat Bots',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://bitbucket.org/shahzain83/musibat',
    project_urls = {
        "Bug Tracker": "https://bitbucket.org/shahzain83/musibat/issues"
    },
    license='MIT',
    packages=['musibatln'],
    install_requires=['requests'],
)