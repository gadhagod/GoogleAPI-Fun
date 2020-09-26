import google_auth_oauthlib
import googleapiclient.discovery 
import googleapiclient.errors
import pprint
from time import sleep
import os

vid = 'kJQP7kiw5Fk'
scopes = ['https://www.googleapis.com/auth/youtube.force-ssl']        

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
api_service_name = 'youtube'
api_version = 'v3'
client_secret = '../client_secret.json'
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secret, scopes)
cred = flow.run_console()
youtube = googleapiclient.discovery.build(
    api_service_name, api_version, credentials=cred
)
request = youtube.videos().list(
    part='snippet,statistics',
    id=vid
)

def main(request):
    response = request.execute()
    print(response)
    if 'items' not in  response:
        main(request)
    data = response['items'][0]
    vid_snippet = data['snippet']
    title = vid_snippet['title']
    likes = str(data['statistics']['likeCount']);
    print(title + ' has ' + likes + ' likes')

main(request)
