from dataclasses import dataclass, field
from typing import Optional, List, Self, Dict


@dataclass
class PluginContext:
    localized_resources: Dict[str, str]
    path: Optional[str] = None
    children: List[List[Self]] = field(default_factory=list)
