from abc import ABC, abstractmethod
from typing import Any, Dict

from vtorch.data.iterators.data_iterator import BaseDataIterator


class InterruptableDataIterator(BaseDataIterator, ABC):
    @abstractmethod
    def state_dict(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def load_state_dict(self, state_dict: Dict[str, Any]) -> None:
        pass
