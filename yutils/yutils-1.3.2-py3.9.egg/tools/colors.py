#!%PYTHON_HOME%\python.exe
# coding: utf-8
# version: python38


NORMAL = '\033[0m'
#UNDERLINE = '\033[4m'


class ColorsConsts:
    GRAY = '\033[90m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PINK = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'


class HighlighterConsts:
    RED = '\033[41m'
    GREEN = '\033[42m'
    YELLOW = '\033[43m'
    BLUE = '\033[44m'
    PINK = '\033[45m'
    CYAN = '\033[46m'
    WHITE = '\033[47m'


COLOR_TRANSLATION = {
    'white': 'WHITE',
    'w': 'WHITE',
    'bold': 'WHITE',
    'gray': 'GRAY',
    'gr': 'GRAY',
    'red': 'RED',
    'r': 'RED',
    'green': 'GREEN',
    'g': 'GREEN',
    'yellow': 'YELLOW',
    'y': 'YELLOW',
    'blue': 'BLUE',
    'b': 'BLUE',
    'pink': 'PINK',
    'p': 'PINK',
    'cyan': 'CYAN',
    'c': 'CYAN',
}


def print_color(text, color, highlight=False, **kwargs):
    attr = COLOR_TRANSLATION[color.lower()]
    prefix = getattr(HighlighterConsts, attr) if highlight else getattr(ColorsConsts, attr)
    print(prefix + text + NORMAL, **kwargs)
