from jft.pf import f as pf

def f(durations, name, δt_ms):
  durations[name] = (
    (durations[name] + δt_ms)/2
    if name
    in durations
    else δt_ms
  )
  return durations

def t_value_update():
  y = {'a': 0, 'b': 1.5}
  z = f({'a': 0, 'b': 1}, 'b', 2)
  return y == z or pf([
    'Value update test failed',
    f'y: {y}',
    f'z: {z}',
  ])

def t_value_create():
  y = {'a': 0, 'b': 1, 'c': 2}
  z = f({'a': 0, 'b': 1}, 'c', 2)
  return y == z or pf([
    'Value create test failed',
    f'y: {y}',
    f'z: {z}',
  ])

t = lambda: all([t_value_update(), t_value_create()])
