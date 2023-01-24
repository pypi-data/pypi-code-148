# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mdSlides', 'mdSlides.scripts']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'packaging>=23.0,<24.0', 'requests>=2.28.2,<3.0.0']

entry_points = \
{'console_scripts': ['mdSlides = mdSlides.scripts.mdSlides:main']}

setup_kwargs = {
    'name': 'mdslides',
    'version': '0.0.5',
    'description': 'A tool for generating slides from markdown files using different backends.',
    'long_description': '# Description\n\n`mdSlides` is a small utility for creating slideshows from markdown files. It is a wrapper around other tools\nthat actually generate the slides (currently only Pandoc) and handles setting up and passing the correct\ncommand options to each tool.\n\nGiven a small Pandoc markdown file named simple.md,\n```markdown\n---\ntitle  : Example Presentation\n---\n\n# First Slide\n\nText\n\n# Second Slide\n\n$\\nabla \\cdot \\vec{E} = \\frac{\\rho}{\\epsilon_0}$\n```\nand running `mdSlides` on it\n```bash\n$ mdSlides simple.md\n```\nwill produce a directory named `simple` that contains a file named `index.html`. You can open the file\nin a web browser to start the slide show.\n\n`mdSlides` will also copy files that are needed for the slideshow, for example css files, images, etc, and\nconfigure the slideshow to use the local files so that you can copy the directory to another computer (like\na web server) and it will still work.\n\nMultiple "engines" are supported. The default engine uses [Pandoc](https://pandoc.org/) to output\na [slidy](https://github.com/slideshow-templates/slideshow-slidy) presentation. To see a list of\nsupported engines, run\n```\n$ mdSlides --list-engines\n```\nOnly a few engines are currently supported, but others will be added in the future.\n\n## Installing\n\nYou can install mdSlides with `pip`\n\n```\npip install mdSlides\n```\n\n',
    'author': 'CD Clark III',
    'author_email': 'clifton.clark@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
