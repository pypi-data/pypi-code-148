# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['manim_mobject_svg']

package_data = \
{'': ['*']}

install_requires = \
['manim>=0.16.0', 'pycairo>=1,<2']

entry_points = \
{'manim.plugins': ['manim_plugintemplate = manim_plugintemplate']}

setup_kwargs = {
    'name': 'manim-mobject-svg',
    'version': '0.1.0',
    'description': 'Create SVG files from VMobject and VGroup',
    'long_description': '# manim-mobject-svg\n\nCreate SVG files from [VMobject](https://docs.manim.community/en/stable/reference/manim.mobject.types.vectorized_mobject.VMobject.html).\n\nInstall: `pip install manim-mobject-svg`\n\nHere\'s an example of how to use this plugin:\n\n```python\nfrom manim import *\nfrom manim_mobject_svg import *\n\na = Square(color=BLUE)\na.to_svg("square.svg")\n```\nThis should create a file `square.svg` in the current directory and return the path to the file. The output should look like this:\n![svg square manim](https://user-images.githubusercontent.com/49693820/214828793-bf764d46-93b2-4622-bd1e-c68c42206b46.svg)\n\nIt\'s also possible to create a SVG file for VGroup.\n\n```python\nfrom manim import *\nfrom manim_mobject_svg import *\n\na = Square(color=BLUE)\nb = Circle(color=RED)\nc = VGroup(a, b)\nc.to_svg("group.svg")\n```\nIt\'ll create a SVG file like this:\n![svg vgroup manim](https://user-images.githubusercontent.com/49693820/214829098-6680ca28-6f2b-4bb6-b376-f7858532c1c3.svg)\n',
    'author': 'Naveen M K',
    'author_email': 'naveen521kk@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/naveen521kk/manim-mobject-svg',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<=3.11',
}


setup(**setup_kwargs)
