import os
from typing import Callable, List


def tfrq(func: Callable, params: List, num_cores=os.cpu_count()):
    import math
    from concurrent.futures import ProcessPoolExecutor
    """
    Executes a given function, `func`, in parallel over a list of parameters, `params`.
    The function uses the number of cores available in the system to divide the parameters into chunks.
    Each chunk is then passed to a separate worker process for concurrent execution.

    Parameters:
        - func (function): The function to be executed in parallel.
        - params (List): The list of parameters to be passed to the function.
        - num_cores: default is os.cpu_count() - an integer

    Returns:
        - results (List): A list of results of the function execution for each parameter.

    Example:

    def square(x):
        return x * x

    params = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    results = pyrallel_process(square, params)

    print(results)
    # output: [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
    """
    chunk_size = math.ceil(len(params) / num_cores)
    chunks = [params[i:i + chunk_size] for i in range(0, len(params), chunk_size)]
    print("Tfrq into", len(chunks), "Chunks for", num_cores, "cores.")
    with ProcessPoolExecutor(max_workers=num_cores) as executor:
        results = list(executor.map(func, chunks))

    return results
