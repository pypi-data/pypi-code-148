#!/usr/bin/env python3
# coding=utf-8
# SPDX-License-Identifier: MIT
"""
Color codes and settings for mcfonts.

These are ANSI color codes.
Set :const:`USE_COLORS` to False to **disable** colored output.
Set :const:`USE_COLORS` to True to **enable** colored output.
"""

USE_COLORS: bool = True

_CSI = "\x1b["
BLACK_FORE = f"{_CSI}30m"
RED_FORE = f"{_CSI}31m"
GREEN_FORE = f"{_CSI}32m"
YELLOW_FORE = f"{_CSI}33m"
BLUE_FORE = f"{_CSI}34m"
MAGENTA_FORE = f"{_CSI}35m"
CYAN_FORE = f"{_CSI}36m"
WHITE_FORE = f"{_CSI}37m"
RESET_FORE = f"{_CSI}39m"

BLACK_BACK = f"{_CSI}40m"
RED_BACK = f"{_CSI}41m"
GREEN_BACK = f"{_CSI}42m"
YELLOW_BACK = f"{_CSI}43m"
BLUE_BACK = f"{_CSI}44m"
MAGENTA_BACK = f"{_CSI}45m"
CYAN_BACK = f"{_CSI}46m"
WHITE_BACK = f"{_CSI}47m"
RESET_BACK = f"{_CSI}49m"

RESET_ALL = f"{_CSI}0m"
BRIGHT = f"{_CSI}1m"
DIM = f"{_CSI}2m"
