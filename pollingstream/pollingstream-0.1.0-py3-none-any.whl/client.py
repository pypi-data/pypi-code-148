import threading, json, requests, time

PROTOCOLV = "V1"

def nil(*args, **kwargs):
	return

class Client:
	sessionid = None
	sessiontoken = None
	pingthread = None
	evthread = None
	interval = None
	timeout = None
	uri = None
	disconnected = False
	events = {
		"connect": nil,
		"disconnect": nil,
		"message": nil
	}
	def __init__(self):
		pass
	def connect(self, uri, path=f"/PStream{PROTOCOLV}"):
		if uri.endswith("/"):
			uri = uri + path[1:]
		else:
			uri = uri + path
		self.uri = uri
		c = requests.post(uri+"/create_session")
		try:
			data = c.json()
			self.interval = data["interval"]
			self.timeout = data["timeout"]
			self.sessionid = data["id"]
			self.sessiontoken = data["token"]
		except:
			raise Exception("amogus")
		#self.pingthread = threading.Thread(target=self.ping,daemon=True)
		self.evthread = threading.Thread(target=self.evthread,daemon=True)
		self.evthread.start()
		self.events["connect"](self.sessionid,self.sessiontoken)
		self.ping()
	def send(self, msg):
		requests.post(self.uri+f'/msg?id={self.sessionid}&token={self.sessiontoken}&msg={msg}')
	def ping(self):
		while not self.disconnected:
			time.sleep(self.interval/1000)
			print(self.uri+f"/ping?id={self.sessionid}&token={self.sessiontoken}")
			r = requests.head(self.uri+f"/ping?id={self.sessionid}&token={self.sessiontoken}")
			print(r.text)
	def evthread(self):
		while not self.disconnected:
			ev = requests.get(self.uri+f'/event?id={self.sessionid}&token={self.sessiontoken}').text
			if ev.startswith("1"):
				self.events["message"](ev[1:])
			elif ev.startswith("-1"):
				self.events["disconnect"]()
				self.disconnected = True
	def event(self, func):
		if func.__name__ == "connect":
			self.events["connect"] = func
		elif func.__name__ == "disconnect":
			self.events["disconnect"] = func
		elif func.__name__ == "message":
			self.events["message"] = func
		#return wrapper
