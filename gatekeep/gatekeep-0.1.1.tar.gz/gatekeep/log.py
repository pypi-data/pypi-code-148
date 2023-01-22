
from datetime import datetime
from os.path import exists

logBackup = []

def log(string)->None:
	string = f"[{datetime.now().strftime('%H:%M:%S')}] {string}\n"
	if exists("Gatekeep/Logs.log"):
		with open("Gatekeep/Logs.log","a") as writer:
			if len(logBackup) > 0:
				[writer.write(line) for line in logBackup]
			writer.write(string)
	else:
		logBackup.append(string)