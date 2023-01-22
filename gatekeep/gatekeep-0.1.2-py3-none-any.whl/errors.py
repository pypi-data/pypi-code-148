from gatekeep.log import log

class WorkInProgress(Exception):
	log("[ERROR] : WorkInProgress")

class SettingNotFoundError(Exception):
	log("[ERROR] : SettingNotFoundError")

class UserExistsError(Exception):
	log("[ERROR] : UserExistsError")

class FalseCredentialsError(Exception):
	log("[ERROR] : FalseCredentialsError")