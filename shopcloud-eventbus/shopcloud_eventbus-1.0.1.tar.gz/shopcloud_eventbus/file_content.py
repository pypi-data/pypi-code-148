requirements_txt = """google-cloud-tasks
python-dateutil
pytz
google-cloud-logging
"""

main_py = """import base64
import json
import logging
import os
from base64 import b64encode
from flask import jsonify

import dateutil.parser
import google.cloud.logging
import pytz
from google.cloud import tasks_v2
from google.cloud.tasks_v2.types import HttpMethod as TaskHttpMethod
from google.protobuf import timestamp_pb2

log_client = google.cloud.logging.Client()
log_client.get_default_handler()
log_client.setup_logging()


def create_task_for_pipeline(queue, endpoint, **kwargs):
    body = kwargs.get('body')
    start_at = kwargs.get('start_at')
    if start_at is not None:
        start_at = dateutil.parser.parse(start_at)

    #
    ## Required for HttpMethod
    #
    # https://googleapis.dev/python/cloudtasks/latest/tasks_v2/types.html#google.cloud.tasks_v2.types.HttpMethod

    method_dict = {
        "POST": 1,
        "GET": 2,
        "HEAD": 3,
        "PUT": 4,
        "DELETE": 5,
        "PATCH": 6,
        "OPTIONS": 7,
        "HTTP_METHOD_UNSPECIFIED": 0,
    }

    task_http_method = TaskHttpMethod(method_dict.get(kwargs.get('http_method', 'POST'), 1))
    task = {
        'http_request': {
            'http_method': task_http_method,
            'url': endpoint,
            'headers': {
                'Content-type': 'application/json',
                'Authorization': "Basic {}".format(
                    b64encode("{}:{}".format(
                        os.environ.get('API_AUTH_USER'),
                        os.environ.get('API_AUTH_PWD'),
                    ).encode("utf-8")).decode("ascii")
                ),
            },
        },
    }

    # request-body only allowed for "POST", "PUT" or "PATCH"
    if task_http_method.name in ["POST", "PUT", "PATCH"]:
        task["http_request"]["body"] = json.dumps(body).encode('utf-8')

    if start_at is not None:
        timestamp = timestamp_pb2.Timestamp()
        timestamp.FromDatetime(start_at.astimezone(pytz.utc))
        task['schedule_time'] = timestamp

    client = tasks_v2.CloudTasksClient()
    parent = client.queue_path(
        project=os.environ.get('TASK_PROJECT'),
        location=os.environ.get('TASK_LOCATION'),
        queue=queue,
    )
    response = client.create_task(parent=parent, task=task)


def main(event, context):
    try:
        if event.get('cloud-tasks') is not None:
            for task in event.get('cloud-tasks', []):
                url = task.get('http_request', {}).get('url')
                create_task_for_pipeline(
                    task.get('queue', 'cloud-tasks-default'),
                    '{}{}'.format(
                        os.environ.get('API_ENDPOINT'),
                        "{}{}".format(
                            "" if url.startswith('/') else "/",
                            url
                        )
                    ),
                    body=task.get('http_request', {}).get('body', None),
                    start_at=task.get('start_at'),
                    http_method=task.get('http_request', {}).get('http_method', 'POST')
                )
    except Exception as e:
        logging.error('exception: {}'.format(e))
        raise e


def main_pub_sub(event, context):
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    data = json.loads(pubsub_message)
    text_payload = data.get('textPayload', '')
    event = json.loads(text_payload[11:])
    logging.info("receive event {}".format(json.dumps(event)))
    main(event, context)


def main_http(request):
    if request.method == 'GET':
        return 'OK'
    elif request.method == 'POST':
        event = request.get_json(silent=True)
        main(event, request)
        return jsonify({'status': 'ok'})

"""
