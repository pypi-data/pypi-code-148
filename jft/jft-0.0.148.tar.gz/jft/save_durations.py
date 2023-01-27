from jft.pickle.save import f as save
from os.path import exists
from jft.pickle.load_if_exists import f as load_if_exists
from os import remove
from jft.pf import f as pf

f = lambda durations: save(durations, 'durations.pickle')

dir_path = '.'
file_path = f'{dir_path}/durations.pickle'
data = {'a': 0, 'b': 1, 'c': {'x': True, 'y': False}}

def up():
  if exists(file_path):
    backup = load_if_exists(file_path)
    remove(file_path)
    return backup

dn = lambda backup: f(backup) if backup else remove(file_path)

def t():
  backup = up()
  y = data
  f(data)
  z = load_if_exists(file_path)
  dn(backup)
  return y == z or pf([
    'Case where pickle does not exist failed.',
    f'y: {y}',
    f'z: {z}',
  ])
