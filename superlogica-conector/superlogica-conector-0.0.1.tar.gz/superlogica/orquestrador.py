from __future__ import annotations
from superlogica.buider import Builder

class Orchestrator:
    
    def __init__(self) -> None:
        self._builder = None

    @property
    def builder(self) -> Builder:
        return self._builder

    @builder.setter
    def builder(self, builder: Builder) -> None:
        self._builder = builder

    def build_conector(self, parameters) -> None:
        token = parameters['token']
        api_key = parameters['api_key']
        object_ = parameters['object']
        kargs = parameters['args']

        self.builder.auth(token=token, api_key= api_key)
        self.builder.configs(object=object_, **kargs)