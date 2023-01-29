import re
import unicodedata


def slugify(value: str, allow_unicode: bool = False) -> str:
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s._-]', '', value)
    return re.sub(r'[-\s]+', '-', value)
