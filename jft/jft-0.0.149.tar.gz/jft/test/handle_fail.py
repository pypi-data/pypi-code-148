from datetime import datetime as dt
from jft.text_colours.danger import f as danger
from jft.text_colours.warning import f as warn
from jft.pickle.save import f as save
from jft.directory.make import f as mkdirine
from jft.directory.remove import f as rmdirie
from jft.pickle.load_if_exists import f as load_pickle

_dir = './_handle_fail'
_failed_pickle_path = f'{_dir}/failed.pickle'

def up(): mkdirine(_dir)
def dn(): rmdirie(_dir)

def f(_Pi_failed, _pi, message, dt_now=None, root='.'):
  dt_now = dt_now or dt.now()
  _Pi_failed.add(_pi)
  save(_Pi_failed, f'{root}/failed.pickle')
  return False, f"{danger('FAIL')} {warn(_pi)} {message} {dt_now}"

def t():
  up()
  y = (
    False,
    ' '.join([
      '\x1b[1;31mFAIL\x1b[0;0m \x1b[0;33mfoo.py\x1b[0;0m foo foo',
      '2022-01-01 00:00:00'
    ])
  )
  z = f(set(['failed.py']), 'foo.py', 'foo foo', dt(2022, 1, 1), _dir)
  z_failed_pickle = load_pickle(_failed_pickle_path)
  dn()
  return all([z == y, z_failed_pickle == {'failed.py', 'foo.py'}])
