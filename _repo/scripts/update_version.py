from _repo import fdata, read_github_version, read_local_version

version = read_github_version()

if not version:
	print('Reading latest version from local file.')
	version = read_local_version()

print(f'Latest version was {version}.')
version += 1

with fdata('version.txt', 'w+') as file:
	file.write(str(version))

print(f'Successfully upgraded version to {version}.')
