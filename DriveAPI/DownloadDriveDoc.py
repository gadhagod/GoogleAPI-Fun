from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
import io
from googleapiclient.http import MediaIoBaseDownload

scopes = 'https://www.googleapis.com/auth/drive'
store = file.Storage('storage.json')
cred = store.get()
if not cred or cred.invalid:
    flow = client.flow_from_clientsecrets('../client_secret.json', scopes)
    cred = tools.run_flow(flow, store)
drive = discovery.build('drive', 'v2', http=cred.authorize(Http()))

file_id = '1hKZtYVU7qr_2mrWmZ-1tytMrilqMD3T-VNPKpJAs26k'
request = drive.files().export_media(fileId=file_id,
                                             mimeType='application/pdf')
fh = io.BytesIO()
downloader = MediaIoBaseDownload(fh, request)
print('It worked!')

