#  Copyright 2022  Dominik Sekotill <dom.sekotill@kodo.org.uk>
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
A Coverage.py plugin module for adding test names as contexts

Coverage reports from *Coverage.py* can include line "contexts"; strings that are attached
to lines of code that provide some sort of contextual information to a reader.

This package consists of a dynamic context plugin for *Coverage.py* that adds unit test
names as contexts.
"""

from __future__ import annotations

from types import FrameType
from typing import Any
from unittest import TestCase

from coverage.plugin import CoveragePlugin
from coverage.plugin_support import Plugins

__version__ = "0.1"


class DynamicContextPlugin(CoveragePlugin):
	"""
	A dynamic context plugin for coverage.py for adding test name contexts

	https://coverage.readthedocs.io/en/latest/contexts.html#dynamic-contexts

	This plugin annotates code lines with the names of tests under which the line was
	reached.
	"""

	def dynamic_context(self, frame: FrameType) -> str|None:  # noqa: D102
		name = frame.f_code.co_name
		if name.startswith("test"):
			return self.test_context(frame, "run")
		if name == "setUp":
			return self.test_context(frame, "setup")
		if name == "tearDown":
			return self.test_context(frame, "teardown")
		if name == "setUpClass":
			return self.testcase_context(frame, "testcase-setup")
		if name == "tearDownClass":
			return self.testcase_context(frame, "testcase-teardown")
		return None

	def test_context(self, frame: FrameType, stage: str) -> str|None:
		"""
		Return a context string for test-case test setup and teardown methods, or None
		"""
		try:
			inst = frame.f_locals["self"]
		except KeyError:
			return None
		if isinstance(inst, TestCase) and inst._testMethodName != "runTest":
			cls = type(inst)
			return f"{stage} :: {inst._testMethodName} ({cls.__module__}.{cls.__name__})"
		return None

	def testcase_context(self, frame: FrameType, stage: str) -> str|None:
		"""
		Return a context string for test-case setup and teardown methods, or None
		"""
		try:
			cls = frame.f_locals["cls"]
		except KeyError:
			return None
		if issubclass(cls, TestCase):
			return f"{stage} :: {cls.__name__} ({cls.__module__})"
		return None


def coverage_init(reg: Plugins, options: dict[str, Any]) -> None:
	"""
	Initialise this plugin module
	"""
	reg.add_dynamic_context(DynamicContextPlugin())
