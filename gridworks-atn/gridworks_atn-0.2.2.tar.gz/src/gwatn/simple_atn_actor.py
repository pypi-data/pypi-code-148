import logging
import time
from typing import Optional

import dotenv
import gridworks.algo_utils as algo_utils
from algosdk.v2client.algod import AlgodClient
from beaker.client import ApplicationClient
from gridworks.algo_utils import BasicAccount
from gridworks.enums import GNodeRole

import gwatn.config as config
from gwatn import DispatchContract
from gwatn.atn_actor_base import AtnActorBase
from gwatn.types import LatestPrice
from gwatn.types import SimTimestep


LOG_FORMAT = (
    "%(levelname) -10s %(sasctime)s %(name) -30s %(funcName) "
    "-35s %(lineno) -5d: %(message)s"
)
LOGGER = logging.getLogger(__name__)


class SimpleAtnActor(AtnActorBase):
    """Simple implementation of an AtnActor, for testing purposes"""

    def __init__(
        self,
        settings: config.AtnSettings = config.AtnSettings(
            _env_file=dotenv.find_dotenv()
        ),
    ):
        super().__init__(settings=settings)
        LOGGER.info("Simple Atn Initialized")

    def latest_price_from_market_maker(self, payload: LatestPrice) -> None:
        pass

    def new_timestep(self, payload: SimTimestep) -> None:
        """Set to work with a timestep per minute"""

        # sends a hb to Scada every minute for DispatchContract
        self.hb_to_scada()

    def repeat_timestep(self, payload: SimTimestep) -> None:
        pass
