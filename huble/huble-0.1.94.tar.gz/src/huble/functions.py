import requests


def fetch_experiment(version_id):
    return requests.get(f"http://localhost:5000/versions/{version_id }").json()
