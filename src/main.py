from sys import argv
from ._this import get_version, PROJECT, REPO
from .drive import login_and_init
import src.commands as commands
from src.commands import actions, login

LOGIN_ARG = 'login='

def ask_for_command(prompt):
	cmdname, *args = input(prompt).split()
	print()
	try:
		chosen_cmd = actions[cmdname]
		chosen_cmd(args)
	except KeyError:
		print(f"Command '{cmdname}' not recognized.")

def main():
	if len(argv) >= 2:
		cmd = argv[1]
		if cmd in ['v', '--version']:
			print(f'{REPO.NAME} version {get_version()}.')
			return
		if cmd.startswith(LOGIN_ARG):
			login([cmd[cmd.index(LOGIN_ARG) + len(LOGIN_ARG):]])

	ask_for_command('Enter command: ')
	while PROJECT.running:
		ask_for_command('\nEnter command: ')

if __name__ == "__main__":
	main()
