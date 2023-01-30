import re
import unicodedata

from c2dn.client import Clip2NetFile


def slugify(value: str, allow_unicode: bool = False) -> str:
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s._-]', '', value.strip())
    return re.sub(r'[-\s]+', '-', value)


def is_c2n_url(url: str) -> bool:
    return url.startswith('https://clip2net.com/clip/')


def url_to_fname(url: str) -> str:
    return url.split('/')[-1]


def get_file_ext(file: Clip2NetFile) -> str:
    if file.short_url and '.' in file.short_url:
        return f'.{file.short_url.split(".")[-1]}'
    if file.long_url and '.' in file.long_url:
        return f'.{file.long_url.split(".")[-1]}'
    return ''
