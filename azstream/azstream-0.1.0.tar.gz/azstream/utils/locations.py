import pathlib, sys


def get_appdir(app_name: str) -> pathlib.Path:
    '''
    Returns a directory where persisten data can be stored.

    - linux: ~/.local/share
    - macOS: ~/Library/Application Support
    - windows: C:/Users/<USER>/AppData/Roaming

    Source: https://tinyurl.com/3fbm99pk
    '''

    home = pathlib.Path.home()
    if sys.platform == 'win32':
        return home / f'AppData/Roaming/{app_name}'
    elif sys.platform == "linux":
        return home / ".local/share/{app_name}"
    elif sys.platform == "darwin":
        return home / "Library/Application Support/{app_name}"