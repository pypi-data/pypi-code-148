"""helper functions/classes for jinja variables ( aka: filters )
"""


# import fields
from .cmn.common_fn import *
from nettoolkit import IPv4





class Vrf():
	def __init__(self, table):
		self.table = table

	def __iter__(self):
		for key, data in self.table.items():
			if self.is_vrf(data): yield data

	@staticmethod
	def is_vrf(data):
		return data['filter'].lower() == 'vrf'

	def vrf_not_none(self):
		for key, data in self.table.items():
			if self.is_vrf(data) and data['vrf'] != "":
				yield data

	def sorted(self):
		self.sorted_vrf = sorted([ _['vrf']  for _ in self.vrf_not_none() ])
		return  self.sorted_vrf

	def sorted_vpnids(self):
		self.sorted_vpnids = sorted([ int(_['vrf_vpnid'])  for _ in self.vrf_not_none() ])
		return self.sorted_vpnids

	def sorted_vrf_data(self):
		for vrf in self.sorted_vrf:
			for data in self.vrf_not_none():
				if data['vrf'] == vrf: 
					yield data
					break

	def sorted_vrf_data_by_vpnid(self):
		for vpnid in self.sorted_vpnids:
			for data in self.vrf_not_none():
				if int(data['vrf_vpnid']) == vpnid: 
					yield data
					break

	def vrf_get(self, vrf):
		for data in self.vrf_not_none():
			if data['vrf'] == vrf: 
				yield data

	def vrf_route_xover_to_blue(self, *vrfs):
		if isinstance(vrfs, str): vrfs = [vrfs,]
		if not isinstance(vrfs, (list,set,tuple)):
			vrfs = [ _ for _ in vrfs ]
		for data in self.vrf_not_none():
			if data['vrf_route_xover_blue'].lower() == 'y' and data['vrf'] in vrfs:
				yield data

	def firewalled_vrf(self, *vrfs):
		if isinstance(vrfs, str): vrfs = [vrfs,]
		if not isinstance(vrfs, (list,set,tuple)):
			vrfs = [ _ for _ in vrfs ]
		for data in self.vrf_not_none():
			if data['vrf_route_xover_blue'].lower() != 'y' and data['vrf'] in vrfs:
				yield data

	def get_vrf_summary_entries(self):
		rm_vrf_summary = {}
		s = ''
		for vrf_data in self.sorted_vrf_data():
			if  vrf_data['vrf'] in ('acn.g1', 'ctv.g1', 'iot.g1', 'bms.g1', 'cio.a1'):
				rm_vrf_summary[vrf_data['vrf']] = vrf_data['vrf_route_xover_blue'].lower().startswith('y')
		for k, v in rm_vrf_summary.items():
			if v:
				s+=f"rm_vrf_summary_{k} "
		return s


	def get_security_to_blue_vrf_xover_rib_groups(self):
		rm_vrf_summary = {}
		s = ''
		for vrf_data in self.sorted_vrf_data():
			if  vrf_data['vrf'] in ('acn.g1', 'ctv.g1', 'iot.g1', 'bms.g1', 'cio.a1'):
				rm_vrf_summary[vrf_data['vrf']] = vrf_data['vrf_route_xover_blue'].lower().startswith('y')
		for k, v in rm_vrf_summary.items():
			if v:
				s+=f" {k}.inet.0"
		return s



class Vlan():
	def __init__(self, table):
		self.table = table

	def __iter__(self):
		for key, data in self.table.items():
			if self.is_vlan(data): yield data

	@staticmethod
	def is_vlan(data):
		return data['filter'].lower() == 'vlan'

	def vlan_between_2k_4k(self):
		for key, data in self.table.items():
			if self.is_vlan(data) and 2000 <= int(data['int_number']) < 4000:
				yield data

	def sorted_vl_range_2k_4k(self):
		return  sorted([ _['int_number']  for _ in self.vlan_between_2k_4k() ])

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

	def blue_peer(self, *peer):
		if isinstance(peer, str):
			peer = [peer, ]
		for data in self:
			if data['bgp_vrf'] == 'blue' and data['bgp_peergrp'] in peer:
				yield data

	def blue_peer_startswith(self, peer):
		for data in self:
			if data['bgp_vrf'] == 'blue' and data['bgp_peergrp'].startswith(peer):
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
	def is_l2_downlinks(data):
		return data['int_type'].lower() in ("vua", "vsa", "via", "vpb-non-mpls" ) 

	@staticmethod
	def is_l3_downlinks(data):
		return data['int_type'].lower() in ("vwb", "vpb" ) 

	@staticmethod
	def interface_type(data, intf_type):
		return data['int_filter'].lower().startswith(intf_type)

	@staticmethod
	def interface_type_ends(data, x):
		return data['int_filter'].lower().endswith(x)

	def get_ospf_to_bgp_non_mpls_export_list_entry(self):
		for phy_data in self:
			if phy_data['int_type'] == 'vpb-non-mpls':
				return "rm_ospf_to_bgp_blue "
		return ""


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

class Block():
	def __init__(self, table):
		self.table = table

	def __iter__(self):
		for key, data in self.table.items():
			if self.is_block(data): yield data

	@staticmethod
	def is_block(data):
		return data['filter'].lower() == 'block'

	def block_of(self, vrf, slot_type):
		for key, data in self.table.items():
			if isinstance(vrf, (str,int)) and isinstance(slot_type, str):
				if self.is_block(data) and data['block_vrf'] == vrf and data['slot_type'] == slot_type:
					yield data
			elif isinstance(vrf, (list,tuple,set)) and isinstance(slot_type, str):
				if self.is_block(data) and data['block_vrf'] in vrf and data['slot_type'] == slot_type:
					yield data
			elif isinstance(vrf, (str,int)) and isinstance(slot_type, (list,tuple,set)):
				if self.is_block(data) and data['block_vrf'] == vrf and data['slot_type'] in slot_type:
					yield data
			elif isinstance(vrf, (list,tuple,set)) and isinstance(slot_type, (list,tuple,set)):
				if self.is_block(data) and data['block_vrf'] in vrf and data['slot_type'] in slot_type:
					yield data
			else:
				print("Non matched data", data)

	def get_dslots(self):
		slots = {}
		for data in self.block_of('global', 'dslot'):
			slots['global_dslot'] = v4addressing(data['subnet'].split("/")[0]+'/27').n_thIP(0, withMask=True)
			break
		for data in self.block_of('blue', 'dslot'):
			slots['blue_dslot'] = v4addressing(data['subnet'].split("/")[0]+'/26').n_thIP(0, withMask=True)
			break
		for data in self.block_of('acc.y1', 'dslot'):
			slots['accy1_dslot'] = v4addressing(data['subnet'].split("/")[0]+'/27').n_thIP(0, withMask=True)
			break
		for data in self.block_of(('acn.g1', 'ctv.g1', 'iot.g1', 'bms.g1'), 'dslot'):
			slots[data['block_vpnid']+'_dslot'] = v4addressing(data['subnet'].split("/")[0]+'/27').n_thIP(0, withMask=True)
		return slots


class Summaries():
	def __init__(self, table):
		self.table = table
		self.aggregated = True 								## make False if individual subnets require instead of summary

	def __get_summaries_from_vrf(self, vrf):
		subnets_list = []
		_Vrf_summaries = Vrf(self.table)
		for vrf_data in _Vrf_summaries.vrf_not_none():
			if vrf_data['vrf'] == vrf:				
				if vrf_data['vrf_summaries'] != "":
					subnets_list.extend(str_to_list(vrf_data['vrf_summaries']))
		##
		_Block_summaries = Block(self.table)
		for blk_data in _Block_summaries.block_of(vrf, ('summary', 'infra',)):
			if blk_data['subnet'] != "":
				subnets_list.extend(str_to_list(blk_data['subnet']))

		return subnets_list

	def __get_summaries_from_vlans(self, vrf):
		subnets_list = []
		_Vlan_summaries = Vlan(self.table)
		for data in _Vlan_summaries.vlans_sorted_range(1600, 4000):
			if data['intvrf'] == vrf:
				if data['subnet'] != "" : subnets_list.append(IPv4(data['subnet']).n_thIP(0, withMask=True))
		return subnets_list

	def get_summaries_for_vrf(self, vrf):
		subnets_list = self.__get_summaries_from_vrf(vrf)
		subnets_list.extend(self.__get_summaries_from_vlans(vrf))
		if self.aggregated:
			return get_summaries(subnets_list)
		else: 
			return subnets_list

	def get_all_vrf_summaries(self):
		aggregates = {}
		_Vrf_summaries = Vrf(self.table)
		for vrf_data in _Vrf_summaries.vrf_not_none():
			aggregates[vrf_data['vrf']] = self.get_summaries_for_vrf(vrf_data['vrf'])
		return aggregates


	def blue_crossover_aggregates(self):
		rl_vrf_pfxs = {}
		for vrf_data in Vrf(self.table):
			if vrf_data['vrf_route_xover_blue'].lower().startswith('y'):
				rl_vrf_pfxs[vrf_data['vrf']] = self.get_summaries_for_vrf(vrf_data['vrf'])
		return rl_vrf_pfxs



def sort(obj):
	return obj.sorted()

