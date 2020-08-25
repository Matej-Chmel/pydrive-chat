from base64 import b64decode
from _repo import fdata_, REPO

def read_github_version():
	try:
		from requests import get, codes
	except ImportError:
		return print("Module 'requests' not found.")

	if not REPO.read_info():
		return None

	url = (
		f"https://api.github.com/repos/{REPO.USER}/"
		f"{REPO.NAME}/contents/_repo/data/version.txt"
	)

	if REPO.PRIVATE:
		path, file = fdata_('.token')
		try:
			with file:
				token = file.read().rstrip('\n')
		except OSError:
			return print(f'File {path} not found.')

		request = get(url, headers={'Authorization': f'token {token}'})
	else:
		request = get(url)
	
	if request.status_code == codes.ok: #pylint: disable=no-member
		print('Reading latest version from GitHub.')
		try:
			return int(b64decode(request.json()['content']))
		except ValueError:
			return print('Content of version file from GitHub could not be converted to an integer.')
	else:
		return print('Repository or version file not found.')

def read_local_version():
	path, file = fdata_('version.txt')
	try:
		with file:
			return int(file.read())
	except OSError:
		print(f"File {path} not found. Assumed version 0.")
		return 0
	except ValueError:
		print('File content could not be converted to an integer. Assumed version 0.')
		return 0
