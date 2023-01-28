from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.6'
DESCRIPTION = 'Intelligent Accountant Reinforcement Learning Toolkit.智能会计强化学习框架。'

# Setting up
setup(
    name="cpagym",
    version=VERSION,
    author="Draco Deng",
    author_email="dracodeng6@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://cpanlp.com",
    packages=find_packages(),
    install_requires=[],
    keywords=['python',' reinforcement learning','gym','openai' 'accounting', 'cpa', 'audit','intelligent accounting', 'linguistic turn', 'linguistic',"intelligent audit","natural language processing","machine learning","finance","certified public accountant",'big four',"会计","注会","注册会计师","审计","智能会计","会计的语言学转向","语言学","智能审计","自然语言处理","机器学习","金融","北外","财会","四大","注册会计","强化学习"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)