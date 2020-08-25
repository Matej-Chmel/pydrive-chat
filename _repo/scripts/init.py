from _repo import cd, REPO, spec, system_call

cd(REPO.ROOT)

system_call(
	'git config core.hooksPath _repo/hooks',
	'Hooks were configured successfully.'
)

def main():
	try:
		from ._x_install_required import install
		install()
	except ImportError:
		print('Requirements installer is missing. Assuming there are no requirements.')

	if not spec.LINUX:
		return

	from glob import glob
	from os import stat, chmod
	from stat import S_IEXEC as EXECUTE_PERMISSION

	hooks = [file for file in glob(f'{REPO.ROOT}/_repo/hooks/*') if '.' not in file]
	for file in hooks:
		chmod(file, stat(file).st_mode | EXECUTE_PERMISSION)

	print('Permissions were granted to all hooks successfully.')

if __name__ == "__main__":
	main()
