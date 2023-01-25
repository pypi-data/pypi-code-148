# Codded By Ariful Islam Arman (ARU)
# writen With python
import os, time, json, sys, random, string, webbrowser, uuid
try:
    from fpdf import FPDF
except:
    os.system('pip install fpdf2')
try:
    from googletrans import Translator, constants
    from pprint import pprint
except:
    os.system('pip install googletrans==3.1.0a0')
    from googletrans import Translator, constants
    from pprint import pprint
translator = Translator()
# color
# Color Value
blueVal = "94m"
redVal = "91m"
greenVal = "32m"
whiteVal = "97m"
yellowVal = "93m"
cyanVal = "96m"
# normal
normal = "\33["
# Bold
bold = "\033[1;"
# italic
italic = "\x1B[3m"
# Color Normal
blue = normal + blueVal  # Blue Color Normal
red = normal + redVal  # Red Color Normal
green = normal + greenVal  # Green Color Normal
white = normal + whiteVal  # white Color Normal
yellow = normal + yellowVal  # yellow Color Normal
cyan = normal + cyanVal  # Cyan Color Normal
# Color Bold
blueBold = bold + blueVal  # Blue Color Bold
redBold = bold + redVal  # Red Color Bold
greenBold = bold + greenVal  # Green Color Bold
whiteBold = bold + whiteVal  # white Color Bold
yellowBold = bold + yellowVal  # yellow Color Bold
cyanBold = bold + cyanVal  # Cyan Color Bold
# color end
end = '\033[0m'
colorArr = ["\033[1;91m", "\033[1;92m", "\033[1;93m", "\033[1;94m", "\033[1;95m", "\033[1;96m"]
# Char Print
def printchar(w, t):  # w=word and t =time
    for word in w + '\n':
        sys.stdout.write(word)
        sys.stdout.flush()
        time.sleep(t)
# Import All Module
try:
    import requests
except:
    printchar(cyanBold + "installing requests.....", 0.05)
    time.sleep(2)
    os.system("pip install requests")
    import requests
    printchar(greenBold + "requests successfully installed.....", 0.05)
    time.sleep(2)
    os.system('clear')
def banner():
    a = random.choice(colorArr)
    r = random.choice(colorArr)
    u = random.choice(colorArr)
    logo = f'''


{a}	 █████╗   {r}  ██████╗  {u}   ██╗   ██╗
{a}	██╔══██╗  {r}  ██╔══██╗ {u}   ██║   ██║
{a}	███████║  {r}  ██████╔╝ {u}   ██║   ██║
{a}	██╔══██║  {r}  ██╔══██╗ {u}   ██║   ██║
{a}	██║  ██║  {r}  ██║  ██║ {u}   ╚██████╔╝
{a}	╚═╝  ╚═╝  {r}  ╚═╝  ╚═╝ {u}    ╚═════╝ 
	'''
    infoC = random.choice(colorArr)
    toolsInfo = f'''{infoC}
    ╔════════════════════════════════════╗
    ║        {random.choice(colorArr)}BD NID INFORMATION {infoC}         ║
    ║     {random.choice(colorArr)}AUTHOR: ARIFUL ISLAM ARMAN {infoC}    ║
    ║          {random.choice(colorArr)}STATUS : PAID    {infoC}         ║
    ╚════════════════════════════════════╝
    '''
    os.system("clear")
    print(logo)
    print(toolsInfo)



def get_info_from_server_bd_pollice_user_aru_():
    os.system('clear')
    banner()
    nid = input(f'\n     {greenBold}ENTER NID: {cyanBold}')
    dob = input(f'\n     {greenBold}ENTER DATE OF BIRTH [YYYY-MM-DD]: {cyanBold}')
    if nid != "" or dob != "":
        os.system('cd')
        os.chdir('/storage/emulated/0')
        if nid.isnumeric():
            try:
                from requests.structures import CaseInsensitiveDict
                url = "http://gd.police.gov.bd/api/NationalIdentityinfo/GetInfoForApp"
                headers = CaseInsensitiveDict()
                headers["Content-Type"] = "application/json"
                headers["User-Agent"] = "Dalvik/2.1.0 (Linux; U; Android 7.1.2; G011A Build/N2G48H)"
                data = '{"nid":"'+nid+'","dob":"'+dob+'","callName":"NIDVerifyAlok"}'
                resp = requests.post(url, headers=headers, data=data)
                if resp.status_code == 200:
                    path_pdf = '/storage/emulated/0/ARU/' + nid + '-'+ resp.json()['nidInfo']['success']['data']['nameEn']+'/'
                    # create
                    pdf = FPDF('P', 'mm', (210, 530))
                    #get font
                    pdf.add_font('Nikosh', '', '/data/data/com.termux/files/home/NID_INFO/NikoshBAN.ttf')
                    pdf.set_font('helvetica', 'BU', 35)
                    pdf.add_page()
                    pdf.set_text_color(247, 125, 24)
                    pdf.cell(25, 0)
                    pdf.cell(0, 30, 'NID INFO BANGLADESH')
                    pdf.ln(2)
                    pdf.image('/data/data/com.termux/files/home/NID_INFO/background.png', x=30, y=120, w=170, h=170, type='', link='')
                    pdf.set_margins(0, 0, 0)
                    try:
                        os.chdir(path_pdf)
                        try:
                            pdf.image(nid + '.jpg', x=75, y=38, w=60, h=60, type='', link='')
                        except:
                            img_data = requests.get(resp.json()['nidInfo']['success']['data']['photo']).content
                            with open('aru-'+nid + '.jpg', 'wb') as handler:
                                handler.write(img_data)
                            pdf.image(nid + '.jpg', x=75, y=38, w=60, h=60, type='', link='')


                    except:
                        os.makedirs(path_pdf)
                        os.chdir(path_pdf)
                        try:
                            pdf.image(nid + '.jpg', x=75, y=38, w=60, h=60, type='', link='')
                        except:
                            img_data = requests.get(resp.json()['nidInfo']['success']['data']['photo']).content
                            with open(nid + '.jpg', 'wb') as handler:
                                handler.write(img_data)
                            pdf.image(nid + '.jpg', x=75, y=38, w=60, h=60, type='', link='')

                    try:
                    	os.chdir(path_pdf)
                    	try:
                    		nid_info_json = open('aru-'+nid+'.txt','r')
                    		nid_info_json.write(json.dumps(json.loads(resp.text),indent=1,ensure_ascii=False))
                    		nid_info_json.close()
                    	except:
                    		nid_info_json = open('aru-'+nid+'.txt','x')
                    		nid_info_json.write(json.dumps(json.loads(resp.text),indent=1,ensure_ascii=False))
                    		nid_info_json.close()
                    except:
                    	try:
                    		os.makedirs(path_pdf)
                    		os.chdir(path_pdf)
                    		nid_info_json = open('aru-'+nid+'.txt','x')
                    		nid_info_json.write(json.dumps(json.loads(resp.text),indent=1,ensure_ascii=False))
                    		nid_info_json.close()
                    	except:
                    		os.chdir(path_pdf)
                    		nid_info_json = open('aru-'+nid+'.txt','r')
                    		nid_info_json.write(json.dumps(json.loads(resp.text),indent=1,ensure_ascii=False))
                    		nid_info_json.close()


                    try:
                        # Name EN
                        pdf.set_text_color(0, 0, 0)
                        nameEn = resp.json()['nidInfo']['success']['data']['nameEn']
                        pdf.set_font('helvetica', '', 25)
                        pdf.cell(25, 0)
                        pdf.cell(0, 210, 'Name: ')
                        pdf.ln(1)
                        pdf.set_font('helvetica', 'B', 25)
                        pdf.cell(55, 0)
                        pdf.cell(0, 208, nameEn)
                        pdf.ln(11)
                    except:
                        pass

                    try:
                        # Father
                        father = resp.json()['nidInfo']['success']['data']['father']
                        pdf.set_font('helvetica', '', 25)
                        pdf.set_text_color(0, 0, 0)
                        pdf.cell(25, 0)
                        pdf.cell(0, 220, 'Father: ')
                        pdf.ln(1)
                        pdf.cell(56, 0)
                        pdf.cell(0, 218, translator.translate(father).text)
                        pdf.ln(14)
                    except:
                        pass

                    try:
                        # Mother
                        mother = resp.json()['nidInfo']['success']['data']['mother']
                        pdf.set_font('helvetica', '', 25)
                        pdf.set_text_color(0, 0, 0)
                        pdf.cell(25, 0)
                        pdf.cell(0, 220, 'Mother: ')
                        pdf.ln(1)
                        pdf.cell(57, 0)
                        pdf.cell(0, 218, translator.translate(mother).text)
                        pdf.ln(12)
                    except:
                        pass

                    try:
                        # spouse
                        spouse = resp.json()['nidInfo']['success']['data']['spouse']
                        if spouse != '':
                            pdf.set_font('helvetica', '', 25)
                            pdf.set_text_color(0, 0, 0)
                            pdf.cell(25, 0)
                            pdf.cell(0, 225, 'Spouse: ')
                            pdf.ln(1)
                            pdf.set_font('Nikosh', '', 30)
                            pdf.cell(59, 0)
                            pdf.cell(0, 223, translator.translate(spouse).text)
                            pdf.ln(12)
                        else:
                            pass
                    except:
                        pass

                    try:
                        dateOfBirth = resp.json()['nidInfo']['success']['data']['dateOfBirth']
                        year = dateOfBirth[:4]
                        month_m = dateOfBirth[5:7]
                        date = dateOfBirth[9:11]
                        if month_m == '01':
                            month = "January"
                        elif month_m == '02':
                            month = "February"
                        elif month_m == '03':
                            month = "March"
                        elif month_m == '04':
                            month = "April"
                        elif month_m == '05':
                            month = "May"
                        elif month_m == '06':
                            month = "June"
                        elif month_m == '07':
                            month = "July"
                        elif month_m == '08':
                            month = "August"
                        elif month_m == '09':
                            month = "September"
                        elif month_m == '10':
                            month = "October"
                        elif month_m == '11':
                            month = "November"
                        elif month_m == '12':
                            month = "December"
                        else:
                            month = month_m
                        # DOB
                        pdf.set_font('helvetica', '', 25)
                        pdf.set_text_color(0, 0, 0)
                        pdf.cell(25, 0)
                        pdf.cell(0, 230, 'Date of Birth: ')
                        pdf.ln(1)
                        pdf.set_text_color(255, 0, 0)
                        pdf.cell(78, 0)
                        pdf.cell(0, 228, date + ' ' + month + ' ' + year)
                        pdf.ln(11)
                    except:
                        pass

                    try:
                        nationalId = resp.json()['nidInfo']['success']['data']['nationalId']
                        # NID No
                        pdf.set_font('helvetica', 'B', 25)
                        pdf.set_text_color(0, 0, 0)
                        pdf.cell(25, 0)
                        pdf.cell(0, 240, 'ID NO: ')
                        pdf.ln(1)
                        pdf.set_font('helvetica', 'B', 29)
                        pdf.set_text_color(255, 0, 0)
                        pdf.cell(55, 0)
                        pdf.cell(0, 238, nationalId)
                        pdf.ln(11)
                    except:
                        pass

                    try:
                        # Blood Group
                        bloodGroup = resp.json()['nidInfo']['success']['data']['bloodGroup']
                        if bloodGroup != "":
                            pdf.set_font('helvetica', '', 25)
                            pdf.set_text_color(0, 0, 0)
                            pdf.cell(25, 0)
                            pdf.cell(0, 245, 'Blood Group: ')
                            pdf.ln(1)
                            pdf.set_text_color(255, 0, 0)
                            pdf.cell(78, 0)
                            pdf.cell(0, 243, bloodGroup)
                            pdf.ln(11)
                        else:
                            pass
                    except:
                        pass

                    # Permanent Address
                    try:
                        division = resp.json()['nidInfo']['success']['data']['permanentAddress']['division']
                        if division != "":
                            # Divition
                            pdf.set_font('Nikosh', '', 25)
                            pdf.set_text_color(0, 0, 0)
                            pdf.cell(25, 0)
                            pdf.cell(0, 255, 'Divition: ')
                            pdf.ln(1)
                            pdf.cell(65, 0)
                            pdf.cell(0, 252, translator.translate(division).text)
                            pdf.ln(11)
                        else:
                            pass
                    except:
                        pass

                    try:
                        district = resp.json()['nidInfo']['success']['data']['permanentAddress']['district']
                        if district != '':
                            # District
                            pdf.set_font('Nikosh', '', 25)
                            pdf.set_text_color(0, 0, 0)
                            pdf.cell(25, 0)
                            pdf.cell(0, 260, 'District: ')
                            pdf.ln(1)
                            pdf.cell(65, 0)
                            pdf.cell(0, 258, translator.translate(district).text)
                            pdf.ln(11)
                        else:
                            pass
                    except:
                        pass

                    try:
                        # Ufozila
                        upozila = resp.json()['nidInfo']['success']['data']['permanentAddress']['upozila']
                        if upozila != '':
                            pdf.set_font('Nikosh', '', 25)
                            pdf.set_text_color(0, 0, 0)
                            pdf.cell(25, 0)
                            pdf.cell(0, 265, 'Ufozila: ')
                            pdf.ln(1)
                            pdf.cell(65, 0)
                            pdf.cell(0, 263, translator.translate(upozila).text)
                            pdf.ln(11)
                        else:
                            pass
                    except:
                        pass

                    try:
                        # unionOrWard
                        unionOrWard = resp.json()['nidInfo']['success']['data']['permanentAddress']['unionOrWard']
                        if unionOrWard != '':
                            pdf.set_font('Nikosh', '', 25)
                            pdf.set_text_color(0, 0, 0)
                            pdf.cell(25, 0)
                            pdf.cell(0, 270, 'Union or Ward: ')
                            pdf.ln(1)
                            pdf.cell(95, 0)
                            pdf.cell(0, 268, translator.translate(unionOrWard).text)
                            pdf.ln(11)
                        else:
                            pass
                    except:
                        pass

                    try:

                        # postOffice
                        postOffice = resp.json()['nidInfo']['success']['data']['permanentAddress']['postOffice']
                        if postOffice != '':
                            pdf.set_font('Nikosh', '', 25)
                            pdf.set_text_color(0, 0, 0)
                            pdf.cell(25, 0)
                            pdf.cell(0, 275, 'Post Office: ')
                            pdf.ln(1)
                            pdf.cell(80, 0)
                            pdf.cell(0, 273, translator.translate(postOffice).text)
                            pdf.ln(11)
                        else:
                            pass
                    except:
                        pass

                    try:
                        # postalCode
                        postalCode = resp.json()['nidInfo']['success']['data']['permanentAddress']['postalCode']
                        if postalCode != '':
                            pdf.set_font('Nikosh', '', 25)
                            pdf.set_text_color(0, 0, 0)
                            pdf.cell(25, 0)
                            pdf.cell(0, 275, 'Postal Code: ')
                            pdf.ln(1)
                            pdf.cell(80, 0)
                            pdf.cell(0, 273, translator.translate(postalCode).text)
                            pdf.ln(11)
                    except:
                        pass

                    try:
                        # MouzaOrMoholla
                        additionalMouzaOrMoholla = resp.json()['nidInfo']['success']['data']['permanentAddress'][
                            'additionalMouzaOrMoholla']
                        if additionalMouzaOrMoholla != '':
                            pdf.set_font('Nikosh', '', 25)
                            pdf.set_text_color(0, 0, 0)
                            pdf.cell(25, 0)
                            pdf.cell(25, 275, 'Mouza Or Moholla: ')
                            pdf.ln(2)
                            pdf.cell(110, 0)
                            pdf.cell(0, 273, translator.translate(additionalMouzaOrMoholla).text)
                            pdf.ln(11)
                        else:
                            pass
                    except:
                        pass

                    # try:
                    #	#VillageOrRoad
                    #	additionalVillageOrRoad = resp.json()['nidInfo']['success']['data']['permanentAddress']['additionalVillageOrRoad']
                    #	if additionalVillageOrRoad == "":
                    #		pass
                    #	else:
                    #		try:
                    #			pdf.set_font('Nikosh', '', 25)
                    #			pdf.set_text_color(0,0,0)
                    #			pdf.cell(25,0)
                    #			pdf.cell(0, 277, 'Village Or Road: ')
                    #			pdf.ln(1)
                    #			pdf.cell(105,0)
                    #			pdf.cell(0,275,translator.translate(additionalVillageOrRoa).text)
                    #			pdf.ln(11)
                    #		except:
                    #			pass
                    # except:
                    #	pass

                    try:
                        # homeOrHoldingNo
                        homeOrHoldingNo = resp.json()['nidInfo']['success']['data']['permanentAddress'][
                            'homeOrHoldingNo']
                        if homeOrHoldingNo != "":
                            pdf.set_font('Nikosh', '', 25)
                            pdf.set_text_color(0, 0, 0)
                            pdf.cell(25, 0)
                            pdf.cell(0, 275, 'Home: ')
                            pdf.ln(1)
                            pdf.cell(55, 0)
                            pdf.cell(0, 273, translator.translate(homeOrHoldingNo).text)
                            pdf.ln(11)
                        else:
                            pass
                    except:
                        pass

                    try:
                        # voterArea
                        voterArea = resp.json()['nidInfo']['success']['data']['voterArea']
                        if voterArea != "":
                            pdf.set_font('Nikosh', '', 25)
                            pdf.set_text_color(0, 0, 0)
                            pdf.cell(25, 0)
                            pdf.cell(0, 280, 'Voter Area: ')
                            pdf.ln(1)
                            pdf.cell(80, 0)
                            pdf.cell(0, 278, translator.translate(voterArea).text)
                            pdf.ln(11)
                        else:
                            pass
                    except:
                        pass

                    try:
                        religion = resp.json()['nidInfo']['success']['data']['religion']
                        # religion
                        if religion != "":
                            pdf.set_font('Nikosh', '', 25)
                            pdf.set_text_color(0, 0, 0)
                            pdf.cell(25, 0)
                            pdf.cell(0, 285, 'Religion: ')
                            pdf.ln(1)
                            pdf.cell(67, 0)
                            pdf.cell(0, 283, religion)
                            pdf.ln(11)
                        else:
                            pass

                    except:
                        pass
                    try:
                        # mobile
                        mobile = resp.json()['nidInfo']['success']['data']['mobile']
                        if mobile != "":
                            pdf.set_font('helvetica', '', 25)
                            pdf.set_text_color(0, 0, 0)
                            pdf.cell(25, 0)
                            pdf.cell(0, 290, 'Mobile: ')
                            pdf.ln(1)
                            pdf.cell(57, 0)
                            pdf.cell(0, 288, mobile)
                            pdf.ln(11)
                        else:
                            pass
                    except:
                        pass
                    try:
                        nidFather = resp.json()['nidInfo']['success']['data']['nidFather']
                        # nidFather
                        if nidFather != '':
                            pdf.set_font('helvetica', 'B', 25)
                            pdf.set_text_color(0, 0, 0)
                            pdf.cell(25, 0)
                            pdf.cell(0, 295, 'NID Father: ')
                            pdf.ln(1)
                            pdf.set_font('helvetica', 'B', 29)
                            pdf.set_text_color(255, 0, 0)
                            pdf.cell(77, 0)
                            pdf.cell(0, 293, nidFather)
                            pdf.ln(11)
                        else:
                            pass
                    except:
                        pass

                    try:
                        nidMother = resp.json()['nidInfo']['success']['data']['nidMother']
                        if nidMother != '':
                            # nidMother
                            pdf.set_font('helvetica', 'B', 25)
                            pdf.set_text_color(0, 0, 0)
                            pdf.cell(25, 0)
                            pdf.cell(0, 300, 'NID Mother: ')
                            pdf.ln(1)
                            pdf.set_font('helvetica', 'B', 29)
                            pdf.set_text_color(255, 0, 0)
                            pdf.cell(77, 0)
                            pdf.cell(0, 298, nidMother)
                            pdf.ln(11)
                        else:
                            pass
                    except:
                        pass
                    pdf.output(nid+'-aru.pdf')
                    printchar(f'    {greenBold}YOUR NID INFO SAVED {cyanBold}{path_pdf} {end}',0.1)
                    printchar(f'    {greenBold}There might be something wrong with the PDF so I would suggest you look at the details in the{cyanBold} {nid}.txt {greenBold} file {end}',0.1)
                    
                else:
                    printchar(f'    {redBold}NID NOT FOUND DATABASE SERVER {end}',0.1)
            except:
                print(f"     {redBold}PLEASE MAKE SURE INTERNET CONNECTION{end}")
def linux():
    try:
    	aproved = str.split(requests.get('https://raw.githubusercontent.com/Aru-Is-Always-King/nid_data/main/aprove.txt').text)
    except:
    	print(redBold+'     NO INTERNET')
    global text
    present_dir = os.getcwd()
    new_path = '.users/.data/.verify/.users/.aprove'
    path = os.path.join(present_dir, new_path)
    text = uuid.uuid4()
    try:
    	os.chdir(path)
    	try:
    		openFile = open('.myID.txt','r')
    		myID = openFile.read()
    		openFile.close()
    		if myID != "":
    			text = myID
    		else:
    			openFile = open('.myID.txt','w')
    			openFile.write(text)
    			openFile.close()
    	except:
    		create = open('.myID.txt','x')
	    	create.write(str(text))
	    	create.close()
    except:
    		os.makedirs(path)
    		os.chdir(path)
	    	create = open('.myID.txt','x')
	    	create.write(str(text))
	    	create.close()
    if text in aproved:
        os.system("clear")
        banner()
        get_info_from_server_bd_pollice_user_aru_()

    else:
        os.system("clear")
        banner()
        printchar(f'    {yellowBold}Your Device ID: {cyanBold}{text}{end}', 0.01)
        printchar(f'    {redBold}Your Device not approved. {greenBold}Please connect with {cyanBold}ARU{end}', 0.1)
        os.system('xdg-open https://www.facebook.com/Aru.Ofc')
