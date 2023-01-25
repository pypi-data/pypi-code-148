#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Eric.
# Distributed under the terms of the Modified BSD License.

import pytest

from ..widgets.example_widget import ExampleWidget


def test_example_creation_blank():
    w = ExampleWidget()
    assert w.value == 'Hello World'
