import time
import random
import os
import sys


class ECore:
    true = True
    false = False

    def __init__(self, pre_option: bool = False):
        self.date = None
        self.list_for_choice = None
        self.input_readme = None
        self.input_project_name = None
        self.input_project_version = None
        self.input_project_authors = None
        self.readme = None
        self.project_name = None
        self.project_version = None
        self.project_authors = None
        self.pre_option = pre_option

    def CPI(self):
        self.input_project_name: str = input('Project name: ')
        self.input_project_version: str = input('Project version [0.0.1]: ')
        self.input_project_authors: str = input('Project authors: ')
        self.input_readme: str = input('Add readme file? [y/n]: ')

        if self.input_project_version == '':
            self.input_project_version = '0.0.1'

        os.mkdir(self.input_project_name)
        os.chdir(self.input_project_name)

        with open('main.py', 'w') as file:
            file.write(f'# {self.input_project_name}\n\n'
                       f'# authors: {self.input_project_authors}\n'
                       f'# version: {self.input_project_version}\n\n\n'
                       f'def Era(name):'
                       f'    print("Hi, " + name)\n\n\n'
                       f'Era(Era)')

        if self.input_readme == 'y':
            with open('README.md', 'w') as file:
                file.write(f'# {self.input_project_name}\n\n'
                           f'authors: {self.input_project_authors}\n'
                           f'version: {self.input_project_version}')

    def CPF(self,
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
                       f'# version: {self.project_version}\n\n\n'
                       f'def Era(name):'
                       f'    print("Hi, " + name)\n\n\n'
                       f'Era(Era)')

        if self.readme == true:
            with open('README.md', 'w') as file:
                file.write(f'# {self.project_name}\n\n'
                           f'authors: {self.project_authors}\n'
                           f'version: {self.project_version}')

    def r(self, list_for_choice: list):
        self.list_for_choice = list_for_choice
        random.choice(self.list_for_choice)
