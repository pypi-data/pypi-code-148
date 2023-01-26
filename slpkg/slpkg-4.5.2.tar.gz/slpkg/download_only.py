#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time

from slpkg.configs import Configs
from slpkg.queries import SBoQueries
from slpkg.utilities import Utilities
from slpkg.downloader import Downloader
from slpkg.views.views import ViewMessage
from slpkg.models.models import session as Session


class Download(Configs, Utilities):
    """ Download the slackbuilds with the sources only. """

    def __init__(self, directory: str, flags: list):
        super(Configs, self).__init__()
        super(Utilities, self).__init__()
        self.flags = flags
        self.directory = directory
        self.flag_directory = '--directory='
        self.session = Session

    def packages(self, slackbuilds: list):
        """ Download the package only. """
        view = ViewMessage(self.flags)
        view.download_packages(slackbuilds, self.directory)
        view.question()

        download_path = self.download_only
        if self.flag_directory in self.flags:
            download_path = self.directory

        start = time.time()
        for sbo in slackbuilds:
            file = f'{sbo}{self.sbo_tar_suffix}'
            location = SBoQueries(sbo).location()
            url = f'{self.sbo_repo_url}/{location}/{file}'

            down_sbo = Downloader(download_path, url, self.flags)
            down_sbo.download()

            sources = SBoQueries(sbo).sources()
            for source in sources:
                down_source = Downloader(download_path, source, self.flags)
                down_source.download()

        elapsed_time = time.time() - start
        self.finished_time(elapsed_time)
