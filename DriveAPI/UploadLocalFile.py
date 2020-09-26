import os

from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools

scopes = 'https://www.googleapis.com/auth/drive'

store = file.Storage('storage.json')
cred = store.get()
if not cred or cred.invalid:
    flow = client.flow_from_clientsecrets('../client_secret.json', scopes)
    cred = tools.run_flow(flow, store)
drive = discovery.build('drive', 'v2', http=cred.authorize(Http()))

files = (
    ('./UploadLocalFile.py', False),
    ('./UploadLocalFile.py', True),
)

for filename, convert in files:
    metadata = {'title': filename}
    res = drive.files().insert(convert=convert, body=metadata,
            media_body=filename, fields='mimeType,exportLinks').execute()
    print('It worked!')
