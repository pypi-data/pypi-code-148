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
"""Test some basic parsing functionality."""

from __future__ import annotations

from typing import NamedTuple

import pytest

import parse_stages as pst


class Case(NamedTuple):
    """Specify a single test case: a string to parse, results."""

    spec: str
    res: pst.BoolExpr


class IdCase(NamedTuple):
    """Specify a single test case for stage IDs: a string to parse, results."""

    spec: str
    res: list[int]


_DEFS = [
    Case(spec="@check", res=pst.TagExpr(tag="check")),
    Case(spec="pep8", res=pst.KeywordExpr(keyword="pep8")),
    Case(spec="not @check", res=pst.NotExpr(child=pst.TagExpr(tag="check"))),
    Case(
        spec="@check and not pep8",
        res=pst.AndExpr(
            children=[
                pst.TagExpr(tag="check"),
                pst.NotExpr(child=pst.KeywordExpr(keyword="pep8")),
            ]
        ),
    ),
    Case(
        spec="not pep8 and @check or @tests or something",
        res=pst.OrExpr(
            children=[
                pst.AndExpr(
                    children=[
                        pst.NotExpr(child=pst.KeywordExpr(keyword="pep8")),
                        pst.TagExpr(tag="check"),
                    ]
                ),
                pst.TagExpr(tag="tests"),
                pst.KeywordExpr(keyword="something"),
            ]
        ),
    ),
    Case(
        spec="black and not black-reformat",
        res=pst.AndExpr(
            children=[
                pst.KeywordExpr(keyword="black"),
                pst.NotExpr(child=pst.KeywordExpr(keyword="black-reformat")),
            ]
        ),
    ),
]

_IDS = [
    IdCase(spec="1", res=[0]),
    IdCase(spec="2,6,4", res=[1, 5, 3]),
    IdCase(spec="1-3,4-6", res=[0, 1, 2, 3, 4, 5]),
    IdCase(spec="1-3,5-6", res=[0, 1, 2, 4, 5]),
    IdCase(spec="1-3,7-10,4", res=[0, 1, 2, 6, 7, 8, 9, 3]),
]


@pytest.mark.parametrize("case", _DEFS)
def test_basic(case: Case) -> None:
    """Make sure we parse a specification correctly."""
    assert pst.parse_spec(case.spec) == case.res


@pytest.mark.parametrize("case", _IDS)
def test_ids_basic(case: IdCase) -> None:
    """Make sure we parse a set of stage IDs correctly."""
    assert pst.parse_stage_ids(case.spec) == case.res
