import numpy as np
import pandas as pd
from contextlib import closing
from functools import partial

import gqcms


def LagrangeScan(
    hubbard, operator, start: float, stop: float, step: float=0.05, method_str: str ="FCI", method_kwargs: dict = {}
) -> pd.DataFrame:
    """
    Computes the energy and expectation value of the constrained Hubbard
    Hamiltonian over a predefined range of Lagrange multipliers using the given
    method. The given method should return a pandas DataFrame with at least
    the columns ['E', 'C', '1PDM'].

    :param hubbard: hubbard class object
    :param operator: matrix representation of the feature operator
    :param start: first Lagrange value, inclusive
    :param stop: last Lagrange value, inclusive
    :param step: difference between two subsequent Lagrange values (default is 0.05)
    :param method_str: method used to solve the constrained Hubbard Hamiltonian, supported methods are 
        FCI, SCI and HF(default is FCI)
    :param method_kwargs: key word arguments passed to the used method

    :return: pandas DataFrame with the at least the columns
        ['E', 'C', '1PDM', 'mu', 'expectation_value']
    """

    multipliers = np.arange(start, stop + step, step)
    
    if method_str == 'FCI':
        scan_result = [
            gqcms.ConstrainedFCI(hubbard, operator, m) for m in multipliers
        ]
        
        return pd.concat(scan_result, ignore_index=True)
        
    elif method_str == 'SCI':
        scan_result = [
            gqcms.ConstrainedSCI(hubbard, operator, m, **method_kwargs)
            for m in multipliers
        ]
    
    elif method_str == 'HF':
        scan_result = []
        
        for m in multipliers:
            HF_solver = gqcms.ConstrainedHartreeFock(hubbard, operator, m, **method_kwargs)
            scan_result.append(HF_solver.solve())
    
    else:
        # Raise error if asked method is not supported
        raise ValueError("Supplied method is not supported yet.")

    # Return one DataFrame
    return pd.concat(scan_result, ignore_index=True, axis=1).T
    

def ExpectationValueScan(
    hubbard: gqcms.Hubbard,
    operator: np.ndarray,
    start: float,
    stop: float,
    step: float = 0.05,
    method_str: str = "FCI",
    method_kwargs: dict = {},
    iterations = 100,
    processes: int = 1,
    threshold: float = 1e-6,
    check_threshold: float = 1e-3,
    lower_boundary: int = -10,
    upper_boundary: int = 10,
    bPrintCheck: bool = True
) -> pd.DataFrame:
    """
    Computes the energy and expectation value of the constrained Hubbard
    Hamiltonian over a predefined range of expectation values

    :param hubbard: hubbard class object
    :param operator: matrix representation of the feature operator
    :param start: first Lagrange value, inclusive
    :param stop: last Lagrange value, inclusive
    :param step: difference between two subsequent Lagrange values (default is 0.05)
    :param method_str: method used to solve the constrained Hubbard Hamiltonian (default is FCI)
    :param method_kwargs: arguments passed to the given method
    :param processes: number of cores multiprocessing can use (default is 1)
    :param lower_boundary: lower boundary of the interval used for the line search (default is -10)
    :param upper_boundary: upper boundary of the interval used for the line search (default is 10)
    :param bPrintCheck: indicate if the number of failed optimizations must be print or not (default is True)

    :return: pandas DataFrame with the at least the columns
        ['E', 'C', '1PDM', 'mu', 'expectation_value']
    """

    expectation_values = np.arange(start, stop+step, step)

    # List to store the result DataFrames
    scan_results = []

    # Define function to optimize
    if method_str == 'FCI':
        
        def f(m, args) -> float:
            """
            Compute the expectation value of the operator.
            :param m: Lagrange multiplier
            """

            hubbard, operator, method_kwargs = args

            result = gqcms.ConstrainedFCI(hubbard, operator, m).squeeze()
            
            return result
    
    elif method_str == 'HF':
        
        def f(m, args) -> float:
            """
            Compute the expectation value of the operator.
            :param m: Lagrange multiplier
            """
            hubbard, operator, method_kwargs = args
            
            HF_solver = gqcms.ConstrainedHartreeFock(hubbard, operator, m, **method_kwargs)
            result = HF_solver.solve()
            
            return result

    elif method_str == 'SCI':
        
        def f(m, args) -> float:
            """
            Compute the expectation value of the operator.
            :param m: Lagrange multiplier
            """
            
            hubbard, operator, method_kwargs = args
            
            result = gqcms.ConstrainedSCI(hubbard, operator, m, **method_kwargs)
            
            return result

    else:
        # Raise error if asked method is not supported
        raise ValueError("Supplied method is not supported yet.")

    

    for expectation_value in expectation_values:
        
        _, result, success = gqcms.LineSearch(
            expectation_value,
            f,
            args=(hubbard, operator, method_kwargs),
            threshold=threshold,
            check_threshold=check_threshold,
            lower_boundary=lower_boundary,
            upper_boundary=upper_boundary,
            maxiter=iterations
        )
        
        # Add success status to dataframe
        result['success'] = success
        # Add requested expectation value
        result['requested_expectation_value'] = expectation_value

        scan_results.append(result)

    # Conver list of pandas Series to a dataframe
    # if method_str == "FCI":
    #     df = pd.concat(scan_results, ignore_index=True)
    #     print(df.info())
    # else:
    df = pd.concat(scan_results, ignore_index=True, axis=1).T

    # Print how many optimizations failed
    if bPrintCheck:
        num_failed = df['success'].value_counts().get(False, 0)
        print(f"There are {num_failed} failed optimizations")

    # Return one DataFrame
    return df
