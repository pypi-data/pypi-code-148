from zipfile import ZipFile
from jft.directory.make import f as mkdirine
from jft.directory.remove import f as rmdirie
from jft.file.load import f as load

_dir = './temp_file_zip_extract'

up = lambda: mkdirine(_dir)
dn = lambda: rmdirie(_dir)

def f(source, destination):
  with ZipFile(source, 'r') as _f: _f.extractall(destination)

def t():
  up()
  f('./jft/file/zip/test_data.zip', _dir)
  y = load('./jft/file/zip/test_y.txt')
  z = load(f'{_dir}/pi.txt')
  dn()
  return y == z
