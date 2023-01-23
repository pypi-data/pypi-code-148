#!/bin/python3
import requests
import json
import sys

def doRequest(url):
    try:
        headers= {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:75.0) Gecko/20100101 Firefox/75.0"
        }
        r = requests.get(url,headers= headers)
        text = r.text
        #print(r.text)
        if r.status_code != 200 or type(text) is not str:
            return False
        return text
    except:
        return False

def loadRequest(url,variable):
    #print(url)
    request = doRequest(url)
    #print(request)
    if request is False:
        return False
    #print(request)
    toJson= json.loads(request)
    if variable in toJson.keys():
        print( toJson[variable])
        return True
    return False
def loadRequestArray(url,variables):
    #print(url)
    request = doRequest(url)
    #print(request)
    if request is False:
        return False
    #print(request)
    toJson= json.loads(request)
    #print(toJson)
    testForPrint = False
    for item in variables:
        #print(variables[item])
        if variables[item] in toJson:
            #print (toJson[item])
            print(toJson[variables[item]])
            testForPrint = True
        else:
            print("No information found for: ", variables[item])
    return testForPrint


def ipapicom(args=['ip'],inRequest=['ip','isp','asn','country','city','countryCode','region','latitude','longitude']):
    url= "http://ip-api.com/json"
    forRequest={}
    cont=0
    
    for item in args:
        #print(type(item) , str(item))
        if item in inRequest:
            #print("founded")
            if item == 'ip':
                forRequest[cont]='query'
            elif item == 'asn':
                forRequest[cont]='as'
            elif item == 'latitude':
                forRequest[cont]='lat'
            elif item == 'longitude':
                forRequest[cont]='lon'
            else:
                forRequest[cont]= item
        cont +=1
    #print(forRequest)
    return loadRequestArray(url,forRequest)

def apimyipcom(args=['ip','country','countryCode']):
    url= "https://api.myip.com"
    return loadRequest(url,"ip")

def myipio(args=['ip'],inRequest=['ip']):
    url="https://api.my-ip.io/ip"
    request = doRequest(url)
    if request is False:
        return False
    if type(request) is str:
        print(request)
    return True

def ipifyorg(args=['ip'],inRequest=['ip']):
    url= "https://api.ipify.org?format=json"
    return loadRequest(url,"ip")  

def ipapico(args=['ip'],inRequest=['ip','isp','asn','city','region','country','countryCode','latitude','latitude']):
    url= "https://ipapi.co/json/"
    #return loadRequest(url,"ip")
    forRequest={}
    cont =0
    
    for item in args:
        #print(type(item) , str(item))
        if item in inRequest:
            #print("founded")
            if item == 'isp':
                forRequest[cont]='org'
            elif item =='countryCode':
                forRequest[cont]='country_code'
            else:
                forRequest[cont]= item
            cont +=1
    #print(forRequest)
    return loadRequestArray(url,forRequest)

def main():
    numberOfArgs = len(sys.argv)
    args = sys.argv

    if(numberOfArgs==1):
        if ipifyorg() is True:
            pass
        elif apimyipcom() is True:
            pass
        elif ipapicom() is True:
            pass
        elif myipio() is True:
            pass
        elif ipapico() is True:
            pass
        else:
            print("Sorry can't obtain the ip Address")
            sys.exit(1)
    elif(args[1]=='--help'):
        #['ip','isp','asn','country','city','countryCode','region','latitude','longitude']
        print("Simple use for myip")
        print("\ncall just to command to se the ip or use this variables\n")   
        print('\033[1m','ip','\033[0m = to see the ip address')
        print('\033[1m','isp','\033[0m = to see the isp provider')
        print('\033[1m','country','\033[0m = to see your contry')
        print('\033[1m','countryCode','\033[0m = to see your Contry Code')
        print('\033[1m','city','\033[0m = to see your city')
        print('\033[1m','region','\033[0m = to see your region')
        print('\033[1m','latitude','\033[0m = to see your latitude')
        print('\033[1m','longitude','\033[0m = to see your longitude')
    else:
        if ipapicom(args):
            pass
        elif ipapico(args):
            pass
        else:
            print("Sorry can't obtain the ip Address")
            sys.exit(1)
    