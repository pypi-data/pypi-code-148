from . import *
from .file import *
from .network import *
from .info import *
from .randoms import *
from .processbar import *
from .media import *
from .cmd import *
from .convert import *
from .utils import *
from .minecraft import *
from .plusmata import *

from pygments import console
import requests


ip = 'https://cdn.damp11113dev.tk'
__version__ = '2023.1.28.10.0.0' # 2022/12/7 | 10 file (no __init__.py) | --- function |


def vercheck():
    try:
        response = requests.get(f"{ip}/file/text/damp11113libver.txt")
        if response.status_code == 404:
            return False
        elif response.status_code == 200:
            if response.text == __version__:
                return True
            else:
                return False
        else:
            return False
    except:
        return False

print(console.colorize("yellow", "library check update..."))
try:
    response = requests.get(f"{ip}/file/text/damp11113libver.txt")
    if response.status_code == 404:
        print(f'{console.colorize("red", "check update failed. please try again (error 404)")}')
        print(f'{console.colorize("yellow", f"library version current: {__version__}")}')
    elif response.status_code == 200:
        if response.text == __version__:
            print(f'{console.colorize("green", "no update available")}')
            print(f'{console.colorize("green", f"library version current: {__version__}")}')
        else:
            print(console.colorize("yellow", "update available"))
            print(f'{console.colorize("green", f"library version current: {__version__}")}')
            print(f'{console.colorize("green", f"new: {response.text}")}')
    else:
        print(f'{console.colorize("red", f"check update failed. please try again (error {response.status_code})")}')
        print(f'{console.colorize("yellow", f"library version current: {__version__}")}')

except:
    print(console.colorize("red", "check update failed. please try again"), f'{__version__}')
    print(f'{console.colorize("yellow", f"library version current: {__version__}")}')