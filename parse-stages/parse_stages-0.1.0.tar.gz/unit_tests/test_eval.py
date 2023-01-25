# Copyright (c) Peter Pentchev <roam@ringlet.net>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
"""Test the evaluation of some simple expressions."""

from __future__ import annotations

import dataclasses

from typing import NamedTuple

import pytest

import parse_stages as pst


@dataclasses.dataclass(frozen=True)
class Environment(pst.TaggedFrozen):
    """Specify an environment to be matched by a spec (or not)."""


class Case(NamedTuple):
    """Specify a single test case: a string to parse, results."""

    spec: str
    matched: list[str]


_ALL = [
    Environment(name="t-black", tags=["check"]),
    Environment(name="t-black-reformat", tags=["do", "reformat"]),
    Environment(name="t-pep8", tags=["check"]),
    Environment(name="t-mypy", tags=["check"]),
    Environment(name="t-pylint", tags=["check"]),
    Environment(name="t-unit-tests", tags=["tests"]),
    Environment(name="t-runner-pep8", tags=["check", "runner"]),
]

_TESTS = [
    Case(spec="@check", matched=["t-black", "t-pep8", "t-mypy", "t-pylint", "t-runner-pep8"]),
    Case(spec="@tests", matched=["t-unit-tests"]),
    Case(spec="@check and not pep8", matched=["t-black", "t-mypy", "t-pylint"]),
    Case(spec="not pep8 and @check", matched=["t-black", "t-mypy", "t-pylint"]),
    Case(spec="@check and pep8 or @tests", matched=["t-pep8", "t-unit-tests", "t-runner-pep8"]),
    Case(spec="black", matched=["t-black", "t-black-reformat"]),
    Case(spec="black and not black-reformat", matched=["t-black"]),
    Case(spec="black and not black-reformat", matched=["t-black"]),
]


@pytest.mark.parametrize("case", _TESTS)
def test_basic(case: Case) -> None:
    """Make sure evaluation works more or less correctly."""
    expr = pst.parse_spec(case.spec)
    assert [env.name for env in _ALL if expr.evaluate(env)] == case.matched
