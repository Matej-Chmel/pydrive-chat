# PyDrive chat
An example repository that shows how to share messages between devices via Google Drive using Python and the [PyDrive](https://pypi.org/project/PyDrive/) package.

## Supported platforms
- Android running the [Termux](https://play.google.com/store/apps/details?id=com.termux&hl=cs) app
- Linux
- OS X
- Windows

In addition, the targeted platform must run Python 3.8 or higher.

## Installing
1. Clone the repo.
2. Initialize the repo by following one of the options:
	1. If you use VS Code, run the [Init repo](.vscode/tasks.json#L51) task.
	2. If you can run batch or shell scripts, run one from the [_repo/init](_repo/init/) directory.
	3. Or run the [_repo/scripts/init.py](_repo/scripts/init.py) directly with `python -m _repo.scripts.init`.
3. Create your own Google's console Project by following this [tutorial](https://pythonhosted.org/PyDrive/quickstart.html).
4. Move *client_secrets.json* (the file they are talking about in the tutorial) to the [res](res/) directory.
5. Run the app by following one of the options:
	1. If you use VS Code, run the [Run](.vscode/tasks.json#L5) task.
	2. If you can run batch or shell scripts, run one from the [_repo/run](_repo/run/) directory.
	3. Or run the [src/main.py](src/main.py) directly with `python -m src.main`.

## Optional arguments
- `v` or `--version`
	- Shows current version number of your local repo and closes the program.
- `login={name}` where you substitute `{name}` with your nickname.
	- Runs command `login {name}` on startup.

## Usage
The app creates a `AppData/pydrive-chat/chat_log.txt` file in your Drive that saves the messages. I will refer to this file as *chat log* in the rest of this text.

The program is controlled by a command-line interface so here is a list of available commands and their usage.

- `empty`
	- Deletes all entries from the chat log.
- `exit`
	- Closes the program.
- `help`
	- Prints names of available commands.
- `help {name}`
	- Prints description of command supplied as an argument.
- `login`
	- Logs you into a Drive.
	- If you didn't login before, it opens a window in your browser from which you can choose an Google account that will be used.
	- After successful login, you will be prompted for a nickname.
- `login {name}`
	- After successful login, the app will attempt to set the name as your nickname.
- `name`
	- Let's you change your nickname with a prompt.
- `name {text}`
	- Skips the prompt and attempts to set text as your nickname.
- `new`
	- Queries last updates from the chat log that were not yet read in this session and displays them.
- `read`
	- Reads the entire chat log.
- `say {text}`
	- Adds new entry to the chat log labeled with your nickname and containing the text supplied as argument.
	- The text can contain whitespace.
- `termux`
	- Tells you if the app detected you are running it on Termux or not.
- `version`
	- Displays the current version number.
- `when`
	- Displays the chat log's date of last modification corrected for the local timezone and daylight saving time.

## Licensing

### Third-party code

Following files are licensed under the Apache License, Version 2.0:
- [src/auth.py](src/auth.py)

Full text of the license available in the [LICENSE_PyDrive](LICENSE_PyDrive) file.

### Own work

Every file that is not mentioned in the previous section is licensed under the Creative Commons Zero v1.0 Universal.

Full text of the license available in the [LICENSE](LICENSE) file.
