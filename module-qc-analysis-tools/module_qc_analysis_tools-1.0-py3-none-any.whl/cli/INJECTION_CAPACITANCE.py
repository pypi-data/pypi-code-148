#!/usr/bin/env python3
import argparse
import importlib.metadata
import logging
import os
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
from module_qc_data_tools import load_json, outputDataFrame, qcDataFrame, save_dict_list

from module_qc_analysis_tools import data
from module_qc_analysis_tools.utils.analysis import perform_qc_analysis
from module_qc_analysis_tools.utils.misc import (
    DataExtractor,
    JsonChecker,
    bcolors,
    get_inputs,
    get_time_stamp,
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
    log.info(" ===================================================")
    log.info(" \tPerforming Injection Capacitance analysis")
    log.info(" ===================================================")
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
        meas_timestamp = get_time_stamp(filename)
        inputDFs = load_json(filename)

        log.debug(
            f" There are results from {len(inputDFs)} chip(s) stored in this file"
        )
        for inputDF in inputDFs:
            qcframe = inputDF.get_results()
            metadata = qcframe.get_meta_data()

            """"" Check file integrity  """ ""
            checker = JsonChecker(inputDF, f"{test_type}")

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
            extractor = DataExtractor(inputDF, f"{test_type}")
            calculated_data = extractor.calculate()

            """""        Plotting       """ ""
            CapMeas = calculated_data.get("CapMeas").get("Values")
            CapMeasPar = calculated_data.get("CapMeasPar").get("Values")
            VDDAcapmeas = calculated_data.get("VDDAcapmeas").get("Values")

            allCpix = []
            for i in range(len(CapMeas)):
                cmeas = abs(CapMeas[i] / (VDDAcapmeas[i] * 10000000))
                cpar = abs(CapMeasPar[i] / (VDDAcapmeas[i] * 10000000))
                cpix = ((cmeas - cpar) / 100) - 0.48e-15
                allCpix += [cpix * 1e15]

            avgCpix = sum(allCpix) / len(allCpix)

            fig, ax1 = plt.subplots()
            ax1.plot(
                range(len(allCpix)),
                allCpix,
                "o",
                label="Pixel injection capacitance",
                markersize=10,
            )
            plt.axhline(
                y=avgCpix,
                color="r",
                linestyle="-",
                label="Average Cpix = " + str(round(avgCpix, 3)) + " fF",
            )
            plt.legend(bbox_to_anchor=(1.0, 1), loc="upper right")
            plt.title(chipname)
            ax1.set_xlabel("N (measurements)")
            ax1.set_ylim(min(allCpix) - 0.1, max(allCpix) + 0.1)
            ax1.set_ylabel("Pixel injection capacitance [fF]")
            plt.grid()
            log.info(
                f" Saving {output_dir}/{test_type}/{timestart}/{chipname}_cpix.png"
            )
            plt.savefig(f"{output_dir}/{test_type}/{timestart}/{chipname}_cpix.png")
            plt.close()

            fig, ax1 = plt.subplots()
            ax1.plot(
                range(len(CapMeas)),
                CapMeas,
                "o",
                label="Capmeasure current circuit",
                markersize=10,
            )
            ax1.set_xlabel("N (measurements)")
            ax1.set_ylabel("CapMeas circuit current [A]")
            plt.grid()
            plt.title(chipname)
            log.info(
                f" Saving {output_dir}/{test_type}/{timestart}/{chipname}_capmeas.png"
            )
            plt.savefig(f"{output_dir}/{test_type}/{timestart}/{chipname}_capmeas.png")
            plt.close()

            fig, ax1 = plt.subplots()
            ax1.plot(
                range(len(CapMeasPar)),
                CapMeasPar,
                "o",
                label="Capmeasure parasitic current circuit",
                markersize=10,
            )
            ax1.set_xlabel("N (measurements)")
            ax1.set_ylabel("CapMeas parasitic current [A]")
            plt.grid()
            plt.title(chipname)
            log.info(
                f" Saving {output_dir}/{test_type}/{timestart}/{chipname}_capmeaspar.png"
            )
            plt.savefig(
                f"{output_dir}/{test_type}/{timestart}/{chipname}_capmeaspar.png"
            )
            plt.close()

            # Load values to dictionary for QC analysis
            results = {}
            results.update({"INJ_CAPACITANCE": avgCpix})

            # Perform QC analysis
            passes_qc = perform_qc_analysis(
                test_type, args.qc_criteria, args.layer, results, args.verbosity
            )

            if passes_qc == -1:
                log.error(
                    bcolors.ERROR
                    + f" QC analysis for {chipname} was NOT successful. Please fix and re-run. Continuing to next chip.."
                    + bcolors.ENDC
                )
                continue
            log.info("")
            if passes_qc:
                log.info(
                    f" Chip {chipname} passes QC? "
                    + bcolors.OKGREEN
                    + f"{passes_qc}"
                    + bcolors.ENDC
                )
            else:
                log.info(
                    f" Chip {chipname} passes QC? "
                    + bcolors.BADRED
                    + f"{passes_qc}"
                    + bcolors.ENDC
                )
            log.info("")

            """"" Information for output json file """ ""
            tmpoutput = {}

            tmpoutput["INJ_CAPACITANCE"] = round(avgCpix, 3)
            tmpoutput["Metadata"] = metadata
            tmpoutput["passes_qc"] = passes_qc
            if output.get(chipname):
                output[chipname].update(tmpoutput)
            else:
                output[chipname] = tmpoutput

        # Make one output file per chip
        for chipname, chip in output.items():
            outputDF = outputDataFrame()
            test_type = os.path.basename(__file__).split(".py")[0]
            outputDF.set_test_type(test_type)
            data = qcDataFrame()
            data.add_property(
                "ANALYSIS_VERSION",
                importlib.metadata.version("module-qc-analysis-tools"),
            )
            data._meta_data.update(chip["Metadata"])
            chip.pop("Metadata")
            if outputDF._passed is not False:
                outputDF.set_pass_flag(chip["passes_qc"])
            chip.pop("passes_qc")
            for result in chip.keys():
                data.add_parameter(result, chip[result])
            outputDF.set_results(data)
            if args.permodule:
                alloutput += [outputDF.to_dict(True)]
                timestamps += [meas_timestamp]
            else:
                log.info(
                    f" Saving output of analysis to: {output_dir}/{test_type}/{timestart}/{chipname}.json"
                )
                outfile = f"{output_dir}/{test_type}/{timestart}/{chipname}.json"
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
