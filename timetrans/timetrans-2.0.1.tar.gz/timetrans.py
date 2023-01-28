from os import system
import datetime
try:
	from googletrans import Translator
except:
	system("pip install googletrans==3.1.0a0")
	from googletrans import Translator
import re
import calendar

translator = Translator()

sec = ["s", "с", "c"]
min = ["m", "м", "х"]
hour = ["h", "ч"]
day = ["d", "д"]
week = ["w", "н"]
mounth = ["mo", "ме"]
year = ["y", "г", "л"]

class timetrans:
  def __init__(self):
    self.text = None

  def get(seconds = str, loungle: str = None, easy: True = None):
    seconds = str(seconds)
    time_list = re.split('(\d+)',''.join(seconds.split()))
    
    if len(time_list) == 1:
    	return None
    if int(time_list[1]) < 1:
    	return None

    if time_list[2].lower() == "" and time_list[0].lower() == "":
    	seconds = f"{time_list[1]} s."
    	
    time_in_s = None
    if time_list[2][:1].lower() in sec or time_list[0][:1].lower() in sec:
       time_in_s = int(time_list[1])
    if time_list[2][:1].lower() in min or time_list[0][:1].lower() in min:
        time_in_s = int(time_list[1]) * 60
    if time_list[2][:1].lower() in hour or time_list[0][:1].lower() in hour:
        time_in_s = int(time_list[1]) * 3600
    if time_list[2][:1].lower() in day or time_list[0][:1].lower() in day:
        time_in_s = int(time_list[1]) * 86400
    if time_list[2][:1].lower() in week or time_list[0][:1].lower() in week:
    	time_in_s = int(time_list[1]) * 604800
    if time_list[2][:2].lower() in mounth or  time_list[0][:2].lower() in mounth:
    	time_in_s = int(time_list[1]) * 2592000
    if time_list[2][:1].lower() in year or time_list[0][:1].lower() in year:
        time_in_s = int(time_list[1]) * 31104000
    if not time_in_s:
    	time_in_s = int(time_list[1])
    
    td = time_in_s
    if easy:
    	s = td % 60
    	m = td // 60%60
    	h = td // 3600
    else:
    	s = td % 60
    	m = td // 60%60
    	h = td // 3600 % 24
    	d = td // 86400 % 7
    	w = td // 604800 % 4
    	mo = td // 2592000 % 12
    	y = td // 31104000
    if loungle:
    	if "".join(loungle.lower().split()).startswith("r"):
    		loungle = "ru"
    	elif "".join(loungle.lower().split()).startswith("e"):
    		loungle = "english"
    	else:
    		loungle = "english"
    
    if easy:
    	text = f"{s} s."
    	if m != 0:
    		if s != 0:
    			sec1 = f"{s} s."
    		else:
    			sec1 = ""
    		text = f"{m} m. {sec1}"
    	if h != 0:
    		if s != 0:
    			sec2 = f"{s} s."
    		else:
    			sec2 = ""
    		if m != 0:
    			min1 = f"{m} m."
    		else:
    			min1 = ""
    		text = f"{h} h. {min1} {sec2}"
    else:
    	text = f"{s} secconds"
    	if m != 0:
    		if s != 0:
    			sec1 = f"{s} secconds"
    		else:
    			sec1 = ""
    		text = f"{m} minutes {sec1}"
    	if h != 0:
    		if m != 0:
    			min1 = f"{m} minutes"
    		else:
    			min1 = ""
    		text = f"{h} hours {min1}"
    	if d != 0:
    		if h != 0:
    			hour1 = f"{h} hours"
    		else:
    			hour1 = ""
    		text = f"{d} days {hour1}"
    	if w != 0:
    		text = f"{w} weeks"
    	if mo != 0:
    		text = f"{mo} months"
    	if y != 0:
    		text = f"{y} years"
      
    try:
      text = translator.translate(text, dest = loungle)
    except:
      text = translator.translate(text, dest = "english")
    return text.text