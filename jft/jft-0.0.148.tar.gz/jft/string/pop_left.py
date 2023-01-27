from jft.pf import f as pf
def f(x): return (x[1:], x[:1])
def t():
  x = 'abcd'
  y = ('bcd', 'a')
  z = f(x)
  return y == z or pf(['y != z', f'x: {x}', f'y: {y}', f'z: {z}'])
