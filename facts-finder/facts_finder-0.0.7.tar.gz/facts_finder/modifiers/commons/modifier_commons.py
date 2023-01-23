
from nettoolkit import *
import pandas as pd

# ================================================================================================
# Dynamic Cisco Key Exchanger
# ================================================================================================
class KeyExchanger():

	def __init__(self, column_mapper, cmd_lst):
		self.column_mapper = column_mapper
		self.cmd_lst = cmd_lst
		self.dfd = self.read_column_mapper()
		self.update_cisco_cmd_lst()

	def read_column_mapper(self):
		dfd = pd.read_excel(self.column_mapper, None)
		for sheet, df in dfd.items():
			if sheet not in self.cmd_lst: continue
			dfd[sheet] = df.fillna("")
		return dfd

	def update_cisco_cmd_lst(self):
		for sheet, df in self.dfd.items():
			if sheet not in self.cmd_lst: continue
			for head in df:
				if not df[head][0]: continue
				self.cmd_lst[sheet][head] = df[head][0]


# ================================================================================================
# Cisco Database Object
# ================================================================================================
class DataFrameInit():

	def __init__(self, capture):
		self.capture = capture
		self.dfd = self.read_int_sheets()

	def read_int_sheets(self):
		dfd = pd.read_excel(self.capture, None)
		ndf = {}
		for sheet, df in dfd.items():
			if sheet not in self.cmd_lst: continue
			ndf[sheet] = df.fillna("")
		return ndf

	@staticmethod
	def _is_sheet_data_available(dataframe_dict, sheet_name):
		try:
			sht_df = dataframe_dict[sheet_name]
			if sht_df.empty:
				print(f"{sheet_name}: sheet data empty.")
				return None
			return sht_df
		except:
			print(f"{sheet_name}: sheet data unavailable.")
			return False



# ================================================================================================
# var Object common calls/methods class
# ================================================================================================
class Var():

	def __getitem__(self, k):
		return self.var[k]

	def __iter__(self):
		for k, v in self.var.items():
			yield k, v

	def update_var(self, key, value):
		self.var[key] = value

	@property
	def pdf_dict(self):
		return {'var': self.var_df }
	
	## Calls

	def create_a_temp_v6_hext2_3_column(self, sht_df):
		"""creates a temporary column for further processing"""
		sht_df['temp'] = sht_df['ipaddr'].apply(get_hext2_3)
		return sht_df


	def convert_to_dataframe(self):
		"""creates a new dictionary of data frame from local variables 
		--> Dictionary of Pandas DataFrame as value
		"""
		df = pd.DataFrame(self.var, index=[0]).T
		df = df.reset_index()
		df.rename(columns={'index': 'var', 0:'default'}, inplace=True)
		df.sort_values(['var'], inplace=True)
		self.var_df = df


	def update_device(self, sht):
		"""updates the multiple fields from show version output
		"""
		sht_df = self._is_sheet_data_available(self.dfd, sht)
		if sht_df.empty: return None
		#
		for k, v in self.cmd_lst[sht].items():
			try:
				x = eval(sht_df[k][0])
			except:
				x = sht_df[k][0]
			if isinstance(x, (int, str)):
				self.update_var(v, x)
			elif isinstance(x, (list, set, tuple)):
				self.update_var(v, "\n".join(x))
		#
		self.update_var('host-name', self['hostname'])		## duplicate entry for various support
		self.hostname = self['hostname']					## self.hostname for late access.


# ----------------------------------------------------------------------------------------------------

def get_hext2_3(ipaddr):
	"""get the hextate 2 and hextate 3 from given ipv6 ip address.
	--> tuple
	"""
	l = eval(ipaddr)
	if isinstance(l, (list, set, tuple)):
		try:
			v6 = IPv6(l[-1][:-2]+"/64")
			h2b = v6.get_hext(2) 
			h3b = v6.get_hext(3) 
			if h2b and h3b and h2b!='0'and h3b!='0':
				return (h2b, h3b)
			return ""
		except: 
			pass
	return ""

# ================================================================================================
# Interfaces Object common calls/methods class
# ================================================================================================
class TableInterfaces():

	@property
	def pdf_dict(self):
		return {'tables': self.pdf}
	
	## Calls


# ================================================================================================
# VRF Object common calls/methods class
# ================================================================================================
class TableVrfs():

	@property
	def pdf_dict(self):
		return {'vrf': self.vrf_df}		

	## Calls

	def update_column_names(self):
		"""rename vrf column name from ``name`` to ``vrf``"""
		self.vrf_df.rename(columns={'name': 'vrf',}, inplace=True)

	def drop_mtmt_vrf(self):
		"""drop rows where vrf is management vrf """
		self.vrf_df.drop(self.vrf_df[
				self.vrf_df["vrf"] == "Mgmt-vrf"
				].index, axis=0, inplace=True)

	def add_filter_col(self):
		"""add filter column for vrf"""
		self.vrf_df['filter'] = "vrf"

	def update_rt(self):
		"""update vrf route targets value from rd values"""
		self.vrf_df['vrf_route_target'] = self.vrf_df['default_rd'].apply(get_rt)

# ----------------------------------------------------------------------------------------------------
def get_rt(default_rd):
	"""get the route target number from rd value"""
	try:
		rt = default_rd.split(":")[-1]
		if rt != "<not set>":
			return rt
		else:
			return ""
	except: return ""

# ================================================================================================


__all__ = [
	'DataFrameInit', 'KeyExchanger', 
	'Var', 'TableInterfaces', 'TableVrfs', 
]