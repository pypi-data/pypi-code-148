"""
Entrypoint module, in case you use `python -mpyfuckery`.


Why does this file exist, and why __main__? For more info, read:

- https://www.python.org/dev/peps/pep-0338/
- https://docs.python.org/2/using/cmdline.html#cmdoption-m
- https://docs.python.org/3/using/cmdline.html#cmdoption-m
"""
# noinspection PyProtectedMember
from fuckery.cli import _main

if __name__ == "__main__":  # pragma: no cover
    _main()
