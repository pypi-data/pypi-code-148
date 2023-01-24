from geopy.distance import lonlat, distance
from shapely.wkt import loads

INTERIOR_ROADS = ['PARKING_ACCESS_ROAD', 'DESTINATION_ROAD', 'DRIVEWAY', 'VEHICLE_SERVICE_AISLE', 'ALLEY', 'ROUNDABOUT', 'SERVICE_AREA_ROAD', 'LIMITED_ACCESS_HIGHWAY']
NON_NAVIGABLE_ROADS = ['TRAIL', 'PATHWAY', 'DRIVE_THROUGH']


def get_segment_length(segment):
    wkt_linestring = segment.wkt_geom
    row_parsed = loads(wkt_linestring)
    coords = list(zip(row_parsed.xy[1], row_parsed.xy[0]))
    n_coords = len(coords) - 1
    dist = 0.0
    for i in range(0, n_coords):
        dist += distance(coords[i], coords[i + 1]).meters
    return dist


def get_wkt_coords(segment):
    wkt_linestring = segment.wkt_geom
    row_parsed = loads(wkt_linestring)
    coords = list(zip(row_parsed.xy[1], row_parsed.xy[0]))
    return coords
