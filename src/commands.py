from .auth import IS_TERMUX
from .drive import *
from ._this import get_version, PROJECT

actions = {}
lines_read = 0
nickname: str = None

# decorator
def command(func):
	actions[func.__name__] = func
	return func

@command
def empty(args = None):
	overwrite_log('')
	print('Chat emptied.')

@command
def exit(args = None):
	PROJECT.running = False

@command
def help(args = None):
	print(f'Available commands:{ENDL}{ENDL.join(sorted([name for name in actions]))}')

@command
def login(args = None):
	print(f"Login {'aborted' if not login_and_init() or not name(args) else 'successful'}")

@command
def name(args: list = None):
	global nickname
	new_name = ' '.join(args) if args else input('Choose your nickname: ')
	while True:
		if new_name == 'exit':
			return False
		if not len(new_name) or ':' in new_name:
			new_name = input("Nicknames cannot be empty and cannot contain ':'.\nEnter your nickname: ")
		else:
			print(f'Nickname set to {(nickname := new_name)}.')
			return True

@command
def new(args = None):
	global lines_read

	content = read_if_modified()
	if content is None:
		return print('*** NO UPDATES ***')

	lines = content.splitlines()
	if lines_read == len(lines):
		return print('*** NO UPDATES ***')
	if lines_read > len(lines):
		lines_read = len(lines)
		return print(f'*** CHAT RECENTLY EMPTIED ***{ENDL}{ENDL.join(lines)}')
	print(ENDL.join(lines[lines_read:]))
	lines_read = len(lines)

@command
def read(args = None):
	content = read_log()
	print(content if content else '*** EMPTY ***')

@command
def say(args: list):
	append_to_log(f"{nickname}: {' '.join(args)}")
	print('Success.')

@command
def termux(args = None):
	print('You are running this from Termux.' if IS_TERMUX else 'You are using other platform than Termux.')

@command
def version(args = None):
	print(f'Current version is {get_version()}.')

@command
def when(args = None):
	print(when_modified().strftime('%d.%m.%Y\t%H:%M:%S.%f')[:-3])
