from __future__ import annotations

from collections.abc import Sequence

from attrs import define, field

from .action import Action
from .rules import Grammar, Rule, rule

@define
class RuleUnion(Rule):
    """Match one of multiple rules."""
    
    rules: Sequence[Rule]
    """The rules to match."""
    name: str = field()
    """The name of the rule."""
    
    @name.default
    def _(self) -> str:
        return f"({'|'.join(map(str, self.rules))})"

    def grammar(self) -> Grammar:
        yield Action.OPTIONAL
        for rule in self.rules[:-1]:
            if (yield rule):
                break
        else:
            yield Action.REQUIRE
            yield self.rules[-1]

@define
class OnceOrMore(Rule):
    """Match a rule one or more times."""
    
    rule: Rule
    """The rule to match."""
    name: str = field()
    """The name of the rule."""

    @name.default
    def _(self) -> str:
        return f"{self.rule}+"

    def grammar(self) -> Grammar:
        yield self.rule
        yield Action.OPTIONAL
        while (yield self.rule): ...

@define
class ZeroOrMore(Rule):
    """Match a rule zero or more times."""
    
    rule: Rule
    """The rule to match."""
    name: str = field()
    """The name of the rule."""

    @name.default
    def _(self) -> str:
        return f"{self.rule}*"

    def grammar(self) -> Grammar:
        yield Action.OPTIONAL
        while (yield self.rule): ...

@define
class Optional(Rule):
    """Optionally match a rule."""
    
    rule: Rule
    """The rule to match."""
    name: str = field()
    """The name of the rule."""
    
    @name.default
    def _(self) -> str:
        return f"{self.rule}?"

    def grammar(self) -> Grammar:
        yield Action.OPTIONAL
        yield self.rule

@rule(name = "Any Character")
def Any() -> Grammar:
    """
    Matches any character.
    """
    yield Action.IS_MATCH

@rule(name = "ASCII Digit")
def AsciiDigit() -> Grammar:
    """
    Matches any ASCII digit.
    """
    yield RuleUnion(list(String(str(x)) for x in range(10)))

@define
class String(Rule):
    """Match a string."""
    
    string: str
    case_sensitive: bool = True
    name: str = field()
    
    @name.default
    def _(self) -> str:
        return repr(self.string) + ("" if self.case_sensitive else "i")
    
    def grammar(self) -> Grammar:
        for char in self.string:
            if self.case_sensitive:
                yield char
            else:
                yield RuleUnion((
                    self.__class__(char.upper()),
                    self.__class__(char.lower())
                ))


