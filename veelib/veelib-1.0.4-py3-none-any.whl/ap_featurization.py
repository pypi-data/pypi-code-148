from geopy.distance import lonlat, distance
import json
import numpy as np
import pandas as pd
import scipy.stats

# import ndm_road_segment_utils as road_utils

INTERIOR_ROADS = ['PARKING_ACCESS_ROAD', 'DESTINATION_ROAD', 'DRIVEWAY', 'VEHICLE_SERVICE_AISLE', 'ALLEY', 'ROUNDABOUT', 'SERVICE_AREA_ROAD', 'LIMITED_ACCESS_HIGHWAY']
NON_NAVIGABLE_ROADS = ['TRAIL', 'PATHWAY', 'DRIVE_THROUGH']

def get_angle_between_aps(pivot_coords, ap1_coord, ap2_coord):
        v0 = np.array(ap1_coord) - np.array(pivot_coords)
        v1 = np.array(ap2_coord) - np.array(pivot_coords)

        angle = np.degrees(np.math.atan2(np.linalg.det([v0,v1]), np.dot(v0,v1)))
        return abs(angle)


def shift_direction_towards_address(generated_ap, addresses):
    shifted_gen_ap_coords = eval(generated_ap.shifted_ap_coordinates)
    shifted_gen_ap_coords = (shifted_gen_ap_coords['lat'], shifted_gen_ap_coords['lng'])
    
    gen_ap_coords = eval(generated_ap.ap_coordinates)
    gen_ap_coords = (gen_ap_coords['lat'], gen_ap_coords['lng'])

    address_coords = (addresses.loc[str(generated_ap.address_id)].rep_point_lat_y, addresses.loc[str(generated_ap.address_id)].rep_point_lng_x)
    
    dist_to_orig_coords = distance(address_coords, gen_ap_coords).meters
    dist_to_shifted_coords = distance(address_coords, shifted_gen_ap_coords).meters

    return pd.Series((int(dist_to_shifted_coords < dist_to_orig_coords), dist_to_orig_coords - dist_to_shifted_coords))


def fow_histogram_segments(fow_hist_array):
    fow_hist = {fow:0 for fow in INTERIOR_ROADS + NON_NAVIGABLE_ROADS}
    keys = fow_hist.keys()
    for fow in json.loads(fow_hist_array):
        if fow in keys:
            fow_hist[fow] += 1
    return pd.Series((list(fow_hist.values())))


def distance_to_address_aps(generated_ap, generated_address_aps, addresses):
    gen_ap_coords = eval(generated_ap.shifted_ap_coordinates)
    gen_ap_coords = (gen_ap_coords['lat'], gen_ap_coords['lng'])

    address_coords = (addresses.loc[str(generated_ap.address_id)].rep_point_lat_y, addresses.loc[str(generated_ap.address_id)].rep_point_lng_x)
    gen_address_aps = generated_address_aps.loc[generated_address_aps.address_id == generated_ap.address_id]
    if len(gen_address_aps) == 0:
        return pd.Series((0, 0, 0))
    
    dist_to_furthest = float('-inf')
    dist_to_closest = float('inf')
    min_angle = float('inf')
    for i, addr_ap in gen_address_aps.iterrows():
        addr_ap_coords = eval(addr_ap.shifted_ap_coordinates)
        addr_ap_coords = (addr_ap_coords['lat'], addr_ap_coords['lng'])
        dist = distance(gen_ap_coords, addr_ap_coords).meters
        if dist < dist_to_closest:
            dist_to_closest = dist
        if dist > dist_to_furthest:
            dist_to_furthest = dist
        angle = get_angle_between_aps(address_coords, addr_ap_coords, gen_ap_coords)
        if angle < min_angle:
            min_angle = angle
    
    return pd.Series((dist_to_closest, dist_to_furthest, angle))


def distance_to_closest_other_address_ap(generated_ap, generated_address_aps):
    min_distance = float('inf')
    
    coords1 = eval(generated_ap.shifted_ap_coordinates)
    c1 = (coords1['lat'], coords1['lng'])
    node1_id = generated_ap.node_id

    find_other_aps = False
    other_generated_aps = generated_address_aps.loc[generated_address_aps.address_id == generated_ap.address_id]
    for i, g_ap in other_generated_aps.iterrows():
        
        if node1_id == g_ap.node_id:
            continue
        
        find_other_aps = True
    
        coords2 = eval(g_ap.shifted_ap_coordinates)
        c2 = (coords2['lat'], coords2['lng'])
        
        dist = distance(c1, c2).meters
        if dist < min_distance:
            min_distance = dist
    
    return (min_distance if find_other_aps else 0)


def add_aggregated_features(generated_aps):

    generated_aps['address_id'] = generated_aps['poi_id']

    # Declare functions inside main function in order to save time by using global variable
    # rather than passing it in every time. This is much faster.
    def num_aps_within_radius(generated_ap, radii, skip_self_node_id=True):
        aps_found_within_radius = [0 for r in radii]
        
        coords1 = eval(generated_ap.shifted_ap_coordinates)
        c1 = (coords1['lat'], coords1['lng'])   
        node1_id = generated_ap.node_id
        
        other_generated_aps = generated_aps.loc[generated_aps.address_id == generated_ap.address_id]
        for i, g_ap in other_generated_aps.iterrows():
            
            if skip_self_node_id and node1_id == g_ap.node_id:
                continue
            
            coords2 = eval(g_ap.shifted_ap_coordinates)
            c2 = (coords2['lat'], coords2['lng'])
            dist = distance(c1, c2).meters

            for i, r in enumerate(radii):
                if dist < r:
                    aps_found_within_radius[i] += 1
            
        return pd.Series((aps_found_within_radius))

    # Features for which should generate likelihood from a normal
    def get_likelihood_of_feature_based_on_other_generated_aps(generated_ap, feature):
        values = []
        other_generated_aps = generated_aps.loc[generated_aps.address_id == generated_ap.address_id]
        for i, g_ap in other_generated_aps.iterrows():
            values.append(g_ap[feature])
        mean = np.mean(values)
        std = np.std(values)
        import math
        likelihood = math.nan
        try:
            likelihood = scipy.stats.norm(mean, std).pdf(generated_ap[feature])
        except Exception:
            pass
            #print(err) will print out "invalid value encountered in double_scalars"
        return likelihood if not np.isnan(likelihood) else 1


    # How about a column that simply indicates how many OTHER APs exist at this POI
    def num_other_generated_aps(generated_ap):
        other_generated_aps = generated_aps.loc[generated_aps.address_id == generated_ap.address_id]
        return len(other_generated_aps) - 1


    # For generated_address_aps
    def num_graph_generated_aps(generated_ap):
        return len(generated_aps.loc[generated_aps.address_id == generated_ap.address_id])


    # For generated_address_aps
    def closest_graph_generated_aps(generated_ap):
        gen_aps = generated_aps.loc[generated_aps.address_id == generated_ap.address_id]
        if len(gen_aps) == 0:
            return pd.Series((-1, -1))
        
        return pd.Series((min(gen_aps.haversine_distance_ap_to_poi), min(gen_aps.distance_traveled_from_source_to_ap_node_meters)))


    def parking_lot_size_rank(generated_ap):
        pl_sizes = set()
        pl_size = generated_ap.num_segments_in_parking_lot_ap_belongs_to
        pl_sizes.add(pl_size)
        other_generated_aps = generated_aps.loc[generated_aps.address_id == generated_ap.address_id]
        for i, gen_ap in other_generated_aps.iterrows():
            pl_sizes.add(gen_ap.num_segments_in_parking_lot_ap_belongs_to)
        
        pl_size_ranks = sorted(list(pl_sizes), reverse=True)
        return pl_size_ranks.index(pl_size)


    def has_other_transitions(generated_ap):
        has_exterior_transition_at_another_ap = 0
        has_interior_transition_at_another_ap = 0
        
        other_generated_aps = generated_aps.loc[generated_aps.address_id == generated_ap.address_id]
        for i, g_ap in other_generated_aps.iterrows():
            transition = json.loads(g_ap.transition_road_segment_fows)
            if transition[0] == 'REGULAR_ROAD':
                has_exterior_transition_at_another_ap = 1
            if transition[0] in road_utils.INTERIOR_ROADS:
                has_interior_transition_at_another_ap = 1
                
        return pd.Series(([has_exterior_transition_at_another_ap, has_interior_transition_at_another_ap]))


    def identify_source_node_differences(generated_ap):
        lowest_source = float('inf')
        highest_source = float('-inf')
        
        other_generated_aps = generated_aps.loc[generated_aps.address_id == generated_ap.address_id]
        for i, g_ap in other_generated_aps.iterrows():
            source_node = g_ap.index_source_node_ap_originated_from
            if source_node < lowest_source:
                lowest_source = source_node
            if source_node > highest_source:
                highest_source = source_node
                
        return pd.Series(([generated_ap.index_source_node_ap_originated_from - lowest_source, highest_source - generated_ap.index_source_node_ap_originated_from]))


    def find_other_aps_closer_and_farther(generated_ap):
        num_closer_aps = 0
        num_farther_aps = 0
        num_closer_aps_same_source_index = 0
        num_farther_aps_same_source_index = 0
        total_other_aps = 0
        
        distance_to_poi = generated_ap.haversine_distance_ap_to_poi
        source_index_of_poi = generated_ap.index_source_node_ap_originated_from
        
        other_generated_aps = generated_aps.loc[generated_aps.address_id == generated_ap.address_id]
        for i, g_ap in other_generated_aps.iterrows():
            
            if generated_ap.node_id == g_ap.node_id:
                continue
                
            total_other_aps += 1
            
            if g_ap.haversine_distance_ap_to_poi < distance_to_poi:
                num_closer_aps += 1
                if source_index_of_poi == g_ap.index_source_node_ap_originated_from:
                    num_closer_aps_same_source_index += 1

            if g_ap.haversine_distance_ap_to_poi > distance_to_poi:
                num_farther_aps += 1
                if source_index_of_poi == g_ap.index_source_node_ap_originated_from:
                    num_farther_aps_same_source_index += 1
        
        if total_other_aps == 0:
                return pd.Series((0, 0, 0, 0, 0, 0, 0, 0))
            
        return pd.Series((num_closer_aps, num_farther_aps, num_closer_aps_same_source_index, num_farther_aps_same_source_index,
                          num_closer_aps/total_other_aps, num_farther_aps/total_other_aps, num_closer_aps_same_source_index/total_other_aps, num_farther_aps_same_source_index/total_other_aps))


    def distance_to_closest_other_ap(generated_ap, skip_self_node_id=True):
        min_distance = float('inf')
        
        coords1 = eval(generated_ap.shifted_ap_coordinates)
        c1 = (coords1['lat'], coords1['lng'])
        node1_id = generated_ap.node_id

        find_other_aps = False
        other_generated_aps = generated_aps.loc[generated_aps.address_id == generated_ap.address_id]
        for i, g_ap in other_generated_aps.iterrows():
            
            if skip_self_node_id and node1_id == g_ap.node_id:
                continue
            
            find_other_aps = True
        
            coords2 = eval(g_ap.shifted_ap_coordinates)
            c2 = (coords2['lat'], coords2['lng'])
            
            dist = distance(c1, c2).meters
            if dist < min_distance:
                min_distance = dist
        
        return (min_distance if find_other_aps else 0)


    generated_aps['parking_lot_rank'] = generated_aps.apply(lambda x: parking_lot_size_rank(x), axis=1)
    
    generated_aps[['has_exterior_transition_at_another_ap', 'has_interior_transition_at_another_ap']] = \
        generated_aps.apply(lambda x: has_other_transitions(x), axis=1)
    
    generated_aps[['lowest_source_difference', 'highest_source_difference']] = \
        generated_aps.apply(lambda x: identify_source_node_differences(x), axis=1)

    generated_aps[['num_closer_access_points', 'num_farther_access_points',
                   'num_closer_aps_same_source_index', 'num_farther_aps_same_source_index',
                   'num_closer_access_points_pct', 'num_farther_access_points_pct',
                   'num_closer_aps_same_source_index_pct', 'num_farther_aps_same_source_index_pct']] = \
        generated_aps.apply(lambda x: find_other_aps_closer_and_farther(x), axis=1)

    generated_aps['distance_to_closest_generated_ap'] = \
        generated_aps.apply(lambda x: distance_to_closest_other_ap(x), axis=1)

    generated_aps[['nearby_aps_within_5_meters', 'nearby_aps_within_10_meters', 'nearby_aps_within_25_meters', 'nearby_aps_within_100_meters']] = \
        generated_aps.apply(lambda x: num_aps_within_radius(x, [5, 10, 25, 100]), axis=1)

    generated_aps[['parking_access_road_along_path', 'destination_road_along_path', \
                   'driveway_along_path', 'vehicle_service_aisle_along_path', \
                   'alley_along_path', 'roundabout_along_path', \
                   'service_area_road_along_path', 'limited_access_highway_along_path', \
                   'trail_along_path', 'pathway_along_path', 'drivethrough_along_path']] = \
        generated_aps.apply(lambda x: fow_histogram_segments(x.fow_histogram_segments_traveled_from_source_to_ap_node), axis=1)

    generated_aps[['parking_access_road_in_parking_lot', 'destination_road_in_parking_lot', \
                   'driveway_in_parking_lot', 'vehicle_service_aisle_in_parking_lot', \
                   'alley_in_parking_lot', 'roundabout_in_parking_lot', \
                   'service_area_road_in_parking_lot', 'limited_access_highway_in_parking_lot', \
                   'trail_in_parking_lot', 'pathway_in_parking_lot', 'drivethrough_in_parking_lot']] = \
        generated_aps.apply(lambda x: fow_histogram_segments(x.fow_histogram_of_parking_lot_ap_belongs_to), axis=1)

    generated_aps['haversine_distance_ap_to_poi_likelihood'] = \
        generated_aps.apply(lambda x: get_likelihood_of_feature_based_on_other_generated_aps(x, 'haversine_distance_ap_to_poi'), axis=1)

    generated_aps['distance_traveled_from_source_to_ap_node_meters_likelihood'] = \
        generated_aps.apply(lambda x: get_likelihood_of_feature_based_on_other_generated_aps(x, 'distance_traveled_from_source_to_ap_node_meters'), axis=1)

    generated_aps['local_closeness_centrality_ap_node_likelihood'] = \
        generated_aps.apply(lambda x: get_likelihood_of_feature_based_on_other_generated_aps(x, 'local_closeness_centrality_ap_node'), axis=1)

    generated_aps['local_degree_centrality_ap_node_likelihood'] = \
        generated_aps.apply(lambda x: get_likelihood_of_feature_based_on_other_generated_aps(x, 'local_degree_centrality_ap_node'), axis=1)

    generated_aps['local_betweenness_centrality_ap_node_likelihood'] = \
        generated_aps.apply(lambda x: get_likelihood_of_feature_based_on_other_generated_aps(x, 'local_betweenness_centrality_ap_node'), axis=1)

    generated_aps['num_other_generated_aps'] = \
        generated_aps.apply(lambda x: num_other_generated_aps(x), axis=1)

    return generated_aps
