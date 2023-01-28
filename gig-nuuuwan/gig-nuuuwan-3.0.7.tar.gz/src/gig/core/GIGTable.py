import os
from dataclasses import dataclass
from functools import cached_property

from utils import WWW, FiledVariable

from gig.core._common import URL_BASE
from gig.core.GIGTableRow import GIGTableRow

ID_FIELD = 'entity_id'


@dataclass
class GIGTable:
    measurement: str
    ent_type_group: str
    time_group: str

    @property
    def table_id(self):
        return '.'.join(
            [
                self.measurement,
                self.ent_type_group,
                self.time_group,
            ]
        )

    @property
    def url_remote_data_path(self):
        return os.path.join(
            URL_BASE,
            f'gig2/{self.table_id}.tsv',
        )

    @cached_property
    def remote_data_list(self) -> list:
        def inner():
            d_list = WWW(self.url_remote_data_path).readTSV()
            non_null_d_list = [d for d in d_list if d]
            return non_null_d_list

        var = FiledVariable(self.table_id + '.remote_data_list', inner)
        return var.value

    @cached_property
    def remote_data_idx(self) -> dict:
        return {d[ID_FIELD]: d for d in self.remote_data_list}

    def get(self, id):
        return GIGTableRow(self.remote_data_idx[id])
