import json
import os

from gatekeep import errors
from gatekeep.log import log

defaultSettings = {
	"salt":int.from_bytes(os.urandom(32),"big"), # Salt for hashing
	"raiseErrors":True, # Raise Errors
	"hashLimit":10000, # Number of times to iterate hash function
	"hashSize":128, # Size of hash output
	"defaultUserData":{},
	"overrideUserCreation":False
}

# importing settings

reloadSettingsFlag = False
SETTINGS:dict = {}

# catching empty settings edge case
try:
	SETTINGS = json.load(open("Gatekeep/Settings.json"))
except json.JSONDecodeError:
	log("JSON decode error while opening settings")
	reloadSettingsFlag = True

# security check
for key in defaultSettings:
	if key not in SETTINGS.keys():
		log(f"Settings missing key [{key}]")
		SETTINGS[key] = defaultSettings[key]
		reloadSettingsFlag = True

# re-write to file
if reloadSettingsFlag:
	log("Reloading settings")
	json.dump(SETTINGS,open("Gatekeep/Settings.json","w"),indent=2)

def getSetting(key):
	value = None
	try:
		value = SETTINGS[key]
	except KeyError:
		if value in defaultSettings.keys():
			value = defaultSettings.keys()
			SETTINGS[key] = value
			json.dump(SETTINGS,open("Gatekeep/Settings.json","w"),indent=2)
		else:
			raise errors.SettingNotFoundError
	return value