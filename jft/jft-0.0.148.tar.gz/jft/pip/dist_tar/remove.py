from os.path import exists
from jft.directory.remove import f as rmdirie
from jft.directories.make import f as mkdirsine

def f(x='.'): rmdirie(f'{x}/dist')
temp_root = './_dist_tars_remove'
target = f'{temp_root}/dist'
def up(): mkdirsine([temp_root, target])
def dn(): rmdirie(temp_root)
def t():
  up()
  f(temp_root)
  result = all([not exists(target), exists(temp_root)])
  dn()
  return result
