from datetime import date
from datetime import datetime as dt
f = lambda x: dt(x.year, x.month, x.day).timestamp()
t = lambda: all([
  f(date(1970,1,1)) == -36000,
  f(date(1970,1,2)) == 50400,
  f(date(2022,3,4)) == 1646312400
])
