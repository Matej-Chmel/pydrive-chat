from .drive import append_to_log, drive, login_and_init, overwrite_log, read_log
from ._this import ENDL, get_version, PROJECT

actions = {}
nickname: str = None

# decorator
def command(func):
	actions[func.__name__] = func
	return func

@command
def exit(args = None):
	PROJECT.running = False

@command
def help(args = None):
	print(f'Available commands:{ENDL}{ENDL.join(sorted([name for name in actions]))}')

@command
def login(args = None):
	print(f"Login {'aborted' if not login_and_init() or not name() else 'successful'}")

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
def read(args = None):
	content = read_log()
	print(content if content else '*** EMPTY ***')

@command
def reset(args = None):
	overwrite_log('')
	print('Chat emptied.')

@command
def say(args: list):
	append_to_log(f"{nickname}: {' '.join(args)}")
	print('Success.')

@command
def version(args = None):
	print(f'Current version is {get_version()}.')
