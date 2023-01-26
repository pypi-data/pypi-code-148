import json
import itertools
import re


def first_lower(s):
	return s[0].lower() + s[1:]


def go_args(lst, left='', right='', type_prefix='', sep=', ', key='name', try_key=None):
	if not lst: return ''
	return left + sep.join(f'{x.get(try_key, x[key])} {prefix_non_primitives(x.get("Type"), type_prefix)}' for x in lst) + right


def go_Args(lst, left='', right='', type_prefix='', sep=', ', key='Name', try_key=""):
	if not lst: return ''
	return left + sep.join(f'{x.get(try_key, x[key])} {prefix_non_primitives(x["Type"], type_prefix)}' for x in lst) + right


def go_args_plural(lst, sep=', ', key='names', try_key=None):
	return sep.join(f'{x.get(try_key, x[key])} []{x["Type"]}' for x in lst)


def exclude(lst, lst2=[], key="nameDb"):
	if not lst: return []
	keys2 = {x[key] for x in lst2 if key in x}
	return [x for x in lst if x.get(key) not in keys2]


def go_vars(lst, fmt='', left='', right='', prefix='', suffix='', sep=', ', key='name', try_key=None):
	if not lst: return ''
	return left + sep.join(prefix + x.get(try_key, fmt.format(**x) if fmt else x[key]) + suffix for x in lst) + right


def go_fmt(lst, fmt='{key}', left='', right='', prefix='', suffix='', sep=', '):
	if not lst: return ''
	return left + sep.join(prefix + fmt.format(**x) + suffix for x in lst) + right


def _fmt(x, i=""):
	return x.replace("$i", i)


def _indent(s='', size=0, indent='\t'):
	return indent * size + s


def db_vars(lst, left='', right='', prefix='', suffix='', suffix_order_asc='', suffix_order_desc='', suffix_array='', sep=', ', start=1, key='nameDb', try_key=""):
	if not lst: return ''
	return left + sep.join(prefix + (x.get(try_key, x[key]) if try_key else x[key]) + _fmt((suffix_array if suffix_array and x.get('isArray') else suffix_order_asc if suffix_order_asc and x.get('ordering') == 2 else suffix_order_desc if suffix_order_desc and x.get('ordering') == 3 else suffix), str(i + start)) for i, x in enumerate(lst)) + right


def nth(lst, fmt='$$i', left='', right='', prefix='', suffix='', sep=', ', start=1):
	if not lst: return ''
	return left + sep.join(prefix + _fmt(fmt, str(i + start)) + suffix for i in range(len(lst))) + right


def go_Vars(lst, left='', right='', prefix='', suffix='', sep=', ', key='Name', try_key=""):
	if not lst: return ''
	return left + sep.join(prefix + (x.get(try_key, x[key]) if try_key else x[key]) + suffix for x in lst) + right


def go_vars_plural(lst, sep=', ', key='names'):
	return sep.join(x[key] for x in lst)


def go_types(lst, sep=', ', key='Type'):
	return sep.join(x[key] for x in lst)


def go_types_plural(lst, sep=', ', key='Type'):
	return sep.join("[]%s" % x[key] for x in lst)


def re_sub(s, regex="", new=""):
	return re.sub(regex, new, s)

# def go_param_name(s):
#   return first_lower(s)
#
#
# def short_name(s):
#   return ''.join(re.findall('[A-Z]', s)).lower()
mappings = {}
aliases = {}


def gql_fmt(f, s):
	if "$1" in f:
		return f.replace("$1", s)
	return f'{f}({s})'


def gql(s, x, schema):
	return conv(s, x, 'gql', schema)


def spanner(s, x, schema):
	return conv(s, x, 'spanner', schema)


def psql(s, x, schema):
	return conv(s, x, 'psql', schema)


def conv_x(s, x, typ, schema):
	return conv(s, x, typ, schema)


go_primitives = {'bool', 'int', 'int64', 'string'}
gql_primitives = {'datetime'}


def prefix_non_primitives(s, prefix="", extras=None):
	if not s: return ""
	ss = s.lstrip("*")
	if ss in go_primitives:
		return s
	elif extras and ss in extras:
		return s
	return prefix + s


def all_in(lst, key=None, target=go_primitives):
	if not lst:
		return False
	if key:
		for x in lst:
			if x[key] not in target:
				return False
	else:
		for x in lst:
			if x not in target:
				return False
	return True


def conv(s, obj, t, schema):
	if t not in obj or obj[t] is None:
		return s
	a, b = ab = obj['Type'], obj[t]['Type']
	x, y = "/" + obj['key'], "/" + obj[t]['key']
	items = itertools.product([a + x, a, x], [b + y, b, y])
	if a and a == b:
		if a in go_primitives:
			return s
	for y in list(items) + [ab]:
		if mappings.get(y):
			return gql_fmt(mappings[y], s)
	bs = b.lstrip('*')
	if bs in schema[t] and bs not in gql_primitives and t == 'gql':
		if schema[t][bs]["kind"] == "EnumDefinition":
			return s  # cast?
		else:
			return s + '.ToGraphql()'
	return s


def alias(s, opts=0):
	return aliases.get(s, [s] if opts == 1 else [])


dart_type_mappings = {
	'string': 'String',
	'bool': 'bool',
	'int': 'int',
}

dart_unknown_types = []


# def dart_type(s, x):
#   a = x['gql']['Type']
#   return f'{dart_type_mappings.get(a,s)} {s}'

def dart_optional_type_get(s, x):
	s = s.replace('*', '').replace("[]", "")
	if s not in dart_type_mappings:
		print('unknown type', s)
		dart_unknown_types.append(s)
	s = dart_type_mappings.get(s, s)
	ret = f'List<{s}>' if x['isArray'] else s
	ret = f'required {ret}' if x['notNull'] else f'{ret}?'
	return ret


def dart_args(lst):
	return '\n'.join(f'{dart_optional_type_get(x["Type"], x)} {x["nameExact"]},' for x in lst)


def nothing(s):
	return s


def unknown_types(lst):
	return [x for x in lst if x.get('Type', '').replace('*', '').replace("[]", "") not in dart_type_mappings]


def basename(name):
	return name.split('/')[-1]


def dumps(obj, indent="\t", **kw):
	return json.dumps(obj, indent=indent, **kw)


def permute(lst, size=2):
	return list(itertools.permutations(lst, size))


def combine(lst, size=2):
	return list(itertools.combinations(lst, size))


def zip_longest(x, *args):
	return list(itertools.zip_longest(*[x, *args]))


def product(lst, size=2):
	return list(itertools.product(lst, size))


def get_chain(obj, *args, default=""):
	if not obj: return ''
	for x in args:
		if x not in obj:
			return default
		obj = obj[x]
	return obj


def reject_chain(obj, *args, default=""):
	if not obj: return []
	ret = []
	for x in obj:
		if get_chain(x, *args, default=None) is None:
			ret.append(x)
	return ret


def uniq(lst, key=None):
	done = set()
	done_add = done.add
	if key is None:
		return [x for x in lst if not (x in done or done_add(x))]
	else:
		return [x for x in lst if not (x[key] in done or done_add(x[key]))]


def merge(lst, lst2=None):
	if not lst or lst2:
		return lst
	return list(lst) + lst2


def to_map(lst, key):
	return {x[key]: x for x in lst}


def lookup(m, key=None, vals=None):
	if not m:
		return m
	if key:
		return [x for x in m if not vals or x[key] == vals or x[key] in vals]
	else:
		return [x for x in m if not vals or x == vals or x in vals]


def map_with(lst, m1, key="key"):
	if not list: return []
	return [m1[x[key]] for x in lst if key in x and x[key] in m1]


def append(lst, lst2, key=None):
	if not key:
		return list(lst) + list(lst2)
	ret, done = [], set()
	for x in lst:
		if x[key] not in done:
			done.add(x[key])
			ret.append(x)
	for x in lst2:
		if x[key] not in done:
			done.add(x[key])
			ret.append(x)
	ret.sort(key=lambda y: y[key])
	return ret


def expand_embed(lst, schema=None, hidden=False):
	ret, done = [], set()
	for x in lst:
		if hidden and "directives" in x and "hidden" in x["directives"]:
			pass
		elif "directives" in x and "embed" in x["directives"]:
			if "fields" in x and x["fields"]:
				for y in x['fields']:
					if y['key'] not in done:
						ret.append(y)
						done.add(y['key'])
			elif schema and x.get('baseType') in schema:
				for y in schema[x['baseType']]['fields']:
					if y['key'] not in done:
						ret.append(y)
						done.add(y['key'])
			else:
				ret.append(x)
				done.add(x['key'])
		else:
			ret.append(x)
			done.add(x['key'])
	return ret


def json_bool(x):
	return "true" if x else "false"


allow_expr_list_re = re.compile(r'<<|>>|\*\*|//|[%~^|&()/*+-]|\d+|\s+')


def iota_eval(fmt='', idx=0, default=''):
	if not fmt:
		return default
	return eval(''.join(allow_expr_list_re.findall(fmt.replace('iota', str(idx)))), {"__builtins__": {}}, {})


def apply_filters(env, m, a):
	env.filters['arg'] = go_args
	env.filters['Arg'] = go_Args
	env.filters['args'] = go_args_plural
	env.filters['exclude'] = exclude
	env.filters['var'] = go_vars
	env.filters['Var'] = go_Vars
	env.filters['nth'] = nth
	env.filters['var_db'] = db_vars
	env.filters['vars'] = go_vars_plural
	env.filters['type'] = go_types
	env.filters['types'] = go_types_plural
	# env.filters['paramname'] = go_param_name
	# env.filters['shortname'] = short_name
	env.filters['gql'] = gql
	env.filters['psql'] = psql
	env.filters['spanner'] = spanner
	env.filters['conv'] = conv_x
	# env.filters['nothing'] = nothing
	env.filters['dart_args'] = dart_args
	env.filters['first_lower'] = first_lower
	env.filters['basename'] = basename
	env.filters['alias'] = alias
	env.filters['indent'] = _indent
	env.filters['prefix_custom'] = prefix_non_primitives
	env.filters['dumps'] = dumps
	env.filters['zip'] = zip_longest
	env.filters['combine'] = combine  # AB
	env.filters['permute'] = permute  # AB, BA
	env.filters['product'] = product  # AA, AB, BA, BB
	env.filters['get'] = get_chain
	env.filters['rejectattrs'] = reject_chain
	env.filters['uniq'] = uniq
	env.filters['merge'] = merge
	env.filters['to_map'] = to_map
	env.filters['lookup'] = lookup
	env.filters['map_with'] = map_with
	env.filters['append'] = append
	env.filters['all_in'] = all_in
	env.filters['fmt'] = go_fmt
	env.filters['json_bool'] = json_bool
	env.filters['regex_replace'] = re_sub
	env.filters['expand_embed'] = expand_embed
	env.filters['iota_eval'] = iota_eval
	# env.filters['unknown_types'] = unknown_types
	# env.filters['dart_type'] = dart_type
	mappings.update(m)
	aliases.update(a)
