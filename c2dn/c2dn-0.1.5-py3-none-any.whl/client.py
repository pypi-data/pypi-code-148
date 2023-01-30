import shutil
import warnings
import requests

from io import StringIO
from dataclasses import dataclass
from urllib.parse import urljoin

from lxml.etree import HTMLParser, parse

from typing import Self, Sequence

__all__ = [
    'Clip2NetClient', 'Clip2NetFolder', 'Clip2NetFile',
]


@dataclass
class Clip2NetFolder:
    uid: str
    name: str


@dataclass
class Clip2NetFile:
    uid: str
    name: str
    parent: Clip2NetFolder
    short_url: str
    long_url: str
    timestamp: str


class Clip2NetClient:

    BASE_URL = 'https://clip2net.com'
    MAIN_URL = '/index.php'
    LOGIN_URL = '/login.html'
    LOGOUT_URL = '/logoff.html'

    DEFAULT_HEADERS = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    }

    def __init__(self, username: str, password: str) -> None:
        self._username = username
        self._password = password
        self._response = self._html = self._pd = None
        self._parser = HTMLParser()
        self._session = requests.Session()
        self._session.headers.update(self.DEFAULT_HEADERS)

    def __enter__(self) -> Self:
        self.login()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.logout()

    def login(self) -> None:
        resp = self._session.get(urljoin(self.BASE_URL, self.LOGIN_URL))
        resp.raise_for_status()
        html = parse(StringIO(resp.text), parser=self._parser, base_url=self.BASE_URL)
        pd = str(html.xpath('//form[@class="login-form"]/input[@name="pd"]/@value')[0])
        self._response = resp = self._session.post(urljoin(self.BASE_URL, self.MAIN_URL), params={
            'pd': pd, 'md': 'members', 'inst': '',
        }, data={
            'username': self._username,
            'password': self._password,
            'mode': 'login_members',
            'redirect_url': '',
            'subpage': 'login',
            'pd': pd,
            'md': 'members',
            'inst': '',
        }, allow_redirects=True)
        resp.raise_for_status()
        self._html = html = parse(StringIO(resp.text), parser=self._parser, base_url=self.BASE_URL)
        self._pd = str(html.xpath('//form[@id="submit_form"]/input[@name="pd"]/@value')[0])

    def logout(self) -> None:
        self._response = self._html = self._pd = None
        resp = self._session.get(urljoin(self.BASE_URL, self.LOGOUT_URL))
        resp.raise_for_status()

    def dir(self) -> Sequence[Clip2NetFolder]:
        if not self._html:
            self.login()
        result = []
        for node in self._html.xpath('//ul[@id="ul_fold"]/li'):
            folder_id = str(node.xpath('./@attr_id')[0])
            folder_name = str(node.xpath('./a[1]//text()')[0])
            result.append(Clip2NetFolder(uid=folder_id, name=folder_name))
        return result

    def ls(self, folder: Clip2NetFolder) -> Sequence[Clip2NetFile]:
        if not self._pd:
            self.login()
        page_idx, unique, result = 1, set(), []
        while True:
            resp = self._session.get(urljoin(self.BASE_URL, self.MAIN_URL), params={
                'pd': self._pd,
                'md': 'files',
                'inst': '',
                'view_mode': '',
                'mode': '',
                'save_qry': 1,
                'nb': 1,
                'new_main2': 1,
                'get_ajax': 1,
                'update': 'new_main2',
                'page': page_idx,
                'sort_by': '',
                'folder_id': folder.uid,
                'type': '',
                'search': '',
                'after': '',
                'before': '',
                'gallery': f'/members.html#&page={page_idx}&sort_by=&folder_id={folder.uid}&type=&search=&after=&before=',
            })
            resp.raise_for_status()
            html = parse(StringIO(resp.text), parser=self._parser, base_url=self.BASE_URL)
            with warnings.catch_warnings():
                warnings.simplefilter(action='ignore', category=FutureWarning)
                if not html.getroot():
                    break
            cnt, elements = 0, html.xpath('//li[@class="box-td kk"]')
            for node in elements:
                uid = str(node.xpath('./@atrr_id')[0])
                if uid not in unique:
                    name = str(node.xpath(f'.//span[@id="kk_{uid}_title"]/text()')[0]).strip()
                    short_url = str(node.xpath('.//a[@class="box-item-pic"]/@href_s')[0]).replace('http://', 'https://')
                    long_url = str(node.xpath('.//a[@class="box-item-pic"]/img/@src')[0])
                    timestamp = str(node.xpath('.//div[@class="box-info-shot"]/text()')[0]).strip()
                    result.append(Clip2NetFile(
                        uid=uid, name=name, parent=folder,
                        short_url=short_url,
                        long_url=urljoin(self.BASE_URL, long_url),
                        timestamp=timestamp,
                    ))
                else:
                    cnt += 1
            if cnt == len(elements):
                break
            page_idx += 1
        return result

    @classmethod
    def download_file(cls, url: str, local_path: str) -> None:
        with requests.get(url, stream=True) as r:
            with open(local_path, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
