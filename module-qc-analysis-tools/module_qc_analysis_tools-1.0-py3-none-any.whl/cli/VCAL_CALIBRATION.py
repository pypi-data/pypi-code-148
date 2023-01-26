#!/usr/bin/env python3
import argparse
import logging
import os
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import pkg_resources
from module_qc_data_tools import load_json, outputDataFrame, qcDataFrame, save_dict_list

from module_qc_analysis_tools import data
from module_qc_analysis_tools.utils.analysis import perform_qc_analysis
from module_qc_analysis_tools.utils.misc import (
    DataExtractor,
    JsonChecker,
    bcolors,
    get_inputs,
    get_time_stamp,
    linear_fit,
    linear_fit_np,
)

parser = argparse.ArgumentParser()
parser.add_argument(
    "-i",
    "--input-meas",
    action="store",
    required=True,
    help="path to the input measurement file or directory containing input measurement files.",
)
parser.add_argument(
    "-o",
    "--output-dir",
    action="store",
    default="outputs",
    help="output directory",
)
parser.add_argument(
    "-q",
    "--qc-criteria",
    action="store",
    default=data / "analysis_cuts.json",
    help="path to json file with QC selection criteria (default: $(module-qc-analysis-tools --prefix)/analysis_cuts.json)",
)
parser.add_argument(
    "-l",
    "--layer",
    action="store",
    default="Unknown",
    help="Layer of module, used for applying correct QC criteria settings. Options: L0, L1, L2 (default)",
)
parser.add_argument(
    "--permodule",
    action="store_true",
    help="Store results in one file per module (default: one file per chip)",
)
parser.add_argument(
    "-f",
    "--fit-method",
    action="store",
    default="numpy",
    choices=["root", "numpy"],
    help="fitting method",
)
parser.add_argument(
    "-v",
    "--verbosity",
    action="store",
    default="INFO",
    help="Log level [options: DEBUG, INFO (default), WARNING, ERROR]",
)
args = parser.parse_args()

log = logging.getLogger(__name__)
log.setLevel(args.verbosity)


def main():
    log.info("")
    log.info(" ==========================================")
    log.info(" \tPerforming VCAL calibration analysis")
    log.info(" ==========================================")
    log.info("")

    test_type = os.path.basename(__file__).split(".py")[0]

    output_dir = f"{args.output_dir}"
    timestart = round(datetime.timestamp(datetime.now()))
    os.makedirs(f"{output_dir}/{test_type}/{timestart}/")

    allinputs = get_inputs(args.input_meas, test_type)

    alloutput = []
    timestamps = []
    for filename in allinputs:
        log.info("")
        log.info(f" Loading {filename}")
        output = {}
        results = {}
        meas_timestamp = get_time_stamp(filename)
        inputDFs = load_json(filename)

        log.debug(
            f" There are results from {len(inputDFs)} chip(s) stored in this file"
        )
        for inputDF in inputDFs:
            qcframe = inputDF.get_results()
            metadata = qcframe.get_meta_data()

            """ Determine test type """
            try:
                testname = inputDF._subtestType
                testprefix = testname.split("_")[0] + "_" + testname.split("_")[1]
                testsuffix = testname.split(testprefix)[1]
            except Exception:
                log.error(
                    bcolors.ERROR
                    + f" {filename}.json does not have subtestType, which is needed for VCAL_CALIBRATION analysis, skipping!"
                    + bcolors.ENDC
                )
                continue

            """"" Check file integrity  """ ""
            checker = JsonChecker(inputDF, test_type)

            try:
                checker.check()
            except BaseException as exc:
                log.exception(exc)
                log.warning(
                    bcolors.WARNING
                    + " JsonChecker check not passed, skipping this input."
                    + bcolors.ENDC
                )
                continue
            else:
                log.debug(" JsonChecker check passed!")
                pass

            try:
                chipname = metadata.get("Name")
                log.debug(f" Found chip name = {chipname} from chip config")
            except Exception:
                log.warning(
                    bcolors.WARNING
                    + "Chip name not found in input from {filename}, skipping."
                    + bcolors.ENDC
                )
                continue

            """""  Calculate quanties   """ ""
            # Vmux conversion is embedded.
            extractor = DataExtractor(inputDF, test_type)
            calculated_data = extractor.calculate()

            """""        Plotting       """ ""
            # task specific - for Vcal Calibration x and y needs to be determined for plotting.
            for key, value in calculated_data.items():
                if value["X"] is True:
                    x_key = key

            x = calculated_data.pop(x_key)

            y_values = ["VcalHi", "VcalMed"]
            for key in y_values:
                value = calculated_data.get(key)
                if not value:
                    # Note: This prevents from entering loop more than once
                    continue
                if args.fit_method == "root":
                    p1, p0 = linear_fit(x["Values"], value["Values"])
                if args.fit_method == "numpy":
                    p1, p0 = linear_fit_np(x["Values"], value["Values"])
                # Convert from V to mV
                p1mv = p1 * 1000
                p0mv = p0 * 1000

                fig, ax1 = plt.subplots()
                ax1.plot(
                    x["Values"],
                    value["Values"],
                    "o",
                    label="Measured data",
                    markersize=10,
                )
                x_line = np.linspace(x["Values"][0], x["Values"][-1], 100)
                ax1.plot(x_line, p1 * x_line + p0, "r--", label="Fitted line")
                ax1.text(
                    x["Values"][0],
                    0.75 * value["Values"][-1],
                    f"y = {p1:.4e} * x + {p0:.4e}",
                )
                ax1.set_xlabel(f"{x_key}[{x['Unit']}]")
                ax1.set_ylabel(f"{key}[{value['Unit']}]")
                ax1.set_title(chipname)
                ax1.legend()
                log.info(
                    f" Saving {output_dir}/{test_type}/{timestart}/{chipname}_{testname}.png"
                )
                plt.savefig(
                    f"{output_dir}/{test_type}/{timestart}/{chipname}_{testname}.png"
                )
                plt.close()

            # Load values to dictionary for QC analysis (later)
            tmpresults = {}
            tmpresults.update({f"{testprefix}_SLOPE{testsuffix}": p1mv})
            tmpresults.update({f"{testprefix}_OFFSET{testsuffix}": p0mv})

            """"" Information for output json file """ ""
            tmpoutput = {}

            tmpoutput[f"{testprefix}_SLOPE{testsuffix}"] = p1mv
            tmpoutput[f"{testprefix}_OFFSET{testsuffix}"] = p0mv
            tmpoutput["Metadata"] = metadata
            if output.get(chipname):
                output[chipname].update(tmpoutput)
                results[chipname].update(tmpresults)
            else:
                output[chipname] = tmpoutput
                results[chipname] = tmpresults

        # Perform QC analysis and make one output file per chip
        for key, chip in output.items():
            for subtest in ["HIGH", "MED"]:
                if results.get(key).get(
                    f"VCAL_{subtest}_SLOPE_SMALL_RANGE"
                ) and results.get(key).get(f"VCAL_{subtest}_SLOPE"):
                    results.get(key).update(
                        {
                            f"VCAL_{subtest}_SLOPE_SMALL_RANGE_RATIO": results.get(
                                key
                            ).get(f"VCAL_{subtest}_SLOPE_SMALL_RANGE")
                            / results.get(key).get(f"VCAL_{subtest}_SLOPE")
                        }
                    )
                    results.get(key).pop(f"VCAL_{subtest}_SLOPE_SMALL_RANGE")

                elif results.get(key).get(
                    f"VCAL_{subtest}_SLOPE_SMALL_RANGE"
                ) and not results.get(key).get(f"VCAL_{subtest}_SLOPE"):
                    log.warning(
                        bcolors.WARNING
                        + f" Results from VCAL_{subtest}_SLOPE test not found. Unable to perform QC analysis on VCAL_{subtest}_SLOPE_SMALL_RANGE"
                        + bcolors.ENDC
                    )
                    results.get(key).pop(f"VCAL_{subtest}_SLOPE_SMALL_RANGE")

                results.get(key).pop(f"VCAL_{subtest}_OFFSET_SMALL_RANGE", "")

            passes_qc = perform_qc_analysis(
                test_type,
                args.qc_criteria,
                args.layer,
                results.get(key),
                args.verbosity,
            )
            if passes_qc == -1:
                log.error(
                    bcolors.ERROR
                    + f" QC analysis for {key} was NOT successful. Please fix and re-run. Continuing to next chip.."
                    + bcolors.ENDC
                )
                continue
            log.info("")
            if passes_qc:
                log.info(
                    f" Chip {key} passes QC? "
                    + bcolors.OKGREEN
                    + f"{passes_qc}"
                    + bcolors.ENDC
                )
            else:
                log.info(
                    f" Chip {key} passes QC? "
                    + bcolors.BADRED
                    + f"{passes_qc}"
                    + bcolors.ENDC
                )
            log.info("")

            outputDF = outputDataFrame()
            test_type = os.path.basename(__file__).split(".py")[0]
            outputDF.set_test_type(test_type)
            data = qcDataFrame()
            data.add_property(
                "ANALYSIS_VERSION",
                pkg_resources.get_distribution("module-qc-analysis-tools").version,
            )
            data._meta_data.update(chip["Metadata"])
            chip.pop("Metadata")
            for param in chip.keys():
                data.add_parameter(param, chip[param])
            outputDF.set_results(data)
            outputDF.set_pass_flag(passes_qc)
            if args.permodule:
                alloutput += [outputDF.to_dict(True)]
                timestamps += [meas_timestamp]
            else:
                outfile = f"{output_dir}/{test_type}/{timestart}/{key}.json"
                log.info(
                    f" Saving output of analysis to: {output_dir}/{test_type}/{timestart}/{key}.json"
                )
                save_dict_list(outfile, [outputDF.to_dict(True)])
    if args.permodule:
        # Only store results from same timestamp into same file
        dfs = np.array(alloutput)
        tss = np.array(timestamps)
        for x in np.unique(tss):
            log.info(
                f" Saving output of analysis to: {output_dir}/{test_type}/{timestart}/module.json"
            )
            save_dict_list(
                f"{output_dir}/{test_type}/{timestart}/module.json",
                dfs[tss == x].tolist(),
            )


if __name__ == "__main__":
    main()
