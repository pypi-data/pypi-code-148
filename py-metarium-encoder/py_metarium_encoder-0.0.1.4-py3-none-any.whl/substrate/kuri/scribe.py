# Author: MetariumProject

# local libraries
from .base import SubstrateKuriUpdater


class SubstrateKuriUpdaterAsScribe(SubstrateKuriUpdater):

    FUNCTION_CALL = "self_register_content"