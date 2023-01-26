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
    getImuxMap,
    getVmuxMap,
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
parser.add_argument("--verbose", action="store_true", help="verbose mode")
args = parser.parse_args()

log = logging.getLogger(__name__)
log.setLevel(args.verbosity)


def get_NtcCalPar(metadata):
    # Read NTC parameters from metadata in the chip config.
    if "NtcCalPar" in metadata:
        NtcCalPar = metadata.get("NtcCalPar")
    else:
        NtcCalPar = [
            0.0007488999981433153,
            0.0002769000129774213,
            7.059500006789676e-08,
        ]
        log.warning(
            bcolors.WARNING
            + " No NtcCalPar found in the input config file! Using the default NTC parameters."
            + bcolors.ENDC
        )
    return NtcCalPar


def get_NfPar(metadata):
    # Read Nf parameters from metadata in the chip config.
    if "NfASLDO" in metadata:
        NfASLDO = metadata.get("NfASLDO")
    else:
        NfASLDO = 1.264
        log.warning(
            bcolors.WARNING
            + f" No NfASLDO found in the input config file! Using the default Nf parameter value {NfASLDO}."
            + bcolors.ENDC
        )
    if "NfDSLDO" in metadata:
        NfDSLDO = metadata.get("NfDSLDO")
    else:
        NfDSLDO = 1.264
        log.warning(
            bcolors.WARNING
            + f" No NfASLDO found in the input config file! Using the default Nf parametervalue {NfASLDO}."
            + bcolors.ENDC
        )
    if "NfACB" in metadata:
        NfACB = metadata.get("NfACB")
    else:
        NfACB = 1.264
        log.warning(
            bcolors.WARNING
            + f" No Nfacb found in the input config file! Using the default Nf parameter value {NfASLDO}."
            + bcolors.ENDC
        )

    return [NfASLDO, NfDSLDO, NfACB]


def calculate_T(calculated_data, NtcCalPar, NfPar):
    # Calculate T External NTC
    Vntc = np.array(calculated_data["Vntc"]["Values"])
    Intc = np.array(calculated_data["Intc"]["Values"])

    Rntc = np.mean(Vntc / Intc)
    A = NtcCalPar[0]
    B = NtcCalPar[1]
    C = NtcCalPar[2]
    AR_TEMP_NTC = 1 / (A + B * np.log(Rntc) + C * ((np.log(Rntc)) ** 3)) - 273.15

    log.debug(f" T Ext NTC: {AR_TEMP_NTC} C")

    # Calculate T External External NTC
    AR_TEMP_EXT = np.mean(np.array(calculated_data["TExtExtNTC"]["Values"]))

    log.debug(f" T Ext Ext NTC: {AR_TEMP_EXT} C")

    # Calculate T MOS sensors
    Vmux14 = np.array(calculated_data["VMonSensAna"]["Values"])
    Vmux16 = np.array(calculated_data["VMonSensDig"]["Values"])
    Vmux18 = np.array(calculated_data["VMonSensAcb"]["Values"])

    def calc_temp_sens(Vmux, Nf):
        V_Bias0 = np.mean(Vmux[:16])
        V_Bias1 = np.mean(Vmux[-16:])
        q = 1.602e-19
        kB = 1.38064852e-23
        dV = V_Bias1 - V_Bias0
        T = dV * q / (Nf * kB * np.log(15)) - 273.15
        return T

    AR_TEMP_ASLDO = calc_temp_sens(Vmux14, NfPar[0])
    AR_TEMP_DSLDO = calc_temp_sens(Vmux16, NfPar[1])
    AR_TEMP_ACB = calc_temp_sens(Vmux18, NfPar[2])

    log.debug(f" T MonSensAna: {AR_TEMP_ASLDO} C")
    log.debug(f" T MonSensDig: {AR_TEMP_DSLDO} C")
    log.debug(f" T MonSensAcb: {AR_TEMP_ACB} C")

    return (
        round(AR_TEMP_NTC, 1),
        round(AR_TEMP_EXT, 1),
        round(AR_TEMP_ASLDO, 1),
        round(AR_TEMP_DSLDO, 1),
        round(AR_TEMP_ACB, 1),
    )


def round_list(list_values, digit=None):
    rounded_list = []
    for item in list_values:
        if item >= 0.01 or item == 0:
            rounded_list.append(round(item, digit))
        else:
            rounded_list.append(
                float(np.format_float_scientific(item, precision=digit))
            )
    return rounded_list


def plot_vdd_vs_trim(trim, vdd, vdd_name, output_name, chipname):
    fig, ax1 = plt.subplots()
    ax1.plot(trim, vdd, "o", label=f"{vdd_name} vs trim")
    if args.fit_method == "root":
        p1, p0 = linear_fit(trim, vdd)
    if args.fit_method == "numpy":
        p1, p0 = linear_fit_np(trim, vdd)
    ax1.axhline(y=1.2, color="r", linestyle="--", label=f"Nominal {vdd_name} value")
    x_line = np.linspace(trim[0], trim[-1], 100)
    ax1.plot(
        x_line,
        p1 * x_line + p0,
        "g-",
        alpha=0.5,
        label=f"Fitted line y = {p1:.3e} * x + {p0:.3e}",
    )
    ax1.set_title(f"{vdd_name} vs Trim Chip {chipname}")
    ax1.set_xlabel("Trim")
    ax1.set_ylabel(f"{vdd_name} (V)")
    ax1.legend()
    log.info(f" Saving {output_name}")
    fig.savefig(output_name)


def main():
    log.info("")
    log.info(" ===============================================")
    log.info(" \tPerforming Analog Readback analysis")
    log.info(" ===============================================")
    log.info("")

    test_type = os.path.basename(__file__).split(".py")[0]
    output_dir = f"{args.output_dir}"
    timestart = round(datetime.timestamp(datetime.now()))
    os.makedirs(f"{output_dir}/{test_type}/{timestart}/")
    allinputs = get_inputs(args.input_meas, test_type)

    alloutput = []
    timestamps = []

    alloutput_int_biases = []
    timestamps_int_biases = []

    for filename in sorted(allinputs):
        log.info("")
        log.info(f" Loading {filename}")
        meas_timestamp = get_time_stamp(filename)
        inputDFs = load_json(filename)
        log.debug(
            f" There are results from {len(inputDFs)} chip(s) stored in this file"
        )

        results = {}
        data = {}
        int_biases = {}
        for inputDF in inputDFs:
            qcframe = inputDF.get_results()
            metadata = qcframe.get_meta_data()

            # Read chipname from input DF
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

            # Create an output DF for each chip
            if chipname not in data:
                data[chipname] = qcDataFrame()
                data[chipname].add_property(
                    "ANALYSIS_VERSION",
                    importlib.metadata.version("module-qc-analysis-tools"),
                )
                data[chipname]._meta_data.update(metadata)
                int_biases[chipname] = {}

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

            """""  Calculate quanties   """ ""
            # Vmux conversion is embedded.
            extractor = DataExtractor(inputDF, test_type)
            calculated_data = extractor.calculate()
            Vmux_map = getVmuxMap()
            Imux_map = getImuxMap()

            AR_values_names = []
            for imux in range(32):
                AR_values_names.append(Imux_map[imux])
            for vmux in range(40):
                AR_values_names.append(Vmux_map[vmux])

            tmpresults = {}
            if inputDF._subtestType == "AR_VMEAS":
                for key in calculated_data:
                    int_biases[chipname][key] = calculated_data[key]["Values"][0]
                AR_values = []
                NOT_MEASURED = 0
                for name in AR_values_names:
                    if name in int_biases[chipname]:
                        AR_values.append(int_biases[chipname][name])
                    else:
                        AR_values.append(NOT_MEASURED)
                data[chipname].add_parameter(
                    "AR_NOMINAL_SETTINGS", round_list(AR_values, 4)
                )
                tmpresults.update({"AR_NOMINAL_SETTINGS": AR_values})

            elif inputDF._subtestType == "AR_TEMP":
                NtcCalPar = get_NtcCalPar(metadata["ChipConfigs"]["RD53B"]["Parameter"])
                NfPar = get_NfPar(metadata["ChipConfigs"]["RD53B"]["Parameter"])
                (
                    AR_TEMP_NTC,
                    AR_TEMP_EXT,
                    AR_TEMP_ASLDO,
                    AR_TEMP_DSLDO,
                    AR_TEMP_ACB,
                ) = calculate_T(calculated_data, NtcCalPar, NfPar)
                # Add parameters for output file
                data[chipname].add_parameter("AR_TEMP_NTC", AR_TEMP_NTC)
                data[chipname].add_parameter("AR_TEMP_EXT", AR_TEMP_EXT)
                data[chipname].add_parameter("AR_TEMP_ASLDO", AR_TEMP_ASLDO)
                data[chipname].add_parameter("AR_TEMP_DSLDO", AR_TEMP_DSLDO)
                data[chipname].add_parameter("AR_TEMP_ACB", AR_TEMP_ACB)
                # Load values to dictionary for QC analysis
                tmpresults.update({"ChipNTC_vs_ExtExt": AR_TEMP_NTC - AR_TEMP_EXT})
                tmpresults.update({"ASLO_ChipNTC": AR_TEMP_ASLDO - AR_TEMP_NTC})
                tmpresults.update({"DSLD_ChipNTC": AR_TEMP_DSLDO - AR_TEMP_NTC})
                tmpresults.update({"ACB_ChipNTC": AR_TEMP_ACB - AR_TEMP_NTC})

            elif inputDF._subtestType == "AR_VDD":
                vdda = calculated_data["VDDA"]["Values"].tolist()
                vddd = calculated_data["VDDD"]["Values"].tolist()
                trimA = calculated_data["SldoTrimA"]["Values"].tolist()
                trimD = calculated_data["SldoTrimD"]["Values"].tolist()
                # Add parameters for output file
                data[chipname].add_parameter("AR_VDDA_VS_TRIM", round_list(vdda, 4))
                data[chipname].add_parameter("AR_VDDD_VS_TRIM", round_list(vddd, 4))
                output_name_vdda = (
                    f"{output_dir}/{test_type}/{timestart}/{chipname}_VDDA_TRIM.png"
                )
                output_name_vddd = (
                    f"{output_dir}/{test_type}/{timestart}/{chipname}_VDDD_TRIM.png"
                )
                plot_vdd_vs_trim(trimA, vdda, "VDDA", output_name_vdda, chipname)
                plot_vdd_vs_trim(trimD, vddd, "VDDD", output_name_vddd, chipname)
                # Load values to dictionary for QC analysis
                tmpresults.update({"AR_VDDA_VS_TRIM": round_list(vdda, 4)})
                tmpresults.update({"AR_VDDD_VS_TRIM": round_list(vddd, 4)})

            else:
                log.warning(
                    bcolors.WARNING
                    + f"{filename}.json does not have any required subtestType. Skipping."
                    + bcolors.ENDC
                )
                continue

            if results.get(chipname):
                results[chipname].update(tmpresults)
            else:
                results[chipname] = tmpresults

        """"" Output a json file """ ""
        for key, df in data.items():
            outputDF = outputDataFrame()
            outputDF.set_test_type(test_type)
            outputDF.set_results(df)

            # Perform QC analysis
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

        if args.verbosity == "DEBUG":
            # Save an output file for only internal biases
            for key in int_biases:
                if args.permodule:
                    alloutput_int_biases += [int_biases[key]]
                    timestamps_int_biases += [meas_timestamp]
                else:
                    log.info(
                        f" Saving DEBUG file with internal biases to: {output_dir}/{test_type}/{timestart}/{key}_internal_biases.json"
                    )
                    outfile = f"{output_dir}/{test_type}/{timestart}/{key}_internal_biases.json"
                    save_dict_list(outfile, [int_biases[key]])
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
        if args.verbosity == "DEBUG":
            # Save an output file for only internal biases
            dfs = np.array(alloutput_int_biases)
            tss = np.array(timestamps_int_biases)
            for x in np.unique(tss):
                log.info(
                    f" Saving DEBUG file with internal biases to: {output_dir}/{test_type}/{timestart}/internal_biases_{x}.json"
                )
                save_dict_list(
                    f"{output_dir}/{test_type}/{timestart}/internal_biases_{x}.json",
                    dfs[tss == x].tolist(),
                )


if __name__ == "__main__":
    main()
