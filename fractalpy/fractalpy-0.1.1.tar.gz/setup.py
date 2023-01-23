# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['fractalpy', 'fractalpy.cli', 'fractalpy.cli.commands', 'fractalpy.fractals']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'imageio>=2.22.4,<3.0.0',
 'matplotlib>=3.6.2,<4.0.0',
 'mpire>=2.6.0,<3.0.0',
 'numba>=0.56.4,<0.57.0',
 'numpy>=1.23.5,<2.0.0',
 'pytest-cov>=4.0.0,<5.0.0',
 'pytest>=7.2.0,<8.0.0',
 'sphinx-rtd-theme>=1.1.1,<2.0.0',
 'sphinx>=5.3.0,<6.0.0',
 'sphinxcontrib-napoleon>=0.7,<0.8']

entry_points = \
{'console_scripts': ['fractalpy = fractalpy.cli.cli_main:main']}

setup_kwargs = {
    'name': 'fractalpy',
    'version': '0.1.1',
    'description': 'A high performance framework for fractal image and video generation',
    'long_description': '# FractalPy\n[![pypi](https://img.shields.io/pypi/v/FractalPy)](https://pypi.org/project/fractalpy/)\n[![tag](https://img.shields.io/github/v/tag/Fergus-OH/FractalPy)]()\n[![python_version](https://img.shields.io/pypi/pyversions/FractalPy)]()\n[![licence](https://img.shields.io/github/license/Fergus-OH/FractalPy)](https://github.com/Fergus-OH/FractalPy/blob/main/LICENCE.md)\n[![code quality](https://img.shields.io/scrutinizer/quality/g/Fergus-OH/FractalPy/main)](https://scrutinizer-ci.com/g/Fergus-OH/FractalPy/)\n[![build](https://img.shields.io/github/actions/workflow/status/Fergus-OH/FractalPy/python-app.yml?branch=main)](https://github.com/Fergus-OH/FractalPy/actions/workflows/python-app.yml)\n[![checks](https://img.shields.io/github/checks-status/Fergus-OH/FractalPy/main)]()\n[![codecov](https://codecov.io/gh/Fergus-OH/FractalPy/branch/main/graph/badge.svg?token=XWYUNL7XIE)](https://codecov.io/gh/Fergus-OH/FractalPy)\n[![docs](https://img.shields.io/readthedocs/fractalpy)](https://fractalpy.readthedocs.io/en/latest/)\n\n<p align="center">\n  <img src= "https://raw.githubusercontent.com/Fergus-OH/mandelbrot-julia-sets/numba/assets/Mandelbrot_4320pts_1000threshold.png" width="800">\n</p>\n\nConsider the recurrence relation $z_{n+1} = z_n^2 + c$ where $c$ is a complex number.\nThe Mandelbrot set is a fractal, defined by the set of complex numbers $c$ for which this recurrence relation, with initial value $z_0 = 0$, does not diverge.\nAnother interesting type of set, which are related to the Mandelbrot set, are Julia sets and are defined for a specific complex number $c$.\nTo keep things brief, we will just establish the definition of a filled-in Julia set and do so in the following way:\nThe filled-in Julia set of a complex number $c$ is the set of initial values $z_0$ for which the previously mentioned recurrence relation does not diverge.\nNot every filled-in Julia set is a fractal, but for almost all complex numbers $c$, they are.\nThis project contains an implementation to generate images and videos relating to the Mandelbrot set and Julia sets.\n\n[//]: # (<img src="https://raw.githubusercontent.com/Fergus-OH/FractalPy/numba/assets/zoom_&#40;-1,186592,-0,1901211&#41;)\n\n[//]: # (_1000thresh_360pts_60frames_15fps.gif" width="400">)\n\n<p align="center">\n  <img src="https://raw.githubusercontent.com/Fergus-OH/FractalPy/numba/assets/zoom_(-1,186592,-0,1901211)_1000thresh_360pts_60frames_15fps-min.gif" width="400">\n  <img src="https://raw.githubusercontent.com/Fergus-OH/FractalPy/numba/assets/spin_(-0,79+0,15j)_1000thresh_360pts_110frames_30fps.gif" width="400">\n</p>\n\n\n\n\n[//]: # (<img src="https://raw.githubusercontent.com/Fergus-OH/mandelbrot-julia-sets/numba/assets/zoom_&#40;10004407000,-0,7436439059192348,-0,131825896951&#41;_5000thresh_480pts_300frames_30fps.gif" width="500">)\n[//]: # (<img src="https://raw.githubusercontent.com/Fergus-OH/mandelbrot-julia-sets/numba/assets/julia_spin2.gif" width="500">)\n  \n\n\n## Installation\nBefore installing the `FractalPy` package, it is recommended to create and activate a virtual environment with `python 3.10`.\nThis can be done with conda by running the following commands in a terminal\n```\n$ conda create --name fractal python==3.10\n```\n\n```\n$ conda activate fractal\n```\nNow the package and it\'s dependencies can be installed in the virtual environment, `fractal`, using pip.\n\nTo install the stable release, run\n```\n$ pip install fractalpy\n```\n\nTo install the latest version, run\n```\n$ pip install git+https://github.com/Fergus-OH/FractalPy.git\n```\n\nTo install an editable installation, clone the repository, checkout the develop branch, and install the contents with pip.\nThis can be done with the following commands\n```\n$ git clone --branch develop https://github.com/Fergus-OH/FractalPy.git\n$ cd FractalPy\n$ pip install -e .\n```\n<!-- After which, a shell for the environment with the editable installation of `fractalpy` can be spawned\n```\n$ poetry shell\n``` -->\n\n## Usage\nTo get started with `FractalPy`, type the following in a terminal to show documentation for the command line \ninterface application\n\n```\n$ fractalpy --help\n```\n\n\nFractalPy can be also be used directly in a notebook or python script by importing the fractalpy package\n\nThere are two ways of using `FractalPy`.\nThe package can be imported to a python script with\n\n```python\nimport fractalpy as frac\n\n# Plot the Mandelbrot set\nfrac.Mandelbrot().plot()\n\n# Plot the Julia set\nfrac.Julia().plot()\n```\n\nThe package also offers a command line interface that can be immediately accessed in the terminal with\n```\nfractalpy --help\n```\n\nFor example, we can create a gif of zooming into the mandelbrot set with the following command:\n```\nfractalpy mandelbrot zoom\n```\n\nIf FFmpeg is installed and accessible via the $PATH environment variable, then `FractalPy` can also generate videos, for example\n```\nfractalpy mandelbrot zoom --extension mp4\n```\n\n`FractalPy` makes use of multiprocessing to generate multiple frames simultaneously and also performs the computationally expensive calculations in parallel with `jit`, making it an extremely fast.\n<!-- ```\nFractal().\n```\n\n\nA notebook with demos can be found [here](https://nbviewer.org/github/Fergus-OH/mandelbrot-julia-sets/blob/numba/demos.ipynb)\n\n<a href="https://nbviewer.org/github/Fergus-OH/mandelbrot-julia-sets/blob/numba/demos.ipynb"><img src="https://raw.githubusercontent.com/jupyter/design/master/logos/Badges/nbviewer_badge.svg" alt="Render nbviewer" /></a> -->\n\n## Documentation\nDocumentation is available on [readthedocs.io](https://fractalpy.readthedocs.io/en/latest/), with a pdf format available\n[here](https://fractalpy.readthedocs.io/_/downloads/en/latest/pdf/).\n',
    'author': "Fergus O'Hanlon",
    'author_email': 'fergusohanlon@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Fergus-OH/FractalPy',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
