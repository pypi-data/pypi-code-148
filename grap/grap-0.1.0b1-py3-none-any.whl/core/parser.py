from __future__ import annotations

from collections.abc import Generator
from functools import partial
from typing import Optional

from attrs import define, Factory, field
from loguru import logger

from .action import Action
from .errors import ParseError
from .rules import Rule


logger.disable("grap.core")

def parse(rule: Rule, text: str) -> ParsedRule:
    """
    Parameters
    ----------
    rule
        The rule to parse the text with.
    
    text
        The text to parse.
    
    Returns
    -------
    The parse tree.
    """
    tree, pointer, consumed = _parse_rule(rule, text)
    assert tree is not None
    assert consumed
    if len(text) - 1 >= pointer:
        raise ParseError(f"not all characters were consumed (expected EOF)", pointer)
    return tree

@define(kw_only = True)
class ParsedRule:
    """
    Attributes
    ----------
    name
        The name of the rule.
    
    rule
        The parsed rule object.
    
    match
        The consumed characters.
    
    span
        The index of the consumed characters in the parsed text.
    
    parent
        The parent rule. This is None when the rule is the root.
    
    inner
        All parsed subrules.
    
    """
    name: str
    rule: Rule
    match: str
    span: tuple[int, int]
    parent: Optional[Rule] = None
    inner: list[Rule] = field(default = Factory(list))

def _parse_rule(
    rule: Rule,
    text: str,
    *,
    pointer: int = 0,
    hooks: Optional[list[int]] = None,
    parents: Optional[list[Rule]] = None,
    all_optional: bool = False,
) -> tuple[Optional[ParsedRule], int, str]:
    """
    Returns
    -------
    A tuple containing the parsed rule, the new position of the
    pointer and the consumed characters as a string.
    """
    if hooks is None: hooks = [pointer]
    if parents is None: parents = []
    
    grammar = rule.grammar()
    
    optional: bool = all_optional
    inner: list[ParsedRule] = []
    any_consumed: bool = False
    consumed = ""
    
    partially_parsed_rule = partial(
        ParsedRule,
        name = rule.name,
        rule = rule,
        parent = None if not parents else parents[-1],
        inner = inner,
    )
    
    try:
        initial = True
        while True:
            if consumed:
                any_consumed = True
            
            if initial:
                rule_or_action = next(grammar)
            else:
                rule_or_action = grammar.send(consumed)
            
            initial = False
            consumed = ""
            
            logger.debug(f"{str(rule_or_action) = }")
            
            if rule_or_action == Action.GO_BACK:
                previous = hooks.pop()
                logger.debug(f"pointer goes back from {pointer} to {previous}")
                pointer = previous
            elif rule_or_action == Action.NO_MATCH:
                if not optional:
                    raise ParseError("did not match", pointer)
                consumed = ""
            elif rule_or_action == Action.IS_MATCH:
                logger.debug("forced consuming char")
                try:
                    char = text[pointer]
                except IndexError:
                    if not optional:
                        raise ParseError("EOF reached", pointer)
                    else:
                        consumed = ""
                        continue
                consumed = char
                hooks.append(pointer)
                pointer += 1
                logger.debug("moved pointer by 1")
            elif rule_or_action == Action.OPTIONAL:
                optional = True
                logger.debug("made rules optional")
            
            elif rule_or_action == Action.REQUIRE:
                if all_optional:
                    logger.debug("encountered REQUIRE but suppressing it")
                else:
                    optional = False
                    logger.debug(f"made rules mandatory for rule {rule} and its subrules")
            
            elif isinstance(rule_or_action, str):
                char = rule_or_action
                if len(char) != 1:
                    raise ParseError("expected char, got {char!r}", pointer)
                logger.debug(f"checking for character {char!r}")
                try:
                    got = text[pointer]
                except IndexError:
                    if not optional:
                        raise ParseError(f"expected {char!r}, got EOF", pointer)
                    else:
                        consumed = ""
                        continue
                if char == got:
                    logger.debug(f"character {char!r} matches")
                    consumed = char
                    hooks.append(pointer)
                    pointer += 1
                    logger.debug("moved pointer by 1")
                else:
                    logger.debug(f"character {char!r} does not match {got!r}")
                    if not optional:
                        raise ParseError(
                            f"expected {char!r}, got {got!r}", pointer
                        )
                    consumed = ""
            elif isinstance(rule_or_action, Rule):
                logger.debug(f"parsing subrule {rule_or_action} of {rule}")
                parsed_subrule, pointer, consumed = _parse_rule(
                    rule_or_action,
                    text,
                    pointer = pointer,
                    #hooks = hooks,
                    parents = [*parents, rule_or_action],
                    all_optional = optional,
                )
                if consumed:
                    assert parsed_subrule is not None
                    inner.append(parsed_subrule)
            
            else:
                raise TypeError(
                    f"invalid object {rule_or_action!r} of type "
                    f"{type(rule_or_action)!r}"
                )
    except StopIteration:
        pass
    
    if any_consumed:
        span = (hooks[-1], pointer) # - (1 if parents else 0))
        match = text[slice(*span)]
        parsed_rule = partially_parsed_rule(match = match, span = span)
    else:
        match = ""
        parsed_rule = None
    logger.debug(f"successfully parsed rule {rule}: {match!r}")
    return parsed_rule, pointer, match
    #return parsed_rule, pointer, any_consumed # when any_consumed is changed to match, there is an infinite loop
