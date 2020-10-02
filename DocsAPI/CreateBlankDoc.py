from apiclient import discovery
from httplib2 import Http
from oauth2client import client
from oauth2client import file
from oauth2client import tools

SCOPES = 'https://www.googleapis.com/auth/documents'
DISCOVERY_DOC = 'https://docs.googleapis.com/$discovery/rest?version=v1'

def setup():
    store = file.Storage('token.json')
    credentials = store.get()

    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets('../client_secret.json', SCOPES)
        credentials = tools.run_flow(flow, store)
    return credentials

def main():
    credentials = setup()
    http = credentials.authorize(Http())
    service = discovery.build('docs', 'v1', http=http, discoveryServiceUrl=DISCOVERY_DOC)
    body = {'title': 'Made from the Google Docs API'}
    doc = service.documents().create(body=body).execute()
    print('It worked!')

main()
