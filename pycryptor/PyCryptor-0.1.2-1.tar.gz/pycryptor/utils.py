from glob import glob
from pathlib import Path
from hashlib import sha256
from contextlib import suppress
from typing import Union, List


def hash_password(password: bytes) -> bytes:
	"""
	creates a 32 byte sha256 hash from password with 100000 iterations

	Args:
	- `password` (bytes): A sequence of bytes of any lenght
	"""
	for _ in range(100000):
		password = sha256(password).digest()
	return password


def find_pattern_match(pattern: str) -> Union[List[Path], None]:
	"""
	finds all paths matching the given pattern

	Args:
	- `pattern` (str): path pattern to be processed

	Returns:
	- `List[Path]`: a list of paths matching the pattern
	- `None`: if the no matches were found for the pattern a null is returned
	"""
	with suppress(SyntaxError):
		return list(map(Path, glob(pattern)))


def validate_path(file_path: Path) -> None:
	"""
	validates that the path given exists and is a file

	Args:
	- file_path (Path): filepath to be validated
	
	Raises:
	- `TypeError`|`ValueError`: unable to convert file_path arg to pathlib.Path
	- `FileNotFoundError`: the file_path arg does not lead to a file
	- `OSError`: the file_path arg leads to a directory
	"""
	if not isinstance(file_path, Path):
		file_path = Path(file_path)

	if not file_path.is_file():
		raise FileNotFoundError(f"unable to locate file: {file_path}")
	
	elif file_path.is_dir():
		raise OSError("path must be a file not a directory")