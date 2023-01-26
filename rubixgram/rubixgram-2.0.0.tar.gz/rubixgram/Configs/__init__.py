import datetime
import pytz
from time import sleep, time
from requests import post, get
from asyncio import run
from re import findall
from random import randint, choice
from json import dumps, loads
from datetime import datetime
from colorama import Fore
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode , urlsafe_b64decode

web = {'app_name': 'Main', 'app_version': '4.0.8', 'platform': 'Web', 'package': 'web.rubika.ir', 'lang_code': 'fa'}

android = {'app_name': 'Main', 'app_version': '3.0.9', 'platform': 'Android', 'package': 'app.rbmain.a', 'lang_code': 'fa'}

class encryptio:
    def __init__(self, auth):
        self.key = bytearray(self.secret(auth), "UTF-8")
        self.iv = bytearray.fromhex('00000000000000000000000000000000')

    def replaceCharAt(self, e, t, i):
        return e[0:t] + i + e[t + len(i):]

    def secret(self, e):
        t = e[0:8]
        i = e[8:16]
        n = e[16:24] + t + e[24:32] + i
        s = 0
        while (s < len(n)):
            e = n[s]
            if e >= '0' and e <= '9':
                t = chr((ord(e[0]) - ord('0') + 5) % 10 + ord('0'))
                n = self.replaceCharAt(n, s, t)
            else:
                t = chr((ord(e[0]) - ord('a') + 9) % 26 + ord('a'))
                n = self.replaceCharAt(n, s, t)
            s += 1
        return n

    def encrypt(self, text):
        return b64encode(AES.new(self.key, AES.MODE_CBC, self.iv).encrypt(pad(text.encode('UTF-8'), AES.block_size))).decode('UTF-8')

    def decrypt(self, text):
        return unpad(AES.new(self.key, AES.MODE_CBC, self.iv).decrypt(urlsafe_b64decode(text.encode('UTF-8'))),AES.block_size).decode('UTF-8')
        
class welcome:
        ir = pytz.timezone("Asia/Tehran")
        time = f"{datetime.now(ir).strftime(f'[{Fore.LIGHTMAGENTA_EX}%H:%M:%S{Fore.LIGHTWHITE_EX}]')}"
        text : str = f"{Fore.LIGHTWHITE_EX}rubixgram library version ({Fore.LIGHTCYAN_EX}2.0.0{Fore.LIGHTWHITE_EX})\n\n{Fore.LIGHTWHITE_EX}StArT > {time} {Fore.LIGHTWHITE_EX}[#] <~> Mr. DaRk <{Fore.LIGHTBLUE_EX}@rubixgram{Fore.LIGHTWHITE_EX}> <~>\n\n. . . . . . . . . . . . .\n\n"
        for txt in text:
        	print(txt, flush=True, end='')
        	sleep(0.0060)