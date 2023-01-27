INTRA_CELL_SEPARATOR = ' '
INTER_CELL_SEPARATOR = '\t'

ESCAPED_DASH = '__ESCAPED_DASH__'


def encode(string: str):
    return string.replace('-', '\\-').replace(' ', '-')


def decode(string: str):
    return string.replace('\\-', ESCAPED_DASH).replace('-', ' ').replace(ESCAPED_DASH, '-')
