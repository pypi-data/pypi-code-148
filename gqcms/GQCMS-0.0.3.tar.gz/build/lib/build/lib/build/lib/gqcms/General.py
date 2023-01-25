from abc import abstractmethod
from collections import deque
import numpy as np
import scipy.sparse.linalg as sparse_linalg
import warnings


class IterativeAlgorithm:
    def __init__(self, env, init_steps: list = [], steps: list = []):

        self._env = env
        self._init_steps = init_steps
        self._steps = steps

    # TODO: print algorithm
    def print(self):
        
        print("  Initialization steps:")
        for i, step in enumerate(self._init_steps):
            try:
                print(f"\t{i+1}. {step.__name__}")
            except AttributeError:
                print(f"\t{i+1}. {step.func.__name__}")

        print("  Iterative steps:")
        for i, step in enumerate(self._steps):
            try:
                print(f"\t{i+1}. {step.__name__}")
            except AttributeError:
                print(f"\t{i+1}. {step.func.__name__}")

    def add_init_step(self, step):
        """
        Add a step to the init sequence
        """
        self._init_steps.append(step)

    def add_step(self, step):
        """
        Add a step at the end of the algorithm
        """
        self._steps.append(step)

    def insert_init_step(self, step, position):
        """
        Insert an init step at a specific position
        """
        self._init_steps.insert(position, step)

    def insert_step(self, position, step):
        """
        Insert a step at a specific position
        """
        self._steps.insert(position, step)

    def add_steps(self, steps: list):
        """
        Add multiple steps to the algorithm
        """
        self._steps.extend(steps)

    def remove_init_step(self, position):
        """
        Remove the init step at the specified position
        """
        del self._init_steps[position]
        
    def remove_step(self, position):
        """
        Remove the step at the specified position
        """
        del self._steps[position]

    def advance(self):
        """
        Run one cycle
        """
        for step in self._steps:
            try:
                step()
            except TypeError:
                step(self._env, self._env.system)

    def _run_init(self):
        """
        Perform the init functions from the init list        
        """

        # Run init steps
        for step in self._init_steps:
            try:
                step()
            except TypeError:
                step(self._env, self._env.system)
            

        self._env.iteration = 0

    def _run(self):
        """
        Run the iterative algorithm
        """

        # Start loop
        for _ in range(1, self._env.MAXITER):
            self._env.iteration += 1

            self.advance()

            if self._env.bconverged:
                # Break if converged
                break

        # No convergence reached, raise error
        else:
            warnings.warn("Max number of iteration reached.")
            # raise Warning("Max number of iteration reached.")

    def solve(self):

        self._run_init()
        self._run()
        
        return self._env


class DIIS:
    def __init__(self, env, P_string: str, max_size: int = None):
        """
        Initialize a DIIS object

        :paramm env: Environment object to store and retrive data
        :param P_string: the matrix name to take from the environment where DIIS is performed on
        :param max_size: maximum number of P matrices that are remembered (default is None, infinite size)
        :param diis_convergence: convergence criteria of rmsd
        """

        self._env = env
        self._P_string = P_string
        self._P_queue = deque(maxlen=max_size)
        self._r_queue = deque(maxlen=max_size)

        # Create a dictionairy to store previously computed overlap between residuals
        self._B_dict = {}

    def _add_P(self):
        """
        Add the current P matrix from the environment to the queue
        also commpute the residual and add it the the queue
        """
        self._P_queue.append(getattr(self._env, self._P_string))
        self._add_r()

    def _add_r(self):
        """
        Computes residual and add to queue
        """
        self._r_queue.append(self.compute_residual())

    def compute_rmsd(self):
        return np.einsum("ij,ij->", self._r_queue[-1], self._r_queue[-1])

    @abstractmethod
    def compute_residual(self):
        pass

    @abstractmethod
    def check_convergence(self):
        pass

    def diis_tensor(self):
        """
        Create the overlap matrix and set P in the environment equal to the diis solution by solving the Pulay equation
        """

        if self._env.iteration >= 1:

            # Create B matrix, consists of overlap between the residual vectors
            N = len(self._r_queue)
            B = np.zeros((N, N))

            for i in range(N):
                for j in range(N):
                    if (i, j) in self._B_dict.keys() or (j, i) in self._B_dict.keys():
                        B[i][j] = self._B_dict[(i, j)]
                    else:
                        r_overlap = np.einsum(
                            "ij,ij->", self._r_queue[i], self._r_queue[j]
                        )
                        B[i][j] = r_overlap
                        self._B_dict[(i, j)] = r_overlap
                        self._B_dict[(j, i)] = r_overlap

            last_row = -np.ones((1, N))
            last_col = -np.append(np.ones((N, 1)), [[0]], 0)

            B_lagrange = np.append(B, last_row, 0)
            B_lagrange = np.append(B_lagrange, last_col, 1)

            # Solve Pulay equation
            rhs_pulay = np.append(np.zeros((N, 1)), [[-1]])
            # C_pulay = linalg.inv(B_lagrange) @ rhs_pulay
            C_pulay = sparse_linalg.lsmr(B_lagrange, rhs_pulay)[0]

            # Create DIIS P matrix and update environment
            setattr(
                self._env,
                self._P_string,
                sum([c_p * P_i for c_p, P_i in zip(C_pulay, self._P_queue)]),
            )

    def diis_step(self):

        # Add current P to the queue and compute residual
        self._add_P()

        setattr(self._env, f"rmsd_{self._P_string}", self.compute_rmsd())

        # If convergence is reached stop algorithm
        if self.check_convergence():
            self._env.bconverged

        # Create DIIS P matrix
        self.diis_tensor()