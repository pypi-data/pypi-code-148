import requests
import json
from datetime import datetime
from dataclasses import dataclass, asdict
from acceldata_sdk.torch_client import TorchClient


@dataclass
class Pipelineb:
    id: str

    def __init__(self, dag_id, **kwargs):
        self.id = dag_id


@dataclass
class PipelineRunb:
    id: str
    pipelineId: str
    state: str
    start_date: datetime
    end_date: datetime

    def __init__(self, dag_run_id, dag_id, state, start_date, end_date, **kwargs):
        self.id = dag_run_id
        self.pipelineId = dag_id
        self.state = "SUCCESS"
        if state is not None and 'failed' in state:
            self.state = 'FAILURE'
        # elif state is not None:
        #     self.state = state
        self.start_date = start_date
        self.end_date = end_date


@dataclass
class Jobb:
    id: str
    downstreamTaskIds: [str]
    state: str
    start_date: datetime
    end_date: datetime
    pipelineId: str
    pipelineRunId: str

    def __init__(self, task_id, dag_id, start_date,end_date, dag_run_id,state="STARTED", downstream_task_ids = [], **kwargs):
        self.id = task_id
        self.pipelineId = dag_id
        self.state = "FINISHED"
        if state is not None and 'fail' in state:
            self.state = 'ERRORED'
        # elif state is not None:
        #     self.state = state
        self.start_date = start_date
        self.end_date = end_date
        self.pipelineRunId = dag_run_id
        self.downstreamTaskIds = downstream_task_ids


@dataclass
class PipelineBulkupdateRequest:
    pipelines: list()
    pipelineruns: list()
    jobs: list()


def collect_data():
    # URL = "http://airflow_airflow-webserver_1:8080/api/v1/dags"
    DAGS_URL = "http://localhost:8082/api/v1/dags"

    PARAMS = {}
    _HEADERS = dict()
    _HEADERS['Authorization'] = 'Basic YWlyZmxvdzphaXJmbG93'
    # sending get request and saving the response as response object
    r = requests.get(url = DAGS_URL, params = PARAMS, headers = _HEADERS)


    # extracting data in json format
    data = r.json()
    print (data)
    dags = data['dags']
    dagruns = list()
    dagidTaskid_downstream = dict()
    for dag in dags:
        tasksperdags = dict()
        DAGSRUNS_URL = f"http://localhost:8082/api/v1/dags/{dag['dag_id']}/dagRuns"
        r = requests.get(url=DAGSRUNS_URL, params=PARAMS, headers=_HEADERS)
        runs = r.json()
        dagruns.extend(runs['dag_runs'])
        DAGStasks_URL = f"http://localhost:8082/api/v1/dags/{dag['dag_id']}/tasks"
        r = requests.get(url=DAGStasks_URL, params=PARAMS, headers=_HEADERS)
        if r.status_code == 200:
            data = r.json()
            tasksperdags[dag['dag_id']] = data['tasks']
            for task in tasksperdags[dag['dag_id']]:
                dagid_taskid = f"{dag['dag_id']}:{task['task_id']}"
                dagidTaskid_downstream[dagid_taskid] = task['downstream_task_ids']

    tasks = list()
    for dagrun in dagruns:
        DAGSRUNStasks_URL = f"http://localhost:8082/api/v1/dags/{dagrun['dag_id']}/dagRuns/{dagrun['dag_run_id']}/taskInstances"
        r = requests.get(url=DAGSRUNStasks_URL, params=PARAMS, headers=_HEADERS)
        tasks_instances = r.json()
        for task_instance in tasks_instances['task_instances']:
            task_instance['dag_run_id'] = dagrun['dag_run_id']
            try:
                task_instance['downstream_task_ids'] = dagidTaskid_downstream[f"{dagrun['dag_id']}:{task_instance['task_id']}"]
            except:
                print ("key not found")
        tasks.extend(tasks_instances['task_instances'])

    temp_pipelines = list()
    temp_pipelineruns = list()
    temp_jobs = list()
    for temp in dags:
        temp_pipelines.append(Pipelineb(**temp))
    for temp in dagruns:
        temp_pipelineruns.append(PipelineRunb(**temp))
    for temp in tasks:
        temp_jobs.append(Jobb(**temp))
    print (tasks_instances)
    bulkUpdateRequest = PipelineBulkupdateRequest(pipelines = temp_pipelines, pipelineruns = temp_pipelineruns, jobs = temp_jobs)
    print (bulkUpdateRequest)
    print (f'json: {bulkUpdateRequest}')

    print(json.dumps(asdict(bulkUpdateRequest)))
    torch_credentials = {
        'url': 'https://torch.acceldata.local:5443/torch',
        'access_key': 'P04IM8FNQRUCRTU',
        'secret_key': 'E6LL9YUPMG4BDTJHT2VZD75HW0B8E5'
    }

    torch_client = TorchClient(**torch_credentials)
    torch_client.bulkupdate_pipeline(bulkUpdateRequest)


if __name__ == '__main__':
    collect_data()
