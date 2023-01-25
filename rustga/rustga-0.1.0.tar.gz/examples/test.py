from math import sin

import rustga


def score_fn(x: list) -> float:
    return sin(sum(x)) ** 2

param = rustga.GAParams(2, 100, 0.1, 0.1, 0.1, 3)
ga = rustga.GASolver(score_fn, param)


print("ans: ", ga.run())
