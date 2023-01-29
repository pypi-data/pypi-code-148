from cubelib.enums import state, bound
from cubelib.types import NextState
from cubelib.p import readPacketsStream, rrPacketsStream
from . import proto

version = '1.0.4-pre1'

supported_versions = [
    47,
    340
]
