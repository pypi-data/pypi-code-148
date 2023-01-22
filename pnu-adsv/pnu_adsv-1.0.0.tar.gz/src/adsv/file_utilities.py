#!/usr/bin/env python3
""" adsv - Analyze delimiter-separated values files
License: 3-clause BSD (see https://opensource.org/licenses/BSD-3-Clause)
Author: Hubert Tournier
"""

import logging
import os

import chardet

CHUNK_SIZE = 16384 # bytes


####################################################################################################
def get_file_encoding(filename):
    """ Try to guess the encoding of the file """
    if not os.path.isfile(filename):
        return ""

    detector = chardet.UniversalDetector()
    with open(filename, "rb") as file:
        line = file.readline()
        while line:
            detector.feed(line)
            if detector.done:
                break
            line = file.readline()
    detector.close()

    logging.debug("Encoding detected='%s'", detector.result)

    return detector.result["encoding"]


####################################################################################################
def get_file_line_terminator(filename):
    """ Return the type of line terminator """
    line_terminator = "\n"

    if not os.path.isfile(filename):
        return ""

    cr_encountered = False
    with open(filename, "rb") as file:
        # Scanning one chunk of the file should be enough...
        buffer = file.read(CHUNK_SIZE)
        for byte in buffer:
            if chr(byte) == '\r':
                cr_encountered = True
            elif chr(byte) == '\n':
                break
            else:
                cr_encountered = False

    if cr_encountered:
        line_terminator = "\r\n"

    logging.debug("Line terminator detected='%s'", repr(line_terminator))

    return line_terminator
