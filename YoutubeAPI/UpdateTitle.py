import os
import google_auth_oauthlib.flow 
import googleapiclient.discovery 
import googleapiclient.errors
import pprint
from time import sleep

vid = 'clY8cSZbH5s'
scopes = ['https://www.googleapis.com/auth/youtube.force-ssl']        

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
api_service_name = 'youtube'
api_version = 'v3'
client_secret = '../client_secret.json'
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secret, scopes)
credentials = flow.run_console()
youtube = googleapiclient.discovery.build(
    api_service_name, api_version, credentials=credentials
)
request = youtube.videos().list(
    part='snippet,statistics',
    id=vid
)

def main(request):
    response = request.execute()
    if 'items' not in  response:
        main(request)
    data = response['items'][0]
    vid_snippet = data['snippet']
    title = vid_snippet['title']
    title_upd = 'This title was made using the Youtube API'
    vid_snippet['title'] = title_upd
    request = youtube.videos().update(
        part='snippet',
        body={
            'id': vid,
            'snippet': vid_snippet
        }
    )
    response = request.execute()
    print('It worked!')

main(request)
