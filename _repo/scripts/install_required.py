from _repo import freq_, PYTHON, system_call

def install():
	path, file = freq_('any.req')
	try:
		with file:
			for line in file:
				line = line.strip()
				if not line.startswith('#'):
					system_call(
						f'{PYTHON} -m pip install {line} --user',
						f"{line.replace('==', ' ')} checked."
					)
		print('Completed setup of packages.')
	except OSError:
		print(f"File {path} not found.")
