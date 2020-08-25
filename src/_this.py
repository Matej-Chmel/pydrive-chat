from _repo import read_local_version, REPO

VERSION = None

def get_version():
	global VERSION
	if VERSION is None:
		VERSION = read_local_version()
	return VERSION

REPO.read_info()
