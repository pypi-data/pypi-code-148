#coding=utf-8
from . import __path__
from . import base
from buildz import confz
import re
import os
import sys
import buildz

"""
[
(url, id),
(url, id, []),
(url, id, [], {}),
]
"""

def listdirs(dirpaths, suffixs=[], excepts=[]):
    if type(dirpaths) == str:
        dirpaths = [dirpaths]
    rst = []
    for dirpath in dirpaths:
        k = listfiles(dirpath, suffixs, excepts)
        rst += k
    return rst

pass

def listfiles(dirpath, suffixs=[], excepts=[]):
    files = os.listdir(dirpath)
    files = [os.path.join(fp) for fp in files]
    if len(suffixs)>0:
        rst = []
        for fp in files:
            for sfx in suffixs:
                if len(fp)<len(sfx):
                    continue
                if fp[-len(sfx):] == sfx:
                    rst.append(fp)
                    break
        files = rst
    if len(excepts)>0:
        rst = []
        for fp in files:
            find = False
            for exp in excepts:
                if len(fp)<len(sfx):
                    continue
                if fp[-len(sfx):] == sfx:
                    find = True
                    break
            if not find:
                rst.append(fp)
        files = rst
    return files

pass

class Config(base.Base):
    def add_file(self, filepath):
        self.filepaths.append(filepath)
        self.reset()
    def reset(self):
        filepaths = self.filepaths
        if type(filepaths) == str:
            filepaths = [filepaths]
        self.filepaths = filepaths
        rst = []
        self.urls = []
        for fp in self.filepaths:
            rst += confz.loadfile(fp)
        for val in rst:
            if len(val)<2:
                print("Error Config:", val)
                continue
            if len(val) == 2:
                val.append([])
            if len(val) == 3:
                val.append({})
            url, path, args, maps = val
            self.urls.append([url, path, args, maps])
    def __init__(self, builds, filepaths, root = None):
        super(Config, self).__init__()
        self.builds = builds
        self.filepaths = filepaths
        if root is not None:
            sys.path.append(root)
        self.reset()
    def deal(self):
        url = self.input.url
        type = self.input.type
        for pt, obj, args, maps in self.urls:
            if len(pt)==0 or pt[0]!="^":
                pt = "^"+pt
            if len(re.findall(pt, url))== 0:
                continue
            obj = self.builds.get(obj)
            obj._set(self)
            try:
                obj.init(*args, **maps)
                if type == base.GET:
                    obj.get()
                elif type == base.POST:
                    obj.post()
                else:
                    pass
            except Exception as exp:
                print("Exp:", exp)
                self.output.set_str(str(exp))
                self.output.finish(True)
            if self.output.finish():
                break
        if self.output() is None:
            self.output.set_str("404 Not Found Config")
pass


def run(profilepaths):
    dirpath = os.path.join(__path__[0], "profiles", "base.confz")
    default_profiles = [dirpath]
    profilepaths += default_profiles
    builder = buildz.Builder(0, default_import = "buildz.base", ref_this = "this")
    for filepath in profilepaths:
        builder.add_file(filepath)
    builder.run("main")
    
pass


