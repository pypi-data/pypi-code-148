from scipy.linalg.lapack import get_lapack_funcs, _compute_lwork
from scipy._lib._util import _asarray_validated
from numpy.linalg import LinAlgError
from numpy import iscomplexobj
import numpy as np 

# SS: Debugging scipy.eigh 

# from scipy.linalg._misc import _datacopied
def _datacopied(arr, original):
    """
        Strict check for `arr` not sharing any data with `original`,
        under the assumption that arr = asarray(original)
    """
    if arr is original:
        return False
    if not isinstance(original, np.ndarray) and hasattr(original, '__array__'):
        return False
    return arr.base is None


def eigh(a, b=None, lower=True, eigvals_only=False, overwrite_a=False,
         overwrite_b=False, turbo=True, eigvals=None, type=1,
         check_finite=True, subset_by_index=None, subset_by_value=None,
         driver=None):
    """
    Solve a standard or generalized eigenvalue problem for a complex
    Hermitian or real symmetric matrix.
    Find eigenvalues array ``w`` and optionally eigenvectors array ``v`` of
    array ``a``, where ``b`` is positive definite such that for every
    eigenvalue λ (i-th entry of w) and its eigenvector ``vi`` (i-th column of
    ``v``) satisfies::
                      a @ vi = λ * b @ vi
        vi.conj().T @ a @ vi = λ
        vi.conj().T @ b @ vi = 1
    In the standard problem, ``b`` is assumed to be the identity matrix.
    Parameters
    ----------
    a : (M, M) array_like
        A complex Hermitian or real symmetric matrix whose eigenvalues and
        eigenvectors will be computed.
    b : (M, M) array_like, optional
        A complex Hermitian or real symmetric definite positive matrix in.
        If omitted, identity matrix is assumed.
    lower : bool, optional
        Whether the pertinent array data is taken from the lower or upper
        triangle of ``a`` and, if applicable, ``b``. (Default: lower)
    eigvals_only : bool, optional
        Whether to calculate only eigenvalues and no eigenvectors.
        (Default: both are calculated)
    subset_by_index : iterable, optional
        If provided, this two-element iterable defines the start and the end
        indices of the desired eigenvalues (ascending order and 0-indexed).
        To return only the second smallest to fifth smallest eigenvalues,
        ``[1, 4]`` is used. ``[n-3, n-1]`` returns the largest three. Only
        available with "evr", "evx", and "gvx" drivers. The entries are
        directly converted to integers via ``int()``.
    subset_by_value : iterable, optional
        If provided, this two-element iterable defines the half-open interval
        ``(a, b]`` that, if any, only the eigenvalues between these values
        are returned. Only available with "evr", "evx", and "gvx" drivers. Use
        ``np.inf`` for the unconstrained ends.
    driver : str, optional
        Defines which LAPACK driver should be used. Valid options are "ev",
        "evd", "evr", "evx" for standard problems and "gv", "gvd", "gvx" for
        generalized (where b is not None) problems. See the Notes section.
        The default for standard problems is "evr". For generalized problems,
        "gvd" is used for full set, and "gvx" for subset requested cases.
    type : int, optional
        For the generalized problems, this keyword specifies the problem type
        to be solved for ``w`` and ``v`` (only takes 1, 2, 3 as possible
        inputs)::
            1 =>     a @ v = w @ b @ v
            2 => a @ b @ v = w @ v
            3 => b @ a @ v = w @ v
        This keyword is ignored for standard problems.
    overwrite_a : bool, optional
        Whether to overwrite data in ``a`` (may improve performance). Default
        is False.
    overwrite_b : bool, optional
        Whether to overwrite data in ``b`` (may improve performance). Default
        is False.
    check_finite : bool, optional
        Whether to check that the input matrices contain only finite numbers.
        Disabling may give a performance gain, but may result in problems
        (crashes, non-termination) if the inputs do contain infinities or NaNs.
    turbo : bool, optional
        *Deprecated since v1.5.0, use ``driver=gvd`` keyword instead*.
        Use divide and conquer algorithm (faster but expensive in memory, only
        for generalized eigenvalue problem and if full set of eigenvalues are
        requested.). Has no significant effect if eigenvectors are not
        requested.
    eigvals : tuple (lo, hi), optional
        *Deprecated since v1.5.0, use ``subset_by_index`` keyword instead*.
        Indexes of the smallest and largest (in ascending order) eigenvalues
        and corresponding eigenvectors to be returned: 0 <= lo <= hi <= M-1.
        If omitted, all eigenvalues and eigenvectors are returned.
    Returns
    -------
    w : (N,) ndarray
        The N (1<=N<=M) selected eigenvalues, in ascending order, each
        repeated according to its multiplicity.
    v : (M, N) ndarray
        (if ``eigvals_only == False``)
    Raises
    ------
    LinAlgError
        If eigenvalue computation does not converge, an error occurred, or
        b matrix is not definite positive. Note that if input matrices are
        not symmetric or Hermitian, no error will be reported but results will
        be wrong.
    See Also
    --------
    eigvalsh : eigenvalues of symmetric or Hermitian arrays
    eig : eigenvalues and right eigenvectors for non-symmetric arrays
    eigh_tridiagonal : eigenvalues and right eiegenvectors for
        symmetric/Hermitian tridiagonal matrices
    Notes
    -----
    This function does not check the input array for being Hermitian/symmetric
    in order to allow for representing arrays with only their upper/lower
    triangular parts. Also, note that even though not taken into account,
    finiteness check applies to the whole array and unaffected by "lower"
    keyword.
    This function uses LAPACK drivers for computations in all possible keyword
    combinations, prefixed with ``sy`` if arrays are real and ``he`` if
    complex, e.g., a float array with "evr" driver is solved via
    "syevr", complex arrays with "gvx" driver problem is solved via "hegvx"
    etc.
    As a brief summary, the slowest and the most robust driver is the
    classical ``<sy/he>ev`` which uses symmetric QR. ``<sy/he>evr`` is seen as
    the optimal choice for the most general cases. However, there are certain
    occasions that ``<sy/he>evd`` computes faster at the expense of more
    memory usage. ``<sy/he>evx``, while still being faster than ``<sy/he>ev``,
    often performs worse than the rest except when very few eigenvalues are
    requested for large arrays though there is still no performance guarantee.
    For the generalized problem, normalization with respect to the given
    type argument::
            type 1 and 3 :      v.conj().T @ a @ v = w
            type 2       : inv(v).conj().T @ a @ inv(v) = w
            type 1 or 2  :      v.conj().T @ b @ v  = I
            type 3       : v.conj().T @ inv(b) @ v  = I
    Examples
    --------
    >>> from scipy.linalg import eigh
    >>> A = np.array([[6, 3, 1, 5], [3, 0, 5, 1], [1, 5, 6, 2], [5, 1, 2, 2]])
    >>> w, v = eigh(A)
    >>> np.allclose(A @ v - v @ np.diag(w), np.zeros((4, 4)))
    True
    Request only the eigenvalues
    >>> w = eigh(A, eigvals_only=True)
    Request eigenvalues that are less than 10.
    >>> A = np.array([[34, -4, -10, -7, 2],
    ...               [-4, 7, 2, 12, 0],
    ...               [-10, 2, 44, 2, -19],
    ...               [-7, 12, 2, 79, -34],
    ...               [2, 0, -19, -34, 29]])
    >>> eigh(A, eigvals_only=True, subset_by_value=[-np.inf, 10])
    array([6.69199443e-07, 9.11938152e+00])
    Request the second smallest eigenvalue and its eigenvector
    >>> w, v = eigh(A, subset_by_index=[1, 1])
    >>> w
    array([9.11938152])
    >>> v.shape  # only a single column is returned
    (5, 1)
    """
    # set lower
    uplo = 'L' if lower else 'U'
    # Set job for Fortran routines
    _job = 'N' if eigvals_only else 'V'

    drv_str = [None, "ev", "evd", "evr", "evx", "gv", "gvd", "gvx"]
    if driver not in drv_str:
        raise ValueError('"{}" is unknown. Possible values are "None", "{}".'
                         ''.format(driver, '", "'.join(drv_str[1:])))

    a1 = _asarray_validated(a, check_finite=check_finite)
    if len(a1.shape) != 2 or a1.shape[0] != a1.shape[1]:
        raise ValueError('expected square "a" matrix')
    overwrite_a = overwrite_a or (_datacopied(a1, a))
    cplx = True if iscomplexobj(a1) else False
    n = a1.shape[0]
    drv_args = {'overwrite_a': overwrite_a}

    if b is not None:
        b1 = _asarray_validated(b, check_finite=check_finite)
        overwrite_b = overwrite_b or _datacopied(b1, b)
        if len(b1.shape) != 2 or b1.shape[0] != b1.shape[1]:
            raise ValueError('expected square "b" matrix')

        if b1.shape != a1.shape:
            raise ValueError("wrong b dimensions {}, should "
                             "be {}".format(b1.shape, a1.shape))

        if type not in [1, 2, 3]:
            raise ValueError('"type" keyword only accepts 1, 2, and 3.')

        cplx = True if iscomplexobj(b1) else (cplx or False)
        drv_args.update({'overwrite_b': overwrite_b, 'itype': type})

    # backwards-compatibility handling
    subset_by_index = subset_by_index if (eigvals is None) else eigvals

    subset = (subset_by_index is not None) or (subset_by_value is not None)

    # Both subsets can't be given
    if subset_by_index and subset_by_value:
        raise ValueError('Either index or value subset can be requested.')

    # Take turbo into account if all conditions are met otherwise ignore
    if turbo and b is not None:
        driver = 'gvx' if subset else 'gvd'

    # Check indices if given
    if subset_by_index:
        lo, hi = [int(x) for x in subset_by_index]
        if not (0 <= lo <= hi < n):
            raise ValueError('Requested eigenvalue indices are not valid. '
                             'Valid range is [0, {}] and start <= end, but '
                             'start={}, end={} is given'.format(n-1, lo, hi))
        # fortran is 1-indexed
        drv_args.update({'range': 'I', 'il': lo + 1, 'iu': hi + 1})

    if subset_by_value:
        lo, hi = subset_by_value
        if not (-inf <= lo < hi <= inf):
            raise ValueError('Requested eigenvalue bounds are not valid. '
                             'Valid range is (-inf, inf) and low < high, but '
                             'low={}, high={} is given'.format(lo, hi))

        drv_args.update({'range': 'V', 'vl': lo, 'vu': hi})

    # fix prefix for lapack routines
    pfx = 'he' if cplx else 'sy'

    # decide on the driver if not given
    # first early exit on incompatible choice
    if driver:
        if b is None and (driver in ["gv", "gvd", "gvx"]):
            raise ValueError('{} requires input b array to be supplied '
                             'for generalized eigenvalue problems.'
                             ''.format(driver))
        if (b is not None) and (driver in ['ev', 'evd', 'evr', 'evx']):
            raise ValueError('"{}" does not accept input b array '
                             'for standard eigenvalue problems.'
                             ''.format(driver))
        if subset and (driver in ["ev", "evd", "gv", "gvd"]):
            raise ValueError('"{}" cannot compute subsets of eigenvalues'
                             ''.format(driver))

    # Default driver is evr and gvd
    else:
        driver = "evr" if b is None else ("gvx" if subset else "gvd")

    lwork_spec = {
                  'syevd': ['lwork', 'liwork'],
                  'syevr': ['lwork', 'liwork'],
                  'heevd': ['lwork', 'liwork', 'lrwork'],
                  'heevr': ['lwork', 'lrwork', 'liwork'],
                  }

    if b is None:  # Standard problem
        print(f"Standard eigenvalue problem: {pfx + driver}") 
        drv, drvlw = get_lapack_funcs((pfx + driver, pfx+driver+'_lwork'),
                                      [a1])
        clw_args = {'n': n, 'lower': lower}
        if driver == 'evd':
            clw_args.update({'compute_v': 0 if _job == "N" else 1})

        lw = _compute_lwork(drvlw, **clw_args)
        # Multiple lwork vars
        if isinstance(lw, tuple):
            lwork_args = dict(zip(lwork_spec[pfx+driver], lw))
        else:
            lwork_args = {'lwork': lw}

        drv_args.update({'lower': lower, 'compute_v': 0 if _job == "N" else 1})
        w, v, *other_args, info = drv(a=a1, **drv_args, **lwork_args)

    else:  # Generalized problem
        # 'gvd' doesn't have lwork query
        if driver == "gvd":
            print(f"generalized eigenvalue problem: {pfx + 'gvd'}")
            drv = get_lapack_funcs(pfx + "gvd", [a1, b1])
            lwork_args = {}
        else:
            print(f"generalized eigenvalue problem: {pfx + driver}")
            drv, drvlw = get_lapack_funcs((pfx + driver, pfx+driver+'_lwork'),
                                          [a1, b1])
            # generalized drivers use uplo instead of lower
            lw = _compute_lwork(drvlw, n, uplo=uplo)
            lwork_args = {'lwork': lw}

        drv_args.update({'uplo': uplo, 'jobz': _job})
        # SS: call of the lapack function 
        print(f"{drv_args} {lwork_args}")
        w, v, *other_args, info = drv(a=a1, b=b1, **drv_args, **lwork_args)
        print(f"info: {info} w: {w} v: {v} other_args: {other_args}")
    # m is always the first extra argument
    w = w[:other_args[0]] if subset else w
    v = v[:, :other_args[0]] if (subset and not eigvals_only) else v

    # Check if we had a  successful exit
    if info == 0:
        if eigvals_only:
            return w
        else:
            return w, v
    else:
        if info < -1:
            raise LinAlgError('Illegal value in argument {} of internal {}'
                              ''.format(-info, drv.typecode + pfx + driver))
        elif info > n:
            raise LinAlgError('The leading minor of order {} of B is not '
                              'positive definite. The factorization of B '
                              'could not be completed and no eigenvalues '
                              'or eigenvectors were computed.'.format(info-n))
        else:
            drv_err = {'ev': 'The algorithm failed to converge; {} '
                             'off-diagonal elements of an intermediate '
                             'tridiagonal form did not converge to zero.',
                       'evx': '{} eigenvectors failed to converge.',
                       'evd': 'The algorithm failed to compute an eigenvalue '
                              'while working on the submatrix lying in rows '
                              'and columns {0}/{1} through mod({0},{1}).',
                       'evr': 'Internal Error.'
                       }
            if driver in ['ev', 'gv']:
                msg = drv_err['ev'].format(info)
            elif driver in ['evx', 'gvx']:
                msg = drv_err['evx'].format(info)
            elif driver in ['evd', 'gvd']:
                if eigvals_only:
                    msg = drv_err['ev'].format(info)
                else:
                    msg = drv_err['evd'].format(info, n+1)
            else:
                msg = drv_err['evr']

            raise LinAlgError(msg)

def main(): 
    S = np.array([[1.               ,0.81471811604023], [0.81471811604023 , 1.              ]])
    Hcore = np.array([[-1.30365848262366,  -1.25605294504914], [-1.25605294504914 ,-1.30365848262366]])
    Eigs, U = eigh(Hcore,S)
    Eigs_ref = np.array([-1.4105283928383148, -0.2569357378989974])
    U_ref = np.array([[0.5249046436007102 ,-1.6427388312443174], [0.5249046436007102,1.6427388312443174]])
    print(f"Eigs: {Eigs} \nU: {U} \nEigs_ref: {Eigs_ref} \nU_ref: {U_ref}")
    assert np.allclose(Eigs,Eigs_ref)
    assert np.allclose(U,-1*U_ref)
    print("test_linalg is passed.")

if __name__ == "__main__": 
    main() 
