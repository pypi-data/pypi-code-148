from typing import Dict, Any, Callable
import functools


def adapt(inputs: Dict[str, Any], rules: Dict[str, str] = {}) -> Dict[str, Any]:
    outputs = inputs
    if rules:
        outputs = {
            new_key: inputs[old_key]
            for new_key, old_key in rules.items()
        }
    return outputs


class Adapter:

    def __init__(self, in_rules: Dict[str, str] = {}, out_rules: Dict[str, str] = {}) -> None:
        self._in_rules = in_rules
        self._out_rules = out_rules

    def __call__(self, func: Callable):
        @functools.wraps(func)
        def f(**kwargs) -> Dict[str, Any]:
            new_kwargs = adapt(kwargs, self._in_rules)
            outputs = func(**new_kwargs)
            assert isinstance(outputs, dict)
            new_outputs = adapt(outputs, self._out_rules)
            return new_outputs
        return f
