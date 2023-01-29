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

class color:
      red = '\033[91m'
      green = '\033[92m'
      blue = '\033[94m'
      yellow = '\033[93m'
      magenta = '\033[95m'
      cyan = '\033[96m'
      white = '\033[97m'
      bold = '\033[1m'
      underline = '\033[4m'
      black='\033[30m'
 
class welcome:
        ir = pytz.timezone("Asia/Tehran")
        time = f"{datetime.now(ir).strftime(f'{Fore.LIGHTYELLOW_EX}[{Fore.LIGHTMAGENTA_EX}%H:%M:%S{Fore.LIGHTYELLOW_EX}]')}"

class chup:
      iLiaShah = f"""{color.bold}
{color.white} 〔༄〕- {color.cyan} 𝗶𝗟𝗶𝗮𝗦𝗵𝗮𝗵 {color.magenta} 𝗩𝗲𝗿𝘀𝗶𝗼𝗻  {color.yellow}3.8.1    

{color.white} 〔༄〕- {color.cyan} 𝗶𝗟𝗶𝗮𝗦𝗵𝗮𝗵 {color.magenta} 𝙲𝚘𝚙𝚢𝚁𝚒𝚐𝚑𝚝 (𝙲) {color.yellow} 2023 {color.red} 𝗶𝗟𝗶𝗮𝗦𝗵𝗮𝗵   

{color.white} 〔༄〕- {color.cyan} 𝗥𝘂𝗯𝗶𝗸𝗮{color.magenta} 𝗖𝗵𝗮𝗻𝗲𝗹𝗹  {color.yellow} @𝚂𝚘𝚞𝚛𝚜𝚎_𝚙𝚢

{color.white} 〔༄〕- {color.cyan} 𝗧𝗶𝗺𝗲 {color.magenta}{welcome.time}

{color.white}⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁
"""
      print(iLiaShah)
        	
for x in range(3):
    for i in ("⢿", "⣻", "⣽", "⣾", "⣷", "⣯", "⣟", "⡿"):
        sleep(0.1)
        if x == 10:
            print('',end='')
            break
        else:
            print( color.magenta+'   𝗟𝗶𝗯𝗿𝗮𝗿𝘆 𝗶𝗟𝗶𝗮𝗦𝗵𝗮𝗵 𝗣𝗹𝗲𝗮𝘀𝗲 𝗪𝗮𝗶𝘁....',color.cyan+i,end='\r')
print(color.white+"\n")

