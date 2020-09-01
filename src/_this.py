from _repo import join, read_local_version, REPO, spec, system_call

ENDL = '\n'
IS_TERMUX = (
	spec.LINUX and
	system_call('uname -o').strip() == 'Android' and
	bool(system_call('command -v termux-open-url', shell=True))
)
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
