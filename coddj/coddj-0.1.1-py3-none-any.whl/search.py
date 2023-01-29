import os
from dotenv import load_dotenv
from googleapiclient.discovery import build


load_dotenv()
YOUTUBE_API_KEY = 'AIzaSyBCTrnuhtMuCaI4s101gGXO10a8I9VnbAA'

youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)


def search(query):
    request = youtube.search().list(
        part='id,snippet',
        q=query,
        maxResults=5,
        type='video'
    )

    response = request.execute()

    search_results = []

    for video in response['items']:
        title = video['snippet']['title']
        video_id = video['id']['videoId']
        item = {
            'name': title,
            'value': f"https://www.youtube.com/watch?v={video_id}"
        }

        search_results.append(item)

    return search_results
