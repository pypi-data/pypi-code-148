from .abstractions import AFactory, AContext
from .strategy import AlastriaNetworkStrategy, LacchainNetworkStrategy
from .context import Context
from organizations.enums import NetworksNames
from .models import FactoryArgsModel


class Creator(AFactory):
    @staticmethod
    def create_object(props: FactoryArgsModel) -> AContext:

        if props.net.name == NetworksNames.AlastriaDefaultName:
            return Context(AlastriaNetworkStrategy(props))
        if props.net.name == NetworksNames.LacchainDefaultName:
            return Context(LacchainNetworkStrategy(props))
        raise Exception("Cant find any strategy.")
