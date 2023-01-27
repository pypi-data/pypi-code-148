Γ = ['def t():', 't = lambda:']
f = lambda x: any([_l.startswith(γ) for γ in Γ for _l in x.split('\n')])
t = lambda: all([
  not f("f = lambda x: False"), f("f = lambda x: False\nt = lambda: False")
])
