import atexit
import os
import sys
from setuptools import setup, find_packages
from setuptools.command.install import install

class CustomInstall(install):
    def run(self):
        def _post_install():
            def find_module_path():
                for p in sys.path:
                    if os.path.isdir(p) and my_name in os.listdir(p):
                        return os.path.join(p, my_name)
            install_path = find_module_path()

            print("Hello-abhishek-Iam-your-package")
            print("+++++++++++++++++++++++++++++++")
            print("***********")
          
            
        atexit.register(_post_install)
        install.run(self)


setup(
  cmdclass={'install': CustomInstall},
  name='python_owasp_zap',
  version='9.0.1',
  description='PoC',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='scythe abhi',
  author_email='scytheabhi97@gmail.com',
  license='MIT',
  keywords='PoC', 
  packages=find_packages(),
  install_requires=[''] 
)