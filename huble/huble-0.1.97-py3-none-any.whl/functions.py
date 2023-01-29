import requests


def fetch_experiment(experiment_id):
    return requests.get(f"http://localhost:8000/experiments/{experiment_id }").json()

