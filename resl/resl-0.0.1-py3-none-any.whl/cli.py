"""
resl.cli
--------

This is the module that implements resl's minimalist
command prompt.
"""
from . import colorful as cor
from .colorful import cprint, cinput


def main():
    cprint("\u2620", cor.OKGREEN)

    while True:
        cmd = cinput(">>", cor.OKCYAN)
        print(cmd)
