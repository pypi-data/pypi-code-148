from ..core import builtins
from ..core.object_base import ObjectBase

__nothing__ = None

# ============================================
# = union, difference, intersectin operators =
# ============================================
"""
    These "operators" get monkey patched onto ObjectBase further down.
"""
def _union_op(self, x):
    """
    This makes u = a+b identical to:
    u = union()(a, b )
    """
    res = builtins.union()

    #add self or all its children to res
    if isinstance(self, builtins.union):
        for c in self.children:
            res.add(c)
    else:
        res.add(self)

    #add x or all its children to res
    if isinstance(x, builtins.union):
        for c in x.children:
            res.add(c)
    else:
        res.add(x)

    return res

def _difference_op(self, x):
    """
    This makes u = a - b identical to:
    u = difference()(a, b )
    """
    res = builtins.difference()

    if isinstance(self, builtins.difference) and len(self.children):
        for c in self.children:
            res.add(c)
    else:
        res.add(self)

    res.add(x)
    return res

def _intersection_op(self, x):
    """
    This makes u = a * b identical to:
    u = intersection()(a, b )
    """
    res = builtins.intersection()

    if isinstance(self, builtins.intersection) and len(self.children):
        for c in self.children:
            res.add(c)
    else:
        res.add(self)

    if isinstance(x, builtins.intersection):
        for c in x.children:
            res.add(c)
    else:
        res.add(x)

    return res

#bind operators to ObjectBase
# &, |, +, -, * operators -> union, difference, intersection
ObjectBase.__add__ = _union_op
ObjectBase.__or__ = _union_op
ObjectBase.__radd__ = _union_op
ObjectBase.__sub__ = _difference_op
ObjectBase.__mul__ = _intersection_op
ObjectBase.__and__ = _intersection_op
ObjectBase.__invert__ = lambda self: builtins.debug()(self)

