from _repo import cd, REPO, system_call

cd(REPO.ROOT)

system_call(
	'git reset --soft HEAD~1',
	'Latest unpushed commit removed.',
	'git reset --soft HEAD'
)
system_call('git reset HEAD -- .', 'Staged changes removed.')

print('Soft reset completed.')
