import jinja2
from inspect import getmembers, isfunction, isclass, isroutine

from .data_collect import DeviceDetails
from .cmn import common_fn as cmn
from . import func as func
from .func import Vrf, Vlan, Physical, Bgp, Aggregated, Loopback, Block, Summaries
from .general import *


class PrepareConfig():

	# -----------------------------------------
	# IMPORT FILTERS FOR JINJA VARIABLES
	# -----------------------------------------
	filters = {}
	filters.update({'Vrf': Vrf, 
		'Vlan': Vlan, 'Physical': Physical, 'Aggregated': Aggregated, 'Loopback': Loopback, 
		'Bgp': Bgp,
		'Block': Block, 
		'Summaries': Summaries
	})
	filters.update(dict(getmembers(cmn, isfunction)))
	filters.update(dict(getmembers(Vrf, lambda x:not(isroutine(x))))['__dict__'] )
	filters.update(dict(getmembers(Vlan, lambda x:not(isroutine(x))))['__dict__'] )
	filters.update(dict(getmembers(Physical, lambda x:not(isroutine(x))))['__dict__'] )
	filters.update(dict(getmembers(Bgp, lambda x:not(isroutine(x))))['__dict__'] )
	filters.update(dict(getmembers(Aggregated, lambda x:not(isroutine(x))))['__dict__'] )
	filters.update(dict(getmembers(Loopback, lambda x:not(isroutine(x))))['__dict__'] )
	filters.update(dict(getmembers(Block, lambda x:not(isroutine(x))))['__dict__'] )
	filters.update(dict(getmembers(Summaries, lambda x:not(isroutine(x))))['__dict__'] )
	filters.update(dict(getmembers(func, isfunction)))

	def __init__(self,
		data_file,
		jtemplate_file,
		output_folder,
		global_variables_file=None,	
		):
		self.data_file = data_file
		self.jtemplate_file = jtemplate_file.replace("\\", '/')
		self.output_folder = output_folder
		self.global_variables_file = global_variables_file

	def start(self):
		# ## LOAD - DATA
		DD = DeviceDetails(self.global_variables_file, self.data_file)

		# ## LOAD - JINJA TEMPLATE AND ENVIRONMENT
		templateLoader = jinja2.FileSystemLoader(searchpath='')
		templateEnv = jinja2.Environment(loader=templateLoader, 
			extensions=['jinja2.ext.loopcontrols', 'jinja2.ext.do',])
		for key, value in self.filters.items():
			templateEnv.filters[key] = value

		# ## TEMPLATE FILE		
		template = templateEnv.get_template(self.jtemplate_file)
		outputText = template.render(DD.data)#, undefined=jinja2.StrictUndefined) # Enable undefined for strict variable check

		# ## WRITE OUT
		model, template_ver = get_model_template_version(self.jtemplate_file)
		op_file = f"{self.output_folder}/{DD.data['var']['hostname']}-{model}-{template_ver}-j2Gen.cfg"
		with open(op_file, 'w') as f:
			f.write(outputText)

