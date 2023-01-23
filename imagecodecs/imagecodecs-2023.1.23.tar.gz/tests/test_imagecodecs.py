# test_imagecodecs.py

# Copyright (c) 2018-2022, Christoph Gohlke
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
# * Neither the name of the copyright holders nor the names of any
#   contributors may be used to endorse or promote products derived
#   from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""Unittests for the imagecodecs package.

:Version: 2023.1.23

"""

import glob
import importlib
import io
import mmap
import os
import os.path as osp
import pathlib
import platform
import re
import sys
import tempfile

import numpy
import pytest
from numpy.testing import assert_allclose, assert_array_equal

try:
    import imagecodecs
    from imagecodecs import _imagecodecs
    from imagecodecs._imagecodecs import (
        bitshuffle,
        blosc,
        blosc2,
        brotli,
        bz2,
        czifile,
        lz4,
        lzf,
        lzfse,
        lzma,
        snappy,
        tifffile,
        zlib,
        zopfli,
        zstd,
    )
    from imagecodecs.imagecodecs import _add_codec, _extensions
except ImportError as exc:
    pytest.exit(str(exc))


try:
    import zarr
    from imagecodecs import numcodecs
except ImportError:
    SKIP_NUMCODECS = True
else:
    SKIP_NUMCODECS = False

    numcodecs.register_codecs()


TEST_DIR = osp.dirname(__file__)
IS_32BIT = sys.maxsize < 2**32
IS_WIN = sys.platform == 'win32'
IS_MAC = sys.platform == 'darwin'
IS_AARCH64 = platform.machine() == 'aarch64'
IS_ARM64 = platform.machine() == 'ARM64'
IS_PYPY = 'PyPy' in sys.version
# running on Windows development computer?
IS_CG = os.environ.get('COMPUTERNAME', '').startswith('CG-')
# running in cibuildwheel environment?
IS_CIBW = os.environ.get('IMAGECODECS_CIBW', False)

numpy.set_printoptions(suppress=True, precision=5)


###############################################################################


def test_version():
    """Assert imagecodecs versions match docstrings."""
    ver = ':Version: ' + imagecodecs.__version__
    assert ver in __doc__
    assert ver in imagecodecs.__doc__


@pytest.mark.parametrize('name', _extensions())
def test_module_exist(name):
    """Assert extension modules are present."""
    try:
        exists = bool(importlib.import_module('._' + name, 'imagecodecs'))
    except ImportError:
        exists = False
    if exists:
        return
    if IS_CG:
        if IS_32BIT and name in ('heif', 'jetraw'):
            pytest.xfail(f'imagecodecs._{name} may be missing')
        elif IS_ARM64 and name == 'jetraw':
            pytest.xfail(f'imagecodecs._{name} may be missing')
    elif IS_CIBW:
        if (
            (name == 'jpeg12' and os.environ.get('IMCD_SKIP_JPEG12', 0))
            or (name == 'jpegxl' and (IS_MAC or IS_32BIT or IS_AARCH64))
            or (name == 'lzham' and IS_MAC)
            or name == 'mozjpeg'
            or name == 'heif'
            or name == 'jetraw'
            # or name == 'nvjpeg'
            # or name == 'nvjpeg2k'
        ):
            pytest.xfail(f'imagecodecs._{name} may be missing')
    else:
        pytest.xfail(f'imagecodecs._{name} may be missing')
    assert exists, f'no module named imagecodecs._{name}'


@pytest.mark.parametrize(
    'name',
    [
        'bitshuffle',
        'blosc',
        'blosc2',
        'brotli',
        'czifile',
        'lz4',
        'lzf',
        'liblzfse',
        # 'lzham',
        'lzma',
        'numcodecs',
        'snappy',
        'tifffile',
        'zopfli',
        'zstd',
        'zarr',
    ],
)
def test_dependency_exist(name):
    """Assert third-party Python packages are present."""
    mayfail = not IS_CG and not IS_CIBW
    if SKIP_NUMCODECS and IS_PYPY:
        mayfail = True
    elif name in ('blosc', 'blosc2', 'snappy'):
        if IS_PYPY or sys.version_info[1] >= 10:
            mayfail = True
    try:
        importlib.import_module(name)
    except ImportError:
        if mayfail:
            pytest.skip(f'{name} may be missing')
        raise


def test_version_functions():
    """Test imagecodecs version functions."""
    assert imagecodecs.version().startswith('imagecodecs')
    assert 'imagecodecs' in imagecodecs.version(dict)
    assert imagecodecs.version(tuple)[1].startswith('cython')
    assert _imagecodecs.version().startswith('imagecodecs.py')
    assert 'imagecodecs.py' in _imagecodecs.version(dict)


def test_stubs():
    """Test stub attributes for non-existing extension."""
    with pytest.raises(AttributeError):
        imagecodecs._STUB
    _add_codec('_stub')
    assert not imagecodecs._STUB
    assert not imagecodecs._stub_check(b'')
    assert imagecodecs._stub_version() == '_stub n/a'
    with pytest.raises(imagecodecs.DelayedImportError):
        imagecodecs._STUB.attr
    with pytest.raises(imagecodecs.DelayedImportError):
        imagecodecs._stub_encode(b'')
    with pytest.raises(imagecodecs.DelayedImportError):
        imagecodecs._stub_decode(b'')
    with pytest.raises(imagecodecs.DelayedImportError):
        raise imagecodecs._stubError()


def test_dir():
    """Assert __dir__ contains delay-loaded attributes."""
    d = dir(imagecodecs)
    assert 'NONE' in d
    assert 'LZW' in d
    assert 'jxr_decode' in d


@pytest.mark.skipif(not imagecodecs.NUMPY, reason='Numpy codec missing')
@pytest.mark.parametrize(
    'codec', ['none', 'str', 'ext', 'codec', 'list', 'fail']
)
@pytest.mark.parametrize('filearg', ['str', 'pathlib', 'bytesio', 'bytes'])
def test_imread_imwrite(filearg, codec):
    """Test imread and imwrite functions."""
    imread = imagecodecs.imread
    imwrite = imagecodecs.imwrite
    data = image_data('rgba', 'uint8')

    if codec == 'ext':
        # auto detect codec from file extension or trial&error
        with TempFileName(suffix='.npy') as fileobj:
            if filearg == 'pathlib':
                fileobj = pathlib.Path(fileobj)
            if filearg == 'bytes':
                fileobj = imagecodecs.numpy_encode(data)
            elif filearg == 'bytesio':
                # must specify codec
                fileobj = io.BytesIO()
                imwrite(fileobj, data, codec=imagecodecs.numpy_encode)
            else:
                imwrite(fileobj, data, level=99)
            if filearg == 'bytesio':
                fileobj.seek(0)
            im, codec = imread(fileobj, return_codec=True)
            assert codec == imagecodecs.numpy_decode
            assert_array_equal(data, im)
        return

    if codec == 'none':
        encode = None
        decode = None
    elif codec == 'str':
        encode = 'numpy'
        decode = 'numpy'
    elif codec == 'list':
        encode = 'npz'
        decode = ['npz']
    elif codec == 'fail':
        encode = 'fail'
        decode = 'fail'
    elif codec == 'codec':
        encode = imagecodecs.numpy_encode
        decode = imagecodecs.numpy_decode

    with TempFileName() as fileobj:
        if filearg == 'pathlib':
            fileobj = pathlib.Path(fileobj)
        elif filearg == 'bytesio':
            fileobj = io.BytesIO()

        if filearg == 'bytes':
            fileobj = imagecodecs.numpy_encode(data)
        elif encode in (None, 'fail'):
            with pytest.raises(ValueError):
                imwrite(fileobj, data, codec=encode)
            imwrite(fileobj, data, codec=imagecodecs.numpy_encode)
        else:
            imwrite(fileobj, data, codec=encode)

        if filearg == 'bytesio':
            fileobj.seek(0)

        if codec == 'fail':
            with pytest.raises(ValueError):
                im = imread(fileobj, codec=decode)
            return

        im, ret = imread(fileobj, codec=decode, return_codec=True)
        assert ret == imagecodecs.numpy_decode
        assert_array_equal(data, im)


def test_none():
    """Test NOP codec."""
    data = b'None'
    assert imagecodecs.none_encode(data) is data
    assert imagecodecs.none_decode(data) is data


@pytest.mark.skipif(not imagecodecs.BITORDER, reason='Bitorder missing')
def test_bitorder():
    """Test BitOrder codec with bytes."""
    decode = imagecodecs.bitorder_decode
    data = b'\x01\x00\x9a\x02'
    reverse = b'\x80\x00Y@'
    # return new string
    assert decode(data) == reverse
    assert data == b'\x01\x00\x9a\x02'
    # provide output
    out = bytearray(len(data))
    decode(data, out=out)
    assert out == reverse
    assert data == b'\x01\x00\x9a\x02'
    # inplace
    with pytest.raises(TypeError):
        decode(data, out=data)
    data = bytearray(data)
    decode(data, out=data)
    assert data == reverse
    # bytes range
    assert BYTES == decode(readfile('bytes.bitorder.bin'))


@pytest.mark.skipif(not imagecodecs.BITORDER, reason='Bitorder missing')
def test_bitorder_ndarray():
    """Test BitOrder codec with ndarray."""
    decode = imagecodecs.bitorder_decode
    data = numpy.array([1, 666], dtype='uint16')
    reverse = numpy.array([128, 16473], dtype='uint16')
    # return new array
    assert_array_equal(decode(data), reverse)
    # inplace
    decode(data, out=data)
    assert_array_equal(data, numpy.array([128, 16473], dtype='uint16'))
    # array view
    data = numpy.array(
        [
            [1, 666, 1431655765, 62],
            [2, 667, 2863311530, 32],
            [3, 668, 1431655765, 30],
        ],
        dtype='uint32',
    )
    reverse = numpy.array(
        [
            [1, 666, 1431655765, 62],
            [2, 16601, 1431655765, 32],
            [3, 16441, 2863311530, 30],
        ],
        dtype='uint32',
    )
    assert_array_equal(decode(data[1:, 1:3]), reverse[1:, 1:3])
    # array view inplace
    decode(data[1:, 1:3], out=data[1:, 1:3])
    assert_array_equal(data, reverse)


@pytest.mark.skipif(not imagecodecs.PACKINTS, reason='Packints missing')
def test_packints_decode():
    """Test PackInts decoder."""
    decode = imagecodecs.packints_decode

    decoded = decode(b'', 'B', 1)
    assert len(decoded) == 0

    decoded = decode(b'a', 'B', 1)
    assert tuple(decoded) == (0, 1, 1, 0, 0, 0, 0, 1)

    decoded = decode(b'ab', 'B', 2)
    assert tuple(decoded) == (1, 2, 0, 1, 1, 2, 0, 2)

    decoded = decode(b'abcd', 'B', 3)
    assert tuple(decoded) == (3, 0, 2, 6, 1, 1, 4, 3, 3, 1)

    decoded = decode(numpy.frombuffer(b'abcd', dtype='uint8'), 'B', 3)
    assert tuple(decoded) == (3, 0, 2, 6, 1, 1, 4, 3, 3, 1)


PACKBITS_DATA = [
    ([], b''),
    ([0] * 1, b'\x00\x00'),  # literal
    ([0] * 2, b'\xff\x00'),  # replicate
    ([0] * 3, b'\xfe\x00'),
    ([0] * 64, b'\xc1\x00'),
    ([0] * 127, b'\x82\x00'),
    ([0] * 128, b'\x81\x00'),  # max replicate
    ([0] * 129, b'\x81\x00\x00\x00'),
    ([0] * 130, b'\x81\x00\xff\x00'),
    ([0] * 128 * 3, b'\x81\x00' * 3),
    ([255] * 1, b'\x00\xff'),  # literal
    ([255] * 2, b'\xff\xff'),  # replicate
    ([0, 1], b'\x01\x00\x01'),
    ([0, 1, 2], b'\x02\x00\x01\x02'),
    ([0, 1] * 32, b'\x3f' + b'\x00\x01' * 32),
    ([0, 1] * 63 + [2], b'\x7e' + b'\x00\x01' * 63 + b'\x02'),
    ([0, 1] * 64, b'\x7f' + b'\x00\x01' * 64),  # max literal
    ([0, 1] * 64 + [2], b'\x7f' + b'\x00\x01' * 64 + b'\x00\x02'),
    ([0, 1] * 64 * 5, (b'\x7f' + b'\x00\x01' * 64) * 5),
    ([0, 1, 1], b'\x00\x00\xff\x01'),  # or b'\x02\x00\x01\x01'
    ([0] + [1] * 128, b'\x00\x00\x81\x01'),  # or b'\x01\x00\x01\x82\x01'
    ([0] + [1] * 129, b'\x00\x00\x81\x01\x00\x01'),  # b'\x01\x00\x01\x81\x01'
    ([0, 1] * 64 + [2] * 2, b'\x7f' + b'\x00\x01' * 64 + b'\xff\x02'),
    ([0, 1] * 64 + [2] * 128, b'\x7f' + b'\x00\x01' * 64 + b'\x81\x02'),
    ([0, 0, 1], b'\x02\x00\x00\x01'),  # or b'\xff\x00\x00\x01'
    ([0, 0] + [1, 2] * 64, b'\xff\x00\x7f' + b'\x01\x02' * 64),
    ([0] * 128 + [1], b'\x81\x00\x00\x01'),
    ([0] * 128 + [1, 2] * 64, b'\x81\x00\x7f' + b'\x01\x02' * 64),
    (
        b'\xaa\xaa\xaa\x80\x00\x2a\xaa\xaa\xaa\xaa\x80\x00'
        b'\x2a\x22\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa',
        b'\xfe\xaa\x02\x80\x00\x2a\xfd\xaa\x03\x80\x00\x2a\x22\xf7\xaa',
    ),
]


@pytest.mark.skipif(not imagecodecs.PACKBITS, reason='Packbits missing')
@pytest.mark.parametrize('data', range(len(PACKBITS_DATA)))
@pytest.mark.parametrize('codec', ['encode', 'decode'])
def test_packbits(codec, data):
    """Test PackBits codec."""
    encode = imagecodecs.packbits_encode
    decode = imagecodecs.packbits_decode
    uncompressed, compressed = PACKBITS_DATA[data]
    uncompressed = bytes(uncompressed)
    if codec == 'decode':
        assert decode(compressed) == uncompressed
    elif codec == 'encode':
        assert len(encode(uncompressed)) <= len(compressed)
        assert encode(uncompressed) == compressed


@pytest.mark.parametrize('data', range(len(PACKBITS_DATA)))
def test_packbits_py(data):
    """Test pure Python PackBits decoder."""
    uncompressed, compressed = PACKBITS_DATA[data]
    uncompressed = bytes(uncompressed)
    assert _imagecodecs.packbits_decode(compressed) == uncompressed


@pytest.mark.skipif(not imagecodecs.PACKBITS, reason='Packbits missing')
def test_packbits_nop():
    """Test PackBits decoding empty data."""
    decode = imagecodecs.packbits_decode
    assert decode(b'\x80') == b''
    assert decode(b'\x80\x80') == b''


@pytest.mark.skipif(not imagecodecs.PACKBITS, reason='Packbits missing')
@pytest.mark.parametrize('output', [None, 'array'])
@pytest.mark.parametrize('codec', ['encode', 'decode'])
@pytest.mark.parametrize('dtype', ['uint8', 'uint16'])
def test_packbits_array(codec, output, dtype):
    """Test PackBits codec with arrays."""
    dtype = numpy.dtype(dtype)
    encode = imagecodecs.packbits_encode
    decode = imagecodecs.packbits_decode
    uncompressed, compressed = PACKBITS_DATA[-1]
    shape = (2, 7, len(uncompressed) // dtype.itemsize)
    data = numpy.zeros(shape, dtype=dtype)
    data[..., :] = numpy.frombuffer(uncompressed, dtype=dtype)
    compressed = compressed * (shape[0] * shape[1])
    if codec == 'encode':
        if output == 'array':
            out = numpy.zeros(data.nbytes, 'uint8')
            assert_array_equal(
                encode(data, out=out),
                numpy.frombuffer(compressed, dtype=dtype).view('uint8'),
            )
        else:
            assert encode(data) == compressed
    else:
        if output == 'array':
            out = numpy.zeros(data.nbytes, 'uint8')
            assert_array_equal(
                decode(compressed, out=out), data.flatten().view('uint8')
            )
        else:
            assert decode(compressed) == data.tobytes()


@pytest.mark.skipif(not imagecodecs.PACKBITS, reason='Packbits missing')
def test_packbits_encode_axis():
    """Test PackBits encoder with samples."""
    data = numpy.zeros((97, 67, 3), dtype=numpy.int16)
    data[10:20, 11:21, 1] = -1
    encoded = imagecodecs.packbits_encode(data, axis=-1)  # very inefficient
    assert len(encoded) > 10000
    assert imagecodecs.packbits_decode(encoded) == data.tobytes()
    encoded = imagecodecs.packbits_encode(data, axis=-2)
    assert len(encoded) < 1200
    assert imagecodecs.packbits_decode(encoded) == data.tobytes()


@pytest.mark.filterwarnings('ignore:invalid value encountered')
@pytest.mark.parametrize('output', ['new', 'out', 'inplace'])
@pytest.mark.parametrize('codec', ['encode', 'decode'])
@pytest.mark.parametrize(
    'kind',
    ['u1', 'u2', 'u4', 'u8', 'i1', 'i2', 'i4', 'i8', 'f4', 'f8', 'B', 'b'],
)
@pytest.mark.parametrize('byteorder', ['>', '<'])
@pytest.mark.parametrize('func', ['delta', 'xor'])
def test_delta(output, byteorder, kind, codec, func):
    """Test Delta codec."""
    # if byteorder == '>' and numpy.dtype(kind).itemsize == 1:
    #     pytest.skip('duplicate test')

    if func == 'delta':
        if not imagecodecs.DELTA:
            pytest.skip('Delta missing')
        encode = imagecodecs.delta_encode
        decode = imagecodecs.delta_decode
        encode_py = _imagecodecs.delta_encode
        # decode_py = _imagecodecs.delta_decode
    elif func == 'xor':
        if not imagecodecs.XOR:
            pytest.skip('Xor missing')
        encode = imagecodecs.xor_encode
        decode = imagecodecs.xor_decode
        encode_py = _imagecodecs.xor_encode
        # decode_py = _imagecodecs.xor_decode

    bytetype = bytearray
    if kind == 'b':
        bytetype = bytes
        kind = 'B'

    axis = -2  # do not change
    if kind[0] in 'iuB':
        low = numpy.iinfo(kind).min
        high = numpy.iinfo(kind).max
        data = numpy.random.randint(
            low, high, size=33 * 31 * 3, dtype=kind
        ).reshape(33, 31, 3)
    else:
        # floating point
        low, high = -1e5, 1e5
        data = numpy.random.randint(
            low, high, size=33 * 31 * 3, dtype='i4'
        ).reshape(33, 31, 3)
    data = data.astype(byteorder + kind)

    data[16, 14] = [0, 0, 0]
    data[16, 15] = [low, high, low]
    data[16, 16] = [high, low, high]
    data[16, 17] = [low, high, low]
    data[16, 18] = [high, low, high]
    data[16, 19] = [0, 0, 0]

    if kind == 'B':
        # data = data.reshape(-1)
        data = data.tobytes()
        diff = encode_py(data, axis=0)
        if output == 'new':
            if codec == 'encode':
                encoded = encode(data, out=bytetype)
                assert encoded == diff
            elif codec == 'decode':
                decoded = decode(diff, out=bytetype)
                assert decoded == data
        elif output == 'out':
            if codec == 'encode':
                encoded = bytetype(len(data))
                if bytetype == bytes:
                    with pytest.raises(TypeError):
                        encode(data, out=encoded)
                else:
                    encode(data, out=encoded)
                    assert encoded == diff
            elif codec == 'decode':
                decoded = bytetype(len(data))
                if bytetype == bytes:
                    with pytest.raises(TypeError):
                        decode(diff, out=decoded)
                else:
                    decode(diff, out=decoded)
                    assert decoded == data
        elif output == 'inplace':
            if codec == 'encode':
                encoded = bytetype(data)
                if bytetype == bytes:
                    with pytest.raises(TypeError):
                        encode(encoded, out=encoded)
                else:
                    encode(encoded, out=encoded)
                    assert encoded == diff
            elif codec == 'decode':
                decoded = bytetype(diff)
                if bytetype == bytes:
                    with pytest.raises(TypeError):
                        decode(decoded, out=decoded)
                else:
                    decode(decoded, out=decoded)
                    assert decoded == data
    else:
        # if func == 'xor' and kind in ('f4', 'f8'):
        #      with pytest.raises(ValueError):
        #          encode(data, axis=axis)
        #      pytest.xfail("XOR codec not implemented for float data")
        diff = encode_py(data, axis=-2)
        if output == 'new':
            if codec == 'encode':
                encoded = encode(data, axis=axis)
                assert_array_equal(encoded, diff)
            elif codec == 'decode':
                decoded = decode(diff, axis=axis)
                assert_array_equal(decoded, data)
        elif output == 'out':
            if codec == 'encode':
                encoded = numpy.zeros_like(data)
                encode(data, axis=axis, out=encoded)
                assert_array_equal(encoded, diff)
            elif codec == 'decode':
                decoded = numpy.zeros_like(data)
                decode(diff, axis=axis, out=decoded)
                assert_array_equal(decoded, data)
        elif output == 'inplace':
            if codec == 'encode':
                encoded = data.copy()
                encode(encoded, axis=axis, out=encoded)
                assert_array_equal(encoded, diff)
            elif codec == 'decode':
                decoded = diff.copy()
                decode(decoded, axis=axis, out=decoded)
                assert_array_equal(decoded, data)


@pytest.mark.skipif(not imagecodecs.FLOATPRED, reason='FloatPred missing')
@pytest.mark.parametrize('output', ['new', 'out'])
@pytest.mark.parametrize('codec', ['encode', 'decode'])
@pytest.mark.parametrize('endian', ['le', 'be'])
@pytest.mark.parametrize('planar', [False, True])
def test_floatpred(planar, endian, output, codec):
    """Test FloatPred codec."""
    encode = imagecodecs.floatpred_encode
    decode = imagecodecs.floatpred_decode
    data = numpy.fromfile(datafiles('rgb.bin'), dtype='<f4').reshape(33, 31, 3)

    if not planar:
        axis = -2
        if endian == 'le':
            encoded = numpy.fromfile(
                datafiles('rgb.floatpred_le.bin'), dtype='<f4'
            )
            encoded = encoded.reshape(33, 31, 3)
            if output == 'new':
                if codec == 'decode':
                    assert_array_equal(decode(encoded, axis=axis), data)
                elif codec == 'encode':
                    assert_array_equal(encode(data, axis=axis), encoded)
            elif output == 'out':
                out = numpy.zeros_like(data)
                if codec == 'decode':
                    decode(encoded, axis=axis, out=out)
                    assert_array_equal(out, data)
                elif codec == 'encode':
                    out = numpy.zeros_like(data)
                    encode(data, axis=axis, out=out)
                    assert_array_equal(out, encoded)
        elif endian == 'be':
            data = data.astype('>f4')
            encoded = numpy.fromfile(
                datafiles('rgb.floatpred_be.bin'), dtype='>f4'
            )
            encoded = encoded.reshape(33, 31, 3)
            if output == 'new':
                if codec == 'decode':
                    assert_array_equal(decode(encoded, axis=axis), data)
                elif codec == 'encode':
                    assert_array_equal(encode(data, axis=axis), encoded)
            elif output == 'out':
                out = numpy.zeros_like(data)
                if codec == 'decode':
                    decode(encoded, axis=axis, out=out)
                    assert_array_equal(out, data)
                elif codec == 'encode':
                    out = numpy.zeros_like(data)
                    encode(data, axis=axis, out=out)
                    assert_array_equal(out, encoded)
    else:
        axis = -1
        data = numpy.ascontiguousarray(numpy.moveaxis(data, 2, 0))
        if endian == 'le':
            encoded = numpy.fromfile(
                datafiles('rrggbb.floatpred_le.bin'), dtype='<f4'
            )
            encoded = encoded.reshape(3, 33, 31)
            if output == 'new':
                if codec == 'decode':
                    assert_array_equal(decode(encoded, axis=axis), data)
                elif codec == 'encode':
                    assert_array_equal(encode(data, axis=axis), encoded)
            elif output == 'out':
                out = numpy.zeros_like(data)
                if codec == 'decode':
                    decode(encoded, axis=axis, out=out)
                    assert_array_equal(out, data)
                elif codec == 'encode':
                    out = numpy.zeros_like(data)
                    encode(data, axis=axis, out=out)
                    assert_array_equal(out, encoded)
        elif endian == 'be':
            data = data.astype('>f4')
            encoded = numpy.fromfile(
                datafiles('rrggbb.floatpred_be.bin'), dtype='>f4'
            )
            encoded = encoded.reshape(3, 33, 31)
            if output == 'new':
                if codec == 'decode':
                    assert_array_equal(decode(encoded, axis=axis), data)
                elif codec == 'encode':
                    assert_array_equal(encode(data, axis=axis), encoded)
            elif output == 'out':
                out = numpy.zeros_like(data)
                if codec == 'decode':
                    decode(encoded, axis=axis, out=out)
                    assert_array_equal(out, data)
                elif codec == 'encode':
                    out = numpy.zeros_like(data)
                    encode(data, axis=axis, out=out)
                    assert_array_equal(out, encoded)


@pytest.mark.skipif(not imagecodecs.FLOAT24, reason='Float24 missing')
@pytest.mark.parametrize(
    'f3, f4, f3_expected',
    [
        # +/-/signalling NaN
        ((0x7F, 0x80, 0x00), (0x7F, 0xC0, 0x00, 0x00), numpy.nan),
        ((0xFF, 0x80, 0x00), (0xFF, 0xC0, 0x00, 0x00), numpy.nan),
        ((0xFF, 0x80, 0x00), (0xFF, 0x80, 0x00, 0x01), numpy.nan),
        # +/- inf
        ((0x7F, 0x00, 0x00), (0x7F, 0x80, 0x00, 0x00), numpy.inf),
        ((0xFF, 0x00, 0x00), (0xFF, 0x80, 0x00, 0x00), -numpy.inf),
        # +/- zero
        ((0x00, 0x00, 0x00), (0x00, 0x00, 0x00, 0x00), 0.0),
        ((0x80, 0x00, 0x00), (0x80, 0x00, 0x00, 0x00), -0.0),
        # +/- one
        ((0x3F, 0x00, 0x00), (0x3F, 0x80, 0x00, 0x00), 1.0),
        ((0xBF, 0x00, 0x00), (0xBF, 0x80, 0x00, 0x00), -1.0),
        # pi
        ((0x40, 0x92, 0x20), (0x40, 0x49, 0x0F, 0xDB), 3.1416016),
        # pi, no rounding
        # ((0x40, 0x92, 0x1F), (0x40, 0x49, 0x0F, 0xDB), 3.141571),
        # pi * 10**-6
        ((0x2C, 0xA5, 0xA8), (0x36, 0x52, 0xD4, 0x27), 3.1415839e-06),
        # pi * 10**6
        ((0x2C, 0xA5, 0xA8), (0x36, 0x52, 0xD4, 0x27), 3.1415839e-06),
        # subnormal 1e-19
        ((0x00, 0x76, 0x0F), (0x1F, 0xEC, 0x1E, 0x4A), 1e-19),
        # overflow 1.85e19
        ((0x7F, 0x00, 0x00), (0x5F, 0x80, 0x5E, 0x9A), numpy.inf),
        # subnormal shift 0
        ((0x00, 0x80, 0x00), (0x20, 0x00, 0x00, 0x00), 1.0842022e-19),
        # encode normal to denormal with rounding
        ((0x00, 0x80, 0x00), (0x1F, 0xFF, 0xFF, 0xFF), 1.0842021e-19),
        # subnormal shift 1
        ((0x00, 0x40, 0x00), (0x1F, 0x80, 0x00, 0x00), 5.421011e-20),
        # minimum positive subnormal, shift 15
        ((0x00, 0x00, 0x01), (0x18, 0x80, 0x00, 0x00), 3.3087225e-24),
        # minimum positive normal
        ((0x01, 0x00, 0x00), (0x20, 0x80, 0x00, 0x00), 2.1684043e-19),
        # round minimum normal float32 to zero; 1.1754943508222875e-38
        ((0x00, 0x00, 0x00), (0x00, 0x80, 0x00, 0x00), 0.0),
        ((0x80, 0x00, 0x00), (0x80, 0x80, 0x00, 0x00), 0.0),
        # round largest denormal float32 to zero; 5.877471754111438e-39
        ((0x00, 0x00, 0x00), (0x00, 0x40, 0x00, 0x00), 0.0),
        ((0x80, 0x00, 0x00), (0x80, 0x40, 0x00, 0x00), 0.0),
    ],
)
@pytest.mark.parametrize('byteorder', ['>', '<'])
@pytest.mark.parametrize('mode', ['encode', 'decode'])
def test_float24(f3, f4, f3_expected, byteorder, mode):
    """Test float24 special numbers."""
    decode = imagecodecs.float24_decode
    encode = imagecodecs.float24_encode

    f3_bytes = bytes(f3)
    f4_bytes = bytes(f4)

    if byteorder == '<':
        f3_bytes = f3_bytes[::-1]

    if mode == 'decode':
        f3_decoded = decode(f3_bytes, byteorder=byteorder)[0]
        if f3_expected is numpy.nan:
            assert numpy.isnan([f3_decoded])[0]
        elif f3_expected in (-numpy.inf, numpy.inf):
            assert f3_decoded == f3_expected
        else:
            assert abs(f3_decoded - f3_expected) < 4e-8
    else:
        f4_array = numpy.frombuffer(f4_bytes, dtype='>f4').astype('=f4')
        f3_encoded = encode(f4_array, byteorder=byteorder)
        assert f3_encoded == f3_bytes


@pytest.mark.skipif(not imagecodecs.FLOAT24, reason='Float24 missing')
@pytest.mark.parametrize('byteorder', ['>', '<'])
def test_float24_roundtrip(byteorder):
    """Test all float24 numbers."""
    f3_bytes = numpy.arange(2**24, dtype='>u4').astype('u1').reshape((-1, 4))
    if byteorder == '>':
        f3_bytes = f3_bytes[:, :3].tobytes()
    else:
        f3_bytes = f3_bytes[:, 2::-1].tobytes()
    f3_decoded = imagecodecs.float24_decode(f3_bytes, byteorder=byteorder)
    f3_encoded = imagecodecs.float24_encode(f3_decoded, byteorder=byteorder)
    assert f3_bytes == f3_encoded


@pytest.mark.skipif(not imagecodecs.LZW, reason='LZW missing')
def test_lzw_corrupt():
    """Test LZW decoder with corrupt stream."""
    # reported by S Richter on 2020.2.17
    fname = datafiles('corrupt.lzw.bin')
    with open(fname, 'rb') as fh:
        encoded = fh.read()
    assert imagecodecs.lzw_check(encoded)
    with pytest.raises(RuntimeError):
        imagecodecs.lzw_decode(encoded, out=655360)


@pytest.mark.skipif(not imagecodecs.LZW, reason='LZW missing')
def test_lzw_msb():
    """Test LZW decoder with MSB."""
    # TODO: add test_lzw_lsb
    decode = imagecodecs.lzw_decode
    for encoded, decoded in [
        (
            b'\x80\x1c\xcc\'\x91\x01\xa0\xc2m6\x99NB\x03\xc9\xbe\x0b'
            b'\x07\x84\xc2\xcd\xa68|"\x14 3\xc3\xa0\xd1c\x94\x02\x02\x80',
            b'say hammer yo hammer mc hammer go hammer',
        ),
        (
            b'\x80\x18M\xc6A\x01\xd0\xd0e\x10\x1c\x8c\xa73\xa0\x80\xc7\x02'
            b'\x10\x19\xcd\xe2\x08\x14\x10\xe0l0\x9e`\x10\x10\x80',
            b'and the rest can go and play',
        ),
        (
            b'\x80\x18\xcc&\xe19\xd0@t7\x9dLf\x889\xa0\xd2s',
            b"can't touch this",
        ),
        (b'\x80@@', b''),
    ]:
        assert imagecodecs.lzw_check(encoded)
        assert decode(encoded) == decoded


@pytest.mark.skipif(not (imagecodecs.LZW and imagecodecs.DELTA), reason='skip')
@pytest.mark.parametrize('output', ['new', 'size', 'ndarray', 'bytearray'])
def test_lzw_decode(output):
    """Test LZW decoder of input with horizontal differencing."""
    decode = imagecodecs.lzw_decode
    delta_decode = imagecodecs.delta_decode
    encoded = readfile('bytes.lzw_horizontal.bin')
    assert imagecodecs.lzw_check(encoded)
    decoded_size = len(BYTES)

    if output == 'new':
        decoded = decode(encoded)
        decoded = numpy.frombuffer(decoded, 'uint8').reshape(16, 16)
        delta_decode(decoded, out=decoded, axis=-1)
        assert_array_equal(BYTESIMG, decoded)
    elif output == 'size':
        decoded = decode(encoded, out=decoded_size)
        decoded = numpy.frombuffer(decoded, 'uint8').reshape(16, 16)
        delta_decode(decoded, out=decoded, axis=-1)
        assert_array_equal(BYTESIMG, decoded)
        # with pytest.raises(RuntimeError):
        decode(encoded, buffersize=32, out=decoded_size)
    elif output == 'ndarray':
        decoded = numpy.zeros_like(BYTESIMG)
        decode(encoded, out=decoded.reshape(-1))
        delta_decode(decoded, out=decoded, axis=-1)
        assert_array_equal(BYTESIMG, decoded)
    elif output == 'bytearray':
        decoded = bytearray(decoded_size)
        decode(encoded, out=decoded)
        decoded = numpy.frombuffer(decoded, 'uint8').reshape(16, 16)
        delta_decode(decoded, out=decoded, axis=-1)
        assert_array_equal(BYTESIMG, decoded)


@pytest.mark.skipif(not imagecodecs.LZW, reason='LZW missing')
def test_lzw_decode_image_noeoi():
    """Test LZW decoder of input without EOI 512x512u2."""
    decode = imagecodecs.lzw_decode
    fname = datafiles('image_noeoi.lzw.bin')
    with open(fname, 'rb') as fh:
        encoded = fh.read()
    fname = datafiles('image_noeoi.bin')
    with open(fname, 'rb') as fh:
        decoded_known = fh.read()
    assert imagecodecs.lzw_check(encoded)
    # new output
    decoded = decode(encoded)
    assert decoded == decoded_known
    # provide output
    decoded = bytearray(len(decoded))
    decode(encoded, out=decoded)
    assert decoded == decoded_known
    # truncated output
    decoded = bytearray(100)
    decode(encoded, out=decoded)
    assert len(decoded) == 100


@pytest.mark.filterwarnings('ignore: PY_SSIZE_T_CLEAN')
@pytest.mark.parametrize(
    'output', ['new', 'bytearray', 'out', 'size', 'excess', 'trunc']
)
@pytest.mark.parametrize('length', [0, 2, 31 * 33 * 3])
@pytest.mark.parametrize('func', ['encode', 'decode'])
@pytest.mark.parametrize(
    'codec',
    [
        'bitshuffle',
        'brotli',
        'blosc',
        'blosc2',
        'bz2',
        'deflate',
        'gzip',
        'lz4',
        'lz4h',
        'lz4f',
        'lzf',
        'lzfse',
        'lzham',
        'lzma',
        'lzw',
        'snappy',
        'zlib',
        'zlibng',
        'zopfli',
        'zstd',
    ],
)
def test_compressors(codec, func, output, length):
    """Test various non-image codecs."""
    if length:
        data = numpy.random.randint(255, size=length, dtype='uint8').tobytes()
    else:
        data = b''

    if codec == 'blosc':
        if not imagecodecs.BLOSC or blosc is None:
            pytest.skip(f'{codec} missing')
        encode = imagecodecs.blosc_encode
        decode = imagecodecs.blosc_decode
        check = imagecodecs.blosc_check
        level = 9
        encoded = blosc.compress(data, clevel=level, typesize=1)
    elif codec == 'blosc2':
        if not imagecodecs.BLOSC2 or blosc2 is None:
            pytest.skip(f'{codec} missing')
        if IS_PYPY:
            pytest.xfail('blosc2.compress fails under PyPy')
        encode = imagecodecs.blosc2_encode
        decode = imagecodecs.blosc2_decode
        check = imagecodecs.blosc2_check
        level = 5
        encoded = blosc2.compress2(data, clevel=level, typesize=1)
    elif codec == 'zlib':
        if not imagecodecs.ZLIB or zlib is None:
            pytest.skip(f'{codec} missing')
        encode = imagecodecs.zlib_encode
        decode = imagecodecs.zlib_decode
        check = imagecodecs.zlib_check
        level = 5
        encoded = zlib.compress(data, level)
    elif codec == 'zlibng':
        if not imagecodecs.ZLIBNG or zlib is None:
            pytest.skip(f'{codec} missing')
        encode = imagecodecs.zlibng_encode
        decode = imagecodecs.zlibng_decode
        check = imagecodecs.zlibng_check
        level = 5
        encoded = zlib.compress(data, level)
    elif codec == 'deflate':
        if not imagecodecs.DEFLATE:
            pytest.skip(f'{codec} missing')
        encode = imagecodecs.deflate_encode
        decode = imagecodecs.deflate_decode
        check = imagecodecs.deflate_check
        level = 8
        # TODO: use a 3rd party libdeflate wrapper
        # encoded = deflate.compress(data, level)
        encoded = encode(data, level)
    elif codec == 'gzip':
        if not imagecodecs.GZIP:
            pytest.skip(f'{codec} missing')
        encode = imagecodecs.gzip_encode
        decode = imagecodecs.gzip_decode
        check = imagecodecs.gzip_check
        level = 8
        encoded = encode(data, level)
        # encoded = gzip.compress(data, level)
    elif codec == 'lzma':
        if not imagecodecs.LZMA or lzma is None:
            pytest.skip(f'{codec} missing')
        encode = imagecodecs.lzma_encode
        decode = imagecodecs.lzma_decode
        check = imagecodecs.lzma_check
        level = 6
        encoded = lzma.compress(data)
    elif codec == 'lzw':
        if not imagecodecs.LZW:
            pytest.skip(f'{codec} missing')
        encode = imagecodecs.lzw_encode
        decode = imagecodecs.lzw_decode
        check = imagecodecs.lzw_check
        level = 6
        encoded = encode(data, level)
    elif codec == 'zstd':
        if not imagecodecs.ZSTD or zstd is None:
            pytest.skip(f'{codec} missing')
        encode = imagecodecs.zstd_encode
        decode = imagecodecs.zstd_decode
        check = imagecodecs.zstd_check
        level = 5
        if length == 0:
            # bug in zstd.compress?
            encoded = encode(data, level)
        else:
            encoded = zstd.compress(data, level)
    elif codec == 'lzf':
        if not imagecodecs.LZF or lzf is None:
            pytest.skip(f'{codec} missing')
        encode = imagecodecs.lzf_encode
        decode = imagecodecs.lzf_decode
        check = imagecodecs.lzf_check
        level = 1
        encoded = lzf.compress(data, ((len(data) * 33) >> 5) + 1)
        if encoded is None:
            pytest.xfail("lzf can't compress empty input")
    elif codec == 'lzfse':
        if not imagecodecs.LZFSE or lzfse is None:
            pytest.skip(f'{codec} missing')
        encode = imagecodecs.lzfse_encode
        decode = imagecodecs.lzfse_decode
        check = imagecodecs.lzfse_check
        level = 1
        encoded = lzfse.compress(data)
    elif codec == 'lzham':
        # TODO: test against pylzham?
        if not imagecodecs.LZHAM:  # or lzham is None
            pytest.skip(f'{codec} missing')
        encode = imagecodecs.lzham_encode
        decode = imagecodecs.lzham_decode
        check = imagecodecs.lzham_check
        level = 5
        encoded = encode(data, level)
    elif codec == 'lz4':
        if not imagecodecs.LZ4 or lz4 is None:
            pytest.skip(f'{codec} missing')
        encode = imagecodecs.lz4_encode
        decode = imagecodecs.lz4_decode
        check = imagecodecs.lz4_check
        level = 1
        encoded = lz4.block.compress(data, store_size=False)
    elif codec == 'lz4h':
        if not imagecodecs.LZ4 or lz4 is None:
            pytest.skip(f'{codec} missing')

        def encode(*args, **kwargs):
            return imagecodecs.lz4_encode(*args, header=True, **kwargs)

        def decode(*args, **kwargs):
            return imagecodecs.lz4_decode(*args, header=True, **kwargs)

        check = imagecodecs.lz4_check
        level = 1
        encoded = lz4.block.compress(data, store_size=True)
    elif codec == 'lz4f':
        if not imagecodecs.LZ4F or lz4 is None:
            pytest.skip(f'{codec} missing')
        encode = imagecodecs.lz4f_encode
        decode = imagecodecs.lz4f_decode
        check = imagecodecs.lz4f_check
        level = 0
        encoded = lz4.frame.compress(data)
    elif codec == 'bz2':
        if not imagecodecs.BZ2 or bz2 is None:
            pytest.skip(f'{codec} missing')
        encode = imagecodecs.bz2_encode
        decode = imagecodecs.bz2_decode
        check = imagecodecs.bz2_check
        level = 9
        encoded = bz2.compress(data, compresslevel=level)
    elif codec == 'bitshuffle':
        if not imagecodecs.BITSHUFFLE or bitshuffle is None:
            pytest.skip(f'{codec} missing')
        encode = imagecodecs.bitshuffle_encode
        decode = imagecodecs.bitshuffle_decode
        check = imagecodecs.bitshuffle_check
        level = 0
        encoded = bitshuffle.bitshuffle(
            numpy.frombuffer(data, 'uint8')
        ).tobytes()
    elif codec == 'brotli':
        if not imagecodecs.BROTLI or brotli is None:
            pytest.skip(f'{codec} missing')
        if func == 'encode' and length == 0:
            # TODO: why?
            pytest.xfail('python-brotli returns different valid results')
        encode = imagecodecs.brotli_encode
        decode = imagecodecs.brotli_decode
        check = imagecodecs.brotli_check
        level = 11
        encoded = brotli.compress(data)
    elif codec == 'zopfli':
        if not imagecodecs.ZOPFLI or zopfli is None:
            pytest.skip(f'{codec} missing')
        encode = imagecodecs.zopfli_encode
        decode = imagecodecs.zopfli_decode
        check = imagecodecs.zopfli_check
        level = 1
        c = zopfli.ZopfliCompressor(zopfli.ZOPFLI_FORMAT_ZLIB)
        encoded = c.compress(data) + c.flush()
    elif codec == 'snappy':
        if not imagecodecs.SNAPPY or snappy is None:
            pytest.skip(f'{codec} missing')
        encode = imagecodecs.snappy_encode
        decode = imagecodecs.snappy_decode
        check = imagecodecs.snappy_check
        level = 1
        encoded = snappy.compress(data)
    else:
        raise ValueError(codec)

    assert check(encoded) in (None, True)

    if func == 'encode':
        size = len(encoded)
        if output == 'new':
            assert encoded == encode(data, level)
        elif output == 'bytearray':
            ret = encode(data, level, out=bytearray)
            assert encoded == ret
        elif output == 'size':
            if codec == 'lz4f':
                pytest.xfail(
                    'LZ4F_compressFrame cannot compress to exact output size'
                )
                encode(data, level, out=size)
            elif codec in ('deflate', 'gzip'):
                # https://github.com/ebiggers/libdeflate/issues/102
                ret = encode(data, level, out=size + 9)
            else:
                ret = encode(data, level, out=size)
            assert encoded == ret[:size]
        elif output == 'out':
            if codec == 'lz4f':
                pytest.xfail(
                    'LZ4F_compressFrame cannot compress to exact output size'
                )
                out = bytearray(size)
            elif codec == 'zstd':
                out = bytearray(max(size, 64))
            # elif codec == 'blosc':
            #     out = bytearray(max(size, 17))  # bug in blosc ?
            elif codec == 'lzf':
                out = bytearray(size + 1)  # bug in liblzf ?
            elif codec in ('deflate', 'gzip'):
                # https://github.com/ebiggers/libdeflate/issues/102
                out = bytearray(size + 9)
            else:
                out = bytearray(size)
            ret = encode(data, level, out=out)
            assert encoded == out[:size]
            assert encoded == ret
        elif output == 'excess':
            out = bytearray(size + 1021)
            ret = encode(data, level, out=out)
            if codec in ('blosc', 'blosc2'):
                # pytest.xfail('blosc output depends on output size')
                assert data == decode(ret)
            else:
                assert ret == out[:size]
                assert encoded == ret
        elif output == 'trunc':
            size = max(0, size - 1)
            out = bytearray(size)
            if size == 0 and codec == 'bitshuffle':
                encode(data, level, out=out) == b''
            else:
                with pytest.raises(RuntimeError):
                    encode(data, level, out=out)
        else:
            raise ValueError(output)
    elif func == 'decode':
        size = len(data)
        if output == 'new':
            assert data == decode(encoded)
        elif output == 'bytearray':
            ret = decode(encoded, out=bytearray)
            assert data == ret
        elif output == 'size':
            ret = decode(encoded, out=size)
            assert data == ret
        elif output == 'out':
            out = bytearray(size)
            ret = decode(encoded, out=out)
            assert data == out
            assert data == ret
        elif output == 'excess':
            out = bytearray(size + 1021)
            ret = decode(encoded, out=out)
            assert data == out[:size]
            assert data == ret
        elif output == 'trunc':
            size = max(0, size - 1)
            out = bytearray(size)
            if length == 0 or codec in ('bz2', 'lzma', 'lz4f', 'lzfse', 'lzw'):
                decode(encoded, out=out)
                assert data[:size] == out
            else:
                # most codecs don't support truncated output
                with pytest.raises(RuntimeError):
                    decode(encoded, out=out)
        else:
            raise ValueError(output)
    else:
        raise ValueError(func)


@pytest.mark.skipif(not imagecodecs.BITSHUFFLE, reason='bitshuffle missing')
@pytest.mark.parametrize('dtype', ['bytes', 'ndarray'])
@pytest.mark.parametrize('itemsize', [1, 2, 4, 8])
@pytest.mark.parametrize('blocksize', [0, 8, 64])
def test_bitshuffle_roundtrip(dtype, itemsize, blocksize):
    """Test Bitshuffle codec."""
    encode = imagecodecs.bitshuffle_encode
    decode = imagecodecs.bitshuffle_decode
    if dtype == 'bytes':
        data = numpy.random.randint(255, size=1024, dtype='uint8').tobytes()
    else:
        data = numpy.random.randint(255, size=1024, dtype=f'u{itemsize}')
        data.shape = 2, 4, 128
    encoded = encode(data, itemsize=itemsize, blocksize=blocksize)
    decoded = decode(encoded, itemsize=itemsize, blocksize=blocksize)
    if dtype == 'bytes':
        assert data == decoded
    else:
        assert_array_equal(data, decoded)


@pytest.mark.parametrize('numthreads', [1, 6])
@pytest.mark.parametrize('level', [None, 1])
@pytest.mark.parametrize('shuffle', ['noshuffle', 'shuffle', 'bitshuffle'])
@pytest.mark.parametrize(
    'compressor', ['blosclz', 'lz4', 'lz4hc', 'zlib', 'zstd']
)
@pytest.mark.parametrize('version', [1, 2])
def test_blosc_roundtrip(version, compressor, shuffle, level, numthreads):
    """Test Blosc codecs."""
    if version == 1:
        if not imagecodecs.BLOSC:
            pytest.skip('blosc missing')
        encode = imagecodecs.blosc_encode
        decode = imagecodecs.blosc_decode
        if compressor == 'zstd':
            compressor = imagecodecs.BLOSC.ZSTD
        if shuffle == 'bitshuffle':
            shuffle = imagecodecs.BLOSC.BITSHUFFLE
    else:
        if not imagecodecs.BLOSC2:
            pytest.skip('blosc2 missing')
        encode = imagecodecs.blosc2_encode
        decode = imagecodecs.blosc2_decode
        if compressor == 'zstd':
            compressor = imagecodecs.BLOSC2.ZSTD
        if shuffle == 'bitshuffle':
            shuffle = imagecodecs.BLOSC2.BITSHUFFLE
    data = numpy.random.randint(255, size=2021, dtype='uint8').tobytes()
    encoded = encode(
        data,
        level=level,
        compressor=compressor,
        shuffle=shuffle,
        numthreads=numthreads,
    )
    decoded = decode(encoded, numthreads=numthreads)
    assert data == decoded


# test data from libaec https://gitlab.dkrz.de/k202009/libaec/tree/master/data
AEC_TEST_DIR = osp.join(TEST_DIR, 'libaec/121B2TestData')

AEC_TEST_OPTIONS = list(
    osp.split(f)[-1][5:-3]
    for f in glob.glob(osp.join(AEC_TEST_DIR, 'AllOptions', '*.rz'))
)

AEC_TEST_EXTENDED = list(
    osp.split(f)[-1][:-3]
    for f in glob.glob(osp.join(AEC_TEST_DIR, 'ExtendedParameters', '*.rz'))
)


@pytest.mark.skipif(not imagecodecs.AEC, reason='aec missing')
@pytest.mark.parametrize('dtype', ['bytes', 'numpy'])
@pytest.mark.parametrize('name', AEC_TEST_EXTENDED)
def test_aec_extended(name, dtype):
    """Test AEC codec with libaec ExtendedParameters."""
    if name == 'sar32bit.j16.r256' and not (
        IS_CG or os.environ.get('AEC_TEST_EXTENDED', False)
    ):
        pytest.xfail('aec extension not built with ENABLE_RSI_PADDING')

    encode = imagecodecs.aec_encode
    decode = imagecodecs.aec_decode

    size = 512 * 512 * 4
    bitspersample = 32
    flags = imagecodecs.AEC.DATA_PREPROCESS | imagecodecs.AEC.PAD_RSI

    matches = re.search(r'j(\d+)\.r(\d+)', name).groups()
    blocksize = int(matches[0])
    rsi = int(matches[1])

    filename = osp.join(AEC_TEST_DIR, 'ExtendedParameters', f'{name}.rz')
    with open(filename, 'rb') as fh:
        rz = fh.read()

    filename = osp.join(
        AEC_TEST_DIR, 'ExtendedParameters', '{}.dat'.format(name.split('.')[0])
    )
    if dtype == 'bytes':
        with open(filename, 'rb') as fh:
            dat = fh.read()
        out = size
    else:
        dat = numpy.fromfile(filename, 'uint32').reshape(512, 512)
        out = numpy.zeros_like(dat)

    # decode
    decoded = decode(
        rz,
        bitspersample=bitspersample,
        flags=flags,
        blocksize=blocksize,
        rsi=rsi,
        out=out,
    )
    if dtype == 'bytes':
        assert decoded == dat
    else:
        pass

    # roundtrip
    if dtype == 'bytes':
        encoded = encode(
            dat,
            bitspersample=bitspersample,
            flags=flags,
            blocksize=blocksize,
            rsi=rsi,
        )
        # fails with AEC_DATA_ERROR if libaec wasn't built with libaec.diff
        decoded = decode(
            encoded,
            bitspersample=bitspersample,
            flags=flags,
            blocksize=blocksize,
            rsi=rsi,
            out=size,
        )
        assert decoded == dat
    else:
        encoded = encode(dat, flags=flags, blocksize=blocksize, rsi=rsi)
        # fails with AEC_DATA_ERROR if libaec wasn't built with libaec.diff
        decoded = decode(
            encoded, flags=flags, blocksize=blocksize, rsi=rsi, out=out
        )
        assert_array_equal(decoded, out)


@pytest.mark.skipif(not imagecodecs.AEC, reason='aec missing')
@pytest.mark.parametrize('name', AEC_TEST_OPTIONS)
def test_aec_options(name):
    """Test AEC codec with libaec 121B2TestData."""
    encode = imagecodecs.aec_encode
    decode = imagecodecs.aec_decode

    rsi = 128
    blocksize = 16
    flags = imagecodecs.AEC.DATA_PREPROCESS
    if 'restricted' in name:
        flags |= imagecodecs.AEC.RESTRICTED
    matches = re.search(r'p(\d+)n(\d+)', name).groups()
    size = int(matches[0])
    bitspersample = int(matches[1])

    if bitspersample > 8:
        size *= 2
    if bitspersample > 16:
        size *= 2

    filename = osp.join(AEC_TEST_DIR, 'AllOptions', f'test_{name}.rz')
    with open(filename, 'rb') as fh:
        rz = fh.read()

    filename = (
        filename.replace('.rz', '.dat')
        .replace('-basic', '')
        .replace('-restricted', '')
    )
    with open(filename, 'rb') as fh:
        dat = fh.read()
    out = size

    # decode
    decoded = decode(
        rz,
        bitspersample=bitspersample,
        flags=flags,
        blocksize=blocksize,
        rsi=rsi,
        out=out,
    )
    assert decoded == dat

    # roundtrip
    encoded = encode(
        dat,
        bitspersample=bitspersample,
        flags=flags,
        blocksize=blocksize,
        rsi=rsi,
    )
    decoded = decode(
        encoded,
        bitspersample=bitspersample,
        flags=flags,
        blocksize=blocksize,
        rsi=rsi,
        out=out,
    )
    assert decoded == dat


@pytest.mark.skipif(not imagecodecs.PGLZ, reason='pglz missing')
def test_pglz():
    """Test PGLZ codec"""
    decode = imagecodecs.pglz_decode
    encode = imagecodecs.pglz_encode
    data = b'111111181111111111111111121111111111111111111111111'

    with pytest.raises(RuntimeError):
        # not compressible
        encode(b'')
    with pytest.raises(ValueError):
        # output must be len(data) + 4
        encode(data, out=len(data))
    with pytest.raises(RuntimeError):
        # not enough output
        decode(encode(data), checkcomplete=True, out=4)
    with pytest.raises(RuntimeError):
        # default output too large
        assert decode(encode(data), checkcomplete=True) == data

    assert decode(b'') == b''
    assert decode(encode(data)) == data
    assert decode(encode(data, header=True), header=True) == data
    assert decode(encode(data), checkcomplete=True, out=len(data)) == data
    assert decode(encode(data), out=len(data)) == data
    assert decode(encode(data), out=len(data) + 7) == data
    assert decode(encode(data, strategy='always'), out=len(data)) == data

    data = data[:8]
    assert decode(encode(data, strategy='always'), out=len(data)) == data
    assert (
        decode(encode(data, strategy=[6, 100, 0, 100, 128, 6]), out=len(data))
        == data
    )
    with pytest.raises(RuntimeError):
        # data too short for default strategy
        encode(data)
    data = b'1234567890abcdefghijklmnopqrstuvwxyz'
    with pytest.raises(RuntimeError):
        # data not compressible
        encode(data, strategy='always')
    assert encode(data, header=True)[4:] == data
    assert decode(encode(data, header=True), header=True) == data


@pytest.mark.skipif(not imagecodecs.RCOMP, reason='rcomp missing')
@pytest.mark.parametrize('dtype', ['u1', 'u2', 'u4', 'i1', 'i2', 'i4'])
@pytest.mark.parametrize('case', [1, 2, 3, 4])
def test_rcomp(dtype, case):
    """Test RCOMP codec."""
    decode = imagecodecs.rcomp_decode
    encode = imagecodecs.rcomp_encode

    data = numpy.load(datafiles('rgb.u1.npy'))
    if dtype[0] == 'i':
        data = data.astype('i2')
        data -= 128
    data = data.astype(dtype)

    encoded = encode(data)
    if case == 1:
        assert_array_equal(
            data, decode(encoded, shape=data.shape, dtype=data.dtype)
        )
    elif case == 2:
        decoded = decode(encoded, shape=data.size, dtype=data.dtype)
        decoded = decoded.reshape(data.shape)
        assert_array_equal(data, decoded)
    elif case == 3:
        out = numpy.zeros_like(data)
        decode(encoded, out=out)
        assert_array_equal(data, out)
    elif case == 4:
        out = numpy.zeros_like(data)
        decode(encoded, shape=data.shape, dtype=data.dtype, out=out)
        assert_array_equal(data, out)


@pytest.mark.skipif(not imagecodecs.JETRAW, reason='jetraw missing')
def test_jetraw():
    """Test Jetraw codec."""
    data = readfile('jetraw.bin')
    im = numpy.empty((2304, 2304), numpy.uint16)
    imagecodecs.jetraw_decode(data, out=im)
    assert im[1490, 1830] == 36569

    imagecodecs.jetraw_init()
    try:
        encoded = imagecodecs.jetraw_encode(im, '500202_fast_bin1x')
    except imagecodecs.JetrawError as exc:
        errmsg = str(exc)
        if 'license' in errmsg:  # or 'identifier' in errmsg:
            # encoding requires a license
            return
        raise exc
    decoded = numpy.empty((2304, 2304), numpy.uint16)
    imagecodecs.jetraw_decode(encoded, out=decoded)
    assert im[1490, 1830] == 36569


@pytest.mark.skipif(not imagecodecs.RGBE, reason='rgbe missing')
def test_rgbe_decode():
    """Test RGBE decoding."""
    decode = imagecodecs.rgbe_decode
    encoded = readfile('384x256.hdr')

    out = decode(encoded)
    assert out.shape == (384, 256, 3)
    assert out.dtype == 'float32'
    assert tuple(out[227, 201]) == (133.0, 73.0, 39.0)

    out[:] = 0.0
    decode(encoded, out=out)
    assert tuple(out[227, 201]) == (133.0, 73.0, 39.0)

    with pytest.raises(ValueError):
        decode(encoded, header=False)

    with pytest.raises(ValueError):
        decode(encoded[77:])

    out[:] = 0.0
    decode(encoded[77:], out=out)
    assert tuple(out[227, 201]) == (133.0, 73.0, 39.0)

    out[:] = 0.0
    decode(encoded[77:], rle=True, out=out)
    assert tuple(out[227, 201]) == (133.0, 73.0, 39.0)

    with pytest.raises(ValueError):
        decode(encoded[77:], rle=False, out=out)

    with pytest.raises(imagecodecs.RgbeError):
        # RGBE_ReadPixels_RLE returned READ_ERROR
        decode(encoded, header=False, out=out)

    # no header, no rle
    encoded = readfile('384x256.rgbe.bin')
    with pytest.raises(ValueError):
        # output required if no header
        decode(encoded)

    out[:] = 0.0
    decode(encoded, out=out)
    assert tuple(out[227, 201]) == (133.0, 73.0, 39.0)
    image = out.copy()

    out[:] = 0.0
    decode(encoded, header=False, out=out)
    assert tuple(out[227, 201]) == (133.0, 73.0, 39.0)

    out[:] = 0.0
    decode(encoded, header=False, rle=False, out=out)
    assert tuple(out[227, 201]) == (133.0, 73.0, 39.0)

    # TODO: not sure why this succeeds
    # decoding non-rle data with rle=True
    out[:] = 0.0
    decode(encoded, header=False, rle=True, out=out)
    assert tuple(out[227, 201]) == (133.0, 73.0, 39.0)
    assert_array_equal(out, image)

    encoded_array = numpy.frombuffer(
        encoded, count=-1, dtype=numpy.uint8
    ).reshape((384, 256, 4))
    out = decode(encoded_array)
    assert out.shape == (384, 256, 3)
    assert out.dtype == 'float32'
    assert tuple(out[227, 201]) == (133.0, 73.0, 39.0)

    out[:] = 0.0
    decode(encoded_array, out=out)
    assert tuple(out[227, 201]) == (133.0, 73.0, 39.0)


@pytest.mark.skipif(not imagecodecs.RGBE, reason='rgbe missing')
def test_rgbe_roundtrip():
    """Test RGBE roundtrips."""
    encode = imagecodecs.rgbe_encode
    decode = imagecodecs.rgbe_decode

    data = decode(readfile('384x256.hdr'))
    assert data.shape == (384, 256, 3)
    assert data.dtype == 'float32'
    assert tuple(data[227, 201]) == (133.0, 73.0, 39.0)

    # encode to bytes
    encoded = encode(data)
    assert encoded[:10] == b'#?RADIANCE'
    assert_array_equal(data, decode(encoded))
    assert_array_equal(data, decode(encode(data, header=True)))
    assert_array_equal(data, decode(encode(data, header=True, rle=True)))
    assert_array_equal(data, decode(encode(data, out=bytearray)))

    assert_array_equal(data[0, 0], numpy.squeeze(decode(encode(data[0, 0]))))

    assert_array_equal(data, decode(encode(data, out=len(encoded))))
    assert_array_equal(data, decode(encode(data, out=len(encoded) + 4)))
    assert_array_equal(data, decode(encode(data, out=bytearray(len(encoded)))))

    with pytest.raises(imagecodecs.RgbeError):
        encode(data, out=1)

    with pytest.raises(imagecodecs.RgbeError):
        encode(data, out=len(encoded) - 1)

    # encode to bytes without header
    encoded = encode(data, header=False)
    assert encoded[:10] != b'#?RADIANCE'
    out = numpy.zeros_like(data)
    decode(encoded, out=out)
    assert_array_equal(data, out)

    encoded = encode(data, header=False, rle=True)
    out = numpy.zeros_like(data)
    decode(encoded, out=out)
    assert_array_equal(data, out)

    encoded = encode(data, header=False, rle=True)
    out = numpy.zeros_like(data)
    decode(encoded, out=out)
    assert_array_equal(data, out)

    # encode to output
    out = numpy.zeros((384, 256, 4), numpy.uint8)
    encode(data, out=out)
    assert_array_equal(decode(out), data)

    with pytest.raises(ValueError):
        encode(data, out=numpy.zeros((384, 256, 3), numpy.uint8))

    with pytest.raises(ValueError):
        encode(data, out=numpy.zeros((384, 255, 4), numpy.uint8))

    out = numpy.zeros((384 * 256 * 4), numpy.uint8)
    encode(data, out=out)
    assert_array_equal(decode(out.reshape((384, 256, 4))), data)


@pytest.mark.skipif(not imagecodecs.CMS, reason='cms missing')
def test_cms_profile():
    """Test cms_profile function."""
    from imagecodecs import cms_profile, cms_profile_validate, CmsError

    with pytest.raises(CmsError):
        cms_profile_validate(b'12345')

    profile = cms_profile(None)
    cms_profile_validate(profile)
    profile = cms_profile('null')
    cms_profile_validate(profile)
    profile = cms_profile('gray')
    cms_profile_validate(profile)
    profile = cms_profile('rgb')
    cms_profile_validate(profile)
    profile = cms_profile('srgb')
    cms_profile_validate(profile)
    profile = cms_profile('xyz')
    cms_profile_validate(profile)
    profile = cms_profile('lab2')
    cms_profile_validate(profile)
    profile = cms_profile('lab4')
    cms_profile_validate(profile)
    profile = cms_profile('adobergb')
    cms_profile_validate(profile)

    primaries = [
        2748779008 / 4294967295,
        1417339264 / 4294967295,
        1.0,
        1288490240 / 4294967295,
        2576980480 / 4294967295,
        1.0,
        644245120 / 4294967295,
        257698032 / 4294967295,
        1.0,
    ]
    whitepoint = [1343036288 / 4294967295, 1413044224 / 4294967295, 1.0]
    transferfunction = numpy.arange(1024, dtype=numpy.uint16)

    profile = cms_profile(
        'gray', whitepoint=whitepoint, transferfunction=transferfunction
    )
    cms_profile_validate(profile)

    transferfunction = transferfunction.astype(numpy.float32)
    transferfunction /= 1024
    profile = cms_profile(
        'rgb',
        whitepoint=whitepoint,
        primaries=primaries,
        transferfunction=transferfunction,
    )
    cms_profile_validate(profile)

    transferfunction = [transferfunction, transferfunction, transferfunction]
    profile = cms_profile(
        'rgb',
        whitepoint=whitepoint,
        primaries=primaries,
        transferfunction=transferfunction,
    )
    cms_profile_validate(profile)

    # xyY
    profile1 = cms_profile(
        'rgb',
        whitepoint=whitepoint,
        primaries=primaries,
        gamma=2.19921875,
    )
    cms_profile_validate(profile1)

    # xy
    profile2 = cms_profile(
        'rgb',
        whitepoint=[1343036288 / 4294967295, 1413044224 / 4294967295],
        primaries=[
            2748779008 / 4294967295,
            1417339264 / 4294967295,
            1288490240 / 4294967295,
            2576980480 / 4294967295,
            644245120 / 4294967295,
            257698032 / 4294967295,
        ],
        gamma=2.19921875,
    )
    cms_profile_validate(profile2)

    # xy rationals
    profile3 = cms_profile(
        'rgb',
        whitepoint=[1343036288, 4294967295, 1413044224, 4294967295],
        primaries=[
            2748779008,
            4294967295,
            1417339264,
            4294967295,
            1288490240,
            4294967295,
            2576980480,
            4294967295,
            644245120,
            4294967295,
            257698032,
            4294967295,
        ],
        gamma=2.19921875,
    )
    cms_profile_validate(profile3)

    assert profile1 == profile2
    assert profile1 == profile3


@pytest.mark.skipif(not imagecodecs.CMS, reason='cms missing')
def test_cms_output_shape():
    """Test _cms_output_shape function."""
    from imagecodecs._cms import _cms_output_shape, _cms_format

    for args, colorspace, planar, expected in (
        (((6, 7), 'u1', 'gray'), 'gray', 0, (6, 7)),
        (((6, 7, 2), 'u1', 'graya'), 'graya', 0, (6, 7, 2)),
        (((5, 6, 7), 'u1', 'gray'), 'gray', 0, (5, 6, 7)),
        (((6, 7, 3), 'u1', 'rgb'), 'gray', 0, (6, 7)),
        (((6, 7, 3), 'u1', 'rgb'), 'rgb', 0, (6, 7, 3)),
        (((6, 7, 3), 'u1', 'rgb'), 'rgba', 0, (6, 7, 4)),
        (((6, 7, 4), 'u1', 'rgba'), 'rgb', 0, (6, 7, 3)),
        (((6, 7, 4), 'u1', 'rgba'), 'cmyk', 0, (6, 7, 4)),
        (((6, 7), 'u1', 'gray'), 'rgb', 0, (6, 7, 3)),
        (((6, 7), 'u1', 'gray'), 'rgba', 0, (6, 7, 4)),
        # planar
        (((6, 7), 'u1', 'gray'), 'rgb', 1, (3, 6, 7)),
        (((6, 7, 2), 'u1', 'graya'), 'graya', 1, (2, 6, 7)),
        (((6, 7, 2), 'u1', 'graya'), 'rgba', 1, (4, 6, 7)),
        (((3, 6, 7), 'u1', 'rgb', 1), 'gray', 0, (6, 7)),
        (((3, 6, 7), 'u1', 'rgb', 1), 'rgb', 0, (6, 7, 3)),
        (((3, 6, 7), 'u1', 'rgb', 1), 'cmyk', 1, (4, 6, 7)),
        (((6, 7, 3), 'u1', 'rgb', 0), 'rgba', 1, (4, 6, 7)),
        (((5, 6, 7), 'u1', 'gray'), 'rgb', 1, (5, 3, 6, 7)),
        (((5, 3, 6, 7), 'u1', 'rgb', 1), 'rgba', 1, (5, 4, 6, 7)),
        (((5, 3, 6, 7), 'u1', 'rgb', 1), 'gray', 0, (5, 6, 7)),
    ):
        fmt = _cms_format(*args)
        # print(imagecodecs._cms._cms_format_decode(fmt))
        shape = _cms_output_shape(fmt, args[0], colorspace, planar)
        assert shape == expected

    fmt = _cms_format((6, 7), 'u1', 'gray')
    with pytest.raises(RuntimeError):
        # output planar with samples < 2
        _cms_output_shape(fmt, (6, 7), 'gray', 1)

    fmt = _cms_format((3, 6, 7), 'u1', 'rgb')
    with pytest.raises(RuntimeError):
        # input planar with ndim < 2
        _cms_output_shape(fmt, (6, 7), 'gray', 1)


@pytest.mark.skipif(not imagecodecs.CMS, reason='cms missing')
def test_cms_format():
    """Test _cms_format function."""
    from imagecodecs._cms import _cms_format, _cms_format_decode

    for args, (dtype, pixeltype, samples, planar, swap, swapfirst) in (
        # data types
        (((1, 1), 'u1'), ('u1', 3, 1, False, False, False)),
        (((1, 1), 'u2'), ('u2', 3, 1, False, False, False)),
        (((1, 1), '>u1'), ('u1', 3, 1, False, False, False)),
        (((1, 1), '>u2'), ('>u2', 3, 1, False, False, False)),
        # (((1, 1), '<f2'), ('f2', 3, 1, False, False, False)),
        (((1, 1), '>f4'), ('>f4', 3, 1, False, False, False)),
        (((1, 1), '<f8'), ('f8', 3, 1, False, False, False)),
        # auto detect pixeltype
        # always gray, except uint8 with 3|4 contig samples are RGB
        (((1, 1, 1), 'u1'), ('u1', 3, 1, False, False, False)),
        (((1, 1, 2), 'u1'), ('u1', 3, 1, False, False, False)),  # not GA
        (((1, 1, 3), 'u1'), ('u1', 4, 3, False, False, False)),
        (((1, 1, 4), 'u1'), ('u1', 4, 4, False, False, False)),
        (((1, 1, 5), 'u1'), ('u1', 3, 1, False, False, False)),  # not CMYKA
        (((1, 1, 6), 'u1'), ('u1', 3, 1, False, False, False)),
        (((1, 1, 3), 'u2'), ('u2', 3, 1, False, False, False)),  # not RGB
        (((1, 1, 4), 'u2'), ('u2', 3, 1, False, False, False)),  # not RGBA
        (((1, 1, 5), 'u2'), ('u2', 3, 1, False, False, False)),  # not CMYKA
        (((2, 1, 1), 'u1'), ('u1', 3, 1, False, False, False)),  # not GA
        (((3, 1, 1), 'u1'), ('u1', 3, 1, False, False, False)),  # not RGB
        (((1, 3), 'u1'), ('u1', 3, 1, False, False, False)),  # not RGB
        (((1, 1, 1, 3), 'u1'), ('u1', 3, 1, False, False, False)),  # not RGB
        # auto detect pixeltype with planar set
        (((1, 1, 3), 'u1', None, True), ('u1', 3, 1, True, False, False)),
        (((1, 1, 3), 'u1', None, False), ('u1', 4, 3, False, False, False)),
        (((1, 1, 4), 'u1', None, False), ('u1', 4, 4, False, False, False)),
        (((2, 1, 3), 'u1', None, True), ('u1', 3, 2, True, False, False)),
        (((2, 1, 3), 'u1', None, False), ('u1', 4, 3, False, False, False)),
        (((2, 1, 3), 'u2', None, False), ('u2', 4, 3, False, False, False)),
        (((2, 1, 4), 'u1', None, False), ('u1', 4, 4, False, False, False)),
        (((3, 1, 3), 'u1', None, True), ('u1', 4, 3, True, False, False)),
        (((4, 1, 3), 'u1', None, True), ('u1', 4, 4, True, False, False)),
        (((4, 1, 3), 'u2', None, True), ('u2', 4, 4, True, False, False)),
        # auto detect planar with colorspace set
        (((2, 1, 1), 'u1', 'gray'), ('u1', 3, 1, False, False, False)),
        (((2, 1, 2), 'u1', 'gray'), ('u1', 3, 1, False, False, False)),
        (((2, 1, 3), 'u1', 'gray'), ('u1', 3, 1, False, False, False)),
        (((2, 1, 2), 'u1', 'graya'), ('u1', 3, 2, False, False, False)),
        (((2, 1, 3), 'u1', 'graya'), ('u1', 3, 2, True, False, False)),
        (((3, 1, 3), 'u1', 'rgb'), ('u1', 4, 3, False, False, False)),
        (((3, 1, 4), 'u1', 'rgb'), ('u1', 4, 4, False, False, False)),
        (((3, 1, 4), 'u1', 'rgba'), ('u1', 4, 4, False, False, False)),
        (((4, 1, 3), 'u1', 'rgba'), ('u1', 4, 4, True, False, False)),
        (((3, 1, 2), 'u1', 'rgb'), ('u1', 4, 3, True, False, False)),
        (((4, 1, 3), 'u1', 'cmy'), ('u1', 5, 3, False, False, False)),
        (((4, 1, 3), 'u1', 'cmyk'), ('u1', 6, 4, True, False, False)),
        (((4, 1, 4), 'u1', 'cmyk'), ('u1', 6, 4, False, False, False)),
        (((4, 1, 5), 'u1', 'cmyk'), ('u1', 6, 5, False, False, False)),
        (((4, 1, 5), 'u1', 'cmyka'), ('u1', 6, 5, False, False, False)),
        (((5, 1, 4), 'u1', 'cmyka'), ('u1', 6, 5, True, False, False)),
        # colorspace and planar set
        (((2, 1, 1), 'u1', 'gray', False), ('u1', 3, 1, False, False, False)),
        (((2, 1, 2), 'u1', 'gray', False), ('u1', 3, 1, False, False, False)),
        (((2, 1, 3), 'u1', 'gray', False), ('u1', 3, 1, False, False, False)),
        (((2, 1, 2), 'u1', 'graya', False), ('u1', 3, 2, False, False, False)),
        (((2, 1, 3), 'u1', 'graya', True), ('u1', 3, 2, True, False, False)),
        (((3, 1, 3), 'u1', 'rgb', False), ('u1', 4, 3, False, False, False)),
        (((3, 1, 4), 'u1', 'rgb', False), ('u1', 4, 4, False, False, False)),
        (((3, 1, 4), 'u1', 'rgba', False), ('u1', 4, 4, False, False, False)),
        (((4, 1, 3), 'u1', 'rgba', True), ('u1', 4, 4, True, False, False)),
        (((4, 1, 3), 'u1', 'rgb', True), ('u1', 4, 4, True, False, False)),
        (((4, 1, 3), 'u1', 'cmy', False), ('u1', 5, 3, False, False, False)),
        (((3, 1, 3), 'u1', 'cmy', True), ('u1', 5, 3, True, False, False)),
        (((4, 1, 3), 'u1', 'cmyk', True), ('u1', 6, 4, True, False, False)),
        (((4, 1, 4), 'u1', 'cmyk', False), ('u1', 6, 4, False, False, False)),
        (((4, 1, 5), 'u1', 'cmyk', False), ('u1', 6, 5, False, False, False)),
        (((4, 1, 5), 'u1', 'cmyka', False), ('u1', 6, 5, False, False, False)),
        (((5, 1, 4), 'u1', 'cmyka', True), ('u1', 6, 5, True, False, False)),
        (((5, 1, 4), 'u1', 'cmyk', True), ('u1', 6, 5, True, False, False)),
        # swapped colorspaces
        (((3, 1, 1), 'u1', 'bgr'), ('u1', 4, 3, True, True, False)),
        (((4, 1, 1), 'u1', 'bgr'), ('u1', 4, 4, True, True, False)),
        (((4, 1, 1), 'u1', 'abgr'), ('u1', 4, 4, True, True, False)),
        (((4, 1, 1), 'u1', 'bgra'), ('u1', 4, 4, True, True, True)),
        (((4, 1, 1), 'u1', 'kymc'), ('u1', 6, 4, True, True, False)),
        (((4, 1, 1), 'u1', 'kcmy'), ('u1', 6, 4, True, False, True)),
    ):
        fmt = _cms_format(*args)
        fmt = _cms_format_decode(fmt)
        assert fmt.dtype == dtype
        assert fmt.pixeltype == pixeltype
        assert fmt.samples == samples
        assert fmt.planar == planar
        assert fmt.swap == swap
        assert fmt.swapfirst == swapfirst

    for args in (
        ((5, 1, 5), 'u1', None, False),  # cannot guess 5 noncontig samples
        ((5, 1, 5), 'u1', None, True),  # cannot guess 5 contig samples
        ((5, 1, 5), 'u1', 'rgb'),  # not rgb(a)
    ):
        with pytest.raises(ValueError):
            fmt = _cms_format(*args)
            fmt = _cms_format_decode(fmt)


@pytest.mark.skipif(not imagecodecs.CMS, reason='cms missing')
@pytest.mark.parametrize('dtype', list('BHfd'))
@pytest.mark.parametrize('outdtype', list('BHfd'))
@pytest.mark.parametrize('planar', [False, True])
@pytest.mark.parametrize('outplanar', [False, True])
@pytest.mark.parametrize('out', [None, True])
def test_cms_identity_transforms(dtype, outdtype, planar, outplanar, out):
    """Test CMS identity transforms."""
    from imagecodecs import cms_transform, cms_profile

    shape = (3, 256, 253) if planar else (256, 253, 3)
    dtype = numpy.dtype(dtype)

    outshape = (3, 256, 253) if outplanar else (256, 253, 3)
    outdtype = numpy.dtype(outdtype)
    if out:
        out = numpy.zeros(outshape, outdtype)
        outshape = None
        outdtype = None

    if dtype.kind == 'u':
        data = numpy.random.randint(
            0, 2 ** (dtype.itemsize * 8) - 1, shape, dtype
        )
    else:
        data = numpy.random.rand(*shape).astype(dtype)

    output = cms_transform(
        data,
        profile=cms_profile('srgb'),
        colorspace='rgb',
        outprofile=cms_profile('srgb'),
        outcolorspace='rgb',
        planar=planar,
        outplanar=outplanar,
        outdtype=outdtype,
        out=out,
    )
    if out is None:
        out = output
    if dtype == out.dtype or (dtype.kind == 'f' and out.dtype.kind == 'f'):
        if shape != out.shape:
            if planar:
                out = numpy.moveaxis(out, -1, 0)
            else:
                out = numpy.moveaxis(out, 0, -1)
        if dtype.kind == 'u':
            assert_array_equal(data, out)
        else:
            assert_allclose(data, out, rtol=1e-3)
    else:
        # TODO: how to verify?
        pass


@pytest.mark.parametrize('optimize', [False, True])
@pytest.mark.parametrize('smoothing', [0, 25])
@pytest.mark.parametrize('subsampling', ['444', '422', '420', '411', '440'])
@pytest.mark.parametrize('itype', ['rgb', 'rgba', 'gray'])
@pytest.mark.parametrize('codec', ['jpeg8', 'jpeg12', 'mozjpeg'])
def test_jpeg_encode(codec, itype, subsampling, smoothing, optimize):
    """Test various JPEG encode options."""
    # general and default options are tested in test_image_roundtrips
    atol = 24 if subsampling != '411' else 48
    if codec == 'jpeg8':
        if not imagecodecs.JPEG8:
            pytest.skip('jpeg8 missing')
        dtype = 'uint8'
        decode = imagecodecs.jpeg8_decode
        encode = imagecodecs.jpeg8_encode
        atol = atol
    elif codec == 'jpeg12':
        if not imagecodecs.JPEG12:
            pytest.skip('jpeg12 missing')
        if not optimize:
            pytest.xfail('jpeg12 fails without optimize')
        dtype = 'uint16'
        decode = imagecodecs.jpeg12_decode
        encode = imagecodecs.jpeg12_encode
        atol = atol * 16
    elif codec == 'mozjpeg':
        if not imagecodecs.MOZJPEG:
            pytest.skip('mozjpeg missing')
        dtype = 'uint8'
        decode = imagecodecs.mozjpeg_decode
        encode = imagecodecs.mozjpeg_encode
        atol = atol
    else:
        raise ValueError(codec)

    dtype = numpy.dtype(dtype)
    data = image_data(itype, dtype)
    data = data[:32, :16].copy()  # make divisible by subsamples

    encoded = encode(
        data,
        level=95,
        subsampling=subsampling,
        smoothing=smoothing,
        optimize=optimize,
    )
    decoded = decode(encoded)

    if itype == 'gray':
        decoded = decoded.reshape(data.shape)

    assert_allclose(data, decoded, atol=atol)


@pytest.mark.skipif(not imagecodecs.JPEG8, reason='jpeg8 missing')
@pytest.mark.parametrize('output', ['new', 'out'])
def test_jpeg8_decode(output):
    """Test JPEG 8-bit decoder with separate tables."""
    decode = imagecodecs.jpeg8_decode
    data = readfile('bytes.jpeg8.bin')
    tables = readfile('bytes.jpeg8_tables.bin')

    if output == 'new':
        decoded = decode(data, tables=tables)
    elif output == 'out':
        decoded = numpy.zeros_like(BYTESIMG)
        decode(data, tables=tables, out=decoded)
    elif output == 'bytearray':
        decoded = bytearray(BYTESIMG.size * BYTESIMG.itemsize)
        decoded = decode(data, out=decoded)
    assert_array_equal(BYTESIMG, decoded)


@pytest.mark.skipif(not imagecodecs.JPEG12, reason='jpeg12 missing')
@pytest.mark.parametrize('output', ['new', 'out', 'bytearray'])
def test_jpeg12_decode(output):
    """Test JPEG 12-bit decoder with separate tables."""
    decode = imagecodecs.jpeg12_decode
    data = readfile('words.jpeg12.bin')
    tables = readfile('words.jpeg12_tables.bin')

    if output == 'new':
        decoded = decode(data, tables=tables)
    elif output == 'out':
        decoded = numpy.zeros_like(WORDSIMG)
        decode(data, tables=tables, out=decoded)
    elif output == 'bytearray':
        decoded = bytearray(WORDSIMG.size * WORDSIMG.itemsize)
        decoded = decode(data, out=decoded)

    assert (
        numpy.max(
            numpy.abs(WORDSIMG.astype('int32') - decoded.astype('int32'))
        )
        < 2
    )


@pytest.mark.skipif(not imagecodecs.JPEG8, reason='jpeg8 missing')
def test_jpeg_rgb_mode():
    """Test JPEG encoder in RGBA mode."""
    # https://github.com/cgohlke/tifffile/issues/146
    RGB = imagecodecs.JPEG8.CS.RGB
    data = image_data('rgb', 'uint8')
    encoded = imagecodecs.jpeg_encode(
        data, colorspace=RGB, outcolorspace=RGB, subsampling='444', level=99
    )
    assert b'JFIF' not in encoded[:16]
    decoded = imagecodecs.jpeg_decode(
        encoded,
        colorspace=RGB,
        outcolorspace=RGB,
    )
    assert_allclose(data, decoded, atol=8)


@pytest.mark.skipif(not imagecodecs.MOZJPEG, reason='mozjpeg missing')
def test_mozjpeg():
    """Test MOZJPEG codec parameters."""
    data = readfile('bytes.jpeg8.bin')
    tables = readfile('bytes.jpeg8_tables.bin')
    decoded = imagecodecs.mozjpeg_decode(data, tables=tables)
    assert_array_equal(BYTESIMG, decoded)

    data = image_data('rgb', 'uint8')
    encoded = imagecodecs.mozjpeg_encode(
        data,
        level=90,
        outcolorspace='ycbcr',
        subsampling='444',
        quanttable=2,
        notrellis=True,
    )
    decoded = imagecodecs.mozjpeg_decode(encoded)
    assert_allclose(data, decoded, atol=16, rtol=0)


@pytest.mark.parametrize('codec', ['ljpeg', 'jpegsof3'])
@pytest.mark.parametrize(
    'fname, result',
    [
        ('1px.ljp', ((1, 1), 'uint16', (0, 0), 0)),
        ('2ch.ljp', ((3528, 2640, 2), 'uint16', (1500, 1024, 1), 3195)),
        ('2dht.ljp', ((288, 384, 3), 'uint8', (22, 56), (150, 67, 166))),
        ('3dht.ljp', ((240, 320, 3), 'uint8', (140, 93), (184, 161, 110))),
        ('gray16.ljp', ((535, 800), 'uint16', (418, 478), 54227)),
        ('gray8.ljp', ((535, 800), 'uint8', (418, 478), 211)),
        ('rgb24.ljp', ((535, 800, 3), 'uint8', (418, 478), (226, 209, 190))),
        ('dng0.ljp', ((256, 256), 'uint16', (111, 75), 51200)),
        ('dng1.ljp', ((256, 256), 'uint16', (111, 75), 51200)),
        ('dng2.ljp', ((256, 256), 'uint16', (111, 75), 51200)),
        ('dng3.ljp', ((256, 256), 'uint16', (111, 75), 51200)),
        ('dng4.ljp', ((256, 256), 'uint16', (111, 75), 51200)),
        ('dng5.ljp', ((256, 256), 'uint16', (111, 75), 51200)),
        ('dng6.ljp', ((256, 256), 'uint16', (111, 75), 51200)),
        ('dng7.ljp', ((256, 256), 'uint16', (111, 75), 51200)),
        ('dcm1-8bit.ljp', ((512, 512), 'uint8', (256, 256), 51)),
        ('dcm1.ljp', ((256, 256), 'uint16', (169, 97), 1192)),
        ('dcm2.ljp', ((256, 256), 'uint16', (169, 97), 1192)),
        ('dcm3.ljp', ((256, 256), 'uint16', (169, 97), 1192)),
        ('dcm4.ljp', ((256, 256), 'uint16', (169, 97), 1192)),
        ('dcm5.ljp', ((256, 256), 'uint16', (169, 97), 1192)),
        ('dcm6.ljp', ((256, 256), 'uint16', (169, 97), 1192)),
        ('dcm7.ljp', ((256, 256), 'uint16', (169, 97), 1192)),
        # tile from Apple DNG
        ('linearraw.ljp', ((378, 504, 3), 'uint16', (20, 30), (114, 212, 88))),
        # https://github.com/cgohlke/imagecodecs/issues/61
        ('pvrg.ljp', ((4608, 2928), 'uint16', (823, 2166), 3050)),
    ],
)
def test_ljpeg(fname, result, codec):
    """Test Lossless JPEG decoders."""
    if codec == 'ljpeg':
        if not imagecodecs.LJPEG:
            pytest.skip('ljpeg missing')
        decode = imagecodecs.ljpeg_decode
        check = imagecodecs.ljpeg_check
    else:
        if not imagecodecs.JPEGSOF3:
            pytest.skip('jpegsof3 missing')
        if fname in ('dcm6.ljp', 'dcm7.ljp'):
            return  # jpegsof3 segfault
        if fname in ('dng0.ljp',):
            pytest.xfail('jpegsof3 known failure or crash')
        decode = imagecodecs.jpegsof3_decode
        check = imagecodecs.jpegsof3_check
    if fname == 'pvrg.ljp':
        pytest.xfail('corrupted LJPEG produced by PVRG')

    try:
        data = readfile(os.path.join('ljpeg', fname))
    except FileNotFoundError:
        pytest.skip(f'{fname} not found')

    assert check(data) in (None, True)
    decoded = decode(data)

    shape, dtype, index, value = result
    assert decoded.shape == shape
    assert decoded.dtype == dtype
    assert_array_equal(decoded[index], value)


@pytest.mark.parametrize('output', ['new', 'out', 'bytearray'])
@pytest.mark.parametrize('fname', ['gray8.ljp', 'gray16.ljp'])
@pytest.mark.parametrize('codec', ['jpegsof3', 'ljpeg'])
def test_jpegsof3(fname, output, codec):
    """Test JPEG SOF3 decoder with 8 and 16-bit images."""
    if codec == 'ljpeg':
        if not imagecodecs.LJPEG:
            pytest.skip('ljpeg missing')
        decode = imagecodecs.ljpeg_decode
        check = imagecodecs.ljpeg_check
    else:
        if not imagecodecs.JPEGSOF3:
            pytest.skip('jpegsof3 missing')
        decode = imagecodecs.jpegsof3_decode
        check = imagecodecs.jpegsof3_check

    shape = 535, 800
    if fname == 'gray8.ljp':
        dtype = 'uint8'
        value = 75
        memmap = True  # test read-only, jpegsof3_decode requires writable
    elif fname == 'gray16.ljp':
        dtype = 'uint16'
        value = 19275
        memmap = False

    data = readfile(os.path.join('ljpeg', fname), memmap=memmap)

    assert check(data) in (None, True)

    if output == 'new':
        decoded = decode(data)
    elif output == 'out':
        decoded = numpy.zeros(shape, dtype)
        decode(data, out=decoded)
    elif output == 'bytearray':
        decoded = bytearray(535 * 800 * numpy.dtype(dtype).itemsize)
        decoded = decode(data, out=decoded)

    assert decoded.shape == shape
    assert decoded.dtype == dtype
    assert decoded[500, 600] == value


@pytest.mark.skipif(not imagecodecs.JPEGXL, reason='jpegxl missing')
@pytest.mark.parametrize('dtype', ['uint8', 'uint16', 'float16', 'float32'])
def test_jpegxl_planar(dtype):
    """Test JPEG XL roundtrip with frames and planar channels."""
    image = image_data('channels', dtype, planar=True, frames=True)
    assert image.shape == (11, 8, 32, 31)
    encoded = imagecodecs.jpegxl_encode(image, photometric='gray', planar=True)
    decoded = imagecodecs.jpegxl_decode(encoded)
    assert_array_equal(image, decoded)


@pytest.mark.skipif(not imagecodecs.JPEGXL, reason='jpegxl missing')
def test_jpegxl_bitspersample():
    """Test JPEG XL with 12 bitspersample."""
    image = image_data('rgb', 'uint16')
    image >>= 4
    encoded = imagecodecs.jpegxl_encode(image, bitspersample=12)
    decoded = imagecodecs.jpegxl_decode(encoded)
    assert_array_equal(image, decoded)


@pytest.mark.skipif(not imagecodecs.JPEGXR, reason='jpegxr missing')
@pytest.mark.parametrize('output', ['new', 'out', 'bytearray'])
def test_jpegxr_decode(output):
    """Test JPEG XR decoder with RGBA32 image."""
    decode = imagecodecs.jpegxr_decode
    image = readfile('rgba32.jxr.bin')
    image = numpy.frombuffer(image, dtype='uint8').reshape(100, 100, -1)
    data = readfile('rgba32.jxr')

    assert imagecodecs.jpegxr_check(data) in (None, True)

    if output == 'new':
        decoded = decode(data)
    elif output == 'out':
        decoded = numpy.zeros_like(image)
        decode(data, out=decoded)
    elif output == 'bytearray':
        decoded = bytearray(image.size * image.itemsize)
        decoded = decode(data, out=decoded)
    assert_array_equal(image, decoded)


@pytest.mark.skipif(not imagecodecs.JPEGXR, reason='jpegxr missing')
@pytest.mark.parametrize('fp2int', [False, True])
def test_jpegxr_fixedpoint(fp2int):
    """Test JPEG XR decoder with Fixed Point 16 image."""
    # test file provided by E. Pojar on 2021.1.27
    data = readfile('fixedpoint.jxr')
    assert imagecodecs.jpegxr_check(data) in (None, True)
    decoded = imagecodecs.jpegxr_decode(data, fp2int=fp2int)
    if fp2int:
        assert decoded.dtype == 'int16'
        assert decoded[0, 0] == -32765
        assert decoded[255, 255] == 32766
    else:
        assert decoded.dtype == 'float32'
        assert abs(decoded[0, 0] + 3.9996338) < 1e-6
        assert abs(decoded[255, 255] - 3.9997559) < 1e-6


@pytest.mark.skipif(not imagecodecs.AVIF, reason='avif missing')
def test_avif_strict_disabled():
    """Test AVIF decoder with file created by old version of libavif."""
    data = readfile('rgba.u1.strict_disabled.avif')
    assert imagecodecs.avif_check(data)
    decoded = imagecodecs.avif_decode(data)
    assert decoded.dtype == 'uint8'
    assert decoded.shape == (32, 31, 4)
    assert tuple(decoded[16, 16]) == (44, 123, 57, 88)


@pytest.mark.skipif(not IS_CG, reason='avif missing')
@pytest.mark.parametrize('codec', ['auto', 'aom', 'rav1e', 'svt'])  # 'libgav1'
def test_avif_encoder(codec):
    """Test various AVIF encoder codecs."""
    data = numpy.load(datafiles('rgb.u1.npy'))
    if codec == 'svt':
        data = data[:200, :300]
        pixelformat = '420'
    else:
        pixelformat = None
    encoded = imagecodecs.avif_encode(
        data, level=6, codec=codec, pixelformat=pixelformat
    )
    decoded = imagecodecs.avif_decode(encoded)
    assert_allclose(decoded, data, atol=5, rtol=0)


@pytest.mark.skipif(not imagecodecs.JPEGLS, reason='jpegls missing')
@pytest.mark.parametrize('output', ['new', 'out', 'bytearray'])
def test_jpegls_decode(output):
    """Test JPEG LS decoder with RGBA32 image."""
    decode = imagecodecs.jpegls_decode
    data = readfile('rgba.u1.jls')
    dtype = 'uint8'
    shape = 32, 31, 4

    assert imagecodecs.jpegls_check(data) in (None, True)

    if output == 'new':
        decoded = decode(data)
    elif output == 'out':
        decoded = numpy.zeros(shape, dtype)
        decode(data, out=decoded)
    elif output == 'bytearray':
        decoded = bytearray(shape[0] * shape[1] * shape[2])
        decoded = decode(data, out=decoded)

    assert decoded.dtype == dtype
    assert decoded.shape == shape
    assert decoded[25, 25, 1] == 97
    assert decoded[-1, -1, -1] == 63


@pytest.mark.skipif(not imagecodecs.BRUNSLI, reason='brunsli missing')
@pytest.mark.parametrize('output', ['new', 'out', 'bytearray'])
def test_brunsli_decode(output):
    """Test Brunsli decoder with RGBA32 image."""
    decode = imagecodecs.brunsli_decode
    data = readfile('rgba.u1.br')
    dtype = 'uint8'
    shape = 32, 31, 4

    assert imagecodecs.brunsli_check(data) in (None, True)

    if output == 'new':
        decoded = decode(data)
    elif output == 'out':
        decoded = numpy.zeros(shape, dtype)
        decode(data, out=decoded)
    elif output == 'bytearray':
        decoded = bytearray(shape[0] * shape[1] * shape[2])
        decoded = decode(data, out=decoded)

    assert decoded.dtype == dtype
    assert decoded.shape == shape
    assert decoded[25, 25, 1] == 100
    assert decoded[-1, -1, -1] == 81


@pytest.mark.skipif(not imagecodecs.BRUNSLI, reason='brunsli missing')
def test_brunsli_encode_jpeg():
    """Test Brunsli encoder with JPEG input."""
    encode = imagecodecs.brunsli_encode
    decode = imagecodecs.brunsli_decode
    jpg = readfile('rgba.u1.jpg')
    jxl = readfile('rgba.u1.br')

    assert imagecodecs.brunsli_check(jpg) in (None, True)
    assert imagecodecs.brunsli_check(jxl) in (None, True)

    encoded = encode(jpg)
    assert encoded == jxl

    decoded = decode(encoded)
    assert decoded.dtype == 'uint8'
    assert decoded.shape == (32, 31, 4)
    assert decoded[25, 25, 1] == 100
    assert decoded[-1, -1, -1] == 81


@pytest.mark.skipif(not imagecodecs.WEBP, reason='webp missing')
@pytest.mark.parametrize('output', ['new', 'out', 'bytearray'])
def test_webp_decode(output):
    """Test WebP decoder with RGBA32 image."""
    decode = imagecodecs.webp_decode
    data = readfile('rgba.u1.webp')
    dtype = 'uint8'
    shape = 32, 31, 4

    assert imagecodecs.webp_check(data)

    if output == 'new':
        decoded = decode(data)
    elif output == 'out':
        decoded = numpy.zeros(shape, dtype)
        decode(data, out=decoded)
    elif output == 'bytearray':
        decoded = bytearray(shape[0] * shape[1] * shape[2])
        decoded = decode(data, out=decoded)

    assert decoded.dtype == dtype
    assert decoded.shape == shape
    assert decoded[25, 25, 1] == 94  # lossy
    assert decoded[-1, -1, -1] == 63


@pytest.mark.skipif(not imagecodecs.WEBP, reason='webp missing')
def test_webp_opaque():
    """Test WebP roundtrip with opaque image."""
    # libwebp drops all-opaque alpha channel
    data = image_data('rgba', 'uint8')
    data[..., 3] = 255

    encoded = imagecodecs.webp_encode(data, level=90, lossless=True, method=5)
    decoded = imagecodecs.webp_decode(encoded)
    assert decoded.shape == (data.shape[0], data.shape[1], 3)
    assert_array_equal(decoded, data[..., :3])

    decoded = imagecodecs.webp_decode(encoded, hasalpha=True)
    assert_array_equal(decoded, data)


@pytest.mark.skipif(not imagecodecs.ZFP, reason='zfp missing')
@pytest.mark.parametrize('execution', [None, 'omp'])
@pytest.mark.parametrize('mode', [(None, None), ('p', None)])  # ('r', 24)
@pytest.mark.parametrize('deout', ['new', 'out', 'bytearray'])  # 'view',
@pytest.mark.parametrize('enout', ['new', 'out', 'bytearray'])
@pytest.mark.parametrize('itype', ['rgba', 'view', 'gray', 'line'])
@pytest.mark.parametrize('dtype', ['float32', 'float64', 'int32', 'int64'])
def test_zfp(dtype, itype, enout, deout, mode, execution):
    """Test ZFP codec."""
    kwargs = {}
    if execution == 'omp':
        if os.environ.get('SKIP_OMP', False):
            pytest.skip('omp test skip because of environment variable')
        kwargs['numthreads'] = 2
        kwargs['chunksize'] = None
    decode = imagecodecs.zfp_decode
    encode = imagecodecs.zfp_encode
    mode, level = mode
    dtype = numpy.dtype(dtype)
    itemsize = dtype.itemsize
    data = image_data(itype, dtype)
    shape = data.shape

    kwargs = dict(mode=mode, level=level, execution=execution, **kwargs)
    encoded = encode(data, **kwargs)

    assert imagecodecs.zfp_check(encoded)

    if enout == 'new':
        pass
    elif enout == 'out':
        encoded = numpy.zeros(len(encoded), 'uint8')
        encode(data, out=encoded, **kwargs)
    elif enout == 'bytearray':
        encoded = bytearray(len(encoded))
        encode(data, out=encoded, **kwargs)

    if deout == 'new':
        decoded = decode(encoded)
    elif deout == 'out':
        decoded = numpy.zeros(shape, dtype)
        decode(encoded, out=decoded)
    elif deout == 'view':
        temp = numpy.zeros((shape[0] + 5, shape[1] + 5, shape[2]), dtype)
        decoded = temp[2 : 2 + shape[0], 3 : 3 + shape[1], :]
        decode(encoded, out=decoded)
    elif deout == 'bytearray':
        decoded = bytearray(shape[0] * shape[1] * shape[2] * itemsize)
        decoded = decode(encoded, out=decoded)
        decoded = numpy.asarray(decoded, dtype=dtype).reshape(shape)

    if dtype.char == 'f':
        atol = 1e-6
    else:
        atol = 20
    assert_allclose(data, decoded, atol=atol, rtol=0)


@pytest.mark.skipif(not imagecodecs.LERC, reason='lerc missing')
# @pytest.mark.parametrize('version', [None, 3])
@pytest.mark.parametrize('level', [None, 0.02])
@pytest.mark.parametrize('planar', [None, True])
@pytest.mark.parametrize('deout', ['new', 'out', 'bytearray'])
@pytest.mark.parametrize('enout', ['new', 'out', 'bytearray'])
@pytest.mark.parametrize('itype', ['gray', 'rgb', 'rgba', 'channels', 'stack'])
@pytest.mark.parametrize(
    'dtype', ['uint8', 'int8', 'uint16', 'int32', 'float32', 'float64']
)
def test_lerc(dtype, itype, enout, deout, planar, level, version=None):
    """Test LERC codec."""
    if version is not None and version < 4 and itype != 'gray':
        pytest.xfail('lerc version does not support this case')
    decode = imagecodecs.lerc_decode
    encode = imagecodecs.lerc_encode
    dtype = numpy.dtype(dtype)
    itemsize = dtype.itemsize
    data = image_data(itype, dtype)
    shape = data.shape
    if level is not None and dtype.kind != 'f':
        level = level * 256

    kwargs = dict(level=level, version=version, planar=planar)
    encoded = encode(data, **kwargs)

    assert imagecodecs.lerc_check(encoded)

    if enout == 'new':
        pass
    elif enout == 'out':
        encoded = numpy.zeros(len(encoded), 'uint8')
        encode(data, out=encoded, **kwargs)
    elif enout == 'bytearray':
        encoded = bytearray(len(encoded))
        encode(data, out=encoded, **kwargs)

    if deout == 'new':
        decoded = decode(encoded)
    elif deout == 'out':
        decoded = numpy.zeros(shape, dtype)
        out = decoded if planar else numpy.squeeze(decoded)
        decode(encoded, out=out)
    elif deout == 'bytearray':
        decoded = bytearray(shape[0] * shape[1] * shape[2] * itemsize)
        decoded = decode(encoded, out=decoded)
        decoded = numpy.asarray(decoded, dtype=dtype).reshape(shape)

    if itype == 'gray':
        decoded = decoded.reshape(shape)

    if level is None:
        level = 0.00001 if dtype.kind == 'f' else 0
    assert_allclose(data, decoded, atol=level, rtol=0)


@pytest.mark.skipif(not imagecodecs.LERC, reason='lerc missing')
@pytest.mark.parametrize(
    'file',
    [
        'world.lerc1',
        'california_400_400_1_float.lerc2',
        'bluemarble_256_256_3_byte.lerc2',
        'zstd.lerc2',
    ],
)
def test_lerc_files(file):
    """Test LERC decoder with lerc testData files."""
    with open(datafiles(f'lerc/{file}'), 'rb') as fh:
        encoded = fh.read()

    decoded = imagecodecs.lerc_decode(encoded, masks=False)
    decoded1, masks = imagecodecs.lerc_decode(encoded, masks=True)

    assert_array_equal(decoded, decoded1)

    if file[:4] != 'zstd':
        out = numpy.zeros_like(masks)
        decoded1, _ = imagecodecs.lerc_decode(encoded, masks=out)
        assert_array_equal(masks, out)

    if file[:5] == 'world':
        assert decoded.dtype == numpy.float32
        assert decoded.shape == (257, 257)
        assert int(decoded[146, 144]) == 1131
        assert masks.dtype == bool
        assert masks.shape == (257, 257)
        assert masks[146, 144] == bool(1)
    elif file[:4] == 'cali':
        assert decoded.dtype == numpy.float32
        assert decoded.shape == (400, 400)
        assert int(decoded[200, 200]) == 1554
        assert masks.dtype == bool
        assert masks.shape == (400, 400)
        assert masks[200, 200] == bool(1)
    elif file[:4] == 'blue':
        assert decoded.dtype == numpy.uint8
        assert decoded.shape == (3, 256, 256)
        assert tuple(decoded[:, 128, 128]) == (2, 5, 20)
        assert masks.dtype == bool
        assert masks.shape == (256, 256)
        assert masks[128, 128] == bool(1)
    elif file[:4] == 'zstd':
        assert decoded.dtype == numpy.uint8
        assert decoded.shape == (512, 512, 3)
        assert tuple(decoded[128, 128]) == (85, 89, 38)
        assert masks is None


@pytest.mark.skipif(not imagecodecs.LERC, reason='lerc missing')
@pytest.mark.parametrize('compression', [None, 'zstd', 'deflate'])
def test_lerc_compression(compression):
    """Test LERC with compression."""
    data = image_data('rgb', 'uint16')
    compressionargs = {
        None: None,
        'zstd': {'level': 10},
        'deflate': {'level': 7},
    }[compression]
    compressed = imagecodecs.lerc_encode(
        data, compression=compression, compressionargs=compressionargs
    )
    decompressed = imagecodecs.lerc_decode(compressed)
    assert_array_equal(data, decompressed)


@pytest.mark.skipif(not imagecodecs.LERC or IS_PYPY, reason='lerc missing')
def test_lerc_masks():
    """Test LERC codec with masks."""

    stack = image_data('stack', numpy.float32)
    masks = image_data('stack', bool)

    # 1 band, no mask
    data = stack[0]
    encoded = imagecodecs.lerc_encode(data)
    decoded, masks1 = imagecodecs.lerc_decode(encoded, masks=True)
    assert masks1 is None
    assert_allclose(data, decoded, atol=0.00001, rtol=0)

    # 1 band, 1 mask
    data = stack[0]
    encoded = imagecodecs.lerc_encode(data, masks=masks[0])
    decoded, masks1 = imagecodecs.lerc_decode(encoded, masks=True)
    assert_array_equal(masks[0], masks1)

    # 1 band, 3 masks
    data = stack[:3]
    encoded = imagecodecs.lerc_encode(data, masks=masks[0], planar=True)
    decoded, masks1 = imagecodecs.lerc_decode(encoded, masks=True)
    assert_array_equal(masks[0], masks1)

    # 3 bands, 3 masks
    data = stack[:3]
    encoded = imagecodecs.lerc_encode(
        data,
        masks=masks[:3],
        planar=True,
    )
    decoded, masks1 = imagecodecs.lerc_decode(encoded, masks=True)
    assert_array_equal(masks[:3], masks1)

    # out
    out = numpy.zeros_like(masks[:3])
    decoded, _ = imagecodecs.lerc_decode(encoded, masks=out)
    assert_array_equal(masks[:3], out)


@pytest.mark.skipif(not imagecodecs.JPEG2K, reason='jpeg2k missing')
@pytest.mark.parametrize('output', ['new', 'out', 'bytearray'])
def test_jpeg2k_int8_4bit(output):
    """Test JPEG 2000 decoder with int8, 4-bit image."""
    decode = imagecodecs.jpeg2k_decode
    data = readfile('int8_4bit.j2k')
    dtype = 'int8'
    shape = 256, 256

    assert imagecodecs.jpeg2k_check(data)

    if output == 'new':
        decoded = decode(data, verbose=2)
    elif output == 'out':
        decoded = numpy.zeros(shape, dtype)
        decode(data, out=decoded)
    elif output == 'bytearray':
        decoded = bytearray(shape[0] * shape[1])
        decoded = decode(data, out=decoded)

    assert decoded.dtype == dtype
    assert decoded.shape == shape
    assert decoded[0, 0] == -6
    assert decoded[-1, -1] == 2


@pytest.mark.skipif(not imagecodecs.JPEG2K, reason='jpeg2k missing')
def test_jpeg2k_ycbc():
    """Test JPEG 2000 decoder with subsampling."""
    decode = imagecodecs.jpeg2k_decode
    data = readfile('ycbc.j2k')

    assert imagecodecs.jpeg2k_check(data)

    decoded = decode(data, verbose=2)
    assert decoded.dtype == 'uint8'
    assert decoded.shape == (256, 256, 3)
    assert tuple(decoded[0, 0]) == (243, 243, 240)
    assert tuple(decoded[-1, -1]) == (0, 0, 0)

    decoded = decode(data, verbose=2, planar=True)
    assert decoded.dtype == 'uint8'
    assert decoded.shape == (3, 256, 256)
    assert tuple(decoded[:, 0, 0]) == (243, 243, 240)
    assert tuple(decoded[:, -1, -1]) == (0, 0, 0)


@pytest.mark.skipif(not imagecodecs.JPEG2K, reason='jpeg2k missing')
@pytest.mark.parametrize('codecformat', [0, 2])
def test_jpeg2k_codecformat(codecformat):
    """Test JPEG 2000 codecformats."""
    data = image_data('rgb', 'uint16')
    encoded = imagecodecs.jpeg2k_encode(
        data, codecformat=codecformat, verbose=2
    )
    assert imagecodecs.jpeg2k_check(encoded) in (None, True)
    decoded = imagecodecs.jpeg2k_decode(encoded, verbose=2)
    assert_array_equal(data, decoded)


@pytest.mark.skipif(not imagecodecs.JPEG2K, reason='jpeg2k missing')
@pytest.mark.parametrize('numthreads', [1, 2])
def test_jpeg2k_numthreads(numthreads):
    """Test JPEG 2000 numthreads."""
    data = image_data('rgb', 'uint8')
    encoded = imagecodecs.jpeg2k_encode(data, numthreads=numthreads, verbose=2)
    assert imagecodecs.jpeg2k_check(encoded) in (None, True)
    decoded = imagecodecs.jpeg2k_decode(
        encoded, numthreads=numthreads, verbose=2
    )
    assert_array_equal(data, decoded)


@pytest.mark.skipif(not imagecodecs.JPEG2K, reason='jpeg2k missing')
@pytest.mark.parametrize('reversible', [False, True])
def test_jpeg2k_reversible(reversible):
    """Test JPEG 2000 reversible."""
    data = image_data('rgb', 'uint8')
    encoded = imagecodecs.jpeg2k_encode(
        data, level=50, reversible=reversible, verbose=2
    )
    assert imagecodecs.jpeg2k_check(encoded) in (None, True)
    decoded = imagecodecs.jpeg2k_decode(encoded, verbose=2)
    assert_allclose(data, decoded, atol=8)


@pytest.mark.skipif(not imagecodecs.JPEG2K, reason='jpeg2k missing')
@pytest.mark.parametrize('mct', [False, True])
def test_jpeg2k_mct(mct):
    """Test JPEG 2000 mct."""
    data = image_data('rgb', 'uint8')
    encoded = imagecodecs.jpeg2k_encode(data, level=50, mct=mct, verbose=2)
    assert imagecodecs.jpeg2k_check(encoded) in (None, True)
    decoded = imagecodecs.jpeg2k_decode(encoded, verbose=2)
    assert_allclose(data, decoded, atol=8)


@pytest.mark.skipif(not imagecodecs.JPEG2K, reason='jpeg2k missing')
@pytest.mark.parametrize('bitspersample', [None, True])
@pytest.mark.parametrize('dtype', ['u1', 'u2', 'u4', 'i1', 'i2', 'i4'])
@pytest.mark.parametrize('planar', [False, True])
def test_jpeg2k(dtype, planar, bitspersample):
    """Test JPEG 2000 codec."""
    dtype = numpy.dtype(dtype)
    itemsize = dtype.itemsize
    data = image_data('rgb', dtype)

    if bitspersample:
        if itemsize == 1:
            bitspersample = 7
            data //= 2
        elif itemsize == 2:
            bitspersample = 12
            if dtype != 'uint16':
                data //= 16
        elif itemsize == 4:
            bitspersample = 26  # max ~26 bits
            data //= 64
    elif itemsize == 4:
        data //= 128  # max 26 bits

    if planar:
        data = numpy.moveaxis(data, -1, 0)

    encoded = imagecodecs.jpeg2k_encode(
        data, planar=planar, bitspersample=bitspersample, verbose=2
    )
    assert imagecodecs.jpeg2k_check(encoded) in (None, True)
    decoded = imagecodecs.jpeg2k_decode(encoded, planar=planar, verbose=2)
    assert_array_equal(data, decoded)


@pytest.mark.skipif(not imagecodecs.JPEGXR, reason='jpegxr missing')
@pytest.mark.parametrize('level', [None, 90, 0.4])
@pytest.mark.parametrize('deout', ['new', 'out', 'bytearray'])  # 'view',
@pytest.mark.parametrize('enout', ['new', 'out', 'bytearray'])
@pytest.mark.parametrize(
    'itype',
    [
        'gray uint8',
        'gray uint16',
        'gray float16',
        'gray float32',
        'rgb uint8',
        'rgb uint16',
        'rgb float16',
        'rgb float32',
        'rgba uint8',
        'rgba uint16',
        'rgba float16',
        'rgba float32',
        'channels uint8',
        'channelsa uint8',
        'channels uint16',
        'channelsa uint16',
        'cmyk uint8',
        'cmyka uint8',
    ],
)
def test_jpegxr(itype, enout, deout, level):
    """Test JPEG XR codec."""
    decode = imagecodecs.jpegxr_decode
    encode = imagecodecs.jpegxr_encode
    itype, dtype = itype.split()
    dtype = numpy.dtype(dtype)
    itemsize = dtype.itemsize
    data = image_data(itype, dtype)
    shape = data.shape

    kwargs = dict(level=level)
    if itype.startswith('cmyk'):
        kwargs['photometric'] = 'cmyk'
    if itype.endswith('a'):
        kwargs['hasalpha'] = True

    encoded = encode(data, **kwargs)

    assert imagecodecs.jpegxr_check(encoded) in (None, True)

    if enout == 'new':
        pass
    elif enout == 'out':
        encoded = numpy.zeros(len(encoded), 'uint8')
        encode(data, out=encoded, **kwargs)
    elif enout == 'bytearray':
        encoded = bytearray(len(encoded))
        encode(data, out=encoded, **kwargs)

    if deout == 'new':
        decoded = decode(encoded)
    elif deout == 'out':
        decoded = numpy.zeros(shape, dtype)
        decode(encoded, out=numpy.squeeze(decoded))
    elif deout == 'view':
        temp = numpy.zeros((shape[0] + 5, shape[1] + 5, shape[2]), dtype)
        decoded = temp[2 : 2 + shape[0], 3 : 3 + shape[1], :]
        decode(encoded, out=numpy.squeeze(decoded))
    elif deout == 'bytearray':
        decoded = bytearray(shape[0] * shape[1] * shape[2] * itemsize)
        decoded = decode(encoded, out=decoded)
        decoded = numpy.asarray(decoded, dtype=dtype).reshape(shape)

    if itype == 'gray':
        decoded = decoded.reshape(shape)

    if level is None:
        atol = 0.00001 if dtype.kind == 'f' else 1
    if level == 90:
        atol = 0.005 if dtype.kind == 'f' else 8 if dtype == 'uint8' else 12
    else:
        atol = 0.1 if dtype.kind == 'f' else 64 if dtype == 'uint8' else 700
    assert_allclose(data, decoded, atol=atol, rtol=0)


@pytest.mark.skipif(not imagecodecs.PNG, reason='png missing')
def test_png_encode_fast():
    """Test PNG encoder with fast settings."""
    data = image_data('rgb', numpy.uint8).squeeze()
    encoded = imagecodecs.png_encode(
        data,
        level=imagecodecs.PNG.COMPRESSION.SPEED,
        strategy=imagecodecs.PNG.STRATEGY.RLE,
        filter=imagecodecs.PNG.FILTER.SUB,
    )
    decoded = imagecodecs.png_decode(encoded)
    assert_array_equal(data, decoded, verbose=True)


@pytest.mark.skipif(not imagecodecs.APNG, reason='apng missing')
def test_apng_encode_fast():
    """Test APNG encoder with fast settings."""
    data = image_data('rgb', numpy.uint8).squeeze()
    encoded = imagecodecs.apng_encode(
        data,
        level=imagecodecs.APNG.COMPRESSION.SPEED,
        strategy=imagecodecs.APNG.STRATEGY.RLE,
        filter=imagecodecs.APNG.FILTER.SUB,
    )
    decoded = imagecodecs.apng_decode(encoded)
    assert_array_equal(data, decoded, verbose=True)


@pytest.mark.skipif(not imagecodecs.PNG, reason='png missing')
def test_png_error():
    """Test PNG exceptions."""
    data = image_data('rgb', numpy.uint8).squeeze()
    encoded = imagecodecs.png_encode(data)

    with pytest.raises(imagecodecs.PngError):
        imagecodecs.png_encode(data, out=bytearray(len(encoded) // 2))

    with pytest.raises(imagecodecs.PngError):
        imagecodecs.png_decode(encoded[: len(encoded) // 2])


@pytest.mark.skipif(not imagecodecs.APNG, reason='apng missing')
def test_apng_error():
    """Test APNG exceptions."""
    data = image_data('rgb', numpy.uint8).squeeze()
    encoded = imagecodecs.apng_encode(data)

    with pytest.raises(imagecodecs.ApngError):
        imagecodecs.apng_encode(data, out=bytearray(len(encoded) // 2))

    with pytest.raises(imagecodecs.ApngError):
        imagecodecs.apng_decode(encoded[: len(encoded) // 2])


@pytest.mark.skipif(not imagecodecs.APNG, reason='apng missing')
@pytest.mark.parametrize('dtype', ['uint8', 'uint16'])
@pytest.mark.parametrize('samples', [1, 2, 3, 4])
def test_apng(samples, dtype):
    """Test APNG codec."""
    shape = (9, 32, 31, samples) if samples > 1 else (9, 32, 31)
    data = numpy.random.randint(
        numpy.iinfo(dtype).max, size=9 * 32 * 31 * samples, dtype=dtype
    ).reshape(shape)
    encoded = imagecodecs.apng_encode(data, delay=100)
    decoded = imagecodecs.apng_decode(encoded)
    assert_array_equal(data, decoded, verbose=True)
    decoded = imagecodecs.apng_decode(encoded, index=0)
    assert_array_equal(data[0], decoded, verbose=True)
    for index in (0, 5, 8):
        decoded = imagecodecs.apng_decode(encoded, index=index)
        assert_array_equal(data[index], decoded, verbose=True)
    if imagecodecs.PNG:
        assert_array_equal(
            imagecodecs.png_decode(encoded), data[0], verbose=True
        )


@pytest.mark.skipif(not imagecodecs.SPNG, reason='spng missing')
@pytest.mark.parametrize('itype', ['rgb', 'rgba', 'gray', 'graya'])
@pytest.mark.parametrize('dtype', ['uint8', 'uint16'])
@pytest.mark.parametrize('level', [None, 5, -1])
def test_spng_encode(itype, dtype, level):
    """Test SPNG encoder."""
    data = image_data(itype, numpy.dtype(dtype)).squeeze()
    encoded = imagecodecs.spng_encode(data, level=level)
    decoded = imagecodecs.png_decode(encoded)
    assert_array_equal(data, decoded, verbose=True)


@pytest.mark.parametrize('level', [None, 5, -1])
@pytest.mark.parametrize('deout', ['new', 'out', 'view', 'bytearray'])
@pytest.mark.parametrize('enout', ['new', 'out', 'bytearray'])
@pytest.mark.parametrize('itype', ['rgb', 'rgba', 'view', 'gray', 'graya'])
@pytest.mark.parametrize('dtype', ['uint8', 'uint16'])
@pytest.mark.parametrize(
    'codec',
    [
        'apng',
        'avif',
        'brunsli',
        'heif',
        'jpeg2k',
        'jpeg8',
        'jpeg12',
        'jpegls',
        'jpegxl',
        'jpegxr',
        'ljpeg',
        'mozjpeg',
        'png',
        'qoi',
        'spng',
        'webp',
    ],
)
def test_image_roundtrips(codec, dtype, itype, enout, deout, level):
    """Test various image codecs."""
    if codec == 'jpeg8':
        if not imagecodecs.JPEG8:
            pytest.skip(f'{codec} missing')
        if itype in ('view', 'graya') or deout == 'view' or dtype == 'uint16':
            pytest.xfail('jpeg8 does not support this case')
        decode = imagecodecs.jpeg8_decode
        encode = imagecodecs.jpeg8_encode
        check = imagecodecs.jpeg8_check
        atol = 24
        if level:
            level += 95
    elif codec == 'jpeg12':
        if not imagecodecs.JPEG12:
            pytest.skip(f'{codec} missing')
        if itype in ('view', 'graya') or deout == 'view' or dtype == 'uint8':
            pytest.xfail('jpeg12 does not support this case')
        decode = imagecodecs.jpeg12_decode
        encode = imagecodecs.jpeg12_encode
        check = imagecodecs.jpeg12_check
        atol = 24 * 16
        if level:
            level += 95
    elif codec == 'mozjpeg':
        if not imagecodecs.MOZJPEG:
            pytest.skip(f'{codec} missing')
        if itype in ('view', 'graya') or deout == 'view' or dtype == 'uint16':
            pytest.xfail('mozjpeg does not support this case')
        decode = imagecodecs.mozjpeg_decode
        encode = imagecodecs.mozjpeg_encode
        check = imagecodecs.mozjpeg_check
        atol = 24
        if level:
            level += 95
    elif codec == 'ljpeg':
        if not imagecodecs.LJPEG:
            pytest.skip(f'{codec} missing')
        if itype in ('rgb', 'rgba', 'view', 'graya') or deout == 'view':
            pytest.xfail('ljpeg does not support this case')
        decode = imagecodecs.ljpeg_decode
        encode = imagecodecs.ljpeg_encode
        check = imagecodecs.ljpeg_check
        if dtype == 'uint16':

            def encode(data, *args, **kwargs):
                return imagecodecs.ljpeg_encode(
                    data, bitspersample=12, *args, **kwargs
                )

    elif codec == 'jpegls':
        if not imagecodecs.JPEGLS:
            pytest.skip(f'{codec} missing')
        if itype in ('view', 'graya') or deout == 'view':
            pytest.xfail('jpegls does not support this case')
        decode = imagecodecs.jpegls_decode
        encode = imagecodecs.jpegls_encode
        check = imagecodecs.jpegls_check
    elif codec == 'webp':
        if not imagecodecs.WEBP:
            pytest.skip(f'{codec} missing')
        decode = imagecodecs.webp_decode
        encode = imagecodecs.webp_encode
        check = imagecodecs.webp_check
        if dtype != 'uint8' or itype.startswith('gray'):
            pytest.xfail('webp does not support this case')
        if itype == 'rgba':

            def decode(data, out=None):
                return imagecodecs.webp_decode(data, hasalpha=True, out=out)

        if level:
            level += 95
    elif codec == 'png':
        if not imagecodecs.PNG:
            pytest.skip(f'{codec} missing')
        decode = imagecodecs.png_decode
        encode = imagecodecs.png_encode
        check = imagecodecs.png_check
    elif codec == 'apng':
        if not imagecodecs.APNG:
            pytest.skip(f'{codec} missing')
        if itype == 'view' or deout == 'view':
            pytest.xfail('apng does not support this case')
        decode = imagecodecs.apng_decode
        encode = imagecodecs.apng_encode
        check = imagecodecs.apng_check
    elif codec == 'spng':
        if not imagecodecs.SPNG:
            pytest.skip(f'{codec} missing')
        if itype == 'view' or deout == 'view':
            pytest.xfail('spng does not support this case')
        if itype == 'graya' or (
            dtype == 'uint16' and itype in ('gray', 'rgb')
        ):
            pytest.xfail('spng does not support this case')
        decode = imagecodecs.spng_decode
        encode = imagecodecs.spng_encode
        check = imagecodecs.spng_check
    elif codec == 'qoi':
        if not imagecodecs.QOI:
            pytest.skip(f'{codec} missing')
        decode = imagecodecs.qoi_decode
        encode = imagecodecs.qoi_encode
        check = imagecodecs.qoi_check
        if (
            itype in ('view', 'gray', 'graya')
            or deout == 'view'
            or dtype == 'uint16'
        ):
            pytest.xfail('qoi does not support this case')
    elif codec == 'jpeg2k':
        if not imagecodecs.JPEG2K:
            pytest.skip(f'{codec} missing')
        if itype == 'view' or deout == 'view':
            pytest.xfail('jpeg2k does not support this case')
        check = imagecodecs.jpeg2k_check
        if level and level > 0:
            level = 100 - level  # psnr

        # enable verbose mode for rare failures
        def encode(data, *args, **kwargs):
            return imagecodecs.jpeg2k_encode(data, verbose=3, *args, **kwargs)

        def decode(data, *args, **kwargs):
            return imagecodecs.jpeg2k_decode(data, verbose=3, *args, **kwargs)

    elif codec == 'jpegxl':
        if not imagecodecs.JPEGXL:
            pytest.skip(f'{codec} missing')
        if itype == 'view' or deout == 'view':
            pytest.xfail('jpegxl does not support this case')
        if level:
            level += 95
        decode = imagecodecs.jpegxl_decode
        encode = imagecodecs.jpegxl_encode
        check = imagecodecs.jpegxl_check
    elif codec == 'brunsli':
        if not imagecodecs.BRUNSLI:
            pytest.skip(f'{codec} missing')
        if itype in ('view', 'graya') or deout == 'view' or dtype == 'uint16':
            pytest.xfail('brunsli does not support this case')
        decode = imagecodecs.brunsli_decode
        encode = imagecodecs.brunsli_encode
        check = imagecodecs.brunsli_check
        atol = 24
        if level:
            level += 95
    elif codec == 'jpegxr':
        if not imagecodecs.JPEGXR:
            pytest.skip(f'{codec} missing')
        if itype == 'graya' or deout == 'view':
            pytest.xfail('jpegxr does not support this case')
        decode = imagecodecs.jpegxr_decode
        encode = imagecodecs.jpegxr_encode
        check = imagecodecs.jpegxr_check
        atol = 10
        if level:
            level = (level + 95) / 100
    elif codec == 'avif':
        if not imagecodecs.AVIF:
            pytest.skip(f'{codec} missing')
        if itype in ('gray', 'graya', 'view') or deout == 'view':
            pytest.xfail('avif does not support this case')
        decode = imagecodecs.avif_decode
        encode = imagecodecs.avif_encode
        check = imagecodecs.avif_check
        if dtype == 'uint16':

            def encode(data, *args, **kwargs):
                return imagecodecs.avif_encode(
                    data, bitspersample=12, *args, **kwargs
                )

        atol = 10
    elif codec == 'heif':
        if not imagecodecs.HEIF:
            pytest.skip(f'{codec} missing')
        if (
            itype in ('gray', 'graya', 'view')
            or deout == 'view'
            or dtype == 'uint16'
        ):
            pytest.xfail('heif does not support this case')
        decode = imagecodecs.heif_decode
        encode = imagecodecs.heif_encode
        check = imagecodecs.heif_check
        atol = 10
        if level:
            level += 95
        if int(imagecodecs.heif_version().split('.')[1]) < 12:
            pytest.xfail('libheif < 1.12 cannot encode small images')
    else:
        raise ValueError(codec)

    dtype = numpy.dtype(dtype)
    itemsize = dtype.itemsize
    data = image_data(itype, dtype)
    shape = data.shape

    if enout == 'new':
        encoded = encode(data, level=level)
    elif enout == 'out':
        encoded = numpy.zeros(
            2 * shape[0] * shape[1] * shape[2] * itemsize, 'uint8'
        )
        ret = encode(data, level=level, out=encoded)
        if codec in ('brunsli', 'avif'):
            # Brunsli and avif decoder don't like extra bytes
            encoded = encoded[: len(ret)]
    elif enout == 'bytearray':
        encoded = bytearray(2 * shape[0] * shape[1] * shape[2] * itemsize)
        ret = encode(data, level=level, out=encoded)
        if codec in ('brunsli', 'avif'):
            # Brunsli and avif decoder don't like extra bytes
            encoded = encoded[: len(ret)]

    if enout != 'out':
        assert check(encoded) in (None, True)

    if deout == 'new':
        decoded = decode(encoded)
    elif deout == 'out':
        decoded = numpy.zeros(shape, dtype)
        decode(encoded, out=numpy.squeeze(decoded))
    elif deout == 'view':
        temp = numpy.zeros((shape[0] + 5, shape[1] + 5, shape[2]), dtype)
        decoded = temp[2 : 2 + shape[0], 3 : 3 + shape[1], :]
        decode(encoded, out=numpy.squeeze(decoded))
    elif deout == 'bytearray':
        decoded = bytearray(shape[0] * shape[1] * shape[2] * itemsize)
        decoded = decode(encoded, out=decoded)
        decoded = numpy.asarray(decoded, dtype=dtype).reshape(shape)

    if itype == 'gray':
        decoded = decoded.reshape(shape)

    if codec == 'webp' and level is not None:  # or itype == 'rgba'
        assert_allclose(data, decoded, atol=32)
    elif codec in ('jpeg8', 'jpeg12', 'jpegxr', 'brunsli', 'mozjpeg', 'heif'):
        assert_allclose(data, decoded, atol=atol)
    elif codec == 'jpegls' and level == 5:
        assert_allclose(data, decoded, atol=6)
    elif codec == 'jpeg2k' and level == 95:
        assert_allclose(data, decoded, atol=6)
    elif codec == 'jpegxl' and level is not None:
        atol = 256 if dtype.itemsize > 1 else 8
        if level < 100:
            atol *= 4
        assert_allclose(data, decoded, atol=atol)
    elif codec == 'avif' and level == 5:
        if dtype.itemsize > 1:
            # TODO: bug in libavif?
            pytest.xfail('why does this fail?')
            atol = 32
        else:
            atol = 6
        assert_allclose(data, decoded, atol=atol)
    else:
        assert_array_equal(data, decoded, verbose=True)


@pytest.mark.skipif(not imagecodecs.GIF, reason='GIF missing')
@pytest.mark.parametrize('deout', ['new', 'out', 'bytearray'])  # 'view'
@pytest.mark.parametrize('enout', ['new', 'out', 'bytearray'])
@pytest.mark.parametrize('frames', [False, True])
@pytest.mark.parametrize('index', [None, 0])
def test_gif_roundtrips(index, frames, enout, deout):
    """Test GIF codec."""
    decode = imagecodecs.gif_decode
    encode = imagecodecs.gif_encode

    dtype = numpy.dtype('uint8')
    data = numpy.squeeze(image_data('gray', dtype, frames=frames))
    if index == 0 and frames:
        shaped = data.shape[1:] + (3,)
    else:
        shaped = data.shape + (3,)
    sized = data.size * 3

    if enout == 'new':
        encoded = encode(data)
    elif enout == 'out':
        encoded = numpy.zeros(2 * data.size, 'uint8')
        encode(data, out=encoded)
    elif enout == 'bytearray':
        encoded = bytearray(2 * data.size)
        encode(data, out=encoded)

    assert imagecodecs.gif_check(encoded)

    if deout == 'new':
        decoded = decode(encoded, index=index)
    elif deout == 'out':
        decoded = numpy.zeros(shaped, dtype)
        decode(encoded, index=index, out=numpy.squeeze(decoded))
    elif deout == 'bytearray':
        decoded = bytearray(sized)
        decoded = decode(encoded, index=index, out=decoded)
        decoded = numpy.asarray(decoded, dtype=dtype).reshape(shaped)

    if index == 0 and frames:
        data = data[index]
    assert_array_equal(data, decoded[..., 1], verbose=True)


@pytest.mark.skipif(not imagecodecs.PNG, reason='png missing')
def test_png_rgba_palette():
    """Test decoding indexed PNG with transparency."""
    png = readfile('rgba.u1.pal.png')
    image = imagecodecs.png_decode(png)
    assert tuple(image[6, 15]) == (255, 255, 255, 0)
    assert tuple(image[6, 16]) == (141, 37, 52, 255)

    if imagecodecs.APNG:
        image = imagecodecs.apng_decode(png)
        assert tuple(image[6, 15]) == (255, 255, 255, 0)
        assert tuple(image[6, 16]) == (141, 37, 52, 255)


TIFF_TEST_DIR = osp.join(TEST_DIR, 'tiff/')
TIFF_FILES = list(
    osp.split(f)[-1][:-4] for f in glob.glob(osp.join(TIFF_TEST_DIR, '*.tif'))
)


@pytest.mark.skipif(not imagecodecs.TIFF, reason='tiff missing')
@pytest.mark.skipif(tifffile is None, reason='tifffile missing')
@pytest.mark.parametrize('asrgb', [False, True])
@pytest.mark.parametrize('name', TIFF_FILES)
def test_tiff_files(name, asrgb):
    """Test TIFF decode with existing files against tifffile."""
    decode = imagecodecs.tiff_decode
    if (
        'depth' in name
        or 'jpeg.u2' in name
        or (not IS_CG and ('webp' in name or 'zstd' in name or 'lzma' in name))
    ):
        pytest.xfail('not supported by libtiff or tiff_decode')

    filename = osp.join(TIFF_TEST_DIR, f'{name}.tif')
    with open(filename, 'rb') as fh:
        encoded = mmap.mmap(fh.fileno(), 0, access=mmap.ACCESS_READ)

    assert imagecodecs.tiff_check(encoded)

    if asrgb:
        if (
            'b1' in name
            or 'u1' in name
            or 'u2' in name
            or 'i1' in name
            or 'i2' in name
        ):
            decoded = decode(encoded, index=0, asrgb=1, verbose=1)
        else:
            with pytest.raises(imagecodecs.TiffError):
                decoded = decode(encoded, index=0, asrgb=1, verbose=1)
        return

    if 'b1' in name:
        pytest.xfail('not supported yet')
    data = tifffile.imread(filename)
    decoded = decode(encoded, index=None, verbose=1)
    if 'jpeg' in name:
        # tiff_decode returns RGBA for jpeg, tifffile returns RGB
        decoded = decoded[..., :3]
    assert_array_equal(data, decoded)


@pytest.mark.skipif(not imagecodecs.TIFF, reason='tiff missing')
@pytest.mark.skipif(tifffile is None, reason='tifffile missing')
@pytest.mark.parametrize('index', [0, 3, 10, 1048576, None, list, slice])
def test_tiff_index(index):
    """Test TIFF decoder index arguments."""
    filename = osp.join(TIFF_TEST_DIR, 'gray.series.u1.tif')
    with open(filename, 'rb') as fh:
        encoded = fh.read()
    if index == 10 or index == 1048576:
        with pytest.raises((IndexError, OverflowError)):
            decoded = imagecodecs.tiff_decode(encoded, index=index)
    elif index == list:
        data = tifffile.imread(filename, series=1)
        decoded = imagecodecs.tiff_decode(encoded, index=[1, 3, 5, 7])
        assert_array_equal(data, decoded)
    elif index == slice:
        for index in (slice(None), slice(1, None, None), slice(1, 3, None)):
            with pytest.raises((IndexError, ValueError)):
                decoded = imagecodecs.tiff_decode(encoded, index=index)
        data = tifffile.imread(filename, series=1)
        for index in (slice(1, None, 2), slice(1, 8, 2)):
            decoded = imagecodecs.tiff_decode(encoded, index=index)
            assert_array_equal(data, decoded)
    elif index is None:
        data = tifffile.imread(filename)
        decoded = imagecodecs.tiff_decode(encoded, index=None)
        assert_array_equal(data, decoded)
    else:
        data = tifffile.imread(filename, key=index)
        decoded = imagecodecs.tiff_decode(encoded, index=index)
        assert_array_equal(data, decoded)


@pytest.mark.skipif(not imagecodecs.TIFF, reason='')
@pytest.mark.skipif(tifffile is None, reason='tifffile missing')
def test_tiff_asrgb():
    """Test TIFF decoder asrgb arguments."""
    filename = osp.join(TIFF_TEST_DIR, 'gray.series.u1.tif')
    with open(filename, 'rb') as fh:
        encoded = fh.read()

    data = tifffile.imread(filename, series=0)
    decoded = imagecodecs.tiff_decode(encoded, index=None, asrgb=True)
    assert decoded.shape[-1] == 4
    assert_array_equal(data, decoded[..., 0])

    data = tifffile.imread(filename, series=1)
    decoded = imagecodecs.tiff_decode(encoded, index=[1, 3, 5, 7], asrgb=True)
    assert decoded.shape[-1] == 4
    assert_array_equal(data, decoded[..., :3])


@pytest.mark.skipif(tifffile is None, reason='tifffile module missing')
@pytest.mark.parametrize('byteorder', ['<', '>'])
@pytest.mark.parametrize('dtype', ['u1', 'u2', 'f2', 'f4'])
@pytest.mark.parametrize('predictor', [False, True])
@pytest.mark.parametrize(
    'codec',
    [
        'deflate',
        'lzw',
        'lzma',
        'zstd',
        'packbits',
        'webp',
        'jpeg',
        'lerc',
        'lerc_zstd',
        'lerc_deflate',
    ],
)
def test_tifffile(byteorder, dtype, codec, predictor):
    """Test tifffile compression."""
    compressionargs = None
    if codec == 'deflate' and not imagecodecs.ZLIB:
        # TODO: this should pass in tifffile >= 2020
        pytest.xfail('zlib missing')
    elif codec == 'lzma' and not imagecodecs.LZMA:
        pytest.xfail('lzma missing')
    elif codec == 'zstd' and not imagecodecs.ZSTD:
        pytest.xfail('zstd missing')
    elif codec == 'packbits' and not imagecodecs.PACKBITS:
        pytest.xfail('packbits missing')
    elif codec == 'jpeg':
        if not imagecodecs.JPEG:
            pytest.xfail('jpeg missing')
        if predictor or dtype != 'u1':
            pytest.xfail('tiff/jpeg do not support this case')
    elif codec == 'jpegxl':
        if not imagecodecs.JPEGXL:
            pytest.xfail('jpegxl missing')
        if predictor:
            pytest.xfail('jpegxl does not support predictor')
    elif codec[:4] == 'lerc':
        if not imagecodecs.LERC:
            pytest.xfail('lerc missing')
        elif dtype == 'f2' or byteorder == '>':
            pytest.xfail('dtype not supported by lerc')
        elif dtype == 'f4' and predictor:
            pytest.xfail('lerc does not work with float predictor')
        if codec == 'lerc_zstd':
            if not imagecodecs.ZSTD:
                pytest.xfail('zstd codec missing')
            compressionargs = {'compression': 'zstd'}
        elif codec == 'lerc_deflate':
            if not imagecodecs.ZLIB:
                pytest.xfail('zlib codec missing')
            compressionargs = {'compression': 'deflate'}
        codec = 'lerc'
    elif codec == 'webp':
        if not imagecodecs.WEBP:
            pytest.xfail('webp missing')
        elif dtype != 'u1':
            pytest.xfail('dtype not supported')
        elif predictor:
            pytest.xfail('webp does not support predictor')

    data = image_data('rgb', dtype)
    if byteorder == '>':
        data = data.byteswap().newbyteorder()

    with io.BytesIO() as fh:
        tifffile.imwrite(
            fh,
            data,
            photometric='rgb',
            compression=codec,
            compressionargs=compressionargs,
            predictor=predictor,
            byteorder=byteorder,
        )
        # with open(f'{codec}_{dtype}.tif', 'wb') as f:
        #     fh.seek(0)
        #     f.write(fh.read())
        fh.seek(0)
        with tifffile.TiffFile(fh) as tif:
            assert tif.byteorder == byteorder
            image = tif.asarray()
        if byteorder == '>':
            image = image.byteswap().newbyteorder()
        if codec != 'jpeg':
            assert_array_equal(data, image, verbose=True)

        if imagecodecs.TIFF:
            if not (predictor and codec in ('packbits', 'lerc')):
                # libtiff does not support {codec} with predictor
                fh.seek(0)
                image2 = imagecodecs.tiff_decode(fh.read())
                assert_array_equal(image2, image, verbose=True)


@pytest.mark.skipif(
    not imagecodecs.LJPEG or tifffile is None, reason='tifffile module missing'
)
@pytest.mark.parametrize('dtype', ['u1'])
def test_tifffile_ljpeg(dtype):
    """Test tifffile with ljpeg compression."""
    data = numpy.squeeze(image_data('gray', dtype))
    with io.BytesIO() as fh:
        tifffile.imwrite(
            fh,
            data,
            photometric='minisblack',
            compression=('jpeg', None, {'lossless': True, 'bitspersample': 8}),
        )
        fh.seek(0)
        image = tifffile.imread(fh)
    assert_array_equal(data, image, verbose=True)


@pytest.mark.skipif(czifile is None, reason='czifile missing')
def test_czifile():
    """Test JpegXR compressed CZI file."""
    fname = datafiles('jpegxr.czi')
    if not osp.exists(fname):
        pytest.skip('large file not included with source distribution')
    if not imagecodecs.JPEGXR:
        pytest.xfail('jpegxr missing')

    with czifile.CziFile(fname) as czi:
        assert czi.shape == (1, 1, 15, 404, 356, 1)
        assert czi.axes == 'BCZYX0'
        # verify data
        data = czi.asarray()
        assert data.flags['C_CONTIGUOUS']
        assert data.shape == (1, 1, 15, 404, 356, 1)
        assert data.dtype == 'uint16'
        assert data[0, 0, 14, 256, 146, 0] == 38086


@pytest.mark.skipif(SKIP_NUMCODECS, reason='numcodecs missing')
def test_numcodecs_register(caplog):
    """Test register_codecs function."""
    numcodecs.register_codecs(verbose=False)
    assert 'already registered' not in caplog.text
    numcodecs.register_codecs(force=True, verbose=False)
    assert 'already registered' not in caplog.text
    numcodecs.register_codecs()
    assert 'already registered' in caplog.text
    numcodecs.register_codecs(force=True)
    assert 'replacing registered numcodec' in caplog.text

    assert isinstance(
        numcodecs.get_codec({'id': 'imagecodecs_lzw'}), numcodecs.Lzw
    )


@pytest.mark.skipif(SKIP_NUMCODECS, reason='zarr or numcodecs missing')
@pytest.mark.parametrize('photometric', ['gray', 'rgb'])
@pytest.mark.parametrize(
    'codec',
    [
        'aec',
        'apng',
        'avif',
        'bitorder',
        'bitshuffle',
        'blosc',
        'blosc2',
        # 'brotli',  # failing
        'byteshuffle',
        'bz2',
        # 'cms',
        'deflate',
        'delta',
        'float24',
        'floatpred',
        'gif',
        'heif',
        # 'jetraw',  # encoder requires a license
        'jpeg',
        'jpeg12',
        'jpeg2k',
        'jpegls',
        'jpegxl',
        'jpegxr',
        'lerc',
        'ljpeg',
        'lz4',
        'lz4f',
        'lzf',
        'lzfse',
        'lzham',
        'lzma',
        'lzw',
        'packbits',
        'pglz',
        'png',
        'qoi',
        'rgbe',
        'rcomp',
        'snappy',
        'spng',
        'tiff',  # no encoder
        'webp',
        'xor',
        'zfp',
        'zlib',
        'zlibng',
        'zopfli',
        'zstd',
    ],
)
def test_numcodecs(codec, photometric):
    """Test numcodecs though roundtrips."""
    data = numpy.load(datafiles('rgb.u1.npy'))
    data = numpy.stack([data, data])
    if photometric == 'rgb':
        shape = data.shape
        chunks = (1, 128, 128, 3)
        axis = -2
    else:
        data = data[:, :, 1].copy()
        shape = data.shape
        chunks = (1, 128, 128)
        axis = -1

    lossless = True
    if codec == 'aec':
        if not imagecodecs.AEC:
            pytest.skip(f'{codec} not found')
        compressor = numcodecs.Aec(
            bitspersample=None, flags=None, blocksize=None, rsi=None
        )
    elif codec == 'apng':
        if not imagecodecs.APNG:
            pytest.skip(f'{codec} not found')
        compressor = numcodecs.Apng(photometric=photometric, delay=100)
    elif codec == 'avif':
        if not imagecodecs.AVIF:
            pytest.skip(f'{codec} not found')
        if photometric != 'rgb':
            pytest.xfail('AVIF does not support grayscale')
        compressor = numcodecs.Avif(
            level=0,
            speed=None,
            tilelog2=None,
            bitspersample=None,
            pixelformat=None,
            numthreads=2,
        )  # lossless
    elif codec == 'bitorder':
        if not imagecodecs.BITORDER:
            pytest.skip(f'{codec} not found')
        compressor = numcodecs.Bitorder()
    elif codec == 'bitshuffle':
        if not imagecodecs.BITSHUFFLE:
            pytest.skip(f'{codec} not found')
        compressor = numcodecs.Bitshuffle(
            itemsize=data.dtype.itemsize, blocksize=0
        )
    elif codec == 'blosc':
        if not imagecodecs.BLOSC:
            pytest.skip(f'{codec} not found')
        compressor = numcodecs.Blosc(
            level=9,
            compressor='blosclz',
            typesize=data.dtype.itemsize * 8,
            blocksize=None,
            shuffle=None,
            numthreads=2,
        )
    elif codec == 'blosc2':
        if not imagecodecs.BLOSC2:
            pytest.skip(f'{codec} not found')
        compressor = numcodecs.Blosc2(
            level=9,
            compressor='blosclz',
            typesize=data.dtype.itemsize * 8,
            blocksize=None,
            shuffle=None,
            numthreads=2,
        )
    elif codec == 'brotli':
        if not imagecodecs.BROTLI:
            pytest.skip(f'{codec} not found')
            # TODO: why are these failing?
        pytest.xfail('not sure why this is failing')
        compressor = numcodecs.Brotli(level=11, mode=None, lgwin=None)
    elif codec == 'byteshuffle':
        if not imagecodecs.BYTESHUFFLE:
            pytest.skip(f'{codec} not found')
        data = data.astype('int16')
        compressor = numcodecs.ByteShuffle(
            shape=chunks, dtype=data.dtype, axis=axis
        )
    elif codec == 'bz2':
        if not imagecodecs.BZ2:
            pytest.skip(f'{codec} not found')
        compressor = numcodecs.Bz2(level=9)
    elif codec == 'deflate':
        if not imagecodecs.DEFLATE:
            pytest.skip(f'{codec} not found')
        compressor = numcodecs.Deflate(level=8)
    elif codec == 'delta':
        if not imagecodecs.DELTA:
            pytest.skip(f'{codec} not found')
        compressor = numcodecs.Delta(shape=chunks, dtype=data.dtype, axis=axis)
    elif codec == 'float24':
        if not imagecodecs.FLOAT24:
            pytest.skip(f'{codec} not found')
        data = data.astype('float32')
        compressor = numcodecs.Float24()
    elif codec == 'floatpred':
        if not imagecodecs.FLOATPRED:
            pytest.skip(f'{codec} not found')
        data = data.astype('float32')
        compressor = numcodecs.FloatPred(
            shape=chunks, dtype=data.dtype, axis=axis
        )
    elif codec == 'gif':
        if not imagecodecs.GIF:
            pytest.skip(f'{codec} not found')
        compressor = numcodecs.Gif()
    elif codec == 'heif':
        if not imagecodecs.HEIF:
            pytest.skip(f'{codec} not found')
        compressor = numcodecs.Heif(photometric=photometric)
        lossless = False  # TODO: lossless not working
        atol = 1
    elif codec == 'jetraw':
        if not imagecodecs.JETRAW:
            pytest.skip(f'{codec} not found')
        if photometric == 'rgb':
            pytest.xfail('Jetraw does not support RGB')
        compressor = numcodecs.Jetraw(
            shape=chunks, identifier='500202_fast_bin1x'
        )
        data = data.astype('uint16')
        lossless = False
        atol = 32
    elif codec == 'jpeg':
        if not imagecodecs.JPEG:
            pytest.skip(f'{codec} not found')
        lossless = False
        atol = 4
        compressor = numcodecs.Jpeg(level=99)
    elif codec == 'jpeg12':
        if not imagecodecs.JPEG12:
            pytest.skip(f'{codec} not found')
        lossless = False
        atol = 4 << 4
        data = data.astype('uint16') << 4
        compressor = numcodecs.Jpeg(level=99, bitspersample=12)
    elif codec == 'jpeg2k':
        if not imagecodecs.JPEG2K:
            pytest.skip(f'{codec} not found')
        compressor = numcodecs.Jpeg2k(level=0)  # lossless
    elif codec == 'jpegls':
        if not imagecodecs.JPEGLS:
            pytest.skip(f'{codec} not found')
        compressor = numcodecs.JpegLs(level=0)  # lossless
    elif codec == 'jpegxl':
        if not imagecodecs.JPEGXL:
            pytest.skip(f'{codec} not found')
        compressor = numcodecs.JpegXl(level=101)  # lossless
    elif codec == 'jpegxr':
        if not imagecodecs.JPEGXR:
            pytest.skip(f'{codec} not found')
        compressor = numcodecs.JpegXr(
            level=1.0, photometric='RGB' if photometric == 'rgb' else None
        )  # lossless
    elif codec == 'lerc':
        if not imagecodecs.LERC:
            pytest.skip(f'{codec} not found')
        if imagecodecs.ZSTD:
            compression = 'zstd'
            compressionargs = {'level': 10}
        else:
            compression = None
            compressionargs = None
        compressor = numcodecs.Lerc(
            level=0.0, compression=compression, compressionargs=compressionargs
        )
    elif codec == 'ljpeg':
        if not imagecodecs.LJPEG:
            pytest.skip(f'{codec} not found')
        if photometric == 'rgb':
            pytest.xfail('LJPEG does not support rgb')
        data = data.astype('uint16') << 2
        compressor = numcodecs.Ljpeg(bitspersample=10)
    elif codec == 'lz4':
        if not imagecodecs.LZ4:
            pytest.skip(f'{codec} not found')
        compressor = numcodecs.Lz4(level=10, hc=True, header=True)
    elif codec == 'lz4f':
        if not imagecodecs.LZ4F:
            pytest.skip(f'{codec} not found')
        compressor = numcodecs.Lz4f(
            level=12,
            blocksizeid=False,
            contentchecksum=True,
            blockchecksum=True,
        )
    elif codec == 'lzf':
        if not imagecodecs.LZF:
            pytest.skip(f'{codec} not found')
        compressor = numcodecs.Lzf(header=True)
    elif codec == 'lzfse':
        if not imagecodecs.LZFSE:
            pytest.skip(f'{codec} not found')
        compressor = numcodecs.Lzfse()
    elif codec == 'lzham':
        if not imagecodecs.LZHAM:
            pytest.skip(f'{codec} not found')
        compressor = numcodecs.Lzham(level=6)
    elif codec == 'lzma':
        if not imagecodecs.LZMA:
            pytest.skip(f'{codec} not found')
        compressor = numcodecs.Lzma(
            level=6, check=imagecodecs.LZMA.CHECK.CRC32
        )
    elif codec == 'lzw':
        if not imagecodecs.LZW:
            pytest.skip(f'{codec} not found')
        compressor = numcodecs.Lzw()
    elif codec == 'packbits':
        if not imagecodecs.PACKBITS:
            pytest.skip(f'{codec} not found')
        if photometric == 'rgb':
            compressor = numcodecs.PackBits(axis=-2)
        else:
            compressor = numcodecs.PackBits()
    elif codec == 'pglz':
        if not imagecodecs.PGLZ:
            pytest.skip(f'{codec} not found')
        compressor = numcodecs.Pglz(strategy=None)
    elif codec == 'png':
        if not imagecodecs.PNG:
            pytest.skip(f'{codec} not found')
        compressor = numcodecs.Png()
    elif codec == 'qoi':
        if not imagecodecs.QOI:
            pytest.skip(f'{codec} not found')
        compressor = numcodecs.Qoi()
        if photometric != 'rgb':
            pytest.xfail('QOI does not support grayscale')
    elif codec == 'rgbe':
        if not imagecodecs.RGBE:
            pytest.skip(f'{codec} not found')
        if photometric != 'rgb':
            pytest.xfail('RGBE does not support grayscale')
        data = data.astype('float32')
        # lossless = False
        compressor = numcodecs.Rgbe(shape=chunks[-3:], header=False, rle=True)
    elif codec == 'rcomp':
        if not imagecodecs.RCOMP:
            pytest.skip(f'{codec} not found')
        compressor = numcodecs.Rcomp(shape=chunks, dtype=data.dtype)
    elif codec == 'snappy':
        if not imagecodecs.SNAPPY:
            pytest.skip(f'{codec} not found')
        compressor = numcodecs.Snappy()
    elif codec == 'spng':
        if not imagecodecs.SPNG:
            pytest.skip(f'{codec} not found')
        compressor = numcodecs.Spng()
    elif codec == 'tiff':
        if not imagecodecs.TIFF:
            pytest.skip(f'{codec} not found')
        pytest.xfail('TIFF encode not implemented')
        compressor = numcodecs.Tiff()
    elif codec == 'webp':
        if not imagecodecs.WEBP:
            pytest.skip(f'{codec} not found')
        if photometric != 'rgb':
            pytest.xfail('WebP does not support grayscale')
        compressor = numcodecs.Webp(level=-1)
    elif codec == 'xor':
        if not imagecodecs.XOR:
            pytest.skip(f'{codec} not found')
        compressor = numcodecs.Xor(shape=chunks, dtype=data.dtype, axis=axis)
    elif codec == 'zfp':
        if not imagecodecs.ZFP:
            pytest.skip(f'{codec} not found')
        data = data.astype('float32')
        compressor = numcodecs.Zfp(
            shape=chunks, dtype=data.dtype, header=False
        )
    elif codec == 'zlib':
        if not imagecodecs.ZLIB:
            pytest.skip(f'{codec} not found')
        compressor = numcodecs.Zlib(level=6)
    elif codec == 'zlibng':
        if not imagecodecs.ZLIBNG:
            pytest.skip(f'{codec} not found')
        compressor = numcodecs.Zlibng(level=6)
    elif codec == 'zopfli':
        if not imagecodecs.ZOPFLI:
            pytest.skip(f'{codec} not found')
        compressor = numcodecs.Zopfli()
    elif codec == 'zstd':
        if not imagecodecs.ZSTD:
            pytest.skip(f'{codec} not found')
        compressor = numcodecs.Zstd(level=10)
    else:
        raise RuntimeError()

    if 0:
        # use ZIP file on disk
        fname = f'test_{codec}.{photometric}.{data.dtype.str[1:]}.zarr.zip'
        store = zarr.ZipStore(fname, mode='w')
    else:
        store = zarr.MemoryStore()
    z = zarr.create(
        store=store,
        overwrite=True,
        shape=shape,
        chunks=chunks,
        dtype=data.dtype.str,
        compressor=compressor,
    )
    z[:] = data
    del z

    z = zarr.open(store, mode='r')
    if codec == 'jetraw':
        pass  # it does not make sense to test Jetraw on tiled, synthetic data
    elif lossless:
        assert_array_equal(z[:], data)
    else:
        assert_allclose(z[:, :150, :150], data[:, :150, :150], atol=atol)

    try:
        store.close()
    except Exception:
        pass


@pytest.mark.skipif(not imagecodecs.JPEG8, reason='jpeg8 missing')
@pytest.mark.skipif(IS_32BIT, reason='data too large for 32-bit')
def test_jpeg8_large():
    """Test JPEG 8-bit decoder with dimensions > 65000."""
    decode = imagecodecs.jpeg8_decode
    try:
        data = readfile('33792x79872.jpg', memmap=True)
    except OSError:
        pytest.skip('large file not included with source distribution')
    if not IS_WIN:
        pytest.xfail("libjpeg-turbo wasn't compiled with libjpeg-turbo.diff")
        # Jpeg8Error: Empty JPEG image (DNL not supported)

    assert imagecodecs.jpeg8_check(data)

    decoded = decode(data, shape=(33792, 79872))
    assert decoded.shape == (33792, 79872, 3)
    assert decoded.dtype == 'uint8'
    assert tuple(decoded[33791, 79871]) == (204, 195, 180)


###############################################################################


class TempFileName:
    """Temporary file name context manager."""

    def __init__(self, name=None, suffix='', remove=True):
        self.remove = bool(remove)
        if not name:
            with tempfile.NamedTemporaryFile(
                prefix='test_', suffix=suffix
            ) as temp:
                self.name = temp.name
        else:
            self.name = osp.join(tempfile.gettempdir(), f'test_{name}{suffix}')

    def __enter__(self):
        return self.name

    def __exit__(self, exc_type, exc_value, traceback):
        if self.remove:
            try:
                os.remove(self.name)
            except Exception:
                pass


def datafiles(pathname, base=None):
    """Return path to data file(s)."""
    if base is None:
        base = osp.dirname(__file__)
    path = osp.join(base, *pathname.split('/'))
    if any(i in path for i in '*?'):
        return glob.glob(path)
    return path


def readfile(fname, memmap=False):
    """Return content of data file."""
    with open(datafiles(fname), 'rb') as fh:
        if memmap:
            data = mmap.mmap(fh.fileno(), 0, access=mmap.ACCESS_READ)
        else:
            data = fh.read()
    return data


def image_data(itype, dtype, planar=False, frames=False):
    """Return test image array."""
    if frames:
        data = DATA
    else:
        data = DATA[0]

    if itype in ('rgb', 'view'):
        data = data[..., [0, 2, 4]]
    elif itype == 'rgba':
        data = data[..., [0, 2, 4, -1]]
    elif itype == 'cmyk':
        data = data[..., [0, 2, 4, 6]]
    elif itype == 'cmyka':
        data = data[..., [0, 2, 4, 6, -1]]
    elif itype == 'gray':
        data = data[..., 0:1]
    elif itype == 'graya':
        data = data[..., [0, -1]]
    elif itype == 'channels':
        data = data[..., :-1]
    elif itype == 'channelsa':
        data = data[..., :]
    elif itype == 'line':
        data = data[0:1, :, 0:1]
    elif itype == 'stack':
        # TODO: remove this
        assert not frames
        assert not planar
        data = numpy.moveaxis(data, -1, 0)
    else:
        raise ValueError('itype not found')

    if planar:
        data = numpy.moveaxis(data, -1, -3)

    data = data.copy()

    dtype = numpy.dtype(dtype)
    if dtype.char == '?':
        data = data > data.mean()
    elif dtype.kind in 'iu':
        iinfo = numpy.iinfo(dtype)
        if dtype.kind == 'u':
            data *= iinfo.max + 1
        else:
            data *= (iinfo.max - iinfo.max) / 2
            data -= 1.0 / 2.0
        data = numpy.rint(data)
        data = numpy.clip(data, iinfo.min, iinfo.max)
    elif dtype.kind != 'f':
        raise NotImplementedError('dtype not supported')

    data = data.astype(dtype)

    if dtype == 'uint16':
        # 12-bit
        data //= 16

    if itype == 'view':
        assert not frames
        assert not planar
        shape = data.shape
        temp = numpy.zeros((shape[0] + 5, shape[1] + 5, shape[2]), dtype)
        temp[2 : 2 + shape[0], 3 : 3 + shape[1], :] = data
        data = temp[2 : 2 + shape[0], 3 : 3 + shape[1], :]

    return data


DATA = numpy.load(datafiles('testdata.npy'))  # (32, 31, 9) float64
BYTES = readfile('bytes.bin')
BYTESIMG = numpy.frombuffer(BYTES, 'uint8').reshape(16, 16)
WORDS = readfile('words.bin')
WORDSIMG = numpy.frombuffer(WORDS, 'uint16').reshape(36, 36, 3)

if __name__ == '__main__':
    import warnings

    # warnings.simplefilter('always')  # noqa
    warnings.filterwarnings('ignore', category=ImportWarning)  # noqa
    argv = sys.argv
    argv.append('-vv')
    sys.exit(pytest.main(argv))
