from typing import Dict, Optional


class GanymedeContext:
    """
    Grants access to ganymede context dict for use without Flow

    Parameters
    ----------
    input_file_name : str
        name of input file
    input_file_name_suffix : str
        file extension of input file
    run_id : str
        timestamp of Airflow run, used to identify run
    task_id: str
        id of Airflow task
    inputs: Dict[str, str]
        contents of input files, keyed by parameter type (e.g. - csv)
    params: Dict[str, str]
        config object
    """

    input_file_name: str
    input_file_name_suffix: str
    run_id: str
    task_id: str
    inputs: Dict[str, str]
    params: Dict[str, str]

    def __init__(self, context: Dict, input_file_name: str = None):
        from pathlib import Path
        from datetime import datetime
        import copy

        dag_id = context["dag"].dag_id
        dag_run_id = context["run_id"]
        initiator = "user"  # TODO: add user email or other identifier
        conf = context["dag_run"].conf
        task_id = context["task"].task_id

        self.run_id = datetime.fromtimestamp(int(dag_run_id) / 1000).isoformat()
        if input_file_name:
            self.input_file_name = str(Path(input_file_name).with_suffix("")).strip()
            self.input_file_name_suffix = Path(input_file_name).suffix

        if conf and task_id:
            self.task_id = task_id
            self.inputs = {}
            for k, v in conf.items():
                key = k.replace(f"{task_id}.", "")
                self.inputs[key] = v

        if conf:
            self.params = conf

        self.context = context

        # Construct dict for metadata table
        dict_inputs = copy.deepcopy(self.inputs)
        dict_inputs.pop("runId")
        dict_inputs = list(dict_inputs.values())

        self.metadata_dict = {
            "flow_id": dag_id,
            "flow_run_id": dag_run_id,
            "initiator": initiator,
            "inputs": dict_inputs,
        }

    def get_param(self, step_name, param="param"):
        import logging

        if f"{step_name}.{param}" not in self.params:
            logging.error(f"{step_name}.{param} not found as a parameter in Flow.")

            available_params = list(self.params.keys())
            logging.info(f"Available Parameters are: {available_params}")

        return self.params[f"{step_name}.{param}"]


class BenchlingContext:
    """
    conn is a Benchling Connection
    """

    conn = None
    run_tag: Optional[str] = None
    display_tag: Optional[str] = None

    def __init__(self, conn, run_tag: str = None, display_tag: str = None):
        self.conn = conn
        self.run_tag = run_tag
        self.display_tag = display_tag
