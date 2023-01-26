#!/usr/bin/env python3
import json
import logging
import os
import sys
from pathlib import Path

from module_qc_analysis_tools.utils.misc import bcolors, getImuxMap, getVmuxMap

log = logging.getLogger(__name__)
log.setLevel("INFO")

if sys.version_info >= (3, 9):
    from importlib import resources
else:
    import importlib_resources as resources


def format_text():
    return " {:^30}: {:^20}: {:^20}: {:^5}"


def print_output_pass(key, results, lower_bound, upper_bound):
    txt = format_text()
    log.info(
        bcolors.OKGREEN
        + txt.format(
            key,
            round(results, 4),
            f"[{lower_bound}, {upper_bound}]",
            "PASS",
        )
        + bcolors.ENDC
    )


def print_output_fail(key, results, lower_bound, upper_bound):
    txt = format_text()
    log.info(
        bcolors.BADRED
        + txt.format(
            key,
            round(results, 4),
            f"[{lower_bound}, {upper_bound}]",
            "FAIL",
        )
        + bcolors.ENDC
    )


def get_layer(layer):
    layers = {"L0": "LZero", "L1": "LOne", "L2": "LTwo"}
    return layers.get(layer)


def check_layer(layer):
    possible_layers = ["L0", "L1", "L2"]
    if layer not in possible_layers:
        log.error(
            bcolors.ERROR
            + f" Layer '{layer}' not recognized or not provided. Provide the layer with the --layer [L0, L1, or L2] option."
            + bcolors.ENDC
        )
        sys.exit(-1)


# The following hardcoded values are from https://gitlab.cern.ch/atlas-itk/pixel/module/itkpix-electrical-qc
def get_nominal_current(layer):
    check_layer(layer)
    # Assumes triplets for L0, quads for L1-L2
    currents_per_chip = {
        "L0": 1.85 * 3,
        "L1": 1.65 * 4,
        "L2": 1.47 * 4,
    }
    return currents_per_chip.get(layer)


def get_nominal_Voffs(layer, lp_mode=False):
    check_layer(layer)
    Voffs = {
        "L0": 1.1,
        "L1": 1.0,
        "L2": 1.0,
    }
    Voffs_lp = {
        "L0": 1.38,
        "L1": 1.38,
        "L2": 1.38,
    }
    if lp_mode:
        return Voffs_lp.get(layer)
    else:
        return Voffs.get(layer)


def get_nominal_RextA(layer):
    check_layer(layer)
    RextA = {
        "L0": 511,
        "L1": 732,
        "L2": 866,
    }
    return RextA.get(layer)


def get_nominal_RextD(layer):
    check_layer(layer)
    RextD = {"L0": 407, "L1": 549, "L2": 590}
    return RextD.get(layer)


# Function to get key from value in muxMaps
def get_key(mydict, val):
    for key, value in mydict.items():
        if val == value:
            return key
    return -1


def perform_qc_analysis_AR(
    test_type, qc_criteria, layer_name, results, verbosity="INFO"
):
    log.setLevel(verbosity)
    # Basically the same function as perform_qc_analysis
    # minus all the initial checks which have already been performed.

    passes_qc_overall = True
    VmuxMap = getVmuxMap()
    ImuxMap = getImuxMap()
    if len(VmuxMap.keys()) + len(ImuxMap.keys()) != len(results):
        log.error(
            bcolors.ERROR
            + " Number of entries in AR_NOMINAL_SETTINGS results does not match number of entries in VmuxMap and ImuxMap - there should be one entry for every Vmux and Imux in those maps. Please fix and re-run!"
            + bcolors.ENDC
        )
        return -1
    for key, value in qc_criteria.items():

        log.debug(f" QC selections for {key}: {value}")
        try:
            lower_bound = value[0]
            upper_bound = value[1]
        except Exception:
            log.error(
                bcolors.ERROR
                + f" QC selections for {key} are ill-formatted, should be list of length 2! Please fix: {value} . Skipping."
                + bcolors.ENDC
            )
            continue

        passes_qc_test = True
        if get_key(VmuxMap, key) != -1:
            index = get_key(VmuxMap, key)
        elif get_key(ImuxMap, key) != -1:
            index = get_key(ImuxMap, key) + len(VmuxMap.keys()) + 1
        else:
            log.error(
                bcolors.ERROR
                + f"Did not find {key} in VmuxMap or ImuxMap - please check!"
                + bcolors.ENDC
            )
            continue
        log.debug(f" Key is {key}, value is {value}, index is {index}")

        if (results[index] < lower_bound) or (results[index] > upper_bound):
            passes_qc_test = False
        if passes_qc_test:
            print_output_pass(key, results[index], lower_bound, upper_bound)
        else:
            print_output_fail(key, results[index], lower_bound, upper_bound)
    passes_qc_overall = passes_qc_overall and passes_qc_test

    return passes_qc_overall


def perform_qc_analysis(test_type, qc_criteria, layer_name, results, verbosity="INFO"):
    log.setLevel(verbosity)
    log.info("")
    log.info("Performing QC analysis!")
    log.info("")
    if not os.path.isfile(Path(qc_criteria)):
        log.error(
            bcolors.ERROR
            + f" Json file with QC criteria ({Path(qc_criteria)}) not found! Exiting."
            + bcolors.ENDC
        )
        return -1
    log.debug(
        f" Reading QC selection criteria from {Path(qc_criteria)} for {layer_name} config"
    )
    try:
        with resources.as_file(Path(qc_criteria)) as path:
            qc_config = json.loads(path.read_text())
    except Exception as e:
        log.debug(e)
        log.error(
            bcolors.ERROR
            + f" QC criteria json file is ill-formated ({Path(qc_criteria)}) - please fix! Exiting."
            + bcolors.ENDC
        )
        return -1
    qc_selections = qc_config.get(test_type)
    if not qc_selections:
        log.error(
            bcolors.ERROR
            + f" QC criteria for {test_type} not found in {Path(qc_criteria)} - please fix! Exiting."
            + bcolors.ENDC
        )
        return -1

    check_layer(layer_name)
    layer = get_layer(layer_name)

    passes_qc_overall = True
    txt = format_text()
    log.info(txt.format("Parameter", "Analysis result", "QC criteria", "Pass"))
    log.info(
        "--------------------------------------------------------------------------------------"
    )

    for key in results.keys():

        if not qc_selections.get(key):
            log.warning(
                bcolors.WARNING
                + f" Selection for {key} not found in QC file! Skipping."
                + bcolors.ENDC
            )
            continue

        # Handle AR_NOMINAL_SETTINGS in completely different function, for now...
        if key == "AR_NOMINAL_SETTINGS":
            passes_qc_test = perform_qc_analysis_AR(
                test_type,
                qc_selections.get(key),
                layer_name,
                results.get(key),
                verbosity,
            )
            passes_qc_overall = passes_qc_overall and passes_qc_test
            continue

        log.debug(f" QC selections for {key}: {qc_selections.get(key)}")
        if type(qc_selections.get(key)) is list:
            if len(qc_selections.get(key)) != 2:
                log.error(
                    bcolors.ERROR
                    + f" QC selections for {key} are ill-formatted, should be list of length 2! Please fix: {qc_selections.get(key)} . Skipping."
                    + bcolors.ENDC
                )
                continue
            lower_bound = qc_selections.get(key)[0]
            upper_bound = qc_selections.get(key)[1]
        elif type(qc_selections.get(key)) is dict:
            layer_bounds = qc_selections.get(key).get(layer)
            if not layer_bounds:
                log.error(
                    bcolors.ERROR
                    + f" QC selections for {key} and {layer} do not exist - please check! Skipping."
                    + bcolors.ENDC
                )
                continue
            lower_bound = layer_bounds[0]
            upper_bound = layer_bounds[1]

        passes_qc_test = True
        if ("AR_VDDA_VS_TRIM" in key) or ("AR_VDDD_VS_TRIM" in key):
            # All values in list must satisfy requirements
            for elem in results.get(key):
                tmp_pass_qc = True
                if (elem < lower_bound) or (elem > upper_bound):
                    passes_qc_test = False
                    tmp_pass_qc = False
                if tmp_pass_qc:
                    print_output_pass(key, elem, lower_bound, upper_bound)
                else:
                    print_output_fail(key, elem, lower_bound, upper_bound)

        else:
            if (results.get(key) < lower_bound) or (results.get(key) > upper_bound):
                passes_qc_test = False
            if passes_qc_test:
                print_output_pass(key, results.get(key), lower_bound, upper_bound)
            else:
                print_output_fail(key, results.get(key), lower_bound, upper_bound)
        passes_qc_overall = passes_qc_overall and passes_qc_test
    log.info(
        "--------------------------------------------------------------------------------------"
    )

    return passes_qc_overall
