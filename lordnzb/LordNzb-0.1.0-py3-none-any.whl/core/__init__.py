
import os
import regex as re
import xml.etree.ElementTree as ET
from datetime import datetime
from urllib.parse import quote as link_encode
from dataclasses import dataclass
from .reg import multi_regex_matching
from .descriptor import CachedProperty

regPas = re.compile("{{(.+)?}}")
m_reg_Head = multi_regex_matching(
    '\"(?P<val>[A-Za-z0-9_]*)\.(?:par|7z|vol|nfo)(?:.+?)\"',
    '(?P<val>[A-Za-z0-9_]*)\.(?:par|7z|vol|nfo)(?:.+?)'
)
regXMLNS = re.compile('{(.+?)}')


def _find_in_xml(root, str):
    for e in root:
        if str in e.tag:
            return e
    return None


@dataclass
class NZB:
    filename: str

    header: str
    password: str

    groups: list
    raw_size: int
    date_time_utc: int

    @CachedProperty
    def name(self):
        _nzb = self.filename.replace(".nzb", "")
        _nzb = regPas.sub("", _nzb)
        return _nzb

    @CachedProperty
    def size(self):
        size = self.raw_size
        for size_name in ['bytes', 'kb', 'mb', 'gb', 'tb']:
            if size >= 1024:
                size = size / 1024
            else:
                size = f"{size:.2f} {size_name}"
                break
        return size

    @CachedProperty
    def link_name(self):
        return link_encode(self.name)

    @CachedProperty
    def link_header(self):
        return link_encode(self.header)

    @CachedProperty
    def link_pass(self):
        return link_encode(self.password)

    @CachedProperty
    def link_one_group(self):
        return link_encode(self.groups[0] if self.groups else '')

    @CachedProperty
    def nzbindex(self):
        return f"https://nzbindex.nl/?q={self.link_header}"

    @CachedProperty
    def nzbking(self):
        return f"https://nzbking.com/?q={self.link_header}"

    @CachedProperty
    def binsearch(self):
        return f"https://binsearch.info/?q={self.link_header}"

    @CachedProperty
    def nzblnk(self):
        return f"nzblnk://?t={self.link_name}&h={self.link_header}&p={self.link_pass}&g={self.link_one_group}&d={self.date_time_utc}"

    def get_date(self):
        if self.date_time_utc is not None:
            return datetime.utcfromtimestamp(self.date_time_utc)
        return None

    def get_date_string(self, dateformat='%Y-%m-%d %H:%M:%S') -> str:
        date = self.get_date()
        if date is not None:
            return date.strftime(dateformat)
        return ""

    def get_date_iso(self):
        date = self.get_date()
        if date is not None:
            return date.isoformat()
        return ""

    def to_dict(self) -> dict:
        """
        return Dictionary with significant values
        """
        date = self.get_date_string()

        return {
            "filename": self.filename,
            "name": self.name,
            "header": self.header,
            "password": self.password,
            "group": self.groups,
            "raw_size": self.raw_size,
            "size": self.size,
            "date": date,
            "nzbindex": self.nzbindex,
            "nzbking": self.nzbking,
            "binsearch": self.binsearch,
            "nzblnk": self.nzblnk
        }

    @staticmethod
    def get_dict_keys() -> list:
        return ['filename', 'name', 'header', 'password', 'group', 'raw_size', 'size', 'date', 'nzbindex', 'nzbking',
                'binsearch', 'nzblnk']


def parser(file_path):
    file_name = os.path.basename(file_path)

    # open XML
    tree = ET.parse(file_path)
    root = tree.getroot()

    # get Passwort
    passw = ""
    _passw = regPas.search(file_name)
    if not _passw is None:
        passw = _passw.group(1)
    else:
        _ele = root.find(".//*[@type='password']")
        if not _ele is None:
           passw = _ele.text

    # get Header

    ele = _find_in_xml(root, 'file')

    header = ""
    _th = ele.attrib['subject']
    _th = m_reg_Head(_th)
    if not _th is None:
        header = _th['val']

    # get Group

    group = []

    ns = regXMLNS.search(root.tag)
    if ns is not None:
        ns = ns.group(0)
    else:
        ns = ""
    groups = ele.findall(".//" + ns + "group")

    for g in groups:
        group.append(g.text)

    # Date

    dateTime = None
    _eleDate = root.find(".//*[@date]")
    if _eleDate is not None:
        dateTime = int(_eleDate.attrib['date'])

    # Size

    size = 0
    _segments = root.findall(".//" + ns + "segment")
    for segm in _segments:
        size += int(segm.attrib['bytes'])

    r_nzb = NZB(
        filename=file_name,
        password=passw,
        header=header,
        date_time_utc=dateTime,
        groups=group,
        raw_size=size,
    )
    return r_nzb