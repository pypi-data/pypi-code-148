from math import prod
from jft.text_colours.bright.cyan import f as cy
from jft.int.is_prime import f as is_prime
from jft.pf import f as pf

def f(x):
  if is_prime(x): return [x]
  factors_list = [i for i in range(2, x) if (not x % i) and is_prime(i)]
  _x = x
  factor = factors_list.pop()
  _X = []
  while factors_list:
    _x = _x//factor
    _X.append(factor)
    factor = factors_list.pop() if _x % factor else factor
  _X.append(_x)
  return _X

def t():
  for x in range(2, 10000):
    z = f(x)
    if prod(z) != x: return pf([
      cy(f'x: {x}'),
      cy(f'z: {z}'),
      cy(f'prod(z): {prod(z)}')
    ])
  return True
