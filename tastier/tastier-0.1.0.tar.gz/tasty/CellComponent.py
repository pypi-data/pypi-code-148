from .util.string import INTRA_CELL_SEPARATOR, decode


class CellComponent:
    def _serialize(self, *values):
        return INTRA_CELL_SEPARATOR.join(values)

    @classmethod
    def parse(cls, cell: str):
        if cell == '':
            return tuple()

        cell_components = cell.split(INTRA_CELL_SEPARATOR)
        assert (n_cell_components := len(cell_components)) % (n_fields := len(cls.__dataclass_fields__)) == 0, \
            f'Number of cell components is not compatible with the number of parser fields for parser {cls}: {n_cell_components} % {n_fields} != 0'

        fields = cls.__dataclass_fields__
        field_keys = tuple(cls.__dataclass_fields__.keys())
        n_fields = len(field_keys)
        result = []

        i = 0
        params = []

        def append_field_value(value):
            field = fields[field_keys[i]]
            params.append(field.type(decode(value) if field.type == str else value))

        for cell_component in cell_components:
            if i < n_fields:
                append_field_value(cell_component)
                i += 1
            else:
                result.append(cls(**{key: value for key, value in zip(field_keys, params)}))
                i = 0
                params = []
                append_field_value(cell_component)
                i += 1

        if len(params) > 0:
            result.append(cls(*params))
            i = 0
            params = []

        return tuple(result)
