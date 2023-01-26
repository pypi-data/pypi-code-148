# -*- coding: utf-8 -*-

# Copyright (c) 2022 Javier Escalada Gómez
# All rights reserved.
# License: BSD 3-Clause Clear License (see LICENSE for details)

"""
A JSON encoder that allows customizing the indentation based on the content and
the width of the line.
"""

__author__ = "Javier Escalada Gómez"
__email__ = "kerrigan29a@gmail.com"
__version__ = "0.5.0"
__license__ = "BSD 3-Clause Clear License"

# Inspiration: https://gist.github.com/jannismain/e96666ca4f059c3e5bc28abb711b5c92

from json import JSONEncoder, dump, dumps


def indentation_policy_default(path, collection, indent, width):
    """Default indentation policy.

    Indent always except when the collection is empty.

    Args:
        path (list): The path of the current collection.
        collection: The collection to be indented.
        indent: The current indentation.
        width (int): The width of the line.
    """
    if len(collection) == 0:
        return False
    return True


class CustomJSONEncoder(JSONEncoder):
    """Custom JSON encoder.

    This class allows customizing the indentation based on the content and the
    width of the line.
    """

    def __init__(self, *args, **kwargs):
        if kwargs.get("indent") is None:
            kwargs.update({"indent": 2})
        if kwargs.get("separators") is None:
            kwargs.update({"separators": (",", ": ")})
        self.compact_item_separator, self.compact_key_separator = kwargs.pop(
            "compact_separators", (", ", ": "))
        self.indentation_policy = kwargs.pop("indentation_policy",
            indentation_policy_default)
        self.width = kwargs.pop("width", 0)
        super().__init__(*args, **kwargs)

    def iterencode(self, o, *args, **kwargs):
        return self._wrap(self._iterencode(o, []))

    def encode(self, o):
        return "".join(self.iterencode(o))

    def _parent_encode(self, o):
        return JSONEncoder.iterencode(self, o)

    def _iterencode(self, o, path):
        if isinstance(o, (list, tuple)):
            yield from self._iterencode_list(o, path)
        elif isinstance(o, dict):
            yield from self._iterencode_dict(o, path)
        else:
            yield from self._parent_encode(o)
    
    def _iterencode_list(self, o, path):
        depth = len(path)
        nl_sep, ind_sep, it_sep, _ = self._config(path, o)
        yield "["
        for i, el in enumerate(o):
            if i > 0:
                yield it_sep
            yield from (nl_sep, (depth + 1) * ind_sep)
            yield from self._iterencode(el, path + [i])
        yield from (nl_sep, depth * ind_sep, "]")
    
    def _iterencode_dict(self, o, path):
        depth = len(path)
        nl_sep, ind_sep, it_sep, key_sep = self._config(path, o)
        yield "{"
        for i, (k, v) in enumerate(o.items()):
            if i > 0:
                yield it_sep
            yield from (nl_sep, (depth + 1) * ind_sep)
            yield from self._parent_encode(k)
            yield key_sep
            yield from self._iterencode(v, path + [k])
        yield from (nl_sep, depth * ind_sep, "}")

    def _indent_str(self):
        if isinstance(self.indent, int):
            return self.indent * " "
        return self.indent

    def _indent_len(self):
        if isinstance(self.indent, int):
            return self.indent
        return len(self.indent)

    def _config(self, path, collection):
        if self.indentation_policy(path, collection, self.indent, self.width):
            return "\n", self._indent_str(), self.item_separator, self.key_separator
        return "", "", self.compact_item_separator, self.compact_key_separator

    def _wrap(self, tokens):
        col = 1
        prefix = ""
        for token in tokens:
            if token == "":
                continue

            if not self.width:
                yield token
                continue

            if token == "\n":
                col = 1
                yield token
                continue

            if col == 1 and all(c in [" ", "\t"] for c in token):
                prefix = token
                col += len(token)
                yield token
                continue

            col += len(token)
            if col > self.width + 1:
                if token in [
                    self.compact_item_separator,
                    self.compact_key_separator,
                    self.item_separator,
                    self.key_separator,
                    "[",
                    "]",
                    "{",
                    "}",
                ]:
                    yield token
                    continue

                new_col = 1 + len(prefix) + self._indent_len() + len(token)
                if new_col <= self.width + 1:
                    yield from ("\n", prefix, self._indent_str())
                    col = new_col

            yield token


def _normalize_kwargs(kwargs, indentation_policy, width):
    if kwargs.get("indent", None) is None:
        kwargs.pop("indentation_policy", None)
        kwargs.pop("width", None)
    else:
        kwargs["cls"] = CustomJSONEncoder
        kwargs["indentation_policy"] = kwargs.get("indentation_policy",
            indentation_policy or indentation_policy_default)
        kwargs["width"] = kwargs.get("width", width)
    return kwargs


def wrap_dump(indentation_policy=None, width=0):
    """Wrap the json.dump function to use the CustomJSONEncoder.

    If indent is None, no indentation is used, otherwise the indentation is
    determined by the indentation_policy and the width.
    """
    def wrapper(*args, **kwargs):
        return dump(*args, **_normalize_kwargs(kwargs, indentation_policy,
            width))
    return wrapper


def wrap_dumps(indentation_policy=None, width=0):
    """Wrap the json.dumps function to use the CustomJSONEncoder.

    If indent is None, no indentation is used, otherwise the indentation is
    determined by the indentation_policy and the width.
    """
    def wrapper(*args, **kwargs):
        return dumps(*args, **_normalize_kwargs(kwargs, indentation_policy,
            width))
    return wrapper
