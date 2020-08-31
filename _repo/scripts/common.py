from ast import literal_eval as eval
from os import chdir as cd
from os.path import abspath, dirname, join, pardir, realpath
from subprocess import CalledProcessError, check_output
from sys import exit

class REPO:
	_INFO_STATUS = DATA = NAME = PRIVATE = REQ = ROOT = USER = None
	@staticmethod
	def read_info():
		if REPO._INFO_STATUS is None:
			path, file = fdata_('info.pydef')
			try:
				with file:
					info = eval(file.read())
					REPO.USER = info['user']
					REPO.NAME = info['repo_name']
					REPO.PRIVATE = info['private']
				REPO._INFO_STATUS = True
			except OSError:
				print(f'File {path} not found.')
				REPO._INFO_STATUS = False
		return REPO._INFO_STATUS

REPO.ROOT = abspath(join(dirname(realpath(__file__)), pardir, pardir))
REPO.DATA = join(REPO.ROOT, '_repo', 'data')
REPO.REQ = join(REPO.ROOT, '_repo', 'init', 'requirements')

try:
	from ._x_specific import spec
except ImportError:
	import platform
	class spec:
		OS_NAME = platform.system().lower()
		LINUX = WINDOWS = None
	spec.LINUX = spec.OS_NAME.startswith('linux')
	spec.WINDOWS = False if spec.LINUX else spec.OS_NAME.startswith('win')

def confirm(prompt):
	while True:
		selected = input(f'{prompt} (y/n): ').lower()
		if selected in ['y', 'yes']:
			return True
		if selected in ['n', 'no']:
			return False
		print(f'Please choose answer yes or no.')

def fopen_(path, mode):
	return path, open(path, mode, encoding='utf-8')

def fdata(filename, mode='r'):
	return open(join(REPO.DATA, filename), mode, encoding='utf-8')

def fdata_(filename, mode='r'):
	return fopen_(join(REPO.DATA, filename), mode)

def freq_(filename, mode='r'):
	return fopen_(join(REPO.REQ, filename), mode)

def system_call(text, success_message=None, alt=None, shell=False):
	try:
		output = check_output(text.split(), shell=shell)
		if success_message is not None:
			print(success_message)
		return output.decode()
	except CalledProcessError as e:
		if alt is not None:
			print(f"Command {text} didn't work, trying an alternative.")
			system_call(alt, success_message)
		else:
			print(
				f'Something went wrong.\n'
				f'Error code: {e.returncode}\n'
				f'More info: {e.output.decode()}\n'
			)
			exit(1)
