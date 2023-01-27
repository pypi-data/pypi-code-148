from random import choice
from jft.dict.frequencies.choose import f as choose
from jft.string.given_name.is_a import f as is_a_given_name
from jft.pickle.load_if_exists import f as load_pickle

def f():
  q3 = load_pickle('./jft/string/given_name/q3.pickle')
  if not q3: raise ValueError('pickle not available')
  q3_keys = sorted(list(q3.keys()))
  q3_keys_where_first_char_in_AZ = q3_keys[:q3_keys.index('aa')]
  _z = choice(q3_keys_where_first_char_in_AZ)
  _2 = q3[_z[-2:]]
  while _2 != '!':
    _2 = choose(q3[_z[-2:]])
    _z += _2
  return _z[:-1]

t = lambda: is_a_given_name(f())
