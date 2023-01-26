# import pafy
# from youtubesearchpython import *
# playlist = pafy.all_playlists_from_channel('UC_aEa8K-EOJ3D6gOs7HcyNg')
# print(playlist)
# # https://www.youtube.com/watch?v=aNGKy1Czctc - video pops up for this

import os
from yt_dlp import YoutubeDL

ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': os.path.join('/tmp', '%(title)s-%(id)s.%(ext)s'),
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}
url = 'https://www.youtube.com/watch?v=Yc1YtCHrK0w'
# with YoutubeDL(ydl_opts) as ydl:
#     ydl.download([url])


with YoutubeDL({'format':'137'}) as ydl:
    ydl.download([url])

