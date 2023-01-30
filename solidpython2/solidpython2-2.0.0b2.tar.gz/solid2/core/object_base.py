from copy import deepcopy
from textwrap import dedent

#don't do relative imports on the global scope to be able to import this file
#from "everywhere"

class ObjectBase:
    def __init__(self):
        self.children = []

    def add(self, c):
        def _add(c):
            assert(hasattr(c, "_render"))
            self.children += [c]

        if isinstance(c, list):
            for cc in c:
                _add(cc)
        else:
            _add(c)

        return self

    def copy(self):
        return deepcopy(self)

    def _render(self):
        s = ''
        for c in self.children:
            s += c._render()
        return s

    def __call__(self, *args):
        #translate(...)(cube())
        #this adds cube() to translate.children
        for a in args:
            self.add(a)
        return self

    def __repr__(self):
        return self.as_scad()

    def as_scad(self):
        from .scad_render import scad_render
        return scad_render(self)[:-1]

    def save_as_scad(self, filename='', outdir=''):
        from .scad_render import scad_render_to_file
        return scad_render_to_file(self, filename, outdir)

    def save_as_stl(self, filename='', outdir=''):
        from .scad_render import render_to_stl_file
        return render_to_stl_file(self, filename)

class OpenSCADObject(ObjectBase):
    def __init__(self, name, params):
        super().__init__()
        self.name = name
        self.params = params

    def _render(self):
        """
            returns the scad code for a given node tuple consiting of name, params
            and children list.

            -> translate(v = [1, 2, 3]) {children[0]; children[1]; ...};\n
        """
        from .utils import indent
        s = self.generate_scad_head()

        if self.children:
            s += " {\n"
            for child in self.children:
                s += indent(child._render())
            s += "}"
        else:
            s += ";"

        return s + "\n"

    def generate_scad_head(self):
        """
            for a given function name and dict of params it returns:
                {name}(p1=v1, p2=v2,...)
                -> translate(v = [1, 2, 3])
        """
        from .utils import unescape_openscad_identifier, py2openscad
        from ..config import config

        param_strings = []
        for p in sorted(self.params.keys()):
            if self.params[p] is None:
                continue

            if config.use_implicit_builtins and \
                        isinstance(self.params[p], OpenSCADParameterFunction):

                param_strings.append(self.params[p]._render())
            else:
                scad_value = py2openscad(self.params[p])
                scad_identifier = unescape_openscad_identifier(p)

                param_strings.append(f'{scad_identifier} = {scad_value}')

        scad_identifier = unescape_openscad_identifier(self.name)
        param_str = ", ".join(param_strings)

        return f'{scad_identifier}({param_str})'

class OpenSCADConstant:
    def __init__(self, name):
        self.name = name

        from .utils import escape_openscad_identifier
        self.__doc__ = escape_openscad_identifier(name)

    def __repr__(self):
        return self._render()

    def _render(self):
        return dedent(self.name)

def scad_inline(code):
    return OpenSCADConstant(code)

class OpenSCADParameterFunction(OpenSCADConstant):
    pass

def scad_inline_parameter_func(code):
    return OpenSCADParameterFunction(code)

