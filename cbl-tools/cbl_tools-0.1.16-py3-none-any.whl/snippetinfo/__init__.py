# a.voss@fh-aachen.de

""" note-tools """

import logging
import pathlib
import sys
from dataclasses import dataclass
from typing import Self                 # from python 3.11
import threading


@dataclass
class CblFormatterUsageInfo(object):
    """Format information/flags."""
    is_timeinfo_used = True             # usually used
    is_timems_used = True               # standard
    is_threadinfo_used = False          # used in case of threading, switch on then


class CblFormatter(logging.Formatter):
    _short_loglevelname: dict[int, str] = {
        logging.CRITICAL: 'C',
        logging.ERROR: 'E',
        logging.WARNING: 'W',
        logging.INFO: 'I',
        logging.DEBUG: 'D',
        logging.NOTSET: 'N',
    }
    _readable_method_name: dict[str, str] = {
        "<module>": "main",
        "__init__": "ctor",
        "__del__": "dtor",
    }
    _thread_names = ["Main", "Anna", "Bill", "Caro", "Duke", "Ella", "Finn", "Gina", "Herb"]

    def __init__(self, usage_info: CblFormatterUsageInfo):
        self.usage_info = usage_info
        self.thread_mapping: dict[int:str] = { threading.main_thread().ident: CblFormatter._thread_names[0] }
        super(CblFormatter, self).__init__(
            fmt='{asctime}{threadname}{levelname} {funcName:25s} {message}',   # keep original names if possible
            datefmt='%I:%M:%S',
            style='{'
        )

    @staticmethod
    def formatHeader(fcn_name: str):
        return f"----- '{fcn_name}' -----"

    def formatTime(self, record, fmt=None):
        if not self.usage_info.is_timeinfo_used:
            return ""
        msec = f".{record.msecs:0<3.0f}" if self.usage_info.is_timems_used else ""
        return f"{super(CblFormatter, self).formatTime(record, fmt)}{msec} "    # assumes that fmt does not include ms

    def formatMessage(self, record):
        record.levelname = CblFormatter._short_loglevelname[record.levelno]

        if record.args is not None and CblNote.CALLFRAME_INFO_KEY in record.args:
            info: CblCallFrameInfo = record.args.pop(CblNote.CALLFRAME_INFO_KEY)
            fcn_name = CblFormatter._readable_method_name.get(info.fcn_name, info.fcn_name)
            if info.is_class:
                fcn_name = f"{info.class_name}{':' if info.is_class_method else '.'}{fcn_name}"
            record.funcName = f"'{fcn_name}' {info.lineno}"
        else:
            record.funcName = f"'{record.funcName}' {record.lineno}"

        if record.levelno != logging.ERROR:
            if len(record.message) > 0 and record.message[0].isspace():
                record.message = ("  " * (len(record.message)-len(lmsg := record.message.lstrip()))) + lmsg
        elif record.args is not None and CblNote.EXCEPTION_KEY in record.args:
            e = record.args.pop(CblNote.EXCEPTION_KEY)
            err_text = f" ({record.message})" if len(record.message) > 0 else ""
            record.message = f">>>>> {e} <<<<<{err_text}"

        if self.usage_info.is_threadinfo_used:
            idt = threading.current_thread().ident
            if idt in self.thread_mapping:
                s_thread = self.thread_mapping[idt]
            else:
                if (used := len(self.thread_mapping)) < len(CblFormatter._thread_names):
                    self.thread_mapping[idt] = CblFormatter._thread_names[used]
                    s_thread = self.thread_mapping[idt]
                else:
                    s_thread = f"{(idt % 10000):04d}"
            record.threadname = f"{s_thread} "
        else:
            record.threadname = ""

        return self._style.format(record)


class CblConsoleHandler(logging.StreamHandler):

    def __init__(self, formatter: logging.Formatter = None):
        super(CblConsoleHandler, self).__init__()
        if formatter is not None:
            self.setFormatter(formatter)

    def emit(self, record):
        try:
            if record.args is not None and CblNote.PRINTARGS_KEY in record.args:
                args = record.args.get(CblNote.PRINTARGS_KEY)
                print(self.format(record), end=args['end'])
            else:
                print(self.format(record))
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)


@dataclass
class CblCallFrameInfo(object):
    class_name: str = ""
    fcn_name: str = ""
    lineno: int = 0
    is_class: bool = False
    is_class_method: bool = False

    @staticmethod
    def from_frame(look_back: int) -> Self:
        frame1 = sys._getframe(1)
        while look_back > 0:
            frame1 = frame1.f_back
            look_back -= 1

        fcn_name = frame1.f_code.co_name
        lineno = frame1.f_lineno

        try:
            if 'self' in frame1.f_locals:  # this is just an educated guess...
                return CblCallFrameInfo(class_name=frame1.f_locals['self'].__class__.__name__, fcn_name=fcn_name,
                                        lineno=lineno, is_class=True)
            elif 'cls' in frame1.f_locals:
                return CblCallFrameInfo(class_name=frame1.f_locals['cls'].__name__, fcn_name=fcn_name,
                                        lineno=lineno, is_class=True, is_class_method=True)
            else:
                return CblCallFrameInfo(fcn_name=fcn_name, lineno=lineno)
        except KeyError:
            return CblCallFrameInfo(fcn_name=fcn_name, lineno=lineno)


class CblNote(object):
    CALLFRAME_INFO_KEY = "cbl_callframe_info"
    EXCEPTION_KEY = "cbl_exception"
    PRINTARGS_KEY = "cbl_printargs"

    """
    Wir nutzen, auch als Beispiel, einen Logger. Es wäre ebenso möglich gewesen, CblNote von Logger abzuleiten
    (von logging.getLoggerClass() ) und über logging.setLoggerClass sich dann einen Logger vom Typ CblNote 
    mit logging.getLogger("cbl_note") zu holen.
    """
    def __init__(self):
        self.usage_info = CblFormatterUsageInfo()
        self.logger = logging.getLogger("cbl_note")
        self.logger.setLevel(logging.DEBUG)
        self.logger.propagate = False
        self.logger.addHandler(CblConsoleHandler(formatter=CblFormatter(self.usage_info)))

    """
    Note that we need to extract callframe-info here due to the unknown call level in Logging.
    """
    @staticmethod
    def _collect_extras(add: dict):
        return {CblNote.CALLFRAME_INFO_KEY: CblCallFrameInfo.from_frame(2), **add}

    def detail(self, msg: str, end: str = '\n', *args, **kwargs):
        extra = CblNote._collect_extras({CblNote.PRINTARGS_KEY: {'end': end}})
        self.logger.debug(msg, extra, *args, **kwargs)

    def info(self, msg: str, end: str = '\n', *args, **kwargs):
        extra = CblNote._collect_extras({CblNote.PRINTARGS_KEY: {'end': end}})
        self.logger.info(msg, extra, *args, **kwargs)

    def error(self, msg: str, error: Exception = None, end: str = '\n', *args, **kwargs):
        extra = CblNote._collect_extras({CblNote.EXCEPTION_KEY: error, CblNote.PRINTARGS_KEY: {'end': end}})
        self.logger.error(msg, extra, *args, **kwargs)

    def show_details(self):
        self.logger.setLevel(logging.DEBUG)

    def hide_details(self):
        self.logger.setLevel(logging.INFO)

    def show_timeinfo(self):
        self.usage_info.is_timeinfo_used = True

    def hide_timeinfo(self):
        self.usage_info.is_timeinfo_used = False

    def show_threadinfo(self):
        self.usage_info.is_threadinfo_used = True

    def hide_threadinfo(self):
        self.usage_info.is_threadinfo_used = False


def with_intro(f):
    def wrap_up_f():
        header = f"{CblFormatter.formatHeader(f.__name__)}"
        print(f"{header}")
        f()
        print(f"{header}\n")
    return wrap_up_f


note = CblNote()


class CblIntro:
    def __init__(self):
        module_path = pathlib.Path(sys.modules['__main__'].__file__)
        name = module_path.stem
        if len(parts := module_path.parts) >= 2 and parts[-2].startswith("0x"):
            detail = f"Topic '{name[2:]}' ('{name}')" if len(name) >= 2 and name[1] == '_' else f"Snippet '{name}'"
            self.header = f"Unit {parts[-2]}, {detail}"
        else:
            self.header = f"'{name}'"

    def __enter__(self):
        print(f"===== {self.header} =====\n")

    def __exit__(self, typ, value, tb):
        print(f"===== {self.header} =====")


intro = CblIntro()

