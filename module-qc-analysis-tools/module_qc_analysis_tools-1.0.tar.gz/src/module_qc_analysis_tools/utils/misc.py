#!/usr/bin/env python3
import glob
import logging
import os

import numpy as np

log = logging.getLogger(__name__)
log.setLevel("INFO")


class JsonFileCheckFailure(Exception):
    pass


class LengthMismatchError(Exception):
    pass


class NegativeMeasurementError(Exception):
    pass


class bcolors:
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    ERROR = "\033[91m"
    BADRED = "\033[91m"
    ENDC = "\033[0m"


def getVmuxMap():
    Vmux_map = {
        0: "GADC",
        1: "ImuxPad",
        2: "Vntc",
        3: "VcalDac",
        4: "VDDAcapmeas",
        5: "VPolSensTop",
        6: "VPolSensBottom",
        7: "VcalHi",
        8: "VcalMed",
        9: "VDiffVTH2",
        10: "VDiffVTH1Main",
        11: "VDiffVTH1Left",
        12: "VDiffVTH1Right",
        13: "VRadSensAna",
        14: "VMonSensAna",
        15: "VRadSensDig",
        16: "VMonSensDig",
        17: "VRadSensCenter",
        18: "VMonSensAcb",
        19: "AnaGND19",
        20: "AnaGND20",
        21: "AnaGND21",
        22: "AnaGND22",
        23: "AnaGND23",
        24: "AnaGND24",
        25: "AnaGND25",
        26: "AnaGND26",
        27: "AnaGND27",
        28: "AnaGND28",
        29: "AnaGND29",
        30: "AnaGND30",
        31: "VrefCore",
        32: "VrefOVP",
        33: "VinA",
        34: "VDDA",
        35: "VrefA",
        36: "Vofs",
        37: "VinD",
        38: "VDDD",
        39: "VrefD",
    }

    return Vmux_map


def getImuxMap():
    Imux_map = {
        0: "Iref",
        1: "CdrVcoMainBias",
        2: "CdrVcoBuffBias",
        3: "ICdrCP",
        4: "ICdrFD",
        5: "CdrBuffBias",
        6: "CMLDrivTap2Bias",
        7: "CMLDrivTap1Bias",
        8: "CMLDrivMainBias",
        9: "Intc",
        10: "CapMeas",
        11: "CapMeasPar",
        12: "IDiffPreMain",
        13: "IDiffPreampComp",
        14: "IDiffComp",
        15: "IDiffVth2",
        16: "IDiffVth1Main",
        17: "IDiffLcc",
        18: "IDiffFB",
        19: "IDiffPreampLeft",
        20: "IDiffVth1Left",
        21: "IDiffPreampRight",
        22: "IDiffPreampTopLeft",
        23: "IDiffVth1Right",
        24: "IDiffPreampTop",
        25: "IDiffPreampTopRight",
        26: "NotUsed26",
        27: "NotUsed27",
        28: "IinA",
        29: "IshuntA",
        30: "IinD",
        31: "IshuntD",
    }
    return Imux_map


class JsonChecker:
    def __init__(self, inputDF, test_type_from_script) -> None:
        # init all available qc types
        self.qc_type = test_type_from_script
        self.inputdataframe = inputDF
        self.qcdataframe = inputDF.get_results()

        self.dict_map = {
            "VCAL_CALIBRATION": {
                "VCAL_HIGH": {
                    "required_keys": ["DACs_input", "Vmux30", "Vmux7"],
                    "InjVcalRange": 1,
                    "MonitorV": 7,
                },
                "VCAL_HIGH_SMALL_RANGE": {
                    "required_keys": ["DACs_input", "Vmux30", "Vmux7"],
                    "InjVcalRange": 0,
                    "MonitorV": 7,
                },
                "VCAL_MED": {
                    "required_keys": ["DACs_input", "Vmux30", "Vmux8"],
                    "InjVcalRange": 1,
                    "MonitorV": 8,
                },
                "VCAL_MED_SMALL_RANGE": {
                    "required_keys": ["DACs_input", "Vmux30", "Vmux8"],
                    "InjVcalRange": 0,
                    "MonitorV": 8,
                },
            },
            "ADC_CALIBRATION": {
                "required_keys": ["DACs_input", "ADC_Vmux8", "Vmux30", "Vmux8"],
                "InjVcalRange": 1,
            },
            "SLDO": {
                "required_keys": [
                    "Temperature",
                    "Current",
                    "Vmux30",
                    "Vmux33",
                    "Vmux37",
                    "Vmux34",
                    "Vmux38",
                    "Vmux36",
                    "Vmux32",
                    "Imux0",
                    "Imux28",
                    "Imux29",
                    "Imux30",
                    "Imux31",
                    "Imux63",
                ]
            },
            "INJECTION_CAPACITANCE": {
                "required_keys": ["Vmux4", "Vmux30", "Imux10", "Imux11", "Imux63"]
            },
            "ANALOG_READBACK": {
                "AR_VMEAS": {
                    "required_keys": [
                        "Vmux30",
                        "Vmux33",
                        "Vmux34",
                        "Vmux35",
                        "Vmux36",
                        "Vmux37",
                        "Vmux38",
                        "Imux28",
                        "Imux29",
                        "Imux30",
                        "Imux31",
                        "Imux63",
                    ],
                },
                "AR_TEMP": {
                    "required_keys": [
                        "Vmux14",
                        "Vmux16",
                        "Vmux18",
                        "Vmux2",
                        "Vmux30",
                        "Imux9",
                        "Imux63",
                        "TExtExtNTC",
                    ],
                },
                "AR_VDD": {
                    "required_keys": [
                        "Vmux34",
                        "Vmux38",
                        "Vmux30",
                    ],
                },
            },
        }

    def check_testtype(self):
        if self.inputdataframe._subtestType != "":
            self.sub_test_type = self.inputdataframe._subtestType
            required_testtype = self.qc_type
            self.required_keywords = self.dict_map[self.qc_type][self.sub_test_type][
                "required_keys"
            ]
        else:
            required_testtype = self.qc_type
            self.required_keywords = self.dict_map[self.qc_type]["required_keys"]

        testtype_from_file = self.inputdataframe._testType
        if not required_testtype == testtype_from_file:
            raise KeyError(
                f'Required testtype of the file "{required_testtype}" is not matched to "{testtype_from_file}" from the file! '
            )

    def check_keywords_exist(self) -> None:
        for required_keyword in self.required_keywords:
            if required_keyword not in self.qcdataframe._data.keys():
                raise KeyError(f"{required_keyword} not found! ")

    def check_keywords_length(self) -> None:
        """Check whether the length of measurements are same."""
        first_keyword = True
        for required_keyword in self.required_keywords:
            if first_keyword:
                len_x = len(self.qcdataframe[required_keyword])
                self.var_x = required_keyword
                first_keyword = False
            if self.qcdataframe.get_x(required_keyword) is True:
                len_x = len(self.qcdataframe[required_keyword])
                self.var_x = required_keyword

        for required_keyword in self.required_keywords:
            if len_x != len(self.qcdataframe[required_keyword]):
                raise LengthMismatchError(
                    f"The length of {required_keyword} is not equal to {self.var_x}!"
                )

    def check_positive_values(self) -> None:
        """Check whether the contents of measurements are valid, i.e. all positive."""
        for required_keyword in self.required_keywords:
            if ((self.qcdataframe[required_keyword]) < 0).sum() > 0:
                raise NegativeMeasurementError(
                    f"Negative measurements observed in {required_keyword}"
                )

    def check_parameters_overwritten(self) -> None:
        """Check whether the parameters are overwritten correctly."""
        if self.inputdataframe._subtestType != "":
            parameters_to_check = self.dict_map[self.qc_type][self.sub_test_type].copy()
        else:
            parameters_to_check = self.dict_map[self.qc_type].copy()

        parameters_to_check.pop("required_keys")

        for k, v in parameters_to_check.items():
            value_from_file = lookup(self.qcdataframe._meta_data, k)
            if value_from_file is None:
                raise KeyError(
                    f"Measurement output file Corrupted! Please check this key: {k}"
                )
            if v != value_from_file:
                raise KeyError(
                    f"Values Mismathed for this key {k}: {value_from_file} from file, but required {v} "
                )

    def check(self) -> None:
        self.check_testtype()
        self.check_keywords_exist()
        self.check_keywords_length()
        self.check_positive_values()
        self.check_parameters_overwritten()


class DataExtractor(JsonChecker):
    def __init__(self, inputDF, test_type_from_script) -> None:
        super().__init__(inputDF, test_type_from_script)
        qcframe = inputDF.get_results()
        self.df = qcframe._data
        self.rImux = qcframe._meta_data["ChipConfigs"]["RD53B"]["Parameter"].get(
            "R_Imux", 10000.0
        )
        self.kIinA = qcframe._meta_data["ChipConfigs"]["RD53B"]["Parameter"].get(
            "kIinA", 21000.0
        )
        self.kIinD = qcframe._meta_data["ChipConfigs"]["RD53B"]["Parameter"].get(
            "kIinD", 21000.0
        )
        self.kIshuntA = qcframe._meta_data["ChipConfigs"]["RD53B"]["Parameter"].get(
            "kIshuntA", 26000.0
        )
        self.kIshuntD = qcframe._meta_data["ChipConfigs"]["RD53B"]["Parameter"].get(
            "kIshuntD", 26000.0
        )
        self.VmuxGrd = "Vmux30"
        self.ImuxGrd = "Imux63"

    def getQuantity(self, key):
        return getattr(self, key, lambda: False)()

    def Vmux0(self):
        return {
            getVmuxMap()[0]: {
                "X": self.df["Vmux0"]["X"],
                "Unit": self.df["Vmux0"]["Unit"],
                "Values": (
                    self.df["Vmux0"]["Values"] - self.df[self.VmuxGrd]["Values"]
                ),
            }
        }

    def Vmux2(self):
        return {
            getVmuxMap()[2]: {
                "X": self.df["Vmux2"]["X"],
                "Unit": self.df["Vmux2"]["Unit"],
                "Values": (
                    self.df["Vmux2"]["Values"] - self.df[self.VmuxGrd]["Values"]
                ),
            }
        }

    def Vmux3(self):
        return {
            getVmuxMap()[3]: {
                "X": self.df["Vmux3"]["X"],
                "Unit": self.df["Vmux3"]["Unit"],
                "Values": (self.df["Vmux3"]["Values"] - self.df[self.VmuxGrd]["Values"])
                * 2,
            }
        }

    def Vmux4(self):
        return {
            getVmuxMap()[4]: {
                "X": self.df["Vmux4"]["X"],
                "Unit": self.df["Vmux4"]["Unit"],
                "Values": (self.df["Vmux4"]["Values"] - self.df[self.VmuxGrd]["Values"])
                * 2,
            }
        }

    def Vmux5(self):
        return {
            getVmuxMap()[5]: {
                "X": self.df["Vmux5"]["X"],
                "Unit": self.df["Vmux5"]["Unit"],
                "Values": self.df["Vmux5"]["Values"] - self.df[self.VmuxGrd]["Values"],
            }
        }

    def Vmux6(self):
        return {
            getVmuxMap()[6]: {
                "X": self.df["Vmux6"]["X"],
                "Unit": self.df["Vmux6"]["Unit"],
                "Values": self.df["Vmux6"]["Values"] - self.df[self.VmuxGrd]["Values"],
            }
        }

    def Vmux7(self):
        return {
            getVmuxMap()[7]: {
                "X": self.df["Vmux7"]["X"],
                "Unit": self.df["Vmux7"]["Unit"],
                "Values": self.df["Vmux7"]["Values"] - self.df[self.VmuxGrd]["Values"],
            }
        }

    def Vmux8(self):
        return {
            getVmuxMap()[8]: {
                "X": self.df["Vmux8"]["X"],
                "Unit": self.df["Vmux8"]["Unit"],
                "Values": self.df["Vmux8"]["Values"] - self.df[self.VmuxGrd]["Values"],
            }
        }

    def Vmux9(self):
        return {
            getVmuxMap()[9]: {
                "X": self.df["Vmux9"]["X"],
                "Unit": self.df["Vmux9"]["Unit"],
                "Values": self.df["Vmux9"]["Values"] - self.df[self.VmuxGrd]["Values"],
            }
        }

    def Vmux10(self):
        return {
            getVmuxMap()[10]: {
                "X": self.df["Vmux10"]["X"],
                "Unit": self.df["Vmux10"]["Unit"],
                "Values": self.df["Vmux10"]["Values"] - self.df[self.VmuxGrd]["Values"],
            }
        }

    def Vmux11(self):
        return {
            getVmuxMap()[11]: {
                "X": self.df["Vmux11"]["X"],
                "Unit": self.df["Vmux11"]["Unit"],
                "Values": self.df["Vmux11"]["Values"] - self.df[self.VmuxGrd]["Values"],
            }
        }

    def Vmux12(self):
        return {
            getVmuxMap()[12]: {
                "X": self.df["Vmux12"]["X"],
                "Unit": self.df["Vmux12"]["Unit"],
                "Values": self.df["Vmux12"]["Values"] - self.df[self.VmuxGrd]["Values"],
            }
        }

    def Vmux13(self):
        return {
            getVmuxMap()[13]: {
                "X": self.df["Vmux13"]["X"],
                "Unit": self.df["Vmux13"]["Unit"],
                "Values": self.df["Vmux13"]["Values"] - self.df[self.VmuxGrd]["Values"],
            }
        }

    def Vmux14(self):
        return {
            getVmuxMap()[14]: {
                "X": self.df["Vmux14"]["X"],
                "Unit": self.df["Vmux14"]["Unit"],
                "Values": self.df["Vmux14"]["Values"] - self.df[self.VmuxGrd]["Values"],
            }
        }

    def Vmux15(self):
        return {
            getVmuxMap()[15]: {
                "X": self.df["Vmux15"]["X"],
                "Unit": self.df["Vmux15"]["Unit"],
                "Values": self.df["Vmux15"]["Values"] - self.df[self.VmuxGrd]["Values"],
            }
        }

    def Vmux16(self):
        return {
            getVmuxMap()[16]: {
                "X": self.df["Vmux16"]["X"],
                "Unit": self.df["Vmux16"]["Unit"],
                "Values": self.df["Vmux16"]["Values"] - self.df[self.VmuxGrd]["Values"],
            }
        }

    def Vmux17(self):
        return {
            getVmuxMap()[17]: {
                "X": self.df["Vmux17"]["X"],
                "Unit": self.df["Vmux17"]["Unit"],
                "Values": self.df["Vmux17"]["Values"] - self.df[self.VmuxGrd]["Values"],
            }
        }

    def Vmux18(self):
        return {
            getVmuxMap()[18]: {
                "X": self.df["Vmux18"]["X"],
                "Unit": self.df["Vmux18"]["Unit"],
                "Values": self.df["Vmux18"]["Values"] - self.df[self.VmuxGrd]["Values"],
            }
        }

    def Vmux30(self):
        return {
            getVmuxMap()[30]: {
                "X": self.df["Vmux30"]["X"],
                "Unit": self.df["Vmux30"]["Unit"],
                "Values": self.df["Vmux30"]["Values"],
            }
        }

    def Vmux31(self):
        return {
            getVmuxMap()[31]: {
                "X": self.df["Vmux31"]["X"],
                "Unit": self.df["Vmux31"]["Unit"],
                "Values": self.df["Vmux31"]["Values"] - self.df[self.VmuxGrd]["Values"],
            }
        }

    def Vmux32(self):
        return {
            getVmuxMap()[32]: {
                "X": self.df["Vmux32"]["X"],
                "Unit": self.df["Vmux32"]["Unit"],
                "Values": (
                    self.df["Vmux32"]["Values"] - self.df[self.VmuxGrd]["Values"]
                )
                * 3.33,
            }
        }

    def Vmux33(self):
        return {
            getVmuxMap()[33]: {
                "X": self.df["Vmux33"]["X"],
                "Unit": self.df["Vmux33"]["Unit"],
                "Values": (
                    self.df["Vmux33"]["Values"] - self.df[self.VmuxGrd]["Values"]
                )
                * 4,
            }
        }

    def Vmux34(self):
        return {
            getVmuxMap()[34]: {
                "X": self.df["Vmux34"]["X"],
                "Unit": self.df["Vmux34"]["Unit"],
                "Values": (
                    self.df["Vmux34"]["Values"] - self.df[self.VmuxGrd]["Values"]
                )
                * 2,
            }
        }

    def Vmux35(self):
        return {
            getVmuxMap()[35]: {
                "X": self.df["Vmux35"]["X"],
                "Unit": self.df["Vmux35"]["Unit"],
                "Values": (
                    self.df["Vmux35"]["Values"] - self.df[self.VmuxGrd]["Values"]
                ),
            }
        }

    def Vmux36(self):
        return {
            getVmuxMap()[36]: {
                "X": self.df["Vmux36"]["X"],
                "Unit": self.df["Vmux36"]["Unit"],
                "Values": (
                    self.df["Vmux36"]["Values"] - self.df[self.VmuxGrd]["Values"]
                )
                * 4,
            }
        }

    def Vmux37(self):
        return {
            getVmuxMap()[37]: {
                "X": self.df["Vmux37"]["X"],
                "Unit": self.df["Vmux37"]["Unit"],
                "Values": (
                    self.df["Vmux37"]["Values"] - self.df[self.VmuxGrd]["Values"]
                )
                * 4,
            }
        }

    def Vmux38(self):
        return {
            getVmuxMap()[38]: {
                "X": self.df["Vmux38"]["X"],
                "Unit": self.df["Vmux38"]["Unit"],
                "Values": (
                    self.df["Vmux38"]["Values"] - self.df[self.VmuxGrd]["Values"]
                )
                * 2,
            }
        }

    def Vmux39(self):
        return {
            getVmuxMap()[39]: {
                "X": self.df["Vmux39"]["X"],
                "Unit": self.df["Vmux39"]["Unit"],
                "Values": (
                    self.df["Vmux39"]["Values"] - self.df[self.VmuxGrd]["Values"]
                ),
            }
        }

    def Imux0(self):
        return {
            getImuxMap()[0]: {
                "X": self.df["Imux0"]["X"],
                "Unit": "A",
                "Values": (self.df["Imux0"]["Values"] - self.df[self.ImuxGrd]["Values"])
                / self.rImux,
            }
        }

    def Imux1(self):
        return {
            getImuxMap()[1]: {
                "X": self.df["Imux1"]["X"],
                "Unit": "A",
                "Values": (self.df["Imux1"]["Values"] - self.df[self.ImuxGrd]["Values"])
                / self.rImux,
            }
        }

    def Imux2(self):
        return {
            getImuxMap()[2]: {
                "X": self.df["Imux2"]["X"],
                "Unit": "A",
                "Values": (self.df["Imux2"]["Values"] - self.df[self.ImuxGrd]["Values"])
                / self.rImux,
            }
        }

    def Imux3(self):
        return {
            getImuxMap()[3]: {
                "X": self.df["Imux3"]["X"],
                "Unit": "A",
                "Values": (self.df["Imux3"]["Values"] - self.df[self.ImuxGrd]["Values"])
                / self.rImux,
            }
        }

    def Imux4(self):
        return {
            getImuxMap()[4]: {
                "X": self.df["Imux4"]["X"],
                "Unit": "A",
                "Values": (self.df["Imux4"]["Values"] - self.df[self.ImuxGrd]["Values"])
                / self.rImux,
            }
        }

    def Imux5(self):
        return {
            getImuxMap()[5]: {
                "X": self.df["Imux5"]["X"],
                "Unit": "A",
                "Values": (self.df["Imux5"]["Values"] - self.df[self.ImuxGrd]["Values"])
                / self.rImux,
            }
        }

    def Imux6(self):
        return {
            getImuxMap()[6]: {
                "X": self.df["Imux6"]["X"],
                "Unit": "A",
                "Values": (self.df["Imux6"]["Values"] - self.df[self.ImuxGrd]["Values"])
                / self.rImux,
            }
        }

    def Imux7(self):
        return {
            getImuxMap()[7]: {
                "X": self.df["Imux7"]["X"],
                "Unit": "A",
                "Values": (self.df["Imux7"]["Values"] - self.df[self.ImuxGrd]["Values"])
                / self.rImux,
            }
        }

    def Imux8(self):
        return {
            getImuxMap()[8]: {
                "X": self.df["Imux8"]["X"],
                "Unit": "A",
                "Values": (self.df["Imux8"]["Values"] - self.df[self.ImuxGrd]["Values"])
                / self.rImux,
            }
        }

    def Imux9(self):
        return {
            getImuxMap()[9]: {
                "X": self.df["Imux9"]["X"],
                "Unit": "A",
                "Values": (self.df["Imux9"]["Values"] - self.df[self.ImuxGrd]["Values"])
                / self.rImux,
            }
        }

    def Imux10(self):
        return {
            getImuxMap()[10]: {
                "X": self.df["Imux10"]["X"],
                "Unit": "A",
                "Values": (
                    self.df["Imux10"]["Values"] - self.df[self.ImuxGrd]["Values"]
                )
                / self.rImux,
            }
        }

    def Imux11(self):
        return {
            getImuxMap()[11]: {
                "X": self.df["Imux11"]["X"],
                "Unit": "A",
                "Values": (
                    self.df["Imux11"]["Values"] - self.df[self.ImuxGrd]["Values"]
                )
                / self.rImux,
            }
        }

    def Imux12(self):
        return {
            getImuxMap()[12]: {
                "X": self.df["Imux12"]["X"],
                "Unit": "A",
                "Values": (
                    self.df["Imux12"]["Values"] - self.df[self.ImuxGrd]["Values"]
                )
                / self.rImux,
            }
        }

    def Imux13(self):
        return {
            getImuxMap()[13]: {
                "X": self.df["Imux13"]["X"],
                "Unit": "A",
                "Values": (
                    self.df["Imux13"]["Values"] - self.df[self.ImuxGrd]["Values"]
                )
                / self.rImux,
            }
        }

    def Imux14(self):
        return {
            getImuxMap()[14]: {
                "X": self.df["Imux14"]["X"],
                "Unit": "A",
                "Values": (
                    self.df["Imux14"]["Values"] - self.df[self.ImuxGrd]["Values"]
                )
                / self.rImux,
            }
        }

    def Imux15(self):
        return {
            getImuxMap()[15]: {
                "X": self.df["Imux15"]["X"],
                "Unit": "A",
                "Values": (
                    self.df["Imux15"]["Values"] - self.df[self.ImuxGrd]["Values"]
                )
                / self.rImux,
            }
        }

    def Imux16(self):
        return {
            getImuxMap()[16]: {
                "X": self.df["Imux16"]["X"],
                "Unit": "A",
                "Values": (
                    self.df["Imux16"]["Values"] - self.df[self.ImuxGrd]["Values"]
                )
                / self.rImux,
            }
        }

    def Imux17(self):
        return {
            getImuxMap()[17]: {
                "X": self.df["Imux17"]["X"],
                "Unit": "A",
                "Values": (
                    self.df["Imux17"]["Values"] - self.df[self.ImuxGrd]["Values"]
                )
                / self.rImux,
            }
        }

    def Imux18(self):
        return {
            getImuxMap()[18]: {
                "X": self.df["Imux18"]["X"],
                "Unit": "A",
                "Values": (
                    self.df["Imux18"]["Values"] - self.df[self.ImuxGrd]["Values"]
                )
                / self.rImux,
            }
        }

    def Imux19(self):
        return {
            getImuxMap()[19]: {
                "X": self.df["Imux15"]["X"],
                "Unit": "A",
                "Values": (
                    self.df["Imux15"]["Values"] - self.df[self.ImuxGrd]["Values"]
                )
                / self.rImux,
            }
        }

    def Imux20(self):
        return {
            getImuxMap()[20]: {
                "X": self.df["Imux20"]["X"],
                "Unit": "A",
                "Values": (
                    self.df["Imux20"]["Values"] - self.df[self.ImuxGrd]["Values"]
                )
                / self.rImux,
            }
        }

    def Imux21(self):
        return {
            getImuxMap()[21]: {
                "X": self.df["Imux21"]["X"],
                "Unit": "A",
                "Values": (
                    self.df["Imux21"]["Values"] - self.df[self.ImuxGrd]["Values"]
                )
                / self.rImux,
            }
        }

    def Imux22(self):
        return {
            getImuxMap()[22]: {
                "X": self.df["Imux22"]["X"],
                "Unit": "A",
                "Values": (
                    self.df["Imux22"]["Values"] - self.df[self.ImuxGrd]["Values"]
                )
                / self.rImux,
            }
        }

    def Imux23(self):
        return {
            getImuxMap()[23]: {
                "X": self.df["Imux23"]["X"],
                "Unit": "A",
                "Values": (
                    self.df["Imux23"]["Values"] - self.df[self.ImuxGrd]["Values"]
                )
                / self.rImux,
            }
        }

    def Imux24(self):
        return {
            getImuxMap()[24]: {
                "X": self.df["Imux24"]["X"],
                "Unit": "A",
                "Values": (
                    self.df["Imux24"]["Values"] - self.df[self.ImuxGrd]["Values"]
                )
                / self.rImux,
            }
        }

    def Imux25(self):
        return {
            getImuxMap()[25]: {
                "X": self.df["Imux25"]["X"],
                "Unit": "A",
                "Values": (
                    self.df["Imux25"]["Values"] - self.df[self.ImuxGrd]["Values"]
                )
                / self.rImux,
            }
        }

    def Imux28(self):
        return {
            getImuxMap()[28]: {
                "X": self.df["Imux28"]["X"],
                "Unit": "A",
                "Values": (
                    self.df["Imux28"]["Values"] - self.df[self.ImuxGrd]["Values"]
                )
                / self.rImux
                * self.kIinA,
            }
        }

    def Imux29(self):
        return {
            getImuxMap()[29]: {
                "X": self.df["Imux29"]["X"],
                "Unit": "A",
                "Values": (
                    self.df["Imux29"]["Values"] - self.df[self.ImuxGrd]["Values"]
                )
                / self.rImux
                * self.kIinD,
            }
        }

    def Imux30(self):
        return {
            getImuxMap()[30]: {
                "X": self.df["Imux30"]["X"],
                "Unit": "A",
                "Values": (
                    self.df["Imux30"]["Values"] - self.df[self.ImuxGrd]["Values"]
                )
                / self.rImux
                * self.kIshuntA,
            }
        }

    def Imux31(self):
        return {
            getImuxMap()[31]: {
                "X": self.df["Imux31"]["X"],
                "Unit": "A",
                "Values": (
                    self.df["Imux31"]["Values"] - self.df[self.ImuxGrd]["Values"]
                )
                / self.rImux
                * self.kIshuntD,
            }
        }

    def IcoreA(self):
        return {
            "IcoreA": {
                "X": False,
                "Unit": "A",
                "Values": self.df["IinA"]["Values"] - self.df["IshuntA"]["Values"],
            }
        }

    def IcoreD(self):
        return {
            "IcoreD": {
                "X": False,
                "Unit": "A",
                "Values": self.df["IinD"]["Values"] - self.df["IshuntD"]["Values"],
            }
        }

    def Iin(self):
        return {
            "Iin": {
                "X": False,
                "Unit": "A",
                "Values": self.df["IinA"]["Values"] + self.df["IinD"]["Values"],
            }
        }

    def calculate(self):

        # Convert values from list to numpy array
        for key, value in self.df.items():
            self.df.update(
                {
                    key: {
                        "X": value["X"],
                        "Unit": value["Unit"],
                        "Values": np.array(value["Values"]),
                    }
                }
            )

        df_keys = self.df.copy().keys()

        # Calculate basic quantities
        for key in df_keys:
            newQuantity = self.getQuantity(key)
            if newQuantity:
                self.df.update(newQuantity)

        # Calculated complex quantities
        if self.df.get("IinA") and self.df.get("IshuntA"):
            self.df.update(self.getQuantity("IcoreA"))
        if self.df.get("IinD") and self.df.get("IshuntD"):
            self.df.update(self.getQuantity("IcoreD"))
        if self.df.get("IinA") and self.df.get("IinD"):
            self.df.update(self.getQuantity("Iin"))

        return self.df


def linear_fit(x, y):
    try:
        import ROOT
    except ImportError:
        log.warning("No PyROOT module found! ")

    from array import array

    """Linear fit with PyROOT

    Args:
        x (array): the x values, input DACs for VCal calibration
        y (array): the y values, measured Vmux[int] for VCal calibration

    Returns:
        result.Parameter(1) (float): the slope of the fitted line
        result.Parameter(0) (float): the offset of the fitted line
    """
    gr = ROOT.TGraph(len(x), array("d", x), array("d", y))

    f = ROOT.TF1("f", "[1] * x + [0]")
    result = gr.Fit(f, "S")

    return result.Parameter(1), result.Parameter(0)


def linear_fit_np(x, y):
    """Linear fit with NumPy. numpy.linalg.lstsq() is called.

    Args:
        x (array): the x values, input DACs for VCal calibration
        y (array): the y values, measured Vmux[int] for VCal calibration

    Returns:
        p1 (float): the slope of the fitted line
        p0 (float): the offset of the fitted line
    """
    A = np.vstack([x, np.ones(len(x))]).T
    p1, p0 = np.linalg.lstsq(A, y, rcond=None)[0]
    return p1, p0


def lookup(input_dict, search_key):
    # recursion to look up the desired key in a dict and record the path
    for k, v in input_dict.items():
        if k == search_key:
            return v
        elif isinstance(v, dict):
            _v = lookup(v, search_key)
            if _v is not None:
                return _v


def get_inputs(input_meas, test_type):
    # Figure out if input if single file or directory
    allinputs = []
    if os.path.isfile(input_meas):
        allinputs = [input_meas]
    elif os.path.isdir(input_meas):
        if test_type not in input_meas:
            raise FileNotFoundError(
                f"The input path {input_meas} does not include the test type {test_type}. Please check the input path."
            )
        allinputs = sorted(glob.glob(f"{input_meas}/*.json"))
        if len(allinputs) == 0:
            raise FileNotFoundError(
                f"No input json files in `{input_meas}` are found! Please check the input path."
            )
    else:
        raise FileNotFoundError(
            "Input is not recognized as single file or path to directory containing files. Please check the input."
        )
    return allinputs


def get_time_stamp(filename):
    # Read timestamp from measurement output file name
    # Assumes that filename ends with pattern: "/{timestamp}/{chipname}.json"
    return filename.split("/")[-2]
