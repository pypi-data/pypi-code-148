import json
from typing import Any
from typing import Callable
from typing import List
from typing import Optional
from typing import Type

import boto3
import yaml
from mypy_boto3_appconfigdata.client import AppConfigDataClient
from mypy_boto3_kms.client import KMSClient
from sitri import Sitri
from sitri.providers.base import ConfigProvider
from sitri.providers.base import PathModeStateProvider
from sitri.providers.contrib.system import SystemConfigProvider
from sitri.providers.contrib.yaml import YamlConfigProvider
from sitri.strategy.index_priority import IndexPriorityStrategy


system = SystemConfigProvider(prefix="TWO")

yaml = YamlConfigProvider(yaml_path="./data.yaml", default_separator="/")
strategy = IndexPriorityStrategy([system, yaml])


class AwsAppConfigProvider(PathModeStateProvider, ConfigProvider):
    """Config provider for AWS AppConfig storage."""

    provider_code = "app_config"
    path_seperator = "."
    client: AppConfigDataClient

    def __init__(
        self,
        application: str,
        environment: str,
        profile: str,
        update_interval: int = 300,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """
        :param vedis_connector: return connection to vedis
        :param hash_name: name for hash (key-value object) in vedis
        """
        super().__init__(*args, **kwargs)

        self.application = application
        self.environment = environment
        self.profile = profile
        self.update_interval = update_interval

        self._poll_interval = None
        self._next_config_token = None

        self._time_last_updated = None
        self._boto3_app_config_client_instance = None
        self._config = None
        self._raw_config = None
        self._content_type = None

        self._init_configuration()

    @property
    def client(self) -> AppConfigDataClient:
        if self._boto3_app_config_client_instance is None:
            self._boto3_app_config_client_instance = boto3.client("appconfigdata")
        return self._boto3_app_config_client_instance

    def _init_configuration(self):
        resp = self.client.start_configuration_session(
            ApplicationIdentifier=self.application,
            ConfigurationProfileIdentifier=self.profile,
            EnvironmentIdentifier=self.environment,
            RequiredMinimumPollIntervalInSeconds=self.update_interval,
        )
        self._next_config_token = resp["InitialConfigurationToken"]

    def _update_configuration(self):
        response = self.client.get_latest_configuration(
            ConfigurationToken=self._next_config_token,
        )
        self._next_config_token = response["NextPollConfigurationToken"]
        self._poll_interval = int(response["NextPollIntervalInSeconds"])
        self._time_last_updated = response["LastUpdatedTime"]
        content = response["Configuration"].read()  # type: bytes
        if content == b"":
            return False

        if response["ContentType"] == "application/x-yaml":
            try:
                self._config = yaml.safe_load(content)
            except yaml.YAMLError as error:
                message = "Unable to parse YAML configuration data"
                if hasattr(error, "problem_mark"):
                    message = (
                        f"{message} at line {error.problem_mark.line + 1} "
                        f"column {error.problem_mark.column + 1}"
                    )
                raise ValueError(message) from error
        elif response["ContentType"] == "application/json":
            try:
                self._config = json.loads(content.decode("utf-8"))
            except json.JSONDecodeError as error:
                raise ValueError(error.msg) from error
        elif response["ContentType"] == "text/plain":
            self._config = content.decode("utf-8")
        else:
            self._config = content

        self._raw_config = content
        self._content_type = response["ContentType"]
        return True

    def get(
        self,
        key: str,
        path_mode: Optional[bool] = None,
        separator: Optional[str] = None,
        **kwargs,
    ) -> Optional[Any]:
        """Get value from config.

        :param key: key or path for search
        :param path_mode: boolean mode switcher
        :param separator: separator for path keys in path mode
        """
        separator = separator if separator else self.path_seperator

        if self._get_path_mode_state(path_mode):
            return self._get_by_path(key, separator=separator)

        try:
            value = self._config[key]
        except KeyError:
            value = None
        return value

    def _get_by_path(self, path: str, separator: str) -> Any:
        """Retrieve value from a dictionary using a list of keys.

        :param path: string with separated keys
        """
        dict_local = self._config.copy()
        keys = path.split(separator)

        for key in keys:
            try:
                dict_local = dict_local[int(key)] if key.isdigit() else dict_local[key]
            except Exception:
                if key not in dict_local.keys():
                    return None

                dict_local = dict_local[key]
        return dict_local

    def keys(
        self,
        path_mode: bool = False,
        separator: Optional[str] = None,
        **kwargs: Any,
    ) -> List[str]:
        """Keys in config.

        :param path_mode: [future] path mode for keys list
        :param separator: [future] separators for keys in path mode
        """
        if not path_mode:
            return list(self._config.keys())
        raise NotImplementedError("Path-mode not implemented!")


# ENV = system.get("env")

# conf = Sitri(
#     config_provider=,
# )

# print(system.get_config("host"))
# # Output: example.com

# print(system.config.keys())
# # Output: ["host", "password"]


# yaml.get("test.test_key1", ":(")
# # Output: :(

# yaml.get("test.test_key1", ":(", path_mode=True)
# # Output: :(

# yaml.get("test.test_key1", ":(", path_mode=True, separator=".")
# # Output: 1

# yaml.get("test/test_key1", ":(", path_mode=True)
# # Output: 1

# yaml.get("test0")
# # Output: 0
