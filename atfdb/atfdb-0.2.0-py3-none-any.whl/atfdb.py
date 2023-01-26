# -------------------------------------------------------------------------------
#     \  |  /
#      \ | /                                              /|     ____
#       \|/        Accelerator Test Facility             / |     |
#     ---*----------------------------------------------/------------------
#       /|\     Brookhaven National Laboratory         /   |  |  |
#      / | \   Brookhaven Science Associates, LLC          |  |
#     /  |  \                                                 |
# -------------------------------------------------------------------------------
#  atf_db_py3.py
#  Python module to support network socket communications to an ATF database
#  using Python3.x
#  Typically, one can use: import atf_db_py3 as atf_db.
# -------------------------------------------------------------------------------

#  Revision history

#  Thu Sep  8 16:14:01 EDT 2022 -- RGM
#  Added GETDS for double precision scalars.

#  Mon Jul 26 14:03:39 EDT 2021 -- RGM
#  Found more locations where P2-P3 string problems.

#  Mon Jul 26 13:07:27 EDT 2021 -- RGM
#  Corrected problem handling string parameters for PUTxx functions.
#  This is a Python 2 to Python 3 gotcha.

#  Wed Jul 21 16:09:45 EDT 2021 -- RGM
#  Improved some comments to make things a little more understandable.

#  Sat May  1 23:23:05 EDT 2021 -- RGM
#  This is a copy of the original atf_db upated for Python 3.x.
#  There have been no updates to the protocl itself, only how Python
#  handles strings in 3.x: Socket messages now have to be read/written
#  as byte strings (i.e., use encode/decode)

#  Fri Jul 27 16:54:45 EDT 2018 -- RGM
#  Corrected minor typos in comments.
#  No technical changes.

#  Sun Nov 19 02:28:48 EST 2017 -- RGM
#  Fixed some comments.
#  Fixed put_binary.

#  Mon Oct 23 14:29:30 EDT 2017 -- RGM
#  Moved to its own directory in /DbSockets/Python

#  Thu Oct 19 12:55:47 EDT 2017 -- RGM
#  Corrected minor typo introduced in earlier updates today.

#  Thu Oct 19 12:46:41 EDT 2017 -- RGM
#  Improved error messages, status, etc.
#  No substantive technical changes.

#  Wed Apr 19 21:19:30 EDT 2017 -- RGM
#  Initial release of new version.

# ===============================================================================

from __future__ import print_function

import datetime
import socket  # for socket create, read, write, etc.
import sys  # for exit
import time  # for time delay, using sleep(...)
from collections import namedtuple
from functools import partial

#  Constants

ATF_DB_RECEIVE_BUFFER_SIZE = 5120
ATF_DB_SEND_BUFFER_SIZE = 5120

#  Message prefixes

ATF_DB_DEBUG = "ATF DB - DEBUG: "
ATF_DB_ERROR = "ATF DB - ERROR: "
ATF_DB_NOTE = "ATF DB - NOTE: "
ATF_DB_SUCCESS = "ATF DB - SUCCESS: "
ATF_DB_WARNING = "ATF DB - WARNING: "


def get_channel_index(channel_name=None):
    general_message = f"{ATF_DB_ERROR}Problem finding database channel index"

    if channel_name is None:
        timestamp()
        print(general_message)
        print(f"{ATF_DB_ERROR}Passed a 'None' channel name")
        return None

    #  Write request
    request = f"GETCHIDX 'X' '{channel_name}'"
    #  Read request
    status = socket_write(request)
    if status is None:
        return None

    reply = socket_read().decode()
    split_reply = reply.split()

    if split_reply[0] == "CHIDXERR":
        timestamp()
        print(general_message)
        print(f"{ATF_DB_ERROR}Channel name: {channel_name}")
    else:
        return split_reply[-1]


def get_templated(channel_index=None, param="", dtype_str="", dtype=None):
    error_message = f"{ATF_DB_ERROR}Problem getting {dtype_str} scalar"

    if channel_index is None:
        timestamp()
        print(error_message)
        print(f"{ATF_DB_ERROR}Channel index is 'None'")
        return None

    request = f"GET{param} 'X' {channel_index}"

    status = socket_write(request)
    if status is None:
        return None

    reply = socket_read().decode()
    split_reply = reply.split()

    if split_reply[0] == "GETFAIL":
        timestamp()
        print(error_message)
        print(f"{ATF_DB_ERROR}Channel index: {channel_index}")
        return None
    else:
        if dtype is None:
            return split_reply[-1]
        else:
            return dtype(split_reply[-1])


def put_templated(channel_index=None, value=None, param="", dtype_str="", dtype=None):
    error_message = f"{ATF_DB_ERROR}Problem writing {dtype_str} scalar to database"

    if channel_index is None:
        timestamp()
        print(error_message)
        print(f"{ATF_DB_ERROR}Channel index is 'None'")
        return None

    if value is None:
        timestamp()
        print(error_message)
        print(f"{ATF_DB_ERROR}{dtype_str.capitalize()} value is 'None'")
        return None

    if dtype in ["binary", "string"]:
        quote = "'"
    else:
        quote = ""
    #  Write request
    request = f"PUT{param} 'X' 'ACK' {channel_index} {quote}{value}{quote}"

    status = socket_write(request)
    if status is None:
        return None

    #  Read reply
    reply = socket_read().decode()
    split_reply = reply.split()

    if split_reply[0] != "PUTOK":
        timestamp()
        print(error_message)
        print(f"{ATF_DB_ERROR}Channel index: {channel_index}")
        print(f"{ATF_DB_ERROR}{dtype_str.capitalize()} value: {value}")
        return None


SocketAPIParameters = namedtuple("SocketAPIParameters", ["dtype_str", "param", "dtype"])

bs_params = SocketAPIParameters(param="BS", dtype_str="binary", dtype=None)
is_params = SocketAPIParameters(param="IS", dtype_str="integer", dtype=int)
rs_params = SocketAPIParameters(param="RS", dtype_str="real", dtype=float)
ds_params = SocketAPIParameters(param="DS", dtype_str="double", dtype=float)
cs_params = SocketAPIParameters(param="CS", dtype_str="string", dtype=str)

get_binary = partial(
    get_templated,
    param=bs_params.param,
    dtype_str=bs_params.dtype_str,
    dtype=bs_params.dtype,
)
put_binary = partial(
    put_templated,
    param=bs_params.param,
    dtype_str=bs_params.dtype_str,
    dtype=bs_params.dtype,
)

get_integer = partial(
    get_templated,
    param=is_params.param,
    dtype_str=is_params.dtype_str,
    dtype=is_params.dtype,
)
put_integer = partial(
    put_templated,
    param=is_params.param,
    dtype_str=is_params.dtype_str,
    dtype=is_params.dtype,
)

get_real = partial(
    get_templated,
    param=rs_params.param,
    dtype_str=rs_params.dtype_str,
    dtype=rs_params.dtype,
)
put_real = partial(
    put_templated,
    param=rs_params.param,
    dtype_str=rs_params.dtype_str,
    dtype=rs_params.dtype,
)

get_double = partial(
    get_templated,
    param=ds_params.param,
    dtype_str=ds_params.dtype_str,
    dtype=ds_params.dtype,
)
put_double = partial(
    put_templated,
    param=ds_params.param,
    dtype_str=ds_params.dtype_str,
    dtype=ds_params.dtype,
)

get_string = partial(
    get_templated,
    param=cs_params.param,
    dtype_str=cs_params.dtype_str,
    dtype=cs_params.dtype,
)
put_string = partial(
    put_templated,
    param=cs_params.param,
    dtype_str=cs_params.dtype_str,
    dtype=cs_params.dtype,
)


def host_connect(host_name=None, port_number=None):
    """Connect to database host"""

    global atf_db_socket

    #  Check for unexpected arguments
    if host_name is None:
        timestamp()
        print(f"{ATF_DB_ERROR}Database host name = 'None'")
        return None

    if port_number is None:
        timestamp()
        print("{ATF_DB_ERROR}Database port number = 'None'")
        return None

    #  Print message that we are trying to connect
    timestamp()
    print("[This module is to be imported from Pyton 3.x scripts.]")
    print(f"{ATF_DB_NOTE}Connecting to database host {host_name} " f"on port {port_number}...")

    #  Create socket
    try:
        atf_db_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except Exception:
        timestamp()
        print(f"{ATF_DB_ERROR}Problem creating socket")
        return None

    #  Allow port to be reused immediately without any waiting
    try:
        atf_db_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    except Exception:
        timestamp()
        print(f"{ATF_DB_ERROR}Problem setting socket option: SO_REUSEADDR")
        return None

    #  Turn on keepalive
    try:
        atf_db_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    except Exception:
        timestamp()
        print(f"{ATF_DB_ERROR}Problem setting socket option: SO_KEEPALIVE")
        return None

    #  Disable Nagle's algorithm
    try:
        atf_db_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    except Exception:
        timestamp()
        print(f"{ATF_DB_ERROR}Problem setting socket option: TCP_NODELAY")
        return None

    #  Connect to ATF host
    try:
        atf_db_socket.connect((host_name, port_number))  # expects tuple
    except Exception:
        timestamp()
        print(f"{ATF_DB_ERROR}Problem connecting to database host")
        print(f"{ATF_DB_ERROR}Host: {host_name}")
        print(f"{ATF_DB_ERROR}Port: {port_number}")
        return None

    try:
        connection_banner = socket_read()  # noqa
    except Exception:
        timestamp()
        print(f"{ATF_DB_ERROR}Problem reading database host connection banner")
        return None

    timestamp()
    print(f"{ATF_DB_SUCCESS}Successful connection to database host.")


def host_disconnect():
    try:
        atf_db_socket.shutdown(0)
        atf_db_socket.close()
        timestamp()
        print(f"{ATF_DB_NOTE}Socket closed")
        return None
    except Exception:
        timestamp()
        print(f"{ATF_DB_ERROR}Problem closing ATF database socket")
        return None


def sleep(sleep_time=None):
    if sleep_time is None:
        timestamp()
        print(f"{ATF_DB_ERROR}Sleep time specified as 'None'")
        return None
    try:
        time.sleep(sleep_time)
    except KeyboardInterrupt:
        print(f"{ATF_DB_WARNING}Sleep terminated by keyboard interrupt")
        sys.exit()
    except Exception:
        timestamp()
        print(f"{ATF_DB_ERROR}sleep() returned error")
        return None

    return 0


def socket_read():
    global atf_db_socket
    try:
        message = atf_db_socket.recv(ATF_DB_RECEIVE_BUFFER_SIZE)
    except Exception:
        timestamp()
        print(f"{ATF_DB_ERROR}Problem reading from socket")
        return None

    return message


def socket_write(message=None):
    global atf_db_socket
    error_message = f"{ATF_DB_ERROR}Problem writing to database socket"

    if message is None:
        timestamp()
        print(error_message)
        print(f"{ATF_DB_ERROR}Message is 'None'")
        return None

    terminated_message = message.encode() + "\n".encode()
    try:
        atf_db_socket.sendall(terminated_message)
    except Exception:
        timestamp()
        print(error_message)
        print(f"{ATF_DB_ERROR}Trying to write the following:")
        print(repr(terminated_message))
        return None

    return 0


def timestamp():
    print("-" * 26)
    print(str(datetime.datetime.now()))
