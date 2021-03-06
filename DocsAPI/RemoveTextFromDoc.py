from apiclient import discovery
from httplib2 import Http
from oauth2client import client
from oauth2client import file
from oauth2client import tools

SCOPES = 'https://www.googleapis.com/auth/documents'
DISCOVERY_DOC = 'https://docs.googleapis.com/$discovery/rest?version=v1'
DOCUMENT_ID = input('Doc id: ')

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
    
    requests = [
         {
            'deleteContentRange': {
                'range': {
                    'startIndex': 1,
                    'endIndex': 6,
                }
            }
        }
    ]
    
    service.documents().batchUpdate(documentId=DOCUMENT_ID, body={'requests': requests}).execute()    
    print('Removed characters 1-5')

main()
