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
"""The hierarchy of classes representing an expression and its components."""

from __future__ import annotations

import abc
import dataclasses

from . import defs


@dataclasses.dataclass(frozen=True)
class BoolExpr(metaclass=abc.ABCMeta):
    """A boolean expression parsed out of a specification string."""

    @abc.abstractmethod
    def evaluate(self, obj: defs.TaggedFrozen | defs.Tagged) -> bool:
        """Evaluate the expression for the specified object."""
        raise NotImplementedError(f"{type(self).__name__}.evaluate() must be overridden")


@dataclasses.dataclass(frozen=True)
class TagExpr(BoolExpr):
    """A tag to be checked against obj.tags."""

    tag: str

    def evaluate(self, obj: defs.TaggedFrozen | defs.Tagged) -> bool:
        """Check whether the tag is present in the object's list of tags."""
        return self.tag in obj.tags


@dataclasses.dataclass(frozen=True)
class KeywordExpr(BoolExpr):
    """A tag to be checked against an object's name or list of tags."""

    keyword: str

    def evaluate(self, obj: defs.TaggedFrozen | defs.Tagged) -> bool:
        """Check whether the tag is present in the object's list of tags."""
        return any(self.keyword in item for item in obj.get_keyword_haystacks())


@dataclasses.dataclass(frozen=True)
class NotExpr(BoolExpr):
    """A negated boolean expression."""

    child: BoolExpr

    def evaluate(self, obj: defs.TaggedFrozen | defs.Tagged) -> bool:
        """Check whether the specified expression does not hold true."""
        return not self.child.evaluate(obj)


@dataclasses.dataclass(frozen=True)
class AndExpr(BoolExpr):
    """An "atom and atom [and atom...]" subexpression."""

    children: list[BoolExpr]

    def evaluate(self, obj: defs.TaggedFrozen | defs.Tagged) -> bool:
        """Check whether all the specified expressions hold true."""
        return all(child.evaluate(obj) for child in self.children)


@dataclasses.dataclass(frozen=True)
class OrExpr(BoolExpr):
    """An "subexpr or subexpr [or subexpr...]" subexpression."""

    children: list[BoolExpr]

    def evaluate(self, obj: defs.TaggedFrozen | defs.Tagged) -> bool:
        """Check whether any of the specified expressions hold(s) true."""
        return any(child.evaluate(obj) for child in self.children)
