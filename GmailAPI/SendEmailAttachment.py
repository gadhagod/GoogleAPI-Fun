import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from email.mime.text import MIMEText
from email.mime.image import MIMEImage   
from email.mime.multipart import MIMEMultipart
import mimetypes
import base64

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

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

    service = build('gmail', 'v1', credentials=creds)
    return service

def main():
    service = setup()
    file = '../images/Logo.png'
    
    to = input('Reciever\'s email: ')
    sender = input('Your email: ')
    subject = input('Subject: ')
    message_text = input('Message text: ')

    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    content_type, encoding = mimetypes.guess_type(file)
    
    if content_type is None or encoding is not None:
        content_type = 'application/octet-stream'
    main_type, sub_type = content_type.split('/', 1)
    if main_type == 'text':
        fp = open(file, 'rb')
        msg = MIMEText(fp.read(), _subtype=sub_type)
        fp.close()
    elif main_type == 'image':
        fp = open(file, 'rb')
        msg = MIMEImage(fp.read(), _subtype=sub_type)
        fp.close()
    elif main_type == 'audio':
        fp = open(file, 'rb')
        msg = MIMEAudio(fp.read(), _subtype=sub_type)
        fp.close()
    else:
        fp = open(file, 'rb')
        msg = MIMEBase(main_type, sub_type)
        msg.set_payload(fp.read())
        fp.close()

    msg.add_header('Content-Disposition', 'attachment', filename=file)
    message.attach(msg)
    
    m = {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}
    message = service.users().messages().send(userId='me', body=m).execute()
    print('Sent')

if __name__ == "__main__": 
    main()
