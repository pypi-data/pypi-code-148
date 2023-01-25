import numpy
import cupy

from numbers import Number
from typing import Optional, Tuple, Union, Iterable, Sequence
from ..device import Device, cpu
from ..array import ArrayType, register_array_type, get_array_module

__all__ = ['CrossPyArray', 'BasicIndexType', 'IndexType']

import logging
logger = logging.getLogger(__name__)

BasicIndexType = Union[int, slice, Iterable[int]]  # non-recursive
IndexType = Union[BasicIndexType, Tuple[BasicIndexType, ...]]  # recursive
ShapeType=Union[Tuple[()], Tuple[int, ...]]

def dim_to_concat(shapes, expected) -> Optional[int]:
    # a boolean list of size #dimensions, true for dimension of same size
    mask = [len(set(d)) == 1 for d in zip(*shapes)]
    if len(mask) == 0:  # all scalars
        return None
    if all(mask):  # can be concat by any dim
        if expected is None:
            logger.info("Concat dim not specified; use 0 by default")
            return 0
        return expected
    elif sum(mask) == len(mask) - 1:
        _dim = mask.index(False)
        if expected is not None and expected != _dim:
            raise ValueError(
                "Cannot concat on dim %s, but %s is feasible" %
                (expected, _dim)
            )
        return _dim
    raise ValueError(
        "Incompatible shapes with %s different dims" % (len(mask) - sum(mask))
    )


HANDLED_FUNCTIONS = {}


def implements(np_function):
    "Register an __array_function__ implementation."
    def decorator(func):
        HANDLED_FUNCTIONS[np_function] = func
        return func

    return decorator


class CrossPyArray(numpy.lib.mixins.NDArrayOperatorsMixin):
    """
    Heterougeneous N-dimensional array compatible with the numpy API with custom implementations of numpy functionality.

    https://numpy.org/doc/stable/user/basics.dispatch.html#basics-dispatch
    """
    def __init__(self, dim: int, shape, array_map) -> None:
        # super().__init__()
        self._distr_dims = [dim]
        self._shape = shape
        self._array_map = array_map

    @classmethod
    def from_array_list(cls, array_list: list, dim=None, unwrapper=lambda x: x) -> 'CrossPyArray':
        if len(array_list) == 0:
            raise NotImplementedError("array with no values not supported")

        try:
            shapes: tuple[ShapeType, ...] = tuple(a.shape for a in array_list)
        except AttributeError:
            raise AttributeError("Arrays are required to have 'shape'")
            # TODO: __len__?
        
        return cls(*CrossPyArray.from_shapes_builder(shapes, lambda i: array_list[i], dim=dim))

    @classmethod
    def from_shapes(cls, shapes: Sequence[ShapeType], block_gen, dim=None) -> 'CrossPyArray':
        """
        :param block_gen: i -> array
        """
        return CrossPyArray(*CrossPyArray.from_shapes_builder(shapes, block_gen, dim=dim))

    @classmethod
    def from_shapes_builder(cls, shapes: Sequence[ShapeType], block_gen, dim=None):
        """
        :param shapes: 
        """
        if len(shapes) == 0:
            raise NotImplementedError("array with no values not supported")

        if len(shapes) == 1:
            final_shape: ShapeType = shapes[0]
            array = block_gen(0)  # TODO: for array in array_list; or zip
            logger.debug(type(array))
            assert array.shape == final_shape
            key = tuple([(0, s) for s in array.shape])
            return None, final_shape, {key: array}

        if not all([len(s) == len(shapes[0]) for s in shapes[1:]]):
            # TODO: optionally add 1 dimension to align
            raise ValueError("Array dimensions mismatch")
        logger.debug(shapes)

        # concat dim; TODO: support topological concat
        concat_dim = dim_to_concat(shapes, dim)
        logger.debug(concat_dim)
        if concat_dim is None:  # scalar
            final_shape: ShapeType = (len(shapes),) # TODO general dim lift
        else:
            # merge shapes
            shape = list(shapes[0])
            shape[concat_dim] = sum([s[concat_dim] for s in shapes])
            final_shape: ShapeType = tuple(shape)
        logger.debug(final_shape)

        array_map = {}
        offsets = [
            0 for _ in range(len(final_shape))
        ]  # TODO topological concat
        # TODO flatten crosspy array
        for ai in range(len(shapes)):
            array = block_gen(ai)  # TODO: for array in array_list; or zip
            logger.debug(type(array))
            key = list(array.shape)  # list[int]
            if len(offsets) > 0 and len(key) == 0:
                key = [1,] # TODO general dim lift
            for i in range(len(offsets)):
                key[i] = (
                    offsets[i], offsets[i] + key[i]
                )  # gradually to list[tuple[int, int]]
                if i == concat_dim:
                    offsets[i] = key[i][1]
            key = tuple(key)  # tuple[tuple[int, int]]
            array_map[key] = array

        return concat_dim, final_shape, array_map

    @property
    def distributed_dims(self) -> list[int]:
        return self._distr_dims

    @property
    def nparts(self) -> int:
        return len(self._array_map)

    @property
    def shape(self) -> tuple[int, ...]:
        return tuple(self._shape)

    @property
    def devices(self):
        return {
            k: getattr(v, 'device', 'cpu')
            for k, v in self._array_map.items()
        }
    
    @property
    def device(self):
        detected = None
        for k, v in self._array_map.items():
            this_device = getattr(v, 'device', cpu(0))
            detected = detected or this_device
            if detected != this_device:
                raise Exception("Multiple devices detected. Use 'devices' attribute.")
        return detected

    @property
    def types(self):
        return {k: type(v) for k, v in self._array_map.items()}

    def to_dict(self):
        return self._array_map

    def values(self):
        return list(self._array_map.values())

    def keys(self):
        return list(self._array_map.keys())

    def item(self):
        if self._shape != ():
            raise IndexError("cannot get item from non-scalars")
        return self._array_map.get(())

    def __len__(self) -> int:
        return self.shape[0]

    def __repr__(self) -> str:
        return str("array %s" % self._array_map)

    def _index_intersection(
        self, part_range: tuple[int, int], target: BasicIndexType
    ) -> Union[BasicIndexType, None]:
        '''On one dimension, given the source range and target index, return

        TODO move to utils
        '''
        l, r = part_range
        if isinstance(
            target, int
        ) and l <= target < r:  # TODO negative indexing
            return (target - l)  # global to local
        elif isinstance(target, Iterable):
            in_range = [
                (i - l) for i in target if l <= i < r
            ]  # TODO negative indexing
            return in_range if len(in_range) else None
        elif isinstance(target, slice):
            # trivial case: target == part_range
            if target.start in (None, l) and target.stop in (None, r) and target.step in (None, 1):
                return slice(0, r-l)
            # trivial case: target and part_range are not overlapped
            if target.start and r <= target.start or target.stop and target.stop <= l:
                return None
            # long path
            new_start = None
            new_stop = None
            for i in range(
                target.start or 0, target.stop or r, target.step or 1
            ):
                if new_start is None and l <= i:
                    new_start = i
                if i < r:
                    new_stop = i + 1
            return slice(
                new_start - l, new_stop -
                l if new_stop is not None else None, target.step
            ) if new_start is not None else None
        elif isinstance(target, self.__class__):
            return target.to_dict()[((l, r),)] # TODO handle general bool mask
        return None

    def __getitem__(self, index: IndexType):  # -> Union[Array, List[Array]]
        """
        Note: CuPy handles out-of-bounds indices differently from NumPy. 
        NumPy handles them by raising an error, but CuPy wraps around them.
        """
        if self._shape == ():
            raise IndexError("scalar is not subscriptable")

        # unify the form to list of slices
        if not isinstance(index, tuple):
            index = (index, )

        # allow optional ellipsis [d0, d1, ...]
        if len(index) - len(self.shape) == 1 and index[-1] is Ellipsis:
            index = index[:-1]

        # def _parse_bool_mask(mask):
        #     # assume mask is 1-D
        #     assert len(mask.shape) == 1
        #     return [i for i in range(mask.shape[0]) if mask[i].item()]
        # index = [(_parse_bool_mask(i) if isinstance(i, self.__class__) else i) for i in index]

        ret = []
        for k, v in self._array_map.items():
            local_indices = []
            for d, i in enumerate(index):
                local_i = self._index_intersection(
                    k[d], i if i is not Ellipsis else slice(None)
                )
                local_indices.append(local_i)
            if all([i is not None for i in local_indices]):
                try:
                    with v.device:
                        ret.append(v[tuple(local_indices)])
                except:
                    ret.append(v[tuple(local_indices)])
        # TODO check out of range in advance
        if len(ret) == 0:
            raise IndexError("Index out of range")
        # FIXME: shape may change!!!
        return CrossPyArray.from_array_list(ret)

    def _check_index(self, index: Tuple[BasicIndexType]):
        def _meta_check(target, max):
            if isinstance(target,
                          int) and (0 <= target < max or 0 > target >= -max):
                return True
            elif isinstance(target, Iterable):
                return all([(0 <= i < max or 0 > i >= -max) for i in target])
            elif isinstance(target, slice):
                return all(
                    [
                        i < max for i in range(
                            target.start or 0, target.stop or max,
                            target.step or 1
                        )
                    ]
                )
            raise TypeError("index out of range", target, "vs", max)

        if not all(
            [_meta_check(i, self._shape[d]) for d, i in enumerate(index)]
        ):
            raise TypeError("index out of range")

    def __setitem__(self, index: IndexType, value):
        """
        Assign :param:`value` to a partition which may not on the current device.

        :param index: index of the target partition(s)

        .. todo:
            Assignment of different values to multiple partitions (ndarrays) are currently NOT supported. The :param:`value` is assigned as a whole to each of the target partition(s).
        """
        # TODO set is much slower than get

        # unify the form to list of slices
        if not isinstance(index, tuple):
            index = (index, )

        # TODO this is actually quite necessary for oor; optimize it!
        # self._check_index(index)

        def _local_assignment(target, local_indices, source, source_indices: Optional[tuple]=None):
            if source_indices is None:
                src = source
            else:
                src = source[tuple(source_indices)
                                ] if len(source_indices) else source.item()
            if hasattr(target, 'device'):  # target is cupy array
                if isinstance(src, self.__class__):
                    src = src.all_to(target.device)
                with target.device:
                    target[tuple(local_indices)] = cupy.asarray(src)
            elif hasattr(source, 'device'):  # numpy <= cupy
                target[tuple(local_indices)] = cupy.asnumpy(src)
            else:  # numpy <= numpy
                target[tuple(local_indices)] = src

        if self.nparts == 1: # short path
            _local_assignment(self.values()[0], index, value)
            return

        # propagate trivial slice (:)
        if index[0] == slice(None) and isinstance(value, self.__class__) and all(
            ok == ik[:len(ok)] for ok,ik in zip(value.keys(), self.keys())
        ):
            # TODO assuming keys/values ordered
            for src,dst in zip(value.values(), self.values()):
                _local_assignment(dst, index, src)
            return

        def _target_shape(index, caps: list[int]):
            """
            :return: The shape of target region defined by index
            """
            def _per_dim_size(target: BasicIndexType, max: int):
                if isinstance(target, int):
                    return 1
                elif isinstance(target, Iterable):
                    try:
                        return len(target) # len might not be available
                    except:
                        try:
                            return target.shape[0]
                        except:
                            # TODO slow!
                            return sum(
                                [1 for _ in target]
                            )
                elif isinstance(target, slice):
                    if target.step in (None, 1):
                        return (target.stop or max) - (target.start or 0)
                    # TODO slow
                    return sum(
                        [
                            1 for _ in range(
                                target.start or 0, target.stop or max,
                                target.step or 1
                            )
                        ]
                    )
                raise TypeError("unknown index type")

            return [_per_dim_size(i, caps[d]) for d, i in enumerate(index)]

        source_shape_start = None
        for k, v in self._array_map.items():
            local_indices = [
                self._index_intersection(k[d], i) for d, i in enumerate(index)
            ]
            if all([i is not None for i in local_indices]):
                target_shape = _target_shape(local_indices, [r[1] for r in k])
                for i in range(len(target_shape), len(k)):
                    target_shape.append(k[i][1] - k[i][0]) # fill up remaining dims
                target_shape = [x for x in target_shape if x > 1] # squeeze
                assert len(target_shape) == len(value.shape)
                if source_shape_start is None:
                    source_shape_start = [0 for _ in range(len(value.shape))]
                source_shape_end = [
                    a + b for a, b in
                    zip(source_shape_start, target_shape)
                ]
                source_indices = [
                    slice(start, stop) for start, stop in
                    zip(source_shape_start, source_shape_end)
                ]
                source_shape_start = source_shape_end
                _local_assignment(v, local_indices, value, source_indices)

    # TODO unify attr
    def sum(self, axis=None, *args, **kwargs):
        # TODO: assuming 1-D
        new_map = {}
        v0 = None
        vv = None
        reduce = axis in self.distributed_dims or axis is None
        # TODO axis=None
        for k,v in self._array_map.items():
            try:
                with v.device:
                    if reduce and vv is not None:
                        v0 = get_array_module(vv).asarray(vv)
                    vv = get_array_module(v).sum(v, axis=axis)
                    if reduce and v0 is not None:
                        vv += v0
            except:
                if reduce and vv is not None:
                    v0 = get_array_module(vv).asarray(vv)
                vv = get_array_module(v).sum(v, axis=axis)
                if reduce and v0 is not None:
                    vv += v0
            new_map[k] = vv
        return CrossPyArray.from_array_list([vv] if reduce else list(new_map.values()))

    # TODO unify attr
    def argmin(self, axis=None, *args, **kwargs):
        new_map = {}
        for k,v in self._array_map.items():
            try:
                with v.device:
                    vv = get_array_module(v).argmin(v, axis=axis)
            except:
                vv = get_array_module(v).argmin(v, axis=axis)
            new_map[k] = vv
        return CrossPyArray.from_array_list(list(new_map.values()))

    def to(self, placement):
        if isinstance(placement, Iterable):
            return self._to_multidevice(placement)
        else:
            return self.all_to(placement)

    def _to_multidevice(self, placement):
        from ..ldevice import LDeviceSequenceBlocked
        Partitioner = LDeviceSequenceBlocked
        mapper = Partitioner(len(placement), placement=placement)
        arr_p = mapper.partition_tensor(self)
        return CrossPyArray.from_array_list(arr_p)

    def all_to(self, device):
        def _aggregate(concat, pull_op):
            output = None
            for k, v in sorted(self._array_map.items()):
                pulled = pull_op(v)
                if output is None:
                    output = pulled
                else:
                    diff_dim = -1
                    shape = [(0, s) for s in output.shape]
                    assert len(shape) == len(k)
                    for i, (range1, range2) in enumerate(zip(shape, k)):
                        if range1 != range2:
                            diff_dim = i
                            break
                    output = concat((output, pulled), axis=diff_dim)
            return output

        if (
            isinstance(device, Device) and
            device.__class__.__name__ == "_CPUDevice"
        ) or (isinstance(device, int) and device < 0):
            return _aggregate(numpy.concatenate, cupy.asnumpy)

        try:
            device = getattr(device, "cupy_device")
        except AttributeError:
            device = cupy.cuda.Device(device)
        with device:
            return _aggregate(cupy.concatenate, cupy.asarray)

    def __array__(self, dtype=None):
        """
        `numpy.array` or `numpy.asarray` that converts this array to a numpy array
        will call this __array__ method to obtain a standard numpy.ndarray.
        """
        logger.debug("ALL TO CPU!")
        return self.all_to(-1)

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        """
        :param ufunc:   A function like numpy.multiply
        :param method:  A string, differentiating between numpy.multiply(...) and
                        variants like numpy.multiply.outer, numpy.multiply.accumulate,
                        and so on. For the common case, numpy.multiply(...), method == '__call__'.
        :param inputs:  A mixture of different types
        :param kwargs:  Keyword arguments passed to the function
        """
        # One might also consider adding the built-in list type to this
        # list, to support operations like np.add(array_like, list)
        _HANDLED_TYPES = (numpy.ndarray, Number, cupy._core.core.ndarray)
        out = kwargs.get('out', ())
        for x in inputs + out:
            # Only support operations with instances of _HANDLED_TYPES.
            # Use ArrayLike instead of type(self) for isinstance to
            # allow subclasses that don't override __array_ufunc__ to
            # handle ArrayLike objects.
            if not isinstance(x, _HANDLED_TYPES + (CrossPyArray, )):
                logger.debug("not handling", type(x))
                return NotImplemented

        # Defer to the implementation of the ufunc on unwrapped values.
        # inputs = tuple(x.values() if isinstance(x, CrossPyArray) else x
        #                for x in inputs)
        if out:
            kwargs['out'] = tuple(
                x.values() if isinstance(x, CrossPyArray) else x for x in out
            )

        if method == '__call__':
            unwrapped_inputs = []
            last_mapping = None
            for input in inputs:
                if isinstance(input, Number):
                    unwrapped_inputs.append([input])
                elif isinstance(input, self.__class__):
                    try:
                        unwrapped_inputs.append(input.values())
                    except:
                        unwrapped_inputs.append(numpy.asarray(input))
                    this_mapping = input.keys()
                    if last_mapping is None or last_mapping == [()]:
                        last_mapping = this_mapping
                    if this_mapping != [()] and not (
                        this_mapping == last_mapping or all(r in n for m in this_mapping for r in m for n in last_mapping)):
                        raise TypeError("inconsistent mappings not supported")
                else:
                    return NotImplemented
            # broadcast inputs
            if last_mapping is not None:
                for input in unwrapped_inputs:
                    while len(input) < len(last_mapping):
                        input.append(input[0]) # often just 2 inputs
                assert all(len(unwrapped_inputs[0]) == len(i) for i in unwrapped_inputs[1:])
            # result = getattr(ufunc, method)(*inputs, **kwargs)
            result = []
            for fine_inputs in zip(*unwrapped_inputs):
                has_device = [hasattr(i, 'device') for i in fine_inputs]
                if any(has_device):
                    with fine_inputs[has_device.index(True)].device: # on lhs device by default
                        fine_inputs = [cupy.asarray(i) for i in fine_inputs]
                        fine_result = getattr(ufunc,
                        method)(*fine_inputs, **kwargs)
                else:
                    fine_result = getattr(ufunc,
                        method)(*fine_inputs, **kwargs)
                result.append(fine_result)

            if type(result) is tuple:
                # multiple return values
                return tuple(type(self).from_array_list(x) for x in result)
            elif method == 'at':
                # no return value
                return None
            else:
                # one return value
                return type(self).from_array_list(result)  # self.__class__(result)
        else:
            raise NotImplementedError(method)
        return NotImplemented

    def __array_function__(self, func, types, args, kwargs):
        if func not in HANDLED_FUNCTIONS:
            return NotImplemented
        # Note: this allows subclasses that don't override
        # __array_function__ to handle DiagonalArray objects.
        if not all(issubclass(t, self.__class__) for t in types):
            return NotImplemented
        return HANDLED_FUNCTIONS[func](*args, **kwargs)

    @property
    def blockview(self):
        return CrossPyArray.BlockView(self)

    class BlockView:
        def __init__(self, xpa: 'CrossPyArray'):
            self.array = xpa

        def __getitem__(self, index):
            assert index >= 0, "Negative index not supported"
            # very ad hoc; assuming ordered keys
            dview = self.array.to_dict()
            for k in dview:
                if index == 0:
                    return dview[k]
                index -= 1
            raise Exception("Oops, it's so fragile right now...")

@implements(numpy.sum)
def _sum(a, axis=None):
    "Implementation of np.sum for CrossPyArray objects"
    return a.sum(axis)


class _CrossPyArrayType(ArrayType):
    def can_assign_from(self, a, b):
        # TODO: We should be able to do direct copies from numpy to cupy arrays, but it doesn't seem to be working.
        # return isinstance(b, (cupy.ndarray, numpy.ndarray))
        raise NotImplementedError
        return isinstance(b, _Array)

    def get_memory(self, a):
        raise NotImplementedError
        return gpu(a.device.id).memory()

    def get_array_module(self, a):
        import sys
        return sys.modules[__name__]


register_array_type(CrossPyArray)(_CrossPyArrayType())
