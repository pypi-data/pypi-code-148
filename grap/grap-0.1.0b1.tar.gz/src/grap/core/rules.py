from __future__ import annotations

from abc import ABCMeta, abstractmethod
from collections.abc import Callable, Generator
import sys

from typing import Optional, overload, TypeAlias, Union

from .action import Action

Grammar: TypeAlias = "Generator[Union[Rule, Action, str], str, None]"


class Rule(metaclass = ABCMeta):
    def __init__(self, name: Optional[str] = None):
        """
        Parameters
        ----------
        name
            The name of the rule. Defaults to the class's name.
        """
        self.name = name or self.__class__.__name__
    
    def __str__(self) -> str:
        return self.name
    
    @abstractmethod
    def grammar(self) -> Grammar:
        ...

@overload
def rule(
    fn: Callable[[], Grammar],
    /, *,
    name: None = None,
    doc: None = None,
) -> type[Rule]: ...

@overload
def rule(
    fn: None = None,
    /, *,
    name: Optional[str] = None,
    doc: Optional[str] = None,
) -> Callable[[Callable[[], Grammar]], type[Rule]]: ...

def rule(
    fn: Optional[Callable[[], Grammar]] = None,
    /, *,
    name: Optional[str] = None,
    doc: Optional[str] = None
) -> Union[
    type[Rule],
    Callable[[Callable[[], Grammar]], type[Rule]],
]:
    """
    Decorator to quickly define a rule.
    
    The function that is decorated should not take any
    arguments. The function is converted into a staic
    method of the newly created rule. The docstring of
    the decorated function is assigned to the rule class.
    
    Parameters
    ----------
    fn
        The function to decorate.
    
    name
        The name of the rule. Defaults to the function's name.
    
    doc
        The docstring of the rule. Defaults to function's docstring.
    
    Examples
    --------
    .. code-block::
       
       from grap.core import Grammar, rule
       
        @rule
        def pet() -> Grammar:
            yield "p"
            yield "e"
            yield "t"
    
    .. code-block::
        
        from grap.core import Grammar, rule
        
        @rule(name = "dog")
        def pet() -> Grammar:
            yield "d"
            yield "o"
            yield "g"
    
    """
    def decorator(fn: Callable[[], Grammar]) -> type[Rule]:
        class R(Rule):
            grammar = staticmethod(fn)
        
        R.__name__ = name or fn.__name__
        R.__doc__ = doc or fn.__doc__
        return R
    
    if fn is None:
        return decorator
    return decorator(fn)


