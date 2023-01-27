from jft.nop_x import f as nopx
from os import rmdir
from os.path import exists
from os import mkdir
from jft.file.save import f as save
from os import listdir
from os.path import isdir
from os import remove

def f(directory, filepaths=[]):
  if not exists(directory): return
  for item in listdir(directory):
    _pi = directory+'/'+item
    f(_pi, filepaths) if isdir(_pi) else remove(_pi)
  rmdir(directory)

temp_dir = './temp_directory_remove'
temp_files_and_content = [
  (f'{temp_dir}/foo.py', 'f = lambda: None\nt = lambda: f() is None'),
  (f'{temp_dir}/xyz.txt', 'xyz'),
]

def up():
  (mkdir if not exists(temp_dir) else nopx)(temp_dir)
  [save(filename, content) for (filename, content) in temp_files_and_content]

def t(): up(); f(temp_dir); return 0 == exists(temp_dir)
