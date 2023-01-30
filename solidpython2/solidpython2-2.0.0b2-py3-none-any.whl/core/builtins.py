from .scad_import import use
from .object_base import ObjectBase
from ..config import config

# ====================
# = dynamic builtins =
# ====================
"""
    This loads all the built in OpenSCAD functions (like circle, square, color,
    translate.....) from builtins.openscad file.
    I intentionally didn't use a *.scad file because it would be ignore through
    .gitignore und would be a pain to maintain (unless we remove *.scad from
    .gitignore, but that would cause a lot of generated files to show up while
    developing...).
"""
if config.use_implicit_builtins:
    use(config.builtins_file, skip_render=True)
else:
    from .builtin_primitives import *

# =============
# = modifiers =
# =============
class ModifierBase(ObjectBase):
    def __init__(self, child=None):
        super().__init__()
        if child:
            self.children += [child]

class debug(ModifierBase):
    def _render(self):
        return "#" + super()._render()

class background(ModifierBase):
    def _render(self):
        return "%" + super()._render()

class root(ModifierBase):
    def _render(self):
        return "!" + super()._render()

class disable(ModifierBase):
    def _render(self):
        return "*" + super()._render()

