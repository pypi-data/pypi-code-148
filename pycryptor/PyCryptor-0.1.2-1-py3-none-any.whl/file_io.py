import os
import struct
from pathlib import Path
from abc import ABC, abstractmethod

from Crypto.Cipher import AES
from rich.progress import Progress

from pycryptor.utils import validate_path
from pycryptor.signature import create_signature, verify_signature


class _BaseIO(ABC):
	def __init__(
			self,
			aes_key: bytes,
			file_path: Path,
			buffer_size: int = 4096
		) -> None:

		self._aes_key = aes_key
		self._file_path = file_path
		self._buffer_size = buffer_size
		
		self._file = open(self._file_path, "rb+")
		self._total_size = os.stat(file_path).st_size

		# cryptography header and CBC cipher
		self._header = None
		self._cipher = None
		self._init_vector = None

		# indicator for when file has been encrypted/decrypted
		self._finished = False
		
		# setup hook will be called before generating the cipher
		# since the EncryptIO and the DecryptIO have different
		# methods of generating/obtaining an initialization vector
		self._setup_hook()
		
		# after the _setup_hook is called and the initialization
		# vector is stored the CBC cipher will be created
		self._create_cipher()

	@abstractmethod
	def _setup_hook(self) -> None: ...

	def _create_cipher(self) -> None:
		self._cipher = AES.new(
			self._aes_key,
			AES.MODE_CBC,
			iv=self._init_vector
		)

	@property
	def finished(self) -> bool:
		return self._finished

	def close(self) -> None:
		self._file.close()

	def __enter__(self) -> object:
		return self

	def __exit__(self) -> None:
		self.close()


class EncryptIO(_BaseIO):
	@property
	def size(self) -> int:
		return self._padded_size

	def _create_header(self) -> None:
		plaintext_size = struct.pack(">Q", self._total_size)

		nonce, tag, ciphertext = create_signature(self._aes_key, self._init_vector)

		self._header = plaintext_size + nonce + tag + ciphertext

	def _add_padding(self) -> None:
		block_offset = (self._total_size % AES.block_size)

		if block_offset:
			padding = b"\xff" * (AES.block_size - block_offset)

			# move to the end of the file and add the padding
			self._file.seek(self._total_size)
			self._file.write(padding)

			self._padded_size = self._file.tell()

			# move back to the start of the file
			self._file.seek(0)
		else:		
			self._padded_size = self._total_size

	def _setup_hook(self) -> None:
		# generate a random initialization vector to be
		# used for the cipher and ciphertext in the header
		self._init_vector = os.urandom(16)
		
		self._create_header()

		# calculate and add required padding if the total
		# file size is not a product of the block size
		self._add_padding()
	
	def _read_buffer(self) -> bytes:
		buffer = self._file.read(self._buffer_size)

		# move back to last offset where the buffer starts
		self._file.seek(self._file.tell() - len(buffer))

		return buffer

	def _encrypt_buffer(self) -> int:
		buffer = self._read_buffer()
		
		ciphertext = self._cipher.encrypt(buffer)

		self._file.write(ciphertext)

		# if the offset is more or equal to the original size
		# the file is fully encrypted and can then have the
		# header written to it
		if self._file.tell() >= self._total_size:
			self._file.write(self._header)
			self._finished = True
		
		return len(buffer)

	def create_task_handler(self, progress: Progress) -> None:
		if self._finished:
			raise IOError("file has already been encrypted")
		
		task = progress.add_task(
			f" {self._file_path.name}",
			total=self.size
		)

		while not self._finished:
			advance_size = self._encrypt_buffer()
			progress.update(task, advance=advance_size)


class DecryptIO(_BaseIO):
	@property
	def size(self) -> int:
		return self._total_size

	def _read_header(self) -> None:
		# move to header start
		self._file.seek(self._total_size)

		# original unencrypted file size in header as unsigned long long
		plaintext_size = struct.unpack(">Q", self._file.read(8))[0]

		# for cryptographic verification
		nonce = self._file.read(16)
		tag = self._file.read(16)
		ciphertext = self._file.read(16)

		self._header = {
			"plaintext_size": plaintext_size,
			"nonce": nonce,
			"tag": tag,
			"ciphertext": ciphertext,
		}

	def _get_init_vector(self):
		# the ciphertext stored in the header is decrypet to the
		# CBC cipher's initialization vector for decrypting the file
		self._init_vector = verify_signature(
			self._aes_key,
			self._header["nonce"],
			self._header["tag"],
			self._header["ciphertext"]
		)
	
	def _setup_hook(self) -> None:
		# removes the header lenght from the total_size
		self._total_size -= 56

		try:
			self._read_header()
		except OSError:
			raise OSError("unable to read encryption header")

		try:
			self._get_init_vector()
		except ValueError:
			raise ValueError("unable to verify signature with encryption key")

		# move offset back to the beginning of the file
		# after having read and decrypted the header
		self._file.seek(0)

	def _read_buffer(self) -> bytes:
		# only read the entire buffer_size if the file end has not been
		# reached to prevent reading the header as part of the next buffer
		current_buffer_size = min(self._total_size - self._file.tell(), self._buffer_size)

		buffer = self._file.read(current_buffer_size)

		# move back to last offset where the buffer starts
		self._file.seek(self._file.tell() - len(buffer))

		return buffer

	def _decrypt_buffer(self) -> int:
		buffer = self._read_buffer()

		plaintext = self._cipher.decrypt(buffer)

		self._file.write(plaintext)

		# if the plaintext_size of the file has been reached
		# or surpassed then the entire file has been decrypted
		if self._file.tell() >= self._header["plaintext_size"]:
			self._file.seek(self._header["plaintext_size"])
			
			# truncate the rest of the file to
			# remove the header and padding
			self._file.truncate()
			
			self._finished = True
		
		return len(buffer)

	def create_task_handler(self, progress: Progress) -> None:
		if self._finished:
			raise IOError("file has already been decrypted")

		task = progress.add_task(
			f" {self._file_path.name}",
			total=self.size
		)

		while not self._finished:
			advance_size = self._decrypt_buffer()
			progress.update(task, advance=advance_size)