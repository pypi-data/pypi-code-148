

import nettoolkit as nt




def get_conditions(jinja_flie):
	d = {'conditions':set(), 'loops':set(), 'variables': set() }
	with open(jinja_flie, 'r') as f:
		lns = f.readlines()
	for ln in lns:
		if ln.strip().startswith("{% for "):
			d['loops'].add(ln)
		elif ln.strip().startswith("{% if") or ln.strip().startswith("{% elif"):
			d['conditions'].add(ln)
		elif ln.strip().startswith("{% set "):
			d['variables'].add(ln)
	return d

def get_variables(jinja_flie):
	conds = set()
	with open(jinja_flie, 'r') as f:
		lns = f.readlines()
	for ln in lns:
		starts, ends = [], []
		for i in range(20):
			if i == 0: s,e = 0,0
			start = nt.STR.find_multi(ln, '{{', start=s, count=None, index=True, beginwith=False)
			end   = nt.STR.find_multi(ln, '}}', start=e, count=None, index=True, beginwith=False)
			if start == -1: break
			starts.append(start)
			ends.append(end)
			s = start+2
			e = end+2

		if starts == []: continue
		for s, e in zip(starts, ends):
			cond = ln[s:e+2]
			# print(cond, end='\t' )
			conds.add(cond)
		# print()
	return conds


# # -----------------------------------------------------------------------------------------
# #  Local Execution steps
# # -----------------------------------------------------------------------------------------

# jinja_flie = 'file.txt'

# d = get_conditions(jinja_flie)
# v = get_variables(jinja_flie)

# # #########################################
# search_var = 'dslot'
# for x in sorted(v):
# 	if x.find(search_var) > 1:
# 		print(x)
# # #########################################


# # #########################################
# # with open('conditions.txt', 'w') as f: 
# # 	for k, v in d.items():
# # 		f.write(f'\n\n// [{k}] //\n')
# # 		for l in sorted(v):
# # 			f.write(f'{l.lstrip()}')
# # #########################################
# search_condition = "sorted"
# for k, v in d.items():
# 	for l in v:
# 		if l.find(search_condition) > 1:
# 			print(l.strip())
# # #########################################

# # -----------------------------------------------------------------------------------------
