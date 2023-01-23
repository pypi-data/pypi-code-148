from typing import List, Optional

from la_panic.data_structure.raw_crash_stack import RawCrashStack
from la_panic.panic_parser.backtrace import Backtrace
from la_panic.panic_parser.core_state import CoreInfo
from la_panic.panic_parser.kext import LoadedKextInfo, KextInBacktraceDependencies
from la_panic.panic_parser.panic_specific.kernel_specific_base import KernelSpecificBase, KernelSpecificPanic


class KernelForceResetAdditionalInfo(KernelSpecificBase, KernelSpecificPanic):
    __backtrace: Backtrace
    __kext_info: LoadedKextInfo

    @staticmethod
    def contains_crashed_core_info() -> bool:
        return False

    def __init__(self, data: str):
        panic_infos = RawCrashStack(data)

        super().__init__(panic_infos, KernelForceResetAdditionalInfo.contains_crashed_core_info())
        self.__backtrace = Backtrace(panic_infos, "Kernel Extensions in backtrace")

        # remove headline
        panic_infos.pop_one()

        kexts_in_backtrace_raw = panic_infos.pop_until_line_containing("last started kext")
        kexts_in_backtrace = KernelForceResetAdditionalInfo.kexts_in_backtrace(kexts_in_backtrace_raw)
        self.__kext_info = LoadedKextInfo(panic_infos)

        for kext in self.__kext_info.loaded_kexts:
            if kext.name in kexts_in_backtrace.backtraced:
                kext.backtrace_info = kexts_in_backtrace
                break

    @staticmethod
    def kexts_in_backtrace(kexts_in_backtrace_raw: List[str]) -> KextInBacktraceDependencies:
        kext_in_backtrace = kexts_in_backtrace_raw.pop(0)
        dependencies = []

        for kext_in_backtrace_raw in kexts_in_backtrace_raw:
            dependencies.append(kext_in_backtrace_raw.split(':')[1])

        return KextInBacktraceDependencies(backtraced=kext_in_backtrace, dependencies=dependencies)

    @property
    def backtrace(self) -> Backtrace:
        return self.__backtrace

    @property
    def kext_info(self) -> LoadedKextInfo:
        return self.__kext_info

    @property
    def crashed_core(self) -> Optional[CoreInfo]:
        return None
