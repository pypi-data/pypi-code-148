import os.path
from hashlib import sha256
import logging
import time


logger = logging.getLogger(__name__)


class Credentials(object):
    def __init__(self, public_key: str, private_key: str):
        self._public_key = str(public_key)
        self._private_key = str(private_key)

    def get(self):
        token = int(1000 * time.time())
        signature = sha256((self._private_key + str(token) + self._public_key).encode()).hexdigest()
        return {
            "public": self._public_key,
            "token": token,
            "signature": signature,
        }

    @staticmethod
    def from_file(file_name: str):
        if not os.path.isfile(file_name):
            logger.warning(f"Could not load credentials from non-existent file '{file_name}'.")
            return None

        with open(file_name, "r") as f:
            lines = f.read().splitlines()

        if len(lines) < 2:
            raise RuntimeError(f"Not enough lines in '{file_name}'. Expected (at least) 2, found {len(lines)}.")

        return Credentials(lines[0], lines[1])
