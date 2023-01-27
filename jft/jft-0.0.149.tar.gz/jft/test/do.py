from time import time
from jft.test.handle_pass import f as hp
from jft.dict.test_durations.to_tuple_list_sorted_by_duration import f as srt
from jft.directory.list_testables import f as list_testables
from os.path import getmtime
from jft.test.make_Pi_to_test import f as make_Pi_t
from jft.pickle.load_if_exists import f as load_pickle
from jft.file.remove import f as remove
from jft.pickle.save import f as save
from jft.strings.pyfiles.to_dict import f as pyfiles_to_dict
from jft.string.contains.function.test import f as has_t
from jft.string.contains.function.run import f as has_f
from jft.test.pi_test_failed import f as _pi_test_failed
from jft.test.handle_fail import f as hf
from jft.text_colours.danger import f as danger
from jft.text_colours.warning import f as warn
def f(test_all=False, t_0=time()):
  _Pi = list_testables()
  try: prev = load_pickle('./last_modified.pickle') or set()
  except EOFError as eofe: remove('./last_modified.pickle'); prev = set()
  last_mods = {py_filename: getmtime(py_filename) for py_filename in _Pi}
  save(last_mods, './last_modified.pickle')
  _Pi_fail = set()
  _A = [_[0] for _ in srt(last_mods)[::-1]]
  _B = set(make_Pi_t(_Pi, test_all, prev, last_mods) + list(_Pi_fail))
  _Pi_t = [a for a in _A if a in _B]
  pyfile_data = pyfiles_to_dict(_Pi_t)
  max_len = 0
  for _pi_index, _pi in enumerate(_Pi_t):
    content = pyfile_data[_pi]
    _m = ' '.join([
      f'[{(100*(_pi_index+1)/len(_Pi_t)):> 6.2f} % of',
      f'{_pi_index+1}/{len(_Pi_t)} files.] Checking {_pi}'
    ])
    max_len = max(max_len, len(_m))
    # print(f'{_m:<{max_len}}', end='\r')
    print(f'{_m:<{max_len}}')
    if not has_t(content): return hf(_Pi_fail, _pi, danger(" has no ")+warn('t()'))
    if not has_f(content): return hf(_Pi_fail, _pi, danger(" has no ")+warn('f()'))
    if _pi_test_failed(_pi): return hf(_Pi_fail, _pi, '')
  return hp(t_0, _Pi_t)
