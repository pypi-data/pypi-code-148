#!/usr/bin/env python3
import argparse
import glob
import json
import logging
import os

log = logging.getLogger(__name__)

parser = argparse.ArgumentParser()
parser.add_argument(
    "-i", "--input-file", action="store", required=True, help="Analysis output file."
)
parser.add_argument(
    "-c",
    "--config-file",
    action="store",
    required=True,
    help="Path to the config file to be modified",
)
parser.add_argument(
    "-t",
    "--config-type",
    action="store",
    required=False,
    help="The config type to be modified. E.g. L2_warm/l2_cold.",
)
args = parser.parse_args()


class WriteConfig:
    ##############
    # This class converts a parameter in a chip config to a given value.
    # `in_path` must be the path to the output directory of the analysis.
    # `config_path` must be the path to the directory ofchip config file in Yarr.
    # If `permodule`, the paths provided much be the path of the correct directory.
    ##############
    def __init__(self, in_path=None, config_path=None, config_type=None):
        self.in_path = in_path
        if config_type:
            self.config_path = os.path.join(config_path, config_type)
        else:
            self.config_path = config_path
        self.in_files = self.get_files(self.in_path)
        self.config_files = self.get_files(self.config_path)
        self.stack = []

    def get_files(self, path):
        allinputs = []
        # Check if input if single file or directory
        if os.path.isfile(path):
            raise KeyError(
                f"The input path `{path}` is a path to a file, not a directory! Please check the input path."
            )
        elif os.path.isdir(path):
            allinputs = sorted(glob.glob(f"{path}/*.json"))
            if len(allinputs) == 0:
                raise FileNotFoundError(
                    f"No input json files in `{path}` are found! Please check the input path."
                )
        else:
            raise FileNotFoundError(
                "Input is not recognized as single file or path to directory containing files. Please check the input."
            )
        return allinputs

    def reset_stack(self):
        self.stack = []

    def lookup(self, input_dict, search_key, update_stack=False):
        # recursion to look up the desired key in a dict and record the path
        for k, v in input_dict.items():
            if k == search_key:
                return v
            elif isinstance(v, dict):
                _v = self.lookup(v, search_key, update_stack)
                if _v is not None:
                    if update_stack:
                        self.stack.append(k)
                    return _v

    def find_VcalPar(self, in_file):
        # find the trim values that gives the closest to nominal vdd value.
        VCAL_MED_SLOPE = float(self.lookup(in_file, "VCAL_MED_SLOPE"))
        VCAL_MED_OFFSET = float(self.lookup(in_file, "VCAL_MED_OFFSET"))
        return [VCAL_MED_SLOPE, VCAL_MED_OFFSET]

    def overwrite(self, config_file, search_key, set_value):
        # search_key is a string which is the name of the parameter that will be overwritten.
        # set_value is the value the parameter that will be overwritten to.
        with open(config_file) as jsonFile:
            config_file_data = json.load(jsonFile)
        self.reset_stack()
        original_search_key = self.lookup(config_file_data, search_key, True)
        if original_search_key is None:
            raise KeyError(f"Parameter not found in config file {config_file}! ")
        log.info(f"[{search_key}] Change from {original_search_key} to {set_value}")
        original_search_key = set_value
        self.stack.reverse()

        part_config_file_data = config_file_data
        for k in self.stack:
            part_config_file_data = part_config_file_data[k]
        part_config_file_data[search_key] = original_search_key

        with open(config_file, "w") as jsonFile:
            json.dump(config_file_data, jsonFile, indent=4)

    def set_VcalPar(self):
        for config_file in self.config_files:
            with open(config_file) as jsonFile:
                config_file_data = json.load(jsonFile)
            config_chip_name = self.lookup(config_file_data, "Name")
            config_chip_serial = int(config_chip_name, base=16)

            # overwrite the parameter
            for in_file in self.in_files:
                found_chip = False
                with open(in_file) as jsonFile:
                    in_file_data = json.load(jsonFile)
                for chip_data in in_file_data:
                    # Check if chip name matched
                    in_chip_serial = self.lookup(chip_data, "serialNumber")
                    if in_chip_serial is None:
                        raise KeyError(
                            f"Chip {config_chip_name} not found in the input files! Please check the input files."
                        )
                    if in_chip_serial != config_chip_serial:
                        log.info(
                            f"Chip {config_chip_name} not found in config. Checking the next chip."
                        )
                    else:
                        found_chip = True
                        VcalPar = self.find_VcalPar(chip_data)
                        self.overwrite(config_file, "VcalPar", VcalPar)
                        break
                if found_chip:
                    break
            if not found_chip:
                raise KeyError(
                    f"Chip {config_chip_name} with serial number {config_chip_serial} not found! Please check the input files."
                )


def main():
    wc = WriteConfig(args.input_file, args.config_file, args.config_type)
    wc.set_VcalPar()


if __name__ == "__main__":
    main()
