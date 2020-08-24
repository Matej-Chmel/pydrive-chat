import re
from sys import argv
from _repo import read_local_version

with open(argv[1], 'r', encoding='utf-8') as file:
	message = file.read()

if re.match(r'^Version\s\d+\.\s[^\s]((.|\n)*)$', message) is None:
	message = f'Version {read_local_version()}. {message}'
	print(f"Formatted message to '{message}'")
else:
	print('Message was formatted fine.')

with open(argv[1], 'w', encoding='utf-8') as file:
	file.write(message)
