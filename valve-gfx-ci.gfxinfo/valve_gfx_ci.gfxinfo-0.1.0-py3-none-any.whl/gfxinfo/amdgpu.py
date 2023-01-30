from dataclasses import dataclass
import os
import re
import requests
import sys

from . import PCIDevice


def host_cpu_name():
    for line in open("/proc/cpuinfo").readlines():
        fields = line.split(":")
        if fields[0].strip() == "model name":
            return fields[1].strip()

    return None


@dataclass
class AMDGPU:
    pci_device: PCIDevice
    asic_type: str
    is_APU: bool
    marketing_name: str

    @property
    def has_bad_marketing_name(self):
        return self.marketing_name in [
            "AMD Radeon(TM) Graphics",
            f"{hex(self.pci_device.product_id)}:f{hex(self.pci_device.revision)}".upper()
        ]

    @property
    def unknown_fields(self):
        missing = set()

        if self.architecture is None:
            missing.add("architecture")
        if self.family is None:
            missing.add("family")
        if self.gfx_version is None:
            missing.add("gfx_version")

        return missing

    def __post_init__(self):
        # Fixup any bad APU marketing name, if possible
        if self.is_APU and self.has_bad_marketing_name:
            if cpu_name := host_cpu_name():
                self.marketing_name = cpu_name

    @property
    def codename(self):
        codenames = {
            # For backwards compatibility with the amdgpu naming
            "TAHITI_XT": "TAHITI",
            "TAHITI_PRO": "TAHITI",
            "CAPEVERDE_XT": "VERDE",
            "CAPEVERDE_PRO": "VERDE",
            "SPECTRE_LITE": "KAVERI",
            "SPECTRE": "KAVERI",
            "SPECTRE_SL": "KAVERI",
            "SPOOKY": "KAVERI",
            "KALINDI": "KABINI",
            "PITCAIRN_XT": "PITCAIRN",
            "PITCAIRN_PRO": "PITCAIRN",
            "ICELAND": "TOPAZ",
            "CARRIZO_EMB": "CARRIZO",
            "VEGAM1": "VEGAM",
            "VEGAM2": "VEGAM",

            # POLARIS
            "ELLESMERE": "POLARIS10",
            "BAFFIN": "POLARIS11",
            "GFX8_0_4": "POLARIS12",

            # VEGA
            "GFX9_0_0": "VEGA10",
            "GFX9_0_2": "RAVEN",
            "GFX9_0_4": "VEGA12",
            "GFX9_0_6": "VEGA20",
            "GFX9_0_C": "RENOIR",

            # NAVI1X
            "GFX10_1_0": "NAVI10",
            "GFX10_1_0_XL": "NAVI10",
            "GFX10_1_1": "NAVI12",
            "GFX10_1_2": "NAVI14",

            # NAVI2X
            "GFX10_3_0": "NAVI21",
            "GFX10_3_1": "NAVI22",
            "GFX10_3_2": "NAVI23",
            "GFX10_3_4": "NAVI24",
            "GFX10_3_5": "REMBRANDT",

            # NAVI3X
            "GFX11_0_0": "NAVI31",
            "GFX11_0_2": "NAVI32",
            "GFX11_0_3": "NAVI33",
        }

        return codenames.get(self.asic_type, self.asic_type)

    @property
    def family(self):
        families = {
            # SI
            "TAHITI": "SI",
            "PITCAIRN": "SI",
            "VERDE": "SI",
            "OLAND": "SI",
            "HAINAN": "SI",
            "KABINI": "SI",
            "BONAIRE": "SI",
            "HAWAII": "SI",
            "KAVERI": "SI",

            # VI
            "TOPAZ": "VI",
            "TONGA": "VI",
            "CARRIZO": "VI",
            "FIJI": "VI",
            "STONEY": "VI",

            # AI
            "POLARIS10": "AI",
            "POLARIS11": "AI",
            "POLARIS12": "AI",
            "VEGAM": "AI",
            "VEGA10": "AI",
            "VEGA12": "AI",
            "VEGA20": "AI",
            "ARCTURUS": "AI",
            "RAVEN": "AI",
            "RENOIR": "AI",
        }

        return families.get(self.codename, "UNK")

    @property
    def architecture(self):
        architectures = {
            # GCN1
            "TAHITI": "GCN1",
            "PITCAIRN": "GCN1",
            "VERDE": "GCN1",
            "OLAND": "GCN1",
            "HAINAN": "GCN1",

            # GCN2
            "KAVERI": "GCN2",
            "BONAIRE": "GCN2",
            "HAWAII": "GCN2",
            "KABINI": "GCN2",
            "MULLINS": "GCN2",

            # GCN3
            "TOPAZ": "GCN3",
            "TONGA": "GCN3",
            "FIJI": "GCN3",
            "CARRIZO": "GCN3",
            "STONEY": "GCN3",

            # GCN4
            "POLARIS10": "GCN4",
            "POLARIS11": "GCN4",
            "POLARIS12": "GCN4",
            "VEGAM": "GCN4",

            # GCN5
            "VEGA10": "GCN5",
            "VEGA12": "GCN5",
            "RAVEN": "GCN5",

            # GCN5.1
            "VEGA20": "GCN5.1",
            "RENOIR": "GCN5.1",

            # CDNA
            "ARCTURUS": "CDNA",

            # CDNA2
            "ALDEBARAN": "CDNA2",

            # Navi / RDNA1
            "NAVI10": "RDNA1",
            "NAVI12": "RDNA1",
            "NAVI14": "RDNA1",
            "CYAN_SKILLFISH": "RDNA1",

            # RDNA2
            "NAVI21": "RDNA2",
            "NAVI22": "RDNA2",
            "NAVI23": "RDNA2",
            "NAVI24": "RDNA2",
            "VANGOGH": "RDNA2",
            "REMBRANDT": "RDNA2",

            # RDNA3
            "NAVI31": "RDNA3",
            "NAVI32": "RDNA3",
            "NAVI33": "RDNA3",
        }

        return architectures.get(self.codename)

    @property
    def base_name(self):
        return f"{self.gfx_version}-{self.codename}".lower()

    @property
    def gfx_version(self):
        versions = {
            # GFX7
            "GCN1": "gfx6",

            # GFX7
            "GCN2": "gfx7",

            # GFX8
            "GCN3": "gfx8",
            "GCN4": "gfx8",

            # GFX9
            "GCN5": "gfx9",
            "GCN5.1": "gfx9",
            "CDNA": "gfx9",
            "CDNA2": "gfx9",

            # GFX10
            "RDNA1": "gfx10",
            "RDNA2": "gfx10",

            # GFX11
            "RDNA3": "gfx11",
        }

        return versions.get(self.architecture)

    @property
    def tags(self):
        tags = set()

        tags.add(f"amdgpu:pciid:{self.pciid}")
        tags.add(f"amdgpu:family:{self.family}")
        tags.add(f"amdgpu:codename:{self.codename}")
        tags.add(f"amdgpu:architecture:{self.architecture}")
        tags.add(f"amdgpu:gfxversion:{self.gfx_version}")
        if self.is_APU:
            tags.add("amdgpu:APU")

        return tags

    @property
    def structured_tags(self):
        return {
            "type": "amdgpu",
            "pciid": self.pciid,
            "family": self.family,
            "codename": self.codename,
            "architecture": self.architecture,
            "gfxversion": self.gfx_version,
            "marketing_name": self.marketing_name,
            "APU": self.is_APU,
        }

    @property
    def pciid(self):
        return str(self.pci_device)

    def __str__(self):
        return (f"<AMDGPU: PCIID {self.pciid} - {self.codename} - {self.family} - "
                f"{self.architecture} - {self.gfx_version.lower()}>")

    def __repr__(self):
        return f"{self.__class__}({self.__dict__})"


class AmdGpuDeviceDB:
    DEVICE_INFO_URL = "https://raw.githubusercontent.com/GPUOpen-Tools/device_info/master/DeviceInfo.cpp"
    DEVICE_INFO_FILENAME = "DeviceInfo.cpp"

    def __init__(self):
        self.is_up_to_date = False
        self.devices = dict()

        try:
            device_info = open(self.device_info_cache_path, 'r').read()
        except FileNotFoundError:
            device_info = self.cache_db()
        self._parse_device_info(device_info)

    @property
    def device_info_cache_path(self):
        package_directory = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(package_directory, self.DEVICE_INFO_FILENAME)

    def _parse_device_info(self, drv):
        self.devices = dict()

        # Expected format:
        # {GDT_GFX10_3_5, 0x164D, 0x00, GDT_HW_GENERATION_GFX103, true, "gfx1035", "AMD Radeon(TM) Graphics"},
        comp_re = re.compile(r"^\s*{\s*GDT_(?P<asic_type>[^,]+),\s*(?P<device_id>0x[\da-fA-F]+),"
                             r"\s*(?P<rev_id>0x[\da-fA-F]+),\s*(?P<generation>.+),\s*(?P<is_APU>true|false),"
                             r"\s*\"(?P<CAL_name>.*)\",\s*\"(?P<marketing_name>.*)\"},\s*$")

        started = False
        for line in drv.splitlines():
            if not started:
                if line == "GDT_GfxCardInfo gs_cardInfo[] = {":
                    started = True
                    continue
            else:
                if line == "};":
                    break

                if m := comp_re.match(line):
                    try:
                        dev = m.groupdict()
                        pci_device = PCIDevice(vendor_id=0x1002, product_id=int(dev["device_id"], 16),
                                               revision=int(dev["rev_id"], 16))
                        self.devices[pci_device] = AMDGPU(pci_device=pci_device,
                                                          asic_type=dev["asic_type"],
                                                          is_APU=dev["is_APU"] == "true",
                                                          marketing_name=dev["marketing_name"])
                    except ValueError:
                        continue

    def cache_db(self):
        r = requests.get(self.DEVICE_INFO_URL, timeout=5)
        r.raise_for_status()
        open(self.device_info_cache_path, "w").write(r.text)
        return r.text

    def update(self):
        if self.is_up_to_date:
            return

        self.cache_db()

        self.is_up_to_date = True

    def check_db(self):
        all_devices_complete = True
        for dev in self.devices.values():
            unknown_fields = dev.unknown_fields
            if len(unknown_fields) > 0:
                print(f"WARNING: The AMD GPU device {dev.pci_device} ({dev.asic_type}) has the following "
                      f"unknown fields: {unknown_fields}", file=sys.stderr)
                all_devices_complete = False

        return all_devices_complete

    def from_pciid(self, pci_device):
        return self.devices.get(pci_device)
