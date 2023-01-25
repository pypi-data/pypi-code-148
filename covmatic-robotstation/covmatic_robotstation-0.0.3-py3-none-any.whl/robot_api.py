""" API to interface with RobotManager API """
import logging
from abc import ABC, abstractmethod
import requests
import logging


class RobotManagerInterface(ABC):
    """ Common interface for the API towards RobotManager"""
    @abstractmethod
    def action_request(self, action_dict) -> str:
        pass

    @abstractmethod
    def check_action(self, action_id) -> dict:
        pass


class RobotManagerHTTPException(Exception):
    pass


class RobotManagerHTTP(RobotManagerInterface):
    def __init__(self, host: str, logger=None):
        self._host = host
        self._logger = logger or logging.getLogger(self.__class__.__name__)
        self._logger.info("Starting with host {}".format(self._host))

    def action_request(self, action_dict) -> str:
        self._logger.info("Requesting action {}".format(action_dict))
        answer = requests.get(self._get_url_from_action(action_dict))
        self._logger.info("Received answer: {}".format(answer))
        if answer.status_code == 200:
            answer_json = answer.json()
            if "action_id" in answer_json:
                return answer_json["action_id"]
            raise RobotManagerHTTPException("Unexpected answer to action request: {}".format(answer))
        raise RobotManagerHTTPException("Action request {} http code not good: {}".format(action_dict, answer))

    def _get_url_from_action(self, action_dict):
        _url = "http://{host}/action/{action}/{machine}/{position}/{plate_name}".format(host=self._host, **action_dict)
        self._logger.info("Returning url {} for action {}".format(_url, action_dict))
        return _url

    def check_action(self, action_id) -> dict:
        _url = "http://{host}/action/check/{action_id}".format(host=self._host, action_id=action_id)
        answer = requests.get(_url)
        if answer.status_code == 200:
            answer_json = answer.json()
            if "state" in answer_json:
                return answer_json
            raise RobotManagerHTTPException("Check unexpected answer for id {}: {}".format(action_id, answer))
        raise RobotManagerHTTPException("Check id {} has error: {}".format(action_id, answer))


class RobotManagerSimulator(RobotManagerInterface):
    """ Simulation API """
    def __init__(self, *args, **kwargs):
        self._check_count = 0
        self._check_before_finish = 10
        self._logger = logging.getLogger(__name__)
        self._logger.info("{} starting!".format(self.__class__.__name__))
        self._logger.info("Received args: {} and {}".format(args, kwargs))

    def action_request(self, action_dict) -> str:
        self._logger.info("Received action request: {}".format(action_dict))
        return "fakeactionid"

    def check_action(self, action_id) -> dict:
        self._logger.info("Received check request for action id: {}".format(action_id))
        status = "pending"

        self._check_count += 1
        if self._check_count == self._check_before_finish:
            self._check_count = 0
            status = "finished"

        self._logger.info("Returning status {}".format(status))
        return {"status": status}

