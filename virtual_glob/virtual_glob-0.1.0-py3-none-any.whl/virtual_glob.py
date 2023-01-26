"""Globbing of virtual file systems."""
from __future__ import annotations

from abc import abstractmethod
from collections import deque
from fnmatch import fnmatchcase
from functools import lru_cache
import re
from typing import Callable, Iterable, Protocol, TypedDict, TypeVar

__version__ = "0.1.0"


PathType = TypeVar("PathType", bound="VirtualPath")
ItemType = TypeVar("ItemType")


class VirtualPath(Protocol):
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the name of this path."""

    @abstractmethod
    def is_dir(self) -> bool:
        """Return True if this path is a directory."""

    @abstractmethod
    def iterdir(self: PathType) -> Iterable[PathType]:
        """Iterate over the contents of this directory.

        :raise FileNotFoundError: if this path does not exist.
        :raises NotADirectoryError: if this path is not a directory.
        """

    @abstractmethod
    def joinpath(self: PathType, *parts: str) -> PathType:
        """Join this path with the given parts."""

    @abstractmethod
    def exists(self) -> bool:
        """Return True if this path exists."""


class DictFs(TypedDict):
    """A virtual file system backed by a dictionary."""

    is_dir: bool
    name: str
    contents: dict[str, DictFs]


class InMemoryPath(VirtualPath):
    """A virtual path, backed by a dictionary."""

    @classmethod
    def from_list(cls, paths: Iterable[str]) -> InMemoryPath:
        """Create a virtual path from a list of POSIX paths,
        if the path ends with a slash it is a directory.
        """
        fs: DictFs = {"is_dir": True, "name": "", "contents": {}}
        for path in paths:
            sub_fs = fs
            is_dir = path.endswith("/")
            parts = path.rstrip("/").split("/")
            for part in parts[:-1]:
                if part in sub_fs["contents"]:
                    sub_sub_fs = sub_fs["contents"][part]
                else:
                    sub_sub_fs = {"is_dir": True, "name": part, "contents": {}}
                    sub_fs["contents"][part] = sub_sub_fs
                sub_fs = sub_sub_fs
            sub_fs["contents"][parts[-1]] = {
                "is_dir": is_dir,
                "name": parts[-1],
                "contents": {},
            }

        return cls(fs)

    def __init__(self, fs: DictFs, path: tuple[str] = ()) -> None:
        """Initialise the path."""
        self._fs = fs
        self._path = path

    def __repr__(self) -> str:
        """Return a string representation of this path."""
        return f"{self.__class__.__name__}({self.path!r})"

    @property
    def path(self) -> str:
        """Return the path as a string."""
        return "/".join(self._path)

    @property
    def name(self) -> str:
        """Return the name of this path."""
        return self._path[-1] if self._path else ""

    def _get_element(self) -> DictFs | None:
        """Get the element at this path."""
        fs = self._fs
        for part in self._path:
            if part not in fs["contents"]:
                return None
            fs = fs["contents"][part]
        return fs

    def is_dir(self) -> bool:
        fs = self._get_element()
        return fs["is_dir"] if fs is not None else False

    def iterdir(self) -> Iterable[InMemoryPath]:
        fs = self._get_element()
        if fs is None:
            raise FileNotFoundError("path does not exist")
        if not fs["is_dir"]:
            raise NotADirectoryError("path is not a directory")
        for name in fs["contents"]:
            yield InMemoryPath(self._fs, self._path + (name,))

    def joinpath(self, *parts: str) -> InMemoryPath:
        return InMemoryPath(self._fs, self._path + parts)

    def exists(self) -> bool:
        return self._get_element() is not None


def glob(
    path: PathType, pattern: str, *, depth_first: bool = True
) -> Iterable[PathType]:
    """Glob a virtual directory."""

    # initial validation and patterns analysis
    if not path.is_dir():
        raise ValueError("path must be a directory")
    if not pattern:
        raise ValueError("pattern must not be empty")
    if pattern.startswith("/"):
        raise ValueError("pattern must be relative")
    only_dir = pattern.endswith("/")
    pattern_parts = pattern.rstrip("/").split("/")

    queue_pop = _pop_lifo if depth_first else _pop_fifo

    # find the common path in the pattern
    common_path: list[str] = []
    for part in pattern_parts[:]:
        if _has_magic(part):
            break
        path = path.joinpath(part)
        common_path.append(part)
        pattern_parts.pop(0)
    if not path.exists():
        return

    if not pattern_parts:
        # then we can short circuit, by simply yielding the path
        if (not only_dir) or path.is_dir():
            yield path
        return

    if not path.is_dir():
        return

    if pattern_parts == ["**"] or (pattern_parts == ["**", "*"] and only_dir):
        # then we can simply yield all the directories recursively
        if common_path and pattern_parts == ["**"]:
            yield path
        path_queue = deque([p for p in path.iterdir() if p.is_dir()])
        while path_queue:
            item = queue_pop(path_queue)
            yield item
            for subpath in item.iterdir():
                if subpath.is_dir():
                    path_queue.append(subpath)
        return

    if pattern_parts == ["**", "*"] and not only_dir:
        # then we can simply yield recursively
        path_queue: deque[PathType] = deque()
        for item in path.iterdir():
            if item.is_dir():
                path_queue.append(item)
            else:
                yield item
        while path_queue:
            item = queue_pop(path_queue)
            yield item
            for child in item.iterdir():
                if child.is_dir():
                    path_queue.append(child)
                else:
                    yield child
        return

    # check for double star
    has_double_star = False
    for part in pattern_parts:
        if "**" in part:
            has_double_star = True
            if part != "**":
                raise ValueError("Invalid pattern: ** must be the only part of a path")

    if not has_double_star:
        yield from _no_double_star(path, pattern_parts, only_dir, queue_pop)
        return

    # if there are `**` parts, before the end of the pattern,
    # then we need to recurse through every possible path to check for matches
    pattern_regex = _create_regex(pattern.rstrip("/"))
    dstar_queue = deque([(path, common_path[:-1])])
    at_root = not bool(common_path)
    while dstar_queue:
        subpath, rel_dir = queue_pop(dstar_queue)
        if (not only_dir) or subpath.is_dir():
            rel_path = "/".join(rel_dir + [subpath.name])
            if pattern_regex.fullmatch(rel_path):
                yield subpath
        if subpath.is_dir():
            if at_root:
                at_root = False
            else:
                rel_dir = rel_dir + [subpath.name]
            dstar_queue.extend([(p, rel_dir) for p in subpath.iterdir()])


_MAGIC_REGEX = re.compile("[*?[]")


def _has_magic(*string: str):
    """Return True if any of the string have magic characters in them."""
    return any(_MAGIC_REGEX.search(s) is not None for s in string)


def _pop_lifo(queue: deque[ItemType]) -> ItemType:
    """Pop the last item from the queue."""
    return queue.pop()


def _pop_fifo(queue: deque[ItemType]) -> ItemType:
    """Pop the first item from the queue."""
    return queue.popleft()


def _no_double_star(
    path: PathType,
    pattern_parts: list[str],
    only_dir: bool,
    queue_pop: Callable[[deque], tuple[PathType, list[str]]],
) -> Iterable[PathType]:
    """No `***` in the pattern,
    so do simple recursion through the pattern parts,
    halting if the start of the path does not match the start of the pattern
    """
    queue = deque([(path, pattern_parts)])
    while queue:
        subpath, parts = queue_pop(queue)
        if not parts:
            if (not only_dir) or subpath.is_dir():
                yield subpath
            continue
        if not subpath.is_dir():
            continue
        if not _has_magic(*parts):
            # then we can short circuit, by simply checking if the path exists
            only_path = subpath.joinpath(*parts)
            if only_path.exists() and ((not only_dir) or only_path.is_dir()):
                yield only_path
            continue
        part = parts[0]
        for subsubpath in subpath.iterdir():
            if fnmatchcase(subsubpath.name, part):
                queue.append((subsubpath, parts[1:]))


@lru_cache(maxsize=128)
def _create_regex(pattern: str) -> re.Pattern:
    """Create a regex from a glob pattern."""
    regex = ""
    for part in pattern.split("/"):
        if part == "**":
            regex += "([^/]+/)*"  # TODO is this rigorously correct?
        else:
            regex += _translate(part) + "/"
    return re.compile(regex.rstrip("/"))


def _translate(pat):
    """Translate a shell PATTERN to a regular expression.

    This is copied from the fnmatch module, but with the following changes:
    - `*` and `?` use `[^/]` instead of `.`
    - The pattern is not anchored at the start or end

    """
    # TODO can we simplify this, or use the fnmatch module?
    i, n = 0, len(pat)
    res = ""
    while i < n:
        c = pat[i]
        i = i + 1
        if c == "*":
            res = res + "[^/]*"
        elif c == "?":
            res = res + "[^/]"
        elif c == "[":
            j = i
            if j < n and pat[j] == "!":
                j = j + 1
            if j < n and pat[j] == "]":
                j = j + 1
            while j < n and pat[j] != "]":
                j = j + 1
            if j >= n:
                res = res + "\\["
            else:
                stuff = pat[i:j]
                if "--" not in stuff:
                    stuff = stuff.replace("\\", r"\\")
                else:
                    chunks = []
                    k = i + 2 if pat[i] == "!" else i + 1
                    while True:
                        k = pat.find("-", k, j)
                        if k < 0:
                            break
                        chunks.append(pat[i:k])
                        i = k + 1
                        k = k + 3
                    chunks.append(pat[i:j])
                    # Escape backslashes and hyphens for set difference (--).
                    # Hyphens that create ranges shouldn't be escaped.
                    stuff = "-".join(
                        s.replace("\\", r"\\").replace("-", r"\-") for s in chunks
                    )
                # Escape set operations (&&, ~~ and ||).
                stuff = re.sub(r"([&~|])", r"\\\1", stuff)
                i = j + 1
                if stuff[0] == "!":
                    stuff = "^" + stuff[1:]
                elif stuff[0] in ("^", "["):
                    stuff = "\\" + stuff
                res = "%s[%s]" % (res, stuff)
        else:
            res = res + re.escape(c)

    return res
