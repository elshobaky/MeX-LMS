from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

from drive_config import config, FOLDER_NAME, FOLDER_ID

def connect():
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile("creds.txt")
    if gauth.credentials is None:
        # Authenticate if they're not there
        config.update(folder_name='', folder_id='')
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        # Refresh them if expired
        gauth.Refresh()
    else:
        # Initialize the saved creds
        gauth.Authorize()
    # Save the current credentials to a file
    gauth.SaveCredentialsFile("creds.txt")
    drive = GoogleDrive(gauth)
    return drive


def create_folder(fname, fid=None):
    drive = connect()
    metadata = {"title": fname,
                "mimeType": "application/vnd.google-apps.folder"}
    if fid:
        metadata["id"] = fid
    folder = drive.CreateFile(metadata)
    folder.Upload()
    return folder['id']


def upload_file(file_path, title=None, fid=None, parent_id=FOLDER_ID):
    if not parent_id:
        x, folder_id = init_drive()
    drive = connect()
    metadata = {}
    if title:
        metadata["title"] = title
    if fid:
        metadata["id"] = fid
    if parent_id:
        metadata["parents"] = [{"kind": "drive#fileLink",
                                "id": parent_id}]
    f = drive.CreateFile(metadata)
    f.SetContentFile(file_path)
    f.Upload()
    return f['id']


def init_drive():
    global FOLDER_NAME, FOLDER_ID
    if not FOLDER_NAME or not FOLDER_ID:
        FOLDER_NAME = "MeX-LMS BACKUP"
        FOLDER_ID = create_folder(FOLDER_NAME)
        config.update(folder_name=FOLDER_NAME, folder_id=FOLDER_ID)
    return FOLDER_NAME, FOLDER_ID


def test():
    init_drive()
    file_path = 'G:\\3M.2A.1E\\Al-Maktba\\LMS\\MeX-LMS2\\mex.db'
    upload_file(file_path, title='MeX-db50.mex')

if __name__ == '__main__':
    test()