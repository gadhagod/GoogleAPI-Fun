# https://www.youtube.com/watch?v=clY8cSZbH5s
import google_auth_oauthlib.flow 
import googleapiclient.discovery 
import googleapiclient.errors
from time import sleep

vid = 'clY8cSZbH5s'
scopes = ['https://www.googleapis.com/auth/youtube.force-ssl']        

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

def update(vid_snippet):
    request = youtube.videos().update(
        part='snippet',
        body={'id': vid, 'snippet': vid_snippet}
    )
    request.execute()
    print('It worked!')

def main(request):
    while True:
        response = request.execute()
        print(response)
        if 'items' not in  response:
            main(request)

        data = response["items"][0]
        vid_snippet = data["snippet"];

        title = vid_snippet['title']
        description = vid_snippet['description']
        views = data['statistics']['viewCount']
        likes = data['statistics']['likeCount']
        dislikes = data['statistics']['dislikeCount']
        comments = data['statistics']['commentCount']

        description_upd = 'This video has ' +  likes + ' likes, ' + dislikes + ' dislikes, and  ' + comments + ' comments. \nSource code: https://github.com/gadhagod/GoogleAPI-Fun/YoutubeAPI/ThisVideoHas__Views.py'
        title_upd = 'This video has ' + views + ' views'

        if description_upd !=  description:
            vid_snippet['description'] = description_upd
            update(vid_snippet)
        if title_upd != title:
            vid_snippet['title'] = title_upd
            update(vid_snippet)
        sleep(7*60)
main(request)
