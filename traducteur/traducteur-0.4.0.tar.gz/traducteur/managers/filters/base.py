from typing import Dict
from ...models.base import BaseModel
from .types.base import BaseTypeFilter


class BaseFilter(BaseModel):
    def for_query(self) -> Dict[str, BaseTypeFilter]:
        d = self.dict()
        return {k: getattr(self, k) for k in d.keys()}
