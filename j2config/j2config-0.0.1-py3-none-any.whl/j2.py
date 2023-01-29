import jinja2
from inspect import getmembers, isfunction, isclass, isroutine

from .data_collect import DeviceDetails
from .cmn import common_fn as cmn
from . import func as func
from .func import Vrf, Vlan, Physical, Bgp, Aggregated, Loopback
from .general import *


class PrepareConfig():
	"""boiler plate code class for start configuration preparation
	"""

	# -----------------------------------------
	# IMPORT FILTERS FOR JINJA VARIABLES
	# -----------------------------------------
	filters = {}
	filters.update({'Vrf': Vrf, 'Bgp': Bgp,
		'Vlan': Vlan, 'Physical': Physical, 'Aggregated': Aggregated, 'Loopback': Loopback, 		
	})
	filters.update(dict(getmembers(cmn, isfunction)))
	filters.update(dict(getmembers(Vrf, lambda x:not(isroutine(x))))['__dict__'] )
	filters.update(dict(getmembers(Vlan, lambda x:not(isroutine(x))))['__dict__'] )
	filters.update(dict(getmembers(Physical, lambda x:not(isroutine(x))))['__dict__'] )
	filters.update(dict(getmembers(Bgp, lambda x:not(isroutine(x))))['__dict__'] )
	filters.update(dict(getmembers(Aggregated, lambda x:not(isroutine(x))))['__dict__'] )
	filters.update(dict(getmembers(Loopback, lambda x:not(isroutine(x))))['__dict__'] )
	filters.update(dict(getmembers(func, isfunction)))

	def __init__(self,
		data_file,
		jtemplate_file,
		output_folder=".",
		global_variables_file=None,	
		):
		self.data_file = data_file
		self.jtemplate_file = jtemplate_file.replace("\\", '/')
		self.output_folder = output_folder
		self.global_variables_file = global_variables_file

	def custom_class_add_to_filter(self, **kwargs):
		"""add custom classes and its methods as jinja filters. External callable.
		"""
		for filtername, cls in kwargs.items():
			try:
				if not self.filters.get(filtername):
					self.filters.update({filtername: cls})
				self.filters.update(dict(getmembers(cls, lambda x:not(isroutine(x))))['__dict__'] )
			except Exception as e:
				raise Exception(f"Class Insertion Failed for filter {filtername}\n{e}")

	def custom_module_methods_add_to_filter(self, *modules):
		"""add custom methods from module(s) as jinja filters. External callable.
		"""
		for module in modules:
			try:
				self.filters.update(dict(getmembers(module, isfunction)))
			except Exception as e:
				raise Exception(f"Module Insertion Failed {module}\n{e}")


	def start(self):
		"""kicks generation
		"""
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

