"""Runs Python App. Supports sync and async."""
from ..app import main as main_app
import sys

def main(args=None):
    print(f'Starting package')

    # Runs main function on app/main.py
    main_app.main(args)

    print(f'Finished package')

if __name__ == '__main__':
    main(sys.argv[1:])