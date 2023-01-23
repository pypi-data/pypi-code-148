"""cisco running-config system level command output parser """

# ------------------------------------------------------------------------------
from collections import OrderedDict
from .common import *

merge_dict = DIC.merge_dict
# ------------------------------------------------------------------------------

class RunningSystem():
	"""object for running config parser
	"""    	

	def __init__(self, cmd_op):
		"""initialize the object by providing the running config output

		Args:
			cmd_op (list, str): running config output, either list of multiline string
		"""    		
		self.cmd_op = verifid_output(cmd_op)
		self.system_dict = {}


	def system_bgp_as_number(self):
		"""get the device bgp as number
		""" 
		for l in self.cmd_op:
			if not l.startswith("router bgp "): continue
			return {'system_bgp_as_number': l.strip().split()[-1]}
		return {}


	def system_ca_certificate(self):
		"""get the device certificate hex values for cisco 9xxx and later series  switches.
		""" 
		ca_start, cert = False, ''
		for l in self.cmd_op:
			if l.strip().startswith("certificate ca 01"):
				ca_start = True
				continue
			if ca_start and l.strip().startswith("quit"):
				break
			if not ca_start: continue
			cert += l+'\n'
		return {'ca_certificate': cert.rstrip()}

	def system_tacacs_server(self):
		"""get list of tacacs server ips from aaa configurations
		"""
		servers, key, port, start = set(), '', '', False
		for l in self.cmd_op:
			spl = l.split()
			if l.startswith("tacacs-server host "):
				servers.add(spl[2])
			if l.startswith("tacacs-server ") and 'key' in spl:
				key = decrypt_type7(spl[spl.index('key')+1])
			if l.startswith("tacacs-server ") and 'port' in spl:
				port = spl[spl.index('port')+1]
			##
			if l.startswith("aaa group server tacacs"):
				start = True
			if start and l.startswith("!"):
				start = False
			if start:
				spl = l.strip().split()
				if spl[0] == 'server-private':
					servers.add(spl[1])
				if 'key' in spl:
					i = spl.index('key')
					if str(spl[i+1]) == '7':
						key = decrypt_type7(spl[i+2])
					else:
						key = spl[i+1]
				if 'port' in spl:
					port = spl[spl.index('key')+1]
		dic = {}
		for i, srv in enumerate(servers):
			dic['tacacs_server_' + str(i+1)] = srv
		dic['tacacs_key'] = key
		dic['tacacs_tcp_port'] = port
		return dic

	def system_name_server(self):
		"""get list of dns name server ips from configurations
		"""
		servers = set()
		for l in self.cmd_op:
			if l.startswith("ip name-server "):
				spl = l.split()
				for i, x in enumerate(spl):
					if i<2: continue
					servers.add(x)
		dic = {}
		for i, srv in enumerate(servers):
			dic['dns_server_' + str(i+1)] = srv
		return dic

	def system_syslog_server(self):
		"""get list of syslog server ips from configurations
		"""
		servers = set()
		for l in self.cmd_op:
			if l.startswith("logging host "):
				spl = l.split()
				for i, x in enumerate(spl):
					if i<2: continue
					servers.add(x)
		dic = {}
		for i, srv in enumerate(servers):
			dic['syslog_server_' + str(i+1)] = srv
		return dic

	def system_ntp_server(self):
		"""get list of ntp server ips from configurations
		"""
		servers = set()
		for l in self.cmd_op:
			if l.startswith("ntp server "):
				spl = l.split()
				for i, x in enumerate(spl):
					if i<2: continue
					servers.add(x)
		dic = {}
		for i, srv in enumerate(servers):
			dic['ntp_server_' + str(i+1)] = srv
		return dic



# ------------------------------------------------------------------------------


def get_system_running(cmd_op, *args):
	"""defines set of methods executions. to get various system parameters.
	uses RunningSystem in order to get all.

	Args:
		cmd_op (list, str): running config output, either list of multiline string

	Returns:
		dict: output dictionary with parsed with system fields
	"""
	R  = RunningSystem(cmd_op)
	R.system_dict.update(R.system_bgp_as_number())
	R.system_dict.update(R.system_ca_certificate())
	R.system_dict.update(R.system_tacacs_server())
	R.system_dict.update(R.system_name_server())
	R.system_dict.update(R.system_syslog_server())
	R.system_dict.update(R.system_ntp_server())


	# # update more interface related methods as needed.
	if not R.system_dict:
		R.system_dict['dummy_col'] = ""

	return R.system_dict

# ------------------------------------------------------------------------------

