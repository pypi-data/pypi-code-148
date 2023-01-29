#!%PYTHON_HOME%\python.exe
# coding: utf-8
# version: python38

"""
For alternatives of classproperties with setters as well, visit:
https://gist.github.com/Skinner927/413c0e9cc8433123f426832f9fe8d931
https://stackoverflow.com/questions/5189699/how-to-make-a-class-property
"""

class classproperty(object):
    def __init__(self, f):
        self.f = f
    def __get__(self, obj, owner):
        return self.f(owner)
