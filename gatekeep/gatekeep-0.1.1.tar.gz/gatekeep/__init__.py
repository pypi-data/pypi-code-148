__version__ = '0.1.1'

# other imports
import os
from gatekeep.gatekeep.log import log

log(" --< Starting Gatekeep >--")

# --< Checking if required files exist >-- #
requiredFiles = [
	"Gatekeep",
	"Gatekeep/Settings.json",
	"Gatekeep/Users.json",
	"Gatekeep/Logs.log"
]

missingFiles = []
log("Verifying Files...")
for path in requiredFiles:
	if not os.path.exists(path):
		missingFiles.append(path)
		log(f"Missing file or folder: {path}")

if len(missingFiles) > 0:
	strMissingFiles = "\n\t".join(missingFiles)
	if input(f"Gatekeep is missing some required files.\n\t{strMissingFiles}\n\n[y/n] can gatekeep create these files\n > ").lower() == "y":
		
		for path in missingFiles:
			log(f"Making file or folder: {path}")
			if "." not in path:
				os.mkdir(path)
			else:
				open(path, "x")
	os.system("clear")



# GK modules
from gatekeep.gatekeep.errors import *
from gatekeep.gatekeep import settings
from gatekeep.gatekeep import users
log("Finished Startup")