from pydantic import BaseModel
from typing import (Dict, List, Union, Literal)
from fiqus.data.DataRoxieParser import RoxieData
from fiqus.data.DataFiQuSMultipole import MPDM


class MonoFiQuS(BaseModel):
    """
        Rutherford cable type
    """
    type: Literal['Mono']
    bare_cable_width: float = None
    bare_cable_height_mean: float = None


class RibbonFiQuS(BaseModel):
    """
        Rutherford cable type
    """
    type: Literal['Ribbon']
    bare_cable_width: float = None
    bare_cable_height_mean: float = None


class RutherfordFiQuS(BaseModel):
    """
        Rutherford cable type
    """
    type: Literal['Rutherford']
    bare_cable_width: float = None
    bare_cable_height_mean: float = None


class ConductorFiQuS(BaseModel):
    """
        Class for conductor type
    """
    cable: Union[RutherfordFiQuS, RibbonFiQuS, MonoFiQuS] = {'type': 'Rutherford'}


class GeneralSetting(BaseModel):
    """
        Class for general information on the case study
    """
    I_ref: List[float] = None


class ModelDataSetting(BaseModel):
    """
        Class for model data
    """
    general_parameters: GeneralSetting = GeneralSetting()
    conductors: Dict[str, ConductorFiQuS] = {}

#######################################################################################################################


class FiQuSGeometry(BaseModel):
    """
        Class for Roxie data
    """
    Roxie_Data: RoxieData = RoxieData()


class FiQuSSettings(BaseModel):
    """
        Class for FiQuS model
    """
    Model_Data_GS: ModelDataSetting = ModelDataSetting()


class RunFiQuS(BaseModel):
    """
        Class for FiQuS run
    """
    type: str = None
    geometry: int = None
    mesh: int = None
    solution: int = None
    launch_gui: bool = None
    overwrite: bool = None


class GeneralFiQuS(BaseModel):
    """
        Class for FiQuS general
    """
    magnet_name: str = None


class FDM(BaseModel):
    """
        Class for FiQuS
    """
    general: GeneralFiQuS = GeneralFiQuS()
    run: RunFiQuS = RunFiQuS()
    magnet: Union[MPDM] = {'type': 'multipole'}
