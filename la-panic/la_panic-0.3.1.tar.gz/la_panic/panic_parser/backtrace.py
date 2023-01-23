import click

from la_panic.data_structure.raw_crash_stack import RawCrashStack
from la_panic.utilities.design_pattern.iteretable_with_last_object_signal import signal_last


class CallStackLevel(object):
    __lr: hex
    __fp: hex

    def __init__(self, callstack_call: str):
        callstack_call_parts = callstack_call.split(":")
        self.__lr = hex(int(callstack_call_parts[1].strip().split(" ")[0], 16))
        self.__fp = hex(int(callstack_call_parts[2].strip(), 16))

    @property
    def lr(self) -> hex:
        return self.__lr

    @property
    def fp(self) -> hex:
        return self.__fp


class Backtrace(object):
    __callstack: [CallStackLevel] = []

    def __init__(self, panic_infos: RawCrashStack):
        callstack_calls = panic_infos.pop_until_line_containing("last started kext")
        for callstack_call in callstack_calls:
            call_stack_level = CallStackLevel(callstack_call)
            self.__callstack.append(call_stack_level)

    @property
    def callstack(self) -> [CallStackLevel]:
        return self.__callstack

    def __repr__(self):
        description = ""

        for call_stack_level in self.__callstack:
            description += click.style(f"\tLR = {call_stack_level.lr},  FP = {call_stack_level.fp}\n", fg='bright_white')

        return description

    def __str__(self):
        return self.__repr__()

    def json(self):
        description = "["

        for last_element, call_stack_level in signal_last(self.__callstack):
            new_line = f"\t  {{ \"LR\": \"{call_stack_level.lr}\", \"FP\": \"{call_stack_level.fp}\" }}"
            if not last_element:
                new_line += ","
            description = "\n".join((description, new_line))

        description = "\n".join((description, "    ]"))

        return description
