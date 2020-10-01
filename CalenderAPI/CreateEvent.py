import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/calendar']

def setup():
    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '../client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    return service
    
service = setup()
summary = input('Event name: ')
location = input('Location: ')
description = input('Description: ')
start = input('Start time (PST): ')
end = input('End time (PST): ')

event = {
  'summary': summary,
  'location': location,
  'description': description,
  'start': {
    'dateTime': start,
    'timeZone': 'America/Los_Angeles',
  },
  'end': {
    'dateTime': end,
    'timeZone': 'America/Los_Angeles',
  },
  'recurrence': [
    'RRULE:FREQ=DAILY;COUNT=2'
  ],
  'attendees': [],
  'reminders': {
    'useDefault': False,
    'overrides': [],
  }
}

event = service.events().insert(calendarId='primary', body=event).execute()
print ('Event created: %s' % (event.get('htmlLink')))
