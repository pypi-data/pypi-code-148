from dataclasses import dataclass
from typing import List

import pandas as pd

from georgstage.model import Opgave, Vagt


N_GASTS = 60
VAGT_TIDER = [0, 4, 8, 12, 16, 20]


@dataclass
class FillResult:
    status: int
    vagter: List[Vagt]


def get_counts(vagter: List[Vagt]):
    """
    Returns function with signature lookup(gast:int, opgave:str) -> count: int
    Treat fysiske vagter special: sum of all fysiske, not just concrete
    """
    stats = {}
    fysiske = (Opgave.ORDONNANS, Opgave.UDKIG,
               Opgave.BJAERGEMAERS, Opgave.RORGAENGER)
    for vagt in vagter:
        if vagt.opgave in fysiske:
            keys = [(vagt.gast, opgave) for opgave in fysiske]
        else:
            keys = [(vagt.gast, vagt.opgave)]
        for key in keys:
            stats[key] = stats.setdefault(key, 0) + 1
    return lambda gast, opgave: stats.get((gast, opgave)) or 0


def get_counts_frame(vagter):
    """
    Returns dataframe with rows = gaster, columns = opgaver, values = count
    """
    counts = get_counts(vagter, N_GASTS)
    df = pd.DataFrame(range(1, N_GASTS + 1), columns=['gast'])
    for opgave in Opgave:
        df[opgave.name] = df.gast.apply(lambda g: counts(g, opgave))
    return df


def get_skifte_for_gast(gast):
    if 0 < gast <= 20:
        return 1
    elif 20 < gast <= 40:
        return 2
    else:
        return 3
