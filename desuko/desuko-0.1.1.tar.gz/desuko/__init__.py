"""Desuko - An extensible Discord bot, written in Python & Pycord.

## How is it structured?
Desuko aims to be modular. It has a base package implemented here and modules
to extend its functionality.

To make changes into Desuko code, please, make sure that your edits will **not** break
any existing modules.
"""
from desuko import bot, loader

__all__ = (
    'bot',
    'loader',
    'modules',
)
