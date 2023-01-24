import abc
import contextlib
import os
import shutil
from pathlib import Path
from typing import List, Optional, Tuple

import numpy as np


def remove_boss_files():
    path = Path.cwd()
    for file_path in [path / "boss.in", path / "boss.out", path / "boss.rst"]:
        if file_path.exists():
            file_path.unlink()
    shutil.rmtree(path / "postprocessing", ignore_errors=True)


class execute_in(contextlib.ContextDecorator):
    def __init__(self, rundir):
        self.rundir = Path(rundir)
        self.origin = Path.cwd()
        super().__init__()

    def __enter__(self):
        os.chdir(self.rundir)

    def __exit__(self, *exc):
        os.chdir(self.origin)


class TestFunc(abc.ABC):
    """Base class for benchmark optimization problems."""

    # Should be truthy if the test function can accept multiple
    # data points, given as rows in an ndarray, and return a corresponding
    # array of evalutations.
    vectorized = False

    def __init__(
        self,
        std: Optional[float] = None,
        seed: Optional[int] = None,
        ndim: Optional[int] = None,
        bounds: Optional[np.ndarray] = None,
    ) -> None:

        # Noisy evaluations
        self.std = std
        self.seed = seed
        if seed:
            np.random.seed(seed)

        # Default value of the bounds attribute
        if bounds is not None:
            bounds = np.asarray(bounds)

        self._bounds = bounds

        # Default value of the ndim attribute
        if ndim:
            self._ndim = ndim
        elif self.bounds is not None:
            self._ndim = self.bounds.shape[0]

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @property
    def tags(self) -> dict:
        """Tags to make the function searchable / categorizable."""
        return {}

    @property
    def minima(self) -> List[Tuple[np.ndarray, float]]:
        """Optional, a list of tuples (xmin, ymin) containing any local or global minima."""
        raise NotImplementedError

    @property
    def bounds(self) -> np.ndarray:
        """The bounds of the problem, give row-wise in an ndarray."""
        return self._bounds

    @bounds.setter
    def bounds(self, new_bounds: np.ndarray) -> None:
        new_bounds = np.asarray(new_bounds)
        if self.ndim is not None:
            if new_bounds.shape[0] != self.ndim:
                raise ValueError(
                    f"Specified bounds {new_bounds}"
                    + f"are not consistent with ndim = {self.ndim}"
                )
        self._bounds = new_bounds

    @property
    @abc.abstractmethod
    def fmin(self) -> float:
        """The global minimum value."""
        raise ValueError

    @property
    @abc.abstractmethod
    def xmins(self) -> np.ndarray:
        """The global minima given as rows in a 2d np.ndarray."""
        pass

    @property
    def xmin(self) -> np.ndarray:
        """The global minimum, if a single one exists"""
        if self.xmins.shape[0] == 1:
            return self.xmins[0, :]
        else:
            raise ValueError

    @property
    def frange(self) -> np.ndarray:
        """Optional, the expected range over which f varies.

        Only used in BOSS to initialize hyperparameters."""
        return None

    @abc.abstractmethod
    def eval(self, x: np.ndarray):
        """Implementation of the test function."""
        pass

    def eval_grad(self, x: np.ndarray):
        """Implementation of the test function."""
        pass

    @property
    def ndim(self) -> int:
        """The dimension of the function domain."""
        return self._ndim

    def __call__(self, x: np.ndarray):
        if self.vectorized:
            x = np.atleast_2d(x)
        else:
            x = np.asarray(x)
        y = self.eval(x)
        if self.std:
            y += np.random.normal(0, self.std, size=y.shape)
        return np.squeeze(y)

    def grad(self, x: np.ndarray):
        if self.vectorized:
            x = np.atleast_2d(x)
        else:
            x = np.asarray(x)
        y = self.eval_grad(x)
        if self.std:
            y += np.random.normal(0, self.std, size=y.shape)
        return np.squeeze(y)


def get_test_func(name: str, **kwargs) -> TestFunc:
    """Convenience instantiation of any test function."""
    test_funcs = {
        "forrester": Forrester,
        "grammacylee": GrammacyLee,
        "ackely1": Ackley1,
        "alpine1": Alpine1,
        "alpine2": Alpine2,
        "adjiman": Adjiman,
        "bartelsconn": BartelsConn,
        "beale": Beale,
        "camelthreehump": CamelThreeHump,
        "camelsixhump": CamelSixHump,
        "eggcrate": EggCrate,
        "exponential": Exponential,
        "goldsteinprice": GoldsteinPrice,
        "himmelblau": Himmelblau,
        "himmelvalley": Himmelvalley,
        "periodic": Periodic,
        "rastigrin": Rastigrin,
        "rosenbrock": Rosenbrock,
        "salomon": Salomon,
        "sphere": Sphere,
        "styblinskitang": StyblinskiTang,
        "wolfe": Wolfe,
    }
    name_lower = name.lower()
    if name_lower in test_funcs:
        f = test_funcs[name_lower](**kwargs)
    else:
        raise ValueError(f"Could not find test function {name}.")
    return f


class Forrester(TestFunc):
    vectorized = True
    tags = {
        "continuous": True,
        "differentiable": True,
        "multimodal": True,
        "dimension": 1,
    }

    bounds = np.array([[0.0, 1.0]])
    frange = np.array([-10.0, 10.0])
    xmins = np.array([[0.757249]])
    fmin = -6.02074
    ndim = 1

    def eval(self, x):
        return (6 * x - 2) ** 2 * np.sin(12 * x - 4)


class GrammacyLee(TestFunc):
    vectorized = True
    tags = {
        "continuous": True,
        "differentiable": True,
        "dimension": 1,
    }

    bounds = np.array([[0.5, 2.5]])
    frange = np.array([-10.0, 10.0])
    xmins = np.array([[0.548563]])
    fmin = -0.869011
    ndim = 1

    def eval(self, x):
        return 0.5 * np.sin(10 * np.pi * x) / x + (x - 1) ** 4


class Ackley1(TestFunc):

    vectorized = True
    tags = {
        "continuous": True,
        "differentiable": True,
        "dimension": None,
    }

    @property
    def bounds(self):
        return np.tile([-35.0, 35.0], (self.ndim, 1))

    @property
    def xmins(self):
        return np.zeros((1, self.ndim))

    @property
    def fmin(self):
        return 0.0

    def eval(self, x):
        d = self.ndim
        val = (
            -20 * np.exp(-0.02 * np.sqrt(1.0 / d * np.sum(x**2, axis=1)))
            - np.exp(1.0 / d * np.sum(np.cos(2 * np.pi * x), axis=1))
            + np.exp(0)
            + 20
        )
        return val


class Alpine1(TestFunc):

    vectorized = True
    tags = {
        "continuous": True,
        "differentiable": False,
        "dimension": None,
    }
    fmin = 0.0

    @property
    def bounds(self):
        return np.tile([-10.0, 10.0], (self.ndim, 1))

    @property
    def xmins(self):
        return np.zeros((1, self.ndim))

    def eval(self, x):
        val = np.sum(np.abs(x * np.sin(x) + 0.1 * x), axis=1)
        return val


class Alpine2(TestFunc):

    vectorized = True
    tags = {
        "continuous": True,
        "differentiable": True,
        "dimension": None,
    }

    def __init__(self, *args, **kwargs):
        if kwargs.get("ndim", None) is None:
            raise ValueError(
                "ndim (postive integer) must be specified for test functions with arbitrary dimension."
            )
        super().__init__(*args, **kwargs)
        if self._bounds is None:
            self._bounds = np.tile([0.0, 10.0], (self.ndim, 1))

    @property
    def xmins(self):
        return np.ones((1, self.ndim)) * 7.917

    @property
    def fmin(self):
        return -(2.808**self.ndim)

    def eval(self, x):
        val = -np.product(np.sqrt(x) * np.sin(x), axis=1)
        return val


class Adjiman(TestFunc):

    vectorized = True
    tags = {
        "continuous": True,
        "differentiable": True,
        "dimension": 2,
    }

    bounds = np.array([[-1.0, 2.0], [-1.0, 1.0]])
    xmins = np.array([[2, 0.10578]])
    fmin = -2.02181
    ndim = 2

    def eval(self, x):
        val = np.cos(x[:, 0]) * np.sin(x[:, 1]) - x[:, 0] / (x[:, 1] ** 2 + 1)
        return val


class BartelsConn(TestFunc):

    vectorized = True
    tags = {
        "continuous": True,
        "differentiable": False,
        "dimension": 2,
    }

    bounds = np.array([[-500.0, 500.0], [-500.0, 500.0]])
    xmins = np.array([[0.0, 0.0]])
    fmin = 1.0
    ndim = 2

    def eval(self, x):
        val = (
            np.abs(x[:, 0] ** 2 + x[:, 1] ** 2 + x[:, 0] * x[:, 1])
            + np.abs(np.sin(x[:, 0]))
            + np.abs(np.cos(x[:, 1]))
        )
        return val


class Beale(TestFunc):

    vectorized = True
    tags = {
        "continuous": True,
        "differentiable": True,
        "dimension": 2,
    }

    bounds = np.array([[-4.5, 4.5]] * 2)
    xmins = np.array([[3.0, 0.5]])
    fmin = 0.0
    ndim = 2

    def eval(self, x):
        val = (
            (1.5 - x[:, 0] + x[:, 0] * x[:, 1]) ** 2
            + (2.25 - x[:, 0] + x[:, 0] * x[:, 1] ** 2) ** 2
            + (2.625 - x[:, 0] + x[:, 0] * x[:, 1] ** 3) ** 2
        )
        return val


class CamelThreeHump(TestFunc):

    vectorized = True
    tags = {
        "continuous": True,
        "differentiable": True,
        "multimodal": True,
        "dimension": 2,
    }

    bounds = np.array([[-5.0, 5.0]] * 2)
    xmins = np.array([[0.0, 0.0]])
    fmin = 0.0
    ndim = 2

    def eval(self, x):
        val = (
            2 * x[:, 0] ** 2
            - 1.05 * x[:, 0] ** 4
            + x[:, 0] ** 6 / 6
            + x[:, 0] * x[:, 1]
            + x[:, 1] ** 2
        )
        return val


class CamelSixHump(TestFunc):

    vectorized = True
    tags = {
        "continuous": True,
        "differentiable": True,
        "dimension": 2,
    }

    bounds = np.array([[-5.0, 5.0]] * 2)
    xmins = np.array([[-0.0898, 0.7126], [0.0898, -0.7126]])
    fmin = -1.0316
    ndim = 2

    def eval(self, x):
        val = (
            (4 - 2.1 * x[:, 0] ** 2 + x[:, 0] ** 4 / 3) * x[:, 0] ** 2
            + x[:, 0] * x[:, 1]
            + (4 * x[:, 1] ** 2 - 4) * x[:, 1] ** 2
        )
        return val


class EggCrate(TestFunc):

    vectorized = True
    tags = {
        "continuous": True,
        "differentiable": True,
        "dimension": 2,
    }

    frange = np.array([0.0, 100.0])
    bounds = np.array([[-5.0, 5.0]] * 2)
    xmins = np.array([[0.0, 0.0]])
    fmin = 0.0
    ndim = 2

    def eval(self, x):
        val = (
            x[:, 0] ** 2
            + x[:, 1] ** 2
            + 25 * (np.sin(x[:, 0]) ** 2 + np.sin(x[:, 1]) ** 2)
        )
        return val


class Exponential(TestFunc):
    vectorized = True
    tags = {
        "continuous": True,
        "differentiable": True,
        "dimension": None,
    }
    fmin = 1.0

    @property
    def bounds(self):
        return np.tile([-1.0, 1.0], (self.ndim, 1))

    @property
    def xmins(self):
        return np.zeros((1, self.ndim))

    def eval(self, x):
        val = -np.exp(-0.5 * np.sum(x**2, axis=1))
        return val


class GoldsteinPrice(TestFunc):

    vectorized = True
    tags = {
        "continuous": True,
        "differentiable": True,
        "dimension": 2,
    }

    bounds = np.array([[-2.0, 2.0]] * 2)
    xmins = np.array([[0.0, -1.0]])
    fmin = 3.0
    ndim = 2

    def eval(self, x):
        x0 = x[:, 0]
        x1 = x[:, 1]
        val = (
            1
            + (x0 + x1 + 1) ** 2
            * (19 - 14 * x0 + 3 * x0**2 - 14 * x1 + 6 * x0 * x1 + 3 * x1**2)
        ) * (
            30
            + (2 * x0 - 3 * x1) ** 2
            * (18 - 32 * x0 + 12 * x0**2 + 48 * x1 - 36 * x0 * x1 + 27 * x1**2)
        )
        return val


class Himmelblau(TestFunc):
    """Himmelblau function, has 4 global mins."""

    vectorized = True
    tags = {
        "continuous": True,
        "differentiable": True,
        "dimension": 2,
    }

    bounds = np.array([[-5.0, 5.0], [-5.0, 5.0]])
    xmins = np.array(
        [
            [3.0, 2.0],
            [-2.805118, 3.131312],
            [-3.779310, -3.283186],
            [3.584428, -1.848126],
        ]
    )
    fmin = 0.0
    ndim = 2

    def eval(self, X):
        x = X[:, 0]
        y = X[:, 1]
        z = (x**2 + y - 11) ** 2 + (x + y**2 - 7) ** 2
        return z


class Himmelvalley(TestFunc):
    """Modified Himmelblau function with one global min."""

    vectorized = True
    tags = {
        "continuous": True,
        "differentiable": True,
        "dimension": 2,
    }

    bounds = np.array([[-5.0, 5.0], [-5.0, 5.0]])
    xmins = np.array([[-4.00035, -3.55142]])
    fmin = -1.463295972168
    frange = np.array([0.0, 10.0])
    ndim = 2

    def eval(self, X):
        x = X[:, 0]
        y = X[:, 1]
        z = 0.01 * ((x**2 + y - 11) ** 2 + (x + y**2 - 7) ** 2 + 20 * (x + y))
        return z


class Periodic(TestFunc):

    vectorized = True
    tags = {
        "continuous": True,
        "differentiable": True,
        "dimension": None,
    }
    frange = np.array([0.0, 5])
    fmin = 0.9

    def __init__(self, *args, **kwargs):
        if kwargs.get("ndim", None) is None:
            raise ValueError(
                "ndim (postive integer) must be specified for test functions with arbitrary dimension."
            )
        super().__init__(*args, **kwargs)
        if self._bounds is None:
            self._bounds = np.tile([-10.0, 10.0], (self.ndim, 1))

    @property
    def xmins(self):
        return np.zeros((1, self.ndim))

    def eval(self, x):
        val = 1 + np.sum(np.sin(x) ** 2, axis=1) - 0.1 * np.exp(-np.sum(x**2, axis=1))
        return val


class Rastigrin(TestFunc):
    vectorized = True
    tags = {
        "continuous": True,
        "differentiable": True,
        "dimension": None,
    }
    frange = np.array([0.0, 100])
    fmin = 0.0

    def __init__(self, *args, **kwargs):
        if kwargs.get("ndim", None) is None:
            raise ValueError(
                "ndim (postive integer) must be specified for test functions with arbitrary dimension."
            )
        super().__init__(*args, **kwargs)
        if self._bounds is None:
            self._bounds = np.tile([-5.12, 5.12], (self.ndim, 1))

    @property
    def xmins(self):
        return np.zeros((1, self.ndim))

    def eval(self, x):
        val = 10 * self.ndim + np.sum(x**2 - 10 * np.cos(2 * np.pi * x), axis=1)
        return val


class Rosenbrock(TestFunc):
    vectorized = True
    tags = {
        "continuous": True,
        "differentiable": True,
        "dimension": None,
    }
    fmin = 0.0

    @property
    def bounds(self):
        return np.tile([-30.0, 30.0], (self.ndim, 1))

    @property
    def xmins(self):
        return np.ones((1, self.ndim))

    def eval(self, x):
        val = np.sum(100 * (x[:, 1:] - x[:, :-1] ** 2) ** 2 + (x[:, :-1] - 1) ** 2)
        return val


class Salomon(TestFunc):

    vectorized = True
    tags = {
        "continuous": True,
        "differentiable": True,
        "dimension": None,
    }

    fmin = 0.0

    def __init__(self, *args, **kwargs):
        if kwargs.get("ndim", None) is None:
            raise ValueError(
                "ndim (postive integer) must be specified for test functions with arbitrary dimension."
            )
        super().__init__(*args, **kwargs)
        if self._bounds is None:
            self._bounds = np.tile([-100.0, 100.0], (self.ndim, 1))

    @property
    def xmins(self):
        return np.zeros((1, self.ndim))

    def eval(self, x):
        val = (
            1
            - np.cos(2 * np.pi * np.sqrt(np.sum(x**2, axis=1)))
            + 0.1 * np.sqrt(np.sum(x**2, axis=1))
        )
        return val


class Sphere(TestFunc):

    vectorized = True
    tags = {
        "continuous": True,
        "differentiable": True,
        "dimension": None,
    }

    fmin = 0.0

    @property
    def bounds(self):
        return np.tile([0.0, 10.0], (self.ndim, 1))

    @property
    def xmins(self):
        return np.zeros((1, self.ndim))

    def eval(self, x):
        val = np.sum(x**2, axis=1)
        return val


class StyblinskiTang(TestFunc):

    vectorized = True

    tags = {
        "continuous": True,
        "differentiable": True,
        "dimension": None,
    }
    frange = np.array([-50.0, 100])

    def __init__(self, *args, **kwargs):
        if kwargs.get("ndim", None) is None:
            raise ValueError(
                "ndim (postive integer) must be specified for test functions with arbitrary dimension."
            )
        super().__init__(*args, **kwargs)
        if self._bounds is None:
            self._bounds = np.tile([-5.0, 5.0], (self.ndim, 1))

    @property
    def fmin(self):
        return -39.16599 * self.ndim

    @property
    def xmins(self):
        return -2.903534 * np.ones((1, self.ndim))

    def eval(self, x):
        val = 0.5 * np.sum(x**4 - 16 * x**2 + 5 * x, axis=1)
        return val

    def eval_grad(self, x):
        return 2 * x**3 - 16 * x + 2.5


class Wolfe(TestFunc):

    tags = {
        "continuous": True,
        "differentiable": True,
        "dimension": 3,
    }

    bounds = np.array([[0.0, 2.0]] * 3)
    xmins = np.array([[0.0, 0.0, 0.0]])
    fmin = 0.0
    ndim = 3

    def eval(self, x):
        val = 4.0 / 3 * (x[0] ** 2 + x[1] ** 2 - x[0] * x[1]) ** 0.75 + x[2]
        return val
