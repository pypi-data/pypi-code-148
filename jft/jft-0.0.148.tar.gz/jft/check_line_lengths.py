from jft.text_colours.success import f as success
from jft.directory.list_testables import f as list_testables
from jft.file.load import f as load
from jft.pf import f as pf
from jft.text_colours.danger import f as danger
from jft.file.save import f as save
from jft.terminal import Terminal
from jft.file.remove import f as remove

# check_line_lengths
def f(filepaths=None, term=None):
  term = term or Terminal()
  term.print('Checking line lengths...', end='\r')
  filepaths = filepaths or list_testables()
  for pi in filepaths:
    ignore_line_lengths = False
    for line_index, line in enumerate(load(pi).split('\n')):
      if 'ignore_overlength_lines' in line: ignore_line_lengths = True
      if len(line) > 80 and not ignore_line_lengths: return pf([
        f'{pi}:{line_index+1}',
        danger(line)
      ], p=term.print)
  term.print(f"{success('PASS')} Line Lengths "+' '*20)
  return True

def t_expected_true():
  _test_files = {
    './a.pz': "\n".join(["abc", "xyz"]),
    './b.pz': "\n".join(["abc", "xyz", '']),
  }

  for (k, v) in _test_files.items(): save(k, v)  
  
  x = list(_test_files.keys())
  y = True
  y_out_stream_list = [
    'Checking line lengths...\r',
    '\x1b[1;32mPASS\x1b[0;0m Line Lengths                     \n'
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

def t_expected_false():
  w = 90
  _test_files = {
    './a.pz': "\n".join(["abc", "xyz"]),
    './b.pz': "\n".join(["abc", "xyz", '']),
    './c.pz': "\n".join(["abc", "xyz", '-'*w, '']),
  }

  for (k, v) in _test_files.items(): save(k, v)  
  
  x = list(_test_files.keys())
  y = False
  y_out_stream_list = [
    'Checking line lengths...\r',
    './c.pz:3\n\x1b[1;31m'+'-'*w+'\x1b[0;0m\n'
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
  if not t_expected_true(): return pf('not t_expected_true()')
  if not t_expected_false(): return pf('not t_expected_false()')
  return True
