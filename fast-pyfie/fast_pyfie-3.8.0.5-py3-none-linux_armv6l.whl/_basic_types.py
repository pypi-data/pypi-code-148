
import ctypes as _cty

from pyfie import _cty_util
from pyfie import _util
from pyfie._imports import _ENABLE_NUMPY, _ENABLE_PYPLOT

if _ENABLE_NUMPY:
    import numpy as _np

    # numpy utils
    def _attach_ndarray_to_ptr(ndarray, dst_type, safe=False):
        if not isinstance(ndarray, _np.ndarray):
            raise RuntimeError("{0} is not ndarray".format(ndarray))

        if safe:
            if issubclass(dst_type, _Numerical):
                elem_cls = dst_type
            elif issubclass(dst_type, _cty._Pointer) and hasattr(dst_type, "_ref_cls"):
                elem_cls = dst_type._ref_cls
            else:
                raise RuntimeError(
                    "attach failed : {0} / {1}".format(ndarray, dst_type))

            if elem_cls._numpy_type != ndarray.dtype:
                raise RuntimeError(
                    "attach failed : {0} / {1}".format(ndarray, dst_type))

            ptr_obj = _cty.cast(ndarray.ctypes.data, elem_cls.PTR)
            _PointerManage.store_private(ptr_obj, ndarray)  # avoid GC
            return ptr_obj
        else:
            if issubclass(dst_type, _Numerical):
                ptr_cls = dst_type.PTR
            elif issubclass(dst_type, _cty._Pointer):
                ptr_cls = dst_type
            else:
                raise RuntimeError(
                    "attach failed : {0} / {1}".format(ndarray, dst_type))

            ptr_obj = _cty.cast(ndarray.ctypes.data, ptr_cls)
            _PointerManage.store_private(ptr_obj, ndarray)  # avoid GC.
            return ptr_obj

    def _attach_ptr_to_ndarray(ptr_obj, size):
        if not isinstance(ptr_obj, _cty._Pointer) and hasattr(ptr_obj, "_ref_cls"):
            raise RuntimeError("attach failed : {0}".format(ptr_obj))

        if not issubclass(ptr_obj._ref_cls, _Numerical):
            raise RuntimeError("attach failed : {0}".format(ptr_obj))

        return _np.ctypeslib.as_array(ptr_obj, (size,))

# ----------------------------------------------------------------------------
# basic types.


class _FromParamSentinel:
    @classmethod
    def from_param(cls, obj):
        return obj


# ポインタオブジェクトによる参照先リソースの管理.
#
# ctypes の仕様では, ポインタの参照先(contents) 構造体/共用体のフィールド, 配列の要素
# これらが取得されるときには "内部バッファーにアクセスするラッパーオブジェクト" が返される.
# つまりこれらに設定されたときのインスタンスそのものが得られるわけではない.
#
# これに対して PyFIE のポインタオブジェクトでは参照先リソースを保持したい場合がある. (参照先リソースを GC で解放させないため)
# 本クラスにではこのようなポインタオブジェクトの参照先リソース管理を実現する.
#
# まずポインタオブジェクトには参照先リソースが埋め込まれる. この参照先リソースは ...
# - ポインタオブジェクトの実際の参照先(contents)と対応していなければならない.
# - ポインタオブジェクトの複製等では参照先リソースも引き継がれなければならない.
#
# これを踏まえて下記実装を行っている.
# - ポインタオブジェクト
#   + .ref 等でインスタンス化されるポインタオブジェクトに参照先リソースを埋め込む.
#   + 一時的にインスタンス化したオブジェクトへアタッチするようなポインタオブジェクトは一時的オブジェクトを参照先リソースとして埋め込む. (GC を防ぐため)
#   + ポインタの .deref による参照先取得では参照先リソースを返す.
#     (これは参照先がポインタフィールドをもつ構造体であった場合等のため)
#   + ポインタの値コピー(.value 等) では参照先リソースもコピーする.
#
# - 構造体
#   + ポインタフィールドが設定される場合, 設定されるポインタオブジェクトを内部で保持.
#   + ポインタフィールドが取得される場合, 内部で保持しているポインタオブジェクトを返す.
#
# 現在下記は未対応.
# - 要素の型がポインタ型である配列の対応.
#   本来であれば要素設定/取得時に(各要素の)参照先リソースを受け継がなければならない. (構造体のポインタフィールドと同じ扱いをする必要がある)
class _PointerManage:

    # 参照先リソース.
    class _ResourceWrapper:
        def __init__(self, instance):
            self._instance = instance

        def get(self):
            return self._instance

        def deref(self):
            return self._instance

    # 参照先リソース. (参照先非アクセス/ndarray 等外部に渡さない参照先に対して使用)
    class _ResourceWrapperPrivate(_ResourceWrapper):
        def deref(self):
            return None

    # ポインタオブジェクトに参照先(instance)リソースを埋め込む.
    @staticmethod
    def store_instance(owner_ptr, instance):
        _PointerManage.apply_resource(
            owner_ptr, _PointerManage._ResourceWrapper(instance))

    # ポインタオブジェクトに参照先(instance/非アクセス)リソースを埋め込む.
    @staticmethod
    def store_private(owner_ptr, instance):
        _PointerManage.apply_resource(
            owner_ptr, _PointerManage._ResourceWrapperPrivate(instance))

    # ポインタオブジェクトに参照先リソース(resource)を埋め込む.
    @staticmethod
    def apply_resource(owner_ptr, resource):
        if not isinstance(resource, (_PointerManage._ResourceWrapper, type(None))):
            raise RuntimeError("invalid resource {0}".format(resource))

        owner_ptr._stored_resource = resource

    # ポインタオブジェクトに埋め込まれている参照先リソースの取得.
    @staticmethod
    def load_resource(owner_ptr):
        return getattr(owner_ptr, "_stored_resource", None)

    # ポインタオブジェクト間での参照先リソース受け渡し.
    @staticmethod
    def share_resource(src_ptr, dst_ptr):
        dst_ptr._stored_resource = getattr(src_ptr, "_stored_resource", None)

    @staticmethod
    def clear_resource(owner_ptr):
        owner_ptr._stored_resource = None

    # ポインタオブジェクトの参照先取得.
    @staticmethod
    def deref(ptr):
        if not hasattr(ptr, "_stored_resource") or ptr._stored_resource is None:
            # 参照先リソースが埋め込まれていないなら埋め込む.
            _PointerManage.store_instance(ptr, ptr.contents)

        resource = ptr._stored_resource

        instance = resource.deref()
        if instance is None:
            return ptr.contents  # private
        else:
            return instance


class _Referable:

    has_PTR = False

    # 後で機能追加を行うための ポインタ 抽象基底クラス.
    class _PointerBase:
        def as_pycapsule(self):
            PyCapsule_Destructor = _cty.CFUNCTYPE(None, _cty.py_object)
            PyCapsule_New = _cty.pythonapi.PyCapsule_New
            PyCapsule_New.restype = _cty.py_object
            PyCapsule_New.argtypes = (_cty.c_void_p, _cty.c_char_p, PyCapsule_Destructor)
            capsule = PyCapsule_New(self.value, None, PyCapsule_Destructor(0))
            return capsule

    @staticmethod
    def get_ptr_cls(tar_cls):

        # ctypes.Union の派生クラスでは, 存在しない属性を hasattr() 等により確認すると
        # その後 その属性を作成してもアクセスできなくなる( ctypes のバグ ?)
        # そのため PTR 属性の存在確認用フラグ has_PTR を用意している...
        if tar_cls.has_PTR:
            return tar_cls.PTR

        # デバッグ用途でポインタクラス(tar_cls)生成をモニタリング(表示)する場合はここで行うとよい...

        # class attribute ---------------------------------

        tar_cls.PTR = type(
            "LP_" + tar_cls.__name__, (_cty.POINTER(tar_cls),
                                       __class__._PointerBase),
            {"_type_": tar_cls}
            # seealso : PyCPointerType_SetProto() @ cpython/Modules/_ctypes/_ctypes.c
        )

        tar_cls.PTR.has_PTR = False
        tar_cls.PTR._ref_cls = tar_cls

        tar_cls.PTR._spell_py_ = getattr(
            tar_cls, "_spell_py_", tar_cls.__name__) + ".PTR"
        tar_cls.PTR._spell_c_ = getattr(
            tar_cls, "_spell_c_",  tar_cls.__name__) + "*"

        # イテラブルな使われ方を禁止する.
        tar_cls.PTR.__iter__ = None

        # instance property ---------------------------------

        tar_cls.PTR.adrs = property(_Referable.__get_adrs)
        tar_cls.PTR.ref = property(_Referable.__get_adrs)

        def value_getter(self):
            if self:
                return _cty.addressof(self.contents)
            else:
                return None  # NULL

        def value_setter(self, v):
            if not v:
                # NULL ポインタ化.
                _cty_util.null_ptr(self)
                _PointerManage.clear_resource(self)
                return

            if isinstance(v, _cty.c_void_p):
                # void ポインタは任意のポインタ型へ代入可能とする. (c_void_p は _Pointer ではないことに注意)
                v = self.__class__.cast(v)
            elif not _cty_util.is_same_ptr(v.__class__, self.__class__):
                raise RuntimeError(
                    "different pointer type. {0} / {1}".format(self.__class__, v.__class__))

            self.contents = v.contents
            _PointerManage.share_resource(v, self)

        tar_cls.PTR.value = property(value_getter, value_setter)

        # deref.
        def deref_getter(self):
            return _PointerManage.deref(self)

        if issubclass(tar_cls, _cty._Pointer):
            def deref_setter(self, v):
                self.contents.contents = v.contents

        elif issubclass(tar_cls, _Numerical):
            def deref_setter(self, v):
                if isinstance(v, tar_cls._python_type):
                    vobj = v
                else:
                    vobj = tar_cls._convert_from_any(v)

                self.contents.value = vobj
        elif issubclass(tar_cls, _SUBase):
            def deref_setter(self, v):
                instance = _PointerManage.deref(self)

                if isinstance(v, tar_cls):
                    instance._copy_from(v)
                else:
                    instance.value = tar_cls._convert_from_any(v)

        elif hasattr(tar_cls, "value"):
            # FHANDLE, VOID.PTR ...
            def deref_setter(self, v):
                self.contents.value = v

        else:
            def deref_setter(self, v):
                self.contents = _copy.copy(v)

        tar_cls.PTR.deref = property(deref_getter, deref_setter)

        # others ... ---------------------------------

        def _convert_from_any(_cls, any_obj):
            if isinstance(any_obj, _cls):
                return any_obj
            if _cty_util.is_same_size_ptr(any_obj.__class__, _cls):
                return _cls.cast(any_obj)
            if isinstance(any_obj, _cls._ref_cls) and hasattr(any_obj, "ref"):
                return any_obj.ref

            # 算術型ポインタに list, tuple をインスタンス化し設定可能とする.
            if _ENABLE_NUMPY:
                if isinstance(any_obj, (list, tuple)) and issubclass(_cls._ref_cls, _Numerical):
                    any_obj = _np.array(
                        any_obj, dtype=_cls._ref_cls._numpy_type)

                if isinstance(any_obj, _np.ndarray):
                    # Numpy が有効であれば ndarray も対応.
                    return _attach_ndarray_to_ptr(any_obj, _cls)
            else:
                if isinstance(any_obj, (list, tuple)) and issubclass(_cls._ref_cls, _Numerical):
                    shape = _util.calc_sequence_shape(any_obj)

                    array_instance = _cls._ref_cls.ARRAY(*shape)
                    _util.copy_sequence(
                        any_obj, array_instance, _cls._ref_cls._python_type)

                    ptr_obj = array_instance.ref
                    # avoid GC.
                    _PointerManage.store_private(ptr_obj, array_instance)
                    return ptr_obj

            # int からポインタ型への変換は禁止。issue #12 参照
            if issubclass(_cls, _cty._Pointer) and isinstance(any_obj, int):
                raise TypeError("wrong type")

            return _cls.cast(any_obj)
        tar_cls.PTR._convert_from_any = classmethod(_convert_from_any)

        def _cast(cls, ptr_obj):
            """
            cast another pointer instance(ptr_obj) to this pointer instance.
            """
            return _cty.cast(ptr_obj, cls)
        tar_cls.PTR.cast = classmethod(_cast)

        tar_cls.PTR.from_param = _Referable._from_param(tar_cls.PTR)

        tar_cls.PTR.__add__ = lambda self, other: _cty_util.ptr_inc(
            self,  other)
        tar_cls.PTR.__sub__ = lambda self, other: _cty_util.ptr_inc(
            self, -other)

        if _ENABLE_NUMPY and issubclass(tar_cls, _Numerical):
            def _ndarray(self, num):
                """
                attach to ndarray. shape is (num, )
                """
                return _attach_ptr_to_ndarray(self, num)
            tar_cls.PTR.ndarray = _ndarray

        tar_cls.has_PTR = True

        return tar_cls.PTR

    @classmethod
    def bless_ptr(cls, ptr_depth=2):
        t = cls
        for i in range(ptr_depth):
            t = _Referable.get_ptr_cls(t)

    def __get_adrs(self):
        ptr_cls = None
        if hasattr(self, "PTR"):
            ptr_cls = self.PTR
        else:
            ptr_cls = _Referable.get_ptr_cls(self.__class__)

        ptr_obj = ptr_cls(self)
        _PointerManage.store_instance(ptr_obj, self)
        return ptr_obj

    @property
    def adrs(self): return self.__get_adrs()

    @property
    def ref(self): return self.__get_adrs()

    @staticmethod
    def _from_param(ptr_cls):
        org_from_param = ptr_cls.from_param

        def _wrap_from_param(cls, obj):
            if isinstance(obj, cls):
                return obj
            if isinstance(obj, cls._ref_cls):
                return obj.ref
            if isinstance(obj, _cty.Array) and hasattr(obj, "ref"):
                # 配列はポインタ型に変換して同様にチェック
                obj_as_ptr = obj.ref
                if isinstance(obj_as_ptr, cls):
                    return obj_as_ptr
                if isinstance(obj_as_ptr, cls._ref_cls):
                    return obj_as_ptr.ref

            try:
                return cls._convert_from_any(obj)
            except Exception:
                pass

            return org_from_param(obj)

        return classmethod(_wrap_from_param)


class _Numerical:

    def __init__(self, val=0):
        if not isinstance(val, self._python_type):
            val = self._python_type(val)
        super().__init__(val)

    @staticmethod
    def create_cls(cls_name, ctypes_cls):  # Factory for this class.
        new_cls = type(cls_name, (_Numerical, ctypes_cls,
                                  _Referable, _Arrayble, _FromParamSentinel), {})

        new_cls._spell_py_ = cls_name
        new_cls._spell_c_ = cls_name

        # value property ...
        new_cls.__value_org = new_cls.value

        def value_getter(self):
            return self.__value_org

        def value_setter(self, v):
            if not isinstance(v, self._python_type):
                v = self._convert_from_any(v)
            self.__value_org = v

        new_cls.value = property(value_getter, value_setter)

        # ポインタ派生型を生成...
        new_cls.bless_ptr()

        # 型変換を可能にする...
        new_cls._python_type = {
            _cty.c_bool: int,
            _cty.c_char: int,
            _cty.c_byte: int,
            _cty.c_ubyte: int,
            _cty.c_short: int,
            _cty.c_ushort: int,
            _cty.c_int: int,
            _cty.c_uint: int,
            _cty.c_long: int,
            _cty.c_ulong: int,
            _cty.c_longlong: int,
            _cty.c_ulonglong: int,
            _cty.c_float: float,
            _cty.c_double: float,
            _cty.c_longdouble: float
        }.get(ctypes_cls, None)

        if _ENABLE_NUMPY:
            new_cls._numpy_type = {
                _cty.c_bool: _np.int8,
                _cty.c_char: _np.int8,
                _cty.c_byte: _np.int8,
                _cty.c_ubyte: _np.uint8,
                _cty.c_short: _np.int16,
                _cty.c_ushort: _np.uint16,
                _cty.c_int: _np.int32,
                _cty.c_uint: _np.uint32,
                # _cty.c_long       : int,
                # _cty.c_ulong      : int,
                # _cty.c_longlong   : int,
                # _cty.c_ulonglong  : int,
                _cty.c_float: _np.float32,
                _cty.c_double: _np.float64
            }.get(ctypes_cls, None)

        return new_cls

    _python_type = None
    _numpy_type = None

    @classmethod
    def _convert_from_any(cls, any_obj):
        if isinstance(any_obj, cls):
            return any_obj

        if isinstance(any_obj, _cty._SimpleCData):
            val = any_obj.value
        elif isinstance(any_obj, str) and _util._is_toplevel(any_obj):
            # 文字列が定義された定数名であれば数値に変換.
            val = _util._get_toplevel(any_obj)
        else:
            val = any_obj

        return cls(cls._python_type(val))

    # param .......

    @classmethod
    def from_param(cls, obj):
        if isinstance(obj, cls):
            return super().from_param(obj)

        try:
            conv_obj = cls._convert_from_any(obj)
        except Exception:
            conv_obj = None

        return super().from_param(conv_obj)

    # repr and format .......

    def __repr__(self):
        return str(self.value)

    def __format__(self, spec):
        return self.value.__format__(spec)

    # operations .......
    # 演算結果は常に python 組み込み型とする. (ただし代入演算子を除く.)

    @staticmethod
    def __ope_lr(self, other, ope):  # ex) self + other.
        if isinstance(other, _cty._SimpleCData):
            other = other.value

        return ope(self.value, other)

    @staticmethod
    def __ope_i(self, other, ope):  # ex) self += other.
        if isinstance(other, _cty._SimpleCData):
            other = other.value

        self.value = self.value.__class__(ope(self.value, other))
        return self

    def __add__(self, other):
        return _Numerical.__ope_lr(self, other, lambda s, o: s + o)

    def __radd__(self, other):
        return _Numerical.__ope_lr(self, other, lambda s, o: o + s)

    def __iadd__(self, other):
        return _Numerical.__ope_i(self, other, lambda s, o: s + o)

    def __sub__(self, other):
        return _Numerical.__ope_lr(self, other, lambda s, o: s - o)

    def __rsub__(self, other):
        return _Numerical.__ope_lr(self, other, lambda s, o: o - s)

    def __isub__(self, other):
        return _Numerical.__ope_i(self, other, lambda s, o: s - o)

    def __mul__(self, other):
        return _Numerical.__ope_lr(self, other, lambda s, o: s * o)

    def __rmul__(self, other):
        return _Numerical.__ope_lr(self, other, lambda s, o: o * s)

    def __imul__(self, other):
        return _Numerical.__ope_i(self, other, lambda s, o: s * o)

    def __truediv__(self, other):
        return _Numerical.__ope_lr(self, other, lambda s, o: s / o)

    def __rtruediv__(self, other):
        return _Numerical.__ope_lr(self, other, lambda s, o: o / s)

    def __itruediv__(self, other):
        return _Numerical.__ope_i(self, other, lambda s, o: s / o)

    def __floordiv__(self, other):
        return _Numerical.__ope_lr(self, other, lambda s, o: s // o)

    def __rfloordiv__(self, other):
        return _Numerical.__ope_lr(self, other, lambda s, o: o // s)

    def __ifloordiv__(self, other):
        return _Numerical.__ope_i(self, other, lambda s, o: s // o)

    def __mod__(self, other):
        return _Numerical.__ope_lr(self, other, lambda s, o: s % o)

    def __rmod__(self, other):
        return _Numerical.__ope_lr(self, other, lambda s, o: o % s)

    def __imod__(self, other):
        return _Numerical.__ope_i(self, other, lambda s, o: s % o)

    def __mod__(self, other):
        return _Numerical.__ope_lr(self, other, lambda s, o: s % o)

    def __rmod__(self, other):
        return _Numerical.__ope_lr(self, other, lambda s, o: o % s)

    def __imod__(self, other):
        return _Numerical.__ope_i(self, other, lambda s, o: s % o)

    def __pow__(self, other):
        return _Numerical.__ope_lr(self, other, lambda s, o: s ** o)

    def __rpow__(self, other):
        return _Numerical.__ope_lr(self, other, lambda s, o: o ** s)

    def __ipow__(self, other):
        return _Numerical.__ope_i(self, other, lambda s, o: s ** o)

    def __lshift__(self, other):
        return _Numerical.__ope_lr(self, other, lambda s, o: s << o)

    def __rlshift__(self, other):
        return _Numerical.__ope_lr(self, other, lambda s, o: o << s)

    def __ilshift__(self, other):
        return _Numerical.__ope_i(self, other, lambda s, o: s << o)

    def __rshift__(self, other):
        return _Numerical.__ope_lr(self, other, lambda s, o: s >> o)

    def __rrshift__(self, other):
        return _Numerical.__ope_lr(self, other, lambda s, o: o >> s)

    def __irshift__(self, other):
        return _Numerical.__ope_i(self, other, lambda s, o: s >> o)

    def __and__(self, other):
        return _Numerical.__ope_lr(self, other, lambda s, o: s & o)

    def __rand__(self, other):
        return _Numerical.__ope_lr(self, other, lambda s, o: o & s)

    def __iand__(self, other):
        return _Numerical.__ope_i(self, other, lambda s, o: s & o)

    def __xor__(self, other):
        return _Numerical.__ope_lr(self, other, lambda s, o: s ^ o)

    def __rxor__(self, other):
        return _Numerical.__ope_lr(self, other, lambda s, o: o ^ s)

    def __ixor__(self, other):
        return _Numerical.__ope_i(self, other, lambda s, o: s ^ o)

    def __or__(self, other):
        return _Numerical.__ope_lr(self, other, lambda s, o: s | o)

    def __ror__(self, other):
        return _Numerical.__ope_lr(self, other, lambda s, o: o | s)

    def __ior__(self, other):
        return _Numerical.__ope_i(self, other, lambda s, o: s | o)

    def __pos__(self):
        return +self.value

    def __neg__(self):
        return -self.value

    def __int__(self):
        return int(self.value)

    def __float__(self):
        return float(self.value)

    def __index__(self):
        return int(self.value)

    def __lt__(self, other):
        return _Numerical.__ope_lr(self, other, lambda s, o: s < o)

    def __le__(self, other):
        return _Numerical.__ope_lr(self, other, lambda s, o: s <= o)

    def __eq__(self, other):
        return _Numerical.__ope_lr(self, other, lambda s, o: s == o)

    def __ne__(self, other):
        return _Numerical.__ope_lr(self, other, lambda s, o: s != o)

    def __gt__(self, other):
        return _Numerical.__ope_lr(self, other, lambda s, o: s > o)

    def __ge__(self, other):
        return _Numerical.__ope_lr(self, other, lambda s, o: s >= o)


class _Arrayble:

    @staticmethod
    def __array_repr(self):
        res = []
        for i in self:
            res.append(i.__repr__())

        return "[ " + ', '.join(res) + " ]"

    @staticmethod
    def __value_getter(self):
        new_ary = self.__class__()
        _util.copy_sequence(self, new_ary)
        return new_ary

    @staticmethod
    def __value_setter(self, v):
        _util.copy_sequence(v, self)

    @staticmethod
    def create_1dim_cls(cls, size):
        array_cls = cls * size
        array_cls.__repr__ = _Arrayble.__array_repr

        def adrs_getter(self):
            elem_ptr_cls = _Referable.get_ptr_cls(self._elem_type_)
            return elem_ptr_cls.cast(_cty.addressof(self))

        array_cls.adrs = property(adrs_getter)
        array_cls.ref = array_cls.adrs

        def _wrap_setitem(self, key, val):
            elem_cls = cls
            # 現状 スライス 時の型変換は未対応.
            if not isinstance(key, slice) and hasattr(elem_cls, "_convert_from_any"):
                val = elem_cls._convert_from_any(val)
            super(array_cls, self).__setitem__(key, val)

        array_cls.__setitem__ = _wrap_setitem

        array_cls.value = property(
            _Arrayble.__value_getter, _Arrayble.__value_setter)

        if _ENABLE_PYPLOT and hasattr(cls, "plot"):
            def _plot_array(self, plot_obj=None, num=None, pattern_obj=None, **kwargs):
                if num is None:
                    num = len(self)
                return self.ref.plot(num, plot_obj=plot_obj, pattern_obj=pattern_obj, **kwargs)

            array_cls.plot = _plot_array

        return array_cls

    @staticmethod
    def create_cls(cls, *size):
        """
        T.ARRAY( 5 )      ... T[5]
        T.ARRAY( 2, 3 )   ... T[2][3]
        """

        array_cls = cls
        for sz in size[::-1]:
            array_cls = _Arrayble.create_1dim_cls(array_cls, sz)
            array_cls._elem_type_ = cls

        array_cls._shape_ = tuple(size)

        sufix = ".ARRAY({0})".format(",".join([str(i) for i in size]))
        array_cls._spell_py_ = getattr(cls, "_spell_py_", cls.__name__) + sufix

        sufix = "".join(["[{0}]".format(i) for i in size])
        array_cls._spell_c_ = getattr(cls, "_spell_c_", cls.__name__) + sufix

        conv_type = getattr(cls, "_python_type", None)

        def _convert_from_any(_cls, any_obj):
            if isinstance(any_obj, _cls):
                return any_obj

            new_array = _cls()
            _util.copy_sequence(any_obj, new_array, conv_type)

            return new_array
        array_cls._convert_from_any = classmethod(_convert_from_any)

        def from_param(cls, obj):
            if not isinstance(obj, cls):
                obj = cls._convert_from_any(obj)

            return obj
        array_cls.from_param = classmethod(from_param)

        # operator overload
        array_cls.__add__ = _Arrayble.__add__
        array_cls.__radd__ = _Arrayble.__radd__
        array_cls.__iadd__ = _Arrayble.__iadd__
        array_cls.__sub__ = _Arrayble.__sub__
        array_cls.__rsub__ = _Arrayble.__rsub__
        array_cls.__isub__ = _Arrayble.__isub__
        array_cls.__mul__ = _Arrayble.__mul__
        array_cls.__rmul__ = _Arrayble.__rmul__
        array_cls.__imul__ = _Arrayble.__imul__
        array_cls.__truediv__ = _Arrayble.__truediv__
        array_cls.__rtruediv__ = _Arrayble.__rtruediv__
        array_cls.__itruediv__ = _Arrayble.__itruediv__
        array_cls.__floordiv__ = _Arrayble.__floordiv__
        array_cls.__rfloordiv__ = _Arrayble.__rfloordiv__
        array_cls.__ifloordiv__ = _Arrayble.__ifloordiv__
        array_cls.__mod__ = _Arrayble.__mod__
        array_cls.__rmod__ = _Arrayble.__rmod__
        array_cls.__imod__ = _Arrayble.__imod__
        array_cls.__mod__ = _Arrayble.__mod__
        array_cls.__rmod__ = _Arrayble.__rmod__
        array_cls.__imod__ = _Arrayble.__imod__
        array_cls.__pow__ = _Arrayble.__pow__
        array_cls.__rpow__ = _Arrayble.__rpow__
        array_cls.__ipow__ = _Arrayble.__ipow__
        array_cls.__lshift__ = _Arrayble.__lshift__
        array_cls.__rlshift__ = _Arrayble.__rlshift__
        array_cls.__ilshift__ = _Arrayble.__ilshift__
        array_cls.__rshift__ = _Arrayble.__rshift__
        array_cls.__rrshift__ = _Arrayble.__rrshift__
        array_cls.__irshift__ = _Arrayble.__irshift__
        array_cls.__and__ = _Arrayble.__and__
        array_cls.__rand__ = _Arrayble.__rand__
        array_cls.__iand__ = _Arrayble.__iand__
        array_cls.__xor__ = _Arrayble.__xor__
        array_cls.__rxor__ = _Arrayble.__rxor__
        array_cls.__ixor__ = _Arrayble.__ixor__
        array_cls.__or__ = _Arrayble.__or__
        array_cls.__ror__ = _Arrayble.__ror__
        array_cls.__ior__ = _Arrayble.__ior__
        array_cls.__pos__ = _Arrayble.__pos__
        array_cls.__neg__ = _Arrayble.__neg__

        return array_cls

    @classmethod
    def ARRAY(cls, *size):
        """
        T.ARRAY( 5 )      ... T[5]
        T.ARRAY( 2, 3 )   ... T[2][3]
        """

        array_cls = _Arrayble.create_cls(cls, *size)
        return array_cls()

    @staticmethod
    def __ope_lr(self, other, ope):  # ex) self + other.
        is_same_type = type(self) is type(other) and hasattr(self, "_shape_") and hasattr(other, "_shape_")
        is_other_numeric = isinstance(other, (int, float, _cty._SimpleCData))
        if not is_same_type and not is_other_numeric:
            raise TypeError(f"unsupported operand type(s): '{self.__class__.__name__}' and '{other.__class__.__name__}'")
        
        # new_obj = self[0].__class__.ARRAY(*self._shape_)
        new_obj = self.__class__()
        if is_same_type:
            assert self._shape_ == other._shape_  # 型が同じなので、サイズも同じはず...
            for idx in range(self._shape_[0]):
                new_obj[idx] = ope(self[idx], other[idx])
        else:
            if isinstance(other, _cty._SimpleCData):
                other_val = other.value
            else:
                other_val = other
            for idx in range(self._shape_[0]):
                new_obj[idx] = ope(self[idx], other_val)
        return new_obj

    @staticmethod
    def __ope_i(self, other, ope):  # ex) self += other.
        is_same_type = type(self) is type(other) and hasattr(self, "_shape_") and hasattr(other, "_shape_")
        is_other_numeric = isinstance(other, (int, float, _cty._SimpleCData))
        if not is_same_type and not is_other_numeric:
            raise TypeError(f"unsupported operand type(s): '{self.__class__.__name__}' and '{other.__class__.__name__}'")
        
        if is_same_type:
            assert self._shape_ == other._shape_
            for idx in range(self._shape_[0]):
                self[idx] = ope(self[idx], other[idx])
        else:
            if isinstance(other, _cty._SimpleCData):
                other_val = other.value
            else:
                other_val = other
            for idx in range(self._shape_[0]):
                self[idx] = ope(self[idx], other_val)
        return self

    def __add__(self, other):
        return _Arrayble.__ope_lr(self, other, lambda s, o: s + o)

    def __radd__(self, other):
        return _Arrayble.__ope_lr(self, other, lambda s, o: o + s)

    def __iadd__(self, other):
        return _Arrayble.__ope_i(self, other, lambda s, o: s + o)

    def __sub__(self, other):
        return _Arrayble.__ope_lr(self, other, lambda s, o: s - o)

    def __rsub__(self, other):
        return _Arrayble.__ope_lr(self, other, lambda s, o: o - s)

    def __isub__(self, other):
        return _Arrayble.__ope_i(self, other, lambda s, o: s - o)

    def __mul__(self, other):
        return _Arrayble.__ope_lr(self, other, lambda s, o: s * o)

    def __rmul__(self, other):
        return _Arrayble.__ope_lr(self, other, lambda s, o: o * s)

    def __imul__(self, other):
        return _Arrayble.__ope_i(self, other, lambda s, o: s * o)

    def __truediv__(self, other):
        return _Arrayble.__ope_lr(self, other, lambda s, o: s / o)

    def __rtruediv__(self, other):
        return _Arrayble.__ope_lr(self, other, lambda s, o: o / s)

    def __itruediv__(self, other):
        return _Arrayble.__ope_i(self, other, lambda s, o: s / o)

    def __floordiv__(self, other):
        return _Arrayble.__ope_lr(self, other, lambda s, o: s // o)

    def __rfloordiv__(self, other):
        return _Arrayble.__ope_lr(self, other, lambda s, o: o // s)

    def __ifloordiv__(self, other):
        return _Arrayble.__ope_i(self, other, lambda s, o: s // o)

    def __mod__(self, other):
        return _Arrayble.__ope_lr(self, other, lambda s, o: s % o)

    def __rmod__(self, other):
        return _Arrayble.__ope_lr(self, other, lambda s, o: o % s)

    def __imod__(self, other):
        return _Arrayble.__ope_i(self, other, lambda s, o: s % o)

    def __mod__(self, other):
        return _Arrayble.__ope_lr(self, other, lambda s, o: s % o)

    def __rmod__(self, other):
        return _Arrayble.__ope_lr(self, other, lambda s, o: o % s)

    def __imod__(self, other):
        return _Arrayble.__ope_i(self, other, lambda s, o: s % o)

    def __pow__(self, other):
        return _Arrayble.__ope_lr(self, other, lambda s, o: s ** o)

    def __rpow__(self, other):
        return _Arrayble.__ope_lr(self, other, lambda s, o: o ** s)

    def __ipow__(self, other):
        return _Arrayble.__ope_i(self, other, lambda s, o: s ** o)

    def __lshift__(self, other):
        return _Arrayble.__ope_lr(self, other, lambda s, o: s << o)

    def __rlshift__(self, other):
        return _Arrayble.__ope_lr(self, other, lambda s, o: o << s)

    def __ilshift__(self, other):
        return _Arrayble.__ope_i(self, other, lambda s, o: s << o)

    def __rshift__(self, other):
        return _Arrayble.__ope_lr(self, other, lambda s, o: s >> o)

    def __rrshift__(self, other):
        return _Arrayble.__ope_lr(self, other, lambda s, o: o >> s)

    def __irshift__(self, other):
        return _Arrayble.__ope_i(self, other, lambda s, o: s >> o)

    def __and__(self, other):
        return _Arrayble.__ope_lr(self, other, lambda s, o: s & o)

    def __rand__(self, other):
        return _Arrayble.__ope_lr(self, other, lambda s, o: o & s)

    def __iand__(self, other):
        return _Arrayble.__ope_i(self, other, lambda s, o: s & o)

    def __xor__(self, other):
        return _Arrayble.__ope_lr(self, other, lambda s, o: s ^ o)

    def __rxor__(self, other):
        return _Arrayble.__ope_lr(self, other, lambda s, o: o ^ s)

    def __ixor__(self, other):
        return _Arrayble.__ope_i(self, other, lambda s, o: s ^ o)

    def __or__(self, other):
        return _Arrayble.__ope_lr(self, other, lambda s, o: s | o)

    def __ror__(self, other):
        return _Arrayble.__ope_lr(self, other, lambda s, o: o | s)

    def __ior__(self, other):
        return _Arrayble.__ope_i(self, other, lambda s, o: s | o)

    def __pos__(self):
        return self + 0

    def __neg__(self):
        return self * -1

class _VoidPointer(_cty.c_void_p, _Referable, _Referable._PointerBase, _Arrayble):

    @classmethod
    def cast(cls, obj):
        return _cty.cast(obj, cls)

    @classmethod
    def from_param(cls, obj):
        try:
            return super().from_param(obj)
        except Exception as e:
            # PyCapsule
            capsule = obj
            try:
                adrs = _cty_util.get_address_from_pycapsule(capsule)
                return _cty.cast(adrs, cls)
            except Exception:
                pass

            # py::capsule of pybind11
            try:
                return _cty.cast(capsule.get_pointer(), cls)
            except Exception:
                pass
            raise e

    # ... void ポインタ配列の要素に他のポインタを代入可能にするため.
    @classmethod
    def _convert_from_any(cls, any_obj):
        if isinstance(any_obj, cls):
            return any_obj

        try:
            return _cty.cast(any_obj, cls)
        except _cty.ArgumentError as e:
            # PyCapsule
            capsule = any_obj
            try:
                adrs = _cty_util.get_address_from_pycapsule(capsule)
                return _cty.cast(adrs, cls)
            except Exception:
                pass

            # py::capsule of pybind11
            try:
                return _cty.cast(capsule.get_pointer(), cls)
            except Exception:
                pass
            raise e


class _SUBase:  # base class of Struct and Union.

    # Factory for struct and union. ---------------------------------

    def _init_fields_resource_repos(self, src_fields, src_fields_dict):
        resource_dict = {}
        for field_name, field_type in self._fields_:
            if _cty_util.is_ptr_cls(field_type):
                resource_dict[field_name] = None  # ポインタフィールドのみ登録場所を用意.

        self._resource_dict = resource_dict

        # 初期リソースを設定
        initial_fields = {}
        for obj, (field_name, _) in zip(src_fields, self._fields_):
            initial_fields[field_name] = obj
        for field_name, obj in src_fields_dict.items():
            initial_fields["_" + field_name] = obj
        for field_name, obj in initial_fields.items():
            self._field_resource_store(field_name, obj)

    def _field_resource_store(self, field_name, field_obj):
        if not hasattr(self, "_resource_dict"):
            return
        if field_name in self._resource_dict:
            self._resource_dict[field_name] = _PointerManage.load_resource(
                field_obj)

    def _field_resource_apply(self, field_name, field_obj):
        if not hasattr(self, "_resource_dict"):
            return
        if field_name in self._resource_dict:
            _PointerManage.apply_resource(
                field_obj, self._resource_dict.get(field_name, None)
            )

    @staticmethod
    def _gen_field_getter(field_name):
        def getter(self):
            field_obj = getattr(self, field_name)
            self._field_resource_apply(field_name, field_obj)
            return field_obj
        return getter

    @staticmethod
    def _gen_field_setter(field_name):
        def setter(self, v):
            try:
                setattr(self, field_name, v)
                self._field_resource_store(field_name, v)
                return
            except Exception:
                pass

            field_info = self._wrap_fields_.get(field_name, None)

            try:
                conv_v = field_info["type"]._convert_from_any(v)
                setattr(self, field_name, conv_v)
                self._field_resource_store(field_name, conv_v)
                return
            except Exception:
                pass

            raise RuntimeError("{0} can't assign {1}".format(v, field_name))

        return setter

    @staticmethod
    def _wrap_field_item(field_name, field_type_cls):
        return {"public_name": field_name, "private_name": "_" + field_name, "type": field_type_cls}

    @staticmethod
    def _create_cls(cls_name, base_cls, pack_size, wrap_fields_list):
        if base_cls not in (_StructBase, _UnionBase):
            raise RuntimeError("{0} is not struct/union".format(base_cls))

        su_cls = type(cls_name, (base_cls, ), {})
        su_cls._pack_ = pack_size

        su_cls._spell_py_ = cls_name
        su_cls._spell_c_ = cls_name

        reserved_word = ("_fields_", "_wrap_fields_", "value",
                         "bless_ptr", "__doc__", "plot", "ref", "ARRAY")

        fields_list = []
        wrap_field_dict = {}
        for field in wrap_fields_list:
            wrap_field_name = field["public_name"]
            priv_field_name = field["private_name"]

            # クラスの属性名 (adrs 等) と構造体メンバ名が衝突していた場合 メンバ名を変更する.
            if hasattr(su_cls, wrap_field_name) or (wrap_field_name in reserved_word):
                _dbg.DEBUG_PRINT("> (!!) Confilict and Change field_name {0} -> {1} / {2}".format(
                    wrap_field_name, "m_" + wrap_field_name, cls_name))
                wrap_field_name = "m_" + wrap_field_name
                priv_field_name = "m_" + priv_field_name

                if _dbg.ENABLE_DEBUG:
                    if hasattr(su_cls, wrap_field_name):
                        _dbg.DEBUG_PRINT(
                            "> (!!) Unsolved Confilict field_name {0} @{1}".format(
                                wrap_field_name, cls_name))
                    if hasattr(su_cls, priv_field_name):
                        _dbg.DEBUG_PRINT(
                            "> (!!) Unsolved Confilict field_name {0} @{1}".format(
                                priv_field_name, cls_name))

            field_cls = field["type"]

            field_getter = _SUBase._gen_field_getter(priv_field_name)
            field_setter = _SUBase._gen_field_setter(priv_field_name)
            setattr(
                su_cls, wrap_field_name,
                property(field_getter, field_setter)
            )

            fields_list.append((priv_field_name, field_cls))

            wrap_field_dict[priv_field_name] = {
                "type": field_cls, "field_name": wrap_field_name}

        su_cls._fields_ = fields_list
        su_cls._wrap_fields_ = wrap_field_dict

        # value 属性による構造体/共用体の一括代入を可能にする.
        def value_getter(self):
            new_obj = self.__class__()
            new_obj._copy_from(self)
            return new_obj

        def value_setter(self, v):
            if self.__class__ != v.__class__:
                v = self._convert_from_any(v)
            self._copy_from(v)
        su_cls.value = property(value_getter, value_setter)

        su_cls.bless_ptr()
        su_cls.__doc__ = "\n" + cls_name + " :\n" + su_cls._class_repr(3)

        return su_cls

    # -----------------------------------------------------------------------------

    def _copy_from(self, other):
        if self.__class__ != other.__class__:
            raise RuntimeError("{0} is not {1}".format(
                other.__class__, self.__class__))

        for field_name in [field["field_name"] for field in self._wrap_fields_.values()]:
            # HACK: 稀にgetattrにてAttributeErrorが発生することがある問題への対策。 see also: !44
            field_name = (field_name + " ")[:-1]
            setattr(self, field_name, getattr(other, field_name))

    def _fields_repr(self, indent=0):
        repr_str = ""
        indent_str = " " * indent

        for private_name, dummy in self._fields_:
            field_name = self._wrap_fields_[private_name]["field_name"]
            field_cls = self._wrap_fields_[private_name]["type"]
            field_cls_spell = getattr(
                field_cls, "_spell_py_", field_cls.__name__)
            if issubclass(field_cls, _SUBase):
                repr_str += indent_str + \
                    "{0} {1} :\n".format(field_cls_spell, field_name)
                field_obj = getattr(self, field_name)
                repr_str += field_obj._fields_repr(indent +
                                                   len(field_cls_spell))
            else:
                repr_str += indent_str + " {0} {1} = {2}\n".format(
                    field_cls_spell, field_name, repr(getattr(self, field_name, "")))

        return repr_str

    @classmethod
    def _class_repr(cls, indent=0):
        repr_str = ""
        indent_str = " " * indent

        for private_name, dummy in cls._fields_:
            field_name = cls._wrap_fields_[private_name]["field_name"]
            field_cls = cls._wrap_fields_[private_name]["type"]
            field_cls_spell = getattr(
                field_cls, "_spell_py_", field_cls.__name__)
            if issubclass(field_cls, _SUBase):
                repr_str += indent_str + \
                    "{0} {1} :\n".format(field_cls_spell, field_name)
                repr_str += field_cls._class_repr(indent +
                                                  len(field_cls_spell))
            else:
                repr_str += indent_str + \
                    " {0} {1}\n".format(field_cls_spell, field_name)

        return repr_str

    @classmethod
    def _get_field_type(cls, field_name):
        # 指定されたフィールド名のタイプを返す.
        for field_info in cls._wrap_fields_.values():
            if field_name == field_info["field_name"]:
                return field_info["type"]

        raise RuntimeError("{0} not has {1}".format(cls, field_name))

    @classmethod
    def _adjust_fields(cls, src_fields, src_fields_dict):
        # リスト src_fields と辞書 src_fields_dict を構造体定義に適応するフィールドのリストに変換する.
        def get_legal_obj(dst_type, src_obj):
            if isinstance(src_obj, dst_type):
                return src_obj

            if hasattr(dst_type, "_python_type") and isinstance(src_obj, dst_type._python_type):
                return src_obj

            if hasattr(dst_type, "_convert_from_any"):
                try:
                    return dst_type._convert_from_any(src_obj)
                except Exception:
                    pass

            # あきらめる
            return src_obj

        legal_fields = []

        for i in range(min(len(cls._fields_), len(src_fields))):
            field_type = cls._fields_[i][1]
            src_obj = src_fields[i]

            legal_fields.append(get_legal_obj(field_type, src_obj))

        legal_fields_dict = {}

        for public_field_name, src_obj in src_fields_dict.items():
            priv_field_name = "_" + public_field_name
            field_info = cls._wrap_fields_.get(priv_field_name, None)
            if field_info is not None:
                legal_obj = get_legal_obj(field_info["type"], src_obj)
            else:
                # あきらめる
                legal_obj = src_obj
            legal_fields_dict[public_field_name] = legal_obj

        return (legal_fields, legal_fields_dict)

    @classmethod
    def _convert_from_any(cls, any_obj):
        if isinstance(any_obj, cls):
            return any_obj

        if isinstance(any_obj, (list, tuple)):
            # リストが渡された場合はコンストラクタ引数とみなし構造体を生成.
            return cls(*any_obj)

        if isinstance(any_obj, dict):
            # ディクショナリが渡された場合はコンストラクタ引数とみなし構造体を生成.
            return cls(**any_obj)

        if _ENABLE_NUMPY:
            if isinstance(any_obj, _np.ndarray):
                # ndarray が渡された場合はコンストラクタ引数とみなし構造体を生成.
                return cls(*any_obj.tolist())

        return any_obj

    @classmethod
    def from_param(cls, obj):
        return super().from_param(cls._convert_from_any(obj))

    @classmethod
    def is_plottable(cls):
        return hasattr(cls, "plot")


class _StructBase(_cty.Structure, _SUBase, _Referable, _Arrayble, _FromParamSentinel):

    @staticmethod
    def _create_cls(struct_name, pack_size, wrap_fields_list):
        return _SUBase._create_cls(struct_name, _StructBase, pack_size, wrap_fields_list)

    def __repr__(self, indent=0):
        repr_str = self.__class__.__name__ + " :\n"
        return repr_str + self._fields_repr(indent + 3)

    def __init__(self, *args, **kwargs):
        adjust_args, adjust_kwargs = self._adjust_fields(args, kwargs)
        super().__init__(*adjust_args, **adjust_kwargs)
        self._init_fields_resource_repos(adjust_args, adjust_kwargs)

    @staticmethod
    def __ope_lr(self, other, ope):  # ex) self + other.
        is_same_type = type(self) is type(other)
        is_other_numeric = isinstance(other, (int, float, _cty._SimpleCData))
        if not is_same_type and not is_other_numeric:
            raise TypeError(f"unsupported operand type(s): '{self.__class__.__name__}' and '{other.__class__.__name__}'")
        new_obj = self.__class__()
        if is_same_type:
            for field_name in [field["field_name"] for field in self._wrap_fields_.values()]:
                self_field = getattr(self, field_name)
                other_field = getattr(other, field_name)
                setattr(new_obj, field_name, ope(self_field, other_field))
        else:
            if isinstance(other, _cty._SimpleCData):
                other_val = other.value
            else:
                other_val = other
            for field_name in [field["field_name"] for field in self._wrap_fields_.values()]:
                self_field = getattr(self, field_name)
                setattr(new_obj, field_name, ope(self_field, other_val))
            
        return new_obj

    @staticmethod
    def __ope_i(self, other, ope):  # ex) self += other.
        is_same_type = type(self) is type(other)
        is_other_numeric = isinstance(other, (int, float, _cty._SimpleCData))
        if not is_same_type and not is_other_numeric:
            raise TypeError(f"unsupported operand type(s): '{self.__class__.__name__}' and '{other.__class__.__name__}'")
        if is_same_type:
            for field_name in [field["field_name"] for field in self._wrap_fields_.values()]:
                self_field = getattr(self, field_name)
                other_field = getattr(other, field_name)
                setattr(self, field_name, ope(self_field, other_field))
        else:
            if isinstance(other, _cty._SimpleCData):
                other_val = other.value
            else:
                other_val = other
            for field_name in [field["field_name"] for field in self._wrap_fields_.values()]:
                self_field = getattr(self, field_name)
                setattr(self, field_name, ope(self_field, other_val))
        return self

    def __add__(self, other):
        return _StructBase.__ope_lr(self, other, lambda s, o: s + o)

    def __radd__(self, other):
        return _StructBase.__ope_lr(self, other, lambda s, o: o + s)

    def __iadd__(self, other):
        return _StructBase.__ope_i(self, other, lambda s, o: s + o)

    def __sub__(self, other):
        return _StructBase.__ope_lr(self, other, lambda s, o: s - o)

    def __rsub__(self, other):
        return _StructBase.__ope_lr(self, other, lambda s, o: o - s)

    def __isub__(self, other):
        return _StructBase.__ope_i(self, other, lambda s, o: s - o)

    def __mul__(self, other):
        return _StructBase.__ope_lr(self, other, lambda s, o: s * o)

    def __rmul__(self, other):
        return _StructBase.__ope_lr(self, other, lambda s, o: o * s)

    def __imul__(self, other):
        return _StructBase.__ope_i(self, other, lambda s, o: s * o)

    def __truediv__(self, other):
        return _StructBase.__ope_lr(self, other, lambda s, o: s / o)

    def __rtruediv__(self, other):
        return _StructBase.__ope_lr(self, other, lambda s, o: o / s)

    def __itruediv__(self, other):
        return _StructBase.__ope_i(self, other, lambda s, o: s / o)

    def __floordiv__(self, other):
        return _StructBase.__ope_lr(self, other, lambda s, o: s // o)

    def __rfloordiv__(self, other):
        return _StructBase.__ope_lr(self, other, lambda s, o: o // s)

    def __ifloordiv__(self, other):
        return _StructBase.__ope_i(self, other, lambda s, o: s // o)

    def __mod__(self, other):
        return _StructBase.__ope_lr(self, other, lambda s, o: s % o)

    def __rmod__(self, other):
        return _StructBase.__ope_lr(self, other, lambda s, o: o % s)

    def __imod__(self, other):
        return _StructBase.__ope_i(self, other, lambda s, o: s % o)

    def __mod__(self, other):
        return _StructBase.__ope_lr(self, other, lambda s, o: s % o)

    def __rmod__(self, other):
        return _StructBase.__ope_lr(self, other, lambda s, o: o % s)

    def __imod__(self, other):
        return _StructBase.__ope_i(self, other, lambda s, o: s % o)

    def __pow__(self, other):
        return _StructBase.__ope_lr(self, other, lambda s, o: s ** o)

    def __rpow__(self, other):
        return _StructBase.__ope_lr(self, other, lambda s, o: o ** s)

    def __ipow__(self, other):
        return _StructBase.__ope_i(self, other, lambda s, o: s ** o)

    def __lshift__(self, other):
        return _StructBase.__ope_lr(self, other, lambda s, o: s << o)

    def __rlshift__(self, other):
        return _StructBase.__ope_lr(self, other, lambda s, o: o << s)

    def __ilshift__(self, other):
        return _StructBase.__ope_i(self, other, lambda s, o: s << o)

    def __rshift__(self, other):
        return _StructBase.__ope_lr(self, other, lambda s, o: s >> o)

    def __rrshift__(self, other):
        return _StructBase.__ope_lr(self, other, lambda s, o: o >> s)

    def __irshift__(self, other):
        return _StructBase.__ope_i(self, other, lambda s, o: s >> o)

    def __and__(self, other):
        return _StructBase.__ope_lr(self, other, lambda s, o: s & o)

    def __rand__(self, other):
        return _StructBase.__ope_lr(self, other, lambda s, o: o & s)

    def __iand__(self, other):
        return _StructBase.__ope_i(self, other, lambda s, o: s & o)

    def __xor__(self, other):
        return _StructBase.__ope_lr(self, other, lambda s, o: s ^ o)

    def __rxor__(self, other):
        return _StructBase.__ope_lr(self, other, lambda s, o: o ^ s)

    def __ixor__(self, other):
        return _StructBase.__ope_i(self, other, lambda s, o: s ^ o)

    def __or__(self, other):
        return _StructBase.__ope_lr(self, other, lambda s, o: s | o)

    def __ror__(self, other):
        return _StructBase.__ope_lr(self, other, lambda s, o: o | s)

    def __ior__(self, other):
        return _StructBase.__ope_i(self, other, lambda s, o: s | o)

    def __pos__(self):
        return self + 0

    def __neg__(self):
        return self * -1

    def __eq__(self, other):
        if not type(self) is type(other):
            return False
        # アドレスをチェック。これはctypes構造体の元から存在する__eq__と挙動を矛盾させないために必要。
        if self.adrs.value == other.adrs.value:
            return True
        # フィールドをチェック
        for field_name in [field["field_name"] for field in self._wrap_fields_.values()]:
            self_field = getattr(self, field_name)
            other_field = getattr(other, field_name)
            if self_field != other_field:
                return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)


class _UnionBase(_cty.Union, _SUBase, _Referable, _Arrayble):

    @staticmethod
    def _create_cls(union_name, pack_size, wrap_fields_list):
        return _SUBase._create_cls(union_name, _UnionBase, pack_size, wrap_fields_list)

    def __repr__(self, indent=0):
        repr_str = self.__class__.__name__ + " :\n"
        return repr_str + self._fields_repr(indent + 3)

    def __init__(self, *args, **kwargs):
        adjust_args, adjust_kwargs = self._adjust_fields(args, kwargs)
        super().__init__(*adjust_args, **adjust_kwargs)
        self._init_fields_resource_repos(adjust_args, adjust_kwargs)


# int だが表示する際 値に対応するラベルを表示するというだけのもの.
class _EnumRepr(int):
    enum_items = {}

    def __new__(cls, v=0):
        if isinstance(v, _cty._SimpleCData):
            v = v.value

        return super().__new__(cls, v)

    @classmethod
    def set_enum_item(cls, name, val):
        cls.enum_items[val] = name
        setattr(cls, name, val)

    @classmethod
    def get_enum_items(cls):
        return cls.enum_items

    def __repr__(self):
        return self.__class__.enum_items.get(self, "unknown")

    def __str__(self): return self.__repr__()

    @staticmethod
    def create_cls(cls_name):
        enum_cls = type(cls_name, (_EnumRepr,), {})
        enum_cls.enum_items = {}
        return enum_cls
