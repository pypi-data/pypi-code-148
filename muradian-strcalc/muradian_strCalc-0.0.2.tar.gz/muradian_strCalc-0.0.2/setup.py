from setuptools import setup, find_packages
import codecs
import os


# with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
#     long_description = "\n" + fh.read()

VERSION = '0.0.2'
DESCRIPTION = 'It a convertor that you use ! likely'
LONG_DESCRIPTION = 'A package that convert a line to interger_calculator '
detailed = '''
    Mostly use as your personal development , it's help to you on string that you was collect
    by input / sources .. 
    example :
    1 2 pl 3 

    here,
    **1** is digit (how many digit you want to use)
    **2 and 3 ** is digit that will summation by 'pl' command

    more example :
    2 23 mi 21  

    pl = Pluse / Summation
    mi = Substraction
    mu = Multiplication
    di = Division 
'''

# Setting up
setup(
    name="muradian_strCalc",
    version=VERSION,
    author="Mozadded Alfeshani",
    author_email="mozaddedalfeshani@gmail.com",
    description="Nothing to say ! you can use that on any assistant",
    long_description_content_type="text/markdown",
    long_description=detailed,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'calcutor', 'assistant',
              'string calculator'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
