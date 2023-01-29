

import pandas as pd
# ---------------------------------------------------------

def read_worksheet(file, wks):
	"""read the excel worksheet 
	returns -> pandas DataFrame
	"""
	try:
		df = pd.read_excel(file, sheet_name=wks).fillna("")
	except:
		raise Exception(f"CRITICAL: {file} File Read failed. Expected Worksheet named '{wks}' missing")
	return df

def read_excel(file):
	"""read the excel file, all worksheet
	returns -> dictionary with sheetname as key and pandas DataFrame as value
	"""
	dfd = pd.read_excel(file, None)
	for k,v in dfd.items():
		dfd[k] = v.fillna("")
	return dfd

def to_int(item):
	"""try to convert item to integer
	"""
	try:
		return int(item)
	except:
		return item


class DeviceDetails():
	""" Device details operations
	"""

	def __init__(self, global_file, device_file):
		self.global_regional_data_file = global_file
		self.device_filename = device_file
		self.read()

	def read(self):
		"""start executing
		"""
		self.dev_details = self.read_device()								## require
		self.wkl = self.get_wkl()											## optional remove after global file removed
		self.region = self.get_region()										## optional remove after global file removed
		all_region_details = self.read_region_details()						## optional remove after global file removed
		self.region_details = self.merge_region_details(all_region_details)	## optional remove after global file removed
		self.var = self.merge_vars()										## optional remove after global file removed, step 2 may need
		self.table = self.dev_details['table'].T.to_dict()					## require
		self.data = {'var': self.var, 'table': self.table}					## require

	def read_device(self):
		"""read device database
		"""
		dr = {'var':{}, 'table':None}
		dr['var']['device'] = read_worksheet(self.device_filename, 'var') 		
		dr['table'] = self.merged_table_columns()
		self.device_details = dr['var']['device']
		return dr

	def merged_table_columns(self):
		"""merge the all different interfaces/protocol etc details from individual tabs in to a single dataframe.
		"""
		dfd = read_excel(self.device_filename)
		del(dfd['var'])
		df_table = pd.DataFrame({'key':[]})
		for k, df in dfd.items():
			df_table = pd.concat([df_table, df], ignore_index=True).fillna("")
		for c in df_table:
			try:		
				df_table[c] = df_table[c].apply(to_int)
				df_table[c] = df_table[c].apply(str)
			except:
				pass
		return df_table

	def get_wkl(self):
		"""get the device location detail from device var details. 'site' field is required for the same.
		"""
		try:
			df_var = self.device_details 
			for _col in df_var.columns:
				if _col == 'var': continue
				default = df_var[df_var['var'] == 'site'][_col]
				wkl = default[default.index[0]]
				if wkl: break
		except:
			raise Exception(f"CRITICAL: Data Read failed. Expected variable 'site' missing in device 'var' Worksheet")
		if not wkl:
			raise Exception(f"CRITICAL: Data Read failed. Expected value of variable 'site' missing on device 'var' Worksheet")
		return wkl

	def get_region(self):
		"""get the region detail from device var details. 'region' field is required for the same.
		"""
		try:
			ndf = self.device_details[self.device_details['var'] == 'region']
			for _col in ndf.columns:
				if _col == 'var': continue
				return ndf[_col][ndf.index[0]]
		except:
			raise Exception(f"CRITICAL: Data Read failed. Expected variable 'region' missing in device 'var' Worksheet")

	def read_region_details(self):
		"""reads global/regional data and drops other irrelavent region details from dataframe. 
		"""
		try:
			df = read_worksheet(self.global_regional_data_file, 'var') 
			for _col in df.columns:
				if _col in ('var', 'default'): continue
				if _col == self.region: continue
				df = df.drop(_col, axis=1)
			return df
		except:
			print("Global database unavailable or incorrect..")

	def _check_n_update_region(self, df):
		df.default = df[self.region] if df[self.region] != "" else df.default

	def merge_region_details(self, df):
		"""merge the region column details with defailt column, deletes region column and leave only default column along with var.
		"""
		if df is None: return pd.DataFrame()
		df.apply(self._check_n_update_region, axis=1)
		df = df.drop(self.region, axis=1)
		return df

	def merge_vars(self):
		"""merge the var details from two different dataframes ( region and device - databases )
		"""
		frames= [self.region_details, self.device_details]
		return pd.concat(frames, ignore_index=True).set_index('var').to_dict()['default']

# ---------------------------------------------------------
