from .localrunner import simulate_run

def init_run(file_url: str, is_config: list, api_key: str, customer: str):
    return simulate_run(file_url, is_config, api_key, customer)