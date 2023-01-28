import os
from dataclasses import dataclass
from functools import cached_property

from utils import WWW, FiledVariable

from gig.core._common import URL_BASE


@dataclass
class EntType:
    name: str

    @staticmethod
    def from_id(id: str):
        if id == 'LK':
            return EntType.COUNTRY

        prefix = id.partition('-')[0]
        n = len(id)

        return EntType.ID_TYPE_CONFIG.get(prefix, {}).get(n, EntType.UNKNOWN)

    @staticmethod
    def list():
        return [
            EntType.COUNTRY,
            EntType.PROVINCE,
            EntType.DISTRICT,
            EntType.DSD,
            EntType.GND,
            EntType.ED,
            EntType.PD,
            EntType.LG,
            EntType.MOH,
        ]

    @property
    def url_remote_data_path(self):
        return os.path.join(
            URL_BASE,
            f'ents/{self.name}.tsv',
        )

    @cached_property
    def remote_data_list(self) -> list:
        def inner():
            d_list = WWW(self.url_remote_data_path).readTSV()
            non_null_d_list = [d for d in d_list if d]
            return non_null_d_list

        return FiledVariable(self.name + '.remote_data_list', inner).value


EntType.COUNTRY = EntType('country')
EntType.PROVINCE = EntType('province')
EntType.DISTRICT = EntType('district')
EntType.DSD = EntType('dsd')
EntType.GND = EntType('gnd')
EntType.ED = EntType('ed')
EntType.PD = EntType('pd')
EntType.LG = EntType('lg')
EntType.MOH = EntType('moh')
EntType.UNKNOWN = EntType('unknown')

EntType.ID_TYPE_CONFIG = {
    'LK': {
        2: EntType.COUNTRY,
        4: EntType.PROVINCE,
        5: EntType.DISTRICT,
        7: EntType.DSD,
        10: EntType.GND,
    },
    'EC': {
        5: EntType.ED,
        6: EntType.PD,
    },
    'LG': {
        8: EntType.LG,
    },
    'MOH': {
        9: EntType.MOH,
    },
}
