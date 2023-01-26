"""Start a HTTP server"""

import os
import sys
import signal
from . import connection
from .httpHandler import Request, Response

PATH = os.getcwd()
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8000

def signal_handler(_, __):
    """Execute handler"""
    print("\nKeyboard interrupt received, killing execution.")
    connection.close(socket)
    sys.exit(0)


def set_config():
    """Set server configurations"""
    global SERVER_HOST, SERVER_PORT, PATH

    for arg in sys.argv:
        arg_list = arg.split("=", maxsplit=1)

        cmd = arg_list[0]
        val = arg_list[1] if len(arg_list) > 1 else ""

        print(cmd, val)
        if val == "":
            continue
        if cmd in ["-h", "--host"]:
            SERVER_HOST = val
        if cmd in ["-p", "--port"]:
            SERVER_PORT = int(val)
        if cmd in ["-pth", "--path"]:
            PATH = val


def get_content(fpath) -> bytes:
    """Get required request contents

    :param path: str - the file path
    :return bytes file contents in bytes
    """
    with open(fpath, 'rb') as file:
        content = file.read()
        file.close()

    return content


def try_or_die(func) -> None:
    """Try a function or die

    :param func: function - Function to be called
    :return None
    """
    try:
        func()
    except Exception:
        return


def log_status(request, response) -> None:
    """Log server status

    :param request: request
    :param response: response
    :return None
    """
    print(
        f"{request.type} [{response.code.decode().split()[0]}]: {request.path}")


def handle_request() -> None:
    """Handle incoming request"""

    con, _ = socket.accept()
    con.settimeout(1)

    request = Request(con.recv(2048).decode())
    response = Response()

    print(request.path)

    path = PATH + request.path

    if not request.is_allowed_type():
        try_or_die(lambda: response.set_content(
            get_content(PATH + '/405.html')))
        response.set_405()
    else:
        try:
            response.set_content_type(request.extension)
            response.set_content(get_content(path))
            response.set_success()
        except FileNotFoundError:
            try_or_die(lambda: response.set_content(
                get_content(PATH + '/404.html')))
            response.set_404()

    con.sendall(response.get_response())
    log_status(request, response)
    con.close()


set_config()

(socket, _) = connection.init(SERVER_HOST, SERVER_PORT)
socket.settimeout(1)
signal.signal(signal.SIGINT, signal_handler)


def main() -> None:
    """Execute starts here"""

    while True:
        try:
            handle_request()
        except TimeoutError:
            continue
