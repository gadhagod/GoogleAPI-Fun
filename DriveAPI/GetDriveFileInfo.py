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

title = input('File name: ')

for f in files:
    if (f['title']) == title:
        print('File ID: ' + f['id'])
        print('Type: ' + f['mimeType'])
        print('Created: ' + f['createdDate'])
        print('Last modified: ' + f['modifiedDate'])
        print('Last modified by you: ' + f['modifiedByMeDate'])
        print('Last opened by you: ' + f['lastViewedByMeDate'])
        for o in f['owners']:
            print('Owner: ' + o['displayName'] + ' (' + o['emailAddress'] + ')')
        print('Last modified by: ' + f['lastModifyingUser']['displayName'] + ' (' + f['lastModifyingUser']['emailAddress'] + ')')

