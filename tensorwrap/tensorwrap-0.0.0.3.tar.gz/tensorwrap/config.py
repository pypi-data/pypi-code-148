import jax
from typing import Any


def list_physical_devices(device_type: Any = "gpu"):
    """Returns a list of physical devices that are currently on the device.
    args:
     - device_type: The type of device to search for. Defaults to gpu."""
    if device_type == 'cuda':
        device_type = "gpu"
    try:
        devices = jax.devices(device_type.lower())
    except:
        devices = []
    return devices
