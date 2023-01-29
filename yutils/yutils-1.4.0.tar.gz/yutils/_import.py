#!%PYTHON_HOME%\python.exe
# coding: utf-8

np = None
pd = None
plt = None


def import_numpy():
    global np
    if np is None:
        import numpy as np
    return np


def import_pandas():
    global pd
    if pd is None:
        import pandas as pd
    return pd


def import_matplotlib():
    global plt
    if plt is None:
        import matplotlib.pyplot as plt
    return plt
