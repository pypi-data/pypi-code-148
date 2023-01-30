__version__ = '1.0.8'

import os
import sys

def enter_path():
    """
    Enter current python file .py path
    """
    path = sys.argv[0]
    path2 = os.path.split(path)[0]
    if path2 != '':
        os.chdir(path2)
    print("Current Path is {}".format(os.getcwd()))
    return os.getcwd()

def main():
    pass

if __name__ == '__main__':
    main()