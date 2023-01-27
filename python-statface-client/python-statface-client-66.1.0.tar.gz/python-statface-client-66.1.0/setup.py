from setuptools import setup
from setuptools.command.install import install
import subprocess


class PostInstallCommand(install):
    def run(self):
        subprocess.check_call(["echo", "yandex depconf prevention"])
        install.run(self)



setup(
   name='python-statface-client',
   version='66.1.0',
   author='Dependency confusion tester',
   author_email='ezzer@yandex-team.ru',
   url='https://medium.com/@alex.birsan/dependency-confusion-4a5d60fec610',
   description='A package to test dependency confusion',
   cmdclass={
        'install': PostInstallCommand,
    },
   )
