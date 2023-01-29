from __future__ import annotations

# 防止安装后引用路径错误，应该加上"."，但是vscode开发时则因为项目路径问题可以不加
try:
    from .dedup import URLFilter, RedisURLFilter
except:
    from dedup import URLFilter, RedisURLFilter


__docformat__ = "restructuredtext"

# Let users know if they're missing any of our hard dependencies
_hard_dependencies = ["redis"]
_missing_dependencies = []

for _dependency in _hard_dependencies:
    try:
        __import__(_dependency)
    except ImportError as _e:
        _missing_dependencies.append(f"{_dependency}: {_e}")

if _missing_dependencies:
    raise ImportError(
        "Unable to import required dependencies:\n" + "\n".join(_missing_dependencies)
    )
del _hard_dependencies, _dependency, _missing_dependencies



__all__ = [
    "URLFilter", "RedisURLFilter"
]

