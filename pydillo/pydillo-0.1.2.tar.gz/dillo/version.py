from cerver.utils.log import LOG_TYPE_NONE, cerver_log_both

from .lib import lib

DILLO_VERSION = "0.1.2"
DILLO_VERSION_NAME = "Version 0.1.2"
DILLO_VERSION_DATE = "22/01/2023"
DILLO_VERSION_TIME = "23:33 CST"
DILLO_VERSION_AUTHOR = "Erick Salas"

version = {
	"id": DILLO_VERSION,
	"name": DILLO_VERSION_NAME,
	"date": DILLO_VERSION_DATE,
	"time": DILLO_VERSION_TIME,
	"author": DILLO_VERSION_AUTHOR
}

dillo_libauth_version_print_full = lib.dillo_libauth_version_print_full
dillo_libauth_version_print_version_id = lib.dillo_libauth_version_print_version_id
dillo_libauth_version_print_version_name = lib.dillo_libauth_version_print_version_name

def pydillo_version_print_full ():
	output = "\nPyDillo Version: {name}\n" \
		"Release Date: {date} - {time}\n" \
		"Author: {author}\n".format (**version)

	cerver_log_both (
		LOG_TYPE_NONE, LOG_TYPE_NONE,
		output.encode ("utf-8")
	)

def pydillo_version_print_version_id ():
	cerver_log_both (
		LOG_TYPE_NONE, LOG_TYPE_NONE,
		f"\nPyDillo Version ID: {version.id}\n".encode ("utf-8")
	)

def pydillo_version_print_version_name ():
	cerver_log_both (
		LOG_TYPE_NONE, LOG_TYPE_NONE,
		f"\nPyDillo Version: {version.name}\n".encode ("utf-8")
	)
