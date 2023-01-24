import os
from typing import Callable, List

from helpers import param_list


def tfrq(func: Callable, params: List, num_cores=os.cpu_count()):
    import math
    from concurrent.futures import ProcessPoolExecutor
    chunk_size = math.ceil(len(params) / num_cores)
    chunks = [params[i:i + chunk_size] for i in range(0, len(params), chunk_size)]
    print("Tfrq into", len(chunks), "Chunks for", num_cores, "cores.")
    with ProcessPoolExecutor(max_workers=num_cores) as executor:
        results = list(executor.map(param_list, [(func, chunk_num, chunk) for chunk_num, chunk in enumerate(chunks)]))

    return results
