from .auth import IS_TERMUX
from .drive import *
from ._this import get_version, PROJECT

actions = {}
lines_read = 0
nickname: str = None

# decorator
def command(*description):
	def _decorator(func):
		actions[func.__name__] = func, '\n'.join(description)
		return func
	return _decorator

def not_recognized(cmdname):
	print(f"Command '{cmdname}' not recognized.")

@command('Clears all content from the chat log and uploads it to the Drive.')
def empty(args = None):
	overwrite_log('')
	print('Chat emptied.')

@command('Closes this app.')
def exit(args = None):
	PROJECT.running = False

@command(
	'If no argument is supplied, displays list of available commands.',
	'Else it displays description of command passed as an argument.'
)
def help(args = None):
	if not args:
		return print(f'Available commands:{ENDL}{ENDL.join(sorted([name for name in actions]))}')
	try:
		print(actions[args[0]][1])
	except KeyError:
		not_recognized(args[0])

@command(
	'Logs you into your Drive.',
	'If you log for the first time, app prompts you for an account that will be used.',
	'After successful login, you will prompted for a nickname.',
	'If you supply name as an argument, app will attempt to set that as your nickname.'
)
def login(args = None):
	global nickname
	print(f"Login {'successful' if login_and_init() and (nickname or name(args)) else 'aborted'}")

@command(
	"Let's you choose your nickname that will be visible in the chat log when you post messages.",
	'If no argument is passed, app prompts you for a new name.',
	'By passing argument, you can set the name directly.',
	"Nickname can contain whitespace, but ':', newlines and empty nicknames aren't allowed."
)
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

@command('Displays last updates from the chat log that were not yet read in this session.')
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

@command('Displays the entire chat log.')
def read(args = None):
	content = read_log()
	print(content if content else '*** EMPTY ***')

@command(
	'Adds new entry to the chat log labeled with your nickname and containing the text supplied as an argument.',
	'The text can contain whitespace.'
)
def say(args: list):
	append_to_log(f"{nickname}: {' '.join(args)}")
	print('Success.')

@command('Tells you if the app detected you are running it on Termux or not.')
def termux(args = None):
	print('You are running this from Termux.' if IS_TERMUX else 'You are using other platform than Termux.')

@command('Displays the current version number.')
def version(args = None):
	print(f'Current version is {get_version()}.')

@command("Displays the chat log's date of last modification corrected for the local timezone and daylight saving time.")
def when(args = None):
	print(when_modified().strftime('%d.%m.%Y\t%H:%M:%S.%f')[:-3])
