import json

from fuzzywuzzy import fuzz
from utils import SECONDS_IN, String, cache, hashx

from gig.core.EntType import EntType


class EntLoadMixin:
    @classmethod
    def from_dict(cls, d):
        d = d.copy()
        if 'area' in d:
            d['area'] = String(d['area']).float

        if 'population' in d:
            d['population'] = String(d['population']).int

        if 'centroid_altitude' in d:
            try:
                d['centroid_altitude'] = String(d['centroid_altitude']).float
            except ValueError:
                d['centroid_altitude'] = 0

        for k in ['centroid', 'subs', 'supers', 'ints', 'eqs']:
            if k in d:
                if d[k]:
                    d[k] = json.loads(d[k].replace('\'', '"'))
        return cls(d)

    @classmethod
    def for_id(cls, id: str):
        ent_type = EntType.from_id(id)
        ent_idx = cls.idx_from_type(ent_type)
        return ent_idx[id]

    @classmethod
    def list_from_type(cls, ent_type: EntType) -> list:
        d_list = ent_type.remote_data_list
        ent_list = [cls.from_dict(d) for d in d_list]
        return ent_list

    @classmethod
    def idx_from_type(cls, ent_type: EntType) -> dict:
        ent_list = cls.list_from_type(ent_type)
        ent_idx = {ent.id: ent for ent in ent_list}
        return ent_idx

    @classmethod
    def list_from_id_list(cls, id_list: list) -> list:
        ent_list = [cls.for_id(id) for id in id_list]
        return ent_list

    @classmethod
    def ids_from_type(cls, ent_type: EntType) -> list:
        ent_list = cls.list_from_type(ent_type)
        id_list = [ent.id for ent in ent_list]
        return id_list

    @classmethod
    def list_from_name_fuzzy(
        cls,
        name_fuzzy: str,
        filter_ent_type: EntType = None,
        filter_parent_id: str = None,
        limit: int = 5,
        min_fuzz_ratio: int = 80,
    ) -> list:

        cache_key = hashx.md5(
            '.'.join(
                [
                    name_fuzzy,
                    filter_ent_type.name if filter_ent_type else str(None),
                    str(filter_parent_id),
                    str(limit),
                    str(min_fuzz_ratio),
                ]
            )
        )

        @cache(cache_key, SECONDS_IN.WEEK)
        def inner():
            ent_and_ratio_list = []
            for entity_type in EntType.list():
                if filter_ent_type and (filter_ent_type != entity_type):
                    continue

                ent_list_from_type = cls.list_from_type(entity_type)
                for ent in ent_list_from_type:
                    if filter_parent_id and ent.is_parent_id(
                        filter_parent_id
                    ):
                        continue

                    fuzz_ratio = fuzz.ratio(ent.name, name_fuzzy)

                    if fuzz_ratio >= min_fuzz_ratio:
                        ent_and_ratio_list.append([ent, fuzz_ratio])

            ent_list = [
                item[0]
                for item in sorted(ent_and_ratio_list, key=lambda x: -x[1])
            ]

            if len(ent_list) >= limit:
                ent_list = ent_list[:limit]

            return [ent.to_json() for ent in ent_list]

        return [cls.from_json(x) for x in inner()]
