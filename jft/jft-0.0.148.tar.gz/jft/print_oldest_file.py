from jft.pickle.load_if_exists import f as load_pickle
from jft.directory.list_testables import f as list_testables
from jft.file.remove import f as remove
from os.path import getmtime
from jft.pickle.save import f as save
from jft.dict.test_durations.to_tuple_list_sorted_by_duration import f as srt
from jft.test.make_Pi_to_test import f as make_Pi_t
from jft.terminal import Terminal
from jft.pf import f as pf
from jft.file.save import f as save_file

# print_oldest_file
def f(filepaths=None, term=None):
  term = term or Terminal()
  filepaths = filepaths or list_testables()
  try: prev = load_pickle('./last_modified.pickle') or set()
  except EOFError as eofe: remove('./last_modified.pickle'); prev = set()
  last_mods = {py_filename: getmtime(py_filename) for py_filename in filepaths}
  save(last_mods, './last_modified.pickle')
  Pi_fail = set()
  _A = [_[0] for _ in srt(last_mods)[::-1]]
  _B = set(make_Pi_t(filepaths, True, prev, last_mods) + list(Pi_fail))
  Pi_t = [a for a in _A if a in _B]
  result = Pi_t[-1]
  term.print(f'Oldest file: {result}')
  return result


def t():
  _test_files = {
    './a.pz': "\n".join(["abc", "xyz"]),
    './b.pz': "\n".join(["abc", "xyz", '']),
  }

  for (k, v) in _test_files.items(): save_file(k, v)
  
  x = list(_test_files.keys())
  y = x[0]
  y_out_stream_list = ['Oldest file: ./a.pz\n']
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
