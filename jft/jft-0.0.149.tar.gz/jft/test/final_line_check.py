from jft.directory.list_testables import f as list_testables
from jft.file.load import f as load
from jft.pf import f as pf
from jft.text_colours.danger import f as danger
from jft.text_colours.success import f as success
from jft.file.save import f as save
from jft.file.remove import f as remove
from jft.terminal import Terminal

def f(pyfilepaths=None, term=None):
  term = term or Terminal()
  term.print('Checking final lines...', end='\r')
  pyfilepaths = pyfilepaths or list_testables()
  for _pi in pyfilepaths:
    _lines = load(_pi).split('\n')
    _last_line_index = len(_lines)-1
    l = _lines[_last_line_index]
    if l != '': return pf(
      ['', f'{_pi}:{_last_line_index}', danger([l])],
      p=term.print
    )
  term.print(f"{success('PASS')} Final lines "+' '*20)
  return True

def t_a_and_b():
  _test_files = {
    './a.pz': "\n".join(["abc", "xyz"]),
    './b.pz': "\n".join(["abc", "xyz", '']),
  }

  for (k, v) in _test_files.items(): save(k, v)  
  
  x = list(_test_files.keys())
  y = False
  y_out_stream_list = [
    'Checking final lines...\r',
    "\n./a.pz:1\n\x1b[1;31m['xyz']\x1b[0;0m\n"
  ]
  term = Terminal(mode='test')
  z = f(x, term=term)
  
  for k in _test_files: remove(k)

  if y != z: return pf([
    'y != z',
    f'y: {y}',
    f'z: {z}'
  ])
  if term.output_stream_as_list != y_out_stream_list: return pf([
    'term.output_stream_as_list != y_out_stream_list',
    f'term.output_stream_as_list: {term.output_stream_as_list}',
    f'y_out_stream_list:          {y_out_stream_list}',
  ])
  return True

def t_b():
  _test_files = {
    './b.pz': "\n".join(["abc", "xyz", '']),
  }

  for (k, v) in _test_files.items(): save(k, v)  
  
  x = list(_test_files.keys())
  y = True
  y_out_stream_list = [
    'Checking final lines...\r',
    '\x1b[1;32mPASS\x1b[0;0m Final lines                     \n'
  ]
  term = Terminal(mode='test')
  z = f(x, term=term)
  
  for k in _test_files: remove(k)

  if y != z: return pf([
    'y != z',
    f'y: {y}',
    f'z: {z}'
  ])
  if term.output_stream_as_list != y_out_stream_list: return pf([
    'term.output_stream_as_list != y_out_stream_list',
    f'term.output_stream_as_list: {term.output_stream_as_list}',
    f'y_out_stream_list:          {y_out_stream_list}',
  ])
  return True

def t():
  if not t_a_and_b(): return pf('not t_a_and_b()')
  if not t_b(): return pf('not t_b()')
  return True
