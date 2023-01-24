import numba
import numpy as np
import pandas as pd
from numba.extending import overload
from bodo.utils.utils import alloc_arr_tup
MIN_MERGE = 32


@numba.njit(no_cpython_wrapper=True, cache=True)
def sort(key_arrs, lo, hi, data):
    omkf__wxlfj = hi - lo
    if omkf__wxlfj < 2:
        return
    if omkf__wxlfj < MIN_MERGE:
        csr__eipvg = countRunAndMakeAscending(key_arrs, lo, hi, data)
        binarySort(key_arrs, lo, hi, lo + csr__eipvg, data)
        return
    stackSize, runBase, runLen, tmpLength, tmp, tmp_data, minGallop = (
        init_sort_start(key_arrs, data))
    fcos__fft = minRunLength(omkf__wxlfj)
    while True:
        ehhg__rhyw = countRunAndMakeAscending(key_arrs, lo, hi, data)
        if ehhg__rhyw < fcos__fft:
            rasfx__imbr = (omkf__wxlfj if omkf__wxlfj <= fcos__fft else
                fcos__fft)
            binarySort(key_arrs, lo, lo + rasfx__imbr, lo + ehhg__rhyw, data)
            ehhg__rhyw = rasfx__imbr
        stackSize = pushRun(stackSize, runBase, runLen, lo, ehhg__rhyw)
        stackSize, tmpLength, tmp, tmp_data, minGallop = mergeCollapse(
            stackSize, runBase, runLen, key_arrs, data, tmpLength, tmp,
            tmp_data, minGallop)
        lo += ehhg__rhyw
        omkf__wxlfj -= ehhg__rhyw
        if omkf__wxlfj == 0:
            break
    assert lo == hi
    stackSize, tmpLength, tmp, tmp_data, minGallop = mergeForceCollapse(
        stackSize, runBase, runLen, key_arrs, data, tmpLength, tmp,
        tmp_data, minGallop)
    assert stackSize == 1


@numba.njit(no_cpython_wrapper=True, cache=True)
def binarySort(key_arrs, lo, hi, start, data):
    assert lo <= start and start <= hi
    if start == lo:
        start += 1
    while start < hi:
        smpjb__acv = getitem_arr_tup(key_arrs, start)
        isst__bmnu = getitem_arr_tup(data, start)
        onmth__zhcmw = lo
        owb__lbb = start
        assert onmth__zhcmw <= owb__lbb
        while onmth__zhcmw < owb__lbb:
            kmc__vwxa = onmth__zhcmw + owb__lbb >> 1
            if smpjb__acv < getitem_arr_tup(key_arrs, kmc__vwxa):
                owb__lbb = kmc__vwxa
            else:
                onmth__zhcmw = kmc__vwxa + 1
        assert onmth__zhcmw == owb__lbb
        n = start - onmth__zhcmw
        copyRange_tup(key_arrs, onmth__zhcmw, key_arrs, onmth__zhcmw + 1, n)
        copyRange_tup(data, onmth__zhcmw, data, onmth__zhcmw + 1, n)
        setitem_arr_tup(key_arrs, onmth__zhcmw, smpjb__acv)
        setitem_arr_tup(data, onmth__zhcmw, isst__bmnu)
        start += 1


@numba.njit(no_cpython_wrapper=True, cache=True)
def countRunAndMakeAscending(key_arrs, lo, hi, data):
    assert lo < hi
    rlqp__wdcau = lo + 1
    if rlqp__wdcau == hi:
        return 1
    if getitem_arr_tup(key_arrs, rlqp__wdcau) < getitem_arr_tup(key_arrs, lo):
        rlqp__wdcau += 1
        while rlqp__wdcau < hi and getitem_arr_tup(key_arrs, rlqp__wdcau
            ) < getitem_arr_tup(key_arrs, rlqp__wdcau - 1):
            rlqp__wdcau += 1
        reverseRange(key_arrs, lo, rlqp__wdcau, data)
    else:
        rlqp__wdcau += 1
        while rlqp__wdcau < hi and getitem_arr_tup(key_arrs, rlqp__wdcau
            ) >= getitem_arr_tup(key_arrs, rlqp__wdcau - 1):
            rlqp__wdcau += 1
    return rlqp__wdcau - lo


@numba.njit(no_cpython_wrapper=True, cache=True)
def reverseRange(key_arrs, lo, hi, data):
    hi -= 1
    while lo < hi:
        swap_arrs(key_arrs, lo, hi)
        swap_arrs(data, lo, hi)
        lo += 1
        hi -= 1


@numba.njit(no_cpython_wrapper=True, cache=True)
def minRunLength(n):
    assert n >= 0
    pcs__lfzkq = 0
    while n >= MIN_MERGE:
        pcs__lfzkq |= n & 1
        n >>= 1
    return n + pcs__lfzkq


MIN_GALLOP = 7
INITIAL_TMP_STORAGE_LENGTH = 256


@numba.njit(no_cpython_wrapper=True, cache=True)
def init_sort_start(key_arrs, data):
    minGallop = MIN_GALLOP
    gligv__elnfv = len(key_arrs[0])
    tmpLength = (gligv__elnfv >> 1 if gligv__elnfv < 2 *
        INITIAL_TMP_STORAGE_LENGTH else INITIAL_TMP_STORAGE_LENGTH)
    tmp = alloc_arr_tup(tmpLength, key_arrs)
    tmp_data = alloc_arr_tup(tmpLength, data)
    stackSize = 0
    ram__gpxh = (5 if gligv__elnfv < 120 else 10 if gligv__elnfv < 1542 else
        19 if gligv__elnfv < 119151 else 40)
    runBase = np.empty(ram__gpxh, np.int64)
    runLen = np.empty(ram__gpxh, np.int64)
    return stackSize, runBase, runLen, tmpLength, tmp, tmp_data, minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def pushRun(stackSize, runBase, runLen, runBase_val, runLen_val):
    runBase[stackSize] = runBase_val
    runLen[stackSize] = runLen_val
    stackSize += 1
    return stackSize


@numba.njit(no_cpython_wrapper=True, cache=True)
def mergeCollapse(stackSize, runBase, runLen, key_arrs, data, tmpLength,
    tmp, tmp_data, minGallop):
    while stackSize > 1:
        n = stackSize - 2
        if n >= 1 and runLen[n - 1] <= runLen[n] + runLen[n + 1
            ] or n >= 2 and runLen[n - 2] <= runLen[n] + runLen[n - 1]:
            if runLen[n - 1] < runLen[n + 1]:
                n -= 1
        elif runLen[n] > runLen[n + 1]:
            break
        stackSize, tmpLength, tmp, tmp_data, minGallop = mergeAt(stackSize,
            runBase, runLen, key_arrs, data, tmpLength, tmp, tmp_data,
            minGallop, n)
    return stackSize, tmpLength, tmp, tmp_data, minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def mergeForceCollapse(stackSize, runBase, runLen, key_arrs, data,
    tmpLength, tmp, tmp_data, minGallop):
    while stackSize > 1:
        n = stackSize - 2
        if n > 0 and runLen[n - 1] < runLen[n + 1]:
            n -= 1
        stackSize, tmpLength, tmp, tmp_data, minGallop = mergeAt(stackSize,
            runBase, runLen, key_arrs, data, tmpLength, tmp, tmp_data,
            minGallop, n)
    return stackSize, tmpLength, tmp, tmp_data, minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def mergeAt(stackSize, runBase, runLen, key_arrs, data, tmpLength, tmp,
    tmp_data, minGallop, i):
    assert stackSize >= 2
    assert i >= 0
    assert i == stackSize - 2 or i == stackSize - 3
    base1 = runBase[i]
    len1 = runLen[i]
    base2 = runBase[i + 1]
    len2 = runLen[i + 1]
    assert len1 > 0 and len2 > 0
    assert base1 + len1 == base2
    runLen[i] = len1 + len2
    if i == stackSize - 3:
        runBase[i + 1] = runBase[i + 2]
        runLen[i + 1] = runLen[i + 2]
    stackSize -= 1
    jof__yxt = gallopRight(getitem_arr_tup(key_arrs, base2), key_arrs,
        base1, len1, 0)
    assert jof__yxt >= 0
    base1 += jof__yxt
    len1 -= jof__yxt
    if len1 == 0:
        return stackSize, tmpLength, tmp, tmp_data, minGallop
    len2 = gallopLeft(getitem_arr_tup(key_arrs, base1 + len1 - 1), key_arrs,
        base2, len2, len2 - 1)
    assert len2 >= 0
    if len2 == 0:
        return stackSize, tmpLength, tmp, tmp_data, minGallop
    if len1 <= len2:
        tmpLength, tmp, tmp_data = ensureCapacity(tmpLength, tmp, tmp_data,
            key_arrs, data, len1)
        minGallop = mergeLo(key_arrs, data, tmp, tmp_data, minGallop, base1,
            len1, base2, len2)
    else:
        tmpLength, tmp, tmp_data = ensureCapacity(tmpLength, tmp, tmp_data,
            key_arrs, data, len2)
        minGallop = mergeHi(key_arrs, data, tmp, tmp_data, minGallop, base1,
            len1, base2, len2)
    return stackSize, tmpLength, tmp, tmp_data, minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def gallopLeft(key, arr, base, _len, hint):
    assert _len > 0 and hint >= 0 and hint < _len
    wpgti__qqppd = 0
    ujzz__cbxyd = 1
    if key > getitem_arr_tup(arr, base + hint):
        toyrm__awoc = _len - hint
        while ujzz__cbxyd < toyrm__awoc and key > getitem_arr_tup(arr, base +
            hint + ujzz__cbxyd):
            wpgti__qqppd = ujzz__cbxyd
            ujzz__cbxyd = (ujzz__cbxyd << 1) + 1
            if ujzz__cbxyd <= 0:
                ujzz__cbxyd = toyrm__awoc
        if ujzz__cbxyd > toyrm__awoc:
            ujzz__cbxyd = toyrm__awoc
        wpgti__qqppd += hint
        ujzz__cbxyd += hint
    else:
        toyrm__awoc = hint + 1
        while ujzz__cbxyd < toyrm__awoc and key <= getitem_arr_tup(arr, 
            base + hint - ujzz__cbxyd):
            wpgti__qqppd = ujzz__cbxyd
            ujzz__cbxyd = (ujzz__cbxyd << 1) + 1
            if ujzz__cbxyd <= 0:
                ujzz__cbxyd = toyrm__awoc
        if ujzz__cbxyd > toyrm__awoc:
            ujzz__cbxyd = toyrm__awoc
        tmp = wpgti__qqppd
        wpgti__qqppd = hint - ujzz__cbxyd
        ujzz__cbxyd = hint - tmp
    assert -1 <= wpgti__qqppd and wpgti__qqppd < ujzz__cbxyd and ujzz__cbxyd <= _len
    wpgti__qqppd += 1
    while wpgti__qqppd < ujzz__cbxyd:
        lev__ykazb = wpgti__qqppd + (ujzz__cbxyd - wpgti__qqppd >> 1)
        if key > getitem_arr_tup(arr, base + lev__ykazb):
            wpgti__qqppd = lev__ykazb + 1
        else:
            ujzz__cbxyd = lev__ykazb
    assert wpgti__qqppd == ujzz__cbxyd
    return ujzz__cbxyd


@numba.njit(no_cpython_wrapper=True, cache=True)
def gallopRight(key, arr, base, _len, hint):
    assert _len > 0 and hint >= 0 and hint < _len
    ujzz__cbxyd = 1
    wpgti__qqppd = 0
    if key < getitem_arr_tup(arr, base + hint):
        toyrm__awoc = hint + 1
        while ujzz__cbxyd < toyrm__awoc and key < getitem_arr_tup(arr, base +
            hint - ujzz__cbxyd):
            wpgti__qqppd = ujzz__cbxyd
            ujzz__cbxyd = (ujzz__cbxyd << 1) + 1
            if ujzz__cbxyd <= 0:
                ujzz__cbxyd = toyrm__awoc
        if ujzz__cbxyd > toyrm__awoc:
            ujzz__cbxyd = toyrm__awoc
        tmp = wpgti__qqppd
        wpgti__qqppd = hint - ujzz__cbxyd
        ujzz__cbxyd = hint - tmp
    else:
        toyrm__awoc = _len - hint
        while ujzz__cbxyd < toyrm__awoc and key >= getitem_arr_tup(arr, 
            base + hint + ujzz__cbxyd):
            wpgti__qqppd = ujzz__cbxyd
            ujzz__cbxyd = (ujzz__cbxyd << 1) + 1
            if ujzz__cbxyd <= 0:
                ujzz__cbxyd = toyrm__awoc
        if ujzz__cbxyd > toyrm__awoc:
            ujzz__cbxyd = toyrm__awoc
        wpgti__qqppd += hint
        ujzz__cbxyd += hint
    assert -1 <= wpgti__qqppd and wpgti__qqppd < ujzz__cbxyd and ujzz__cbxyd <= _len
    wpgti__qqppd += 1
    while wpgti__qqppd < ujzz__cbxyd:
        lev__ykazb = wpgti__qqppd + (ujzz__cbxyd - wpgti__qqppd >> 1)
        if key < getitem_arr_tup(arr, base + lev__ykazb):
            ujzz__cbxyd = lev__ykazb
        else:
            wpgti__qqppd = lev__ykazb + 1
    assert wpgti__qqppd == ujzz__cbxyd
    return ujzz__cbxyd


@numba.njit(no_cpython_wrapper=True, cache=True)
def mergeLo(key_arrs, data, tmp, tmp_data, minGallop, base1, len1, base2, len2
    ):
    assert len1 > 0 and len2 > 0 and base1 + len1 == base2
    arr = key_arrs
    arr_data = data
    copyRange_tup(arr, base1, tmp, 0, len1)
    copyRange_tup(arr_data, base1, tmp_data, 0, len1)
    cursor1 = 0
    cursor2 = base2
    dest = base1
    setitem_arr_tup(arr, dest, getitem_arr_tup(arr, cursor2))
    copyElement_tup(arr_data, cursor2, arr_data, dest)
    cursor2 += 1
    dest += 1
    len2 -= 1
    if len2 == 0:
        copyRange_tup(tmp, cursor1, arr, dest, len1)
        copyRange_tup(tmp_data, cursor1, arr_data, dest, len1)
        return minGallop
    if len1 == 1:
        copyRange_tup(arr, cursor2, arr, dest, len2)
        copyRange_tup(arr_data, cursor2, arr_data, dest, len2)
        copyElement_tup(tmp, cursor1, arr, dest + len2)
        copyElement_tup(tmp_data, cursor1, arr_data, dest + len2)
        return minGallop
    len1, len2, cursor1, cursor2, dest, minGallop = mergeLo_inner(key_arrs,
        data, tmp_data, len1, len2, tmp, cursor1, cursor2, dest, minGallop)
    minGallop = 1 if minGallop < 1 else minGallop
    if len1 == 1:
        assert len2 > 0
        copyRange_tup(arr, cursor2, arr, dest, len2)
        copyRange_tup(arr_data, cursor2, arr_data, dest, len2)
        copyElement_tup(tmp, cursor1, arr, dest + len2)
        copyElement_tup(tmp_data, cursor1, arr_data, dest + len2)
    elif len1 == 0:
        raise ValueError('Comparison method violates its general contract!')
    else:
        assert len2 == 0
        assert len1 > 1
        copyRange_tup(tmp, cursor1, arr, dest, len1)
        copyRange_tup(tmp_data, cursor1, arr_data, dest, len1)
    return minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def mergeLo_inner(arr, arr_data, tmp_data, len1, len2, tmp, cursor1,
    cursor2, dest, minGallop):
    while True:
        qgrk__wvetr = 0
        hcj__atyn = 0
        while True:
            assert len1 > 1 and len2 > 0
            if getitem_arr_tup(arr, cursor2) < getitem_arr_tup(tmp, cursor1):
                copyElement_tup(arr, cursor2, arr, dest)
                copyElement_tup(arr_data, cursor2, arr_data, dest)
                cursor2 += 1
                dest += 1
                hcj__atyn += 1
                qgrk__wvetr = 0
                len2 -= 1
                if len2 == 0:
                    return len1, len2, cursor1, cursor2, dest, minGallop
            else:
                copyElement_tup(tmp, cursor1, arr, dest)
                copyElement_tup(tmp_data, cursor1, arr_data, dest)
                cursor1 += 1
                dest += 1
                qgrk__wvetr += 1
                hcj__atyn = 0
                len1 -= 1
                if len1 == 1:
                    return len1, len2, cursor1, cursor2, dest, minGallop
            if not qgrk__wvetr | hcj__atyn < minGallop:
                break
        while True:
            assert len1 > 1 and len2 > 0
            qgrk__wvetr = gallopRight(getitem_arr_tup(arr, cursor2), tmp,
                cursor1, len1, 0)
            if qgrk__wvetr != 0:
                copyRange_tup(tmp, cursor1, arr, dest, qgrk__wvetr)
                copyRange_tup(tmp_data, cursor1, arr_data, dest, qgrk__wvetr)
                dest += qgrk__wvetr
                cursor1 += qgrk__wvetr
                len1 -= qgrk__wvetr
                if len1 <= 1:
                    return len1, len2, cursor1, cursor2, dest, minGallop
            copyElement_tup(arr, cursor2, arr, dest)
            copyElement_tup(arr_data, cursor2, arr_data, dest)
            cursor2 += 1
            dest += 1
            len2 -= 1
            if len2 == 0:
                return len1, len2, cursor1, cursor2, dest, minGallop
            hcj__atyn = gallopLeft(getitem_arr_tup(tmp, cursor1), arr,
                cursor2, len2, 0)
            if hcj__atyn != 0:
                copyRange_tup(arr, cursor2, arr, dest, hcj__atyn)
                copyRange_tup(arr_data, cursor2, arr_data, dest, hcj__atyn)
                dest += hcj__atyn
                cursor2 += hcj__atyn
                len2 -= hcj__atyn
                if len2 == 0:
                    return len1, len2, cursor1, cursor2, dest, minGallop
            copyElement_tup(tmp, cursor1, arr, dest)
            copyElement_tup(tmp_data, cursor1, arr_data, dest)
            cursor1 += 1
            dest += 1
            len1 -= 1
            if len1 == 1:
                return len1, len2, cursor1, cursor2, dest, minGallop
            minGallop -= 1
            if not qgrk__wvetr >= MIN_GALLOP | hcj__atyn >= MIN_GALLOP:
                break
        if minGallop < 0:
            minGallop = 0
        minGallop += 2
    return len1, len2, cursor1, cursor2, dest, minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def mergeHi(key_arrs, data, tmp, tmp_data, minGallop, base1, len1, base2, len2
    ):
    assert len1 > 0 and len2 > 0 and base1 + len1 == base2
    arr = key_arrs
    arr_data = data
    copyRange_tup(arr, base2, tmp, 0, len2)
    copyRange_tup(arr_data, base2, tmp_data, 0, len2)
    cursor1 = base1 + len1 - 1
    cursor2 = len2 - 1
    dest = base2 + len2 - 1
    copyElement_tup(arr, cursor1, arr, dest)
    copyElement_tup(arr_data, cursor1, arr_data, dest)
    cursor1 -= 1
    dest -= 1
    len1 -= 1
    if len1 == 0:
        copyRange_tup(tmp, 0, arr, dest - (len2 - 1), len2)
        copyRange_tup(tmp_data, 0, arr_data, dest - (len2 - 1), len2)
        return minGallop
    if len2 == 1:
        dest -= len1
        cursor1 -= len1
        copyRange_tup(arr, cursor1 + 1, arr, dest + 1, len1)
        copyRange_tup(arr_data, cursor1 + 1, arr_data, dest + 1, len1)
        copyElement_tup(tmp, cursor2, arr, dest)
        copyElement_tup(tmp_data, cursor2, arr_data, dest)
        return minGallop
    len1, len2, tmp, cursor1, cursor2, dest, minGallop = mergeHi_inner(key_arrs
        , data, tmp_data, base1, len1, len2, tmp, cursor1, cursor2, dest,
        minGallop)
    minGallop = 1 if minGallop < 1 else minGallop
    if len2 == 1:
        assert len1 > 0
        dest -= len1
        cursor1 -= len1
        copyRange_tup(arr, cursor1 + 1, arr, dest + 1, len1)
        copyRange_tup(arr_data, cursor1 + 1, arr_data, dest + 1, len1)
        copyElement_tup(tmp, cursor2, arr, dest)
        copyElement_tup(tmp_data, cursor2, arr_data, dest)
    elif len2 == 0:
        raise ValueError('Comparison method violates its general contract!')
    else:
        assert len1 == 0
        assert len2 > 0
        copyRange_tup(tmp, 0, arr, dest - (len2 - 1), len2)
        copyRange_tup(tmp_data, 0, arr_data, dest - (len2 - 1), len2)
    return minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def mergeHi_inner(arr, arr_data, tmp_data, base1, len1, len2, tmp, cursor1,
    cursor2, dest, minGallop):
    while True:
        qgrk__wvetr = 0
        hcj__atyn = 0
        while True:
            assert len1 > 0 and len2 > 1
            if getitem_arr_tup(tmp, cursor2) < getitem_arr_tup(arr, cursor1):
                copyElement_tup(arr, cursor1, arr, dest)
                copyElement_tup(arr_data, cursor1, arr_data, dest)
                cursor1 -= 1
                dest -= 1
                qgrk__wvetr += 1
                hcj__atyn = 0
                len1 -= 1
                if len1 == 0:
                    return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            else:
                copyElement_tup(tmp, cursor2, arr, dest)
                copyElement_tup(tmp_data, cursor2, arr_data, dest)
                cursor2 -= 1
                dest -= 1
                hcj__atyn += 1
                qgrk__wvetr = 0
                len2 -= 1
                if len2 == 1:
                    return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            if not qgrk__wvetr | hcj__atyn < minGallop:
                break
        while True:
            assert len1 > 0 and len2 > 1
            qgrk__wvetr = len1 - gallopRight(getitem_arr_tup(tmp, cursor2),
                arr, base1, len1, len1 - 1)
            if qgrk__wvetr != 0:
                dest -= qgrk__wvetr
                cursor1 -= qgrk__wvetr
                len1 -= qgrk__wvetr
                copyRange_tup(arr, cursor1 + 1, arr, dest + 1, qgrk__wvetr)
                copyRange_tup(arr_data, cursor1 + 1, arr_data, dest + 1,
                    qgrk__wvetr)
                if len1 == 0:
                    return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            copyElement_tup(tmp, cursor2, arr, dest)
            copyElement_tup(tmp_data, cursor2, arr_data, dest)
            cursor2 -= 1
            dest -= 1
            len2 -= 1
            if len2 == 1:
                return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            hcj__atyn = len2 - gallopLeft(getitem_arr_tup(arr, cursor1),
                tmp, 0, len2, len2 - 1)
            if hcj__atyn != 0:
                dest -= hcj__atyn
                cursor2 -= hcj__atyn
                len2 -= hcj__atyn
                copyRange_tup(tmp, cursor2 + 1, arr, dest + 1, hcj__atyn)
                copyRange_tup(tmp_data, cursor2 + 1, arr_data, dest + 1,
                    hcj__atyn)
                if len2 <= 1:
                    return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            copyElement_tup(arr, cursor1, arr, dest)
            copyElement_tup(arr_data, cursor1, arr_data, dest)
            cursor1 -= 1
            dest -= 1
            len1 -= 1
            if len1 == 0:
                return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            minGallop -= 1
            if not qgrk__wvetr >= MIN_GALLOP | hcj__atyn >= MIN_GALLOP:
                break
        if minGallop < 0:
            minGallop = 0
        minGallop += 2
    return len1, len2, tmp, cursor1, cursor2, dest, minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def ensureCapacity(tmpLength, tmp, tmp_data, key_arrs, data, minCapacity):
    xmqb__vackf = len(key_arrs[0])
    if tmpLength < minCapacity:
        yjnf__nne = minCapacity
        yjnf__nne |= yjnf__nne >> 1
        yjnf__nne |= yjnf__nne >> 2
        yjnf__nne |= yjnf__nne >> 4
        yjnf__nne |= yjnf__nne >> 8
        yjnf__nne |= yjnf__nne >> 16
        yjnf__nne += 1
        if yjnf__nne < 0:
            yjnf__nne = minCapacity
        else:
            yjnf__nne = min(yjnf__nne, xmqb__vackf >> 1)
        tmp = alloc_arr_tup(yjnf__nne, key_arrs)
        tmp_data = alloc_arr_tup(yjnf__nne, data)
        tmpLength = yjnf__nne
    return tmpLength, tmp, tmp_data


def swap_arrs(data, lo, hi):
    for arr in data:
        txdy__awwqp = arr[lo]
        arr[lo] = arr[hi]
        arr[hi] = txdy__awwqp


@overload(swap_arrs, no_unliteral=True)
def swap_arrs_overload(arr_tup, lo, hi):
    johay__huer = arr_tup.count
    buo__kuj = 'def f(arr_tup, lo, hi):\n'
    for i in range(johay__huer):
        buo__kuj += '  tmp_v_{} = arr_tup[{}][lo]\n'.format(i, i)
        buo__kuj += '  arr_tup[{}][lo] = arr_tup[{}][hi]\n'.format(i, i)
        buo__kuj += '  arr_tup[{}][hi] = tmp_v_{}\n'.format(i, i)
    buo__kuj += '  return\n'
    kvo__wuixw = {}
    exec(buo__kuj, {}, kvo__wuixw)
    fyu__eoxc = kvo__wuixw['f']
    return fyu__eoxc


@numba.njit(no_cpython_wrapper=True, cache=True)
def copyRange(src_arr, src_pos, dst_arr, dst_pos, n):
    dst_arr[dst_pos:dst_pos + n] = src_arr[src_pos:src_pos + n]


def copyRange_tup(src_arr_tup, src_pos, dst_arr_tup, dst_pos, n):
    for src_arr, dst_arr in zip(src_arr_tup, dst_arr_tup):
        dst_arr[dst_pos:dst_pos + n] = src_arr[src_pos:src_pos + n]


@overload(copyRange_tup, no_unliteral=True)
def copyRange_tup_overload(src_arr_tup, src_pos, dst_arr_tup, dst_pos, n):
    johay__huer = src_arr_tup.count
    assert johay__huer == dst_arr_tup.count
    buo__kuj = 'def f(src_arr_tup, src_pos, dst_arr_tup, dst_pos, n):\n'
    for i in range(johay__huer):
        buo__kuj += (
            '  copyRange(src_arr_tup[{}], src_pos, dst_arr_tup[{}], dst_pos, n)\n'
            .format(i, i))
    buo__kuj += '  return\n'
    kvo__wuixw = {}
    exec(buo__kuj, {'copyRange': copyRange}, kvo__wuixw)
    hhgcc__wzjak = kvo__wuixw['f']
    return hhgcc__wzjak


@numba.njit(no_cpython_wrapper=True, cache=True)
def copyElement(src_arr, src_pos, dst_arr, dst_pos):
    dst_arr[dst_pos] = src_arr[src_pos]


def copyElement_tup(src_arr_tup, src_pos, dst_arr_tup, dst_pos):
    for src_arr, dst_arr in zip(src_arr_tup, dst_arr_tup):
        dst_arr[dst_pos] = src_arr[src_pos]


@overload(copyElement_tup, no_unliteral=True)
def copyElement_tup_overload(src_arr_tup, src_pos, dst_arr_tup, dst_pos):
    johay__huer = src_arr_tup.count
    assert johay__huer == dst_arr_tup.count
    buo__kuj = 'def f(src_arr_tup, src_pos, dst_arr_tup, dst_pos):\n'
    for i in range(johay__huer):
        buo__kuj += (
            '  copyElement(src_arr_tup[{}], src_pos, dst_arr_tup[{}], dst_pos)\n'
            .format(i, i))
    buo__kuj += '  return\n'
    kvo__wuixw = {}
    exec(buo__kuj, {'copyElement': copyElement}, kvo__wuixw)
    hhgcc__wzjak = kvo__wuixw['f']
    return hhgcc__wzjak


def getitem_arr_tup(arr_tup, ind):
    ohlwf__ndaq = [arr[ind] for arr in arr_tup]
    return tuple(ohlwf__ndaq)


@overload(getitem_arr_tup, no_unliteral=True)
def getitem_arr_tup_overload(arr_tup, ind):
    johay__huer = arr_tup.count
    buo__kuj = 'def f(arr_tup, ind):\n'
    buo__kuj += '  return ({}{})\n'.format(','.join(['arr_tup[{}][ind]'.
        format(i) for i in range(johay__huer)]), ',' if johay__huer == 1 else
        '')
    kvo__wuixw = {}
    exec(buo__kuj, {}, kvo__wuixw)
    rrzcj__gtw = kvo__wuixw['f']
    return rrzcj__gtw


def setitem_arr_tup(arr_tup, ind, val_tup):
    for arr, xnsi__xrmah in zip(arr_tup, val_tup):
        arr[ind] = xnsi__xrmah


@overload(setitem_arr_tup, no_unliteral=True)
def setitem_arr_tup_overload(arr_tup, ind, val_tup):
    johay__huer = arr_tup.count
    buo__kuj = 'def f(arr_tup, ind, val_tup):\n'
    for i in range(johay__huer):
        if isinstance(val_tup, numba.core.types.BaseTuple):
            buo__kuj += '  arr_tup[{}][ind] = val_tup[{}]\n'.format(i, i)
        else:
            assert arr_tup.count == 1
            buo__kuj += '  arr_tup[{}][ind] = val_tup\n'.format(i)
    buo__kuj += '  return\n'
    kvo__wuixw = {}
    exec(buo__kuj, {}, kvo__wuixw)
    rrzcj__gtw = kvo__wuixw['f']
    return rrzcj__gtw


def test():
    import time
    qqjg__jxb = time.time()
    swx__nbg = np.ones(3)
    data = np.arange(3), np.ones(3)
    sort((swx__nbg,), 0, 3, data)
    print('compile time', time.time() - qqjg__jxb)
    n = 210000
    np.random.seed(2)
    data = np.arange(n), np.random.ranf(n)
    rhm__hiz = np.random.ranf(n)
    jnrc__atoq = pd.DataFrame({'A': rhm__hiz, 'B': data[0], 'C': data[1]})
    qqjg__jxb = time.time()
    sigt__romxi = jnrc__atoq.sort_values('A', inplace=False)
    zympy__vmqv = time.time()
    sort((rhm__hiz,), 0, n, data)
    print('Bodo', time.time() - zympy__vmqv, 'Numpy', zympy__vmqv - qqjg__jxb)
    np.testing.assert_almost_equal(data[0], sigt__romxi.B.values)
    np.testing.assert_almost_equal(data[1], sigt__romxi.C.values)


if __name__ == '__main__':
    test()
