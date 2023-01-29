#!/usr/bin/env python
from flask import Flask, request, jsonify
from waitress import serve
import os
import json

import kubiya
from kubiya.action_store import ActionStore

from typing import Optional, Dict, Any, Union
from pydantic import BaseModel, Json
import traceback


class Request(BaseModel):
    action: Optional[str]
    input:  Union[str, dict, Json[Any], list, bytes]
    secrets: Optional[Dict]
    action_store: Optional[str]
    inbox_id: Optional[str]
    runner: Optional[str]


def execute_handler(request: Request, action_store: ActionStore) -> Any:
    try:
        if request.action == '__KUBIYA_DISCOVER__':
            return {
                "name": action_store.get_name(),
                "version": action_store.get_version(),
                "registered_actions": action_store.get_registered_actions(),
                "secrets": action_store.get_registered_secrets(),
                "kubiya_version": "python-sdk: " + kubiya.__version__,
                "actions_metadata": action_store._action_metadata,
                "icon_url": action_store.icon_url,
            }

        if request.secrets:
            setattr(action_store, "secrets", request.secrets)
        return action_store.execute_action(request.action, request.input)
    except Exception as e:
        return {
            "error": str(e),
            "stacktrace": traceback.format_exc(),
        }


def handle(req, store: ActionStore):
    """handle a request to the function
    Args:
        req (str): request body
    """

    try:
        # data = json.loads(req)
        request = Request.parse_raw(req)

        return {
            "inbox_id": request.inbox_id,
            "runner": request.runner,
            "output": execute_handler(request=request, action_store=store),
        }

    # return req
    except Exception as e:
        return {
            "error": str(e),
            "stacktrace": traceback.format_exc(),
        }
