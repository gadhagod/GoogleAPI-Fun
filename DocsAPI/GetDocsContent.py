from apiclient import discovery
from httplib2 import Http
from oauth2client import client
from oauth2client import file
from oauth2client import tools

SCOPES = 'https://www.googleapis.com/auth/documents.readonly'
DISCOVERY_DOC = 'https://docs.googleapis.com/$discovery/rest?version=v1'
DOCUMENT_ID = input('Doc id: ')

def get_credentials():
    store = file.Storage('token.json')
    credentials = store.get()

    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets('../client_secret.json', SCOPES)
        credentials = tools.run_flow(flow, store)
    return credentials


def read_strucutural_elements(elements):
    text = ''
    for value in elements:
        if 'paragraph' in value:
            elements = value.get('paragraph').get('elements')
            for elem in elements:
                text += read_paragraph_element(elem)
        elif 'table' in value:
            table = value.get('table')
            for row in table.get('tableRows'):
                cells = row.get('tableCells')
                for cell in cells:
                    text += read_strucutural_elements(cell.get('content'))
        elif 'tableOfContents' in value:
            toc = value.get('tableOfContents')
            text += read_strucutural_elements(toc.get('content'))
    return text

def main():
    credentials = get_credentials()
    http = credentials.authorize(Http())
    service = discovery.build('docs', 'v1', http=http, discoveryServiceUrl=DISCOVERY_DOC)
    doc = service.documents().get(documentId=DOCUMENT_ID).execute()
    print(doc['body']['content'][1]['paragraph']['elements'][1]['textRun']['content'])

main()
