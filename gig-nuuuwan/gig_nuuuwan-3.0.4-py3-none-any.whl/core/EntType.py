import os
from dataclasses import dataclass
from functools import cached_property

from utils import SECONDS_IN, WWW, cache

from gig.core._common import URL_BASE


@dataclass
class EntType:
    name: str

    @staticmethod
    def from_id(id: str):
        n = len(id)
        if id[:2] == 'LK':
            if n == 2:
                return EntType.COUNTRY
            if n == 4:
                return EntType.PROVINCE
            if n == 5:
                return EntType.DISTRICT
            if n == 7:
                return EntType.DSD
            if n == 10:
                return EntType.GND

        if id[:2] == 'EC':
            if n == 5:
                return EntType.ED
            if n == 6:
                return EntType.PD

        if id[:2] == 'PS':
            return EntType.PS

        if id[:2] == 'LG':
            return EntType.LG

        if id[:3] == 'MOH':
            return EntType.MOH

        return EntType.UNKNOWN

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
        @cache('EntType.' + self.name, SECONDS_IN.WEEK)
        def inner():
            d_list = WWW(self.url_remote_data_path).readTSV()
            non_null_d_list = [d for d in d_list if d]
            return non_null_d_list

        return inner()


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
