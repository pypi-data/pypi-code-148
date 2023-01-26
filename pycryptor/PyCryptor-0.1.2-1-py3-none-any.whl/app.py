from pathlib import Path
from argparse import ArgumentParser

from Crypto.Cipher import AES
from rich.progress import Progress

from pycryptor.file_io import EncryptIO, DecryptIO
from pycryptor.utils import (
	hash_password,
	find_pattern_match,
	validate_path
)


class App:
	ENCRYPT = 0
	DECRYPT = 1

	def __init__(self, parser: ArgumentParser) -> None:
		args = parser.parse_args()

		if not args.paths:
			parser.error("no filepaths provided")

		if args.encrypt and args.decrypt:
			parser.error("too many modes selected")
		
		if args.key is None:
			parser.error("missing key argument when decrypting")

		if (args.buffer_size % AES.block_size):
			parser.error(f"buffer_size must be a product of {AES.block_size}")

		path_args = []
		for path in args.paths:
			matches = find_pattern_match(path)

			if not matches:
				matches = [Path(path)]

			for match in matches:
				try:
					validate_path(match)
				except OSError as e:
					parser.error(e)

			path_args.extend(matches)
		
		self._mode = self.ENCRYPT if args.encrypt else self.DECRYPT
		self._mode_str = "encrypt" if args.encrypt else "decrypt"

		self._key = hash_password(args.key.encode())
		self._paths = path_args
		self._buffer_size = args.buffer_size


	def _display_logo(self) -> None:
		print(
			"\n\x1b[96m"
			" ╔═════════════════════════════════════════════════════════╗\n"
			" ║      ____        ______                 __              ║\n"
			" ║     / __ \__  __/ ____/______  ______  / /_____  _____  ║\n"
			" ║    / /_/ / / / / /   / ___/ / / / __ \/ __/ __ \/ ___/  ║\n"
			" ║   / ____/ /_/ / /___/ /  / /_/ / /_/ / /_/ /_/ / /      ║\n"
			" ║  /_/    \__, /\____/_/   \__, / .___/\__/\____/_/       ║\n"
			" ║        /____/           /____/_/                        ║\n"
			" ║                                                         ║\n"
			" ╚═════════════════════════════════════════════════════════╝"
			"\x1b[0m\n"
		)

	def _display_params(self) -> None:
		print(
			f" operation mode : {self._mode_str}\n"
			f" total files    : {len(self._paths)} files\n"
			f" buffer size    : {self._buffer_size}\n"
		)

	def run(self) -> None:
		self._display_logo()
		self._display_params()

		with Progress() as progress:
			for path in self._paths:
				if self._mode == self.ENCRYPT:
					crypt_file = EncryptIO(self._key, path, self._buffer_size)
				else:
					crypt_file = DecryptIO(self._key, path, self._buffer_size)

				crypt_file.create_task_handler(progress)
				crypt_file.close()