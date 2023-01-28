# encoding = utf-8

import base64
import binascii
import json
import random
import string
from urllib import parse
import requests
from Crypto.Cipher import AES
from retrying import retry


def get_random():
    random_str = ''.join(random.sample(string.ascii_letters + string.digits, 16))
    return random_str


def len_change(text):
    pad = 16 - len(text) % 16
    text = text + pad * chr(pad)
    text = text.encode("utf-8")
    return text


def aes(text, key):
    iv = b'0102030405060708'
    text = len_change(text)
    cipher = AES.new(key.encode(), AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(text)
    encrypt = base64.b64encode(encrypted).decode()
    return encrypt


def b(text, str_g):
    first_data = aes(text, '0CoJUm6Qyw8W8jud')
    second_data = aes(first_data, str_g)
    return second_data


def c(text):
    e = '010001'
    f = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb' \
        '7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf6952801' \
        '04e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575' \
        'cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
    text = text[::-1]
    result = pow(int(binascii.hexlify(text.encode()), 16), int(e, 16), int(f, 16))
    return format(result, 'x').zfill(131)


def get_final_param(text, str_g):
    params = b(text, str_g)
    return {'params': params, 'encSecKey': c(str_g)}


def get_music_list(params, enc_sec_key):
    url = "https://music.163.com/weapi/cloudsearch/get/web?csrf_token="

    payload = 'params=' + parse.quote(params) + '&encSecKey=' + parse.quote(enc_sec_key)
    headers = {
        'authority': 'music.163.com',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,'
                      ' like Gecko) Chrome/84.0.4147.135 Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded',
        'accept': '*/*',
        'origin': 'https://music.163.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://music.163.com/search/',
        'accept-language': 'zh-CN,zh;q=0.9',
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.text


def get_reply(params, enc_seckey):
    url = "https://music.163.com/weapi/song/enhance/player/url/v1?csrf_token="
    payload = 'params=' + parse.quote(params) + '&encSecKey=' + parse.quote(enc_seckey)
    headers = {
        'authority': 'music.163.com',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,'
                      ' like Gecko) Chrome/84.0.4147.135 Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded',
        'accept': '*/*',
        'origin': 'https://music.163.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://music.163.com/',
        'accept-language': 'zh-CN,zh;q=0.9'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.text


def get_wyy_song_dict(song_name):
    try:
        d = json.dumps({"hlpretag": "<span class=\"s-fc7\">", "hlposttag": "</span>", "s": song_name,
                        "type": "1", "offset": "0", "total": "true", "limit": "30", "csrf_token": ""})
        random_param = get_random()
        param = get_final_param(d, random_param)
        song_list = get_music_list(param['params'], param['encSecKey'])
        if len(song_list) > 0:
            num = 1
            song_dict = {}
            song_list = json.loads(song_list)['result']['songs']
            for i, item in enumerate(song_list):
                param = get_final_param(json.dumps({"ids": "[" + str(item["id"]) + "]", "level": "standard",
                                                    "encodeType": "", "csrf_token": ""}), random_param)
                song_info = get_reply(param['params'], param['encSecKey'])
                song_info = json.loads(song_info)
                if song_info["data"][0]["url"] is None:
                    continue
                song = dict({})
                song["music_name"] = item["name"].replace("'", "’")
                song["music_artist"] = item["ar"][0]["name"]
                song["music_album"] = item["al"]["name"]
                song["music_picUrl"] = item['al']["picUrl"]
                song["music_id"] = song_info["data"][0]["id"]
                song["music_url"] = song_info["data"][0]["url"]
                song_dict[str(num)] = song
                num += 1
            return song_dict
        else:
            return None
    except:
        return None

@retry(stop_max_attempt_number=5)
def get_kw_music_dict(song_name):
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept - encoding': 'gzip, deflate',
        'accept - language': 'zh - CN, zh;q = 0.9',
        'cache - control':'no - cache',
        'Connection': 'keep-alive',
        'csrf': 'HH3GHIQ0RYM',
        'Referer': 'http://www.kuwo.cn/search/list?key=%E5%91%A8%E6%9D%B0%E4%BC%A6',
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/99.0.4844.51 Safari/537.36',
        'Cookie': '_ga=GA1.2.218753071.1648798611; _gid=GA1.2.144187149.1648798611; _gat=1; '
                  'Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1648798611; '
                  'Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1648798611; kw_token=HH3GHIQ0RYM'
    }
    search_url = "http://www.kuwo.cn/api/www/search/searchMusicBykeyWord"
    search_data = {
        'key': song_name,
        'pn': '1',
        'rn': '80',
        'httpsStatus': '1',
        'reqId': '858597c1-b18e-11ec-83e4-9d53d2ff08ff'
    }
    num = 1
    song_dict = {}
    song_list = requests.get(search_url, params=search_data, headers=headers, timeout=20).json()
    songs_req_id = song_list["reqId"]
    if song_list["data"]["list"] == []:
        return None
    for item in song_list["data"]["list"]:
        try:
            song = dict({})
            song_rid = item["rid"]
            music_url = 'http://www.kuwo.cn/api/v1/www/music/playUrl?mid={}&type=convert_url3' \
                        '&httpsStatus=1&reqId={}'\
                        .format(song_rid, songs_req_id)
            response_data = requests.get(music_url).json()
            song["music_name"] = item["name"]
            song["music_artist"] = item["artist"]
            song["music_album"] = item["album"]
            song["music_picUrl"] = item["pic"]
            song["music_id"] = song_rid
            song["music_url"] = response_data["data"]["url"]
            song_dict[str(num)] = song
            num += 1
        except:
            continue
    return song_dict
get_kw_music_dict("孤勇者")