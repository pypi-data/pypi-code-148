import datetime
import importlib
import logging
import traceback
from pathlib import Path
import yaml
import json

from transportlib.utils import safe_count_csv_rows, write_run_log


def read_config(path_to_config_file):
    with open(path_to_config_file, 'r') as file:
        tasks = yaml.load(file, Loader=yaml.FullLoader)

    logging.info(f"Display config file content:")
    logging.info(json.dumps(tasks, indent=4, sort_keys=True, default=str))

    return tasks


def get_task_by_name(
        tasks,
        target_name,
):
    available_names = []
    task = None
    for candidate_task in tasks:
        candidate_name = candidate_task.get('name')
        available_names.append(candidate_name)

        if target_name == candidate_name:
            task = candidate_task

    if task is None:
        logging.error(f"Cannot find name {target_name}")
        logging.error("Display available names")
        logging.error(json.dumps(available_names, indent=4))
        task = {}

    return task


def execute_config_task(
        task,
        watermark_val_prev,
        watermark_val_curr,
):
    # Start time
    start_time = datetime.datetime.utcnow()
    task_name = task.get('name', '')

    # prepare
    output_folder = Path('output')
    output_folder.mkdir(exist_ok=True, parents=True)

    csv_file_name = task.get('csv_file_name', '')
    csv_file_path = output_folder.joinpath(f'{csv_file_name}.csv')

    if csv_file_path.exists():
        logging.info(f"deleting old file {csv_file_path}")
        csv_file_path.unlink()

    # Get Source Transport
    path_to_source_transport_module = task.get('source_transport', {}).get('path_to_module', '')
    source_transport_name = task.get('source_transport', {}).get('transport_name', '')
    source_transport_kwargs = task.get('source_transport', {}).get('kwargs', {})

    source_transport_kwargs.update(
        {
            'csv_file_path': csv_file_path,
            'watermark_val_prev': watermark_val_prev,
            'watermark_val_curr': watermark_val_curr,
        }
    )

    source_transport_module = importlib.import_module(path_to_source_transport_module)
    source_transport = getattr(source_transport_module, source_transport_name)

    # Get Destination Transport
    path_to_destination_transport_module = task.get('destination_transport', {}).get('path_to_module', '')
    destination_transport_name = task.get('destination_transport', {}).get('transport_name', '')
    destination_transport_kwargs = task.get('destination_transport', {}).get('kwargs', {})
    destination_transport_kwargs.update(
        {
            'csv_file_path': csv_file_path
        }
    )

    destination_transport_module = importlib.import_module(path_to_destination_transport_module)
    destination_transport = getattr(destination_transport_module, destination_transport_name)

    if source_transport is None:
        raise ValueError('No Source Transport is specified!!!')

    if destination_transport is None:
        raise ValueError('No Destination Transport is specified!!!')

    # Run Source
    try:
        source_transport(**source_transport_kwargs).run()
        destination_transport(**destination_transport_kwargs).run()
    except Exception as e:
        status = 'error'
        stacktrace = traceback.format_exc()
        logging.error(stacktrace)
    else:
        stacktrace = None
        status = 'success'


    # Write log
    finish_time = datetime.datetime.utcnow()
    num_rows = safe_count_csv_rows(csv_file_path=csv_file_path)
    num_items = num_rows - 1 if num_rows != 0 else 0

    write_run_log(task_name=task_name,
                  start_time=start_time,
                  finish_time=finish_time,
                  num_items=num_items,
                  status=status,
                  stacktrace=stacktrace
                  )

    logging.info('Log written successfully')

