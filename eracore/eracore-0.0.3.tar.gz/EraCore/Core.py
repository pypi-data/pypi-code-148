import time
import random
import os
import sys


class ECore:
    def __init__(self, pre_option: bool = False):
        self.readme = None
        self.project_name = None
        self.project_version = None
        self.project_authors = None
        self.pre_option = pre_option

    def CP(self,
           project_name: str,
           project_version: str,
           project_authors: str,
           readme: bool = False):
        self.readme = readme
        self.project_name = project_name
        self.project_version = project_version
        self.project_authors = project_authors

        os.mkdir(self.project_name)
        os.chdir(self.project_name)

        with open('main.py', 'w') as file:
            file.write(f'# {self.project_name}\n\n'
                       f'# authors: {self.project_authors}\n'
                       f'# version: {self.project_version}\n')

        if self.readme == True:
            with open('README.md', 'w') as file:
                file.write(f'# {self.project_name}\n\n'
                           f'authors: {self.project_authors}\n'
                           f'version: {self.project_version}')
