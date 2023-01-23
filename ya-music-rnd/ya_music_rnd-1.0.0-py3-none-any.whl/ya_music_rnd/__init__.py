import random
from urllib import request, error
from time import sleep
from webbrowser import open
import re


class YandexMusicRnd:

    def __init__(self,
                 max_index: int = 10000000,
                 open_url: bool = True,
                 max_iterations: int = 60,
                 find_clear: str = 'no',
                 find_have_albom: str = 'all',
                 find_have_similar: str = 'all',
                 find_have_clips: str = 'all',
                 show_progress: bool = True,
                 quiet: bool = False
                 ):
        """
        Init class
        :param max_index:
        :param open_url:
        :param max_iterations:
        :param find_clear:
        :param find_have_albom:
        :param find_have_similar:
        :param find_have_clips:
        :param show_progress:
        :param quiet:
        """

        self.max_index = max_index
        self.open_url = open_url
        self.max_iterations = max_iterations
        self.cur_iteration = 0
        self.find_clear = find_clear
        self.find_have_albom = find_have_albom
        self.find_have_similar = find_have_similar
        self.find_have_clips = find_have_clips
        self.show_progress = show_progress
        self.quiet = quiet

    def get_artist(self, open_url: bool = None) -> str:
        """

        :param open_url:
        :return: Site url
        """

        if open_url is None:
            open_url = self.open_url

        found = False
        while not found:
            if self.cur_iteration >= self.max_iterations:
                break

            self.cur_iteration += 1

            index = random.randint(1, self.max_index)

            site = f'https://music.yandex.ru/artist/{index}'

            if not self.quiet and self.show_progress:
                self.print_progress(site)

            try:
                response = request.urlopen(site)
            except error.HTTPError as e:
                pass
            else:
                html = response.read().decode(response.headers.get_content_charset())
                found = self.check_filter(html)

            sleep(1)

        if found:
            if open_url:
                open(site)
        else:
            if not self.quiet:
                print(f'За максимальное количество итераций ({self.max_iterations}) результат не найден.')
            site = ''

        return site

    def check_filter(self, html) -> bool:
        """
        Check filter parameters
        :param html:
        :return: Bool
        """

        clear = False
        albom = False
        similar = False
        clips = False

        if len(re.findall('>Главное</span>', html)) == 0:
            clear = True
        else:
            if len(re.findall('>Альбомы</a>', html)) >= 1:
                albom = True
            if len(re.findall('>Похожие</a>', html)) >= 1:
                similar = True
            if len(re.findall('>Клипы</a>', html)) >= 1:
                clips = True

        if self.find_clear == 'yes':
            if clear:
                return True
            else:
                return False

        if clear and self.find_clear == 'no':
            return False

        if self.find_have_albom == 'yes' and not albom:
            return False

        if self.find_have_albom == 'no' and albom:
            return False

        if self.find_have_similar == 'yes' and not similar:
            return False

        if self.find_have_similar == 'no' and similar:
            return False

        if self.find_have_clips == 'yes' and not clips:
            return False

        if self.find_have_clips == 'no' and clips:
            return False

        return True

    def print_progress(self, site: str) -> None:
        """
        Print progress
        :param site: Current site url
        :return: None
        """
        print(f'{site} [{self.cur_iteration}/{self.max_iterations}]')

    @property
    def max_index(self) -> int:
        return self.__max_index

    @max_index.setter
    def max_index(self, max_index: int):
        self.__max_index = max_index

    @property
    def open_url(self) -> bool:
        return self.__open_url

    @open_url.setter
    def open_url(self, open_url: bool):
        self.__open_url = open_url

    @property
    def max_iterations(self) -> int:
        return self.__max_iterations

    @max_iterations.setter
    def max_iterations(self, max_iterations: int):
        self.__max_iterations = max_iterations

    @property
    def quiet(self) -> bool:
        return self.__quiet

    @quiet.setter
    def quiet(self, quiet: bool):
        self.__quiet = quiet

    @property
    def show_progress(self) -> bool:
        return self.__show_progress

    @show_progress.setter
    def show_progress(self, show_progress: bool):
        self.__show_progress = show_progress

    @property
    def find_have_albom(self) -> str:
        return self.__find_have_albom

    @find_have_albom.setter
    def find_have_albom(self, find_have_albom: str):
        self.__find_have_albom = find_have_albom

    @property
    def find_have_similar(self) -> str:
        return self.__find_have_similar

    @find_have_similar.setter
    def find_have_similar(self, find_have_similar: str):
        self.__find_have_similar = find_have_similar

    @property
    def find_have_clips(self) -> str:
        return self.__find_have_clips

    @find_have_clips.setter
    def find_have_clips(self, find_have_clips: str):
        self.__find_have_clips = find_have_clips

    @property
    def find_clear(self) -> str:
        return self.__find_clear

    @find_clear.setter
    def find_clear(self, find_clear: str):
        self.__find_clear = find_clear
