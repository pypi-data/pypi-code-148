from httpx import Response, codes

from phiterm.utils.cli_console import log_auth_error_msg, log_server_error_msg


def invalid_response(r: Response) -> bool:
    """returns true if the response is invalid"""

    if r.status_code in (
        codes.UNAUTHORIZED,
        codes.BAD_REQUEST,
    ):
        log_auth_error_msg()
        return True
    if codes.is_server_error(r.status_code):
        log_server_error_msg()
        return True
    return False
