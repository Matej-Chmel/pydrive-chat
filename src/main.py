from sys import argv
from ._this import get_version, PROJECT, REPO
from .drive import login_and_init, setup_gauth
import src.commands as commands
from src.commands import actions, login, not_recognized

LOGIN_ARG = 'login='

def ask_for_command(prompt):
	cmdname, *args = input(prompt).split()
	print()
	try:
		chosen_cmd = actions[cmdname]
		chosen_cmd[0](args)
	except KeyError:
		not_recognized(cmdname)

def main():
	try:
		try:
			option = argv[1]
			if option in ['v', '--version']:
				return print(f'{REPO.NAME} version {get_version()}.')
			setup_gauth()
			if option.startswith(LOGIN_ARG):
				login([option[option.index(LOGIN_ARG) + len(LOGIN_ARG):]])
		except IndexError:
			setup_gauth()
	except FileNotFoundError:
		return print(
			"File 'res/client_secrets.json' is missing.\n"
			"Please refer to Installation section in 'README.md' in the root of this repo."
		)

	ask_for_command('Enter command: ')
	while PROJECT.running:
		ask_for_command('\nEnter command: ')

if __name__ == "__main__":
	main()
