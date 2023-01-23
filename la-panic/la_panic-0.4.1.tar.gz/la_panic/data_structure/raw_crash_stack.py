
class EmptyRawCrashStack(Exception):
    pass


class RawCrashStack(object):
    __index = 0
    __crash_stack: [str]

    def __init__(self, panic_info_string: str):
        self.__crash_stack = list(filter(None, panic_info_string.strip().split("\n")))

    def pop(self, numer_of_pops: int = 1) -> [str]:
        if len(self.__crash_stack) == self.__index:
            raise EmptyRawCrashStack

        values = []
        for _ in range(numer_of_pops):
            current_index_value = self.__crash_stack[self.__index]
            self.__index += 1
            values.append(current_index_value)

        return values

    def pop_one(self) -> str:
        return self.pop()[0]

    def pop_value_from_key_value_pair(self) -> str:
        return self.pop_one().split(':')[1].strip()

    def pop_hex_value_from_key_value_pair(self) -> hex:
        return hex(int(self.pop_one().split(':')[1], 16))

    def pop_until_line_containing(self, substring: str):
        if len(self.__crash_stack) == self.__index:
            raise EmptyRawCrashStack

        lines_until_substring = []
        while substring not in self.__crash_stack[self.__index]:
            lines_until_substring.append(self.__crash_stack[self.__index])
            self.__index += 1

        return lines_until_substring
