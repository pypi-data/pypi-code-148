import dataclasses
from typing import List, Union, Dict, Optional

from vatis.asr_commons.json.deserialization import JSONDeserializable


@dataclasses.dataclass(frozen=True)
class SpokenCommandConfig(JSONDeserializable):
    command: str
    regex: List[str]
    enabled: bool

    @staticmethod
    def from_json(json_dict: dict):
        return SpokenCommandConfig(**json_dict)


class CommandsExpressions:
    def __init__(self, expressions: Union[str, Dict[str, List[str]], List[SpokenCommandConfig]] = None):
        if expressions is None:
            self._expressions: Dict[str, List[str]] = {}
        elif isinstance(expressions, str):
            self._expressions: Dict[str, List[str]] = CommandsExpressions._parse_tsv_string(expressions)
        elif isinstance(expressions, dict):
            self._expressions: Dict[str, List[str]] = expressions.copy()
        elif isinstance(expressions, list):
            self._expressions: Dict[str, List[str]] = self._parse_command_config_list(expressions)
        else:
            raise ValueError(f'Unsupported type: {type(expressions)}')

    @staticmethod
    def _parse_tsv_string(tsv_str: str) -> Dict[str, List[str]]:
        expressions: Dict[str, List[str]] = {}

        for line in tsv_str.split('\n'):
            tokens = line.split('\t')
            expressions[tokens[0]] = tokens[1:]

        return expressions

    @staticmethod
    def _parse_command_config_list(expressions: List[SpokenCommandConfig]) -> Dict[str, List[str]]:
        parsed_expressions: Dict[str, List[str]] = {}

        for command_config in expressions:
            if not isinstance(command_config, SpokenCommandConfig):
                raise ValueError(f'Bad type: {type(command_config)}')

            if command_config.command not in parsed_expressions:
                parsed_expressions[command_config.command] = command_config.regex.copy()
            else:
                raise ValueError(f'Duplicate command: {command_config.command}')

        return parsed_expressions

    def get(self, key: str) -> List[str]:
        expressions: Optional[List[str]] = self._expressions.get(key, [])

        if expressions is None:
            expressions = []

        return expressions

    def get_commands(self) -> List[str]:
        return [command for command in self._expressions]
