"""
Reading data from RAW Limax files.

Anonymization.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd

from limax import log
from limax.console import console
from limax.model import LX, LXData, LXMetaData
from limax.plot import plot_lx_matplotlib


logger = log.get_logger(__file__)


def read_limax_dir(input_dir: Path, output_dir: Path) -> None:
    """Read limax data from folder."""
    # process all files
    for limax_csv in input_dir.glob("**/*.csv"):
        limax_csv_rel = limax_csv.relative_to(input_dir)
        output_path: Path = Path(output_dir / limax_csv_rel)
        parse_limax_file(limax_csv=limax_csv, output_dir=output_path.parent)


def _parse_metadata(md_lines: List[str]) -> LXMetaData:
    """Parse metadata from metadata lines."""
    md_dict: Dict[str, Any] = {
        "mid": "-",
        "datetime": "-",
        "height": -1.0,
        "weight": -1.0,
        "sex": "NA",
        "food_abstinence": "-",
        "smoking": False,
        "oxygen": False,
        "ventilation": False,
        "medication": False,
    }
    tokens: List[str]

    if len(md_lines) == 11:
        """
        Format 1 (length=11):

        # mID 102
        # 'doc' (, )
        # Dr. Max Mustermann
        # 01.01.2010 08:30
        # utouARg
        # 160 cm
        # 70 kg
        # 43,295187
        # 44,395187
        # 630,0
        # Nahrungskarenz: über 3 Std., Raucher: Nein, Sauerstoff: Nein, Beatmung: Nein, Medikation: Ja
        """
        # print("Old limax format")

        tokens = md_lines[10].split(",")
        md_dict["mid"] = md_lines[0].split()[1]
        md_dict["datetime"] = md_lines[3]
        md_dict["height"] = float(md_lines[5].split()[0])
        md_dict["weight"] = float(md_lines[6].split()[0])
        md_dict["food_abstinence"] = tokens[0].split(":")[1].strip()
        md_dict["smoking"] = tokens[1].split(":")[1].strip()
        md_dict["oxygen"] = tokens[2].split(":")[1].strip()
        md_dict["ventilation"] = tokens[3].split(":")[1].strip()
        md_dict["medication"] = tokens[4].split(":")[1].strip()

        for key in ["smoking", "oxygen", "ventilation", "medication"]:
            if md_dict[key].lower() == "ja":
                md_dict[key] = True
            elif md_dict[key].lower() == "nein":
                md_dict[key] = False
            else:
                logger.error(f"Invalid value in metadata: '{key}: {md_dict[key]}'")
                md_dict[key] = True

    elif len(md_lines) == 14:
        """
        Format 2 (length=14):

        # mID XXX;;;;
        # 'doc' (; );;;
        # anordnender Arzt;;;;
        # Untersuchungsdatum Uhrzeit;;;;
        # Name Vorname;;;;
        # Geburtsdatum;;;;
        # männlich;;;;
        # Körpergröße in cm;;;;
        # Gewicht in kg;;;;
        # 24;664728;;;
        # 305;0;;;
        # Nahrungskarenz: über 3 Std.; Raucher: Nein; Sauerstoff: Nein; Beatmung: Nein; Medikation: Ja
        # Wir berichten Ihnen über die durchgeführten Untersuchungen bei unserem gemeinsamen Patienten / unserer gemeinsamen Patientin:;;;;
        # Der LiMAx-Test gibt die aktuelle Leberfunktionskapazität des CYP1A2-Systems an. Aktuell ist dieser Wert ...;;;;
        """
        # print("New limax format")
        tokens = md_lines[11].split(";")
        md_dict["mid"] = md_lines[0].split()[1]
        md_dict["datetime"] = md_lines[3]
        try:
            md_dict["height"] = float(md_lines[7].split()[0])
        except ValueError as err:
            logger.error(err)
        try:
            md_dict["weight"] = float(md_lines[8].split()[0])
        except ValueError as err:
            logger.error(err)
        md_dict["food_abstinence"] = tokens[0].split(":")[1].strip()
        md_dict["smoking"] = tokens[1].split(":")[1].strip()
        md_dict["oxygen"] = tokens[2].split(":")[1].strip()
        md_dict["ventilation"] = tokens[3].split(":")[1].strip()
        md_dict["medication"] = tokens[4].split(":")[1].strip()
        md_dict["sex"] = md_lines[6].strip()

        for key in ["smoking", "oxygen", "ventilation", "medication"]:
            if md_dict[key].lower() == "ja":
                md_dict[key] = True
            elif md_dict[key].lower() == "nein":
                md_dict[key] = False
            else:
                logger.error(f"Invalid value in metadata: '{key}: {md_dict[key]}'")
                md_dict[key] = True
    else:
        raise ValueError("Unsupported LiMAx MetaData format.")

    lx_metadata: LXMetaData = LXMetaData(**md_dict)
    return lx_metadata


def parse_limax_file(
    limax_csv: Path,
    output_dir: Optional[Path] = None,
) -> LX:
    """Read limax data."""
    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)
        # limax_path = output_dir / f"{limax_csv.stem}.txt"
        json_path = output_dir / f"{limax_csv.stem}.json"
        fig_path = output_dir / f"{limax_csv.stem}.png"
        console.log(f"Processing '{limax_csv}' -> '{json_path}'")

    # anonymize file (drop name & birth date)
    # drop_lines = [
    #     "# Geburtsdatum",
    #     "# Name",
    # ]
    # lines: List[str] = []
    # with open(limax_csv, "r") as f_in:
    #     raw_lines: List[str] = f_in.readlines()
    #
    #     for line in raw_lines:
    #         for drop in drop_lines:
    #             if line.startswith(drop):
    #                 continue
    #         lines.append(line)
    #
    # with open(limax_path, "w") as f_limax:
    #     f_limax.write("\n".join(lines))

    # parse file
    line_offset = -1
    lines: List[str] = []

    with open(limax_csv, "r") as f:
        raw_lines: List[str] = f.readlines()

        # cleanup lines
        for line in raw_lines:
            if line.startswith("# "):
                line = line[2:]
            # remove ending characters
            line = line.replace(";;;;", "")
            line = line.strip()
            if len(line) > 0:
                lines.append(line)

        # find metadata offset in clean lines
        for k, line in enumerate(lines):
            if line.startswith("Zeit"):
                line_offset = k
                break
        else:
            raise ValueError(
                f"No line starting with 'Zeit' in csv, invalid LIMAX file: {limax_csv}"
            )

    md_lines = lines[:line_offset]
    data_lines = lines[line_offset + 1 :]

    # parse metadata
    lx_metadata: LXMetaData = _parse_metadata(md_lines)

    # parse data
    time, dob, error = [], [], []
    for line in data_lines:
        # cleanup of lines
        tokens = [t.strip() for t in line.split("\t")]
        time.append(int(tokens[0]))
        dob.append(float(tokens[1]))
        error.append(str(tokens[2]))

    d: Dict[str, Any] = {
        "time": time,
        "dob": dob,
        "error": error,
    }
    df = pd.DataFrame(data=d)
    df = df[["time", "dob", "error"]]

    # sort by time (some strange artefacts in some files)
    df.sort_values(by=["time"], inplace=True)
    lx_data = LXData(
        time=list(df.time.values), dob=list(df.dob.values), error=list(df.error.values)
    )
    lx = LX(metadata=lx_metadata, data=lx_data)

    # serialization to JSON
    if output_dir:
        with open(json_path, "w") as f_json:
            f_json.write(lx.json(indent=2))
        plot_lx_matplotlib(lx, fig_path=fig_path)

    return lx


if __name__ == "__main__":
    from limax import (
        EXAMPLE_LIMAX_PATIENT1_PATH,
        EXAMPLE_LIMAX_PATIENT2_PATH,
        EXAMPLE_LIMAX_PATIENT3_PATH,
        PROCESSED_DIR,
    )

    for path in [
        EXAMPLE_LIMAX_PATIENT1_PATH,
        EXAMPLE_LIMAX_PATIENT2_PATH,
        EXAMPLE_LIMAX_PATIENT3_PATH,
    ]:
        lx = parse_limax_file(limax_csv=path, output_dir=PROCESSED_DIR)
        console.print(lx)
        console.print(lx.json())
        console.print(lx.data.to_df())

    # read_limax_dir(input_dir=RAW_DIR, output_dir=PROCESSED_DIR)
