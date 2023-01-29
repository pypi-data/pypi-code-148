import requests


def get_experiment_details(version_id):
    response = requests.get(
        f"http://localhost:8000/verisons/{version_id}/",
    )
    response = response.json()
    graph = response['experiment']['pipeline']['pipelineJSON']
    url = f"https://ipfs.filebase.io/ipfs/{response['experiment']['model']['filePath']}"
    return graph,url