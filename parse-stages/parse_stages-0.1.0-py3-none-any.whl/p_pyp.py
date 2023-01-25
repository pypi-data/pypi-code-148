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
"""Parse an expression using the pyparsing library."""

from __future__ import annotations

import pyparsing as pyp

from . import expr


_p_ws = pyp.White()[...]

_p_tag = pyp.Char("@").suppress() + pyp.Word(pyp.alphanums + "_-")

_p_keyword = pyp.Word(pyp.alphanums + "_-")

_p_atom = _p_tag | _p_keyword

_p_not_atom = pyp.Literal("not").suppress() + _p_ws.suppress() + _p_atom

_p_and_expr = (_p_not_atom | _p_atom) + (
    _p_ws.suppress() + pyp.Literal("and").suppress() + _p_ws.suppress() + (_p_not_atom | _p_atom)
)[...]

_p_or_expr = (
    _p_and_expr
    + (_p_ws.suppress() + pyp.Literal("or").suppress() + _p_ws.suppress() + _p_and_expr)[...]
)

_p_spec = _p_ws.suppress() + _p_or_expr


@_p_tag.set_parse_action
def _parse_tag(tokens: pyp.ParseResults) -> expr.TagExpr:
    """Parse a tag name."""
    assert len(tokens) == 1 and isinstance(tokens[0], str), repr(tokens)
    return expr.TagExpr(tag=tokens[0])


@_p_keyword.set_parse_action
def _parse_keyword(tokens: pyp.ParseResults) -> expr.KeywordExpr:
    """Parse a keyword."""
    assert len(tokens) == 1 and isinstance(tokens[0], str), repr(tokens)
    return expr.KeywordExpr(keyword=tokens[0])


@_p_atom.set_parse_action
def _parse_atom(tokens: pyp.ParseResults) -> expr.BoolExpr:
    """Parse an atom (a tag or a keyword)."""
    assert len(tokens) == 1 and isinstance(tokens[0], (expr.TagExpr, expr.KeywordExpr))
    return tokens[0]


@_p_not_atom.set_parse_action  # type: ignore[misc]
def _parse_not_atom(tokens: pyp.ParseResults) -> expr.NotExpr:
    """Parse a "not @tag" or "not keyword" element."""
    assert len(tokens) == 1 and isinstance(tokens[0], expr.BoolExpr)
    return expr.NotExpr(child=tokens[0])


@_p_and_expr.set_parse_action  # type: ignore[misc]
def _parse_and_expr(tokens: pyp.ParseResults) -> expr.BoolExpr:
    """Parse a "atom [and atom...]" subexpression."""
    children: list[expr.BoolExpr] = tokens.as_list()
    assert children and all(isinstance(item, expr.BoolExpr) for item in children)
    if len(children) == 1:
        return children[0]

    return expr.AndExpr(children=children)


@_p_or_expr.set_parse_action  # type: ignore[misc]
def _parse_or_expr(tokens: pyp.ParseResults) -> expr.BoolExpr:
    """Parse a "subexpr [or subexpr...]" subexpression."""
    children: list[expr.BoolExpr] = tokens.as_list()
    assert children and all(isinstance(item, expr.BoolExpr) for item in children)
    if len(children) == 1:
        return children[0]

    return expr.OrExpr(children=children)


_p_complete = _p_spec.leave_whitespace()


def parse_spec(spec: str) -> expr.BoolExpr:
    """Parse an expression using the pyparsing library."""
    res = _p_complete.parse_string(spec, parse_all=True).as_list()
    assert len(res) == 1 and isinstance(res[0], expr.BoolExpr), repr(res)
    return res[0]


_p_stage_id = pyp.Word(pyp.srange("[1-9]"), pyp.srange("[0-9]"))

_p_stage_range = _p_stage_id + pyp.Opt(pyp.Literal("-").suppress() + _p_stage_id)

_p_stage_ids = _p_stage_range + (pyp.Literal(",").suppress() + _p_stage_range)[...]


@_p_stage_id.set_parse_action
def _parse_stage_id(tokens: pyp.ParseResults) -> int:
    """Parse a single stage ID, return it as a zero-based index."""
    assert len(tokens) == 1 and isinstance(tokens[0], str), repr(tokens)
    res = int(tokens[0]) - 1
    assert res >= 0, repr((tokens, res))
    return res


@_p_stage_range.set_parse_action
def _parse_stage_range(tokens: pyp.ParseResults) -> list[int]:
    """Parse a range of stage IDs (possibly only containing a single one)."""
    if len(tokens) == 1:
        assert isinstance(tokens[0], int), repr(tokens)
        return [tokens[0]]

    assert (
        len(tokens) == 2
        and isinstance(tokens[0], int)
        and isinstance(tokens[1], int)
        and tokens[0] < tokens[1]
    ), repr(tokens)
    return list(range(tokens[0], tokens[1] + 1))


_p_stage_ids_complete = _p_stage_ids.leave_whitespace()


def parse_stage_ids(spec: str) -> list[int]:
    """Parse a list of stage ranges, return them as zero-based indices."""
    res: list[int] = _p_stage_ids_complete.parse_string(spec, parse_all=True).as_list()
    assert all(isinstance(item, int) and item >= 0 for item in res), repr(res)
    return res
