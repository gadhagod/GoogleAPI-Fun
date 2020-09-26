from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

scopes = "https://www.googleapis.com/auth/drive.readonly"
client_secret = "../client_secret.json"

store = file.Storage('storage.json')
cred = store.get()

if not cred or cred.invalid:
    flow = client.flow_from_clientsecrets(client_secret, scopes)
    cred = tools.run_flow(flow, store)

service = build('drive', 'v2', http=cred.authorize(Http()))
files = service.files().list().execute().get('items', [])

for f in files:
    print(f['title'])
