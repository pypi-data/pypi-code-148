import json
import click
from datetime import datetime

from la_panic.panic_parser.backtrace import Backtrace
from la_panic.panic_parser.core_state import CrashedCoreState, CoreState, CoreInfo
from la_panic.data_structure.raw_crash_stack import RawCrashStack
from la_panic.panic_parser.kext import LoadedKextInfo
from la_panic.panic_parser.sliders import KernelSliders
from la_panic.panic_parser.versions import KernelPanicVersions, KernelVersion, MetadataIOSVersion
from la_panic.panic_parser.zone import ZoneInfo
from la_panic.utilities.apple_date_time import AppleDateTime
from la_panic.utilities.device_types import iPhoneModels
from la_panic.utilities.device_types import iPhoneModel


class KernelPanicMetadata(object):
    __raw_json: object
    __bug_type: str
    __timestamp: datetime
    __os_version: MetadataIOSVersion

    def __init__(self, metadata: {str: object}):
        self.__bug_type = metadata["bug_type"]
        self.__timestamp = AppleDateTime.datetime(metadata["timestamp"])
        self.__os_version = MetadataIOSVersion(metadata['os_version'])

        self.__raw_json = metadata

    @property
    def bug_type(self):
        return self.__bug_type

    @property
    def os_version(self):
        return self.__os_version


class KernelPanicAdditionInfo(object):
    __panicked_task: str
    __roots_installed: int
    __panic_log_version: str
    __general_info: str
    # beta/official
    __release_type: str
    __versions: KernelPanicVersions
    __secure_boot: bool
    __backtrace: Backtrace
    __sliders: KernelSliders
    __cores_count = 0
    __cores_state: [CoreState] = []

    def __init__(self, panic_info_string: str):
        panic_infos = RawCrashStack(panic_info_string)

        self.__general_info = panic_infos.pop_one()
        crashed_core_state = CrashedCoreState(panic_infos.pop(9))

        # Remove Debugger message and Memory ID
        panic_infos.pop(2)

        self.__release_type = panic_infos.pop_value_from_key_value_pair()
        self.__versions = KernelPanicVersions(panic_infos)
        self.__secure_boot = True if panic_infos.pop_value_from_key_value_pair() == 'YES' else False
        self.__roots_installed = int(panic_infos.pop_value_from_key_value_pair())
        self.__panic_log_version = panic_infos.pop_value_from_key_value_pair()
        self.__sliders = KernelSliders(panic_infos)

        # Remove epoch time info
        panic_infos.pop(6)

        self.__zone_info = ZoneInfo(panic_infos)
        self.__cores_state = KernelPanicAdditionInfo.parse_cores_state(panic_infos, crashed_core_state)
        self.__compressor_info = panic_infos.pop_one()
        self.__panicked_task = panic_infos.pop_one()
        self.__panicked_thread = panic_infos.pop_one()
        self.__backtrace = Backtrace(panic_infos)
        self.__kext_info = LoadedKextInfo(panic_infos)

    @staticmethod
    def parse_cores_state(panic_infos: RawCrashStack, crashed_core_state: CrashedCoreState):
        cores_retired_instruction_data = []
        cores_count = 0
        cores_state = []

        finished_counting_cpu_cores = False
        while not finished_counting_cpu_cores:
            potential_retired_instruction_data = panic_infos.pop_one()
            if potential_retired_instruction_data.find("TPIDRx_ELy") != -1:
                break

            cores_retired_instruction_data.append(potential_retired_instruction_data)
            cores_count += 1

        for core_index in range(cores_count):
            core_state_str = panic_infos.pop_one()
            core_state = CoreInfo(core_index, cores_retired_instruction_data[core_index], core_state_str)
            cores_state.append(core_state)

            if core_state.crashed:
                core_state.update_crashed_state(crashed_core_state)

        return cores_state

    @property
    def crashed_core(self) -> CoreInfo:
        return list(filter(lambda core_state: core_state.crashed, self.__cores_state))[0]

    @property
    def backtrace(self) -> Backtrace:
        return self.__backtrace

    @property
    def sliders(self) -> KernelSliders:
        return self.__sliders
    
    @property
    def versions(self) -> KernelPanicVersions:
        return self.__versions

    @property
    def kext_info(self):
        return self.__kext_info


class ExtendedKernelPanic(object):
    __raw_json: object
    __additional_info: KernelPanicAdditionInfo
    __panic_flags: str
    __timestamp: datetime
    __incident_id: str
    __kernel: KernelVersion
    __model: iPhoneModel
    __os_version: MetadataIOSVersion

    def __init__(self, data: str):
        raw_json = json.loads(data)

        self.__os_version = MetadataIOSVersion(raw_json['build'])
        self.__model = iPhoneModels().get_model(raw_json['product'])
        self.__kernel = KernelVersion(raw_json['kernel'])
        self.__incident_id = raw_json['incident']
        self.__timestamp = AppleDateTime.datetime(raw_json['date'])
        self.__panic_flags = raw_json['panicFlags']
        self.__additional_info = KernelPanicAdditionInfo(raw_json['panicString'])

        self.__raw_json = raw_json

    @property
    def json(self) -> str:
        return f"\"timestamp\": \"{self.__timestamp}\",\n\
    \"os_version\": \"{self.__os_version.version}\",\n\
    \"model\" : \"{self.model.name}\",\n\
    \"xnu\": \"{self.kernel.xnu}\",\n\
    \"sliders\": {self.sliders},\n\
    \"backtrace\": {self.backtrace},\n\
    \"crashed_core\": {self.crashed_core},\n\
    \"kext\": {self.kext_info}"""

    @property
    def kernel(self) -> KernelVersion:
        return self.__kernel

    @property
    def model(self) -> iPhoneModel:
        return self.__model

    @property
    def crashed_core(self) -> CoreInfo:
        return self.__additional_info.crashed_core

    @property
    def backtrace(self) -> Backtrace:
        return self.__additional_info.backtrace

    @property
    def sliders(self) -> KernelSliders:
        return self.__additional_info.sliders
    
    @property
    def versions(self) -> KernelPanicVersions:
        return self.__additional_info.versions

    @property
    def kext_info(self) -> LoadedKextInfo:
        return self.__additional_info.kext_info

    @property
    def incident_id(self) -> str:
        return self.__incident_id

    @property
    def timestamp(self) -> datetime:
        return self.__timestamp


class KernelPanic(object):
    __metadata: KernelPanicMetadata
    __panic: ExtendedKernelPanic
    __filename: str

    def __init__(self, metadata: {str: object}, panic_data: str, filename: str):
        self.__filename = filename
        self.__metadata = KernelPanicMetadata(metadata)
        self.__panic = ExtendedKernelPanic(panic_data)

    @property
    def timestamp(self):
        return self.__panic.timestamp

    @property
    def incident_id(self):
        return self.__panic.incident_id

    @property
    def bug_type(self):
        return self.__metadata.bug_type

    @property
    def xnu(self) -> str:
        return self.__panic.kernel.xnu

    @property
    def model(self) -> iPhoneModel:
        return self.__panic.model

    @property
    def crashed_core(self) -> CoreInfo:
        return self.__panic.crashed_core

    @property
    def backtrace(self) -> Backtrace:
        return self.__panic.backtrace

    @property
    def sliders(self) -> KernelSliders:
        return self.__panic.sliders
    
    @property
    def os_version(self) -> str:
        return self.__metadata.os_version.version

    @property
    def iboot_version(self) -> str:
        return self.__panic.versions.iboot

    @property
    def kext_info(self) -> [LoadedKextInfo]:
        return self.__panic.kext_info

    def json(self):
        return f"{{\n\
    \"bug_type\": {self.bug_type},\n\
    {self.__panic.json}\n\
    }}"

    def __repr__(self):
        description = ''
        description += click.style(f'{self.incident_id} {self.timestamp}\n{self.__filename}\n\n', fg='cyan')

        description += click.style(f'Exception: Panic\n', bold=True)
        description += "\n"
        description += click.style('Metadata:\n', bold=True)
        description += click.style(f'\tBug Type: {self.bug_type}\n')
        description += click.style(f'\tTimestamp: {self.timestamp}\n')
        description += click.style(f"\tiPhone Model: {self.model}\n")
        description += click.style(f"\tXNU Version: {self.xnu}\n")
        description += "\n\n"
        description += click.style(f"Crashed Core Registers:", bold=True)
        description += click.style(f"{self.crashed_core}")
        description += "\n\n"
        description += click.style(f"Backtrace:\n", bold=True)
        description += click.style(f"{self.backtrace}")
        description += "\n\n"
        description += click.style(f"Sliders:\n", bold=True)
        description += click.style(f"{self.sliders}")
        description += "\n\n"
        description += click.style(f"Loaded kexts:\n", bold=True)
        description += click.style(f"{self.kext_info}")

        return description

    def __str__(self):
        return self.__repr__()
    
    
