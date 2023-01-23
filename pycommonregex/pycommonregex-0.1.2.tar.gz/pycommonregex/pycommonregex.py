import re

def is_int(num):
    return isinstance(num, int)

def is_positive_int(s):
    return bool(re.match(r"^\d+$", s))

def is_decimal_num(s):
    return bool(re.match(r"^\d*(\.\d+)?$", s))

def is_num(s):
    return bool(re.match(r"^-?\d*(\.\d+)?$", s))

def is_alpha_numeric(s):
    return bool(re.match(r"^[a-zA-Z0-9]*$", s))

def is_alpha_numeric_with_space(s):
    return bool(re.match(r"^[a-zA-Z0-9 ]*$", s))

def is_email(email):
    return bool(re.match(r"^([a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6})$", email))

def is_good_password(password):
    re1 = re.compile(r'[A-Z]')
    re2 = re.compile(r'[a-z]')
    re3 = re.compile(r'[0-9]')
    re4 = re.compile(r'[^\w\s]')
    return (
        len(password) >= 8 and
        re1.search(password) and
        re2.search(password) and
        re3.search(password) and
        re4.search(password)
    )

def is_username(username):
    pattern = re.compile(r'^(?![-_]*$)[A-Za-z0-9][A-Za-z0-9-_]{3,20}[A-Za-z0-9]$')
    return pattern.search(username) is not None


def is_url(url):
    pattern = re.compile(r'^(?:http|ftp)s?://' # http:// or https://
                         r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
                         r'localhost|' #localhost...
                         r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
                         r'(?::\d+)?' # optional port
                         r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return bool(pattern.match(url))

def is_ipv4(IPv4):
    pattern = re.compile(r"^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$")
    return bool(pattern.match(IPv4))


def is_ipv6(address):
    pattern = re.compile(r"^(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))$")
    return pattern.match(address) is not None


def is_date_yyyy_mm_dd(date):
    date_regex = r"^([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))$"
    return bool(re.match(date_regex, date))

def is_date_dd_mm_yyyy(date):
    date_regex = r"^((0[1-9]|[12]\d|3[01])-(0[1-9]|1[0-2])-[12]\d{3})$"
    return bool(re.match(date_regex, date))

def is_time_hh_mm_12h(time):
    time_regex = r"^(1[0-2]|0?[1-9]):[0-5][0-9] ?[AaPp][Mm]$"
    return bool(re.match(time_regex, time))


def is_time_hh_mm_24h(time):
    time_regex = r"^([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$"
    return bool(re.match(time_regex, time))

def is_time_hh_mm(time):
    time_regex_12h = r"^(1[0-2]|0?[1-9]):[0-5][0-9] ?[AaPp][Mm]$"
    time_regex_24h = r"^([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$"
    return bool(re.match(time_regex_12h, time)) or bool(re.match(time_regex_24h, time))

def is_html_tag(html):
    html_regex = r"<\/?[a-z][^>]*>"
    return bool(re.match(html_regex, html))

def is_slug(slug):
    slug_regex = r"^[a-z0-9]+(?:-[a-z0-9]+)*$"
    return bool(re.match(slug_regex, slug))

def is_tel(tel):
    tel_regex = r"^(?:(?:\(?(?:00|\+)([1-4]\d\d|[1-9]\d?)\)?)?[\-\.\ \\\/]?)?((?:\(?\d{1,}\)?[\-\.\ \\\/]?){0,})(?:[\-\.\ \\\/]?(?:#|ext\.?|extension|x)[\-\.\ \\\/]?(\d+))?$"
    return bool(re.match(tel_regex, tel))
