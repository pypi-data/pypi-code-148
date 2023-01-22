"""MIT License

Copyright (c) 2023-present Tanner B. Corcoran

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""

from typing import Union
from . import exceptions
from . import constants
from . import models
from . import types
import plogging
import logging
import inspect
import string
import typing
import prepr
import re


str_formatter = string.Formatter()
del string


plural_flag_to_plural = {
    "p": "s",
    "P": "S",
    "ep": "es",
    "eP": "eS",
    "Ep": "Es",
    "EP": "ES",
}


def _default_fmt(field_name: str, _format_spec: str, _conversion: str) -> str:
    return f"{{{field_name}{_conversion}{_format_spec}}}"


def _mangled_fmt(parent: str, child: str, _format_spec: str, _conversion: str) -> str:
    return f"{{_{parent}__{child}{_conversion}{_format_spec}}}"


class AllPretty:
    def __repr__(self, *args, **kwargs) -> prepr.pstr:
        attrs = {k:getattr(self, k) for k in self.__slots__}
        return prepr.prepr(self).kwargs(**attrs).build(simple=True, *args, **kwargs)


class ParseArg(AllPretty):
    __slots__ = ("key", "pretext", "fmt", "required")
    def __init__(self, key: str, pretext: str, fmt: str, required: bool) -> None:
        self.key = key
        self.pretext = pretext
        self.fmt = fmt
        self.required = required


class Flag(AllPretty):
    """Stores any valid flag in `VALID_FLAGS` along with any plural specifiers and extra defaults
    connected to it.
    
    """
    _log = plogging.setup_new("Flag", level=logging.INFO, package=__name__)
    __slots__ = ("name", "plurals", "parse_args", "parse_args_locked", "extras")
    def __init__(self, name: str) -> None:
        Flag._log.debug(f"Creating flag: '{name}'")
        self.name = name
        self.plurals: set[str] = set()
        self.parse_args: list[ParseArg] = list()
        self.parse_args_locked: bool = False # if True, no additional parse args will be added
        self.extras: set[str] = set()
        # extras are stored as a defaultdict to act as a lazy ordered set
        # self.extras: collections.defaultdict[str, None] = collections.defaultdict(lambda: None)

    def get_parse_info(self, defaults: dict[str, typing.Any],
                       target_regex: str = None) -> tuple[re.Pattern, int]:
        len_ = 0
        parse_data: list[str] = [target_regex or "(\d+)"]
        for arg in self.parse_args:
            # add pretext
            len_ += len(arg.pretext)
            parse_data.append(re.escape(arg.pretext))

            # handle if plural flag
            if arg.key in constants.PLURAL_FLAGS:
                parse_data.append(f"(?:{plural_flag_to_plural[arg.key]})?")
                continue
            
            # get the corresponding value from defaults
            try:
                default = defaults[arg.key]
            except KeyError as exc:
                raise exceptions.ParseError(f"Missing default: {arg.key}") from exc
            
            # handle if function
            if inspect.isfunction(default):
                parse_data.append(".*?")
                continue

            # handle arg with str(ifyable) default
            default = str(default)
            if arg.required:
                len_ += len(default)
                parse_data.append(re.escape(default))
                continue
            parse_data.append(f"(?:{re.escape(default)})?")

        return re.compile("".join(parse_data).strip("\\ ")), len_

    def get_plurals(self) -> dict[str, str]:
        """Get converted plural flags.
        
        """
        Flag._log.debug(f"Acquiring converted plural specifiers for flag: '{self.name}'")
        plurals = {f"_{self.name}__{spec}": plural_flag_to_plural[spec]
                   for spec in self.plurals}
        return plurals
    
    def get_empty_plurals(self) -> dict[str, str]:
        """Get plural flags with values as empty strings.
        
        """
        Flag._log.debug(f"Acquiring empty plural specifiers for flag: '{self.name}'")
        plurals = {f"_{self.name}__{spec}": "" for spec in self.plurals}
        return plurals

    def get_extras(self, defaults: dict) -> tuple[dict[str, str],
                                                  dict[str, typing.Callable[[models.TimeValue],
                                                                            typing.Any]]]:
        """Get extra flags with their corresponding values from `defaults`.
        
        """
        kwargs: dict[str, str] = dict()
        funcs: dict[str, typing.Callable[[models.TimeValue], typing.Any]] = dict()
        Flag._log.debug(f"Acquiring extras for flag: '{self.name}' with defaults: {defaults}")
        for ext in self.extras:
            try:
                d = defaults[ext]
                if inspect.isfunction(d):
                    funcs[f"_{self.name}__{ext}"] = d
                else:
                    kwargs[f"_{self.name}__{ext}"] = d
            except KeyError as exc:
                raise KeyError(f"Missing default: {ext}") from exc
        return kwargs, funcs
    
    def get_empty_extras(self) -> dict[str, str]:
        """Get extras with values as empty strings.
        
        """
        Flag._log.debug(f"Acquiring empty extras for flag: '{self.name}'")
        extras = {f"_{self.name}__{ext}": "" for ext in self.extras}
        return extras

    def get_empty_kwargs(self) -> dict[str, str]:
        """Get plurals, extras, and this flag with values as empty strings.
        
        """
        Flag._log.debug(f"Acquiring empty kwargs for flag: '{self.name}'")
        kwargs = {self.name: ""}
        kwargs.update(self.get_empty_plurals())
        kwargs.update(self.get_empty_extras())
        return kwargs


class Flags(list[Flag], AllPretty):
    _log = plogging.setup_new("Flags", level=logging.INFO, package=__name__)
    def __contains__(self, other: Union[str, Flag]) -> bool:
        if isinstance(other, Flag):
            other = other.name
        for f in self:
            if f.name == other:
                return True
        return False
    
    def __getitem__(self, index: Union[str, Flag, int]) -> Flag:
        if isinstance(index, int):
            return super().__getitem__(index)

        if isinstance(index, Flag):
            index = index.name
        for f in self:
            if f.name == index:
                return f
        raise KeyError
    
    @typing.overload
    def get(self, index: Union[str, Flag, int], /) -> Flag: ...
    @typing.overload
    def get(self, index: Union[str, Flag, int], default: types.T, /) -> Union[Flag, types.T]: ...
    def get(self, index: Union[str, Flag, int], default = types.MISSING, /):
        """Get a `Flag` instance contained within this list given a flag name (str), a `Flag`
        instance (in which case `Flag.name` is used), or an integer (in which case the value at
        that index is returned). If a `default` is provided, that default will be returned if no
        `Flag` instance is found.
        
        """
        if default is types.MISSING:
            Flags._log.debug(f"Acquiring flag by index: {index}")
            return self[index]
        Flags._log.debug(f"Acquiring flag by index: {index}; default={default}")
        try:
            return self[index]
        except KeyError:
            return default


def _add_parse_args(literal_text: str, field_name: str, _format_spec: str, _conversion: str,
                    required: bool, current_base_flag: Flag) -> None:
    if not current_base_flag.parse_args_locked:
        current_base_flag.parse_args.append(ParseArg(field_name, literal_text,
                                                     _default_fmt(field_name, _format_spec,
                                                                  _conversion), required))


def _add_parented_flag(literal_text: str, field_name: str, _format_spec: str, _conversion: str,
                       flags: Flags, current_base_flag: Union[Flag, None]) -> str:
    left, _, right = field_name.partition(".")

    # determine the parent and child flags
    if left in constants.BASE_FLAGS:
        parent, child = left, right
    elif right in constants.BASE_FLAGS:
        child, parent = left, right
    else:
        raise ValueError(f"Flag specifies a parent but no valid base flag was found: {field_name}")

    if child in constants.BASE_FLAGS:
        raise ValueError("Child flag may not be a base flag")

    # get or create a flag
    flag = flags.get(parent, None)
    if flag is None:
        flag = Flag(parent)
        flags.append(flag)
    
    # add parse args
    if current_base_flag is not None:
        if flag.name == current_base_flag.name:
            parse_args_required = True
        else:
            parse_args_required = False
        _add_parse_args(literal_text, child, _format_spec, _conversion, parse_args_required,
                        current_base_flag)
        
    # add the info to the flag
    if child in constants.PLURAL_FLAGS:
        flag.plurals.add(child)
    else:
        flag.extras.add(child)

    return _mangled_fmt(parent, child, _format_spec, _conversion)


def _add_plural_flag(literal_text: str, field_name: str, _format_spec: str, _conversion: str,
                     current_base_flag: Union[Flag, None]) -> str:
    if not current_base_flag:
        raise ValueError("Plural flags may not be used before a base flag if a parent is not "
                         "specified. Try specifying a parent or prefixing the flag name with an "
                         "underscore")
    current_base_flag.plurals.add(field_name)
    _add_parse_args(literal_text, field_name, _format_spec, _conversion, False, current_base_flag)
    return _mangled_fmt(current_base_flag.name, field_name, _format_spec, _conversion)


def _add_extra(literal_text: str, field_name: str, _format_spec: str, _conversion: str,
               current_base_flag: Union[Flag, None]) -> str:
    if not current_base_flag:
        raise ValueError("Extra flags may not be used before a base flag if a parent is not "
                         "specified. Try specifying a parent or prefixing the flag name with an "
                         "underscore")
    current_base_flag.extras.add(field_name)
    _add_parse_args(literal_text, field_name, _format_spec, _conversion, True, current_base_flag)
    return _mangled_fmt(current_base_flag.name, field_name, _format_spec, _conversion)


def _add_base_flag(field_name: str, _format_spec: str, _conversion: str, flags: Flags) -> str:
    if field_name not in flags:
        flags.append(Flag(field_name))
    return _default_fmt(field_name, _format_spec, _conversion)


def update_fmt(fmt: types.SupportsBracketFormat) -> tuple[Flags, types.SupportsBracketFormat]:
    data: list[str] = list()
    flags: Flags = Flags()
    current_base_flag: Flag = None
    for literal_text, field_name, format_spec, conversion in str_formatter.parse(fmt):
        if literal_text:
            data.append(literal_text)

        # usually only happens at the very end if there is leftover text
        if field_name is None and format_spec is None and conversion is None:
            continue
        
        if not field_name:
            raise ValueError("Positional-only fields are not allowed in this context")

        _format_spec = f":{format_spec}" if format_spec else ""
        _conversion = f"!{conversion}" if conversion else ""

        # ignored
        if field_name.startswith("_"):
            data.append(_default_fmt(field_name, _format_spec, _conversion))
            continue

        # field specifies a parent
        if "." in field_name:
            data.append(_add_parented_flag(literal_text, field_name, _format_spec, _conversion,
                                           flags, current_base_flag))
            continue
        
        # field is a plural flag
        if field_name in constants.PLURAL_FLAGS:
            data.append(_add_plural_flag(literal_text, field_name, _format_spec, _conversion,
                                         current_base_flag))
            continue
        
        # field is a base flag
        if field_name in constants.BASE_FLAGS:
            data.append(_add_base_flag(field_name, _format_spec, _conversion, flags))
            if current_base_flag:
                current_base_flag.parse_args_locked = True
            current_base_flag = flags.get(field_name)
            continue
        

        data.append(_add_extra(literal_text, field_name, _format_spec, _conversion,
                               current_base_flag))
    
    return flags, "".join(data)
        