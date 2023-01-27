from importlib import import_module
from jft.directory.make import f as mkdirine
from jft.directory.remove import f as rmdirie
from jft.file.save import f as save

f = lambda x: not import_module(x.replace('/','.').replace('..','')[:-3]).t()

_dir = './_pi_test_failed'
_expected_pass_pi_path = f'{_dir}/_expected_pass.py'
_expected_fail_pi_path = f'{_dir}/_expected_fail.py'

def up():
  mkdirine(_dir)
  save(_expected_pass_pi_path, 'f = lambda: None\nt = lambda: True')
  save(_expected_fail_pi_path, 'f = lambda: None\nt = lambda: False')

def dn(): rmdirie(_dir)

def t():
  up()
  result = all([not f(_expected_pass_pi_path), f(_expected_fail_pi_path)])
  dn()
  return result
