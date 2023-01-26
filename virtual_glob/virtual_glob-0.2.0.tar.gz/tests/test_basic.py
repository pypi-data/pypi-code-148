from __future__ import annotations

from pathlib import Path
import sys

import pytest

from virtual_glob import InMemoryPath, glob

TESTS: list[tuple[str | list[str], str, list[str]]] = [
    # simple file names
    ("a.txt", "b.txt", []),
    ("a.txt", "A.txt", []),  # case sensitive
    ("a.txt", "a.txt", ["a.txt"]),
    ("a.txt", "*.txt", ["a.txt"]),
    ("a.txt", "a.*", ["a.txt"]),
    ("a.txt", "?.txt", ["a.txt"]),
    ("a.txt", "a?.txt", []),
    ("a.txt", "[a].txt", ["a.txt"]),
    ("a.txt", "[a-z].txt", ["a.txt"]),
    ("a.txt", "[A-Z].txt", []),
    ("a.txt", "[!a].txt", []),
    ("a.txt", "[!A].txt", ["a.txt"]),
    ("a.txt", "[!A-Z].txt", ["a.txt"]),
    ("a.txt", "[!a-z].txt", []),
    # simple directories
    ("a/b.txt", "c/b.txt", []),
    ("a/b.txt", "a/b.txt", ["a/b.txt"]),
    ("a/b.txt", "*/b.txt", ["a/b.txt"]),
    ("a/b.txt", "*", ["a"]),
    # multiple directories
    (("a/b/c", "d/e/c"), "*/*/c", ["a/b/c", "d/e/c"]),
    (("a/b/c", "d/b/c"), "*/b/c", ["a/b/c", "d/b/c"]),
    (("a/b/c/", "a/d/c/"), "a/*/c", ["a/b/c", "a/d/c"]),
    (("a/b/c/", "a/d/c"), "a/*/c/", ["a/b/c"]),
    # recurse with **
    ("a/b/c/d.txt", "a/b/c/d.txt", ["a/b/c/d.txt"]),
    ("a/b/c/d.txt", "a/b/c/?.txt", ["a/b/c/d.txt"]),
    ("a/b/c/d.txt", "a/b/c/[a-z].txt", ["a/b/c/d.txt"]),
    ("a/b/c/d.txt", "a/b/c/[!0-9].txt", ["a/b/c/d.txt"]),
    ("a/b/c/d.txt", "a/**/c/d.txt", ["a/b/c/d.txt"]),
    ("a/b/c/d.txt", "a/**/**/c/d.txt", ["a/b/c/d.txt"]),
    ("a/b/c/d.txt", "a/**/**/c/?.txt", ["a/b/c/d.txt"]),
    ("a/b/c/d.txt", "a/**/**/c/d?.txt", []),
    ("a/b/c/d.txt", "a/**/**/c/[a-z].txt", ["a/b/c/d.txt"]),
    ("a/b/c/d.txt", "a/**/**/c/[0-9].txt", []),
    ("a/b/c/d.txt", "a/**/**/c/[!0-9].txt", ["a/b/c/d.txt"]),
    ("a/b/c/d.txt", "a/**/d.txt", ["a/b/c/d.txt"]),
    ("a/b/c/d.txt", "**/*", ["a", "a/b", "a/b/c", "a/b/c/d.txt"]),
    ("a/b/c/d.txt", "**", ["a", "a/b", "a/b/c"]),
    ("a/b/c/d.txt", "**/", ["a", "a/b", "a/b/c"]),
    ("a/b/c/d.txt", "**/d.txt", ["a/b/c/d.txt"]),
    ("a/b/c/d.txt", "a/b/**/*", ["a/b/c", "a/b/c/d.txt"]),
    ("a/b/c/d.txt", "a/b/**", ["a/b", "a/b/c"]),
    ("a/b/c/d.txt", "a/b/**/", ["a/b", "a/b/c"]),
    ("a/b/c/d.txt", "a/b/c/d.txt/**", []),
    # recursing can end anywhere
    ("a/b/b/d.txt", "a/**/b/b/d.txt", ["a/b/b/d.txt"]),
    ("a/b/b/d.txt", "a/**/b/d.txt", ["a/b/b/d.txt"]),
    # Return only directories if pattern ends with a pathname components separator
    ("a/b/c/d.txt", "**/*/", ["a", "a/b", "a/b/c"]),
]


@pytest.mark.parametrize(
    "paths, pattern, expected", TESTS, ids=[f"{t[0]};{t[1]}" for t in TESTS]
)
def test_baseline_pathlib(
    paths: str | list[str], pattern: str, expected: list[str], tmp_path: Path
) -> None:
    """A test baseline, against the behaviour of `pathlib.Path.glob`"""
    if pattern == "A.txt":
        pytest.skip("case sensitive")
    if pattern.endswith("/") and sys.version_info < (3, 11):
        pytest.skip("only returning directories added in python 3.11")

    if isinstance(paths, str):
        paths = [paths]
    for path in paths:
        path_obj = tmp_path / path
        path_obj.parent.mkdir(parents=True, exist_ok=True)
        if path.endswith("/"):
            path_obj.mkdir(parents=True, exist_ok=True)
        else:
            path_obj.touch()

    assert (
        sorted(
            [
                p.relative_to(tmp_path).as_posix()
                for p in tmp_path.glob(pattern)
                # `**` also returns the directory itself, which we don't want
                if p != tmp_path
            ]
        )
        == expected
    )


@pytest.mark.parametrize(
    "paths, pattern, expected", TESTS, ids=[f"{t[0]};{t[1]}" for t in TESTS]
)
def test_pathlib(
    paths: str | list[str], pattern: str, expected: list[str], tmp_path: Path
) -> None:
    """Test using `pathlib.Path` as the virtual filesystem."""
    if pattern == "A.txt":
        # TODO case-sensitivity depends on the filesystem, in particular the .exists()
        pytest.skip("case sensitive")

    if isinstance(paths, str):
        paths = [paths]
    for path in paths:
        path_obj = tmp_path / path
        path_obj.parent.mkdir(parents=True, exist_ok=True)
        if path.endswith("/"):
            path_obj.mkdir(parents=True, exist_ok=True)
        else:
            path_obj.touch()

    assert (
        sorted([p.relative_to(tmp_path).as_posix() for p in glob(tmp_path, pattern)])
        == expected
    )


@pytest.mark.parametrize(
    "paths, pattern, expected", TESTS, ids=[f"{t[0]};{t[1]}" for t in TESTS]
)
def test_virtual(paths: str | list[str], pattern: str, expected: list[str]) -> None:
    """Test using `pathlib.Path` as the virtual filesystem."""
    path = InMemoryPath.from_list([paths] if isinstance(paths, str) else paths)
    assert sorted([p.path for p in glob(path, pattern)]) == expected


@pytest.mark.parametrize("glob_str", ("**", "**/", "**/*", "**/*/"))
def test_depth_first(glob_str) -> None:
    """Test that the depth-first search is used."""
    path = InMemoryPath.from_list(["a/b/c/d/", "e/f/g/h/"])
    expected = ["e", "e/f", "e/f/g", "e/f/g/h", "a", "a/b", "a/b/c", "a/b/c/d"]
    assert [p.path for p in glob(path, glob_str, depth_first=True)] == expected


@pytest.mark.parametrize("glob_str", ("**", "**/", "**/*", "**/*/"))
def test_breadth_first(glob_str) -> None:
    """Test that the breadth-first search is used."""
    path = InMemoryPath.from_list(["a/b/c/d/", "e/f/g/h/"])
    expected = ["a", "e", "a/b", "e/f", "a/b/c", "e/f/g", "a/b/c/d", "e/f/g/h"]
    assert [p.path for p in glob(path, glob_str, depth_first=False)] == expected


def test_depth_first_files() -> None:
    """Test that the depth-first search is used."""
    path = InMemoryPath.from_list(["a/b/c/d", "a/b/x", "a/b/y", "e/f/g/h"])
    expected = [
        "e",
        "e/f",
        "e/f/g",
        "e/f/g/h",
        "a",
        "a/b",
        "a/b/x",
        "a/b/y",
        "a/b/c",
        "a/b/c/d",
    ]
    assert [p.path for p in glob(path, "**/*", depth_first=True)] == expected


def test_breadth_first_files() -> None:
    """Test that the breadth-first search is used."""
    path = InMemoryPath.from_list(["a/b/c/d", "a/b/x", "a/b/y", "e/f/g/h"])
    expected = [
        "a",
        "e",
        "a/b",
        "a/b/x",
        "a/b/y",
        "e/f",
        "a/b/c",
        "a/b/c/d",
        "e/f/g",
        "e/f/g/h",
    ]
    assert [p.path for p in glob(path, "**/*", depth_first=False)] == expected


def test_symlink_pathlib(tmp_path: Path):
    """Test follow_symlinks for Path."""
    path = tmp_path / "a/d/c"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch()
    (tmp_path / "a/b").symlink_to(tmp_path / "a/d")
    assert {p.relative_to(tmp_path).as_posix() for p in glob(tmp_path, "**/c")} == {
        "a/d/c"
    }
    assert {
        p.relative_to(tmp_path).as_posix()
        for p in glob(tmp_path, "**/c", follow_symlinks=True)
    } == {"a/b/c", "a/d/c"}


def test_symlink_in_memory():
    """Test follow_symlinks for InMemoryPath."""
    path = InMemoryPath.from_list(["a/b/c", "a/d/c"])
    path.joinpath("a", "b")._get_element()["is_symlink"] = True
    assert {p.path for p in glob(path, "**/c")} == {"a/d/c"}
    assert {p.path for p in glob(path, "**/c", follow_symlinks=True)} == {
        "a/b/c",
        "a/d/c",
    }
