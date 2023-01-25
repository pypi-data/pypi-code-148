# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from .TimeSpan import TimeSpan
from ...InteropHelpers.InteropUtils import InteropUtils


class DateTime(object):
    
    __weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type DateTime
        
        Returns
        ----------
        
        DateTime:
            Instance wrapping the .net type DateTime
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer._get_interop_ptr()
        
        instance = DateTime._DateTime__weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(DateTime, cls).__new__(cls)
            DateTime._DateTime__weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type DateTime
        
        Returns
        ----------
        
        DateTime:
            Instance wrapping the .net type DateTime
        """
        if '_DateTime__pointer' in dir(self):
            return
        
        if type(net_pointer) is not c_void_p:
            self.__pointer_owner = net_pointer
            self.__pointer = net_pointer._get_interop_ptr()
        else:
            self.__pointer = net_pointer
        
        self.__finalizer = weakref.finalize(self, self.__finalizerfunc)
        self.__finalizer.atexit = False
    
    def __finalizerfunc(self):
        del DateTime._DateTime__weakrefs[self.__pointer.value]
        InteropUtils.free_hptr(self.__pointer)
        self.__finalizer.detach()
    
    def _get_interop_ptr(self) -> c_void_p:
        return self.__pointer
    
    def _dispose_ptr(self):
        self.__finalizer()
    
    def __enter__(self):
        pass
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__finalizer()
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("datetime_constructor")
    __interop_func.restype = c_void_p
    @staticmethod
    def Constructor(ticks: int) -> c_void_p:
        """
        Parameters
        ----------
        
        ticks: int
            Underlying .Net type is long
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type DateTime
        """
        ticks_long = ctypes.c_longlong(ticks)
        
        result = InteropUtils.invoke("datetime_constructor", ticks_long)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("datetime_constructor3")
    __interop_func.restype = c_void_p
    @staticmethod
    def Constructor3(year: int, month: int, day: int) -> c_void_p:
        """
        Parameters
        ----------
        
        year: int
            Underlying .Net type is int
        
        month: int
            Underlying .Net type is int
        
        day: int
            Underlying .Net type is int
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type DateTime
        """
        result = InteropUtils.invoke("datetime_constructor3", year, month, day)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("datetime_constructor6")
    __interop_func.restype = c_void_p
    @staticmethod
    def Constructor6(year: int, month: int, day: int, hour: int, minute: int, second: int) -> c_void_p:
        """
        Parameters
        ----------
        
        year: int
            Underlying .Net type is int
        
        month: int
            Underlying .Net type is int
        
        day: int
            Underlying .Net type is int
        
        hour: int
            Underlying .Net type is int
        
        minute: int
            Underlying .Net type is int
        
        second: int
            Underlying .Net type is int
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type DateTime
        """
        result = InteropUtils.invoke("datetime_constructor6", year, month, day, hour, minute, second)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("datetime_constructor9")
    __interop_func.restype = c_void_p
    @staticmethod
    def Constructor9(year: int, month: int, day: int, hour: int, minute: int, second: int, millisecond: int) -> c_void_p:
        """
        Parameters
        ----------
        
        year: int
            Underlying .Net type is int
        
        month: int
            Underlying .Net type is int
        
        day: int
            Underlying .Net type is int
        
        hour: int
            Underlying .Net type is int
        
        minute: int
            Underlying .Net type is int
        
        second: int
            Underlying .Net type is int
        
        millisecond: int
            Underlying .Net type is int
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type DateTime
        """
        result = InteropUtils.invoke("datetime_constructor9", year, month, day, hour, minute, second, millisecond)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("datetime_constructor12")
    __interop_func.restype = c_void_p
    @staticmethod
    def Constructor12(year: int, month: int, day: int, hour: int, minute: int, second: int, millisecond: int, microsecond: int) -> c_void_p:
        """
        Parameters
        ----------
        
        year: int
            Underlying .Net type is int
        
        month: int
            Underlying .Net type is int
        
        day: int
            Underlying .Net type is int
        
        hour: int
            Underlying .Net type is int
        
        minute: int
            Underlying .Net type is int
        
        second: int
            Underlying .Net type is int
        
        millisecond: int
            Underlying .Net type is int
        
        microsecond: int
            Underlying .Net type is int
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type DateTime
        """
        result = InteropUtils.invoke("datetime_constructor12", year, month, day, hour, minute, second, millisecond, microsecond)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("datetime_add")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p, c_void_p]
    def Add(self, value: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        value: c_void_p
            GC Handle Pointer to .Net type TimeSpan
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type DateTime
        """
        result = InteropUtils.invoke("datetime_add", self.__pointer, value)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("datetime_adddays")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p, ctypes.c_double]
    def AddDays(self, value: float) -> c_void_p:
        """
        Parameters
        ----------
        
        value: float
            Underlying .Net type is double
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type DateTime
        """
        result = InteropUtils.invoke("datetime_adddays", self.__pointer, value)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("datetime_addhours")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p, ctypes.c_double]
    def AddHours(self, value: float) -> c_void_p:
        """
        Parameters
        ----------
        
        value: float
            Underlying .Net type is double
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type DateTime
        """
        result = InteropUtils.invoke("datetime_addhours", self.__pointer, value)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("datetime_addmilliseconds")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p, ctypes.c_double]
    def AddMilliseconds(self, value: float) -> c_void_p:
        """
        Parameters
        ----------
        
        value: float
            Underlying .Net type is double
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type DateTime
        """
        result = InteropUtils.invoke("datetime_addmilliseconds", self.__pointer, value)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("datetime_addmicroseconds")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p, ctypes.c_double]
    def AddMicroseconds(self, value: float) -> c_void_p:
        """
        Parameters
        ----------
        
        value: float
            Underlying .Net type is double
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type DateTime
        """
        result = InteropUtils.invoke("datetime_addmicroseconds", self.__pointer, value)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("datetime_addminutes")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p, ctypes.c_double]
    def AddMinutes(self, value: float) -> c_void_p:
        """
        Parameters
        ----------
        
        value: float
            Underlying .Net type is double
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type DateTime
        """
        result = InteropUtils.invoke("datetime_addminutes", self.__pointer, value)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("datetime_addmonths")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p, ctypes.c_int]
    def AddMonths(self, months: int) -> c_void_p:
        """
        Parameters
        ----------
        
        months: int
            Underlying .Net type is int
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type DateTime
        """
        result = InteropUtils.invoke("datetime_addmonths", self.__pointer, months)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("datetime_addseconds")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p, ctypes.c_double]
    def AddSeconds(self, value: float) -> c_void_p:
        """
        Parameters
        ----------
        
        value: float
            Underlying .Net type is double
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type DateTime
        """
        result = InteropUtils.invoke("datetime_addseconds", self.__pointer, value)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("datetime_addticks")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p, ctypes.c_longlong]
    def AddTicks(self, value: int) -> c_void_p:
        """
        Parameters
        ----------
        
        value: int
            Underlying .Net type is long
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type DateTime
        """
        value_long = ctypes.c_longlong(value)
        
        result = InteropUtils.invoke("datetime_addticks", self.__pointer, value_long)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("datetime_addyears")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p, ctypes.c_int]
    def AddYears(self, value: int) -> c_void_p:
        """
        Parameters
        ----------
        
        value: int
            Underlying .Net type is int
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type DateTime
        """
        result = InteropUtils.invoke("datetime_addyears", self.__pointer, value)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("datetime_compare")
    __interop_func.restype = ctypes.c_int
    __interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def Compare(t1: c_void_p, t2: c_void_p) -> int:
        """
        Parameters
        ----------
        
        t1: c_void_p
            GC Handle Pointer to .Net type DateTime
        
        t2: c_void_p
            GC Handle Pointer to .Net type DateTime
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("datetime_compare", t1, t2)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("datetime_compareto")
    __interop_func.restype = ctypes.c_int
    __interop_func.argtypes = [c_void_p, c_void_p]
    def CompareTo(self, value: c_void_p) -> int:
        """
        Parameters
        ----------
        
        value: c_void_p
            GC Handle Pointer to .Net type Object
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("datetime_compareto", self.__pointer, value)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("datetime_compareto2")
    __interop_func.restype = ctypes.c_int
    __interop_func.argtypes = [c_void_p, c_void_p]
    def CompareTo2(self, value: c_void_p) -> int:
        """
        Parameters
        ----------
        
        value: c_void_p
            GC Handle Pointer to .Net type DateTime
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("datetime_compareto2", self.__pointer, value)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("datetime_daysinmonth")
    __interop_func.restype = ctypes.c_int
    @staticmethod
    def DaysInMonth(year: int, month: int) -> int:
        """
        Parameters
        ----------
        
        year: int
            Underlying .Net type is int
        
        month: int
            Underlying .Net type is int
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("datetime_daysinmonth", year, month)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("datetime_equals")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p, c_void_p]
    def Equals(self, value: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        value: c_void_p
            GC Handle Pointer to .Net type Object
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("datetime_equals", self.__pointer, value)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("datetime_equals2")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p, c_void_p]
    def Equals2(self, value: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        value: c_void_p
            GC Handle Pointer to .Net type DateTime
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("datetime_equals2", self.__pointer, value)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("datetime_equals3")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def Equals3(t1: c_void_p, t2: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        t1: c_void_p
            GC Handle Pointer to .Net type DateTime
        
        t2: c_void_p
            GC Handle Pointer to .Net type DateTime
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("datetime_equals3", t1, t2)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("datetime_frombinary")
    __interop_func.restype = c_void_p
    @staticmethod
    def FromBinary(dateData: int) -> c_void_p:
        """
        Parameters
        ----------
        
        dateData: int
            Underlying .Net type is long
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type DateTime
        """
        dateData_long = ctypes.c_longlong(dateData)
        
        result = InteropUtils.invoke("datetime_frombinary", dateData_long)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("datetime_fromfiletime")
    __interop_func.restype = c_void_p
    @staticmethod
    def FromFileTime(fileTime: int) -> c_void_p:
        """
        Parameters
        ----------
        
        fileTime: int
            Underlying .Net type is long
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type DateTime
        """
        fileTime_long = ctypes.c_longlong(fileTime)
        
        result = InteropUtils.invoke("datetime_fromfiletime", fileTime_long)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("datetime_fromfiletimeutc")
    __interop_func.restype = c_void_p
    @staticmethod
    def FromFileTimeUtc(fileTime: int) -> c_void_p:
        """
        Parameters
        ----------
        
        fileTime: int
            Underlying .Net type is long
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type DateTime
        """
        fileTime_long = ctypes.c_longlong(fileTime)
        
        result = InteropUtils.invoke("datetime_fromfiletimeutc", fileTime_long)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("datetime_fromoadate")
    __interop_func.restype = c_void_p
    @staticmethod
    def FromOADate(d: float) -> c_void_p:
        """
        Parameters
        ----------
        
        d: float
            Underlying .Net type is double
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type DateTime
        """
        result = InteropUtils.invoke("datetime_fromoadate", d)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("datetime_isdaylightsavingtime")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p]
    def IsDaylightSavingTime(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("datetime_isdaylightsavingtime", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("datetime_tobinary")
    __interop_func.restype = ctypes.c_longlong
    __interop_func.argtypes = [c_void_p]
    def ToBinary(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is long
        """
        result = InteropUtils.invoke("datetime_tobinary", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("datetime_get_date")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def get_Date(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type DateTime
        """
        result = InteropUtils.invoke("datetime_get_date", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("datetime_get_day")
    __interop_func.restype = ctypes.c_int
    __interop_func.argtypes = [c_void_p]
    def get_Day(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("datetime_get_day", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("datetime_get_dayofyear")
    __interop_func.restype = ctypes.c_int
    __interop_func.argtypes = [c_void_p]
    def get_DayOfYear(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("datetime_get_dayofyear", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("datetime_gethashcode")
    __interop_func.restype = ctypes.c_int
    __interop_func.argtypes = [c_void_p]
    def GetHashCode(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("datetime_gethashcode", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("datetime_get_hour")
    __interop_func.restype = ctypes.c_int
    __interop_func.argtypes = [c_void_p]
    def get_Hour(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("datetime_get_hour", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("datetime_get_millisecond")
    __interop_func.restype = ctypes.c_int
    __interop_func.argtypes = [c_void_p]
    def get_Millisecond(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("datetime_get_millisecond", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("datetime_get_microsecond")
    __interop_func.restype = ctypes.c_int
    __interop_func.argtypes = [c_void_p]
    def get_Microsecond(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("datetime_get_microsecond", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("datetime_get_nanosecond")
    __interop_func.restype = ctypes.c_int
    __interop_func.argtypes = [c_void_p]
    def get_Nanosecond(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("datetime_get_nanosecond", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("datetime_get_minute")
    __interop_func.restype = ctypes.c_int
    __interop_func.argtypes = [c_void_p]
    def get_Minute(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("datetime_get_minute", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("datetime_get_month")
    __interop_func.restype = ctypes.c_int
    __interop_func.argtypes = [c_void_p]
    def get_Month(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("datetime_get_month", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("datetime_get_now")
    __interop_func.restype = c_void_p
    @staticmethod
    def get_Now() -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type DateTime
        """
        result = InteropUtils.invoke("datetime_get_now")
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("datetime_get_second")
    __interop_func.restype = ctypes.c_int
    __interop_func.argtypes = [c_void_p]
    def get_Second(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("datetime_get_second", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("datetime_get_ticks")
    __interop_func.restype = ctypes.c_longlong
    __interop_func.argtypes = [c_void_p]
    def get_Ticks(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is long
        """
        result = InteropUtils.invoke("datetime_get_ticks", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("datetime_get_timeofday")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def get_TimeOfDay(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeSpan
        """
        result = InteropUtils.invoke("datetime_get_timeofday", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("datetime_get_today")
    __interop_func.restype = c_void_p
    @staticmethod
    def get_Today() -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type DateTime
        """
        result = InteropUtils.invoke("datetime_get_today")
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("datetime_get_year")
    __interop_func.restype = ctypes.c_int
    __interop_func.argtypes = [c_void_p]
    def get_Year(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("datetime_get_year", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("datetime_isleapyear")
    __interop_func.restype = ctypes.c_ubyte
    @staticmethod
    def IsLeapYear(year: int) -> bool:
        """
        Parameters
        ----------
        
        year: int
            Underlying .Net type is int
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("datetime_isleapyear", year)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("datetime_parse")
    __interop_func.restype = c_void_p
    @staticmethod
    def Parse(s: str) -> c_void_p:
        """
        Parameters
        ----------
        
        s: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type DateTime
        """
        s_ptr = InteropUtils.utf8_to_ptr(s)
        
        result = InteropUtils.invoke("datetime_parse", s_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("datetime_subtract")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p, c_void_p]
    def Subtract(self, value: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        value: c_void_p
            GC Handle Pointer to .Net type DateTime
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeSpan
        """
        result = InteropUtils.invoke("datetime_subtract", self.__pointer, value)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("datetime_subtract2")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p, c_void_p]
    def Subtract2(self, value: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        value: c_void_p
            GC Handle Pointer to .Net type TimeSpan
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type DateTime
        """
        result = InteropUtils.invoke("datetime_subtract2", self.__pointer, value)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("datetime_tooadate")
    __interop_func.restype = ctypes.c_double
    __interop_func.argtypes = [c_void_p]
    def ToOADate(self) -> float:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        float:
            Underlying .Net type is double
        """
        result = InteropUtils.invoke("datetime_tooadate", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("datetime_tofiletime")
    __interop_func.restype = ctypes.c_longlong
    __interop_func.argtypes = [c_void_p]
    def ToFileTime(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is long
        """
        result = InteropUtils.invoke("datetime_tofiletime", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("datetime_tofiletimeutc")
    __interop_func.restype = ctypes.c_longlong
    __interop_func.argtypes = [c_void_p]
    def ToFileTimeUtc(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is long
        """
        result = InteropUtils.invoke("datetime_tofiletimeutc", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("datetime_tolocaltime")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def ToLocalTime(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type DateTime
        """
        result = InteropUtils.invoke("datetime_tolocaltime", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("datetime_tolongdatestring")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def ToLongDateString(self) -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("datetime_tolongdatestring", self.__pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("datetime_tolongtimestring")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def ToLongTimeString(self) -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("datetime_tolongtimestring", self.__pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("datetime_toshortdatestring")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def ToShortDateString(self) -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("datetime_toshortdatestring", self.__pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("datetime_toshorttimestring")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def ToShortTimeString(self) -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("datetime_toshorttimestring", self.__pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("datetime_tostring")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def ToString(self) -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("datetime_tostring", self.__pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("datetime_tostring2")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p, c_void_p]
    def ToString2(self, format: str) -> str:
        """
        Parameters
        ----------
        
        format: str
            Underlying .Net type is string
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        format_ptr = InteropUtils.utf8_to_ptr(format)
        
        result = InteropUtils.invoke("datetime_tostring2", self.__pointer, format_ptr)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("datetime_touniversaltime")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def ToUniversalTime(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type DateTime
        """
        result = InteropUtils.invoke("datetime_touniversaltime", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("datetime_tryparse")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def TryParse(s: str, result: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        s: str
            Underlying .Net type is string
        
        result: c_void_p
            GC Handle Pointer to .Net type DateTime&
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        s_ptr = InteropUtils.utf8_to_ptr(s)
        
        result2 = InteropUtils.invoke("datetime_tryparse", s_ptr, resultOut)
        return result2
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("datetime_op_equality")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def op_Equality(d1: c_void_p, d2: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        d1: c_void_p
            GC Handle Pointer to .Net type DateTime
        
        d2: c_void_p
            GC Handle Pointer to .Net type DateTime
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("datetime_op_equality", d1, d2)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("datetime_op_inequality")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def op_Inequality(d1: c_void_p, d2: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        d1: c_void_p
            GC Handle Pointer to .Net type DateTime
        
        d2: c_void_p
            GC Handle Pointer to .Net type DateTime
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("datetime_op_inequality", d1, d2)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("datetime_getdatetimeformats")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def GetDateTimeFormats(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type string[]
        """
        result = InteropUtils.invoke("datetime_getdatetimeformats", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("datetime_get_utcnow")
    __interop_func.restype = c_void_p
    @staticmethod
    def get_UtcNow() -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type DateTime
        """
        result = InteropUtils.invoke("datetime_get_utcnow")
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("datetime_get_minvalue")
    __interop_func.restype = c_void_p
    @staticmethod
    def get_MinValue() -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type DateTime
        """
        result = InteropUtils.invoke("datetime_get_minvalue")
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("datetime_get_maxvalue")
    __interop_func.restype = c_void_p
    @staticmethod
    def get_MaxValue() -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type DateTime
        """
        result = InteropUtils.invoke("datetime_get_maxvalue")
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("datetime_get_unixepoch")
    __interop_func.restype = c_void_p
    @staticmethod
    def get_UnixEpoch() -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type DateTime
        """
        result = InteropUtils.invoke("datetime_get_unixepoch")
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
