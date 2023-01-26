# Author: MetariumProject

# local libraries
from .base import SubstrateScribeUpdater


class SubstrateScribeUpdaterAsScribe(SubstrateScribeUpdater):

    FUNCTION_CALL = "update_scribe_authority_status"