from dataclasses import dataclass
from typing import (
    Any,
    Dict,
    List,
    NewType,
)

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Workflow:
    name: str
    args: Dict[str, Any]


@dataclass_json
@dataclass
class Mapping:
    target: str
    triggers: List[Workflow]


MappingDict = NewType("MappingDict", Dict[str, Dict[str, Workflow]])


if __name__ == "__main__":
    mp = {
        "type": "mapping",
        "target": "GreetingWorkflow",
        "triggers": [{"name": "TriggerWorkflow", "args": {"name": "@"}}],
    }
    wf = {"type": "workflow", "name": "TriggerWorkflow", "args": {"name": "Workflow Team"}}
    m = Mapping.from_dict(mp)
    w = Workflow.from_dict(wf)
    print(m)
    print(w)
