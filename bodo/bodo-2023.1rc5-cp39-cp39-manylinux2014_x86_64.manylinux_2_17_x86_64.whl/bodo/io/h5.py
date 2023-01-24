"""
Analysis and transformation for HDF5 support.
"""
import types as pytypes
import numba
from numba.core import ir, types
from numba.core.ir_utils import compile_to_numba_ir, find_callname, find_const, get_definition, guard, replace_arg_nodes, require
import bodo
import bodo.io
from bodo.utils.transform import get_const_value_inner


class H5_IO:

    def __init__(self, func_ir, _locals, flags, arg_types):
        self.func_ir = func_ir
        self.locals = _locals
        self.flags = flags
        self.arg_types = arg_types

    def handle_possible_h5_read(self, assign, lhs, rhs):
        ordiv__uxwx = self._get_h5_type(lhs, rhs)
        if ordiv__uxwx is not None:
            iaddm__jrm = str(ordiv__uxwx.dtype)
            akow__xuxej = 'def _h5_read_impl(dset, index):\n'
            akow__xuxej += (
                "  arr = bodo.io.h5_api.h5_read_dummy(dset, {}, '{}', index)\n"
                .format(ordiv__uxwx.ndim, iaddm__jrm))
            ehtah__xpvkl = {}
            exec(akow__xuxej, {}, ehtah__xpvkl)
            fmm__vvmk = ehtah__xpvkl['_h5_read_impl']
            uldm__qkctt = compile_to_numba_ir(fmm__vvmk, {'bodo': bodo}
                ).blocks.popitem()[1]
            rnthz__ftu = rhs.index if rhs.op == 'getitem' else rhs.index_var
            replace_arg_nodes(uldm__qkctt, [rhs.value, rnthz__ftu])
            edi__babn = uldm__qkctt.body[:-3]
            edi__babn[-1].target = assign.target
            return edi__babn
        return None

    def _get_h5_type(self, lhs, rhs):
        ordiv__uxwx = self._get_h5_type_locals(lhs)
        if ordiv__uxwx is not None:
            return ordiv__uxwx
        return guard(self._infer_h5_typ, rhs)

    def _infer_h5_typ(self, rhs):
        require(rhs.op in ('getitem', 'static_getitem'))
        rnthz__ftu = rhs.index if rhs.op == 'getitem' else rhs.index_var
        jrjvs__nqkuw = guard(find_const, self.func_ir, rnthz__ftu)
        require(not isinstance(jrjvs__nqkuw, str))
        val_def = rhs
        obj_name_list = []
        while True:
            val_def = get_definition(self.func_ir, val_def.value)
            require(isinstance(val_def, ir.Expr))
            if val_def.op == 'call':
                return self._get_h5_type_file(val_def, obj_name_list)
            require(val_def.op in ('getitem', 'static_getitem'))
            qlz__vouwq = (val_def.index if val_def.op == 'getitem' else
                val_def.index_var)
            hpdco__lkclg = get_const_value_inner(self.func_ir, qlz__vouwq,
                arg_types=self.arg_types)
            obj_name_list.append(hpdco__lkclg)

    def _get_h5_type_file(self, val_def, obj_name_list):
        require(len(obj_name_list) > 0)
        require(find_callname(self.func_ir, val_def) == ('File', 'h5py'))
        require(len(val_def.args) > 0)
        sajfy__wjt = get_const_value_inner(self.func_ir, val_def.args[0],
            arg_types=self.arg_types)
        obj_name_list.reverse()
        import h5py
        bxnad__ulmgj = h5py.File(sajfy__wjt, 'r')
        san__onfs = bxnad__ulmgj
        for hpdco__lkclg in obj_name_list:
            san__onfs = san__onfs[hpdco__lkclg]
        require(isinstance(san__onfs, h5py.Dataset))
        ztbnj__wnzn = len(san__onfs.shape)
        omfx__eibpf = numba.np.numpy_support.from_dtype(san__onfs.dtype)
        bxnad__ulmgj.close()
        return types.Array(omfx__eibpf, ztbnj__wnzn, 'C')

    def _get_h5_type_locals(self, varname):
        ctdz__wjhp = self.locals.pop(varname, None)
        if ctdz__wjhp is None and varname is not None:
            ctdz__wjhp = self.flags.h5_types.get(varname, None)
        return ctdz__wjhp
