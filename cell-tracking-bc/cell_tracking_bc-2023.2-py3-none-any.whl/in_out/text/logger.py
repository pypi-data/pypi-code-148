# Copyright CNRS/Inria/UCA
# Contributor(s): Eric Debreuve (since 2021)
#
# eric.debreuve@cnrs.fr
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

import logging as lggg
import platform as pltf
import sys as sstm
import time
from pathlib import Path as path_t
from typing import Any, Callable, ClassVar, Dict, Union

from rich.color import Color as color_t
from rich.console import Console as console_t
from rich.style import Style as style_t
from rich.text import Text as text_t


# This module is certainly imported early. Therefore, the current time should be close enough to the real start time.
_START_TIME = time.time()


_MESSAGE_FORMAT = (
    "%(asctime)s[%(levelname)s]\t- "
    "%(message)s @ "
    "%(module)s:%(funcName)s:%(lineno)d"
)
_DATE_FORMAT = "%Y-%m-%d@%H:%M:%S"

_SYSTEM_DETAILS = (
    "architecture",
    "machine",
    "node",
    "platform",
    "processor",
    "python_branch",
    "python_build",
    "python_compiler",
    "python_implementation",
    "python_revision",
    "python_version",
    "release",
    "system",
    "version",
)
_SYSTEM_DETAILS = {_dtl.capitalize(): getattr(pltf, _dtl)() for _dtl in _SYSTEM_DETAILS}
_MAX_DETAIL_NAME_LENGTH = max(map(len, _SYSTEM_DETAILS.keys()))


class color_handler_t(lggg.Handler):
    _LEVEL_COLOR: ClassVar[Dict[int, Union[str, style_t]]] = {
        lggg.DEBUG: "orchid",
        lggg.INFO: "white",
        lggg.WARNING: "yellow",
        lggg.ERROR: "orange3",
        lggg.CRITICAL: "red",
    }
    _GRAY_STYLE: ClassVar[style_t] = style_t(color=color_t.from_rgb(150, 150, 150))
    _ACTUAL: ClassVar[str] = r" Actual=[^.]+\."
    _EXPECTED: ClassVar[str] = r" Expected([!<>]=|: )[^.]+\."

    formatter: lggg.Formatter = None
    console: console_t = None

    def __init__(self, /, *, level=lggg.NOTSET) -> None:
        """"""
        super().__init__(level=level)

        self.formatter = lggg.Formatter(fmt=_MESSAGE_FORMAT, datefmt=_DATE_FORMAT)
        self.console = console_t(
            record=True, force_terminal=True, width=1000, tab_size=5
        )

        self.setFormatter(self.formatter)

    def emit(self, record: lggg.LogRecord, /) -> None:
        """"""
        cls = self.__class__

        formatted = self.formatter.format(record)
        highlighted = text_t(formatted)
        highlighted.append(f" +{_ElapsedTime()}", style="green")

        highlighted.stylize("dodger_blue2", end=19)
        highlighted.highlight_words(
            (f"[{record.levelname}]",), style=cls._LEVEL_COLOR[record.levelno]
        )
        highlighted.highlight_regex(
            f"@ {record.module}:{record.funcName}:{record.lineno}",
            style=cls._GRAY_STYLE,
        )
        highlighted.highlight_regex(cls._ACTUAL, style="red")
        highlighted.highlight_regex(cls._EXPECTED, style="green")

        self.console.print(highlighted)


LOGGER = lggg.getLogger(name="color_w_rich")
LOGGER.setLevel(lggg.INFO)  # Minimum desired level
LOGGER.addHandler(color_handler_t())


def AddFileHandler(file: Union[str, path_t], /) -> None:
    """"""
    if file.exists():
        raise ValueError(f"{file}: File already exists")

    handler = lggg.FileHandler(file)
    formatter = lggg.Formatter(fmt=_MESSAGE_FORMAT, datefmt=_DATE_FORMAT)
    handler.setFormatter(formatter)
    LOGGER.addHandler(handler)


def SaveLOGasHTML(file: Union[str, path_t], /) -> None:
    """"""
    if file.exists():
        raise ValueError(f"{file}: File already exists")

    console = getattr(LOGGER.handlers[0], "console", None)
    if (console is None) or not isinstance(console, console_t):
        raise ValueError(
            "Cannot save logging record as HTML: Handler has no RICH console"
        )

    with open(file, "w") as accessor:
        accessor.write(console.export_html())


def WhereFunction(function: Any, /) -> str:
    """"""
    return f"{function.__module__}:{function.__name__}"


def WhereMethod(obj: Any, method: Callable, /) -> str:
    """
    method: Could be a str instead, which would require changing method.__name__ into getattr(cls, method). But if the
        method name changes while forgetting to change the string in the call to WhereMethod accordingly, then an
        exception would be raised here.
    """
    cls = obj.__class__

    return f"{cls.__module__}:{cls.__name__}:{method.__name__}"


def LogSystemDetails() -> None:
    """"""
    details = "\n".join(
        f"    {_key:>{_MAX_DETAIL_NAME_LENGTH}}: {_vle}"
        for _key, _vle in _SYSTEM_DETAILS.items()
    )

    modules = sstm.modules
    with_versions = []
    for name in modules.keys():
        if name.startswith("_") or ("." in name):
            continue

        module = modules[name]
        version = getattr(module, "__version__", None)
        if version is not None:
            with_versions.append(f"{name}={version}")
    modules = ", ".join(with_versions)

    LOGGER.info(
        f"SYSTEM DETAILS\n"
        f"{details}\n"
        f"    {'Python Modules':>{_MAX_DETAIL_NAME_LENGTH}}:\n"
        f"    {modules}"
    )


def PrintElapsedTime() -> None:
    """"""
    print(f">>> ELAPSED TIME: {_ElapsedTime()} >>>")


def _ElapsedTime() -> str:
    """"""
    output = time.strftime("%Hh %Mm %Ss", time.gmtime(time.time() - _START_TIME))
    while output.startswith("00") and (" " in output):
        output = output.split(maxsplit=1)[-1]

    return output
