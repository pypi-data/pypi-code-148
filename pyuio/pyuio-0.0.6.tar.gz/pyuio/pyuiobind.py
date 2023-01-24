from pyuiolib import _process_read, _process_write #functions from pyuiolib.c
import ctypes
import errno
from struct import pack, unpack
from typing import Union, Iterable

class asap_datatypes:
    """
    Contains the macros for the datatypes that this python module uses.
    Used types are:
    uint8, int8, uint16, int16, uint32, int32, uint64, int64, single (32 bit float), double (64bit float)
    """
    uint8 = 0
    int8 = 1
    uint16 = 2
    int16 = 3
    uint32 = 4
    int32 = 5
    uint64 = 6
    int64 = 7
    single = 8
    double = 9
    dataSizes = [1,1,2,2,4,4,8,8,4,8]

class asap_element:
    """
    The main class of the module, holds information about the data to read or write to.

    ...

    Attributes
    ----------
    address : int
        The starting memory address of the asap element that is to be read or modified
    size_element : int
        The size in bytes of a single element of the given datatype uint8 = 1, uint16 = 2 etc.
    size_t : int
        The total size in bytes of the memory range that is to be read or modified, array of 3 uint16 = 6 etc.
    datatype : int
        The datatype of the asap element, see the asap_datatypes class.
    """
    address = 0
    size_element = 0
    size_t =  0
    dataType = 0

    def __init__(self, address:int, dataType: int, arraySize:int = 1):
        """
        Parameters
        ----------
        address : int
            The starting memory address of the asap element that is to be read or modified
        datatype : int
            One of the datatypes from the asap_datatypes class
        arraySize : int, optional
            The size of the array to read, if reading a single value instead of an array it is not required and defaults to 1
            Note: this is the array size of asap elements not in bytes, so an array of 3 uint32 or 3 uint16 should both have 3 in this field.

        Raises
        ------
        ValueError
            address is less than 0 &| datatype is not one of the constants in asap_datatypes &| arraySize is less than 1
        TypeError
            address &| datatype &| arraySize is not of type int
        """
        if address < 0:
            raise ValueError(f"address must be a positive int, entered was: {address}")
        if type(address) is not int:
            raise TypeError(f"address must be an int, entered was {type(address)}")
        if dataType < 0 or dataType > 9:
            raise ValueError("please use a datatype from the asap_datatypes class, this one is out of range")
        if type(dataType) is not int:
            raise TypeError("please use a datatype from the asap_datatypes class, this one is the wrong datatype")
        if arraySize < 1:
            raise ValueError(f"arraySize can't be smaller than 1, entered was {arraySize}")
        if type(arraySize) is not int:
            raise TypeError(f"arraySize should be of type int, but it was: {type(arraySize)}")
        self.address = address
        self.dataType = dataType
        self.size_element = asap_datatypes.dataSizes[dataType]
        self.size_t = self.size_element*arraySize

    def process_read(self, pid: int, return_bytes:bool=False) -> Union[bytes, int, float, list[int], list[float]]:
        """
        Read data from the memory of a running process.\\
        Returns bytes, an integer, a float or a list of integers or floats

        Parameters
        ----------
        pid : int
            The process id that you wish to write to
        return_bytes : bool, optional
            Return the value as the raw bytes instead of the converted value.

        Raises
        ------
        ReferenceError
            The memory address is outside the caller's or the investigated process accessible address space.
        PermessionError
            The caller does not have permission to access the address space of the given pid.
            Generally also gets raised when the given pid is killed and one still tries to access it.
        ProcessLookupError
            No process with the given pid exists.
        Exception
            Other errno that are not accounted for, see the man page for process_vm_readv/writev.
        """
        array = [0]*self.size_t
        array = (ctypes.c_uint8 * self.size_t)(*array)
        res = _process_read(pid, self.address, ctypes.addressof(array), self.size_t) #not terribly happy with how I'm passing this buffer if someone is reading this and knows a better way, please let me know.
        if res < 0:
            if res == -errno.EFAULT:
                raise ReferenceError("The address is not in an accessible memory location to either this process or the process that is being written to.")
            elif res == -errno.EPERM:
                raise PermissionError("Insufficient permissions to access process memory space.")
            elif res == -errno.ESRCH:
                raise ProcessLookupError(f"No process exists with the pid {pid}.")
            else:
                raise Exception(f"An exception occured of an unknown type, memory read likely failed. errno: -{res}")
        if return_bytes:
            return bytes(array)
        return convert_to_value(array, self.size_element, self.dataType)

    def process_write(self, pid: int, data: Union[int, float, list[int], list[float]]):
        """
        Write data into the memory of a running process.

        Parameters
        ----------
        pid : int
            The process id that you wish to write to
        data : int, float, list(int), list(float)
            The information that needs to be written into the process

        Raises
        ------
        ReferenceError
            The memory address is outside the caller's or the investigated process accessible address space.
        PermessionError
            The caller does not have permission to access the address space of the given pid.
            Generally also gets raised when the pid is killed and one still tries to access it.
        ProcessLookupError
            No process with the given pid exists.
        Exception
            Other errno that are not accounted for, see the man page for process_vm_readv/writev.
        """
        array = convert_to_bytes(data, self.size_element, self.dataType)
        array = (ctypes.c_uint8 * self.size_t)(*array)
        res = _process_write(pid, self.address, ctypes.addressof(array), self.size_t) #not terribly happy with how I'm passing this buffer if someone is reading this and knows a better way, please let me know.
        if res < 0:
            if res == -errno.EFAULT:
                raise ReferenceError("The address is not in an accessible memory location to either this process or the process that is being written to.")
            elif res == -errno.EPERM:
                raise PermissionError("Insufficient permissions to access process memory space.")
            elif res == -errno.ESRCH:
                raise ProcessLookupError(f"No process exists with the pid {pid}.")
            else:
                raise Exception(f"An exception occured of an unknown type, memory write likely failed. errno: -{res}")

        

def chunks(lst : list, n : int) -> Iterable:
    """
    Not really part of the module, for internal use.\\
    Convert a list into chunks of a certain size.

    Parameters
    ----------
    lst : list
        The list that is to be split into chunks
    n : int 
        The size of the chunks that it needs to be split into
    """
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def convert_to_bytes(data, dataSize: int, dataType: int) -> bytes:
    """
    Not really part of the module, for internal use.\\
    Convert an int/float or list of ints/floats into the raw binary representation in the form of a byte array

    Parameters
    ----------
    data : int, float, list(int), list(float)
        The data that needs to be converted to bytes
    dataSize : int
        The size of a single element in bytes
    dataType: int
        The asap datatype of the data
    """
    array = []
    if not isinstance(data, list):
        data = [data]
    if dataType == asap_datatypes.int8:
        for unit in data:
            array += pack("b", unit)
    elif dataType == asap_datatypes.int16:
        for unit in data:
            array += pack("h", unit)
    elif dataType == asap_datatypes.int32:
        for unit in data:
            array += pack("i", unit)
    elif dataType == asap_datatypes.int64:
        for unit in data:
            array += pack("q", unit)
    elif dataType == asap_datatypes.single:
        for unit in data:
            array += pack("f", unit)
    elif dataType == asap_datatypes.double:
        for unit in data:
            array += pack("d", unit)
    else:
        for unit in data:
            array += int.to_bytes(unit, dataSize, 'little')
    return array

def convert_to_value(data: list, dataSize: int, dataType: int) -> Union[int, float, list[int], list[float]]:
    """
    Not really part of the module, for internal use.\\
    Convert a byte array into a value or a list of values

    Parameters
    ----------
    data : list(int)
        The bytes that need to be converted to usable value
    dataSize : int
        The size of a single element in bytes
    dataType: int
        The asap datatype of the data
    """
    dataBlocks = chunks(data, dataSize)
    array = []
    if dataType == asap_datatypes.int8 or dataType == asap_datatypes.int16 or dataType == asap_datatypes.int32 or dataType == asap_datatypes.int64:
        for unit in dataBlocks:
            array.append(int.from_bytes(bytearray(unit), 'little', signed=True))
    elif dataType == asap_datatypes.single:
        for unit in dataBlocks:
            array.append(unpack("f", bytearray(unit))[0])
    elif dataType == asap_datatypes.double:
        for unit in dataBlocks:
            array.append(unpack("d", bytearray(unit))[0])
    else:
        for unit in dataBlocks:
            array.append(int.from_bytes(bytearray(unit), 'little', signed=False))
    if len(array) == 1:
        array = array[0] 
    return array


def process_write(pid: int, asap_ele: asap_element, data: Union[int, float, list[int], list[float]]):
    """
    Write data into the memory of a running process.

    Parameters
    ----------
    pid : int
        The process id that you wish to write to
    asap_ele : asap_element
        The asap element containing the necessary information to correctly write the data, see the asap_element class
    data : int, float, list(int), list(float)
        The information that needs to be written into the process

    Raises
    ------
    ReferenceError
        The memory address is outside the caller's or the investigated process accessible address space.
    PermessionError
        The caller does not have permission to access the address space of the given pid.
        Generally also gets raised when the pid is killed and one still tries to access it.
    ProcessLookupError
        No process with the given pid exists.
    Exception
        Other errno that are not accounted for, see the man page for process_vm_readv/writev.
    """
    array = convert_to_bytes(data, asap_ele.size_element, asap_ele.dataType)
    array = (ctypes.c_uint8 * asap_ele.size_t)(*array)
    res = _process_write(pid, asap_ele.address, ctypes.addressof(array), asap_ele.size_t) #not terribly happy with how I'm passing this buffer if someone is reading this and knows a better way, please let me know.
    if res < 0:
        if res == -errno.EFAULT:
            raise ReferenceError("The address is not in an accessible memory location to either this process or the process that is being written to.")
        elif res == -errno.EPERM:
            raise PermissionError("Insufficient permissions to access process memory space.")
        elif res == -errno.ESRCH:
            raise ProcessLookupError(f"No process exists with the pid {pid}.")
        else:
            raise Exception(f"An exception occured of an unknown type, memory write likely failed. errno: -{res}")

def process_read(pid: int, asap_ele: asap_element, return_bytes:bool=False) -> Union[bytes, int, float, list[int], list[float]]:
    """
    Read data from the memory of a running process.\\
    Returns bytes, an integer, a float or a list of integers or floats

    Parameters
    ----------
    pid : int
        The process id that you wish to write to
    asap_ele : asap_element
        The asap element containing the necessary information to correctly write the data, see the asap_element class
    return_bytes : bool, optional
        Return the value as the raw bytes instead of the converted value.

    Raises
    ------
    ReferenceError
        The memory address is outside the caller's or the investigated process accessible address space.
    PermessionError
        The caller does not have permission to access the address space of the given pid.
        Generally also gets raised when the given pid is killed and one still tries to access it.
    ProcessLookupError
        No process with the given pid exists.
    Exception
        Other errno that are not accounted for, see the man page for process_vm_readv/writev.
    """
    array = [0]*asap_ele.size_t
    array = (ctypes.c_uint8 * asap_ele.size_t)(*array)
    res = _process_read(pid, asap_ele.address, ctypes.addressof(array), asap_ele.size_t) #not terribly happy with how I'm passing this buffer if someone is reading this and knows a better way, please let me know.
    if res < 0:
        if res == -errno.EFAULT:
            raise ReferenceError("The address is not in an accessible memory location to either this process or the process that is being written to.")
        elif res == -errno.EPERM:
            raise PermissionError("Insufficient permissions to access process memory space.")
        elif res == -errno.ESRCH:
            raise ProcessLookupError(f"No process exists with the pid {pid}.")
        else:
            raise Exception(f"An exception occured of an unknown type, memory read likely failed. errno: -{res}")
    if return_bytes:
        return bytes(array)
    return convert_to_value(array, asap_ele.size_element, asap_ele.dataType)