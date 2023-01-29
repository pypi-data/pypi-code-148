#!/usr/bin/env python

# stdlib imports
import argparse
import logging
import pathlib
import sys
import warnings

# third party imports
import numpy as np
import pandas as pd
import rasterio

# local imports
from esi_utils_pager.calc import calc_pager_events


def main():
    helpstr = (
        "Render complete empirical PAGER results.\n\n"
        "Default behavior renders PAGER results for a set of earthquakes\n"
        "as a formatted DataFrame with multiple rows of exposure and loss,\n"
        "one row per country, plus a final row with totals. Output columns (in order):\n"
        "EventID: ComCat event ID\n"
        "Time: Event Time (y-m-d h:m:s)\n"
        "Latitude: Event hypocentral latitude\n"
        "Longitude: Event hypocentral longitude\n"
        "Depth: Event hypocentral depth\n"
        "Magnitude: Event magnitude\n"
        "Location: Event location description\n"
        "CountryCode: Country code where exposures/losses occur (or Total)\n"
        "MMI01: Population exposure to shaking at MMI level 1\n"
        "...\n"
        "MMI10: Population exposure to shaking at MMI level 10\n"
        "Fatalities: Fatalities due to shaking\n"
        "EconMMI01: Economic exposure to shaking at MMI level 1\n"
        "...\n"
        "EconMMI10: Economic exposure to shaking at MMI level 10\n"
        "Dollars: Economic losses (USD) due to shaking\n"
    )
    parser = argparse.ArgumentParser(
        description=helpstr,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("gridfolder", help="A valid ShakeMap grid.xml file.")

    parser.add_argument(
        "-o", "--outfile", help="Specify output file (.xlsx for Excel, .csv for CSV)"
    )
    parser.add_argument(
        "-v",
        "--verbose",
        default=False,
        action="store_true",
        help="Print progress output to the screen",
    )

    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(message)s",
        handlers=[logging.StreamHandler()],
    )

    gridfolder = pathlib.Path(args.gridfolder)
    dataframe = calc_pager_events(gridfolder, args.verbose)

    if args.outfile:
        print(f"Saving {len(dataframe)} rows to {args.outfile}")
        if args.outfile.endswith(".xlsx"):
            dataframe.to_excel(args.outfile, index=False)
        else:
            dataframe.to_csv(args.outfile, index=False)
        sys.exit(0)
    else:
        print(dataframe.to_string(index=False))


if __name__ == "__main__":
    main()
