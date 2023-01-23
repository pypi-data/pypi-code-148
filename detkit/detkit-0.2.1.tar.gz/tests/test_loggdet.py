#! /usr/bin/env python

# SPDX-FileCopyrightText: Copyright 2022, Siavash Ameli <sameli@berkeley.edu>
# SPDX-License-Identifier: BSD-3-Clause
# SPDX-FileType: SOURCE
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the license found in the LICENSE.txt file in the root directory
# of this source tree.


# =======
# Imports
# =======

import numpy
import numpy.linalg
from detkit import loggdet, orthogonalize, ortho_complement


# ============
# test loggdet
# ============

def test_loggdet():
    """
    Test for `loggdet` function.
    """

    def pr(A, pr=5):
        print(numpy.around(A, pr))

    # n = 100
    n = 10
    m = 5
    A = numpy.random.rand(n, n)
    X = numpy.random.rand(n, m)

    # Make A a PSD matrix, and make X orthogonal
    A = A.T @ A

    sym_pos = False
    X_orth = True

    if X_orth:
        orthogonalize(X)

    # Pre-compute Xp, the orthonormal complement of X
    Xp = numpy.random.randn(n, n-m)
    ortho_complement(Xp, X, X_orth)

    C = X.T @ numpy.linalg.inv(A) @ X
    sign_00, logdet_00 = numpy.linalg.slogdet(A)
    sign_01, logdet_01 = numpy.linalg.slogdet(C)
    sign_0 = sign_00
    logdet_0 = logdet_00 + logdet_01

    XtX = X.T @ X
    XtXinv = numpy.linalg.inv(XtX)
    P = X @ XtXinv @ X.T
    N = A + P - A @ P
    logdet_7 = numpy.linalg.slogdet(XtX)[1] + numpy.linalg.slogdet(N)[1]
    print('%16.8f' % logdet_7)

    # Using C++
    logdet_1, sign_1, flops_1 = loggdet(A, X, method='legacy', sym_pos=sym_pos,
                                        X_orth=False, flops=True)
    logdet_2, sign_2, flops_2 = loggdet(A, X, method='proj', sym_pos=True,
                                        X_orth=X_orth, flops=True)
    logdet_31, sign_31, flops_31 = loggdet(A, X, Xp=None, method='comp',
                                           sym_pos=sym_pos, X_orth=X_orth,
                                           flops=True)
    logdet_32, sign_32, flops_32 = loggdet(A, X, Xp=Xp, method='comp',
                                           sym_pos=sym_pos, X_orth=X_orth,
                                           flops=True)

    # Using scipy
    logdet_4, sign_4 = loggdet(A, X, method='legacy', sym_pos=sym_pos,
                               X_orth=False, use_scipy=True)
    logdet_5, sign_5 = loggdet(A, X, method='proj', sym_pos=True,
                               X_orth=X_orth, use_scipy=True)
    logdet_6, sign_6 = loggdet(A, X, Xp=Xp, method='comp', sym_pos=sym_pos,
                               X_orth=X_orth, use_scipy=True)

    print('%16.8f, %+d' % (logdet_0, sign_0))
    print('%16.8f, %+d, %ld' % (logdet_1, sign_1, flops_1))
    print('%16.8f, %+d, %ld' % (logdet_2, sign_2, flops_2))
    print('%16.8f, %+d, %ld' % (logdet_31, sign_31, flops_31))
    print('%16.8f, %+d, %ld' % (logdet_32, sign_32, flops_32))
    print('%16.8f, %+d' % (logdet_4, sign_4))
    print('%16.8f, %+d' % (logdet_5, sign_5))
    print('%16.8f, %+d' % (logdet_6, sign_6))


# ===========
# Script main
# ===========

if __name__ == "__main__":
    test_loggdet()
