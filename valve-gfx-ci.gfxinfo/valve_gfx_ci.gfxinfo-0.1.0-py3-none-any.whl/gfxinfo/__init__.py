import os

from .pcidevice import PCIDevice
from .amdgpu import AmdGpuDeviceDB
from .intel import IntelGpuDeviceDB
from .virt import VirtIOGpuDeviceDB
from .gfxinfo_vulkan import VulkanInfo


SUPPORTED_GPU_DBS = [AmdGpuDeviceDB(), IntelGpuDeviceDB(), VirtIOGpuDeviceDB()]


def pci_devices():
    def readfile(root, filename):
        with open(os.path.join(root, filename)) as f:
            return f.read().strip()

    pciids = []
    for root, dirs, files in os.walk('/sys/devices/'):
        if root == "/sys/devices/":
            dirs[0:] = [d for d in dirs if d.startswith("pci")]

        if set(["vendor", 'device', 'revision']).issubset(files):
            pci_dev = PCIDevice(vendor_id=int(readfile(root, "vendor"), 16),
                                product_id=int(readfile(root, "device"), 16),
                                revision=int(readfile(root, "revision"), 16))
            pciids.append(pci_dev)

    return pciids


def find_gpu():
    """For now we only support single-gpu DUTs"""
    devices = pci_devices()

    for pci_device in devices:
        for gpu_db in SUPPORTED_GPU_DBS:
            if gpu := gpu_db.from_pciid(pci_device):
                return gpu

    # We could not find the GPU in our databases, update them
    for gpu_db in SUPPORTED_GPU_DBS:
        gpu_db.update()

    # Retry, now that we have updated our DBs
    for pci_device in devices:
        for gpu_db in SUPPORTED_GPU_DBS:
            if gpu := gpu_db.from_pciid(pci_device):
                return gpu


def cache_db():
    for gpu_db in SUPPORTED_GPU_DBS:
        gpu_db.cache_db()


def check_db():
    result = True
    for gpu_db in SUPPORTED_GPU_DBS:
        if not gpu_db.check_db():
            result = False
    return result


def find_gpu_from_pciid(pciid):
    for gpu_db in SUPPORTED_GPU_DBS:
        if gpu := gpu_db.from_pciid(pciid):
            return gpu

    # We could not find the GPU, retry with updated DBs
    for gpu_db in SUPPORTED_GPU_DBS:
        gpu_db.update()
        if gpu := gpu_db.from_pciid(pciid):
            return gpu


__all__ = ['pci_devices', 'find_gpu', 'cache_db', 'VulkanInfo']
