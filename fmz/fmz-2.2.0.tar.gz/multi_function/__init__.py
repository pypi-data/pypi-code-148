from .requests_download import download
from .bot import chat
from .qr import makeqr
from .pinyin import pin, pin1, duoyin
from .translate import zh2en, en2zh, translate
from .get_music import get_wyy_song_dict, get_kw_music_dict
from .WordCloud import wcloud
from .send_email import send_email
from easygui import msgbox, fileopenbox, buttonbox, ynbox, ccbox
from turtle import *
from datetime import datetime
import os
from requests import get


__version__ = "2.2.0"
directory = (os.path.split(os.path.realpath(__file__))[0]).split("\\")
directory = "/".join(directory)+"/"

if os.path.exists(directory+"font") == False:
    os.mkdir(directory+"font")
if os.path.exists(directory+"font/simfang.ttf") == False:
    c = get("https://fumingzhe.mynatapp.cc/static/fonts/simfang.ttf").content
    f = open(directory+"font/simfang.ttf", "wb")
    f.write(c)
    f.close()