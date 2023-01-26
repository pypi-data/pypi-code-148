import numpy as np


class _Agg:
    def __init__(self, col_name):
        self.col_name = col_name

    def _get_func(self):
        raise NotImplemented

    def as_tuple(self):
        func = self._get_func()
        return self.col_name, func


class Count(_Agg):
    def __init__(self):
        super().__init__(None)

    def _get_func(self):
        return np.size


class Min(_Agg):
    def _get_func(self):
        return np.min


class Max(_Agg):
    def _get_func(self):
        return np.max


class Mean(_Agg):
    def _get_func(self):
        return np.mean


class Std(_Agg):
    def _get_func(self):
        return np.std


class Any(_Agg):
    def _get_func(self):
        return lambda x: x.values[0] if len(x) else np.NaN


class UniqueVals(_Agg):
    def _get_func(self):
        return lambda x: np.unique(x.values).tolist() if len(x) else []


class Lambda(_Agg):
    def __init__(self, col_name, func):
        super().__init__(col_name)
        self.func = func

    def _get_func(self):
        return self.func


