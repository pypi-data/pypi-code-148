from jmespaths import parser
from jmespaths.visitor import Options

__version__ = '1.0.1'


def compile(expression):
    return parser.Parser().parse(expression)


def search(expression, data, options=None):
    return parser.Parser().parse(expression).search(data, options=options)


def replace(expression, data, *args, options=None):
    return parser.Parser().parse(expression).replace(data, *args, options=options)
