from la_panic.data_structure.raw_crash_stack import RawCrashStack
from la_panic.panic_parser.backtrace import Backtrace
from la_panic.panic_parser.kext import LoadedKextInfo
from la_panic.panic_parser.panic_specific.kernel_force_reset_panic import KernelForceResetAdditionalInfo
from la_panic.panic_parser.panic_specific.kernel_specific_base import KernelSpecificBase, KernelSpecificPanic


class KernelFullPanicAdditionalInfo(KernelSpecificBase, KernelSpecificPanic):
    __kext_info: LoadedKextInfo
    __backtrace: Backtrace

    def __init__(self, data: str):
        panic_infos = RawCrashStack(data)

        super().__init__(panic_infos, KernelFullPanicAdditionalInfo.contains_crashed_core_info())
        self.__backtrace = Backtrace(panic_infos, "last started kext")
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

    # __panicked_task: str
    # __roots_installed: int
    # __panic_log_version: str
    # __general_info: str
    # # beta/official
    # __release_type: str
    # __versions: KernelPanicVersions
    # __secure_boot: bool
    # __backtrace: Backtrace
    # __sliders: KernelSliders
    # __cores_count = 0
    # __cores_state: [CoreState] = []
    #
    # def __init__(self, panic_info_string: str):
    #     panic_infos = RawCrashStack(panic_info_string)
    #
    #     self.__general_info = panic_infos.pop_one()
    #     crashed_core_state = CrashedCoreState(panic_infos.pop(9))
    #
    #     # Remove Debugger message and Memory ID
    #     panic_infos.pop(2)
    #
    #     self.__release_type = panic_infos.pop_value_from_key_value_pair()
    #     self.__versions = KernelPanicVersions(panic_infos)
    #     self.__secure_boot = True if panic_infos.pop_value_from_key_value_pair() == 'YES' else False
    #     self.__roots_installed = int(panic_infos.pop_value_from_key_value_pair())
    #     self.__panic_log_version = panic_infos.pop_value_from_key_value_pair()
    #     self.__sliders = KernelSliders(panic_infos)
    #
    #     # Remove epoch time info
    #     panic_infos.pop(6)
    #
    #     self.__zone_info = ZoneInfo(panic_infos)
    #     self.__cores_state = KernelFullPanicAdditionalInfo.parse_cores_state(panic_infos, crashed_core_state)
    #     self.__compressor_info = panic_infos.pop_one()
    #     self.__panicked_task = panic_infos.pop_one()
    #     self.__panicked_thread = panic_infos.pop_one()
    #     self.__backtrace = Backtrace(panic_infos)
    #     self.__kext_info = LoadedKextInfo(panic_infos)
    #
    # @staticmethod
    # def parse_cores_state(panic_infos: RawCrashStack, crashed_core_state: CrashedCoreState):
    #     cores_retired_instruction_data = []
    #     cores_count = 0
    #     cores_state = []
    #
    #     finished_counting_cpu_cores = False
    #     while not finished_counting_cpu_cores:
    #         potential_retired_instruction_data = panic_infos.pop_one()
    #         if potential_retired_instruction_data.find("TPIDRx_ELy") != -1:
    #             break
    #
    #         cores_retired_instruction_data.append(potential_retired_instruction_data)
    #         cores_count += 1
    #
    #     for core_index in range(cores_count):
    #         core_state_str = panic_infos.pop_one()
    #         core_state = CoreInfo(core_index, cores_retired_instruction_data[core_index], core_state_str)
    #         cores_state.append(core_state)
    #
    #         if core_state.crashed:
    #             core_state.update_crashed_state(crashed_core_state)
    #
    #     return cores_state
    #
    # @property
    # def crashed_core(self) -> CoreInfo:
    #     return list(filter(lambda core_state: core_state.crashed, self.__cores_state))[0]
    #
    # @property
    # def backtrace(self) -> Backtrace:
    #     return self.__backtrace
    #
    # @property
    # def sliders(self) -> KernelSliders:
    #     return self.__sliders
    #
    # @property
    # def versions(self) -> KernelPanicVersions:
    #     return self.__versions
    #
    # @property
    # def kext_info(self):
    #     return self.__kext_info
