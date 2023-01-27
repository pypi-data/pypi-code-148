from os import linesep

from .CellComponent import CellComponent
from .util.string import INTRA_CELL_SEPARATOR, INTER_CELL_SEPARATOR
from .util.operator import pipe


class Corpus:
    def __init__(self, data: tuple[tuple[tuple]]):
        self.data = data

    def write(self, path: str, header: str):
        with open(path, 'w') as file:
            header | pipe | INTER_CELL_SEPARATOR.join | pipe | file.write
            # file.write(INTER_CELL_SEPARATOR.join(header))
            linesep | pipe | file.write
            # file.write(linesep)
            for sequence in self.data:
                for row in sequence:
                    file.write(
                        INTER_CELL_SEPARATOR.join(
                            INTRA_CELL_SEPARATOR.join(
                                cell_component.serialized
                                for cell_component in cell
                            )
                            for cell in row
                        )
                    )
                    file.write(linesep)
                file.write(linesep)

        return self

    @classmethod
    def read(cls, path: str, parsers = tuple[CellComponent], with_header: bool = True):
        passed_header = False
        entries = []
        sequence_entries = []
        with open(path, 'r') as file:
            for line in file.readlines():
                if line == linesep:
                    entries.append(tuple(sequence_entries))
                    sequence_entries = []
                    continue

                if with_header and not passed_header:
                    passed_header = True
                    continue

                cells = line[:-1].split(INTER_CELL_SEPARATOR)
                assert (n_cells := len(cells)) == (n_parsers := len(parsers)), f'Number of cells is not equal to the number of parsers: {n_cells} != {n_parsers}'

                sequence_entries.append(
                    tuple(
                        parser.parse(cell)
                        for cell, parser in zip(cells, parsers)
                    )
                )

        if len(sequence_entries) > 0:
            entries.append(tuple(sequence_entries))

        return cls(tuple(entries))
