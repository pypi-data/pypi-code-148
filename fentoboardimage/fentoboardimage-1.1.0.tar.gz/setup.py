# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fentoboardimage']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.0.0,<10.0.0']

setup_kwargs = {
    'name': 'fentoboardimage',
    'version': '1.1.0',
    'description': 'FenToBoardImage takes a Fen string representing a Chess position, and renders a Pillow image of the resulting position.',
    'long_description': '<div align="center">\n  <img src="https://raw.githubusercontent.com/reedkrawiec/fenToBoardImage/main/documentation/logo.png" />\n</div>\n\n# About\n\nfentoboardimage takes a Fen string representing a Chess position, and renders a PIL image of the resulting position.\n\n###  You can customize:\n- the size and color of the board\n- piece sprites\n- black or white perspective\n- Board highlighting for last move\n- Arrows\n\n# Installation\n\nInstall the package using pip\n```\n$ pip install fentoboardimage\n```\n\nThen import the fenToImage and loadPiecesFolder functions and use them as follows:\n```\nfrom fentoboardimage import fenToImage, loadPiecesFolder\n\nboardImage = fenToImage(\n\tfen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",\n\tsquarelength=100,\n\tpieceSet=loadPiecesFolder("./pieces"),\n\tdarkColor="#D18B47",\n\tlightColor="#FFCE9E"\n)\n```\n\nIn order to load a piece set, the pieces must follow this file structure, and must be a .png:\n```\n-piece_set_name\n  -white\n    - Knight.png\n    - Rook.png\n    - Pawn.png\n    - Bishop.png\n    - Queen.png\n    - King.png\n  -black\n    - Knight.png\n    - Rook.png\n    - Pawn.png\n    - Bishop.png\n    - Queen.png\n    - King.png\n```\n\n# Usage\n\nThe fenToBoardImage has these parameters:\n\nfen: str\n\n\tFen string representing a position\n\nsquarelength: int\n\n\tthe length of one square on the board\n\n\tresulting board will be 8 * squarelength long\n\npieceSet: `loadPiecesFolder`\n\n\tthe piece set, loaded using the `loadPiecesFolder` function\n\ndarkColor: str\n\n\tdark square color on the board\n\nlightColor: str\n\n\tlight square color on the board\n\nflipped: boolean\n\n\tdefault = False\n\n\tWhether to flip to board, and render it from black\'s perspective\n\nArrowSet: `loadArrowsFolder`\n\n\tthe piece set, loaded using the `loadArrowsFolder` function\n\nThe loadPiecesFolder has one parameter:\n\nArrows: list[(str,str)]\n\n  A list of tuples containing coordinates to place arrows. In the\n  format of (start, end) using standard chess notation for the squares.\n\nlastMove: dict\n  A dictionary containing the fields `before`, `after`, `darkColor` and `lightColor`. `before` and `after`  using standard chess notation for the squares, and `darkColor` and `lightColor` should be hex strings.\n\npath: str\n\n\tLoads piece set located at the path provided.\n\nThe loadArrowsFolder has one parameter:\n\npath: str\n\n\tLoads arrow set located at the path provided.\n\n\n# Dependencies\n- [Pillow](https://pypi.org/project/Pillow/)\n',
    'author': 'Reed Krawiec',
    'author_email': 'reedkrawiec@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
