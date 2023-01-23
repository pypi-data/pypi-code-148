from typing import List
from typing import Optional

import gridworks.conversion_factors as cf
import numpy as np
import pendulum
from pydantic import BaseModel

import gwatn.errors as errors
import gwatn.property_format as property_format
import gwatn.utils as utils
from gwatn.data_classes import MarketType
from gwatn.enums import EmitterPumpFeedbackModel
from gwatn.enums import MixingValveFeedbackModel
from gwatn.schemata import AtnBid
from gwatn.schemata import AtnParamsHeatpumpwithbooststore as AtnParams
from gwatn.schemata import FloParamsHeatpumpwithbooststore as FloParams
from gwatn.schemata import FloParamsHeatpumpwithbooststore_Maker as FloParams_Maker
from gwatn.schemata import MarketSlot
from gwatn.schemata import MarketTypeGt_Maker
from gwatn.schemata import PriceQuantityUnitless
from gwatn.strategies.heatpumpwithbooststore.flo import (
    HeatPumpWithBoostStore__Flo as Flo,
)


DUMMY_ALGO_TXN = "gqNzaWfEQNPXbrAiWd+cNgsIaM3N0PSu3repauvmjuHmoKjh6sd3L5U4/YpovcXN7/ATH1LgcI4cgV+SU3VQ6bsm/gfAOQyjdHhuiaNhbXTNB9CjZmVlzQPoomZ2HaNnZW6qc2FuZG5ldC12MaJnaMQgaJXPYTdWaeTNSs8FMMzPNfV7SrHXqJgFsJLxRbSPjzCibHbNBAWjcmN2xCBWkH3PValty0Rb0cyZo69Alhp4IbNKFnhXtgJ++A9EzKNzbmTEIOJPEbccL6IqmeBeaLzbLav25U9jBMjloaIyF1eY9HFxpHR5cGWjcGF5"


class DijkstraChoice(BaseModel):
    PowerImportedKw: float
    NextNodeCostDollars: float


class CostAndQuantityBought(BaseModel):
    QuantityBought: float
    Cost: float


class SlotStuff(BaseModel):
    Slot: MarketSlot
    BidParams: Optional[FloParams] = None
    Flo: Optional[Flo] = None
    Bid: Optional[AtnBid] = None
    Price: Optional[float] = None


def dummy_bid() -> AtnBid:
    return AtnBid(
        BidderAlias="d1.isone.dummy.ta",
        BidderGNodeInstanceId="00000000-0000-0000-0000-000000000000",
        MarketSlotName="rt60gate30b.d1.isone.ver.keene.1577836800",
        BidList=[],
        SignedMarketFeeTxn=DUMMY_ALGO_TXN,
    )


def dummy_slot_stuff(slot: MarketSlot) -> SlotStuff:
    return SlotStuff(
        Slot=slot, FloStartIdx=50, BidParams=dummy_flo_params(), AtnBid=dummy_bid()
    )


def is_dummy_slot_stuff(bid_stuff: SlotStuff) -> bool:
    if is_dummy_flo_params(bid_stuff.BidParams):
        return True
    return False


def name_from_market_slot(slot: MarketSlot) -> str:
    return f"{slot.Type.Name.value}.{slot.MarketMakerAlias}.{slot.StartUnixS}"


def market_slot_from_name(market_slot_name: str) -> MarketSlot:
    """rt60gate30b.d1.isone.ver.keene.1577836800"""
    if not property_format.is_market_slot_name_lrd_format(market_slot_name):
        raise Exception(
            f"market slot alias {market_slot_name} does not have market"
            " slot alias lrd format!"
        )
    words = market_slot_name.split(".")
    market_type_name = words[0]
    market_type_dc = MarketType.by_id[market_type_name]
    market_type = MarketTypeGt_Maker.dc_to_tuple(market_type_dc)
    market_maker_alias = ".".join(words[1:-1])
    slot_start = int(words[-1])
    return MarketSlot(
        Type=market_type, MarketMakerAlias=market_maker_alias, StartUnixS=slot_start
    )


def is_dummy_atn_params(atn_params: AtnParams) -> bool:
    if atn_params.GNodeAlias == "d1.isone.dummy.ta":
        return True
    return False


def is_dummy_flo_params(flo_params: FloParams) -> bool:
    if flo_params.RtElecPriceUid == "00000000-0000-0000-0000-000000000000":
        return True
    return False


def dummy_flo_params() -> FloParams:
    return FloParams(
        RtElecPriceUid="00000000-0000-0000-0000-000000000000",
        WeatherUid="00000000-0000-0000-0000-000000000000",
    )


def get_k(atn_params: AtnParams) -> float:
    dt = atn_params.SystemMaxHeatOutputDeltaTempF
    gpm = atn_params.SystemMaxHeatOutputGpm
    swt = atn_params.SystemMaxHeatOutputSwtF
    rt = atn_params.RoomTempF
    return float(gpm * np.log(1 - dt / (swt - rt)))


def get_system_max_heat_output_kw_avg(atn_params: AtnParams) -> float:
    """What is the max heat that the system put out?  ASSUMES that the hydronic
    fluid is water.

    Args:
        tea_params: Uses the system_max_heat_output_delta_temp_f and
        the system_max_heat_output_gpm.

    Returns:
        float: max heat ouput of the heating system, in kw
    """
    gpm = atn_params.SystemMaxHeatOutputGpm
    delta_temp = atn_params.SystemMaxHeatOutputDeltaTempF
    c = cf.POUNDS_OF_WATER_PER_GALLON * cf.MINUTES_PER_HOUR / cf.BTU_PER_KWH
    if gpm == 0 or delta_temp == 0:
        raise Exception(
            f"max gpm is {gpm}, max delta_temp is {delta_temp}. Cannot calculate system heat output."
        )
    pwr = c * delta_temp * gpm
    return pwr


def get_max_store_kwh_th(params: AtnParams) -> float:
    return (
        cf.KWH_TH_PER_GALLON_PER_DEG_F
        * params.StoreSizeGallons
        * (params.MaxStoreTempF - params.ZeroPotentialEnergyWaterTempF)
    )
