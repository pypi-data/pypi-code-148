import setuptools

__version__ = "0.1.1"
__description__ = 'The package targets protocol for uploading and reusing task and libraries'
__author__ = 'Jennie Automation Protocol <saurabh@ask-jennie.com>'

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='ask-jennie',
     version=__version__,
     author="ASK Jennie",
     py_modules=["jennie"],
     install_requires=['requests', 'bs4', 'xlrd'],
     entry_points={
        'console_scripts': [
            'jennie=jennie:execute'
        ],
     },
     author_email=__author__,
     description= __description__,
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/Ask-Jennie/jennie",
     packages=setuptools.find_packages(),
     classifiers=[
         "License :: OSI Approved :: MIT License",
         "Programming Language :: Python :: 3",
         "Programming Language :: Python :: 3.7",
     ],
 )