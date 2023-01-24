from enum import Enum


class OrganizationsSwitches(str, Enum):
    Organizations = "organizations manager"
    OrganizationsIssuer = "organizations issuer manager"
    OrganizationsIntermediary = "organizations intermediary manager"


class NetworksNames(str, Enum):
    AlastriaDefaultName = "Alastria"
    LacchainDefaultName = "Lacchain"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)
