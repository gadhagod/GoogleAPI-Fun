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
        
    requests = [{
        'insertInlineImage': {
            'location': {
                'index': 1
            },
            'uri':
                'https://raw.githubusercontent.com/gadhagod/GoogleAPI-Fun/master/images/Logo.png',
            'objectSize': {
                'height': {
                    'magnitude': 100,
                    'unit': 'PT'
                },
                'width': {
                    'magnitude': 100,
                    'unit': 'PT'
                }
            }
        }
    }]

    body = {'requests': requests}
    response = service.documents().batchUpdate(
        documentId=DOCUMENT_ID, body=body).execute()
    insert_inline_image_response = response.get('replies')[0].get(
        'insertInlineImage')
    print('Inserted images at first character')

main()
