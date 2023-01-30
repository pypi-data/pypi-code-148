from superlogica.sl_builder import SuperlogicaBuilder
from superlogica.orquestrador import Orchestrator

class Connection:
    def __init__(self, parameters) -> None:
        self.parameters = parameters
        self.director = Orchestrator()
        self.builder = SuperlogicaBuilder()
        self.director.builder = self.builder

    def get(self, pages):
        self.director.build_conector(parameters=self.parameters)
        return self.builder.conector.results(pages=pages)