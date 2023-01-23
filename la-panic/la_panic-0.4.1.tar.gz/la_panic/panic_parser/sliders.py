import click

from la_panic.data_structure.raw_crash_stack import RawCrashStack


class KernelSliders(object):
    __kernel_text_exec_base: hex
    __kernel_text_exec_slide: hex
    __kernel_text_base: hex
    __kernel_slide: hex
    __kernel_cache_base: hex
    __kernel_cache_slide: hex

    def __init__(self, panic_infos: RawCrashStack):
        self.__kernel_cache_slide = panic_infos.pop_hex_value_from_key_value_pair()
        self.__kernel_cache_base = panic_infos.pop_hex_value_from_key_value_pair()
        self.__kernel_slide = panic_infos.pop_hex_value_from_key_value_pair()
        self.__kernel_text_base = panic_infos.pop_hex_value_from_key_value_pair()
        self.__kernel_text_exec_slide = panic_infos.pop_hex_value_from_key_value_pair()
        self.__kernel_text_exec_base = panic_infos.pop_hex_value_from_key_value_pair()

    def json(self):
        return f"""{{
        "kernel_slide": \"{self.__kernel_slide}\",
        "kernel_cache_base": \"{self.__kernel_cache_base}\",
        "kernel_cache_slide": \"{self.__kernel_cache_slide}\",
        "kernel_text_base": \"{self.__kernel_text_base}\",
        "kernel_text_exec_base": \"{self.__kernel_text_exec_base}\",
        "kernel_text_exec_slide": \"{self.__kernel_text_exec_slide}\"
    }}"""

    def __repr__(self):
        description = ""

        description += click.style(f"\tKernel Slide = 0x{int(self.__kernel_slide, 16):016x}\n")
        description += click.style(f"\tKernel Text Base = 0x{int(self.__kernel_text_base, 16):016x}\n")
        description += click.style(f"\tKernel Text Exec Base: 0x{int(self.__kernel_text_exec_base, 16):016x}\n")
        description += click.style(f"\tKernel Text Exec Slide: 0x{int(self.__kernel_text_exec_slide, 16):016x}\n")
        description += click.style(f"\tKernel Cache Base: 0x{int(self.__kernel_cache_base, 16):016x}\n")
        description += click.style(f"\tKernel Cache Slide: 0x{int(self.__kernel_cache_slide, 16):016x}\n")

        return description

    def __str__(self):
        return self.__repr__()
