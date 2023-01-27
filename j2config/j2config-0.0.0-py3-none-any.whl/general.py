
def get_model_template_version(template_file):
	"""returns the template version/model from template file if defined with variables `template_version` and `set model`.
	return dash (`-`) if none.
	"""
	template_ver, model = '-', '-'
	with open(template_file, 'r') as f:
		lns = f.readlines()
		for l in lns:
			if l.find("template_version") > 0:
				template_ver = l.split('"')[1]
			if l.find("set model") > 0:
				model = l.split('"')[1].lower()
	return model,template_ver
