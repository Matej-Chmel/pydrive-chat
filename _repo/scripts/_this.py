from os import chdir as cd
from os.path import abspath, dirname, join, pardir, realpath
import platform
from subprocess import CalledProcessError, check_output as execute
from sys import exit

OS_NAME = platform.system().lower()
OS_LINUX = OS_NAME.startswith('linux')
PYTHON = 'python' if OS_LINUX or not OS_NAME.startswith('win') else 'py'

REPO_ROOT = abspath(join(dirname(realpath(__file__)), pardir, pardir))
REPO_DATA = join(REPO_ROOT, '_repo', 'data')
REPO_REQ = join(REPO_ROOT, '_repo', 'init', 'requirements')

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
	return open(join(REPO_DATA, filename), mode, encoding='utf-8')

def fdata_(filename, mode='r'):
	return fopen_(join(REPO_DATA, filename), mode)

def freq_(filename, mode='r'):
	return fopen_(join(REPO_REQ, filename), mode)

def system_call(text, success_message=None, alt=None):
	try:
		output = execute(text.split())
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
