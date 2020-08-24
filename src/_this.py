from _repo import read_local_version

VERSION = None

def get_version():
	global VERSION
	if VERSION is None:
		VERSION = read_local_version()
	return VERSION
