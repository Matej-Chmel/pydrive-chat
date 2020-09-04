from datetime import datetime, timedelta
from io import BytesIO
from pathlib import Path
from time import altzone, daylight, localtime, timezone
from pydrive.auth import GoogleAuth, AuthenticationRejected
from pydrive.drive import GoogleDrive as Drive, GoogleDriveFile as File
from requests import patch
from .auth import gauth
from ._this import ENDL, res_

CHAT_LOG: File = None
FILE_TYPE = 'application/vnd.google-apps.file'
FOLDER_TYPE = 'application/vnd.google-apps.folder'
LAST_READ: datetime = None
UTC_OFFSET_SECS = -(altzone if daylight and localtime().tm_isdst > 0 else timezone)

drive: Drive = None

def setup_gauth():
	path = res_('client_secrets.json')
	if not Path(path).is_file():
		raise FileNotFoundError
	GoogleAuth.DEFAULT_SETTINGS['client_config_file'] = path

def empty_contents_of_(file):
	patch(
		f"https://www.googleapis.com/upload/drive/v3/files/{file['id']}?uploadType=multipart",
		headers={'Authorization': f"Bearer {gauth.credentials.token_response['access_token']}"},
		files={
			'data': ('metadata', '{}', 'application/json'),
			'file': BytesIO()
		}
	)

def ensure_item(title: str, mime_type=None, parents=None, trashed=False):
	query = f"title='{title}'"
	if mime_type:
		query += f" and mimeType='{mime_type}'"
	if parents:
		query += f""" and {
			' and '.join(f"'{item['id']}' in parents" for item in parents)
		}""" if type(parents) is list else f" and '{parents['id']}' in parents"
	if trashed is not None:
		query += f' and trashed={str(trashed).lower()}'

	try:
		return drive.ListFile({'q': query}).GetList()[0]
	except IndexError:
		metadata = {'title': title}
		if mime_type:
			metadata['mimeType'] = mime_type
		if parents:
			metadata['parents'] = [
				{'id': item['id']} for item in parents
			] if type(parents) is list else [{'id': parents['id']}]

		file = drive.CreateFile(metadata)
		file.Upload()
		return file

def log_into_drive():
	creds_path = res_('creds.json')

	if Path(creds_path).is_file():
		gauth.LoadCredentialsFile(creds_path)
	else:
		try:
			gauth.LocalWebserverAuth()
			gauth.SaveCredentialsFile(creds_path)
		except:
			return None

	return Drive(gauth)

def login_and_init():
	global CHAT_LOG, drive
	drive = log_into_drive()
	if drive is None:
		return False

	app_data = ensure_item('AppData', FOLDER_TYPE)
	app_folder = ensure_item('pydrive-chat', FOLDER_TYPE, app_data)
	CHAT_LOG = ensure_item('chat_log.txt', parents=app_folder)

	return True

def append_to_log(text):
	CHAT_LOG.SetContentString(f'{CHAT_LOG.GetContentString()}{text}{ENDL}')
	CHAT_LOG.Upload()

def overwrite_log(text=None):
	if not text:
		empty_contents_of_(CHAT_LOG)
		CHAT_LOG.Upload()
		CHAT_LOG.SetContentString('')
	else:
		CHAT_LOG.SetContentString(text)
		CHAT_LOG.Upload()

def read_log():
	return CHAT_LOG.GetContentString()

def read_if_modified():
	global LAST_READ, LINES_READ

	def was_modified():
		modified_at = when_modified()
		if LAST_READ < modified_at:
			LAST_READ = modified_at
			return True
		return False

	if LAST_READ is None or was_modified():
		return CHAT_LOG.GetContentString()
	return None

def when_modified():
	return datetime.strptime(CHAT_LOG['modifiedDate'], '%Y-%m-%dT%H:%M:%S.%fZ') + timedelta(seconds=UTC_OFFSET_SECS)
