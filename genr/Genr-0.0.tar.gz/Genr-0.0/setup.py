from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("/home/manomay/Desktop/PsyTech/genr.ai/requirements.txt", "r") as f:
    install_requires = f.read().splitlines()

setup(
    name='Genr',
    version='0.0',
    author='Psytech',
    author_email='manomay@psytech.ai',
    description='A library to cater all your NLP tasks using LLMs',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/psytech42/genr.ai',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=install_requires,
)