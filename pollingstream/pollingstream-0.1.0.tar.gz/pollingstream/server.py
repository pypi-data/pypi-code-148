import socket, threading, json, random, time

PROTOCOLV = "V1"

def _nil(*args, **kwargs):
	return

class Server:
	sessions = {}
	longpolqueue = {}
	pings = {}
	charset = "abcdefghijklmnopqrstuvwxyz"
	charset += charset.upper()
	
	events = {
		"connect": _nil,
		"disconnect": _nil,
		"message": _nil
	}
	serverthrd = None
	running = False
	def __init__(self,path=f"/PStream{PROTOCOLV}",ip="0.0.0.0",port=5000,interval=30000,timeout=60000):
		self.path = path
		self.ip = ip
		self.port = port
		self.interval = interval
		self.timeout = timeout

		self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
		self.s.bind((ip,port))
	def run(self):
		self.running = True
		self.serverthread()
	def stop(self):
		self.running = False
		self.serverthrd.stop()
		self.serverthrd = None
	def serverthread(self):
		self.s.listen(5)
		print(f"Started serving on IP {self.ip} Port {self.port}")
		while self.running:
			conn, addr = self.s.accept()
			threading.Thread(target=self.qhandler,args=(conn,addr,),daemon=True).start()
	def qhandler(self, conn, addr):
		req = conn.recv(8000).decode("utf-8")
		if req.startswith(f"POST {self.path}/create_session HTTP/1.1"):
			id = ""
			token = ""
			for i in range(16):
				id += random.choice(self.charset)
				token += random.choice(self.charset)
			obj = json.dumps({"token":token,"id":id,"interval":self.interval,"timeout":self.timeout})
			resp = b'HTTP/1.1 200 OK\nConnection: close\nContent-type: application/json\n\n'+obj.encode("utf-8")
			conn.send(resp)
			conn.close()
			self.longpolqueue[id] = []
			self.sessions[id] = token
			self.pings[id] = [threading.Thread(target=self.pingthread,args=(id,),daemon=True),False]
			self.pings[id][0].start()
			self.events["connect"](id,token)
		elif req.startswith(f"POST {self.path}/msg"):
			try:
				queryr = req.split("\n")[0].split("?")[1].split("&")
				query = {}
				for p in queryr:
					query[p.split("=")[0]] = p.split("=")[1].split(" HTTP/1.1")[0]
				id = query["id"]
				token = query["token"]
				msg = query["msg"]
				if not self.sessions[id] == token:
					raise Exception("amogus")
				self.events["message"](id,msg) # msg
				conn.send(b'HTTP/1.1 200 OK\nConnection: close\n\nOK')
				conn.close()
			except Exception as e:
				print(str(e))
				conn.send(b'HTTP/1.1 400 Bad Request')
				conn.close()
		elif req.split("\n")[0].split("?")[0].startswith(f"GET {self.path}/event"):
			try:
				queryr = req.split("\n")[0].split("?")[1].split("&")
				query = {}
				for p in queryr:
					query[p.split("=")[0]] = p.split("=")[1].split(" HTTP/1.1")[0]
				id = query["id"]
				token = query["token"]
				if not "-1" in self.longpolqueue[id]:
					if not self.sessions[id] == token:
						raise Exception("amogus")
			except:
				#print("bad req")
				conn.send(b'HTTP/1.1 400 Bad Request')
				conn.close()
				return
			# Authorization complete xdddzs
			while self.running:
				if len(self.longpolqueue[id])>0:
					self.longpolqueue[id].reverse()
					msg = self.longpolqueue[id].pop()
					self.longpolqueue[id].reverse()
					conn.send(b'HTTP/1.1 200 OK\nConnection: close\nContent-type: plain/text\n\n'+str(msg).encode("utf-8"))
					conn.close()
					break
		elif req.split("\n")[0].split("?")[0].startswith(f"HEAD {self.path}/ping"):
			try:
				queryr = req.split("\n")[0].split("?")[1].split("&")
				query = {}
				for p in queryr:
				#print(p)
					query[p.split("=")[0]] = p.split("=")[1].split(" HTTP/1.1")[0]
				id = query["id"]
				token = query["token"]
				if not self.sessions[id] == token:
					raise Exception("amogus")
				self.pings[id][1] = True
				conn.send(b'HTTP/1.1 200 OK\nConnection: close')
				conn.close()
			except Exception as e:
				print(str(e))
				conn.send(b'HTTP/1.1 400 Bad Request')
				conn.close()
				return
		else:
			conn.send(b'HTTP/1.1 404 Not Found\nConnection: close\n\n404 NOT FOUND') # cursed 404
			conn.close()
	def event(self, func):
		if func.__name__ == "connect":
			self.events["connect"] = func
		elif func.__name__ == "disconnect":
			self.events["disconnect"] = func
		elif func.__name__ == "message":
			self.events["message"] = func
	def disconnect(self,id):
		self.longpolqueue[id] = ["-1"]
		del self.sessions[id]
		del self.pings[id]
		self.events["disconnect"](id)
	def send(self,id,data):
		try:
			self.longpolqueue[id].append("1"+str(data))
			return True
		except:
			return False
	def pingthread(self,id):
		passed = 0
		while self.running:
			if not id in self.sessions:
				break
			time.sleep(1)
			passed += 1000
			if passed >= self.interval:
				if self.pings[id][1]:
					passed = 0
					self.pings[id][1] = False
			if passed == self.timeout:
				self.disconnect(id)
				break
