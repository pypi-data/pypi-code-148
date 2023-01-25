from la_panic.data_structure.raw_crash_stack import RawCrashStack
from la_panic.panic_parser.backtrace import Backtrace
from la_panic.panic_parser.kext import LoadedKextInfo
from la_panic.panic_parser.panic_specific.kernel_specific_base import KernelSpecificBase, KernelSpecificPanic


class KernelFullPanicAdditionalInfo(KernelSpecificBase, KernelSpecificPanic):
    __kext_info: LoadedKextInfo
    __backtrace: Backtrace

    def __init__(self, data: str):
        panic_infos = RawCrashStack(data)

        super().__init__(panic_infos, KernelFullPanicAdditionalInfo.contains_crashed_core_info())
        self.__backtrace = Backtrace(panic_infos, "last started kext", self.sliders.kernel_cache_slide)
        self.__kext_info = LoadedKextInfo(panic_infos)

    @property
    def backtrace(self) -> Backtrace:
        return self.__backtrace

    @property
    def kext_info(self) -> LoadedKextInfo:
        return self.__kext_info

    @staticmethod
    def contains_crashed_core_info() -> bool:
        return True
