"""
To manage devices
"""

import pandas as pd

from preheat_open.building_unit import BaseBuildingUnit

from .data import load_box_data
from .helpers import now, sanitise_datetime_input, timedelta


class Device(BaseBuildingUnit):
    """
    A device is a grouping of signals originating from a single physical data source (device),
    which is not linked to the building model
    """

    def __init__(self, unit_type: str, unit_data: dict, building_ref):
        unit_data_reshaped = {
            "coversBuilding": True,
            "zoneIds": [],
            "shared": False,
            "id": unit_data["id"],
            "name": unit_data["name"],
        }
        for c in unit_data["components"]:
            unit_data_reshaped[c["name"]] = c

        super().__init__(
            unit_type, unit_data_reshaped, building_ref, load_data_by="cid"
        )

    def describe(
        self, display: bool = True, prefix: str = "", components: bool = True, **kwargs
    ):
        return super().describe(
            display=display,
            prefix=prefix,
            components=components,
            show_subtype=False,
            **kwargs
        )

    def load_state(self, seconds_back: int = 300, t_now=None) -> None:
        t_now = now() if t_now is None else sanitise_datetime_input(t_now)
        # Check if recent enough to expect raw data
        if t_now > now() - timedelta(days=7):
            resolution = "raw"
        else:
            resolution = "minute"
        self._state = load_box_data(
            self.get_all_component_cids(),
            t_now - timedelta(seconds=seconds_back),
            t_now,
            resolution,
        )

    def get_state(
        self,
        update: bool = False,
        estimate: str = "last",
        seconds_back: int = 300,
        t_now=None,
    ) -> pd.Series:
        return super().get_state(
            update=update,
            estimate=estimate,
            seconds_back=seconds_back,
            t_now=t_now,
            by="cid",
        )
