#!/usr/bin/python3
# -*- coding: utf-8 -*-

import subprocess
from pathlib import Path
from typing import Union
from urllib.parse import unquote
from multiprocessing import Process

from slpkg.configs import Configs
from slpkg.progress_bar import ProgressBar


class Downloader(Configs):
    """ Wget downloader. """

    def __init__(self, path: Union[str, Path], url: str, flags: list):
        self.path = path
        self.url = url
        self.flags = flags
        self.flag_no_silent = '--no-silent'
        self.filename = url.split('/')[-1]
        self.color = self.colour()
        self.bold = self.color['bold']
        self.green = self.color['green']
        self.yellow = self.color['yellow']
        self.red = self.color['red']
        self.blue = self.color['blue']
        self.endc = self.color['endc']
        self.byellow = f'{self.bold}{self.yellow}'
        self.bred = f'{self.bold}{self.red}'
        self.progress = ProgressBar()
        self.output = 0
        self.stderr = None
        self.stdout = None

    def wget(self):
        """ Wget downloader. """
        if self.downloader == 'wget':
            self.output = subprocess.call(f'{self.downloader} {self.wget_options} --directory-prefix={self.path} '
                                          f'"{self.url}"', shell=True, stderr=self.stderr, stdout=self.stdout)
        elif self.downloader == 'curl':
            self.output = subprocess.call(f'{self.downloader} {self.curl_options} "{self.url}" --output '
                                          f'{self.path}/{self.filename}', shell=True, stderr=self.stderr,
                                          stdout=self.stdout)
        else:
            raise SystemExit(f"{self.red}Error:{self.endc} Downloader '{self.downloader}' not supported.\n")

        if self.output != 0:
            raise SystemExit(self.output)

    def check_if_downloaded(self):
        """ Checks if the file downloaded. """
        url = unquote(self.url)
        file = url.split('/')[-1]
        path_file = Path(self.path, file)
        if not path_file.exists():
            raise SystemExit(f"\n{self.red}FAILED {self.output}:{self.endc} '{self.blue}{self.url}{self.endc}' "
                             f"to download.\n")

    def download(self):
        """ Starting multiprocessing download process. """
        if self.silent_mode and self.flag_no_silent not in self.flags:

            done = f' {self.byellow} Done{self.endc}'
            self.stderr = subprocess.DEVNULL
            self.stdout = subprocess.DEVNULL

            message = f'[{self.green}Downloading{self.endc}]'

            # Starting multiprocessing
            p1 = Process(target=self.wget)
            p2 = Process(target=self.progress.bar, args=(message, self.filename))

            p1.start()
            p2.start()

            # Wait until process 1 finish
            p1.join()

            # Terminate process 2 if process 1 finished
            if not p1.is_alive():

                if p1.exitcode != 0:
                    done = f' {self.bred} Failed{self.endc}'
                    self.output = p1.exitcode

                print(f'{self.endc}{done}', end='')
                p2.terminate()

            # Wait until process 2 finish
            p2.join()

            # Restore the terminal cursor
            print('\x1b[?25h')
        else:
            self.wget()

        self.check_if_downloaded()
