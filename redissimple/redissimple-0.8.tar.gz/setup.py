import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='redissimple',
    version='0.8',
    author='Vikash Jain',
    author_email='vikash.jain@galaxyweblinks.co.in',
    description='A library to use Redis Package',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/vcjain/redis-simple',
    project_urls = {
        "Bug Tracker": "https://github.com/vcjain/redis-simple/issues"
    },
    license='MIT',
    packages=['redissimple'],
    install_requires=['redis'],
)
