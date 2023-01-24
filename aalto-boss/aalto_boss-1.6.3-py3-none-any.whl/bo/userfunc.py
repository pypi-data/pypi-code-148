import numpy as np
from boss.utils.arrays import shape_consistent_XY


class UserFunc:
    """Wrapper class for BOSS user functions. """

    def __init__(self, func, dim):
        self.func = func
        self.dim = dim

    def eval(self, X_in):
        X_in = np.atleast_2d(X_in)
        output = self.func(X_in)

        if isinstance(output, tuple):
            X_out = output[0]
            Y = output[1]
        else:
            Y = output
            X_out = X_in

        return shape_consistent_XY(X_out, Y, self.dim)

    def __call__(self, X_in):
        return self.eval(X_in)
