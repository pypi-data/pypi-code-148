from pydantic import BaseModel
from typing import List


class Region(BaseModel):
    name: str = None
    number: int = None


class Regions(BaseModel):
    names: List[str] = None
    numbers: List[int] = None


class PoweredRegions(BaseModel):
    names: List[str] = None
    numbers: List[int] = None
    currents: List[float] = None
    sigmas: List[float] = None
    mu_rs: List[float] = None


class InducedRegions(BaseModel):
    names: List[str] = None
    numbers: List[int] = None
    sigmas: List[float] = None
    mu_rs: List[float] = None


class IronRegions(BaseModel):
    names: List[str] = None
    numbers: List[int] = None
    sigmas: List[float] = None
    mu_rs: List[float] = None


class AirRegion(BaseModel):
    name: str = None
    number: int = None
    sigma: float = None
    mu_r: float = None


class AirFarFieldRegion(BaseModel):
    name: str = None
    number: int = None
    radius_in: float = None
    radius_out: float = None


class Powered(BaseModel):
    vol: PoweredRegions = PoweredRegions()  # volume region
    surf_in: Regions = Regions()  # input terminal surface region
    surf_out: Regions = Regions()  # output terminal surface region
    cochain: Regions = Regions()  # winding cochain (cut)


class Induced(BaseModel):
    vol: InducedRegions = InducedRegions()  # volume region
    cochain: Regions = Regions()  # winding cochain (cut)


class Iron(BaseModel):
    vol: IronRegions = IronRegions()  # volume region
    surf: Regions = Regions()  # surface region


class Air(BaseModel):
    vol: AirRegion = AirRegion()  # volume region
    surf: Region = Region()  # surface region
    line: Region = Region()    # line region


class AirFarField(BaseModel):
    vol: AirFarFieldRegion = AirFarFieldRegion()  # volume region
    surf: Region = Region()  # surface region


class RegionsModel(BaseModel):
    powered: Powered = Powered()
    induced: Induced = Induced()
    iron: Iron = Iron()
    air: Air = Air()
    air_far_field: AirFarField = AirFarField()


# if __name__ == "__main__":
#     write = True
#     read = False
#
#     def read_regions(regions_file_name):
#         with open(regions_file_name, 'r') as stream:
#             yaml_str = ruamel.yaml.safe_load(stream)
#         return RegionsModel(**yaml_str)
#
#     def flist(x):
#         retval = ruamel.yaml.comments.CommentedSeq(x)
#         retval.fa.set_flow_style()  # fa -> format attribute
#         return retval
#
#     if write:
#         model = RegionsModel()
#         model.powered.vol = [1, 2]
#         data_dict = model.dict()
#         yaml = ruamel.yaml.YAML()
#         yaml.default_flow_style = False
#         yaml.emitter.alt_null = 'Null'
#
#         def my_represent_none(self, data):
#             return self.represent_scalar('tag:yaml.org,2002:null', 'null')
#
#         yaml.representer.add_representer(type(None), my_represent_none)
#         with open('cct_regions_empty.yaml', 'w') as yaml_file:
#             yaml.dump(model.dict(), yaml_file)
#     if read:
#         regions_file_name = 'cct1_regions_manual.yaml'
#         regions = read_regions(regions_file_name)
