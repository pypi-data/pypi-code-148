import sys
import urllib,os,subprocess
import time
import urllib.request
import requests
plt = sys.platform

def win():
    import ctypes, sys
    def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    if is_admin():
        from pywinauto.application import Application
        from pywinauto.keyboard import send_keys
        url = 'https://launchpad.net/veracrypt/trunk/1.25.9/+download/VeraCrypt%20Setup%201.25.9.exe' 
        filename = 'VeraCrypt Setup 1.25.9.exe'  
        
        with open(filename, "wb") as f:
            print("Downloading %s" % filename)
            response = requests.get(url, stream=True)
            total_length = response.headers.get('content-length')
            if total_length is None: 
                f.write(response.content)
            else:
                dl = 0
                total_length = int(total_length)
                for data in response.iter_content(chunk_size=4096):
                    dl += len(data)
                    f.write(data)
                    done = int(50 * dl / total_length)
                    sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )    
                    sys.stdout.flush()
        urllib.request.urlretrieve(url, filename)
        print(os.getcwd())
        app = Application().start(r'VeraCrypt Setup 1.25.9.exe')
        time.sleep(2)
        send_keys("{ENTER}")
        time.sleep(2)
        send_keys("{a}")
        send_keys("{ENTER}")
        send_keys("{ENTER}")
        send_keys("{ENTER}")
        send_keys("{ENTER}")
        send_keys("{ENTER}")
        send_keys("{ENTER}")
        send_keys("{LEFT}")
        send_keys("{ENTER}")
        send_keys("{LEFT}")
        send_keys("{ENTER}")
    else:
        # Re-run the program with admin rights
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    

def mac():
    url = "https://launchpad.net/veracrypt/trunk/1.25.9/+download/VeraCrypt_1.25.9.dmg"
    filename = 'VeraCrypt Setup 1.25.9.exe'  
    urllib.request.urlretrieve(url, filename)

def lin():
    from pywinauto.linux.keyboard import send_keys
    send_keys('{ENTER}')
    subprocess.run(["sudo","add-apt-repository","ppa:unit193/encryption"],check=True)
    send_keys('^y')
    subprocess.run(["sudo","apt","update"],check=True)
    subprocess.run(["sudo","apt","install","veracrypt"],check=True)
