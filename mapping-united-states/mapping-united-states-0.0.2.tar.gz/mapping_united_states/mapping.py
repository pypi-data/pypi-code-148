import logging
from typing import Optional, List

from shapely import Polygon
import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
from tqdm import tqdm

from mapping_united_states import CensusData


class MappingItemOptions:
    is_visible: bool
    line_color: Optional[str]
    line_thickness: Optional[float]
    fill_color: Optional[str]

    def __init__(self, line_color: Optional[str] = None, line_thickness: Optional[float] = None,
                 fill_color: Optional[str] = None):
        self.is_visible = True
        self.line_color = line_color
        self.line_thickness = line_thickness
        self.fill_color = fill_color


class WaterMappingItemOptions(MappingItemOptions):
    min_water_area: Optional[int]

    def __init__(self, line_color: Optional[str] = None, line_thickness: Optional[float] = None,
                 fill_color: Optional[str] = None, min_water_area: Optional[int] = None):
        super().__init__(line_color, line_thickness, fill_color)
        self.min_water_area = min_water_area


class MappingOptions:
    plot_size: tuple
    border: MappingItemOptions
    water: WaterMappingItemOptions
    primary_roads: MappingItemOptions
    secondary_roads: MappingItemOptions
    neighborhood_roads: MappingItemOptions
    limiting_region: Optional[Polygon]

    def __init__(self):
        self.limiting_region = None
        self.plot_size = (45, 45)
        self.border = MappingItemOptions(line_color='#433B34', line_thickness=6, fill_color='#F4F3EA')
        self.water = WaterMappingItemOptions(line_color='#63D4E6', line_thickness=2, fill_color='#CFEEF6',
                                             min_water_area=9000000)
        self.primary_roads = MappingItemOptions(line_color='#433B34', line_thickness=4)
        self.secondary_roads = MappingItemOptions(line_color='#433B34', line_thickness=3)
        self.neighborhood_roads = MappingItemOptions(line_color='#433B34', line_thickness=1)


def map_area(export_file_name: str, areas: List[str], map_options: MappingOptions, census_data: CensusData):
    county_geoids = get_geoids_for_areas(areas, census_data)
    counties = census_data.get_counties()
    counties = counties[counties.GEOID.isin(county_geoids)]

    logging.info(f'Processing {len(counties)} Counties')
    if map_options.limiting_region is not None:
        counties = counties.clip(map_options.limiting_region)

    bounding_box_geometry = counties['geometry'].unary_union
    shape = gpd.GeoDataFrame({'name': 'Bounding Box', 'geometry': bounding_box_geometry}, crs="EPSG:4326",
                             index=[0])

    fig, ax = plt.subplots(figsize=map_options.plot_size)
    ax.axis('off')

    if map_options.border.is_visible:
        border_fill_color = __get_color(map_options.border.fill_color)
        border_line_thickness = __get_line_thickness(map_options.border.line_thickness)
        shape.plot(ax=ax, linewidth=border_line_thickness / 2, edgecolor=border_fill_color,
                   facecolor=border_fill_color)

    map_water(ax, county_geoids, map_options.water, map_options.limiting_region, census_data)
    map_roads(ax, county_geoids, map_options, map_options.limiting_region, census_data)

    if map_options.border.is_visible:
        border_line_thickness = __get_line_thickness(map_options.border.line_thickness)
        border_line_color = __get_color(map_options.border.line_color)
        shape.plot(ax=ax, linewidth=border_line_thickness, edgecolor=border_line_color, facecolor='none')

    logging.info('Exporting...')
    plt.tight_layout()
    plt.savefig(export_file_name, transparent=True)
    plt.close()


def get_geoids_for_areas(areas: List[str], census_data: CensusData) -> []:
    ret = []

    states = census_data.get_states_info()

    for area in areas:
        include_only_fips = []

        if len(area) == 2:
            if area.isdigit():
                state_code = area
            else:
                if area not in states:
                    raise Exception(f'Unable to find the state abbreviation "{area}"')

                state_code = states[area]['STATE']
        elif len(area) == 5:
            state_code = area[:2]
            include_only_fips = [area]
        else:
            raise Exception(f"""Unrecognized code. 
            Please provide the State FIPS Code, 2 letter state abbreviation, or county FIPS code. 
            You provided: "{area}"
            """)

        counties = census_data.get_counties_by_fips_code(state_code)

        for c in counties:
            if len(include_only_fips) > 0:
                if c['GEOID'] in include_only_fips:
                    ret.append(c['GEOID'])
            else:
                ret.append(c['GEOID'])

    return ret


def map_roads(ax: plt.Axes, county_geoids: [], map_options: MappingOptions, limiting_region: Optional[Polygon],
              census_data: CensusData):
    if (not map_options.primary_roads.is_visible
            and not map_options.neighborhood_roads.is_visible
            and not map_options.secondary_roads.is_visible):
        return

    for geoid in tqdm(county_geoids, unit='counties', desc='Mapping Roads'):
        county_roads = census_data.get_roads_for_county(geoid)

        if map_options.neighborhood_roads.is_visible:
            local_neighborhood_road = county_roads[county_roads.MTFCC == 'S1400']
            if not local_neighborhood_road.empty:
                line_thickness = __get_line_thickness(map_options.neighborhood_roads.line_thickness)
                line_color = __get_color(map_options.neighborhood_roads.line_color)
                line_fill = __get_color(map_options.neighborhood_roads.fill_color)

                if limiting_region is not None:
                    local_neighborhood_road = local_neighborhood_road.clip(limiting_region)

                local_neighborhood_road.plot(ax=ax, linewidth=line_thickness, edgecolor=line_color,
                                             facecolor=line_fill)

        if map_options.secondary_roads.is_visible:
            secondary_road = county_roads[(county_roads.MTFCC == 'S1200') | (county_roads.MTFCC == 'S1630')]
            if not secondary_road.empty:
                line_thickness = __get_line_thickness(map_options.secondary_roads.line_thickness)
                line_color = __get_color(map_options.secondary_roads.line_color)
                line_fill = __get_color(map_options.secondary_roads.fill_color)

                if limiting_region is not None:
                    secondary_road = secondary_road.clip(limiting_region)

                secondary_road.plot(ax=ax, linewidth=line_thickness, edgecolor=line_color, facecolor=line_fill)

        if map_options.primary_roads.is_visible:
            primary_road = county_roads[county_roads.MTFCC == 'S1100']
            if not primary_road.empty:
                line_thickness = __get_line_thickness(map_options.primary_roads.line_thickness)
                line_color = __get_color(map_options.primary_roads.line_color)
                line_fill = __get_color(map_options.primary_roads.fill_color)

                if limiting_region is not None:
                    primary_road = primary_road.clip(limiting_region)

                primary_road.plot(ax=ax, linewidth=line_thickness, edgecolor=line_color, facecolor=line_fill)


def map_water(ax: plt.Axes, county_geoids: [], options: WaterMappingItemOptions, limiting_region: Optional[Polygon],
              census_data: CensusData):
    if not options.is_visible:
        return

    water_areas = []

    for geoid in tqdm(county_geoids, unit='counties', desc='Mapping Water'):
        water = census_data.get_area_water_for_county(geoid)
        if options.min_water_area is not None:
            water = water[water.AWATER > options.min_water_area]

        water_areas.append(water)

    logging.info('Combining Water Shapes')
    combined_water = pd.concat(water_areas)
    bounding_box_geometry = combined_water['geometry'].unary_union
    shape = gpd.GeoDataFrame({'name': 'Bounding Box', 'geometry': bounding_box_geometry}, crs="EPSG:4269",
                             index=[0])

    if limiting_region is not None:
        shape = shape.clip(limiting_region)

    logging.info('Plotting Water')
    fill_color = __get_color(options.fill_color)
    line_thickness = __get_line_thickness(options.line_thickness)
    line_color = __get_color(options.line_color)
    shape.plot(ax=ax, linewidth=line_thickness, edgecolor=line_color, facecolor=fill_color)
    logging.info('Done with Water.')


def __get_line_thickness(thickness: Optional[float]) -> float:
    return thickness if thickness is not None else 1


def __get_color(color: str) -> str:
    if color is not None:
        return color

    return 'none'
