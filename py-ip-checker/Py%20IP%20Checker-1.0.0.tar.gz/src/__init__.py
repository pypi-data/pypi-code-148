import requests as re

class IP:
	def __init__(self, ipi: str):
		try:
			r = re.get('https://ipwho.is/' + ipi).json()
			self.IP = r['ip']
			self.IPtype = r['type']
			self.continent = r['continent']
			self.continent_code = r['continent_code']
			self.country = r['country']
			self.country_code = r['country_code']
			self.region = r['region']
			self.region_code = r['region_code']
			self.city = r['city']
			self.lat = r['latitude']
			self.lon = r['longitude']
			self.postal = r['postal']
			self.calling_code = r['calling_code']
			self.capital = r['capital']
			self.borders = r['borders']
			self.emoji = r['flag']['emoji']
			self.emoji_unicode = r['flag']['emoji_unicode']
			self.connection_asn = r['connection']['asn']
			self.connection_org = r['connection']['org']
			self.connection_isp = r['connection']['isp']
			self.connection_domain = r['connection']['domain']
			self.timezone_id = r['timezone']['id']
			self.timezone_abbr = r['timezone']['abbr']
			self.timezone_offset = r['timezone']['offset']
			self.timezone_utc = r['timezone']['utc']
			self.current_time = r['timezone']['current_time']
		except Exception as ex:
			print('Python exception: ' + ex)