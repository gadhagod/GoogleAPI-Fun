import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def main():
    insummary = input('Event Name: ')
    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    events_result = service.events().list(calendarId='primary', singleEvents=True,
                                        orderBy='startTime').execute()['items']
    for item in events_result:
        if item['summary'] == insummary:
            print('ID: ' + item['id'])
            print('Link: ' + item['htmlLink'])
            print('Created: ' + item['created'])
            print('Last updated: ' + item['updated'])
            print('Starts: ' + item['start']['dateTime'])
            print('Ends: ' + item['end']['dateTime'])
            print('Organizer: ' + item['organizer']['email'])
main()

