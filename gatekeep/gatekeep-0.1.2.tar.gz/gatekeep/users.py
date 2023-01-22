
import hashlib
import json

from gatekeep import errors
from gatekeep import settings
from gatekeep.log import log

userList:dict
try:
	userList = json.load(open("Gatekeep/Users.json"))
except:
	userList = {}

# --< UTIL FUNCTIONS >-- #
def throw(error:Exception)->None:
	if settings.getSetting("raiseErrors"):
		raise error

def hash(string)->str:
		return str(hashlib.pbkdf2_hmac(
			'sha256',
    	bytes(string,'utf-8'), # Convert the password to bytes
	    int.to_bytes(settings.getSetting("salt"),32,"big"), # Provide the salt
  	  settings.getSetting("hashLimit"), # It is recommended to use at least 100,000 iterations of SHA-256 
    	dklen=settings.getSetting("hashSize") # Get a 128 byte key
))

def updateUsers()->None:
	json.dump(userList,open("Gatekeep/Users.json","w"),indent=2)

# --< public >-- #
def create(username:str,password:str,*,clearance:int=-1,data:dict={})->None:
	log(f"Creating new user: {username}")
	if username in userList.keys():
		log("Username Found")
		if not login(username,password):
			throw(errors.UserExistsError)
			return
		elif not settings.getSetting("overrideUserCreation"):
			log("User exists : config guarded")
			throw(errors.UserExistsError)
			return
	
	userList[username] = {
		"password":hash(password),
		"clearance":clearance,
		"data":settings.getSetting("defaultUserData")
	}
	if data != {}:
		userList[username]["data"] = data
	updateUsers()
	log("Creation successful")

def getAll()->list:
	keys:list = []
	[keys.append(key) for key in userList.keys()]
	return keys

def getData(username,password)->dict:
	if login(username,password):
		log(f"Data from user {username} provided")
		return userList[username]["data"]

def setData(username,password,data)->None:
	if login(username,password):
		userList[username]["data"] = data
		updateUsers()

def login(username,password)->bool:
	try:
		user = userList[username]
	except KeyError:
		log(f"Login from user {username} failed : no user exists")
		return False
	
	if user["password"] == hash(password):
		log(f"Login from user {username} successful")
		return True
	log(f"Login from user {username} failed : wrong password")
	return False
	