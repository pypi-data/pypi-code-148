import inspect
from pathlib import Path
from .. import config, include, use, import_scad

if config.use_implicit_builtins:
    raise Exception("ExpSolid: unfortunately ImplicitCAD can't handle bosl2...")

bosl2_dir = Path(__file__).absolute().parent.parent / "libs/BOSL2"

#include bosl2/std.scad
include(bosl2_dir/"std.scad")
stdlibs = []

with open(bosl2_dir / "std.scad") as f:
    for l in f.readlines():
        l = l.strip()
        if not l.startswith("include <"):
            continue
        l = l.replace("include <", "").replace(">", "")
        include(bosl2_dir / l, skip_render=True)
        stdlibs.append(l)

#use all other bosl2/*.scad files that are not included in stdlibs
for f in bosl2_dir.iterdir():
    if not f.suffix == ".scad" or f.name in stdlibs:
        continue
    if f.name in ["std.scad", "builtins.scad", "bosl1compat.scad"]:
        continue

    name = f.name.replace(".scad","")
    frame = inspect.currentframe()
    frame.f_locals[name] = import_scad(bosl2_dir / f, use_not_include=False)

#TODO: extend this with all kinds of bosl2 features
from ..core.object_base import ObjectBase
ObjectBase.tag = lambda self, *args, **kwargs: tag(*args, **kwargs)(self)
ObjectBase.attach = lambda self, *args, **kwargs: attach(*args, **kwargs)(self)


#============ attachable add =============
#enhance the add function of the attachable OpenSCADObject so it can be used
#properly: cf. 07-libs-bosl2-attachable.py
attachable_default_add = attachable.add

def attachable_add(self, c):
    if len(self.children) == 0:
        attachable_default_add(self, c)
    elif len(self.children) == 1:
        attachable_default_add(self, union()(c))
    else:
        assert(len(self.children) == 2)
        self.children[1].add(c)

attachable.add = attachable_add
#============ attachable add end =============

