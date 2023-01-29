#!%PYTHON_HOME%\python.exe
# coding: utf-8
# version: python38

from yutils.tools.colors import print_color


def verbose_print(verbose, *args, color=None, **kwargs):
    if verbose:
        printer(*args, color=color, **kwargs)


def printer(*args, color=None, **kwargs):
    if color is None:
        print(*args, **kwargs)
    else:
        text = ' '.join('{}'.format(arg) for arg in args)
        print_color(text, color=color, **kwargs)


def ignore(*args, color=None):
    pass


def get_verbose_printer(verbose):
    func = printer if verbose else ignore
    return func


def get_verbose_level_printer(verbose_level):
    if not verbose_level:
        return ignore

    def level_printer(level, *args, color=None, **kwargs):
        if level <= verbose_level:
            printer(*args, color=color, **kwargs)

    return level_printer
