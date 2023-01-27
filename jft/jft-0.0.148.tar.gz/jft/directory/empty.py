from jft.directory.make import f as mkdir
from jft.file.save import f as save
from string import ascii_lowercase as az
from jft.directory.remove import f as rmdir
from os import listdir
from jft.file.remove import f as remove

r = './temp'
up = lambda: [mkdir(r), *[save(f'{r}/{_}.txt', _) for _ in az]]
dn = lambda: rmdir(r)
f = lambda x: [remove(f'{r}/{filename}') for filename in listdir(x)]

def t():
  up()
  α = len(listdir(r))
  f(r)
  ω = len(listdir(r))
  result = all([α>ω, ω==0])
  dn()
  return result
