from enum import auto, IntEnum

class Action(IntEnum):
    """
    An action influences the behaviour of the parser.
    
    There is generally no need to use them. The predefined rules in
    :mod:`grap.core.common` cover most of them.
    """
    
    GO_BACK = auto()
    """
    Moves the pointer to the previous position.
    """
    
    NO_MATCH = auto()
    """
    Acts like a rule that never matches anything.
    """
    
    IS_MATCH = auto()
    """
    Acts like a rule that always matches anything.
    """
    
    OPTIONAL = auto()
    r"""
    Suppresses :class:`errors.ParseError`\s for the
    current rule and each subrule.
    """
    
    REQUIRE = auto()
    r"""
    The parser will raise a :class:`ParseError`\s when
    following rules are not consumed. This has no effect
    when ``OPTIONAL`` was yielded by a parent rule.
    """
