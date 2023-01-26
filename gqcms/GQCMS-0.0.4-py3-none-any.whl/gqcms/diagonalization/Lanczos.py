import numpy as np


def Lanczos(operator: np.ndarray, m: int = 400) -> np.ndarray:
    """
    Will perform the Lanczos algorithm

    :param operator: the operator to diagonalize

    Will return a tridiagonal matrix
    """
    # intitializing
    # unit vectors
    H = operator
    I = np.eye(H.shape[0])
    V = np.zeros_like(H)
    T = np.zeros((m, m))

    # First iteration
    v = I[:, 0]
    w_prime = H @ v
    alpha = w_prime.T @ v
    w = w_prime - alpha * v
    V[:, 0] = v
    v_old = v

    # following iterations
    for i in range(1, m):
        beta = np.sqrt(w.T @ w)
        if beta > 1e-8:
            v = w / beta
        else:
            v = I[:, i]
            for j in range(V.shape[1]):
                v -= v.T @ V[:, j]
                beta = 1
            v = v / np.linalg.norm(v)
        # Fill in the T matrix
        T[i - 1, i - 1] = alpha
        if i != m:
            T[i - 1, i] = beta
            T[i, i - 1] = beta

        V[:, i] = v
        w_prime = H @ v
        alpha = w_prime.T @ v
        w = w_prime - alpha * v - beta * v_old
        v_old = v

    return T, V[:, :m]
