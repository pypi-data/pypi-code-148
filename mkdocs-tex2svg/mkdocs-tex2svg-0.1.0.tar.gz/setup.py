#  License: GNU GPLv3+, Rodrigo Schwencke (Copyleft)

import os
import sys
from setuptools import setup

username = os.getenv('TWINE_USERNAME')
password = os.getenv('TWINE_PASSWORD')

VERSION = '0.1.0'
GIT_MESSAGE_FOR_THIS_VERSION ="""Write Documentation
"""

if sys.argv[-1] == 'publish':
    if os.system("pip freeze | grep build"):
        print("'build' is not installed.\nUse `pip install build`.\nExiting.")
        sys.exit()
    if os.system("pip freeze | grep twine"):
        print("'twine' is not installed.\nUse `pip install twine`.\nExiting.")
        sys.exit()
    os.system("python -m build")
    if ((username is not None) and (password is not None)):
        os.system(f"python -m twine upload dist/* -u {username} -p {password}")
    else:
        os.system(f"python -m twine upload dist/*")
    print(f"You probably also want to git push project, create v{VERSION} tag, and push it too :\n")
    gitExport=input("Do you want to do it right now? [y(default) / n]")
    if gitExport=="y" or gitExport=="":
        os.system(f"git add . && git commit -m 'v{VERSION} : {GIT_MESSAGE_FOR_THIS_VERSION}' && git push")
        os.system(f"git tag -a {VERSION} -m 'v{VERSION}'")
        os.system(f"git push --tags")
    else:
        print("You may still consider adding the following new tag later on :")
        print(f"git tag -a {VERSION} -m 'v{VERSION}'")
        print(f"git push --tags")
    sys.exit()

setup(
    name="mkdocs-tex2svg",
    version=VERSION,
    packages=["mkdocs_tex2svg"],
    install_requires=['Markdown>=2.3.1'],
    author="Rodrigo Schwencke",
    author_email="rod2ik.dev@gmail.com",
    description="Converts (inline and/or block) LaTeX snippets in Mkdocs, as base64 SVGs, natively & dynamically compatible with Mkdocs Light & Dark Themes, directly from your Markdown",
    long_description_content_type="text/markdown",
    long_description="""Project Page : [rod2ik/mkdocs-tex2svg](https://gitlab.com/rod2ik/mkdocs-tex2svg)

This project is part of other mkdocs-related projects.  
If interested, please consider having a look at this page for a more complete Documentation (Installation, Configuration and Rendering Examples), as well as all other mkdocs-related projects:

* Installation and Configs : [https://eskool.gitlab.io/mkhack3rs/maths/tables/](https://eskool.gitlab.io/mkhack3rs/maths/tables/)
* Rendering Examples : [https://eskool.gitlab.io/mkhack3rs/maths/tables/examples/](https://eskool.gitlab.io/mkhack3rs/maths/tables/examples/)

This project is the exclusive work of :

* Rodrigo Schwencke at [rod2ik/mkdocs-tex2svg](https://gitlab.com/rod2ik/mkdocs-tex2svg)

Licence : [GPLv3+](https://opensource.org/licenses/GPL-3.0), Copyleft [Rodrigo Schwencke / rod2ik](https://gitlab.com/rod2ik)""",
    keywords='mkdocs python markdown tex latex mathematics variation table svg',
    license="GPLv3+",
    url="https://gitlab.com/rod2ik/mkdocs-tex2svg.git",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Education',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Topic :: Documentation',
        'Topic :: Text Processing',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows :: Windows 10',
    ],
)
