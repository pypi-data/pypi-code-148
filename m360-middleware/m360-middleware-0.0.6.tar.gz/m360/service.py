"""
Copyright (C) 2022 Corsair M360, Inc - All Rights Reserved.
Unauthorized copying of this file, via any medium is strictly prohibited.
Proprietary and confidential.
"""

import os
import copy
import json
import socket
import logging

from m360 import constants, utils

_logger = logging.getLogger(__name__)

class Service(object):
    """Offers service related helper methods"""

    # singleton
    _instance = None

    def __init__(self):
        _logger.debug("Service created")

    @staticmethod
    def service_singleton():
        """Access the singleton receiver"""

        if Service._instance:
            return Service._instance

        if not Service._instance:
            _logger.debug("Creating service instance")
            Service._instance = Service()

        return Service._instance

    @staticmethod
    def __load_contract(path_or_obj):
        """
        Load the contract dict either from a path with a JSON file or just clone the passed dict
        @param path_or_obj  {Union[dict, str]}  Either a contract dict or a path to a JSON file containing the data
        @returns {dict} The contract object
        """
        if not path_or_obj or (type(path_or_obj) is str and not path_or_obj.strip()):
            _logger.error("Missing Service Contract!")
            raise Exception("Missing Service Contract!")

        if type(path_or_obj) is str:
            contract = utils.json_file_to_dict(path_or_obj)
            if not contract or (type(contract) is dict and len(contract.keys()) == 0):
                _logger.error("Invalid service contract found in the provided file!")
                raise Exception("Invalid service contract found in the provided file!")
        else:
            try:
                contract = copy.deepcopy(path_or_obj)
            except Exception as e:
                _logger.error(e)
                raise Exception("Unable to parse the service contract that you provided as a JSON object!")
        return contract

    @staticmethod
    def __make_request(*, method="get", path, headers=None, body=None, limit):
        """
        Utility method to make calls to APIs for this specific class
        """
        # build url
        url = constants.GATEWAY_MAINTENANCE_IP
        if (":" + str(constants.GATEWAY_MAINTENANCE_PORT)) not in url:
            url += ":" + str(constants.GATEWAY_MAINTENANCE_PORT)
        url += path
        if "https://" not in url:
            url = "https://" + url

        # make request with retry strategy
        delay = 0.001 if constants.MW_TESTING else 5
        res = utils.retry_request(method=method, url=url, is_json=True, retries=(limit - 1), retry_delay=delay,
                                  headers=headers, body=body).json()
        return res.get("data")

    @staticmethod
    def get(path_or_obj):
        """
        Fetches the JSON copy that represents the service as it's registered in the API gateway
        @param path_or_obj  {Union[dict, str]}  Either a contract dict or a path to a JSON file containing the data
        @returns {dict} API call response
        """
        # load contract data
        contract = Service.__load_contract(path_or_obj)
        # call API
        return Service.__make_request(path="/service", limit=3, headers={"service": contract.get("name"),
                                                                         "version": str(contract.get("version"))})

    @staticmethod
    def register(path_or_obj, ip, config):
        """
        Formulates a payload from provided parameters and makes a POST request call to the gateway maintenance API
        to register the service.
        @param path_or_obj  {Union[dict, str]}  Either a contract dict or a path to a JSON file containing the data
        @param ip           {str}
        @param config       {dict}
        @returns {dict} API call response
        """
        # load contract data
        contract = Service.__load_contract(path_or_obj)
        # check IP
        if not ip or (type(ip) is str and not ip.strip()):
            _logger.error("Missing IP Address Value!")
            raise Exception("Missing IP Address Value!")

        if config and (type(config) is dict and config.get("platform") == "kubernetes"):
            if not config.get("platformOptions"):
                raise Exception("Missing 'platformOptions' in config")
            if not contract.get("ports"):
                contract["ports"] = {}
            exposed_port = config.get("platformOptions").get("exposedPort")
            contract["ports"]["data"] = exposed_port
            contract["ports"]["maintenance"] = exposed_port

        contract["host"] = {
            "weight": int(contract.get("host").get("weight")) if contract.get("host") and contract.get("host").get(
                "weight") else 1,
            "hostname": socket.gethostname(),
            "ip": ip
        }

        # call API
        return Service.__make_request(method="post", path="/service/register", limit=3, body=contract)

    @staticmethod
    def ensure_ip_address(config):
        """
        Ensures that the provided IP address value in the configuration object is based on the platform being used
        @param config   {dict}
        @returns {bool} API call response
        """
        if not config or type(config) is not dict:
            _logger.error("Invalid configuration")
            raise Exception("Invalid configuration")

        # if the platform hosting the microservice is kubernetes, the IP address is provided as an env variable
        # we do not ping the ip address because it will not be reachable from the pod
        if config.get("platform") == "kubernetes":
            return True

        # otherwise, ping the ip address and get the numeric_host from the response.
        # This works for manual deployment and other deployment.
        # This also works for docker deployment
        #      IF CONFIGURATION.IP EQUALS THE NAME OF THE DOCKER SWARM SERVICE
        # TODO: make sure the below works and is equivalent to the description above
        domain = config.get("ip").replace("http:", "").replace("https:", "").replace("/", "")
        _logger.debug("Getting IP address for domain: " + domain)
        ip = socket.gethostbyname(domain)
        _logger.debug("Domain's IP address is: " + ip)
        if ip:
            config["ip"] = ip

        return True

    @staticmethod
    def get_endpoint_info(request):
        """
        This method returns the request endpoint information that was detected by the gateway and injected in the
        headers
        @param request   {dict}
        @returns {dict}
        """
        if not request:
            return None
        headers = utils.get_req_headers(request)
        if not headers or not headers.get("m360"):
            return None
        try:
            m360 = headers.get("m360")
            if m360:
                m360 = utils.from_json(m360)
                return m360.get("API")
            return None
        except Exception as e:
            _logger.error(e)
            return None


def instance():
    """Get the singleton instance of the service"""
    _logger.debug("calling service_instance, os.pid=%d", os.getpid())
    return Service.service_singleton()
