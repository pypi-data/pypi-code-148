"""
pyuio.

A python library to expose the Linux Userspace IO to python, currently implements process_vm_readv and process_vm_writev from sys/uio.h.
"""
from .pyuiobind import asap_datatypes, asap_element, process_read, process_write

__version__ = "0.0.6"
__author__ = "Maud Spierings"
__credits__ = "GOcontroll Modular Embedded Electronics"