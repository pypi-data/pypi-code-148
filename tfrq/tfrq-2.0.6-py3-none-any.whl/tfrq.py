from typing import Callable, List


def tfrq(func: Callable, params: List, num_cores=None, config=None):
    import math
    from concurrent.futures import ProcessPoolExecutor
    from helpers import param_list, config_default_values
    import os

    if num_cores is None:
        num_cores = os.cpu_count()

    if config is None:
        config = config_default_values

    else:
        for cfg in config_default_values:
            if cfg not in config:
                config[cfg] = config_default_values[cfg]

    chunk_size = math.ceil(len(params) / num_cores)
    chunks = [params[i:i + chunk_size] for i in range(0, len(params), chunk_size)]
    print("Tfrq into", len(chunks), "Chunks for", num_cores, "cores.")
    with ProcessPoolExecutor(max_workers=num_cores) as executor:
        results = list(
            executor.map(param_list, [(func, chunk_num, chunk, config) for chunk_num, chunk in enumerate(chunks)]))

    errors = []
    final_results = []
    for res in results:
        final_results.append(res[0])
        errors.append(res[1])

    if config["return_errors"]:
        return final_results, errors
    else:
        return final_results
