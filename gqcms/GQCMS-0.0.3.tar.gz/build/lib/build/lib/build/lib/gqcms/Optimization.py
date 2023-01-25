import numpy as np


def LineSearch(
    a: float,
    f: callable,
    args: tuple = (),
    lower_boundary: float = -10.0,
    upper_boundary: float = 10.0,
    threshold: float = 1e-6,
    check_threshold: float = 1e-3,
    maxiter: int = 100,
    blog: bool = False,
) -> tuple:
    """
    Optimizes the expectation value of function f to the value a by splitting the interval of lower_boundary
    and upper_boundary in halve. This function assumes that f is a strictly rising function in the interval 
    [lower_boundary, upper_boundary].

    :param f: function to optimize, must return a pandas Series with at least the column 'expectation_value'
    :param a: requested value of the function
    :param args: arguments for the function f
    :param lower_boundary: minimum value of the Lagrange multiplier (default is -10.0)
    :param upper_boundary: maximum value of the Lagrange multiplier (default is 10.0)
    :param threshold: minimum difference between computed and requested value (default is 1e-3)
    :param maxiter: maximum number of iterations (default is 100)
    
    :return: a tuple with the optimized value and a bool wheter or not the optimization is
        successful
    """

    # Evaluate the center of mu_range
    x = (lower_boundary + upper_boundary) / 2
    result = f(x, args)

    # Compute difference between computed population and requested
    da = result['expectation_value'] - a

    iteration = 0
    # Stop if the threshold or the maximum number of iterations is reached
    while np.abs(da) > threshold and iteration < maxiter:
        iteration += 1

        # If the difference between the true value and the current value is 
        # possitive, than the current x value is too large. The upper boundary
        # is reduced by setting it equal to the current x value.
        if da > 0:
            upper_boundary = x

        # If the difference between the true value and the current value is 
        # negative, than the current x value is too low. The lower boundary
        # is reduced by setting it equal to the current x value.
        else:
            lower_boundary = x

        # Take the center of the new interval as the new x value
        x = (lower_boundary + upper_boundary) / 2

        # Recomputed the function value
        result = f(x, args)

        # Compute difference between computed population and requested
        da = result['expectation_value'] - a

    # Print end result if log is on
    if blog:
        print(
            f"x: {x}\t da: {da}\t result: {result}\t a: {a}\t iterations: {iteration}"
        )

    # Check optimization
    success = np.abs(f(x, args)['expectation_value'] - a) < check_threshold

    return x, result, success

