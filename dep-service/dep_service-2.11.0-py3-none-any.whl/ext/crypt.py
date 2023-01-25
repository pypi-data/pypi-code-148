"""Crypt tickets."""

from typing import Dict

from base64 import urlsafe_b64decode, urlsafe_b64encode

from spec.types import AnyApp
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms

import ujson


def add_state_cipher(app: AnyApp) -> None:
    """Add app state cipher."""

    cipher = create_cipher(
        key=app.settings.cipher_key.get_secret_value(),  # noqa
        nonce=app.settings.cipher_nonce.get_secret_value(),  # noqa
    )

    app.state.cipher = cipher


def create_cipher(key: str, nonce: str) -> Cipher:
    """Create cipher."""

    c_key, c_nonce = urlsafe_b64decode(key), urlsafe_b64decode(nonce)
    algorithm = algorithms.ChaCha20(c_key, c_nonce)
    return Cipher(algorithm, mode=None, backend=default_backend())


def crypt(crypto_data: Dict, cipher: Cipher) -> str:
    """Crypt data."""

    crypto = cipher.encryptor().update(ujson.dumps(crypto_data).encode())
    return urlsafe_b64encode(crypto).decode()


def uncrypt(crypto: str,  cipher: Cipher) -> Dict:
    """Uncrypt data."""
    decoded = urlsafe_b64decode(crypto.encode())
    try:
        return ujson.loads(cipher.decryptor().update(decoded))
    except ujson.JSONDecodeError:
        return dict()
