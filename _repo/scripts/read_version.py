from ast import literal_eval as eval
from base64 import b64decode
from _repo import fdata_

def read_github_version():
	path, file = fdata_('info.pydef')
	try:
		from requests import get, codes
		with file:
			info = eval(file.read())
	except ImportError:
		return print("Module 'requests' not found.")
	except OSError:
		return print(f'File {path} not found.')

	url = (
		f"https://api.github.com/repos/{info['user']}/"
		f"{info['repo_name']}/contents/_repo/data/version.txt"
	)

	if info['private']:
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
