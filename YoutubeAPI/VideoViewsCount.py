import google_auth_oauthlib
import googleapiclient.discovery 
import googleapiclient.errors

vid = 'kJQP7kiw5Fk'
scopes = ['https://www.googleapis.com/auth/youtube.force-ssl']        

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
    if 'items' not in  response:
        main(request)
    data = response['items'][0]
    vid_snippet = data['snippet']
    title = vid_snippet['title']
    views = str(data['statistics']['viewCount']);
    print(title + ' has ' + views + ' views')

main(request)
