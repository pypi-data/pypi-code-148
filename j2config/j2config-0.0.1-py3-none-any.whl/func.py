"""helper functions/classes for jinja variables ( aka: filters )
"""


# import fields
from .cmn.common_fn import *
from nettoolkit import IPv4





class Vrf():
	"""device vrf/instances
	"""
	def __init__(self, table):
		self.table = table

	def __iter__(self):
		for key, data in self.table.items():
			if self.is_vrf(data): yield data

	@staticmethod
	def is_vrf(data):
		"""condition: `filter==vrf` """
		return data['filter'].lower() == 'vrf'

	def vrf_not_none(self):
		"""condition: `vrf is not None` """
		for key, data in self.table.items():
			if self.is_vrf(data) and data['vrf'] != "":
				yield data

	def sorted(self):
		"""list of available vrfs sorted by `vrf` field.
		--> list
		"""
		self.sorted_vrf = sorted([ _['vrf']  for _ in self.vrf_not_none() ])
		return  self.sorted_vrf

	def sorted_vpnids(self):
		"""list of available vrfs sorted by `vrf_vpnid` field.
		--> list
		"""
		self.sorted_vpnids = sorted([ int(_['vrf_vpnid'])  for _ in self.vrf_not_none() ])
		return self.sorted_vpnids

	def sorted_vrf_data(self):
		"""vrf data generator, sorted by vrf names
		--> slice of data
		"""
		for vrf in self.sorted_vrf:
			for data in self.vrf_not_none():
				if data['vrf'] == vrf: 
					yield data
					break

	def sorted_vrf_data_by_vpnid(self):
		"""vrf data generator, sorted by vpnids
		--> slice of data
		"""
		for vpnid in self.sorted_vpnids:
			for data in self.vrf_not_none():
				if int(data['vrf_vpnid']) == vpnid: 
					yield data
					break

	def vrf_get(self, vrf):
		"""get a particular vrf data
		--> slice of data
		"""
		for data in self.vrf_not_none():
			if data['vrf'] == vrf: 
				yield data




class Vlan():
	def __init__(self, table):
		self.table = table

	def __iter__(self):
		for key, data in self.table.items():
			if self.is_vlan(data): yield data

	@staticmethod
	def is_vlan(data):
		return data['filter'].lower() == 'vlan'


	def __vlans_range(self, start, stop):
		for data in self:
			if start <= int(data['int_number']) < stop:
				yield data

	def _sorted_vl_range(self, start, stop):
		vlans = [ int(data['int_number']) for data in self if start <= int(data['int_number']) < stop ]
		return vlans	

	def vlans_sorted_range(self, start, stop):
		for vlan in self._sorted_vl_range(start, stop):
			for data in self:
				if start <= int(data['int_number']) < stop:
					if int(data['int_number']) == vlan:
						yield data
						break

	def vlan(self, n):
		for data in self:
			if int(data['int_number']) == n:
				yield data
				break

	def of_instance(self, vrf):
		for data in self:
			if data and data['intvrf'] == vrf: yield data


class Bgp():
	def __init__(self, table):
		self.table = table

	def __iter__(self):
		for key, data in self.table.items():
			if self.is_bgp(data): yield data

	@staticmethod
	def is_bgp(data):
		return data['filter'].lower() == 'bgp'

	def vrf_not_none(self):
		for key, data in self.table.items():
			if self.is_bgp(data) and data['bgp_vrf'] != "":
				yield data

	def bgp_peers(self, vrf):
		for data in self:
			if data['bgp_vrf'] == vrf:
				yield data


class Physical():
	def __init__(self, table):
		self.table = table

	@staticmethod
	def is_physical(data):
		return data['filter'].lower() == 'physical'

	def __iter__(self):
		for key, data in self.table.items():
			if self.is_physical(data): yield data

	def sorted(self):
		return  sorted([ int(_['int_number'])  for _ in self ])

	def uplinks(self):
		for data in self:
			if data['int_filter'].lower().startswith('uplink'):
				yield data		

	def sorted_interfaces(self):
		for intf in self.sorted():
			for data in self:
				if int(data['int_number']) == intf:
					yield data
					break

	def interface(self, n):
		for data in self:
			if int(data['int_number']) == n:
				yield data
				break

	@staticmethod
	def interface_type(data, intf_type):
		return data['int_filter'].lower().startswith(intf_type)

	@staticmethod
	def interface_type_ends(data, x):
		return data['int_filter'].lower().endswith(x)


class Aggregated():
	def __init__(self, table):
		self.table = table

	def __iter__(self):
		for key, data in self.table.items():
			if self.is_aggregated(data): yield data

	@staticmethod
	def is_aggregated(data):
		return data['filter'].lower() == 'aggregated'


class Loopback():
	def __init__(self, table):
		self.table = table

	def __iter__(self):
		for key, data in self.table.items():
			if self.is_loopback(data): yield data

	@staticmethod
	def is_loopback(data):
		return data['filter'].lower() == 'loopback'



def sort(obj):
	return obj.sorted()

