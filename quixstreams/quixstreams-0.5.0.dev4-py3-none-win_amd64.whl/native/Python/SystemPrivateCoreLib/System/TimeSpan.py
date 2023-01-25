# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from ...InteropHelpers.InteropUtils import InteropUtils


class TimeSpan(object):
    
    def __init__(self, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            Pointer to .Net type TimeSpan in memory as bytes
        
        Returns
        ----------
        
        TimeSpan:
            Instance wrapping the .net type TimeSpan
        """
        
        self.__pointer = net_pointer
        
        self.__finalizer = weakref.finalize(self, self.__finalizerfunc)
        self.__finalizer.atexit = False
    
    def __finalizerfunc(self):
        InteropUtils.free_uptr(self.__pointer)
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
    __interop_func = InteropUtils.get_function("timespan_constructor")
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
            GC Handle Pointer to .Net type TimeSpan
        """
        ticks_long = ctypes.c_longlong(ticks)
        
        result = InteropUtils.invoke("timespan_constructor", ticks_long)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("timespan_constructor2")
    __interop_func.restype = c_void_p
    @staticmethod
    def Constructor2(hours: int, minutes: int, seconds: int) -> c_void_p:
        """
        Parameters
        ----------
        
        hours: int
            Underlying .Net type is int
        
        minutes: int
            Underlying .Net type is int
        
        seconds: int
            Underlying .Net type is int
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeSpan
        """
        result = InteropUtils.invoke("timespan_constructor2", hours, minutes, seconds)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("timespan_constructor3")
    __interop_func.restype = c_void_p
    @staticmethod
    def Constructor3(days: int, hours: int, minutes: int, seconds: int) -> c_void_p:
        """
        Parameters
        ----------
        
        days: int
            Underlying .Net type is int
        
        hours: int
            Underlying .Net type is int
        
        minutes: int
            Underlying .Net type is int
        
        seconds: int
            Underlying .Net type is int
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeSpan
        """
        result = InteropUtils.invoke("timespan_constructor3", days, hours, minutes, seconds)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("timespan_constructor4")
    __interop_func.restype = c_void_p
    @staticmethod
    def Constructor4(days: int, hours: int, minutes: int, seconds: int, milliseconds: int) -> c_void_p:
        """
        Parameters
        ----------
        
        days: int
            Underlying .Net type is int
        
        hours: int
            Underlying .Net type is int
        
        minutes: int
            Underlying .Net type is int
        
        seconds: int
            Underlying .Net type is int
        
        milliseconds: int
            Underlying .Net type is int
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeSpan
        """
        result = InteropUtils.invoke("timespan_constructor4", days, hours, minutes, seconds, milliseconds)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("timespan_constructor5")
    __interop_func.restype = c_void_p
    @staticmethod
    def Constructor5(days: int, hours: int, minutes: int, seconds: int, milliseconds: int, microseconds: int) -> c_void_p:
        """
        Parameters
        ----------
        
        days: int
            Underlying .Net type is int
        
        hours: int
            Underlying .Net type is int
        
        minutes: int
            Underlying .Net type is int
        
        seconds: int
            Underlying .Net type is int
        
        milliseconds: int
            Underlying .Net type is int
        
        microseconds: int
            Underlying .Net type is int
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeSpan
        """
        result = InteropUtils.invoke("timespan_constructor5", days, hours, minutes, seconds, milliseconds, microseconds)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("timespan_get_ticks")
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
        result = InteropUtils.invoke("timespan_get_ticks", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("timespan_get_days")
    __interop_func.restype = ctypes.c_int
    __interop_func.argtypes = [c_void_p]
    def get_Days(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("timespan_get_days", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("timespan_get_hours")
    __interop_func.restype = ctypes.c_int
    __interop_func.argtypes = [c_void_p]
    def get_Hours(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("timespan_get_hours", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("timespan_get_milliseconds")
    __interop_func.restype = ctypes.c_int
    __interop_func.argtypes = [c_void_p]
    def get_Milliseconds(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("timespan_get_milliseconds", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("timespan_get_microseconds")
    __interop_func.restype = ctypes.c_int
    __interop_func.argtypes = [c_void_p]
    def get_Microseconds(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("timespan_get_microseconds", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("timespan_get_nanoseconds")
    __interop_func.restype = ctypes.c_int
    __interop_func.argtypes = [c_void_p]
    def get_Nanoseconds(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("timespan_get_nanoseconds", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("timespan_get_minutes")
    __interop_func.restype = ctypes.c_int
    __interop_func.argtypes = [c_void_p]
    def get_Minutes(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("timespan_get_minutes", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("timespan_get_seconds")
    __interop_func.restype = ctypes.c_int
    __interop_func.argtypes = [c_void_p]
    def get_Seconds(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("timespan_get_seconds", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("timespan_get_totaldays")
    __interop_func.restype = ctypes.c_double
    __interop_func.argtypes = [c_void_p]
    def get_TotalDays(self) -> float:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        float:
            Underlying .Net type is double
        """
        result = InteropUtils.invoke("timespan_get_totaldays", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("timespan_get_totalhours")
    __interop_func.restype = ctypes.c_double
    __interop_func.argtypes = [c_void_p]
    def get_TotalHours(self) -> float:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        float:
            Underlying .Net type is double
        """
        result = InteropUtils.invoke("timespan_get_totalhours", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("timespan_get_totalmilliseconds")
    __interop_func.restype = ctypes.c_double
    __interop_func.argtypes = [c_void_p]
    def get_TotalMilliseconds(self) -> float:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        float:
            Underlying .Net type is double
        """
        result = InteropUtils.invoke("timespan_get_totalmilliseconds", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("timespan_get_totalmicroseconds")
    __interop_func.restype = ctypes.c_double
    __interop_func.argtypes = [c_void_p]
    def get_TotalMicroseconds(self) -> float:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        float:
            Underlying .Net type is double
        """
        result = InteropUtils.invoke("timespan_get_totalmicroseconds", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("timespan_get_totalnanoseconds")
    __interop_func.restype = ctypes.c_double
    __interop_func.argtypes = [c_void_p]
    def get_TotalNanoseconds(self) -> float:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        float:
            Underlying .Net type is double
        """
        result = InteropUtils.invoke("timespan_get_totalnanoseconds", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("timespan_get_totalminutes")
    __interop_func.restype = ctypes.c_double
    __interop_func.argtypes = [c_void_p]
    def get_TotalMinutes(self) -> float:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        float:
            Underlying .Net type is double
        """
        result = InteropUtils.invoke("timespan_get_totalminutes", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("timespan_get_totalseconds")
    __interop_func.restype = ctypes.c_double
    __interop_func.argtypes = [c_void_p]
    def get_TotalSeconds(self) -> float:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        float:
            Underlying .Net type is double
        """
        result = InteropUtils.invoke("timespan_get_totalseconds", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("timespan_add")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p, c_void_p]
    def Add(self, ts: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        ts: c_void_p
            GC Handle Pointer to .Net type TimeSpan
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeSpan
        """
        result = InteropUtils.invoke("timespan_add", self.__pointer, ts)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("timespan_compare")
    __interop_func.restype = ctypes.c_int
    __interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def Compare(t1: c_void_p, t2: c_void_p) -> int:
        """
        Parameters
        ----------
        
        t1: c_void_p
            GC Handle Pointer to .Net type TimeSpan
        
        t2: c_void_p
            GC Handle Pointer to .Net type TimeSpan
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("timespan_compare", t1, t2)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("timespan_compareto")
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
        result = InteropUtils.invoke("timespan_compareto", self.__pointer, value)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("timespan_compareto2")
    __interop_func.restype = ctypes.c_int
    __interop_func.argtypes = [c_void_p, c_void_p]
    def CompareTo2(self, value: c_void_p) -> int:
        """
        Parameters
        ----------
        
        value: c_void_p
            GC Handle Pointer to .Net type TimeSpan
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("timespan_compareto2", self.__pointer, value)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("timespan_fromdays")
    __interop_func.restype = c_void_p
    @staticmethod
    def FromDays(value: float) -> c_void_p:
        """
        Parameters
        ----------
        
        value: float
            Underlying .Net type is double
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeSpan
        """
        result = InteropUtils.invoke("timespan_fromdays", value)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("timespan_duration")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def Duration(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeSpan
        """
        result = InteropUtils.invoke("timespan_duration", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("timespan_equals")
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
        result = InteropUtils.invoke("timespan_equals", self.__pointer, value)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("timespan_equals2")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p, c_void_p]
    def Equals2(self, obj: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        obj: c_void_p
            GC Handle Pointer to .Net type TimeSpan
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("timespan_equals2", self.__pointer, obj)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("timespan_equals3")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def Equals3(t1: c_void_p, t2: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        t1: c_void_p
            GC Handle Pointer to .Net type TimeSpan
        
        t2: c_void_p
            GC Handle Pointer to .Net type TimeSpan
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("timespan_equals3", t1, t2)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("timespan_gethashcode")
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
        result = InteropUtils.invoke("timespan_gethashcode", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("timespan_fromhours")
    __interop_func.restype = c_void_p
    @staticmethod
    def FromHours(value: float) -> c_void_p:
        """
        Parameters
        ----------
        
        value: float
            Underlying .Net type is double
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeSpan
        """
        result = InteropUtils.invoke("timespan_fromhours", value)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("timespan_frommilliseconds")
    __interop_func.restype = c_void_p
    @staticmethod
    def FromMilliseconds(value: float) -> c_void_p:
        """
        Parameters
        ----------
        
        value: float
            Underlying .Net type is double
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeSpan
        """
        result = InteropUtils.invoke("timespan_frommilliseconds", value)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("timespan_frommicroseconds")
    __interop_func.restype = c_void_p
    @staticmethod
    def FromMicroseconds(value: float) -> c_void_p:
        """
        Parameters
        ----------
        
        value: float
            Underlying .Net type is double
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeSpan
        """
        result = InteropUtils.invoke("timespan_frommicroseconds", value)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("timespan_fromminutes")
    __interop_func.restype = c_void_p
    @staticmethod
    def FromMinutes(value: float) -> c_void_p:
        """
        Parameters
        ----------
        
        value: float
            Underlying .Net type is double
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeSpan
        """
        result = InteropUtils.invoke("timespan_fromminutes", value)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("timespan_negate")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def Negate(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeSpan
        """
        result = InteropUtils.invoke("timespan_negate", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("timespan_fromseconds")
    __interop_func.restype = c_void_p
    @staticmethod
    def FromSeconds(value: float) -> c_void_p:
        """
        Parameters
        ----------
        
        value: float
            Underlying .Net type is double
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeSpan
        """
        result = InteropUtils.invoke("timespan_fromseconds", value)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("timespan_subtract")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p, c_void_p]
    def Subtract(self, ts: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        ts: c_void_p
            GC Handle Pointer to .Net type TimeSpan
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeSpan
        """
        result = InteropUtils.invoke("timespan_subtract", self.__pointer, ts)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("timespan_multiply")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p, ctypes.c_double]
    def Multiply(self, factor: float) -> c_void_p:
        """
        Parameters
        ----------
        
        factor: float
            Underlying .Net type is double
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeSpan
        """
        result = InteropUtils.invoke("timespan_multiply", self.__pointer, factor)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("timespan_divide")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p, ctypes.c_double]
    def Divide(self, divisor: float) -> c_void_p:
        """
        Parameters
        ----------
        
        divisor: float
            Underlying .Net type is double
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeSpan
        """
        result = InteropUtils.invoke("timespan_divide", self.__pointer, divisor)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("timespan_divide2")
    __interop_func.restype = ctypes.c_double
    __interop_func.argtypes = [c_void_p, c_void_p]
    def Divide2(self, ts: c_void_p) -> float:
        """
        Parameters
        ----------
        
        ts: c_void_p
            GC Handle Pointer to .Net type TimeSpan
        
        Returns
        -------
        
        float:
            Underlying .Net type is double
        """
        result = InteropUtils.invoke("timespan_divide2", self.__pointer, ts)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("timespan_fromticks")
    __interop_func.restype = c_void_p
    @staticmethod
    def FromTicks(value: int) -> c_void_p:
        """
        Parameters
        ----------
        
        value: int
            Underlying .Net type is long
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeSpan
        """
        value_long = ctypes.c_longlong(value)
        
        result = InteropUtils.invoke("timespan_fromticks", value_long)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("timespan_parse")
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
            GC Handle Pointer to .Net type TimeSpan
        """
        s_ptr = InteropUtils.utf8_to_ptr(s)
        
        result = InteropUtils.invoke("timespan_parse", s_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("timespan_tryparse")
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
            GC Handle Pointer to .Net type TimeSpan&
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        s_ptr = InteropUtils.utf8_to_ptr(s)
        
        result2 = InteropUtils.invoke("timespan_tryparse", s_ptr, resultOut)
        return result2
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("timespan_tostring")
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
        result = InteropUtils.invoke("timespan_tostring", self.__pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("timespan_tostring2")
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
        
        result = InteropUtils.invoke("timespan_tostring2", self.__pointer, format_ptr)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("timespan_op_equality")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def op_Equality(t1: c_void_p, t2: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        t1: c_void_p
            GC Handle Pointer to .Net type TimeSpan
        
        t2: c_void_p
            GC Handle Pointer to .Net type TimeSpan
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("timespan_op_equality", t1, t2)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("timespan_op_inequality")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def op_Inequality(t1: c_void_p, t2: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        t1: c_void_p
            GC Handle Pointer to .Net type TimeSpan
        
        t2: c_void_p
            GC Handle Pointer to .Net type TimeSpan
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("timespan_op_inequality", t1, t2)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("timespan_get_zero")
    __interop_func.restype = c_void_p
    @staticmethod
    def get_Zero() -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeSpan
        """
        result = InteropUtils.invoke("timespan_get_zero")
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("timespan_get_maxvalue")
    __interop_func.restype = c_void_p
    @staticmethod
    def get_MaxValue() -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeSpan
        """
        result = InteropUtils.invoke("timespan_get_maxvalue")
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("timespan_get_minvalue")
    __interop_func.restype = c_void_p
    @staticmethod
    def get_MinValue() -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeSpan
        """
        result = InteropUtils.invoke("timespan_get_minvalue")
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("timespan_get_nanosecondspertick")
    __interop_func.restype = ctypes.c_longlong
    @staticmethod
    def get_NanosecondsPerTick() -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is long
        """
        result = InteropUtils.invoke("timespan_get_nanosecondspertick")
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("timespan_get_tickspermicrosecond")
    __interop_func.restype = ctypes.c_longlong
    @staticmethod
    def get_TicksPerMicrosecond() -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is long
        """
        result = InteropUtils.invoke("timespan_get_tickspermicrosecond")
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("timespan_get_tickspermillisecond")
    __interop_func.restype = ctypes.c_longlong
    @staticmethod
    def get_TicksPerMillisecond() -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is long
        """
        result = InteropUtils.invoke("timespan_get_tickspermillisecond")
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("timespan_get_tickspersecond")
    __interop_func.restype = ctypes.c_longlong
    @staticmethod
    def get_TicksPerSecond() -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is long
        """
        result = InteropUtils.invoke("timespan_get_tickspersecond")
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("timespan_get_ticksperminute")
    __interop_func.restype = ctypes.c_longlong
    @staticmethod
    def get_TicksPerMinute() -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is long
        """
        result = InteropUtils.invoke("timespan_get_ticksperminute")
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("timespan_get_ticksperhour")
    __interop_func.restype = ctypes.c_longlong
    @staticmethod
    def get_TicksPerHour() -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is long
        """
        result = InteropUtils.invoke("timespan_get_ticksperhour")
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("timespan_get_ticksperday")
    __interop_func.restype = ctypes.c_longlong
    @staticmethod
    def get_TicksPerDay() -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is long
        """
        result = InteropUtils.invoke("timespan_get_ticksperday")
        return result
