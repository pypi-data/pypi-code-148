# Copyright CNRS/Inria/UCA
# Contributor(s): Eric Debreuve (since 2021)
#
# eric.debreuve@cnrs.fr
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

import numbers as nmbr
import tempfile as temp
from pathlib import Path as path_t
from typing import IO, Dict, Optional, Sequence, Tuple, Union

import xlsxwriter as xlsx
from xlsxwriter.format import Format as xlsx_format_t
from xlsxwriter.workbook import Workbook as workbook_t
from xlsxwriter.worksheet import Worksheet as worksheet_t

from cell_tracking_BC.in_out.text.logger import LOGGER
from cell_tracking_BC.standard.uid import AlphaColumnFromIndex
from cell_tracking_BC.type.analysis import analysis_t
from cell_tracking_BC.type.compartment.cell import cell_t, state_e
from cell_tracking_BC.in_out.file.sheet import (
    SheetNameFromLongName,
    SortAndWriteCSVLines,
)
from cell_tracking_BC.type.track.single.thread import thread_track_t
from cell_tracking_BC.type.track.multiple.structured import tracks_t
from cell_tracking_BC.type.compartment.base import compartment_t, compartment_id_t


division_times_h = Dict[int, Sequence[int]]
death_time_h = Dict[int, int]


INVALID_TRACK_MARKER = "Invalid"
PRUNED_TRACK_MARKER = "Pruned"
VALID_TRACK_MARKER = "Valid"

_DASH_TYPES = (
    "solid",
    "round_dot",
    "square_dot",
    "dash",
    "dash_dot",
    "long_dash",
    "long_dash_dot",
    "long_dash_dot_dot",
)
_N_DASH_TYPES = _DASH_TYPES.__len__()


def SaveCompartmentsFeaturesToXLSX(
    base_path: Union[str, path_t],
    analysis: analysis_t,
    /,
) -> None:
    """"""
    if isinstance(base_path, str):
        base_path = path_t(base_path)
    if base_path.is_dir():
        base_path /= "features.xlsx"

    for compartment_id in tuple(compartment_id_t):
        path = (
            base_path.parent
            / f"{base_path.stem}-{str.lower(compartment_id.name)}{base_path.suffix}"
        )

        if path.exists():
            print(f"{path}: File (or folder) already exists...")
            path = path_t(temp.mkdtemp()) / path.name
            print(f"Using {path} instead")

        workbook = xlsx.Workbook(str(path))
        pruned_format = workbook.add_format({"bg_color": "gray"})
        division_format = workbook.add_format({"bg_color": "blue"})
        death_format = workbook.add_format({"bg_color": "red"})

        csv_path = path.with_suffix(".csv")
        csv_accessor = open(csv_path, mode="w")

        tracks = analysis.tracks
        if (tracks is None) or (tracks.__len__() == 0):
            LOGGER.warning("Sequence with no valid tracks.")
        else:
            one_compartment = (
                analysis.segmentations[0].cells[0].compartments[compartment_id]
            )
            if not isinstance(one_compartment, compartment_t):
                one_compartment = one_compartment[0]
            for feature in one_compartment.available_features:
                _SaveFeature(
                    compartment_id,
                    feature,
                    tracks,
                    workbook,
                    csv_accessor,
                    pruned_format,
                    division_format,
                    death_format,
                )

        workbook.close()
        csv_accessor.close()


def _SaveFeature(
    compartment_id: compartment_id_t,
    feature: str,
    tracks: tracks_t,
    workbook: workbook_t,
    csv_accessor: IO,
    pruned_format: Optional[xlsx_format_t],
    division_format: Optional[xlsx_format_t],
    death_format: Optional[xlsx_format_t],
    /,
) -> None:
    """"""
    sheet_name = SheetNameFromLongName(feature)
    worksheet = workbook.add_worksheet(sheet_name)
    csv_accessor.write(f"--- Feature {feature}\n")

    per_row_limits = {}
    csv_lines = []
    for track in tracks.all_structured_iterator:
        root_time_point = track.topologic_root_time_point
        for path, label in track.LabeledThreadIterator(topologic_mode=True):
            row = label - 1

            if feature not in path[0].features:
                message = f'Feature "{feature}" missing'
                worksheet.write_string(row, 0, message)
                csv_lines.append(f"{label}, {message}")
                continue

            evolution = []
            for cell in path:
                compartment = cell.compartments[compartment_id]
                if isinstance(compartment, compartment_t):
                    evolution.append(compartment.features[feature])
                else:
                    evolution.append(
                        tuple(_cpt.features[feature] for _cpt in compartment)
                    )
            if not isinstance(evolution[0], nmbr.Number):
                message = f'Feature of type "{type(evolution[0]).__name__}" unhandled'
                worksheet.write_string(0, 0, message)
                csv_accessor.write(message + "\n")
                return

            if root_time_point > 0:
                worksheet.write_row(row, 0, root_time_point * ("x",))
            worksheet.write_row(row, root_time_point, evolution)
            csv_lines.append(
                f"{label}, " + root_time_point * "," + ", ".join(map(str, evolution))
            )

            _SetStateBasedCellFormat(
                worksheet,
                row,
                root_time_point,
                path,
                evolution,
                pruned_format,
                division_format,
                death_format,
            )

            per_row_limits[row + 1] = (
                root_time_point,
                root_time_point + evolution.__len__() - 1,
            )

    _WriteExtras(
        tracks,
        per_row_limits,
        workbook,
        sheet_name,
        worksheet,
        pruned_format,
        division_format,
        death_format,
    )
    SortAndWriteCSVLines(csv_lines, csv_accessor)


def SaveCellEventsToXLSX(
    path: Union[str, path_t],
    analysis: analysis_t,
    /,
    *,
    division_response: str = None,
    death_response: str = None,
) -> None:
    """"""
    if isinstance(path, str):
        path = path_t(path)
    if path.is_dir():
        path /= "cell_events.xlsx"

    if path.exists():
        print(f"{path}: File (or folder) already exists...")
        path = path_t(temp.mkdtemp()) / path.name
        print(f"Using {path} instead")

    workbook = xlsx.Workbook(str(path))
    pruned_format = workbook.add_format({"bg_color": "gray"})
    division_format = workbook.add_format({"bg_color": "blue"})
    death_format = workbook.add_format({"bg_color": "red"})

    csv_path = path.with_suffix(".csv")
    csv_accessor = open(csv_path, mode="w")

    tracks = analysis.tracks
    if (tracks is None) or (tracks.__len__() == 0):
        LOGGER.warning("Sequence with no valid tracks.")
    else:
        division_time_points = tracks.DivisionTimePoints()
        death_time_points = tracks.DeathTimePoints(
            analysis.sequence.length, with_living_leaves=True
        )
        for SaveEvents, time_point in zip(
            (_SaveDivisionEvents, _SaveDeathEvents),
            (division_time_points, death_time_points),
        ):
            SaveEvents(workbook, csv_accessor, time_point, tracks)

        n_divisions = sum(_tck.n_dividing_cells for _tck in tracks)
        _SaveEventCounts(workbook, csv_accessor, n_divisions, death_time_points)

        for event, response in zip(
            ("division", "death"), (division_response, death_response)
        ):
            if response is not None:
                _SaveEventResponse(
                    event,
                    workbook,
                    csv_accessor,
                    response,
                    tracks,
                    pruned_format,
                    division_format,
                    death_format,
                )

    workbook.close()
    csv_accessor.close()


def _SaveDivisionEvents(
    workbook: xlsx.Workbook,
    csv_accessor: IO,
    division_time_points: Optional[division_times_h],
    tracks: tracks_t,
    /,
) -> None:
    """"""
    if (division_time_points is None) or (division_time_points.__len__() == 0):
        LOGGER.warning("Division Events: No associated tracks.")
        return

    sheet_name = SheetNameFromLongName("division times")
    worksheet = workbook.add_worksheet(sheet_name)
    csv_accessor.write("--- Division Times\n")

    total_n_topologic_threads = tracks.total_n_topologic_threads
    for label in range(1, total_n_topologic_threads + 1):
        row = label - 1

        if label not in division_time_points:
            worksheet.write_string(
                row, 0, f"{INVALID_TRACK_MARKER} or {PRUNED_TRACK_MARKER}"
            )
            csv_accessor.write(
                f"{label}:, {INVALID_TRACK_MARKER} or {PRUNED_TRACK_MARKER}\n"
            )
            continue

        time_points = division_time_points[label]
        if (time_points is None) or (time_points.__len__() == 0):
            worksheet.write_string(row, 0, "No Divisions")
            csv_accessor.write(f"{label}:, No Divisions\n")
        else:
            worksheet.write_row(row, 0, time_points)
            csv_accessor.write(f"{label}:," + ", ".join(map(str, time_points)) + "\n")

    worksheet.write_string(total_n_topologic_threads, 0, "END")


def _SaveDeathEvents(
    workbook: xlsx.Workbook,
    csv_accessor: IO,
    death_time_points: Optional[death_time_h],
    tracks: tracks_t,
    /,
) -> None:
    """"""
    if (death_time_points is None) or (death_time_points.__len__() == 0):
        LOGGER.warning("Death Events: No associated tracks.")
        return

    sheet_name = SheetNameFromLongName("death time")
    worksheet = workbook.add_worksheet(sheet_name)
    csv_accessor.write("--- Death Times\n")

    total_n_topologic_threads = tracks.total_n_topologic_threads
    for label in range(1, total_n_topologic_threads + 1):
        row = label - 1

        if label not in death_time_points:
            worksheet.write_string(
                row, 0, f"{INVALID_TRACK_MARKER} or {PRUNED_TRACK_MARKER}"
            )
            csv_accessor.write(
                f"{label}:, {INVALID_TRACK_MARKER} or {PRUNED_TRACK_MARKER}\n"
            )
            continue

        time_point = death_time_points[label]
        if time_point is None:
            worksheet.write_string(row, 0, "No Death")
            csv_accessor.write(f"{label}:, No Death\n")
        else:
            worksheet.write_number(row, 0, time_point)
            csv_accessor.write(f"{label}:, {time_point}\n")

    worksheet.write_string(total_n_topologic_threads, 0, "END")


def _SaveEventCounts(
    workbook: xlsx.Workbook,
    csv_accessor: IO,
    n_divisions: int,
    death_time_points: Optional[death_time_h],
    /,
) -> None:
    """"""
    sheet_name = SheetNameFromLongName("event counts")
    worksheet = workbook.add_worksheet(sheet_name)
    csv_accessor.write("--- Event Counts\n")

    n_deaths_pattern = 0
    n_deaths_track = 0
    if death_time_points is not None:
        for time_point in death_time_points.values():
            if time_point is not None:
                if time_point >= 0:
                    n_deaths_pattern += 1
                else:
                    n_deaths_track += 1

    for r_idx, (title, value) in enumerate(
        zip(
            ("divisions", "death (pattern)", "death (topologic)", "death"),
            (
                n_divisions,
                n_deaths_pattern,
                n_deaths_track,
                n_deaths_pattern + n_deaths_track,
            ),
        )
    ):
        worksheet.write_string(r_idx, 0, title)
        worksheet.write_number(r_idx, 1, value)
        csv_accessor.write(f"{title}, {value}\n")


def _SaveEventResponse(
    event: str,
    workbook: xlsx.Workbook,
    csv_accessor: IO,
    name: str,
    tracks: tracks_t,
    pruned_format: xlsx_format_t,
    division_format: xlsx_format_t,
    death_format: xlsx_format_t,
    /,
) -> None:
    """"""
    sheet_name = SheetNameFromLongName(f"{event} response")
    worksheet = workbook.add_worksheet(sheet_name)
    csv_accessor.write(f"--- {event.title()} response\n")

    per_row_limits = {}
    csv_lines = []
    for track in tracks.all_structured_iterator:
        if name not in track.features:
            message = f'Track without "{name}" response'
            for label in track.topologic_labels:
                worksheet.write_string(label - 1, 0, message)
                csv_lines.append(f"{label}, {message}")
            continue

        root_time_point = track.topologic_root_time_point
        for label, response in track.features[name].items():
            row = label - 1
            if response is None:
                message = "Track too Short for Valid Response"
                worksheet.write_string(row, 0, message)
                csv_lines.append(f"{label}, {message}")
            else:
                worksheet.write_row(row, root_time_point, response)
                csv_lines.append(
                    f"{label}, " + root_time_point * "," + ", ".join(map(str, response))
                )

                if isinstance(track, thread_track_t):
                    cells = track
                else:
                    leaf_idx = track.topologic_labels.index(label)
                    leaf = track.topologic_leaves[leaf_idx]
                    cells = track.PathFromTo(track.topologic_root, leaf)
                _SetStateBasedCellFormat(
                    worksheet,
                    row,
                    root_time_point,
                    cells,
                    response,
                    pruned_format,
                    division_format,
                    death_format,
                )

                per_row_limits[label] = (
                    root_time_point,
                    root_time_point + response.__len__() - 1,
                )

    _WriteExtras(
        tracks,
        per_row_limits,
        workbook,
        sheet_name,
        worksheet,
        pruned_format,
        division_format,
        death_format,
    )
    SortAndWriteCSVLines(csv_lines, csv_accessor)


def _WriteExtras(
    tracks: tracks_t,
    per_row_limits: Dict[int, Tuple[int, int]],
    workbook: workbook_t,
    sheet_name: str,
    worksheet: worksheet_t,
    pruned_format: xlsx_format_t,
    division_format: xlsx_format_t,
    death_format: xlsx_format_t,
    /,
) -> None:
    """"""
    next_available_row = tracks.total_n_topologic_threads

    worksheet.write_string(next_available_row, 0, "END")
    next_available_row += 2  # With margin

    _AddCellStateLegend(
        worksheet, next_available_row, pruned_format, division_format, death_format
    )
    next_available_row += 3  # With margin

    if per_row_limits.__len__() > 0:
        chart = workbook.add_chart({"type": "line"})
        for l_idx, (row, (min_col, max_col)) in enumerate(per_row_limits.items()):
            min_col = AlphaColumnFromIndex(min_col)
            max_col = AlphaColumnFromIndex(max_col)
            chart.add_series(
                {
                    "name": str(row),
                    "values": f"='{sheet_name}'!${min_col}${row}:${max_col}${row}",
                    "line": {
                        "width": 1.0,
                        "dash_type": _DASH_TYPES[l_idx % _N_DASH_TYPES],
                    },
                }
            )
        worksheet.insert_chart(f"A{next_available_row}", chart)


def _SetStateBasedCellFormat(
    worksheet: worksheet_t,
    row: int,
    root_time_point: int,
    cells: Sequence[cell_t],
    values: Sequence,
    pruned_format: xlsx_format_t,
    division_format: xlsx_format_t,
    death_format: xlsx_format_t,
    /,
) -> None:
    """"""
    for time_point, cell in enumerate(cells, start=root_time_point):
        if cell.state is state_e.discarded:
            cell_format = pruned_format
        elif cell.state is state_e.dividing:
            cell_format = division_format
        elif cell.state is state_e.dead:
            cell_format = death_format
        else:
            cell_format = None

        if cell_format is not None:
            value = values[time_point - root_time_point]
            worksheet.write_number(row, time_point, value, cell_format)


def _AddCellStateLegend(
    worksheet: worksheet_t,
    row: int,
    pruned_format: Optional[xlsx_format_t],
    division_format: Optional[xlsx_format_t],
    death_format: Optional[xlsx_format_t],
    /,
) -> None:
    """"""
    for col, state, cell_format in zip(
        range(3),
        ("Dividing", "Dead", "Pruned"),
        (division_format, death_format, pruned_format),
    ):
        if cell_format is not None:
            worksheet.write_string(row, col, state, cell_format)
