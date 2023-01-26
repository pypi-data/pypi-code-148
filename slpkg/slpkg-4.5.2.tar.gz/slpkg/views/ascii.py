#!/usr/bin/python3
# -*- coding: utf-8 -*-

import shutil

from slpkg.configs import Configs


class Ascii(Configs):
    """ ascii characters. """
    def __init__(self):
        super(Configs, self).__init__()
        self.vertical_line = '│'
        self.horizontal_line = '─'
        self.horizontal_vertical = '┼'
        self.upper_right_corner = '┐'
        self.lower_left_corner = '└'
        self.lower_right_corner = '┘'
        self.upper_left_corner = '┌'
        self.horizontal_and_up = '┴'
        self.horizontal_and_down = '┬'
        self.vertical_and_right = '├'
        self.vertical_and_left = '┤'

        self.color = self.colour()
        self.bold = self.color['bold']
        self.blue = self.color['blue']
        self.green = self.color['green']
        self.cyan = self.color['cyan']
        self.red = self.color['red']
        self.yellow = self.color['yellow']
        self.violet = self.color['violet']
        self.endc = self.color['endc']
        self.bgreen = f'{self.bold}{self.green}'
        self.bred = f'{self.bold}{self.red}'

        self.columns, self.rows = shutil.get_terminal_size()

    def draw_package_title_box(self, message, title):
        """ Drawing package title box. """
        middle_title = int((self.columns / 2) - len(title) + 2)
        print(f'{self.bgreen}{self.upper_left_corner}' + f'{self.horizontal_line}' * (self.columns - 2) +
              f'{self.upper_right_corner}')
        print(f'{self.vertical_line}' + ' ' * middle_title + f'{title}' + ' ' *
              (self.columns - middle_title - len(title) - 2) + f'{self.vertical_line}')
        self.draw_middle_line()
        print(f'{self.vertical_line}{self.endc} {message}' + ' ' * (self.columns - len(message) - 3) +
              f'{self.bgreen}{self.vertical_line}')
        self.draw_middle_line()
        print(f'{self.bgreen}{self.vertical_line}{self.endc} Package:' + ' ' * 27 + 'Version:' +
              ' ' * (self.columns - 51) + f'Size{self.bgreen} {self.vertical_line}{self.endc}')

    def draw_view_package(self, package, version, color):
        """ Draw nad print the packages. """
        print(f'{self.bgreen}{self.vertical_line} {self.bold}{color}{package}{self.endc}' + ' ' * (35 - len(package)) +
              f'{self.blue}{version}' + ' ' * ((self.columns - 37) - len(version) - 1) +
              f'{self.bgreen}{self.vertical_line}{self.endc}')

    def draw_log_package(self, package):
        """ Drawing and print logs packages. """
        print(f'  {self.lower_left_corner}{self.horizontal_line}{self.cyan} {package}{self.endc}\n')

    def draw_middle_line(self):
        """ Drawing a middle line. """
        print(f'{self.bgreen}{self.vertical_and_right}' + f'{self.horizontal_line}' *
              (self.columns - 2) + f'{self.vertical_and_left}')

    def draw_dependency_line(self):
        """ Drawing  the dependencies line. """
        print(f'{self.bgreen}{self.vertical_line}{self.endc} Dependencies:' + ' ' * (self.columns - 16) +
              f'{self.bgreen}{self.vertical_line}{self.endc}')

    def draw_bottom_line(self):
        """ Drawing the bottom line. """
        print(f'{self.bold}{self.green}{self.lower_left_corner}' + f'{self.horizontal_line}' *
              (self.columns - 2) + f'{self.lower_right_corner}{self.endc}')

    def draw_checksum_error_box(self, name, checksum, file_check):
        """ Drawing checksum error box. """
        print('\n' + self.bred + self.upper_left_corner + self.horizontal_line * (self.columns - 2) +
              self.upper_right_corner)
        print(f"{self.bred}{self.vertical_line}{self.bred} Error:{self.endc} MD5SUM check for "
              f"'{self.cyan}{name}'{self.red} FAILED!" + ' ' * (self.columns - (len(name)) - 37) + self.vertical_line)
        print(self.bred + self.vertical_and_right + self.horizontal_line * (self.columns - 2) + self.vertical_and_left)
        print(f'{self.bred}{self.vertical_line}{self.yellow} Expected:{self.endc} {checksum}{self.bred}'
              + ' ' * (self.columns - (len(checksum)) - 13) + self.vertical_line)
        print(f'{self.bred}{self.vertical_line}{self.violet} Found:{self.endc} {file_check}{self.bred}'
              + ' ' * (self.columns - (len(file_check)) - 10) + self.vertical_line)
        print(self.bred + self.lower_left_corner + self.horizontal_line * (self.columns - 2) +
              self.lower_right_corner + self.endc)
