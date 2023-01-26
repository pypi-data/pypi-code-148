from typing import Any
from CxAdmin.api import CxItem


class CxEnvironment(CxItem):
    def getTenant(self) -> Any:
        raise NotImplementedError()

    def getRegions(self) -> Any:
        raise NotImplementedError()

    def get(self) -> Any:
        return self._httpClient.get(self._path).json()
