#!/usr/bin/env python
import argparse
import logging
import os
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import pkg_resources
from module_qc_data_tools import load_json, outputDataFrame, qcDataFrame, save_dict_list

from module_qc_analysis_tools import data
from module_qc_analysis_tools.utils.analysis import (
    get_nominal_current,
    get_nominal_RextA,
    get_nominal_RextD,
    get_nominal_Voffs,
    perform_qc_analysis,
)
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
    "-n",
    "--nChips",
    action="store",
    type=int,
    default=4,
    help="Number of chips powered in parallel (e.g. 4 for a quad module, 3 for a triplet, 1 for an SCC.)",
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
parser.add_argument("--lp-enable", action="store_true", help="low power mode")
args = parser.parse_args()

log = logging.getLogger(__name__)
log.setLevel(args.verbosity)


def main():
    log.info("")
    log.info(" =======================================")
    log.info(" \tPerforming SLDO analysis")
    log.info(" =======================================")
    log.info("")

    test_type = os.path.basename(__file__).split(".py")[0]

    # SLDO parameters
    RextA = get_nominal_RextA(args.layer)
    RextD = get_nominal_RextD(args.layer)

    allinputs = get_inputs(args.input_meas, test_type)

    output_dir = f"{args.output_dir}"
    timestart = round(datetime.timestamp(datetime.now()))
    os.makedirs(f"{output_dir}/{test_type}/{timestart}/")

    alloutput = []
    timestamps = []
    for filename in sorted(allinputs):
        log.info("")
        log.info(f" Loading {filename}")
        meas_timestamp = get_time_stamp(filename)
        inputDFs = load_json(filename)

        log.debug(
            f" There are results from {len(inputDFs)} chip(s) stored in this file"
        )
        for inputDF in inputDFs:
            qcframe = inputDF.get_results()
            metadata = qcframe.get_meta_data()

            try:
                kShuntA = (
                    metadata.get("ChipConfigs")
                    .get("RD53B")
                    .get("Parameter")
                    .get("KShuntA")
                )
                log.debug(f" Found kShuntA = {kShuntA} from chip config")
            except Exception:
                log.warning(
                    bcolors.WARNING
                    + " No KShuntA parameter found in chip metadata. Using default KShuntA = 1040"
                    + bcolors.ENDC
                )
                kShuntA = 1040

            try:
                kShuntD = (
                    metadata.get("ChipConfigs")
                    .get("RD53B")
                    .get("Parameter")
                    .get("KShuntD")
                )
                log.debug(f" Found kShuntD = {kShuntD} from chip config")
            except Exception:
                log.warning(
                    bcolors.WARNING
                    + " No KShuntD parameter found in chip metadata. Using default KShuntD = 1040"
                    + bcolors.ENDC
                )
                kShuntD = 1040.0

            try:
                chipname = metadata.get("Name")
                log.debug(f" Found chip name = {chipname} from chip config")
            except Exception:
                log.error(
                    bcolors.ERROR
                    + f" Chip name not found in input from {filename}, skipping."
                    + bcolors.ENDC
                )
                continue

            R_eff = 1.0 / ((kShuntA / RextA) + (kShuntD / RextD)) / args.nChips

            Vofs = get_nominal_Voffs(args.layer, args.lp_enable)

            p = np.poly1d([R_eff, Vofs])
            p1 = np.poly1d([R_eff, 0])

            """"" Check file integrity  """ ""
            checker = JsonChecker(inputDF, test_type)

            try:
                checker.check()
            except BaseException as exc:
                log.exception(exc)
                log.error(
                    bcolors.ERROR
                    + " JsonChecker check not passed, skipping this input."
                    + bcolors.ENDC
                )
                continue
            else:
                log.debug(" JsonChecker check passed!")
                pass

            """""  Calculate quanties   """ ""
            extractor = DataExtractor(inputDF, test_type)
            calculated_data = extractor.calculate()

            passes_qc = True

            # Plot parameters
            Iint_max = (
                max(
                    max(calculated_data["Iref"]["Values"] * 100000),
                    max(calculated_data["IcoreD"]["Values"]),
                    max(calculated_data["IcoreA"]["Values"]),
                    max(calculated_data["IshuntD"]["Values"]),
                    max(calculated_data["IshuntA"]["Values"]),
                    max(calculated_data["IinD"]["Values"]),
                    max(calculated_data["IinA"]["Values"]),
                )
                + 0.1
            )
            I_max = max(calculated_data["SetCurrent"]["Values"]) + 0.2
            V_max = max(
                max(calculated_data["VrefOVP"]["Values"]),
                max(calculated_data["Vofs"]["Values"]),
                max(calculated_data["VDDD"]["Values"]),
                max(calculated_data["VDDA"]["Values"]),
                max(calculated_data["VinD"]["Values"]),
                max(calculated_data["VinA"]["Values"]),
            )
            T_min = min(0.0, min(calculated_data["Temperature"]["Values"]))
            T_max = max(calculated_data["Temperature"]["Values"])

            # Internal voltages visualization
            fig, ax1 = plt.subplots()
            ax1.plot(
                calculated_data["SetCurrent"]["Values"],
                calculated_data["VinA"]["Values"],
                marker="o",
                markersize=4,
                label="VinA",
                color="tab:red",
            )
            ax1.plot(
                calculated_data["SetCurrent"]["Values"],
                calculated_data["VinD"]["Values"],
                marker="o",
                markersize=4,
                label="VinD",
                color="tab:red",
                linestyle="--",
            )
            ax1.plot(
                calculated_data["SetCurrent"]["Values"],
                calculated_data["VDDA"]["Values"],
                marker="o",
                markersize=4,
                label="VDDA",
                color="tab:blue",
            )
            ax1.plot(
                calculated_data["SetCurrent"]["Values"],
                calculated_data["VDDD"]["Values"],
                marker="o",
                markersize=4,
                label="VDDD",
                color="tab:blue",
                linestyle="--",
            )
            ax1.plot(
                calculated_data["SetCurrent"]["Values"],
                calculated_data["Vofs"]["Values"],
                marker="o",
                markersize=4,
                label="Vofs",
                color="tab:orange",
            )
            ax1.plot(
                calculated_data["SetCurrent"]["Values"],
                calculated_data["VrefOVP"]["Values"],
                marker="o",
                markersize=4,
                label="VrefOVP",
                color="tab:cyan",
            )

            xp = np.linspace(0, I_max, 1000)
            ax1.plot(
                xp,
                p(xp),
                label=f"V = {R_eff:.3f} I + {Vofs:.2f}",
                color="tab:brown",
                linestyle="dotted",
            )
            ax1.set_xlabel("I [A]")
            ax1.set_ylabel("V [V]")
            plt.title(f"VI curve for chip: {chipname}")
            plt.xlim(0, I_max)
            ax1.set_ylim(0.0, V_max)
            ax1.legend(loc="upper left", framealpha=0)
            plt.grid()

            ax2 = ax1.twinx()
            ax2.plot(
                calculated_data["SetCurrent"]["Values"],
                calculated_data["Temperature"]["Values"],
                marker="^",
                markersize=4,
                color="tab:green",
                label="Temperature (NTC)",
                linestyle="-.",
            )
            ax2.set_ylabel("T [C]")
            ax2.set_ylim(T_min, T_max)
            ax2.legend(loc="upper right", framealpha=0)

            plt.tight_layout()
            log.info(f" Saving {output_dir}/{test_type}/{timestart}/{chipname}_VI.png")
            plt.savefig(f"{output_dir}/{test_type}/{timestart}/{chipname}_VI.png")
            plt.clf()

            ax1.cla()
            ax2.cla()
            f = plt.figure()
            f.clear()
            plt.close(f)

            # Internal currents visualization
            fig, ax1 = plt.subplots()
            ax1.plot(
                calculated_data["SetCurrent"]["Values"],
                calculated_data["IinA"]["Values"],
                marker="o",
                markersize=4,
                label="IinA",
                color="tab:red",
            )
            ax1.plot(
                calculated_data["SetCurrent"]["Values"],
                calculated_data["IinD"]["Values"],
                marker="o",
                markersize=4,
                label="IinD",
                color="tab:red",
                linestyle="--",
            )
            ax1.plot(
                calculated_data["SetCurrent"]["Values"],
                calculated_data["IshuntA"]["Values"],
                marker="o",
                markersize=4,
                label="IshuntA",
                color="tab:blue",
            )
            ax1.plot(
                calculated_data["SetCurrent"]["Values"],
                calculated_data["IshuntD"]["Values"],
                marker="o",
                markersize=4,
                label="IshuntD",
                color="tab:blue",
                linestyle="--",
            )
            ax1.plot(
                calculated_data["SetCurrent"]["Values"],
                calculated_data["IcoreA"]["Values"],
                marker="o",
                markersize=4,
                label="IcoreA",
                color="tab:orange",
            )
            ax1.plot(
                calculated_data["SetCurrent"]["Values"],
                calculated_data["IcoreD"]["Values"],
                marker="o",
                markersize=4,
                label="IcoreD",
                color="tab:orange",
                linestyle="--",
            )
            ax1.plot(
                calculated_data["SetCurrent"]["Values"],
                calculated_data["Iref"]["Values"] * 100000,
                marker="o",
                markersize=4,
                label="Iref*100k",
                color="tab:cyan",
            )
            ax1.set_xlabel("I [A]")
            ax1.set_ylabel("I [A]")
            plt.title(f"Currents for chip: {chipname}")

            plt.xlim(0, I_max)
            plt.ylim(0.0, Iint_max)
            ax1.legend(loc="upper left", framealpha=0)
            plt.grid()

            ax2 = ax1.twinx()
            ax2.plot(
                calculated_data["SetCurrent"]["Values"],
                calculated_data["Temperature"]["Values"],
                marker="^",
                markersize=4,
                color="tab:green",
                label="Temperature (NTC)",
                linestyle="-.",
            )
            ax2.set_ylabel("T [C]")
            ax2.set_ylim(T_min, T_max)
            ax2.legend(loc="upper right", framealpha=0)

            plt.tight_layout()
            log.info(f" Saving {output_dir}/{test_type}/{timestart}/{chipname}_II.png")
            plt.savefig(f"{output_dir}/{test_type}/{timestart}/{chipname}_II.png")
            plt.clf()

            ax1.cla()
            ax2.cla()
            f = plt.figure()
            f.clear()
            plt.close(f)

            # SLDO fit
            VinAvg = (
                calculated_data["VinA"]["Values"] + calculated_data["VinD"]["Values"]
            ) / 2.0
            if args.fit_method == "root":
                slope, offset = linear_fit(
                    calculated_data["SetCurrent"]["Values"], VinAvg
                )
            else:
                slope, offset = linear_fit_np(
                    calculated_data["SetCurrent"]["Values"], VinAvg
                )

            # Residual analysis
            residual_VinA = (
                p1(calculated_data["SetCurrent"]["Values"])
                - (
                    calculated_data["VinD"]["Values"]
                    - calculated_data["Vofs"]["Values"]
                )
            ) * 1000
            residual_VinD = (
                p1(calculated_data["SetCurrent"]["Values"])
                - (
                    calculated_data["VinD"]["Values"]
                    - calculated_data["Vofs"]["Values"]
                )
            ) * 1000
            residual_Vin = p1(calculated_data["SetCurrent"]["Values"]) - (
                VinAvg - calculated_data["Vofs"]["Values"]
            )
            residual_Vofs = (Vofs - calculated_data["Vofs"]["Values"]) * 1000
            # residual_Iref = (
            #    4.0 - calculated_data["Iref"]["Values"] * 1000000
            # )  # To-do: remove hardcode here

            plt.plot(
                calculated_data["SetCurrent"]["Values"],
                (
                    p(calculated_data["SetCurrent"]["Values"])
                    - calculated_data["VinA"]["Values"]
                )
                * 1000,
                marker="o",
                markersize=4,
                label=f"{R_eff:.3f}I+{Vofs:.2f}-VinA",
                color="tab:red",
            )
            plt.plot(
                calculated_data["SetCurrent"]["Values"],
                (
                    p(calculated_data["SetCurrent"]["Values"])
                    - calculated_data["VinD"]["Values"]
                )
                * 1000,
                marker="o",
                markersize=4,
                label=f"{R_eff:.3f}I+{Vofs:.2f}-VinD",
                color="tab:red",
                linestyle="--",
            )
            plt.plot(
                calculated_data["SetCurrent"]["Values"],
                residual_VinA,
                marker="o",
                markersize=4,
                label=f"{R_eff:.3f}I+Vofs-VinA",
                color="tab:blue",
            )
            plt.plot(
                calculated_data["SetCurrent"]["Values"],
                residual_VinD,
                marker="o",
                markersize=4,
                label=f"{R_eff:.3f}I+Vofs-VinD",
                color="tab:blue",
                linestyle="--",
            )
            plt.plot(
                calculated_data["SetCurrent"]["Values"],
                residual_Vofs,
                marker="o",
                markersize=4,
                label=f"{Vofs}-Vofs",
                color="tab:orange",
            )
            plt.xlabel("I [A]")
            plt.ylabel("V [mV]")
            plt.title(f"VI curve for chip: {chipname}")
            plt.xlim(0, I_max)
            plt.ylim(-30.0, 100)
            plt.legend(loc="upper right", framealpha=0)
            plt.grid()
            plt.tight_layout()
            log.info(
                f" Saving {output_dir}/{test_type}/{timestart}/{chipname}_VIresidual.png"
            )
            plt.savefig(
                f"{output_dir}/{test_type}/{timestart}/{chipname}_VIresidual.png"
            )
            plt.clf()

            f = plt.figure()
            f.clear()
            plt.close(f)

            # Find point measured closest to nominal input current
            sldo_nom_input_current = get_nominal_current(args.layer)
            log.debug(f" Calculated nominal current to be: {sldo_nom_input_current}")
            idx = (
                np.abs(calculated_data["SetCurrent"]["Values"] - sldo_nom_input_current)
            ).argmin()
            log.debug(
                f' Closest current measured to nominal is: {calculated_data["SetCurrent"]["Values"][idx]}'
            )

            # Load values to dictionary for QC analysis
            results = {}
            results.update({"SLDOLinearity": max(residual_Vin)})
            results.update(
                {
                    "VInA_VInD": max(
                        abs(
                            calculated_data["VinA"]["Values"]
                            - calculated_data["VinD"]["Values"]
                        )
                    )
                }
            )
            results.update({"SLDO_VDDA": calculated_data["VDDA"]["Values"][idx]})
            results.update({"SLDO_VDDD": calculated_data["VDDD"]["Values"][idx]})
            results.update({"SLDO_VINA": calculated_data["VinA"]["Values"][idx]})
            results.update({"SLDO_VIND": calculated_data["VinD"]["Values"][idx]})
            results.update({"SLDO_VOFFS": calculated_data["Vofs"]["Values"][idx]})
            results.update({"SLDO_IINA": calculated_data["IinA"]["Values"][idx]})
            results.update({"SLDO_IIND": calculated_data["IinD"]["Values"][idx]})
            results.update({"SLDO_IREF": calculated_data["Iref"]["Values"][idx] * 1e6})
            results.update({"SLDO_ISHUNTA": calculated_data["IshuntA"]["Values"][idx]})
            results.update({"SLDO_ISHUNTD": calculated_data["IshuntD"]["Values"][idx]})

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

            """"" Output a json file """ ""
            outputDF = outputDataFrame()
            outputDF.set_test_type(test_type)
            data = qcDataFrame()
            data._meta_data.update(metadata)
            data.add_property(
                "ANALYSIS_VERSION",
                pkg_resources.get_distribution("module-qc-analysis-tools").version,
            )
            # Load values to store in output file
            analog_overhead = calculated_data["IshuntA"]["Values"][idx] / (
                calculated_data["IinA"]["Values"][idx]
                - calculated_data["IshuntA"]["Values"][idx]
            )
            digital_overhead = calculated_data["IshuntD"]["Values"][idx] / (
                calculated_data["IinD"]["Values"][idx]
                - calculated_data["IshuntD"]["Values"][idx]
            )
            data.add_parameter("SLDO_VI_SLOPE", round(slope, 4))
            data.add_parameter("SLDO_VI_OFFSET", round(offset, 4))
            data.add_parameter(
                "SLDO_NOM_INPUT_CURRENT", round(sldo_nom_input_current, 4)
            )
            data.add_parameter(
                "SLDO_VDDA", round(calculated_data["VDDA"]["Values"][idx], 4)
            )
            data.add_parameter(
                "SLDO_VDDD", round(calculated_data["VDDD"]["Values"][idx], 4)
            )
            data.add_parameter(
                "SLDO_VINA", round(calculated_data["VinA"]["Values"][idx], 4)
            )
            data.add_parameter(
                "SLDO_VIND", round(calculated_data["VinD"]["Values"][idx], 4)
            )
            data.add_parameter(
                "SLDO_VOFFS", round(calculated_data["Vofs"]["Values"][idx], 4)
            )
            data.add_parameter(
                "SLDO_IINA", round(calculated_data["IinA"]["Values"][idx], 4)
            )
            data.add_parameter(
                "SLDO_IIND", round(calculated_data["IinD"]["Values"][idx], 4)
            )
            data.add_parameter(
                "SLDO_IREF", round(calculated_data["Iref"]["Values"][idx] * 1e6, 4)
            )
            data.add_parameter(
                "SLDO_ISHUNTA", round(calculated_data["IshuntA"]["Values"][idx], 4)
            )
            data.add_parameter(
                "SLDO_ISHUNTD", round(calculated_data["IshuntD"]["Values"][idx], 4)
            )
            data.add_parameter("SLDO_ANALOG_OVERHEAD", round(analog_overhead, 4))
            data.add_parameter("SLDO_DIGITAL_OVERHEAD", round(digital_overhead, 4))

            outputDF.set_results(data)
            outputDF.set_pass_flag(passes_qc)
            if args.permodule:
                alloutput += [outputDF.to_dict(True)]
                timestamps += [meas_timestamp]
            else:
                outfile = f"{output_dir}/{test_type}/{timestart}/{chipname}.json"
                log.info(
                    f" Saving output of analysis to: {output_dir}/{test_type}/{timestart}/{chipname}.json"
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
