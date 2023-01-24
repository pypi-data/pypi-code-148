import os
from typing import Callable, List

from tqdm import tqdm

config_default_values = {"pass_as_single_argument": True, "return_errors": False, "print_errors": True}


def param_list(exec_data):
    func = exec_data[0]
    chunk_id = exec_data[1]
    params = exec_data[2]
    config = exec_data[3]

    results = []
    errors = []
    for param in tqdm(params, desc=f"processing: - chunk_num[{str(chunk_id)}] pid[{str(os.getpid())}]"):
        try:
            if config["pass_as_single_argument"]:
                results.append(func(param))
            else:
                results.append(func(*param))
        except Exception as e:
            if config["print_errors"]:
                print(e)
            errors.append(e)
    return results, errors


def tfrq(func: Callable, params: List, num_cores=None, config=None):
    import math
    from concurrent.futures import ProcessPoolExecutor
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
