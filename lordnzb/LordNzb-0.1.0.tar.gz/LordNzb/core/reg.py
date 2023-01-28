import regex as re


class multi_regex_matching():
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