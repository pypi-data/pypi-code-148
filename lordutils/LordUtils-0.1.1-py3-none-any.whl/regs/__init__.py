
# pip install regex
import regex as re


def replace_ignore_case(s: str, replace: str, val: str):
    return re.sub(re.escape(replace), val, s, flags=re.IGNORECASE)


class regReplace:
    def __init__(self, r, ingnoreCase=False):
        if ingnoreCase:
            self.r = re.compile(r, flags=re.IGNORECASE)
        else:
            self.r = re.compile(r)

    def __call__(self, value, repl):
        return self.r.sub(repl, value)


class regGroup:
    def __init__(self, r, flags=0):
        self.r = re.compile(r, flags=flags)

    def __call__(self, value, multi=False):
        if multi:
            return [m.groupdict() for m in self.r.finditer(value)]
        else:
            _m = self.r.search(value)
            if _m is None:
                return None
            else:
                return _m.groupdict()


class multiRegMatching:
    def __init__(self, *regs, flags=0):
        self.regs = [re.compile(reg, flags=flags) for reg in regs]

    def __call__(self, value):
        for r in self.regs:
            _m = r.search(value)
            if _m is None:
                continue
            else:
                return _m.groupdict()
        return None
