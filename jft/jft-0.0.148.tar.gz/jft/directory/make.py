from os.path import exists
from os import mkdir
from re import L
from jft.nop_x import f as nop_x
from jft.directory.remove import f as remove
from jft.pf import f as pf

def f(x='./jft/classes'):
  if exists(x): return nop_x(x)
  try: mkdir(x)
  except FileNotFoundError as fe:
    f('/'.join(x.split('/')[:-1]))
    f(x)

temp_path_0 = './temp_dir_make'
temp_path_1 = f'{temp_path_0}/_'

def dn():
  remove(temp_path_1)
  remove(temp_path_0)

def t():
  f(x=temp_path_1)
  result = exists(temp_path_1)
  dn()
  return result or pf(
    f'Failed to create temporary directory: {temp_path_1}'
  )
