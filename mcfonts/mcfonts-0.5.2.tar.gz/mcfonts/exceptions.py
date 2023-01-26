#!/usr/bin/env python3
# coding=utf-8
# SPDX-License-Identifier: MIT
"""General exceptions."""


class GlyphLimitError(Exception):
    """
    Raised when a font has 65,535 characters allocated and that no more can be added.
    """


class RangestringError(Exception):
    """
    Raised when a rangestring is invalid.
    """


class ProviderError(Exception):
    """
    Raised when a :class:`mcfonts.providers.AnyProvider` is expected but not found.
    """
