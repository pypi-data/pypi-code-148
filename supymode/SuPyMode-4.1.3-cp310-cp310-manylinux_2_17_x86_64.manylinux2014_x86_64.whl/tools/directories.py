#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from pathlib import Path

import SuPyMode

RootPath = Path(SuPyMode.__path__[0])

ZeroPath = Path(os.path.dirname(RootPath))

ReportPath = os.path.join(RootPath.parents[0], 'Reports')

example_directory = os.path.join(RootPath, 'examples')

validation_data_path = os.path.join(RootPath, 'validation_data')

temporary_image_path = os.path.join(RootPath.parents[0], 'temporary_data')

# -
