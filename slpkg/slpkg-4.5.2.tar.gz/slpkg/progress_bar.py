#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
from progress.spinner import PixelSpinner

from slpkg.configs import Configs


class ProgressBar(Configs):

    def __init__(self):
        self.color = self.colour()
        self.bold = self.color['bold']
        self.violet = self.color['violet']
        self.bviolet = f'{self.bold}{self.violet}'
        self.endc = self.color['endc']

    def bar(self, message, filename):
        """ Creating progress bar. """
        spinner = PixelSpinner(f'{self.endc}{message} {filename} {self.bviolet}')
        # print('\033[F', end='', flush=True)
        while True:
            time.sleep(0.1)
            spinner.next()
