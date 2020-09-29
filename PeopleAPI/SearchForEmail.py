import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/contacts.readonly']

def main():
    creds = None
    
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('../client_secret.json', SCOPES) 
            creds = flow.run_local_server(port=0)
            
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('people', 'v1', credentials=creds)

    results = service.people().connections().list(
        resourceName='people/me',
        personFields='names,emailAddresses').execute()
    connections = results.get('connections', [])
    
    contactin = input('Contact full name: ')

    for person in connections:
        name = person.get('names', [])[0]['displayName']
        #print(name)
        emails = person.get('emailAddresses', [])
        if name == contactin:
            print(emails[0]['value'])
main()
