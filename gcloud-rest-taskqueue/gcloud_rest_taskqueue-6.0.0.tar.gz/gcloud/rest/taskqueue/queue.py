"""
An asynchronous push queue for Google Appengine Task Queues
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from future import standard_library
standard_library.install_aliases()
from builtins import object
import json
import logging
import os
from typing import Any
from typing import AnyStr
from typing import Dict
from typing import IO
from typing import Optional
from typing import Tuple
from typing import Union

from gcloud.rest.auth import SyncSession  # pylint: disable=no-name-in-module
from gcloud.rest.auth import BUILD_GCLOUD_REST  # pylint: disable=no-name-in-module
from gcloud.rest.auth import Token  # pylint: disable=no-name-in-module

# Selectively load libraries based on the package
if BUILD_GCLOUD_REST:
    from requests import Session
else:
    from aiohttp import ClientSession as Session  # type: ignore[assignment]

SCOPES = [
    'https://www.googleapis.com/auth/cloud-tasks',
]

log = logging.getLogger(__name__)


def init_api_root(api_root               )                    :
    if api_root:
        return True, api_root

    host = os.environ.get('CLOUDTASKS_EMULATOR_HOST')
    if host:
        return True, 'http://{}/v2beta3'.format((host))

    return False, 'https://cloudtasks.googleapis.com/v2beta3'


class PushQueue(object):
    #_api_root: str
    #_api_is_dev: bool
    #_queue_path: str

    def __init__(
            self, project     , taskqueue     , location      = 'us-central1',
            service_file                                   = None,
            session                    = None, token                  = None,
            api_root                = None,
    )        :
        self._api_is_dev, self._api_root = init_api_root(api_root)
        self._queue_path = (
            'projects/{}/locations/{}/queues/{}'.format((project), (location), (taskqueue))
        )

        self.session = SyncSession(session)
        self.token = token or Token(
            service_file=service_file, scopes=SCOPES,
            session=self.session.session,  # type: ignore[arg-type]
        )

    def headers(self)                  :
        if self._api_is_dev:
            return {'Content-Type': 'application/json'}

        token = self.token.get()
        return {
            'Authorization': 'Bearer {}'.format((token)),
            'Content-Type': 'application/json',
        }

    def task_name(self, task_id     )       :
        return '{}/tasks/{}'.format((self._queue_path), (task_id))

    # https://cloud.google.com/tasks/docs/reference/rest/v2beta3/projects.locations.queues.tasks/create
    def create(
        self, task                ,
        session                    = None,
        timeout      = 10,
    )       :
        url = '{}/{}/tasks'.format((self._api_root), (self._queue_path))
        payload = json.dumps({
            'task': task,
            'responseView': 'FULL',
        }).encode('utf-8')

        headers = self.headers()

        s = SyncSession(session) if session else self.session
        resp = s.post(url, headers=headers, data=payload,
                            timeout=timeout)
        return resp.json()

    # https://cloud.google.com/tasks/docs/reference/rest/v2beta3/projects.locations.queues.tasks/delete
    def delete(
        self, tname     ,
        session                    = None,
        timeout      = 10,
    )       :
        url = '{}/{}'.format((self._api_root), (tname))

        headers = self.headers()

        s = SyncSession(session) if session else self.session
        resp = s.delete(url, headers=headers, timeout=timeout)
        return resp.json()

    # https://cloud.google.com/tasks/docs/reference/rest/v2beta3/projects.locations.queues.tasks/get
    def get(
        self, tname     , full       = False,
        session                    = None,
        timeout      = 10,
    )       :
        url = '{}/{}'.format((self._api_root), (tname))
        params = {
            'responseView': 'FULL' if full else 'BASIC',
        }

        headers = self.headers()

        s = SyncSession(session) if session else self.session
        resp = s.get(url, headers=headers, params=params,
                           timeout=timeout)
        return resp.json()

    # https://cloud.google.com/tasks/docs/reference/rest/v2beta3/projects.locations.queues.tasks/list
    def list(
        self, full       = False, page_size      = 1000,
        page_token      = '',
        session                    = None,
        timeout      = 10,
    )       :
        url = '{}/{}/tasks'.format((self._api_root), (self._queue_path))
        params                             = {
            'responseView': 'FULL' if full else 'BASIC',
            'pageSize': page_size,
            'pageToken': page_token,
        }

        headers = self.headers()

        s = SyncSession(session) if session else self.session
        resp = s.get(url, headers=headers, params=params,
                           timeout=timeout)
        return resp.json()

    # https://cloud.google.com/tasks/docs/reference/rest/v2beta3/projects.locations.queues.tasks/run
    def run(
        self, tname     , full       = False,
        session                    = None,
        timeout      = 10,
    )       :
        url = '{}/{}:run'.format((self._api_root), (tname))
        payload = json.dumps({
            'responseView': 'FULL' if full else 'BASIC',
        }).encode('utf-8')

        headers = self.headers()

        s = SyncSession(session) if session else self.session
        resp = s.post(url, headers=headers, data=payload,
                            timeout=timeout)
        return resp.json()

    def close(self)        :
        self.session.close()

    def __enter__(self)               :
        return self

    def __exit__(self, *args     )        :
        self.close()
