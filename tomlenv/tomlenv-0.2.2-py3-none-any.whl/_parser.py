import ast
import copy
import dataclasses
import os
import pathlib
import tomllib
from datetime import date, datetime, time
from os import path
from typing import Any

_LIBRARY_PREFIX = "TOMLENV_"
CONF_FILEPATH_KEY = _LIBRARY_PREFIX + "CONF_FILEPATH"


class ConfigError(ValueError):
    """An error raised if no valid configuration was found."""


class DataclassError(ValueError):
    """An error raised if the target object is not a dataclass."""


class ParseError(RuntimeError):
    """An error raised if configuration is not parsable."""


class Parser:
    def __init__(self):
        self._filepath = ""
        self._environ = {}

    def load(self, obj: object, env: dict[str, Any] = None):
        """
        Searches for configs in toml files and the environment
        and loads matching keys into the fields of obj.

        Environment values override toml file configs.
        """
        if not dataclasses.is_dataclass(obj):
            raise DataclassError(f"Object is not a dataclass, has type: {type(obj)}")

        if not self._filepath:
            default_path = path.join(os.getcwd(), "config.toml")

            config_path = pathlib.Path(os.getenv(CONF_FILEPATH_KEY, default_path))
            if not config_path.is_absolute():
                config_path = (pathlib.Path(os.getcwd()) / config_path).absolute()

            try:
                os.stat(config_path)
            except FileNotFoundError:
                raise ConfigError(
                    f"No config file found at '{config_path}', try setting '{CONF_FILEPATH_KEY}'"
                )
            self._filepath = config_path

        if not self._environ:
            if not env:
                self._environ = copy.deepcopy(os.environ)
            else:
                self._environ = copy.deepcopy(env)

        toml = ""
        with open(file=self._filepath, mode="r", encoding="utf-8") as f:
            toml = f.read()

        raw_config = self._build_raw_config(toml, self._environ)
        self._load_raw_config(obj, raw_config)

    def _build_raw_config(self, toml: str, environ: dict[str, Any]) -> dict[str, Any]:
        """Create a raw configuration dict from a toml file and an environment."""
        try:
            config = tomllib.loads(toml)
        except TOMLDecodeError as err:
            raise ParseError(f"Unable to parse TOML file") from err

        for env_key, env_val in environ.items():
            if env_key == CONF_FILEPATH_KEY:
                continue
            if not env_key.startswith(_LIBRARY_PREFIX):
                continue

            key = env_key.removeprefix(_LIBRARY_PREFIX).lower()
            orig_val = config.get(key)
            if orig_val is None:
                continue

            if type(orig_val) in [list, dict]:
                config[key] = ast.literal_eval(env_val)
            elif type(orig_val) in [datetime, date]:
                try:
                    datetime_match = tomllib._re.RE_DATETIME.match(env_val)
                    config[key] = tomllib._re.match_to_datetime(datetime_match)
                except ValueError as err:
                    raise ParseError(
                        f"Invalid date or datetime, key: {env_key}"
                    ) from err
            elif type(orig_val) is time:
                try:
                    localtime_match = tomllib._re.RE_LOCALTIME.match(env_val)
                    config[key] = tomllib._re.match_to_localtime(localtime_match)
                except ValueError as err:
                    raise ParseError(f"Invalid time, key: {env_key}") from err
            elif type(orig_val) is bool:
                if env_val.lower().startswith("true") or env_val == "1":
                    config[key] = True
                elif env_val.lower().startswith("false") or env_val == "0":
                    config[key] = False
                else:
                    raise ParseError(f"Invalid bool, key: {env_key}") from err
            else:
                config[key] = env_val

        return config

    def _load_raw_config(self, obj: object, raw_conf: dict[str, Any]):
        """Load configurations from path and environment."""
        if not dataclasses.is_dataclass(obj):
            raise DataclassError("object is not a dataclass")

        raw_conf_keys = raw_conf.keys()
        fields = [(field.name, field.type) for field in dataclasses.fields(obj)]

        for (name, typ) in fields:
            if name not in raw_conf_keys:
                continue

            obj.__setattr__(name, raw_conf[name])
