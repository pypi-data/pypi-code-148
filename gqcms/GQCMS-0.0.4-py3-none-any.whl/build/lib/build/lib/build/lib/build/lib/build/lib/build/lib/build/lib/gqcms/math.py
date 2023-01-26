def derivative(values, h):
    """
    Compute the numerical derivative up to second order
    """

    return [None, *[(values[i+1] - values[i-1])/h for i in range(1, len(values)-1)], None]