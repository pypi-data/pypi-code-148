#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###################
#    This tool encodes Web payloads with some different encoding.
#    Copyright (C) 2022, 2023  Maurice Lambert

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
###################

r"""
This tool encodes Web payloads with some different encoding.

~# python3.11 WebPayloadsEncodings.py javascript 'this is my test'
String.fromCharCode(116,104,105,115,32,105,115,32,109,121,32,116,101,115,116)
~# python3.11 WebPayloadsEncodings.py pourcent 'this is my test'
%74%68%69%73%20%69%73%20%6d%79%20%74%65%73%74
~# python3.11 WebPayloadsEncodings.py 'this is my test'
'ms', 'sql server', 'sql_server', 'ms sql', 'ms_sql'
         char(116)+char(104)+char(105)+char(115)+char(32)+char(105)+char(115)+char(32)+char(109)+char(121)+char(32)+char(116)+char(101)+char(115)+char(116)
'sqlite', 'oracle', 'oracle sql', 'oracle_sql', 'postgre', 'postgresql'
         char(116)||char(104)||char(105)||char(115)||char(32)||char(105)||char(115)||char(32)||char(109)||char(121)||char(32)||char(116)||char(101)||char(115)||char(116)
'mysql', 'mariadb'
         CONCAT(char(116),char(104),char(105),char(115),char(32),char(105),char(115),char(32),char(109),char(121),char(32),char(116),char(101),char(115),char(116))
'unicode'
         \u{0074}\u{0068}\u{0069}\u{0073}\u{0020}\u{0069}\u{0073}\u{0020}\u{006d}\u{0079}\u{0020}\u{0074}\u{0065}\u{0073}\u{0074}
'javascript', 'script'
         String.fromCharCode(116,104,105,115,32,105,115,32,109,121,32,116,101,115,116)
'html unicode', 'html_unicode', 'unicode html', 'unicode_html'
         &bsol;u{0074}&bsol;u{0068}&bsol;u{0069}&bsol;u{0073}&bsol;u{0020}&bsol;u{0069}&bsol;u{0073}&bsol;u{0020}&bsol;u{006d}&bsol;u{0079}&bsol;u{0020}&bsol;u{0074}&bsol;u{0065}&bsol;u{0073}&bsol;u{0074}
'hexa escaping', 'hexadecimal escaping', 'hexa_escaping', 'hexadecimal_escaping', 'hexa escape', 'hexa_escape', 'hexadecimal escape', 'hexadecimal_escape'
         \x74\x68\x69\x73\x20\x69\x73\x20\x6d\x79\x20\x74\x65\x73\x74
'octal escaping', 'octal_escaping', 'octal escape', 'octal_escape'
         \164\150\151\163\040\151\163\040\155\171\040\164\145\163\164
'hexadecimal', 'hexa'
         0x74686973206973206d792074657374
'html', 'html_decimal', 'html decimal'
         &#116;&#104;&#105;&#115;&#32;&#105;&#115;&#32;&#109;&#121;&#32;&#116;&#101;&#115;&#116;
'html hexadecimal', 'html_hexadecimal', 'html hexa', 'html_hexa'
         &#x74;&#x68;&#x69;&#x73;&#x20;&#x69;&#x73;&#x20;&#x6d;&#x79;&#x20;&#x74;&#x65;&#x73;&#x74;
'url', 'uri', 'pourcent'
         %74%68%69%73%20%69%73%20%6d%79%20%74%65%73%74
'2pourcent', 'pourcent2', 'double pourcent', 'double_pourcent'
         %2574%2568%2569%2573%2520%2569%2573%2520%256d%2579%2520%2574%2565%2573%2574
~# 

>>> code = payloads_encodings("html", 'this is my test')
&#116;&#104;&#105;&#115;&#32;&#105;&#115;&#32;&#109;&#121;&#32;&#116;&#101;&#115;&#116;
>>> code = payloads_encodings("all", 'this is my test')
'ms', 'sql server', 'sql_server', 'ms sql', 'ms_sql'
    char(116)+char(104)+char(105)+char(115)+char(32)+char(105)+char(115)+char(32)+char(109)+char(121)+char(32)+char(116)+char(101)+char(115)+char(116)
'sqlite', 'oracle', 'oracle sql', 'oracle_sql', 'postgre', 'postgresql'
    char(116)||char(104)||char(105)||char(115)||char(32)||char(105)||char(115)||char(32)||char(109)||char(121)||char(32)||char(116)||char(101)||char(115)||char(116)
'mysql', 'mariadb'
    CONCAT(char(116),char(104),char(105),char(115),char(32),char(105),char(115),char(32),char(109),char(121),char(32),char(116),char(101),char(115),char(116))
'unicode'
    \u{0074}\u{0068}\u{0069}\u{0073}\u{0020}\u{0069}\u{0073}\u{0020}\u{006d}\u{0079}\u{0020}\u{0074}\u{0065}\u{0073}\u{0074}
'javascript', 'script'
    String.fromCharCode(116,104,105,115,32,105,115,32,109,121,32,116,101,115,116)
'html unicode', 'html_unicode', 'unicode html', 'unicode_html'
    &bsol;u{0074}&bsol;u{0068}&bsol;u{0069}&bsol;u{0073}&bsol;u{0020}&bsol;u{0069}&bsol;u{0073}&bsol;u{0020}&bsol;u{006d}&bsol;u{0079}&bsol;u{0020}&bsol;u{0074}&bsol;u{0065}&bsol;u{0073}&bsol;u{0074}
'hexa escaping', 'hexadecimal escaping', 'hexa_escaping', 'hexadecimal_escaping', 'hexa escape', 'hexa_escape', 'hexadecimal escape', 'hexadecimal_escape'
    \x74\x68\x69\x73\x20\x69\x73\x20\x6d\x79\x20\x74\x65\x73\x74
'octal escaping', 'octal_escaping', 'octal escape', 'octal_escape'
    \164\150\151\163\040\151\163\040\155\171\040\164\145\163\164
'hexadecimal', 'hexa'
    0x74686973206973206d792074657374
'html', 'html_decimal', 'html decimal'
    &#116;&#104;&#105;&#115;&#32;&#105;&#115;&#32;&#109;&#121;&#32;&#116;&#101;&#115;&#116;
'html hexadecimal', 'html_hexadecimal', 'html hexa', 'html_hexa'
    &#x74;&#x68;&#x69;&#x73;&#x20;&#x69;&#x73;&#x20;&#x6d;&#x79;&#x20;&#x74;&#x65;&#x73;&#x74;
'url', 'uri', 'pourcent'
    %74%68%69%73%20%69%73%20%6d%79%20%74%65%73%74
'2pourcent', 'pourcent2', 'double pourcent', 'double_pourcent'
    %2574%2568%2569%2573%2520%2569%2573%2520%256d%2579%2520%2574%2565%2573%2574
>>>

Tests:
~# python3.11 -m doctest -v WebPayloadsEncodings.py
23 tests in 18 items.
23 passed and 0 failed.
Test passed.
"""

__version__ = "0.0.2"
__author__ = "Maurice Lambert"
__author_email__ = "mauricelambert434@gmail.com"
__maintainer__ = "Maurice Lambert"
__maintainer_email__ = "mauricelambert434@gmail.com"
__description__ = (
    "This tool encodes Web payloads with some different encoding."
)
license = "GPL-3.0 License"
__url__ = "https://github.com/mauricelambert/WebPayloadsEncodings"

copyright = """
WebPayloadsEncodings  Copyright (C) 2022, 2023  Maurice Lambert
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions.
"""
__license__ = license
__copyright__ = copyright

__all__ = ["payloads_encodings"]

print(copyright)

from collections import defaultdict
from typing import Union, Iterable
from binascii import hexlify
from sys import argv, stderr


def encode(string: Union[str, bytes]) -> bytes:

    """
    This function encodes strings.

    >>> encode('abc')
    b'abc'
    >>> encode(b'abc')
    b'abc'
    >>>
    """

    if isinstance(string, str):
        return string.encode()
    return string


def pourcent_encoding(string: Union[str, bytes]) -> str:

    """
    This function encodes string with pourcent encoding (URL encoding).

    >>> pourcent_encoding('abc')
    '%61%62%63'
    >>>
    """

    return "%" + hexlify(encode(string), "%").decode()


def double_pourcent_encoding(string: Union[str, bytes]) -> str:

    """
    This function double encodes string with pourcent encoding (URL encoding).

    >>> double_pourcent_encoding('abc')
    '%2561%2562%2563'
    >>>
    """

    return pourcent_encoding(string).replace("%", "%25")


def html_decimal(string: Union[str, bytes], leading_zeros: int = 2) -> str:

    """
    This function encodes strings in HTML decimal encoding.

    >>> html_decimal('abc')
    '&#97;&#98;&#99;'
    >>> html_decimal('abc', leading_zeros=4)
    '&#0097;&#0098;&#0099;'
    >>>
    """

    return (
        "&#"
        + ";&#".join(
            [str(char).rjust(leading_zeros, "0") for char in encode(string)]
        )
        + ";"
    )


def html_hexadecimal(string: Union[str, bytes], leading_zeros: int = 2) -> str:

    """
    This function encodes strings in HTML hexadecimal encoding.

    >>> html_hexadecimal('abc')
    '&#x61;&#x62;&#x63;'
    >>> html_hexadecimal('abc', leading_zeros=4)
    '&#x0061;&#x0062;&#x0063;'
    >>>
    """

    return (
        "&#x"
        + ";&#x".join(
            [
                hex(char)[2:].rjust(leading_zeros, "0")
                for char in encode(string)
            ]
        )
        + ";"
    )


def sqlite_char(string: Union[str, bytes]) -> str:

    """
    This function returns a SQLite payload to write string without quotes.

    >>> sqlite_char('abc')
    'char(97)||char(98)||char(99)'
    >>>
    """

    return sql_char(string, delimiter="||")


postgresql_char = oracle_sql_char = sqlite_char


def sql_char(string: Union[str, bytes], delimiter: str = "||") -> str:

    """
    This function returns a SQL payload to write string without quotes.

    >>> sql_char('abc')
    'char(97)||char(98)||char(99)'
    >>> sql_char('abc', delimiter='+')
    'char(97)+char(98)+char(99)'
    >>>
    """

    return delimiter.join(f"char({char})" for char in encode(string))


def ms_sql_char(string: Union[str, bytes]) -> str:
         
    """
    This function returns a MS SQL Server payload to write string without quotes.

    >>> ms_sql_char('abc')
    'char(97)+char(98)+char(99)'
    >>>
    """

    return sql_char(string, delimiter="+")


def mariadb_sql_char(string: Union[str, bytes]) -> str:

    """
    This function returns a MS SQL Server payload to write string without quotes.

    >>> mariadb_sql_char('abc')
    'CONCAT(char(97),char(98),char(99))'
    >>>
    """

    return "CONCAT(" + sql_char(string, delimiter=",") + ")"


mysql_char = mariadb_sql_char


def hexa_number(string: Union[str, bytes]) -> str:

    """
    This function returns a long hexadecimal number from strings.

    >>> hexa_number('abc')
    '0x616263'
    >>>
    """

    return "0x" + hexlify(encode(string)).decode()


def javascript_char(string: Union[str, bytes]) -> str:

    """
    This function returns a javascript payload to write string without quotes.

    >>> javascript_char('abc')
    'String.fromCharCode(97,98,99)'
    >>>
    """

    return (
        "String.fromCharCode("
        + ",".join(str(char) for char in encode(string))
        + ")"
    )


def hexa_escaping(string: Union[str, bytes]) -> str:

    r"""
    This function returns a hexadecimal payload to bypass basic filters.

    >>> print(hexa_escaping('abc'))
    \x61\x62\x63
    >>>
    """

    return r"\x" + r"\x".join(f"{char:0>2x}" for char in encode(string))

def octal_escaping(string: Union[str, bytes]) -> str:

    r"""
    This function returns a octal payload to bypass basic filters.

    >>> print(octal_escaping('abc'))
    \141\142\143
    >>>
    """

    return "\\" + "\\".join(f"{char:0>3o}" for char in encode(string))


def unicode(string: Union[str, bytes], leading_zeros: int = 4) -> str:

    r"""
    This function returns a hexadecimal payload to bypass basic filters.

    >>> print(unicode('abc'))
    \u{0061}\u{0062}\u{0063}
    >>> print(unicode('abc', 8))
    \u{00000061}\u{00000062}\u{00000063}
    >>>
    """

    return (
        r"\u{"
        + r"}\u{".join(
            hex(char)[2:].rjust(leading_zeros, "0") for char in encode(string)
        )
        + "}"
    )


def unicode_html_escaping(
    string: Union[str, bytes], leading_zeros: int = 4
) -> str:

    r"""
    This function returns a hexadecimal payload to bypass basic filters.

    >>> unicode_html_escaping('abc')
    '&bsol;u{0061}&bsol;u{0062}&bsol;u{0063}'
    >>> unicode_html_escaping('abc', 8)
    '&bsol;u{00000061}&bsol;u{00000062}&bsol;u{00000063}'
    >>>
    """

    return unicode(string, leading_zeros).replace("\\", "&bsol;")


def payloads_encodings(encoding: str, *payloads: Iterable[str]) -> int:

    """
    This function encodes payloads.
    """

    encodings = {
        "ms": ms_sql_char,
        "sqlite": sqlite_char,
        "oracle": oracle_sql_char,
        "oracle sql": oracle_sql_char,
        "oracle_sql": oracle_sql_char,
        "postgre": postgresql_char,
        "postgresql": postgresql_char,
        "sql server": ms_sql_char,
        "sql_server": ms_sql_char,
        "ms sql": ms_sql_char,
        "ms_sql": ms_sql_char,
        "mysql": mysql_char,
        "mariadb": mariadb_sql_char,
        "unicode": unicode,
        "javascript": javascript_char,
        "script": javascript_char,
        "html unicode": unicode_html_escaping,
        "html_unicode": unicode_html_escaping,
        "unicode html": unicode_html_escaping,
        "unicode_html": unicode_html_escaping,
        "hexa escaping": hexa_escaping,
        "hexadecimal escaping": hexa_escaping,
        "hexa_escaping": hexa_escaping,
        "hexadecimal_escaping": hexa_escaping,
        "hexa escape": hexa_escaping,
        "hexa_escape": hexa_escaping,
        "hexadecimal escape": hexa_escaping,
        "hexadecimal_escape": hexa_escaping,
        "octal escaping": octal_escaping,
        "octal_escaping": octal_escaping,
        "octal escape": octal_escaping,
        "octal_escape": octal_escaping,
        "hexadecimal": hexa_number,
        "hexa": hexa_number,
        "html": html_decimal,
        "html_decimal": html_decimal,
        "html decimal": html_decimal,
        "html hexadecimal": html_hexadecimal,
        "html_hexadecimal": html_hexadecimal,
        "html hexa": html_hexadecimal,
        "html_hexa": html_hexadecimal,
        "url": pourcent_encoding,
        "uri": pourcent_encoding,
        "pourcent": pourcent_encoding,
        "2pourcent": double_pourcent_encoding,
        "pourcent2": double_pourcent_encoding,
        "double pourcent": double_pourcent_encoding,
        "double_pourcent": double_pourcent_encoding,
    }

    function = encodings.get(encoding.lower())
    if encoding == "all":
        functions = defaultdict(list)
        for name, function in encodings.items():
            functions[function].append(repr(name))
        for function, names in functions.items():
            print(", ".join(names))
            for payload in payloads:
                print("   ", function(payload))
    elif function:
        for payload in payloads:
            print(function(payload))
    else:
        print("Error: encoding not found.", file=stderr)
        print("Encodings availables: ", list(encodings.values()), file=stderr)
        return 5

    return 0


def main() -> int:

    """
    The main function to use this tool from command line arguments.
    """

    if len(argv) == 1:
        print(
            "USAGES:\n WebPayloadsEncodings [payload]\n WebPayloadsEncodings [encoding] [payloads ...]",
            file=stderr,
        )
        return 1
    elif len(argv) == 2:
        payloads = [argv[1]]
        encoding = "all"
    else:
        encoding = argv[1]
        payloads = argv[2:]

    return payloads_encodings(encoding, *payloads)


if __name__ == "__main__":
    exit(main())
