# Author: MetariumProject

# local libraries
from .base import SubstrateScribeUpdater


class SubstrateScribeUpdaterAsRoot(SubstrateScribeUpdater):

    FUNCTION_CALL = "force_update_scribe_authority_status"
