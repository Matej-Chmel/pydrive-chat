from ._this import get_version, REPO
from sys import argv

def main():
	if len(argv) >= 2 and argv[1] in ['v', '--version']:
		print(f'{REPO.NAME} version {get_version()}.')
		return
	print(f'Hello from {REPO.NAME}.')

if __name__ == "__main__":
	main()
