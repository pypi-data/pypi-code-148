from typing import Tuple

from Crypto.Cipher import AES


def create_signature(aes_key: bytes, plaintext: bytes) -> Tuple[bytes, bytes, bytes]:
	"""
	creates a unique signature using an EAX cipher

	Args:
	- `aes_key` (bytes): 128 or 192 or 256 bit aes symmetric key
	- `plaintext` (bytes): random data to be encrypted as signature

	Returns:
	- `Tuple[bytes, bytes, bytes]`: returns the nonce, tag, and ciphertext of the signature
	"""
	cipher = AES.new(aes_key, AES.MODE_EAX)
	ciphertext, tag = cipher.encrypt_and_digest(plaintext)

	return cipher.nonce, tag, ciphertext


def verify_signature(aes_key: bytes, nonce: bytes, tag: bytes, ciphertext: bytes) -> bytes:
	"""
	verifies a signature generated using an EAX cipher

	Args:
	- `aes_key` (bytes): 128 or 192 or 256 bit aes symmetric key
	- `nonce` (bytes): 16 byte pseudo-random number
	- `tag` (bytes): 16 byte authentication tag
	- `ciphertext` (bytes): 16 byte encrypted block
	
	Raises:
	- `ValueError`: the signature can't be verified by the key
	"""
	cipher = AES.new(aes_key, AES.MODE_EAX, nonce)
	plaintext = cipher.decrypt_and_verify(ciphertext, tag)

	return plaintext