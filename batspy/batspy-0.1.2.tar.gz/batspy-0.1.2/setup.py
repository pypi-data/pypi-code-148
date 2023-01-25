from setuptools import setup, find_packages

setup(
    name='batspy',
    version='0.1.2',
    description='Testing framework for bash scripts',
    author='Tom Shabtay',
    author_email='tomshabtay@gmail.com',
    url='https://github.com/tomshabtay/batspy',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
    ],
)
