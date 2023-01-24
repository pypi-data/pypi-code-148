"""
Copyright (C) 2022 Corsair M360, Inc - All Rights Reserved.
Unauthorized copying of this file, via any medium is strictly prohibited.
Proprietary and confidential.
"""
import traceback
import logging
import docker
import subprocess
import re

from m360 import constants, utils

_logger = logging.getLogger(__name__)

class Maintenance(object):
    """Handles communication with the gateway"""

    _service_name = None
    _service_version = None

    def __init__(self, configuration, app_name, registry, service, awareness):

        self._configuration = configuration
        self._app_name = app_name
        self._registry = registry
        self._service = service
        self._awareness = awareness
        _logger.debug("Maintenance init complete")

    def reload_registry(self, ignore_list=None):
        try:
            res = self._registry.reload()
            self.notify_brothers("/registry/reload", ignore_list)
            return {
                "name": self._app_name,
                "registry": res
            }
        except Exception as e:
            _logger.error(traceback.format_exc())
            raise e

    def reload_awareness(self, ignore_list=None):
        try:
            res = self._awareness.reload(constants.GATEWAY_MAINTENANCE_IP, constants.GATEWAY_MAINTENANCE_PORT, {})
            self.notify_brothers("/awareness/reload", ignore_list)
            return {
                "name": self._app_name,
                "awareness": res
            }
        except Exception as e:
            _logger.error(e)
            raise e

    @staticmethod
    def get_current_ip():
        my_ip = None
        try:
            result = subprocess.run(['hostname', '-i'], stdout=subprocess.PIPE)
            my_ip = re.sub(r"[\n\t\s]*", "", result.stdout.decode('utf-8'))
        except Exception as e:
            _logger.error(e)
        _logger.debug("Found current host ip: " + my_ip)
        return my_ip

    def get_brothers(self, ignore_list):
        """Invokes gateway APIs"""
        ignore_list = ignore_list.copy() if ignore_list else []
        res = {
            "brothers": [],
            "ignoreList": ignore_list
        }
        platform = self._configuration.get("platform")
        # skip logic if not in docker or kube env
        if platform != "docker" and platform != "kubernetes":
            _logger.debug("Skipping get_brothers because platform is: " + platform)
            return res
        pf_options = self._configuration.get("platformOptions")
        if not pf_options or not isinstance(pf_options, dict):
            _logger.error("Missing 'platformOptions' from config: " + str(self._configuration))
            raise Exception("Configuration must specify 'platformOptions' when platform is '" + platform + "'")

        my_ip = self.get_current_ip()
        if my_ip:
            ignore_list.append(my_ip)

        if platform == "kubernetes":
            # ".subsets[].addresses[].ip"
            #
            # TOKEN=$(cat /var/run/secrets/kubernetes.io/serviceaccount/token); \
            # curl https://kubernetes.default.svc/api/v1/namespaces/${namespace}/endpoints/${service-name} \
            #    --header "Authorization: Bearer $TOKEN" --insecure

            # read token from file
            with open(constants.SVC_ACCOUNT_TOKEN_PATH, mode="r", encoding="utf8") as f:
                kube_token = f.read()
            # get sibling IPs
            api_url = "https://kubernetes.default.svc/api/v1/namespaces/" + \
                      self._configuration.get("platformOptions").get("namespace") + "/endpoints/" + \
                      self._configuration.get("platformOptions").get("service")
            api_res = utils.request(url=api_url, headers={"Authorization": "Bearer " + kube_token}, is_json=True).json()

            # extract the hosts ip addresses
            ip_addresses = res.get("brothers")
            if api_res and isinstance(api_res, dict) and api_res.get("subsets") \
                    and isinstance(api_res.get("subsets"), list):
                subsets = api_res.get("subsets")
                for subset in subsets:
                    if subset.get("addresses") and isinstance(subset.get("addresses"), list):
                        addresses = subset.get("addresses")
                        for address in addresses:
                            host_ip = address.get("ip")
                            # if this host entry is not in the ignore_list, then add it
                            if host_ip and host_ip not in ignore_list:
                                ip_addresses.append(host_ip)
            else:
                raise Exception("Invalid Kubernetes API response")
        else:  # platform == "docker":
            # ".[].NetworkSettings.Networks.mike.IPAddress"
            #
            # curl --unix-socket /var/run/docker.sock -X GET \
            # http://v2/containers/json?filters=%7B%22label%22%3A%5B%22com.docker.swarm.service.name%3Dmy_service%22%5D%7D
            ip_addresses = res.get("brothers")
            client = docker.from_env()
            label_filter = "com.docker.swarm.service.name=" + self._configuration.get("platformOptions").get("service")
            network_name = self._configuration.get("platformOptions").get("network")
            containers = client.containers.list(filters={"label": [label_filter]})
            # loop over containers to get their IPs
            try:
                for cont in containers:
                    if cont.attrs["NetworkSettings"] and cont.attrs["NetworkSettings"]["Networks"] \
                            and cont.attrs["NetworkSettings"]["Networks"] \
                            and cont.attrs["NetworkSettings"]["Networks"][network_name]:
                        host_ip = cont.attrs["NetworkSettings"]["Networks"][network_name]["IPAddress"]
                        # if this host entry is not in the ignore_list, then add it
                        if host_ip and host_ip not in ignore_list:
                            ip_addresses.append(host_ip)
            except Exception:
                _logger.error(traceback.format_exc())

        return res

    def notify_brothers(self, endpoint, ignore_list):
        res = self.get_brothers(ignore_list)
        bros = res.get("brothers")
        upd_ignore_list = res.get("ignoreList")
        maintenance_port = self._configuration.get("contract").get("ports").get("maintenance")
        if bros and len(bros) > 0:
            for bro in bros:
                url = "https://" + bro + ":" + str(maintenance_port) + endpoint
                try:
                    utils.request(url=url, query={"ignoreList": upd_ignore_list}, is_json=True)
                except Exception:
                    _logger.error(traceback.format_exc())
                    _logger.error("Call failed to: " + url)
