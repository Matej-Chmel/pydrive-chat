from _repo import join, read_local_version, REPO

ENDL = '\n'
VERSION = None

def fres(filename, mode='r'):
	return open(join(PROJECT.RES, filename), mode, encoding='utf-8')

def get_version():
	global VERSION
	if VERSION is None:
		VERSION = read_local_version()
	return VERSION

def res_(filename):
	return join(PROJECT.RES, filename)

class PROJECT:
	RES = join(REPO.ROOT, 'res')
	running = True

REPO.read_info()
