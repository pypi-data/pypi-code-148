from re import findall
from pathlib import Path
from random import randint, choice
from json import loads, dumps, JSONDecodeError
from requests import post,get
from rubika.encryption import encryption
import datetime
import time
import urllib
import sys
from urllib import request,parse

class accesses:
	class admin:
		pin               = "PinMessages"
		newAdmin          = "SetAdmin"
		editInfo          = "ChangeInfo"
		banMember         = "BanMember"
		changeLink        = "SetJoinLink"
		editMembersAccess = "SetMemberAccess"
		deleteMessages    = "DeleteGlobalAllMessages"

	class user:
		viewMembers = "ViewMembers"
		viewAdmins  = "ViewAdmins"
		sendMessage = "SendMessages"
		addMember   = "AddMember"

class clients:
	web = {
		"app_name"    : "Main",
		"app_version" : "4.0.7",
		"platform"    : "Web",
		"package"     : "web.rubika.ir",
		"lang_code"   : "fa"
	}

	android = {
		"app_name"    : "Main",
		"app_version" : "2.8.1",
		"platform"    : "Android",
		"package"     : "ir.resaneh1.iptv",
		"lang_code"   : "fa"
	}

address_MTN = [
			'https://messengerg2c26.iranlms.ir',
			"https://messengerg2c33.iranlms.ir",
			'https://messengerg2c22.iranlms.ir',
			'https://messengerg2c55.iranlms.ir',
			'https://messengerg2c57.iranlms.ir',
			'https://messengerg2c15.iranlms.ir',
			'https://messengerg2c16.iranlms.ir',
			'https://messengerg2c46.iranlms.ir' ,
			'https://messengerg2c39.iranlms.ir',
			'https://messengerg2c40.iranlms.ir',
			'https://messengerg2c41.iranlms.ir',
			'https://messengerg2c6.iranlms.ir',
			'https://messengerg2c7.iranlms.ir',
			'https://messengerg2c63.iranlms.ir',
			'https://messengerg2c31.iranlms.ir',
			'https://messengerg2c3.iranlms.ir'
			]

address_FILE = [
			'https://messengerg2c26.iranlms.ir',
			'https://messengerg2c39.iranlms.ir',
			'https://messengerg2c7.iranlms.ir',
			'https://messengerg2c17.iranlms.ir',
			'https://messengerg2c46.iranlms.ir'
			]

address_POLL = [
			'https://messengerg2c13.iranlms.ir',
			'https://messengerg2c26.iranlms.ir'
			]

def print_slow(str):
	for letter in str:
		sys.stdout.write(letter)
		sys.stdout.flush()
		time.sleep(0.03)

BIPurple="\033[1;95m"
red="\[\033[0;31m\]"
yellow="\033[0;33m"
green='\033[32m'
purple="\033[0;35m"
blue="\[\033[0;34m\]"
darkblue = '\033[34m'
bluo_p = '\033[44m'
pink_p = '\033[45m'
white = '\033[00m'
BICyan="\033[1;96m"
BGreen="\033[1;32m"
BWhite="\033[1;37m"
BYellow="\033[1;33m"

print_slow(f"\n{BICyan}    BeLectron {BWhite}Library {BGreen} Version 2.2.1\n    Copyright © 2023 {BIPurple}BeL BoT {BWhite}{bluo_p}< rubika.ir/BeL_BoT >\n\n{white}{BWhite}    Activating{BYellow} please be patient . . . ")
print(f"{BWhite}")

__BeLectron__ = "BeLectron BoT"

class Token:
	def __init__( self, auth ,app_name =__BeLectron__, displayWelcome = True ):
		if displayWelcome : print(f"")
		self.auth = auth
		self.enc = encryption(auth)

	@staticmethod
	def _getURL():
		return choice(address_MTN)

	@staticmethod
	def _SendFile():
		return choice(address_FILE)

	@staticmethod
	def _SendPoll():
		return choice(address_POLL)


	@staticmethod
	def _parse(mode:str, text:str):
		results = []
		if mode.upper() == "HTML":
			realText = text.replace("<b>","").replace("</b>","").replace("<i>","").replace("</i>","").replace("<pre>","").replace("</pre>","")
			bolds = findall("<b>(.*?)</b>",text)
			italics = findall("<i>(.*?)</i>",text)
			monos = findall("<pre>(.*?)</pre>",text)

			bResult = [realText.index(i) for i in bolds]
			iResult = [realText.index(i) for i in italics]
			mResult = [realText.index(i) for i in monos]

			for bIndex,bWord in zip(bResult,bolds):
				results.append({
					"from_index": bIndex,
					"length": len(bWord),
					"type": "Bold"
				})
			for iIndex,iWord in zip(iResult,italics):
				results.append({
					"from_index": iIndex,
					"length": len(iWord),
					"type": "Italic"
				})
			for mIndex,mWord in zip(mResult,monos):
				results.append({
					"from_index": mIndex,
					"length": len(mWord),
					"type": "Mono"
				})

		elif mode.lower() == "markdown":
			realText = text.replace("**","").replace("__","").replace("`","")
			bolds = findall(r"\*\*(.*?)\*\*",text)
			italics = findall(r"\_\_(.*?)\_\_",text)
			monos = findall("`(.*?)`",text)

			bResult = [realText.index(i) for i in bolds]
			iResult = [realText.index(i) for i in italics]
			mResult = [realText.index(i) for i in monos]

			for bIndex,bWord in zip(bResult,bolds):
				results.append({
					"from_index": bIndex,
					"length": len(bWord),
					"type": "Bold"
				})
			for iIndex,iWord in zip(iResult,italics):
				results.append({
					"from_index": iIndex,
					"length": len(iWord),
					"type": "Italic"
				})
			for mIndex,mWord in zip(mResult,monos):
				results.append({
					"from_index": mIndex,
					"length": len(mWord),
					"type": "Mono"
				})

		return results

	def _requestSendFile(self, file):
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"requestSendFile",
			"input":{
				"file_name": str(file.split("/")[-1]),
				"mime": file.split(".")[-1],
				"size": Path(file).stat().st_size
			},
			"client": clients.web
		}))},url=Token._SendFile()).json()["data_enc"]))["data"]

	def _uploadFile(self, file):
		if not "http" in file:
			frequest = Token._requestSendFile(self, file)
			bytef = open(file,"rb").read()

			hash_send = frequest["access_hash_send"]
			file_id = frequest["id"]
			url = frequest["upload_url"]

			header = {
				'auth':self.auth,
				'Host':url.replace("https://","").replace("/UploadFile.ashx",""),
				'chunk-size':str(Path(file).stat().st_size),
				'file-id':str(file_id),
				'access-hash-send':hash_send,
				"content-type": "application/octet-stream",
				"content-length": str(Path(file).stat().st_size),
				"accept-encoding": "gzip",
				"user-agent": "okhttp/3.12.1"
			}

			if len(bytef) <= 131072:
				header["part-number"], header["total-part"] = "1","1"

				while True:
					try:
						j = post(data=bytef,url=url,headers=header).text
						j = loads(j)['data']['access_hash_rec']
						break
					except Exception as e:
						continue

				return [frequest, j]
			else:
				t = round(len(bytef) / 131072 + 1)
				for i in range(1,t+1):
					if i != t:
						k = i - 1
						k = k * 131072
						while True:
							try:
								header["chunk-size"], header["part-number"], header["total-part"] = "131072", str(i),str(t)
								o = post(data=bytef[k:k + 131072],url=url,headers=header).text
								o = loads(o)['data']
								break
							except Exception as e:
								continue
					else:
						k = i - 1
						k = k * 131072
						while True:
							try:
								header["chunk-size"], header["part-number"], header["total-part"] = str(len(bytef[k:])), str(i),str(t)
								p = post(data=bytef[k:],url=url,headers=header).text
								p = loads(p)['data']['access_hash_rec']
								break
							except Exception as e:
								continue
						return [frequest, p]
		else:
			frequest = loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
				"method":"requestSendFile",
				"input":{
					"file_name": file.split("/")[-1],
					"mime": file.split(".")[-1],
					"size": len(get(file).content)
				},
				"client": clients.web
			}))},url=Token._SendFile()).json()["data_enc"]))["data"]

			hash_send = frequest["access_hash_send"]
			file_id = frequest["id"]
			url = frequest["upload_url"]
			bytef = get(file).content

			header = {
				'auth':self.auth,
				'Host':url.replace("https://","").replace("/UploadFile.ashx",""),
				'chunk-size':str(len(get(file).content)),
				'file-id':str(file_id),
				'access-hash-send':hash_send,
				"content-type": "application/octet-stream",
				"content-length": str(len(get(file).content)),
				"accept-encoding": "gzip",
				"user-agent": "okhttp/3.12.1"
			}

			if len(bytef) <= 131072:
				header["part-number"], header["total-part"] = "1","1"

				while True:
					try:
						j = post(data=bytef,url=url,headers=header).text
						j = loads(j)['data']['access_hash_rec']
						break
					except Exception as e:
						continue

				return [frequest, j]
			else:
				t = round(len(bytef) / 131072 + 1)
				for i in range(1,t+1):
					if i != t:
						k = i - 1
						k = k * 131072
						while True:
							try:
								header["chunk-size"], header["part-number"], header["total-part"] = "131072", str(i),str(t)
								o = post(data=bytef[k:k + 131072],url=url,headers=header).text
								o = loads(o)['data']
								break
							except Exception as e:
								continue
					else:
						k = i - 1
						k = k * 131072
						while True:
							try:
								header["chunk-size"], header["part-number"], header["total-part"] = str(len(bytef[k:])), str(i),str(t)
								p = post(data=bytef[k:],url=url,headers=header).text
								p = loads(p)['data']['access_hash_rec']
								break
							except Exception as e:
								continue
						return [frequest, p]

	@staticmethod
	def _getThumbInline(image_bytes:bytes):
		import io, base64, PIL.Image
		im = PIL.Image.open(io.BytesIO(image_bytes))
		width, height = im.size
		if height > width:
			new_height = 40
			new_width  = round(new_height * width / height)
		else:
			new_width  = 40
			new_height = round(new_width * height / width)
		im = im.resize((new_width, new_height), PIL.Image.ANTIALIAS)
		changed_image = io.BytesIO()
		im.save(changed_image, format='PNG')
		changed_image = changed_image.getvalue()
		return base64.b64encode(changed_image)

	@staticmethod
	def _getImageSize(image_bytes:bytes):
		import io, PIL.Image
		im = PIL.Image.open(io.BytesIO(image_bytes))
		width, height = im.size
		return [width , height]

	def getChats(self, start_id=None):
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"getChats",
			"input":{
				"start_id":start_id
			},
			"client": clients.web
		}))},url=Token._getURL()).json()["data_enc"]))

	def sendMessage(self, chat_id, text, metadata=[], parse_mode=None, message_id=None):
		inData = {
			"method":"sendMessage",
			"input":{
				"object_guid":chat_id,
				"rnd":f"{randint(100000,999999999)}",
				"text":text,
				"reply_to_message_id":message_id
			},
			"client": clients.web
		}
		if metadata != [] : inData["input"]["metadata"] = {"meta_data_parts":metadata}
		if parse_mode != None :
			inData["input"]["metadata"] = {"meta_data_parts":Token._parse(parse_mode, text)}
			inData["input"]["text"] = text.replace("<b>","").replace("</b>","").replace("<i>","").replace("</i>","").replace("<pre>","").replace("</pre>","") if parse_mode.upper() == "HTML" else text.replace("**","").replace("__","").replace("`","")

		while 1:
			try:
				return loads(self.enc.decrypt(loads(request.urlopen(request.Request(Token._getURL(), data=dumps({"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps(inData))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc')))
				break
			except: continue


	def editMessage(self, gap_guid, newText, message_id):
		inData = {
			"method":"editMessage",
			"input":{
				"message_id":message_id,
				"object_guid":gap_guid,
				"text":newText,
			},
			"client": clients.web
		}

		while 1:
			try:
				return loads(self.enc.decrypt(loads(request.urlopen(request.Request(Token._getURL(), data=dumps({"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps(inData))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc')))
				break
			except: continue



	def deleteMessages(self, chat_id, message_ids):
		inData = {
			"method":"deleteMessages",
			"input":{
				"object_guid":chat_id,
				"message_ids":message_ids,
				"type":"Global"
			},
			"client": clients.web
		}

		while 1:
			try:
				return loads(self.enc.decrypt(loads(request.urlopen(request.Request(Token._getURL(), data=dumps({"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps(inData))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc')))
				break
			except: continue

	def getUserInfo(self, chat_id):
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"getUserInfo",
			"input":{
				"user_guid":chat_id
			},
			"client": clients.web
		}))},url=Token._getURL()).json()["data_enc"]))
	
	def getBlockedUsers(self):
		return self.methods.methodsRubika("json",methode ="getBlockedUsers",indata = {},wn = clien.web)
	
	def Infolinkpost(self,linkpost):
		return self.methods.methodsRubika("json",methode ="getLinkFromAppUrl",indata = {"app_url": linkpost},wn = clien.web)


	def getMessages(self, chat_id,min_id):
		inData = {
		    "method":"getMessagesInterval",
		    "input":{
		        "object_guid":chat_id,
		        "middle_message_id":min_id
		    },
		    "client": clients.web
		}

		while 1:
			try:
				return loads(self.enc.decrypt(loads(request.urlopen(request.Request(Token._getURL(), data=dumps({"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps(inData))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc'))).get("data").get("messages")
				break
			except: continue


	def deleteUserChat(self, user_guid, last_message):
		inData = {
		    "method":"deleteUserChat",
		    "input":{
		        "last_deleted_message_id":last_message,
		        "user_guid":user_guid
		    },
		    "client": clients.web
		}

		while 1:
			try:
				return loads(self.enc.decrypt(loads(request.urlopen(request.Request(Token._getURL(), data=dumps({"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps(inData))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc')))
				break
			except: continue

	def getInfoByUsername(self, username):
		''' username should be without @ '''
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"getObjectByUsername",
			"input":{
				"username":username
			},
			"client": clients.web
		}))},url=Token._getURL()).json().get("data_enc")))

	def banGroupMember(self, chat_id, user_id):
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"banGroupMember",
			"input":{
				"group_guid": chat_id,
				"member_guid": user_id,
				"action":"Set"
			},
			"client": clients.web
		}))},url=Token._getURL()).json()["data_enc"]))

	def unbanGroupMember(self, chat_id, user_id):
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"client": clients.android,
			"input":{
				"group_guid": chat_id,
				"member_guid": user_id,
				"action":"Unset"
			},
			"method":"banGroupMember"
		}))},url=Token._getURL()).json()["data_enc"]))

	def invite(self, chat_id, user_ids):
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"addGroupMembers",
			"input":{
				"group_guid": chat_id,
				"member_guids": user_ids
			},
			"client": clients.web
		}))},url=Token._getURL()).json()["data_enc"]))

	def inviteChannel(self, chat_id, user_ids):
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"addChannelMembers",
			"input":{
				"channel_guid": chat_id,
				"member_guids": user_ids
			},
			"client": clients.web
		}))},url=Token._getURL()).json()["data_enc"]))



	def getGroupAdmins(self, chat_id):
		inData = {
			"method":"getGroupAdminMembers",
			"input":{
				"group_guid":chat_id
			},
			"client": clients.android
		}

		while 1:
			try:
				return loads(self.enc.decrypt(loads(request.urlopen(request.Request(Token._getURL(), data=dumps({"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps(inData))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc')))
				break
			except: continue



	def getChannelInfo(self, channel_guid):
		inData = {
			"method":"getChannelInfo",
			"input":{
				"channel_guid":channel_guid
			},
			"client": clients.android
		}

		while 1:
			try:
				return loads(self.enc.decrypt(loads(request.urlopen(request.Request(Token._getURL(), data=dumps({"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps(inData))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc')))
				break
			except: continue


	def ADD_NumberPhone(self, first_num, last_num, numberPhone):
		inData = {
			"method":"addAddressBook",
			"input":{
				"first_name":first_num,
				"last_name":last_num,
				"phone":numberPhone
			},
			"client": clients.android
		}

		while 1:
			try:
				return loads(self.enc.decrypt(loads(request.urlopen(request.Request(Token._getURL(), data=dumps({"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps(inData))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc')))
				break
			except: continue



	def getMessagesInfo(self, chat_id, message_ids):
		inData = {
			"method":"getMessagesByID",
			"input":{
				"object_guid": chat_id,
				"message_ids": message_ids
			},
			"client": clients.web
		}

		while 1:
			try:
				return loads(self.enc.decrypt(loads(request.urlopen(request.Request(Token._getURL(), data=dumps({"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps(inData))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc'))).get("data").get("messages")
				break
			except: continue

	def setMembersAccess(self, chat_id, access_list):
		return post(json={
			"api_version": "4",
			"auth": self.auth,
			"client": clients.android,
			"data_enc": self.enc.encrypt(dumps({
				"access_list": access_list,
				"group_guid": chat_id
			})),
			"method": "setGroupDefaultAccess"
		}, url=Token._getURL())

	def getGroupMembers(self, chat_id, start_id=None):
		return loads(self.enc.decrypt(post(json={
			"api_version":"5",
				"auth": self.auth,
				"data_enc": self.enc.encrypt(dumps({
					"method":"getGroupAllMembers",
					"input":{
						"group_guid": chat_id,
						"start_id": start_id
					},
					"client": clients.web
			}))
		}, url=Token._getURL()).json()["data_enc"]))


	def getGroupMembers(self, chat_id, start_id=None):
		return loads(self.enc.decrypt(post(json={
			"api_version":"5",
				"auth": self.auth,
				"data_enc": self.enc.encrypt(dumps({
					"method":"getGroupAllMembers",
					"input":{
						"group_guid": chat_id,
						"start_id": start_id
					},
					"client": clients.web
			}))
		}, url=Token._getURL()).json()["data_enc"]))

	def getGroupInfo(self, chat_id):
		return loads(self.enc.decrypt(post(
			json={
				"api_version":"5",
				"auth": self.auth,
				"data_enc": self.enc.encrypt(dumps({
					"method":"getGroupInfo",
					"input":{
						"group_guid": chat_id,
					},
					"client": clients.web
			}))}, url=Token._getURL()).json()["data_enc"]))

	def getGroupLink(self, chat_id):
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"getGroupLink",
			"input":{
				"group_guid":chat_id
			},
			"client": clients.web
		}))},url=Token._getURL()).json().get("data_enc"))).get("data").get("join_link")

	def changeGroupLink(self, chat_id):
		return loads(self.enc.decrypt(post(json={
			"api_version":"4",
			"auth":self.auth,
			"client": clients.android,
			"data_enc":self.enc.encrypt(dumps({
				"group_guid": chat_id
			})),
			"method":"setGroupLink",
		},url=Token._getURL()).json()["data_enc"]))

	def setGroupTimer(self, chat_id, time):
		return loads(self.enc.decrypt(post(json={
			"api_version":"4",
			"auth":self.auth,
			"client": clients.android,
			"data_enc":self.enc.encrypt(dumps({
				"group_guid": chat_id,
				"slow_mode": time,
				"updated_parameters":["slow_mode"]
			})),
			"method":"editGroupInfo"
		},url=Token._getURL()).json()["data_enc"]))

	def setGroupAdmin(self, chat_id, user_id):
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"setGroupAdmin",
			"input":{
				"group_guid": chat_id,
				"access_list":["PinMessages","DeleteGlobalAllMessages","BanMember","SetMemberAccess"],
				"action": "SetAdmin",
				"member_guid": user_id
			},
			"client": clients.android
		}))},url=Token._getURL()).json()["data_enc"]))

	def setChannelAdmin(self, chat_id, user_id, access_list=[]):
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"setChannelAdmin",
			"input":{
				"group_guid": chat_id,
				"access_list": access_list,
				"action": "SetAdmin",
				"member_guid": user_id
			},
			"client": clients.android
		}))},url=Token._getURL()).json()["data_enc"]))
	
	def deleteChannelAdmin(self,guid_channel,guid_admin):
	       return self.methods.methodsRubika("json",methode ="setChannelAdmin",indata = {"channel_guid": guid_channel,"action": "UnsetAdmin","member_guid": guid_admin},wn = clien.android)
        
	def deleteGroupAdmin(self, chat_id, user_id):
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"setGroupAdmin",
			"input":{
				"group_guid": chat_id,
				"action": "UnsetAdmin",
				"member_guid": user_id
			},
			"client": clients.android
		}))},url=Token._getURL()).json()["data_enc"]))

	def logout(self):
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"logout",
			"input":{},
			"client": clients.web
		}))},url=Token._getURL()).json()["data_enc"]))


	def forwardMessages(self, From, message_ids, to):
		inData = {
			"method":"forwardMessages",
			"input":{
				"from_object_guid": From,
				"message_ids": message_ids,
				"rnd": f"{randint(100000,999999999)}",
				"to_object_guid": to
			},
			"client": clients.web
		}

		while 1:
			try:
				return loads(self.enc.decrypt(loads(request.urlopen(request.Request(Token._getURL(), data=dumps({"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps(inData))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc')))
				break
			except: continue

	def getStickersByEmoji(self,emojee):
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"getStickersByEmoji",
			"input":{
				"emoji_character": emojee,
				"suggest_by": "All"
			},
			"client": clients.web
		}))},url=Token._getURL()).json()["data_enc"]))

	def setActionChatun(self,guid):
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"setActionChat",
			"input":{
				"action": "Unmute",
				"object_guid": guid
			},
			"client": clients.web
		}))},url=Token._getURL()).json()["data_enc"]))

	def setActionChatmut(self,guid):
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"setActionChat",
			"input":{
				"action": "Mute",
				"object_guid": guid
			},
			"client": clients.web
		}))},url=Token._getURL()).json()["data_enc"]))

	def chatGroupvisit(self,guid,visiblemsg):
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"editGroupInfo",
			"input":{
				"chat_history_for_new_members": "Visible",
				"group_guid": guid,
				"updated_parameters": visiblemsg
			},
			"client": clients.web
		}))},url=Token._getURL()).json()["data_enc"]))

	def sendPoll(self,guid,SOAL,LIST):
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"createPoll",
			"input":{
				"allows_multiple_answers": "false",
				"is_anonymous": "true",
				"object_guid": guid,
				"options":LIST,
				"question":SOAL,
				"rnd":f"{randint(100000,999999999)}",
				"type":"Regular"
			},
			"client": clients.web
		}))},url=Token._SendPoll()).json()["data_enc"]))

	def chatGrouphidden(self,guid,hiddenmsg):
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"editGroupInfo",
			"input":{
				"chat_history_for_new_members": "Hidden",
				"group_guid": guid,
				"updated_parameters": hiddenmsg
			},
			"client": clients.web
		}))},url=Token._getURL()).json()["data_enc"]))

	def seenChats(self, seenList):
		# seenList must be a dict , keys are object guids and values are last message’s id, {"guid":"msg_id"}
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"seenChats",
			"input":{
				"seen_list": seenList
			},
			"client": clients.web
		}))},url=Token._getURL()).json()["data_enc"]))

	def sendChatAction(self, chat_id, action):
		#every some seconds before sending message this request should send
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"sendChatActivity",
			"input":{
				"activity": action,
				"object_guid": chat_id
			},
			"client": clients.web
		}))},url=Token._getURL()).json()["data_enc"]))
	
	def HideChatGroup(self,guid,hiddenmsg):
	       return self.methods.methodsRubika("json",methode ="editGroupInfo",indata = {"chat_history_for_new_members": "Hidden","group_guid": guid_gap,"updated_parameters": hiddenmsg},wn = clien.web)
        
	def pin(self, chat_id, message_id):
		return loads(self.enc.decrypt(post(json={"api_version": "4", "auth": self.auth, "client": clients.android,
			 "data_enc": self.enc.encrypt(dumps({
			 	"action":"Pin",
			 	"message_id": message_id,
			 	"object_guid": chat_id
			 })),
			"method": "setPinMessage"
		},url=Token._getURL())))

	def unpin(self, chat_id, message_id):
		return loads(self.enc.decrypt(post(json={"api_version": "4", "auth": self.auth, "client": clients.android,
			 "data_enc": self.enc.encrypt(dumps({
			 	"action":"Unpin",
			 	"message_id": message_id,
			 	"object_guid": chat_id
			 })),
			"method": "setPinMessage"
		},url=Token._getURL()).json()["data_enc"]))

	def joinGroup(self, link):
		hashLink = link.split("/")[-1]
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"joinGroup",
			"input":{
				"hash_link": hashLink
			},
			"client": clients.web
		}))},url=Token._getURL()).json()["data_enc"]))

	def joinChannel(self, link):
		hashLink = link.split("/")[-1]
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"joinChannelByLink",
			"input":{
				"hash_link": hashLink
			},
			"client": clients.web
		}))},url=Token._getURL()).json()["data_enc"]))

	def groupPreviewByJoinLink(self, link):
		hashLink = link.split("/")[-1]
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"groupPreviewByJoinLink",
			"input":{
				"hash_link": hashLink
			},
			"client": clients.web
		}))},url=Token._getURL()).json()["data_enc"]))["data"]
		
	def deleteChatHistory(self, group,msg_id):
		inData = {
			"method":"deleteChatHistory",
			"input":{
				"last_message_id": msg_id,
				"object_guid": group
			},
			"client": clients.web
		}

		while 1:
			try:
				return loads(self.enc.decrypt(loads(request.urlopen(request.Request(Token._getURL(), data=dumps({"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps(inData))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc')))
				break
			except: continue
	
	def Postion(self,guid,guiduser):
		return self.methods.methodsRubika("json",methode ="requestChangeObjectOwner",indata = {"object_guid": guid,"new_owner_user_guid": guiduser},wn = clien.android)
		
	def getPostion(self,guid):
		return self.methods.methodsRubika("json",methode ="getPendingObjectOwner",indata = {"object_guid": guid},wn = clien.android)

	def leaveGroup(self, chat_id):
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"leaveGroup",
			"input":{
				"group_guid": chat_id
			},
			"client": clients.web
		}))},url=Token._getURL()).json()["data_enc"]))
	
	def editnameGroup(self,groupgu,namegp,biogp):
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"editGroupInfo",
			"input":{
				"description": biogp,
				"group_guid": groupgu,
				"title":namegp,
				"updated_parameters":["title","description"]
			},
			"client": clients.web
		}))},url=Token._getURL()).json()["data_enc"]))

	def editbioGroup(self,groupgu,biogp,namegp):
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"editGroupInfo",
			"input":{
				"description": biogp,
				"group_guid": groupgu,
				"title":namegp,
				"updated_parameters":["title","description"]
			},
			"client": clients.web
		}))},url=Token._getURL()).json()["data_enc"]))

	def joinChannelByID(self, chat_id):
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"joinChannelAction",
			"input":{
				"action": "Join",
				"channel_guid": chat_id
			},
			"client": clients.web
		}))},url=Token._getURL()).json()["data_enc"]))

	def LeaveChannel(self, chat_id):
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"joinChannelAction",
			"input":{
				"action": "Leave",
				"channel_guid": chat_id
			},
			"client": clients.web
		}))},url=Token._getURL()).json()["data_enc"]))

	def block(self, chat_id):
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"setBlockUser",
			"input":{
				"action": "Block",
				"user_guid": chat_id
			},
			"client": clients.web
		}))},url=Token._getURL()).json()["data_enc"]))

	def unblock(self, chat_id):
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"setBlockUser",
			"input":{
				"action": "Unblock",
				"user_guid": chat_id
			},
			"client": clients.web
		}))},url=Token._getURL()).json()["data_enc"]))

	def sendPhoto(self, chat_id, file, size=[], thumbnail=None, caption=None, message_id=None):
		uresponse = Token._uploadFile(self, file)
		if thumbnail == None: thumbnail = "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"
		elif "." in thumbnail:thumbnail = str(Token._getThumbInline(open(file,"rb").read() if not "http" in file else get(file).content))

		if size == []: size = Token._getImageSize(open(file,"rb").read() if not "http" in file else get(file).content)

		file_inline = {
			"dc_id": uresponse[0]["dc_id"],
			"file_id": uresponse[0]["id"],
			"type":"Image",
			"file_name": file.split("/")[-1],
			"size": str(len(get(file).content if "http" in file else open(file,"rb").read())),
			"mime": file.split(".")[-1],
			"access_hash_rec": uresponse[1],
			"width": size[0],
			"height": size[1],
			"thumb_inline": thumbnail
		}
		inData = {
				"method":"sendMessage",
				"input":{
					"file_inline": file_inline,
					"object_guid": chat_id,
					"rnd": f"{randint(100000,999999999)}",
					"reply_to_message_id": message_id
				},
				"client": clients.web
			}
		if caption != None: inData["input"]["text"] = caption


		while 1:
			try:
				return loads(self.enc.decrypt(loads(request.urlopen(request.Request(Token._SendFile(), data=dumps({"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps(inData))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc')))
				break
			except: continue


	def sendVoice(self, chat_id, file, time, caption=None, message_id=None):
		# file's format must be ogg. time must be ms (type: float). 
		uresponse = Token._uploadFile(self, file)
		inData = {
				"method":"sendMessage",
				"input":{
					"file_inline": {
						"dc_id": uresponse[0]["dc_id"],
						"file_id": uresponse[0]["id"],
						"type":"Voice",
						"file_name": file.split("/")[-1],
						"size": str(len(get(file).content if "http" in file else open(file,"rb").read())),
						"time": time,
						"mime": file.split(".")[-1],
						"access_hash_rec": uresponse[1],
					},
					"object_guid":chat_id,
					"rnd":f"{randint(100000,999999999)}",
					"reply_to_message_id":message_id
				},
				"client": clients.web
			}

		if caption != None: inData["input"]["text"] = caption


		while 1:
			try:
				return loads(self.enc.decrypt(loads(request.urlopen(request.Request(Token._SendFile(), data=dumps({"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps(inData))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc')))
				break
			except: continue


	def sendVideo(guid_GAP, file, caption=None, message_id=None):
		uresponse = Token._uploadFile(self, file)
		
		thumbnail = "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"
		file_id = str(uresponse[0]["id"])
		mime = file.split(".")[-1]
		dc_id = uresponse[0]["dc_id"]
		access_hash_rec = uresponse[1]
		file_name = file.split("/")[-1]
		size = str(len(get(file).content if "http" in file else open(file,"rb").read()))

		inData = {
			"method":"sendMessage",
			"input":{
				"object_guid":guid_GAP,
				"reply_to_message_id":message_id,
				"rnd":f"{randint(100000,999999999)}",
				"file_inline":{
					"access_hash_rec":access_hash_rec,
					"auto_play":False,
					"dc_id":dc_id,
					"file_id":file_id,
					"file_name":file_name,
					"height":426,
					"mime":mime,
					"size":size,
					"thumb_inline":thumbnail,
					"time":5241,
					"type":"Video",
					"width":424
				}
			},
			"client": clients.web
		}

		if caption != None: inData["input"]["text"] = caption


		while 1:
			try:
				return loads(self.enc.decrypt(loads(request.urlopen(request.Request(Token._SendFile(), data=dumps({"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps(inData))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc')))
				break
			except: continue



	def sendDocument(self, chat_id, file, caption=None, message_id=None):
		# Token.sendDocument("guid","./file.txt", caption="anything", message_id="12345678")
		uresponse = Token._uploadFile(self, file)

		file_id = str(uresponse[0]["id"])
		mime = file.split(".")[-1]
		dc_id = uresponse[0]["dc_id"]
		access_hash_rec = uresponse[1]
		file_name = file.split("/")[-1]
		size = str(len(get(file).content if "http" in file else open(file,"rb").read()))

		inData = {
			"method":"sendMessage",
			"input":{
				"object_guid":chat_id,
				"reply_to_message_id":message_id,
				"rnd":f"{randint(100000,999999999)}",
				"file_inline":{
					"dc_id":str(dc_id),
					"file_id":str(file_id),
					"type":"File",
					"file_name":file_name,
					"size":size,
					"mime":mime,
					"access_hash_rec":access_hash_rec
				}
			},
			"client": clients.web
		}

		if caption != None: inData["input"]["text"] = caption


		while 1:
			try:
				return loads(self.enc.decrypt(loads(request.urlopen(request.Request(Token._SendFile(), data=dumps({"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps(inData))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc')))
				break
			except: continue

	def sendLocation(self, chat_id, location:list, message_id=None):
		# location = [float(x), float(y)]
		return loads(self.enc.decrypt(post(json={
			"api_version":"4",
			"auth":self.auth,
			"client": clients.android,
			"data_enc":self.enc.encrypt(dumps({
				"is_mute": False,
				"object_guid":chat_id,
				"rnd":f"{randint(100000,999999999)}",
				"location":{
					"latitude": location[0],
					"longitude": location[1]
				},
				"reply_to_message_id":message_id
			})),
			"method":"sendMessage"
		},url=Token._getURL()).json()["data_enc"]))

	#def getChannelMembers(self, channel_guid, text=None, start_id=None):
		#return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			#"method":"getChannelAllMembers",
			#"input":{
				#"channel_guid":channel_guid,
				#"search_text":text,
				#"start_id":start_id,
			#},
			#"client": clients.web
		#}))},url=Token._getURL()).json()["data_enc"]))


	def getChannelMembers(self, channel_guid, text=None, start_id=None):
		inData = {
			"method":"getChannelAllMembers",
			"input":{
				"channel_guid":channel_guid,
				"search_text":text,
				"start_id":start_id,
			},
			"client": clients.android
		}

		while 1:
			try:
				return loads(self.enc.decrypt(loads(request.urlopen(request.Request(Token._getURL(), data=dumps({"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps(inData))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc')))
				break
			except: continue


	def getChatsUpdate(self):
		inData = {
			"method":"getChatsUpdates",
			"input":{
				"state":time_stamp,
			},
			"client": clients.web
		}

		while 1:
			try:
				return loads(self.enc.decrypt(loads(request.urlopen(request.Request(Token._getURL(), data=dumps({"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps(inData))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc'))).get("data").get("chats")
				break
			except: continue

	def getChatUpdate(self, chat_id):
		time_stamp = str(round(datetime.datetime.today().timestamp()) - 200)
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"getMessagesUpdates",
			"input":{
				"object_guid":chat_id,
				"state":time_stamp
			},
			"client": clients.web
		}))},url=Token._getURL()).json().get("data_enc"))).get("data").get("updated_messages")

	def myStickerSet(self):
		time_stamp = str(round(datetime.datetime.today().timestamp()) - 200)
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"getMyStickerSets",
			"input":{},
			"client": clients.web
		}))},url=Token._getURL()).json().get("data_enc"))).get("data")

	def uploadAvatar(self,myguid,main,thumbnail=None):
		mainID = str(Token._uploadFile(self, main)[0]["id"])
		thumbnailID = str(Token._uploadFile(self, thumbnail or main)[0]["id"])
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"uploadAvatar",
			"input":{
				"object_guid":myguid,
				"thumbnail_file_id":thumbnailID,
				"main_file_id":mainID
			},
			"client": clients.web
		}))},url=Token._getURL()).json()["data_enc"]))

	def startVoiceChat(self, chat_id):
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"createGroupVoiceChat",
			"input":{
				"chat_guid":chat_id
			},
			"client": clients.web
		}))},url=Token._getURL()).json()["data_enc"]))

	def editVoiceChat(self, chat_id,voice_chat_id, title):
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"setGroupVoiceChatSetting",
			"input":{
				"chat_guid":chat_id,
				"voice_chat_id" : voice_chat_id,
				"title" : title ,
				"updated_parameters": ["title"]
			},
			"client": clients.web
		}))},url=Token._getURL()).json()["data_enc"]))

	def finishVoiceChat(self, chat_id, voice_chat_id):
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"discardGroupVoiceChat",
			"input":{
				"chat_guid":chat_id,
				"voice_chat_id" : voice_chat_id
			},
			"client": clients.web
		}))},url=Token._getURL()).json()["data_enc"]))

	def getAvatars(self,myguid):
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"getAvatars",
			"input":{
				"object_guid":myguid,
			},
			"client": clients.web
		}))},url=Token._getURL()).json().get("data_enc"))).get("data").get("avatars")

	def deleteAvatar(self,myguid,avatar_id):
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"deleteAvatar",
			"input":{
				"object_guid":myguid,
				"avatar_id":avatar_id
			},
			"client": clients.web
		}))},url=Token._getURL()).json()["data_enc"]))
	
	def deleteContact(self,guid_user):
		return self.methods.methodsRubika("json",methode ="deleteContact",indata = {"user_guid":guid_user},wn = clien.web)

	def editProfile(self, **kwargs):
		if "username" in list(kwargs.keys()):
			return loads(self.enc.decrypt(post(json={
				"api_version":"4",
				"auth":self.auth,
				"client": clients.android,
				"data_enc":self.enc.encrypt(dumps({
					"username": kwargs.get("username"),
					"updated_parameters":["username"]
				})),
				"method":"updateUsername"
			},url=Token._getURL()).json()["data_enc"]))
			kwargs = kwargs.pop("username")

		if len(list(kwargs.keys())) > 0:
			return loads(self.enc.decrypt(post(json={
				"api_version":"4",
				"auth":self.auth,
				"client": clients.android,
				"data_enc":self.enc.encrypt(dumps({
					"first_name": kwargs.get("first_name"),
					"last_name": kwargs.get("last_name"),
					"bio": kwargs.get("bio"),
					"updated_parameters":list(kwargs.keys())
				})),
				"method":"updateProfile"
			},url=Token._getURL()).json()["data_enc"]))

	def sendGIF(self, chat_id, file, width, height, thumbnail="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", caption=None, message_id=None):
		uresponse = Token._uploadFile(self, file)

		file_id = str(uresponse[0]["id"])
		mime = file.split(".")[-1]
		dc_id = uresponse[0]["dc_id"]
		access_hash_rec = uresponse[1]
		file_name = file.split("/")[-1]
		size = str(len(get(file).content if "http" in file else open(file,"rb").read()))

		return loads(self.enc.decrypt(post(json={
			"api_version":"4",
			"auth":self.auth,
			"client": clients.android,
			"data_enc":self.enc.encrypt(dumps({
				"object_guid": chat_id,
				"is_mute": False,
				"rnd": randint(100000,999999999),
				"file_inline": {
					"access_hash_rec": access_hash_rec,
					"dc_id": dc_id,
					"file_id": file_id,
					"auto_play": False,
					"file_name": file_name,
					"width": width,
					"height": height,
					"mime": mime,
					"size": size,
					"thumb_inline": thumbnail,
					"type": "Gif"
				},
				"text": caption,
				"reply_to_message_id":message_id
			})),
			"method":"sendMessage"
		},url=Token._getURL()).json()["data_enc"]))


	def votePoll(self, poll_id, option_index):
		return loads(self.enc.decrypt(post(json={
			"api_version":"4",
			"auth":self.auth,
			"client": clients.android,
			"data_enc":self.enc.encrypt(dumps({
				"poll_id": poll_id,
				"selection_index": option_index
			})),
			"method": "votePoll"
		}, url=Token._getURL()).json()["data_enc"]))

	def search(self, text):
		return loads(self.enc.decrypt(post(json={
			"api_version":"4",
			"auth":self.auth,
			"client": clients.android,
			"data_enc":self.enc.encrypt(dumps({
				"search_text": text
			})),
			"method": "searchGlobalObjects"
		}, url=Token._getURL()).json()["data_enc"]))

	def getPollStatus(self, poll_id):
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"getPollStatus",
			"input":{
				"poll_id":poll_id,
			},
			"client": clients.web
		}))},url=Token._getURL()).json()["data_enc"]))

	def getPollOptionVoters(self, poll_id, option_index, start_id=None):
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"getPollOptionVoters",
			"input":{
				"poll_id":poll_id,
				"selection_index": option_index,
				"start_id": start_id
			},
			"client": clients.web
		}))},url=Token._getURL()).json()["data_enc"]))["data"]

	#def getMe(self):
		#return Token(self.app_name, auth=self.auth, displayWelcome=False).getUserInfo(loads(open(self.app_name+".json","rt").read()).get("data").get("user").get("user_guid"))

class Socket:
	data = {"error":[],"messages":[]}

	def __init__(self, auth):
		self.auth = auth
		self.enc = encryption(auth)

	def on_open(self, ws):
		def handShake(*args):
			ws.send(dumps({
				"api_version": "4",
				"auth": self.auth,
				"data_enc": "",
				"method": "handShake"
			}))

		import _thread
		_thread.start_new_thread(handShake, ())

	def on_error(self, ws, error):
		Socket.data["error"].append(error)

	def on_message(self, ws, message):
		try:
			parsedMessage = loads(message)
			Socket.data["messages"].append({"type": parsedMessage["type"], "data": loads(self.enc.decrypt(parsedMessage["data_enc"]))})
		except KeyError: pass

	def on_close(self, ws, code, msg):
		return {"code": code, "message": msg}

	def handle(self, OnOpen=None, OnError=None, OnMessage=None, OnClose=None, forEver=True):
		import websocket # pip install websocket-client

		ws = websocket.WebSocketApp(
			choice([
		"wss://jsocket1.iranlms.ir:80" ,
		"wss://jsocket2.iranlms.ir:80" ,
		"wss://jsocket3.iranlms.ir:80",
		"wss://jsocket5.iranlms.ir:80"
		 ]),
			on_open=OnOpen or Socket(self.auth).on_open,
			on_message=OnMessage or Socket(self.auth).on_message,
			on_error=OnError or Socket(self.auth).on_error,
			on_close=OnClose or Socket(self.auth).on_close
		)

		if forEver : ws.run_forever()
