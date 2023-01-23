from functools import cached_property
from typing import Optional

from la_panic.utilities.design_pattern.iteretable_with_last_object_signal import signal_last


class CrashedCoreState(object):
    def __init__(self, core_state_info: [str]):
        for line in core_state_info:
            register_line = line.split(':')
            register_name = register_line[0].strip()
            for part in register_line[1:]:
                address_value_and_next_register_name = list(filter(None, part.split(" ")))
                address = hex(int(address_value_and_next_register_name[0], 16))
                self.__setattr__(register_name, address)

                if len(address_value_and_next_register_name) != 1:
                    register_name = address_value_and_next_register_name[1]


class CoreState(object):
    pc: hex
    lr: hex
    fp: hex
    __crashed: bool = False

    def __init__(self, core_state: str):
        if core_state.find("panicked") != -1:
            self.__crashed = True
            return

        self.pc = hex(int(core_state.split("PC=")[1].split(",")[0], 16))
        self.lr = hex(int(core_state.split("LR=")[1].split(",")[0], 16))
        self.fp = hex(int(core_state.split("FP=")[1].split(",")[0], 16))

    @property
    def crashed(self) -> bool:
        return self.__crashed


class CoreInfo(object):
    __index: int
    __retired_instruction: hex
    __crashed: bool
    __core_state: CoreState

    def __init__(self, core_index: int, core_retired_instruction_data: Optional[str], core_state: str):
        if core_retired_instruction_data:
            self.__retired_instruction = "0x".join(core_retired_instruction_data.split('0x')[1])

        self.__index = core_index
        self.__core_state = CoreState(core_state)

    @property
    def index(self) -> int:
        return self.__index

    @property
    def crashed(self) -> bool:
        return self.__core_state.crashed

    @property
    def state(self) -> CoreState:
        return self.__core_state

    def update_crashed_state(self, crashed_core_state: CrashedCoreState):
        for register_name, register_value in vars(crashed_core_state).items():
            self.__core_state.__setattr__(register_name, register_value)

    @cached_property
    def __registers(self) -> {str: hex}:
        registers: {str: hex} = {}

        for register_name, register_value in vars(self.__core_state).items():
            if "crashed" in register_name:
                continue
            registers[register_name] = register_value

        return registers

    def json(self):
        description = f"""{{\n\t"core_index": {self.__index},"""

        for last_object, register_name in signal_last(vars(self.__core_state)):
            if "crashed" in register_name:
                continue

            register_value = getattr(self.__core_state, register_name)
            new_line = f"\t\"{register_name}\": \"{register_value}\""
            if not last_object:
                new_line += ","
            description = "\n".join((description, new_line))

        description = "\n".join((description, "    }"))

        return description

    def __repr__(self):
        description = ""

        counter = 0
        for register_name, register_value in self.__registers.items():
            if counter % 4 == 0:
                description += "\n"
            counter += 1

            description += f'{register_name} = 0x{int(register_value, 16):016x} '.rjust(30)

        return description

    def __str__(self):
        return self.__repr__()
