# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jetdb']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'jetdb',
    'version': '0.3.1',
    'description': 'This module is designed for everyone to easily handle txt files. JSON file handling will be added soon.',
    'long_description': '<h1>Disclaimer</h1>\nThis package has strict syntax. If you do not like strict syntax, do not use.\nThis package makes file handling simpler. <br><br>Current Version: [Version 0.3.1]\n<br><br>\nMost functions are still in development, so please report bugs if there are any.\nReport bugs by sending an email to adityasrijeet12355@gmail.com\n<br><br>\n<h1>Example Code</h1>\n<br>\n\n```python\nfrom jetdb import functions\ndb = functions()\ndb.setup()\n```\n<h1>Functions Supplied</h1>\n\n• Setup - Updates, Restarts, Removes dependencies in the background\n<br>\n• Add - Adds a line\n<br>\n• Index - Finds the line number for you\n<br>\n• Index Replace - Indexes the line and replaces it\n<br>\n• New File - Creates a new file for you\n<br>\n• Clear - Clears a whole file for you\n<h1>How to use functions</h1>\n<br>\nExample code:<br><br>\n\n```python\nfrom jetdb import functions\ndb = functions()\ndb.setup()\nfilename = "--> INSERT FILENAME HERE <--"\ndb.clear(f"{filename}")\ndb.add(f"{filename}", "This module is cool!", msg=False)\ndb.add(f"{filename}", "This module is cool!", msg=True)\ndb.index_replace(f"{filename}", "This module is cool!", "This module is the best", msg=False)\ndb.index(f"{filename}", "This module is the best")\ndb.printRead(f"{filename}")\n```\n  \nYou get it, use the variable you used to control the functions, then you add the function name after it.\n<br><br>\nExample code:<br>\n```python\n  from jetdb import functions\n  db = functions()\n  db.setup()\n  db.printRead(f"{filename}")\n```\n\n<br>\nThat previous block of code will read a file and print it.\n<h1>Changelog</h1>\n<br>\n<h2>Version 0.3.1</h2>\n<br>\n-\\ Removed one dependency\n<br> -\\ Custom Error bug fix\n<br> -\\ Colorama dependency changed again\n<br> -\\ Colorama injection revamp\n<h2>Version 0.3.0</h2>\n<br>\n-\\ Changed the dependencies\n<br> -\\ Minor error bug fixes\n<br> -\\ Colorama dependency change\n<br> -\\ Colorama now gets installed in your project\n<h2>Version 0.2.99</h2>\n<br>\n-\\ Changed the dependencies\n<br> -\\ Minor error bug fixes\n<br> + Colorama\n<br> + Custom Errors\n<h2>Version 0.2.4</h2>\n<br>\n-\\ Changed the dependencies\n<br> -\\ Minor error bug fixes\n<br> + Added description\n<br> + Added Changelog\n<h2>Version 0.2.0</h2>\n<br>\n+ Added a dependency\n<br> + Added index feature\n<br> - Removed search line feature\n<br> -\\ Remastered new file feature\n<br> -\\ Remastered Index Replace feature\n<h2>Version 0.1.5</h2>\n<br>\n+ Added a dependency\n<br> + Added search line feature\n<br> -\\ Remastered new file feature\n<br> -\\ Remastered Index Replace feature\n<h2>Version 0.1.1</h2>\n<br>\n-\\ Minor bug fixes\n<br>\n-\\ Revamped speed\n<br> -\\ Patched up clear file function\n<h2>Version 0.1.0</h2>\n<br>\nHow everything started:\n<br>\n+ Wait function<br>\n+ Add line function<br>\n+ Replace line function beta',
    'author': 'Srijeet Aditya',
    'author_email': 'adityasrijeet12355@egmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
