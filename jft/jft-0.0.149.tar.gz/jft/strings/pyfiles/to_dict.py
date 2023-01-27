from jft.file.load import f as load
from jft.file.save import f as save
from jft.directory.make import f as mkdir
from jft.file.remove import f as remove
from jft.directory.remove import f as remove_dir
f = lambda x: {φ: load(φ) for φ in x}
_root = '../temp_pyfiles_to_dict'
_Pi = [(f'{_root}/foo.py', 'foo'), (f'{_root}/bar.py', 'bar')]
dn = lambda: [*[remove(_pi_f) for (_pi_f, _) in _Pi], remove_dir(_root)]
up = lambda: [mkdir(_root), *[save(_pi_f, _pi_d) for _pi_f, _pi_d in _Pi]]
def t():
  up()
  y = {f'{_root}/foo.py': 'foo', f'{_root}/bar.py': 'bar'}
  z = f([f'{_root}/foo.py', f'{_root}/bar.py'])
  dn()
  return y == z
