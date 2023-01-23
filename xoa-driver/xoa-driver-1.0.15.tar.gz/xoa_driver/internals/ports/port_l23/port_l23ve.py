import functools
from typing import TYPE_CHECKING
from .bases.port_l23 import BasePortL23
from .bases.port_reception_statistics import PortReceptionStatistics
from .bases.port_transmission_statistics import PortTransmissionStatistics

from xoa_driver.internals.core.commands import (
    P_MDIXMODE,
    # P_ENGINENAMES, #TODO: need to implement
    # P_ENGINELOAD, #TODO: need to implement
)
if TYPE_CHECKING:
    from xoa_driver.internals.core import interfaces as itf
from xoa_driver.internals.utils import attributes as utils
from xoa_driver.internals.utils.indices import index_manager as idx_mgr
from xoa_driver.internals.indices.streams.base_stream import BaseStreamIdx
from xoa_driver.internals.indices.filter.base_filter import BaseFilterIdx
from xoa_driver.internals.state_storage import ports_state

VEStreamIndices = idx_mgr.IndexManager[BaseStreamIdx]
VEFilterIndices = idx_mgr.IndexManager[BaseFilterIdx]

class Engine:
    def __init__(self, conn: "itf.IConnection", module_id: int, port_id: int) -> None:
        # self.names = P_ENGINENAMES(conn, module_id, port_id)
        # self.load = P_ENGINELOAD(conn, module_id, port_id)
        ...

class PortStatistics:
    """L23 VE port statistics"""

    def __init__(self, conn: "itf.IConnection", module_id: int, port_id: int) -> None:
        self.rx = PortReceptionStatistics(conn, module_id, port_id)
        """L23 VE port's RX statistics."""
        
        self.rx = PortTransmissionStatistics(conn, module_id, port_id)
        """L23 VE port's TX statistics."""

class PortL23VE(BasePortL23):
    """L23 VE port"""

    def __init__(self, conn: "itf.IConnection", module_id: int, port_id: int) -> None:
        super().__init__(conn, module_id, port_id)

        self._local_states = ports_state.PortL23LocalState()
        
        self.mdix_mode = P_MDIXMODE(conn, module_id, port_id)
        """MDI/MDIX mode.
        Representation of P_MDIXMODE
        """

        self.engine = Engine(conn, module_id, port_id)
        """Engine is not supported yet."""
        
        self.statistics = PortStatistics(conn, module_id, port_id)
        
        self.streams: VEStreamIndices = idx_mgr.IndexManager(
            conn, 
            BaseStreamIdx, 
            module_id, 
            port_id
        )
        """L23 VE port's stream index manager."""

        self.filters: VEFilterIndices = idx_mgr.IndexManager(
            conn, 
            BaseFilterIdx, 
            module_id, 
            port_id
        )
        """L23 VE port's filter index manager."""
    
    @property
    def info(self) -> ports_state.PortL23LocalState:
        return self._local_states
    
    async def _setup(self):
        await self._local_states.initiate(self)
        self._local_states.register_subscriptions(self)
        return self
    
    on_mdix_mode_change = functools.partialmethod(utils.on_event, P_MDIXMODE)
    """Register a callback to the event that the port's MDI/MDIX mode changes."""