from geopy.distance import lonlat, distance, GeodesicDistance
import geopy
import json
import logging
import pandas as pd
import networkx as nx
import numpy as np
from shapely.geometry import Point, LineString
from shapely.wkt import loads

import sys
sys.path.append("/workspace/pyspark-app")

from .ndm_road_segment_utils import *
# Note, this geocoder API is deprecated
# from apple.geo.client.fwdgeo import FwdGeoClient
# FWDGEO_URL = "https://gsp-ssl.ls.apple.com/fwdgeo.arpc"

'''
Define the features obtained during AP retrieval (recall)
'''
address_ap_features = [
    'address_ap_index',
    'poi_id',
    'ap_coordinates',
    'shifted_ap_coordinates',
    'node_id',
    'segment_id',
    'road_name_matches_poi_street',
    'haversine_distance_ap_to_poi',
]

ap_features = [
    'poi_id',
    'node_id',
    'index_source_node_ap_originated_from',
    'transition_road_segment_ids',
    'ap_coordinates',
    'haversine_distance_ap_to_poi',
    'transition_road_segment_fows',
    'distance_traveled_from_source_to_ap_node_meters',
    'num_segments_traveled_from_source_to_ap_node',
    'fow_histogram_segments_traveled_from_source_to_ap_node',
    'num_segments_in_parking_lot_ap_belongs_to',
    'fow_histogram_of_parking_lot_ap_belongs_to',
    'pct_incoming_edges_to_ap_node_interior',
    'pct_incoming_edges_to_ap_node_exterior',
    'pct_outgoing_edges_from_ap_node_interior',
    'pct_outgoing_edges_from_ap_node_exterior',
    'local_degree_centrality_ap_node',
    'local_betweenness_centrality_ap_node',
#    'local_pagerank_centrality_ap_node',
    'local_closeness_centrality_ap_node',
    'num_heading_changes_from_source_to_ap_node',
    'total_angle_heading_changes_from_source_to_ap_node',
    'avg_angle_heading_changes_from_source_to_ap_node',
    # 'parcel_area',
    # 'parcel_perimeter',
    # 'ap_distance_from_parcel_boundary',
]


def get_coords_of_address(address, city, state):
    fwd_client = FwdGeoClient(FWDGEO_URL)
    resp = fwd_client.request(address, city, state)
    lat = resp.placeResult[0].place.center.lat
    lng = resp.placeResult[0].place.center.lng
    return lat, lng


def get_rtree_bounding_box_coords(lat, lng, distance_kilometers=0.5):
    bearings = [225, 45]
    bounding_coords = []
    for bearing in bearings:
        l = GeodesicDistance(kilometers=distance_kilometers).destination(geopy.Point(lat, lng), bearing)
        bounding_coords.extend([l[1], l[0]])
    return bounding_coords


def get_address_source_nodes(poi_location, graph, interior_graph_reversed, cc_dict, tree, num_nearest, k=15):
    # Search through k closest nodes to find num_nearest nodes that come from distinct connected components
    component_sources = list(tree.nearest(poi_location, k))

    cc_set = set()
    sources = []
    for cs in component_sources:
        cs = str(cs)
        if cc_dict[cs] not in cc_set:
            cc_set.add(cc_dict[cs])
            sources.append(cs)

            # Stop if we have found enough starting nodes
            if len(sources) == num_nearest:
                return sources
    
    return sources


def get_source_nodes(poi_location, segments, graph, interior_graph_reversed, cc_dict, cc_list, tree, num_nearest, k=15):
    # Search through k closest nodes to find num_nearest nodes that come from distinct connected components
    component_sources = list(tree.nearest(poi_location, k))

    max_dist = 0
    for cs in component_sources:
        cs = str(cs)
        ap_coords = (graph.nodes[cs]['pos'][1], graph.nodes[cs]['pos'][0])
        dist_to_addr = distance((poi_location[1], poi_location[0]), ap_coords).kilometers
        if dist_to_addr > max_dist:
            max_dist = dist_to_addr

    cc_set = set()
    sources = []
    
    # Get the set of all regular roads surrounding the address point
    reg_road_ids_nearby = set()
    bounding_box = get_rtree_bounding_box_coords(poi_location[1], poi_location[0], distance_kilometers=max_dist)
    nodes_in_bounding_box = list(tree.intersection(bounding_box))

    for node in nodes_in_bounding_box:
        node = str(node)

        fows = graph.nodes[node].get('in_fow', []) + graph.nodes[node].get('out_fow', [])
        road_ids = graph.nodes[node].get('in_road_ids', []) + graph.nodes[node].get('out_road_ids', [])
        for fow, road_id in zip(fows, road_ids):
            if fow in ["REGULAR_ROAD", "LIMITED_ACCESS_HIGHWAY"]:
                reg_road_ids_nearby.add(road_id)

    for cs in component_sources:
        cs = str(cs)
        cc_index = cc_dict[cs]

        # This determines if a node belonging to the cc has not been used and is not simply a single node
        if cc_index not in cc_set and len(cc_list[cc_index]) > 1:
            ap_coords = (graph.nodes[cs]['pos'][1], graph.nodes[cs]['pos'][0])

            # Check if the node has regular roads touching it, if so, does it lead to a good parking lot?
            in_fows = graph.nodes[cs].get('in_fow', [])            
            out_fows = graph.nodes[cs].get('out_fow', [])

            # Although we identify a node leading to a parking lot, is it a parking lot that is close to the address point?
            # Since the len(connected component segments) > 1, we know there is an interior road, just need to check exterior
            if "REGULAR_ROAD" in in_fows or "REGULAR_ROAD" in out_fows:
                interior_road_leads_towards_address_point = False

                # It does not matter if the road is incoming or outgoing, check if it leads towards or away from the address point
                fows = in_fows + out_fows
                road_ids = graph.nodes[cs].get('in_road_ids', []) + graph.nodes[cs].get('out_road_ids', [])

                for fow, road in zip(fows, road_ids):
                    if fow != "REGULAR_ROAD":
                        parsed_coords = get_wkt_coords(segments.loc[road])
                        # if len(parsed_coords) < 3:
                        #     print(segments.loc[road].wkt_geom)
                        secondary_coords = None
                        
                        if parsed_coords[0][0] == ap_coords[0] and parsed_coords[0][1] == ap_coords[1]:
                            secondary_coords = parsed_coords[1]
                        elif parsed_coords[-1][0] == ap_coords[0] and parsed_coords[-1][1] == ap_coords[1]:
                            secondary_coords = parsed_coords[-2]
                        if secondary_coords == None:
                            print(segments.loc[road])
                            # print("road segment feature_id")
                            # print(segments.loc[road].feature_id)
                            # print("road segment wkt")
                            # print(segments.loc[road].wkt_geom)
                            # print("road segment from node id")
                            # print(segments.loc[road].from_node)
                            # print("road segment to node id")
                            # print(segments.loc[road].to_node)
                            print("ap_coords[0], ap_coords[1]")
                            print([ap_coords[0],ap_coords[1]])
                            print("parsed_coords ")
                            print(parsed_coords)
                            print([parsed_coords[0][0], parsed_coords[0][1]])
                            print([parsed_coords[-1][0], parsed_coords[-1][1]])
                        # If the angle is > 90, it means the coordinate is going further away from the address point
                        if get_angle_between_points(ap_coords, (poi_location[1], poi_location[0]), secondary_coords) < 90:
                            interior_road_leads_towards_address_point = True
                            break
                
                if not interior_road_leads_towards_address_point:
                    continue

            # Verify it is not across a regular road 
            address_point_to_ap_node_line = LineString([poi_location, (ap_coords[1], ap_coords[0])])
            node_across_regular_road = False

            road_ids = graph.nodes[cs].get('in_road_ids', []) + graph.nodes[cs].get('out_road_ids', [])

            try:
                for road in reg_road_ids_nearby:
                    if road in road_ids:
                         continue
                    if loads(segments.loc[road].wkt_geom).crosses(address_point_to_ap_node_line):
                        node_across_regular_road = True
                        break
            except (Exception,KeyError) as err:
                print(err)

            if node_across_regular_road:
                continue
            
            cc_set.add(cc_index)
            sources.append(cs)

            # Stop if we have found enough starting nodes
            if len(sources) == num_nearest:
                return sources
    
    return sources


# Find the road segments whose street name matches the AddressPoint/POIs address
# and search along the road to find the best AP placement. Should
# a road segment not be found with the same name, a back-up 'REGULAR'
# road segment can be used to place an optional AP.
#
# This function can be used in advance to generate APs or be used for AddressPoint/POIs which had no APs
# after the precision model was ran to safely place a reasonable AP.
def find_address_based_ap(lat, lng, street, segments, graph, interior_graph_reversed, cc_dict, cc_list, tree, cutoff=1000, num_nearest_sources=8, non_named_road_allowed=True, num_aptas_allowable=2, alternative_apta_distance_cap=10, shift_distance=2):
    loc = (lng, lat)

    sources = get_address_source_nodes(loc, graph, interior_graph_reversed, cc_dict, tree, num_nearest_sources)
    
    # Contains all regular road segments that were reached from the parking lot crawl
    segment_ids = set()

    # Dictionary indicates which regular road came from which origin source node
    path_node_seg_dict = {}

    # Source provides the closest nodes to the lat/lng in separate connected components
    for j, s in enumerate(sources):

        lengths, paths = nx.single_source_dijkstra(interior_graph_reversed, source=s, weight='length', cutoff=cutoff)

        # The node is the end-point of the graph traversal and the path is the nodes touched starting with source.
        # This loop iterates over all possible paths found originating from the source.
        for node, path in paths.items():
            end_node = graph.nodes[node]
            
            in_road_fows = end_node.get('in_fow', [])
            in_road_ids = end_node.get('in_road_ids', [])
            out_road_fows = end_node.get('out_fow', [])
            out_road_ids = end_node.get('out_road_ids', [])

            has_reg_road = False

            # Search through all incoming and outgoing fows for regular road segments
            for i, in_fow in enumerate(in_road_fows):
                if in_fow == "REGULAR_ROAD":
                    segment_ids.add(in_road_ids[i])
                    path_node_seg_dict[in_road_ids[i]] = node
                    has_reg_road = True

            for i, out_fow in enumerate(out_road_fows):
                if out_fow == "REGULAR_ROAD":
                    segment_ids.add(out_road_ids[i])
                    path_node_seg_dict[out_road_ids[i]] = node
                    has_reg_road = True

            if has_reg_road:
                break
   
    # Regular roads which have the same street name as the POI street
    street_name_match_segment_ids = set()
    non_street_name_match_segment_ids = set()

    if street:
        for s_id in segment_ids:
            seg = segments.loc[s_id]
            added = False
            if not pd.isna(seg.street_names):
                seg_st_names = seg.street_names.split("/")
                for s in street.split("/"):
                    if s in seg_st_names:
                        street_name_match_segment_ids.add(s_id)
                        added = True
                        break

            if not added:
                non_street_name_match_segment_ids.add(s_id)

    aptas = []

    # Variables to hold information related to the best potential location for the address-based AP   
    if len(street_name_match_segment_ids) > 0:
        closest_ap_coord_dist = float('inf')
        closest_ap_coord = None
        shifted_ap_coord = None
        path_end_node = None
        final_segment_id = None
        street_name_match = True

        # At most we allow 1 APTA to come from a named road, otherwise two APs on the same road stretch don't make sense.
        for s_id in street_name_match_segment_ids:
            wkt_coords = get_wkt_coords(segments.loc[s_id])

            for i in range(1, len(wkt_coords)):
                dist = distance(wkt_coords[i-1], wkt_coords[i]).meters
                lat_diff = wkt_coords[i][0] - wkt_coords[i-1][0]
                lng_diff = wkt_coords[i][1] - wkt_coords[i-1][1]

                # Interpolate between wkt_coords along a segment at 5% intervals
                for pct in range(0, 105, 5):
                    pct /= 100
                    new_lat = wkt_coords[i-1][0] + (pct*lat_diff)
                    new_lng = wkt_coords[i-1][1] + (pct*lng_diff)

                    dist = distance((loc[1], loc[0]), (new_lat, new_lng)).meters
                    if dist < closest_ap_coord_dist:
                        closest_ap_coord = (new_lat, new_lng)
                        closest_ap_coord_dist = dist
                        path_end_node = path_node_seg_dict[s_id]
                        final_segment_id = s_id

        if len(aptas) < num_aptas_allowable:
            pct_move = shift_distance/closest_ap_coord_dist
            lat_diff = loc[1] - closest_ap_coord[0]
            lng_diff = loc[0] - closest_ap_coord[1]
            shifted_lat = closest_ap_coord[0] + (pct_move*lat_diff)
            shifted_lng = closest_ap_coord[1] + (pct_move*lng_diff)
            shifted_ap_coord = (shifted_lat, shifted_lng)

            aptas.append(pd.Series((closest_ap_coord, shifted_ap_coord, path_end_node, final_segment_id, street_name_match, closest_ap_coord_dist)))

    # No named road, but a regular road does exist nearby which can be used instead
    if non_named_road_allowed:
        while len(aptas) < num_aptas_allowable and len(non_street_name_match_segment_ids) > 0:
            closest_ap_coord_dist = float('inf')
            closest_ap_coord = None
            shifted_ap_coord = None
            path_end_node = None
            final_segment_id = None
            street_name_match = False 

            for s_id in non_street_name_match_segment_ids:
                wkt_coords = get_wkt_coords(segments.loc[s_id])
                for i in range(1, len(wkt_coords)):
                    dist = distance(wkt_coords[i-1], wkt_coords[i]).meters
                    lat_diff = wkt_coords[i][0] - wkt_coords[i-1][0]
                    lng_diff = wkt_coords[i][1] - wkt_coords[i-1][1]
                    
                    # Interpolate between wkt_coords along a segment at 5% intervals
                    for pct in range(0, 105, 5):
                        pct /= 100
                        new_lat = wkt_coords[i-1][0] + (pct*lat_diff)
                        new_lng = wkt_coords[i-1][1] + (pct*lng_diff)
                        
                        dist = distance((loc[1], loc[0]), (new_lat, new_lng)).meters
                        if dist < closest_ap_coord_dist:
                            closest_ap_coord = (new_lat, new_lng)
                            closest_ap_coord_dist = dist
                            path_end_node = path_node_seg_dict[s_id]
                            final_segment_id = s_id

            pct_move = shift_distance/closest_ap_coord_dist
            lat_diff = loc[1] - closest_ap_coord[0]
            lng_diff = loc[0] - closest_ap_coord[1]
            shifted_lat = closest_ap_coord[0] + (pct_move*lat_diff)
            shifted_lng = closest_ap_coord[1] + (pct_move*lng_diff)
            shifted_ap_coord = (shifted_lat, shifted_lng)

            # We remove the s_id and add this APTA
            non_street_name_match_segment_ids.remove(final_segment_id)
            if len(aptas) == 0:
                aptas.append(pd.Series((closest_ap_coord, shifted_ap_coord, path_end_node, final_segment_id, street_name_match, closest_ap_coord_dist)))
            else:
                previous_ap_coord_dist = aptas[0][5]
                if (closest_ap_coord_dist - previous_ap_coord_dist) < alternative_apta_distance_cap:
                    aptas.append(pd.Series((closest_ap_coord, shifted_ap_coord, path_end_node, final_segment_id, street_name_match, closest_ap_coord_dist)))

    return aptas


def featurize_address_ap(lat, lng, ap_data, unique_id):
    aptas = ap_data

    df = []
    for i, apta in enumerate(aptas):
        ap_coords = {"lat": apta[0][0], "lng": apta[0][1]}
        shifted_ap_coords = {"lat": apta[1][0], "lng": apta[1][1]}
        ap_node = apta[2]
        segment_id = apta[3]
        street_name_match = apta[4]
        df.append([i, unique_id, json.dumps(ap_coords), json.dumps(shifted_ap_coords), ap_node, segment_id, street_name_match, apta[5]])

    return pd.DataFrame(df, columns=address_ap_features)
    

def find_graph_crawl_aps(lat, lng, segments, graph, interior_graph_reversed, cc_dict, cc_list, tree, cutoff=1000, num_nearest_sources=4):
    loc = (lng, lat)

    # nodes containing potential APs
    ap_nodes = set()
    ap_nodes_list = []
    
    # segment pairs that identified the potential AP node
    ap_segment_id_pairs = []

    # segments along path from source to AP node
    ap_segments_along_path = []
    
    # number segments in parking area per AP node
    road_segments_in_parking_region_attached_to_ap_node = []
    
    # source index AP node was encountered at
    source_indices_of_ap_nodes = []
    
    sources = get_source_nodes(loc, segments, graph, interior_graph_reversed, cc_dict, cc_list, tree, num_nearest_sources)
    all_nodes_touched = set()

    # Source provides the closest nodes to the lat/lng 
    for j, s in enumerate(sources):
        
        # Don't bother exploring this source if seen before, all paths will already have been traversed
        if s not in all_nodes_touched:
            lengths, paths = nx.single_source_dijkstra(interior_graph_reversed, source=s, weight='length', cutoff=cutoff)

            # For this single source node, what road segments comprise the parking lot.
            segments_from_source = set()

            # This feature will be modified even after an AP node is found, since other paths may contain more
            # road segments increasing the size of the parking lot. Therefore it must be maintained outside the loop
            # below, and we track how many new APs were found that should use this interior_road_region segment set.
            num_new_ap_nodes_from_source = 0


            # The node is the end-point of the graph traversal and the path is the nodes touched starting with source.
            # This loop iterates over all possible paths found originating from the source.
            for node, path in paths.items(): 
                segments_along_path = []

                # Follow a path and identify any APs that arise
                for i, n in enumerate(path):
                    
                    # Indicate a path has used this node before
                    all_nodes_touched.add(n)

                    current_node_id = path[i]
                    
                    if (i == 0):
                        # All transition nodes require two segments except for the scenario in which the closest node
                        # has a regular road attached (which means we stop at this point), but if it also
                        # interior segments, we can plot an AP
                        in_fows = graph.nodes[current_node_id].get('in_fow', [])
                        out_fows = graph.nodes[current_node_id].get('out_fow', [])

                        # Determine the type of transition (regular -> interior or interior -> interior)
                        if "REGULAR_ROAD" in in_fows:
                            in_fows = ["REGULAR_ROAD"]
                        else:
                            in_fows = set(in_fows).intersection(INTERIOR_ROADS)
                        
                        for in_fow in in_fows:
                            for out_fow in set(out_fows).intersection(INTERIOR_ROADS):

                                # A transition occurs which indicates a potential AP
                                if in_fow != out_fow:
                                    incoming_road_index = graph.nodes[current_node_id].get('in_fow').index(in_fow)
                                    prev_seg_id = graph.nodes[current_node_id].get('in_road_ids')[incoming_road_index]

                                    outgoing_road_index = graph.nodes[current_node_id].get('out_fow').index(out_fow)
                                    seg_id = graph.nodes[current_node_id].get('out_road_ids')[outgoing_road_index]

                                    # Add the node
                                    if n not in ap_nodes:
                                        # Add the two road id pairs as transition segments
                                        # - prev_seg_id is the id of the edge that is leading to the entrance/AP node
                                        # - cur_seg_id is the id of the edge going away from the AP node to the node inside the parking lot
                                        #      cur_seg_id can use wkt_geom to shift APs along the edge potentially using likelihood map

                                        # Add the node as an entrance here.
                                        num_new_ap_nodes_from_source += 1
                                        ap_nodes.add(n)
                                        ap_nodes_list.append(n)
                                        
                                        ap_segment_id_pairs.append([prev_seg_id, seg_id])
                                        ap_segments_along_path.append(segments_along_path)
                                        source_indices_of_ap_nodes.append(j)
                                        graph.nodes[n]['potential_ap'] = 1
 
                    elif (i > 0):

                        # Get the edge that connected the previous node and the current node
                        previous_node_id = path[i-1]

                        # Get the edge and the fow of the edge that connects the two above nodes
                        prev_road_in_ids = set(graph.nodes[previous_node_id].get('in_road_ids'))
                        cur_road_out_ids = set(graph.nodes[current_node_id].get('out_road_ids'))
                        seg_id = prev_road_in_ids.intersection(cur_road_out_ids).pop()
                        segments_from_source.add(seg_id)
                        segments_along_path.append(seg_id)

                        # Grab the fow for the segment connecting the current and previous nodes
                        fow_last_segment = segments.loc[seg_id].form_of_way

                        # Check to see if there are any other incoming road types connecting to this node
                        in_fows = graph.nodes[current_node_id].get('in_fow', [])
                        allowable_fows = set(INTERIOR_ROADS).union(set(["REGULAR_ROAD"]))
                        in_fows = set(in_fows).intersection(allowable_fows)
                        
                        # If the value below > 0, indicates a transition occurs at this node.
                        if len(set(in_fows).difference(set([fow_last_segment]))) > 0 and fow_last_segment not in set(NON_NAVIGABLE_ROADS):

                            if "REGULAR_ROAD" in in_fows:
                                # There is a transition at this node indicating an incoming regular road and an outging interior road.
                                # We know the outgoing is interior, since it is the fow of the last segment crawled, and this crawler
                                # would not crawl non-interior roads.
                                other_type = "REGULAR_ROAD"
                            else:
                                # There is an interior-to-interior transition.
                                # Find an/the other road segment with differing road type to complete the pair.
                                # The first 'other' road type is taken, may want to explore a hierarchy
                                other_type = set(in_fows).difference(set([fow_last_segment])).pop()

                            other_road_index = graph.nodes[current_node_id].get('in_fow').index(other_type)
                            prev_seg_id = graph.nodes[current_node_id].get('in_road_ids')[other_road_index]

                            if n not in ap_nodes:
                                # Add the two road id pairs as transition segments
                                # - prev_seg_id is the id of the edge that is leading to the entrance/AP node
                                # - cur_seg_id is the id of the edge going away from the AP node to the node inside the parking lot
                                #      cur_seg_id can use wkt_geom to shift APs along the edge potentially using likelihood map

                                # Add the node as an entrance here.
                                num_new_ap_nodes_from_source += 1
                                ap_nodes.add(n)
                                ap_nodes_list.append(n)
                                ap_segment_id_pairs.append([prev_seg_id, seg_id])
                                ap_segments_along_path.append(segments_along_path)
                                source_indices_of_ap_nodes.append(j)
                                graph.nodes[n]['potential_ap'] = 1

                    # If an incoming road had type regular road, stop the crawl of this path early,
                    # so we don't cross regular roads
                    if "REGULAR_ROAD" in in_fows:
                        break

            # Add the segments from the source node for each new AP added since segments_from_source is not
            # known apriori and must be added once we know all APs from said source.
            for i in range(num_new_ap_nodes_from_source):
                road_segments_in_parking_region_attached_to_ap_node.append(list(segments_from_source))
    
    return pd.Series((ap_nodes_list, ap_segment_id_pairs, ap_segments_along_path,
                      road_segments_in_parking_region_attached_to_ap_node, source_indices_of_ap_nodes))


def find_graph_crawl_exit_aps(lat, lng, segments, graph, interior_graph_reversed, cc_dict, cc_list, tree, cutoff=1000, num_nearest_sources=4):
    loc = (lng, lat)

    # nodes containing potential APs
    ap_nodes = set()
    ap_nodes_list = []

    # segment pairs that identified the potential AP node
    ap_segment_id_pairs = []

    # segments along path from source to AP node
    ap_segments_along_path = []

    # number segments in parking area per AP node
    road_segments_in_parking_region_attached_to_ap_node = []

    # source index AP node was encountered at
    source_indices_of_ap_nodes = []

    sources = get_source_nodes(loc, segments, graph, interior_graph_reversed, cc_dict, cc_list, tree, num_nearest_sources)
    all_nodes_touched = set()
    
    # Source provides the closest nodes to the lat/lng
    for j, s in enumerate(sources):

        # Don't bother exploring this source if seen before, all paths will already have been traversed
        if s not in all_nodes_touched:
            lengths, paths = nx.single_source_dijkstra(interior_graph_reversed, source=s, weight='length', cutoff=cutoff)

            # For this single source node, what road segments comprise the parking lot.
            segments_from_source = set()

            # This feature will be modified even after an AP node is found, since other paths may contain more
            # road segments increasing the size of the parking lot. Therefore it must be maintained outside the loop
            # below, and we track how many new APs were found that should use this interior_road_region segment set.
            num_new_ap_nodes_from_source = 0


            # The node is the end-point of the graph traversal and the path is the nodes touched starting with source.
            # This loop iterates over all possible paths found originating from the source.
            for node, path in paths.items():
                segments_along_path = []

                # Follow a path and identify any APs that arise
                for i, n in enumerate(path):

                    # Indicate a path has used this node before
                    all_nodes_touched.add(n)

                    current_node_id = path[i]

                    if (i == 0):
                        # All transition nodes require two segments except for the scenario in which the closest node
                        # has a regular road attached (which means we stop at this point), but if it also
                        # interior segments, we can plot an AP
                        in_fows = graph.nodes[current_node_id].get('in_fow', [])
                        out_fows = graph.nodes[current_node_id].get('out_fow', [])

                        # Determine the type of transition (regular -> interior or interior -> interior)
                        if "REGULAR_ROAD" in out_fows:
                            out_fows = ["REGULAR_ROAD"]
                        else:
                            out_fows = set(out_fows).intersection(INTERIOR_ROADS)

                        for out_fow in out_fows:
                            for in_fow in set(in_fows).intersection(INTERIOR_ROADS):

                                # A transition occurs which indicates a potential AP
                                if in_fow != out_fow:
                                    incoming_road_index = graph.nodes[current_node_id].get('in_fow').index(in_fow)
                                    prev_seg_id = graph.nodes[current_node_id].get('in_road_ids')[incoming_road_index]

                                    outgoing_road_index = graph.nodes[current_node_id].get('out_fow').index(out_fow)
                                    seg_id = graph.nodes[current_node_id].get('out_road_ids')[outgoing_road_index]

                                    # Add the node
                                    if n not in ap_nodes:
                                        # Add the two road id pairs as transition segments
                                        # - prev_seg_id is the id of the edge that is leading to the entrance/AP node
                                        # - cur_seg_id is the id of the edge going away from the AP node to the node inside the parking lot
                                        #      cur_seg_id can use wkt_geom to shift APs along the edge potentially using likelihood map

                                        # Add the node as an entrance here.
                                        num_new_ap_nodes_from_source += 1
                                        ap_nodes.add(n)
                                        ap_nodes_list.append(n)

                                        ap_segment_id_pairs.append([seg_id, prev_seg_id])
                                        ap_segments_along_path.append(segments_along_path)
                                        source_indices_of_ap_nodes.append(j)
                                        graph.nodes[n]['potential_ap'] = 1

                    elif (i > 0):

                        # Get the edge that connected the previous node and the current node
                        previous_node_id = path[i-1]

                        # Get the edge and the fow of the edge that connects the two above nodes
                        cur_road_in_ids = set(graph.nodes[current_node_id].get('in_road_ids'))
                        prev_road_out_ids = set(graph.nodes[previous_node_id].get('out_road_ids'))
                        seg_id = cur_road_in_ids.intersection(prev_road_out_ids).pop()
                        segments_from_source.add(seg_id)
                        segments_along_path.append(seg_id)
                        
                        # Grab the fow for the segment connecting the current and previous nodes
                        fow_last_segment = segments.loc[seg_id].form_of_way

                        # Check to see if there are any other incoming road types connecting to this node
                        out_fows = graph.nodes[current_node_id].get('out_fow', [])
                        allowable_fows = set(INTERIOR_ROADS).union(set(["REGULAR_ROAD"]))
                        out_fows = set(out_fows).intersection(allowable_fows)

                        # If the value below > 0, indicates a transition occurs at this node.
                        if len(set(out_fows).difference(set([fow_last_segment]))) > 0 and fow_last_segment not in set(NON_NAVIGABLE_ROADS):
                            if "REGULAR_ROAD" in out_fows:
                                # There is a transition at this node indicating an incoming regular road and an outging interior road.
                                # We know the outgoing is interior, since it is the fow of the last segment crawled, and this crawler
                                # would not crawl non-interior roads.
                                other_type = "REGULAR_ROAD"
                            else:
                                # There is an interior-to-interior transition.
                                # Find an/the other road segment with differing road type to complete the pair.
                                # The first 'other' road type is taken, may want to explore a hierarchy
                                other_type = set(out_fows).difference(set([fow_last_segment])).pop()

                            other_road_index = graph.nodes[current_node_id].get('out_fow').index(other_type)
                            outgoing_seg_id = graph.nodes[current_node_id].get('out_road_ids')[other_road_index]

                            if n not in ap_nodes:
                                # Add the two road id pairs as transition segments
                                # - prev_seg_id is the id of the edge that is leading to the entrance/AP node
                                # - cur_seg_id is the id of the edge going away from the AP node to the node inside the parking lot
                                #      cur_seg_id can use wkt_geom to shift APs along the edge potentially using likelihood map

                                # Add the node as an entrance here.
                                num_new_ap_nodes_from_source += 1
                                ap_nodes.add(n)
                                ap_nodes_list.append(n)
                                ap_segment_id_pairs.append([outgoing_seg_id, seg_id])
                                ap_segments_along_path.append(segments_along_path)
                                source_indices_of_ap_nodes.append(j)
                                graph.nodes[n]['potential_ap'] = 1

                        # If an incoming road had type regular road, stop the crawl of this path early,
                        # so we don't cross regular roads
                        if "REGULAR_ROAD" in out_fows:
                            break

            # Add the segments from the source node for each new AP added since segments_from_source is not
            # known apriori and must be added once we know all APs from said source.
            for i in range(num_new_ap_nodes_from_source):
                road_segments_in_parking_region_attached_to_ap_node.append(list(segments_from_source))

    return pd.Series((ap_nodes_list, ap_segment_id_pairs, ap_segments_along_path,
                      road_segments_in_parking_region_attached_to_ap_node, source_indices_of_ap_nodes))


def get_angle_between_points(pivot, coord_1, coord_2):
        np.set_printoptions(suppress=True)
        np.seterr(all='raise')
        angle = 0
        import warnings
        with warnings.catch_warnings():
            try:
                v0 = np.array(coord_1) - np.array(pivot)
                v1 = np.array(coord_2) - np.array(pivot)

                angle = np.degrees(np.math.atan2(np.linalg.det([v0,v1]), np.dot(v0,v1)))
            except TypeError as e:
                print('error found:', e)
                print(pivot)
                print(coord_1)
                print(coord_2)
                # print(pivot)   
                # print(coord_1)    
                # print(coord_2) 
        return abs(angle)


def featurize_graph_crawl_aps(lat, lng, address, ap_data, segments, graph, tree, generated_ap_identifier):
    ap_nodes, ap_transition_segments_at_node, ap_segments_along_path_to_node,\
    segments_in_interior_region_for_node, source_nodes = ap_data

    df = []
    for i in range(len(ap_nodes)):

        # Coordinates of node for which potential AP is at
        ap_coords = {"lat": graph.nodes[ap_nodes[i]]['pos'][1], "lng": graph.nodes[ap_nodes[i]]['pos'][0]}

        parcel_area = 0
        parcel_perimeter = 0
        ap_distance_to_parcel_boundary = 0
        gen_ap_point = Point(ap_coords['lng'], ap_coords['lat'])

        # if address.point_type == 'PARCEL':
        #     try:
        #         polygons = loads(address.wkt_geom)

        #         for poly in polygons.geoms:
        #             parcel_area = poly.area
        #             parcel_perimeter = poly.length
        #             ap_distance_to_parcel_boundary = poly.distance(gen_ap_point)
        #             if ap_distance_to_parcel_boundary == 0:
        #                 ap_distance_to_parcel_boundary = -1 * poly.exterior.distance(gen_ap_point)
        #             break

        #     except:
        #         pass

        # What are the fow of the two segments that comprise the AP at said node
        ap_fow_transition = [segments.loc[ap_transition_segments_at_node[i][0]].form_of_way, segments.loc[ap_transition_segments_at_node[i][1]].form_of_way]

        # What index was the source node the AP node came from
        source_node = source_nodes[i]

        # How far is the node with the potential AP from the POI itself
        distance_from_poi_to_ap = distance((lat, lng), (ap_coords['lat'], ap_coords['lng'])).meters

        # How how many road segments, and distance along said road segments, from source node to node with AP
        ap_distance_traveled = sum([segments.loc[s].haversine_meters for s in ap_segments_along_path_to_node[i]])
        ap_num_segments_traveled = len(ap_segments_along_path_to_node[i])

        # For the road segments between the source node and the AP node, what are the fow encountered?
        #     Can expand this feature below into one-hot of has_fow_road_type_<>, and/or a count of fow
        #     for the precision model.
        ap_segment_traveled_fow_histogram = [segments.loc[s].form_of_way for s in ap_segments_along_path_to_node[i]]

        num_heading_changes_along_segments_traveled = 0
        total_angle_heading_changes_along_segments_traveled = 0
        for j in range(1, len(ap_segments_along_path_to_node[i])):
            prev_seg = ap_segments_along_path_to_node[i][j-1]
            cur_seg = ap_segments_along_path_to_node[i][j]

            prev_wkt_coords = get_wkt_coords(segments.loc[prev_seg])
            cur_wkt_coords = get_wkt_coords(segments.loc[cur_seg])
            pivot = None
            pos1 = None
            pos2 = None
            if prev_wkt_coords[0] == cur_wkt_coords[0]:
                pivot = prev_wkt_coords[0]
                pos1, pos2 = prev_wkt_coords[-1], cur_wkt_coords[-1]

            elif prev_wkt_coords[0] == cur_wkt_coords[-1]:
                pivot = prev_wkt_coords[0]
                pos1, pos2 = prev_wkt_coords[-1], cur_wkt_coords[0]

            elif prev_wkt_coords[-1] == cur_wkt_coords[0]:
                pivot = prev_wkt_coords[-1]
                pos1, pos2 = prev_wkt_coords[0], cur_wkt_coords[-1]

            elif prev_wkt_coords[-1] == cur_wkt_coords[-1]:
                pivot = prev_wkt_coords[-1]
                pos1, pos2 = prev_wkt_coords[0], cur_wkt_coords[0]

            angle = get_angle_between_points(pivot, pos1, pos2)
        
            # 180 degrees - 30 degrees (30 deg is minimum angle to consider it a true heading change)
            min_angle_distance = 30
            if angle < (180 - min_angle_distance):
                num_heading_changes_along_segments_traveled += 1

            total_angle_heading_changes_along_segments_traveled += (180-angle)
        
        avg_angle_heading_changes_along_segments_traveled = 0
        if ap_num_segments_traveled > 0:
            avg_angle_heading_changes_along_segments_traveled = total_angle_heading_changes_along_segments_traveled/ap_num_segments_traveled 

        # How many segments comprise the parking lot of which the potential AP node is a part of
        interior_lot_size = len(segments_in_interior_region_for_node[i])

        # For the road segments in the interior lot region (parking lot) what are the types of fow
        #     Can expand this feature below into one-hot of has_fow_road_type_<>, and/or a count of fow
        #     for the precision model.
        interior_lot_histogram = [segments.loc[s].form_of_way for s in segments_in_interior_region_for_node[i]]

        # What % of incoming edges at the node ap are interior vs. exterior
        pct_incoming_edges_interior_node_ap = sum([1 if s in INTERIOR_ROADS else 0 for s in graph.nodes[ap_nodes[i]]['in_fow']])/\
                                              len(graph.nodes[ap_nodes[i]]['in_fow'])
        pct_incoming_edges_exterior_node_ap = 1 - pct_incoming_edges_interior_node_ap

        # What % of incoming edges at the node ap are interior vs. exterior
        pct_outgoing_edges_interior_node_ap = sum([1 if s in INTERIOR_ROADS else 0 for s in graph.nodes[ap_nodes[i]]['out_fow']])/\
                                              len(graph.nodes[ap_nodes[i]]['out_fow'])
        pct_outgoing_edges_exterior_node_ap = 1 - pct_outgoing_edges_interior_node_ap

        # Perhaps should explore using more than 30 nodes, but this is reasonable for now
        nearest_nodes_for_centrality = 30
        closest_nodes = [str(n) for n in list(tree.nearest(graph.nodes[ap_nodes[i]]['pos'], nearest_nodes_for_centrality))]
        subgraph = graph.subgraph(closest_nodes)

        # Degree centrality measures the importance of a node as a function of the number of edges it has
        #     Local degree centrality is more useful if useful at all
        degree_centralities_subgraph = nx.degree_centrality(subgraph)
        degree_centrality = degree_centralities_subgraph[ap_nodes[i]]

        # Betweenness centrality quantifies the number of times a node acts as a bridge
        # along the shortest path between two other nodes
        #     In the precision model, can plot roc curve as a function of betweeness centrality
        betweenness_centralities_subgraph = nx.betweenness_centrality(subgraph)
        betweenness_centrality = betweenness_centralities_subgraph[ap_nodes[i]]

        # Pagerank centrality
        # pagerank_centralities_subgraph = nx.pagerank(subgraph)
        # pagerank_centrality = pagerank_centralities_subgraph[ap_nodes[i]]

        # Closeness centrality
        closeness_centralities_subgraph = nx.closeness_centrality(subgraph)
        closeness_centrality = closeness_centralities_subgraph[ap_nodes[i]]

        ap = [generated_ap_identifier, ap_nodes[i], source_node, json.dumps(ap_transition_segments_at_node[i]),
              json.dumps(ap_coords), distance_from_poi_to_ap, json.dumps(ap_fow_transition), ap_distance_traveled,
              ap_num_segments_traveled, json.dumps(ap_segment_traveled_fow_histogram),
              interior_lot_size, json.dumps(interior_lot_histogram),
              pct_incoming_edges_interior_node_ap, pct_incoming_edges_exterior_node_ap,
              pct_outgoing_edges_interior_node_ap, pct_outgoing_edges_exterior_node_ap,
              degree_centrality, betweenness_centrality, closeness_centrality,
              num_heading_changes_along_segments_traveled, total_angle_heading_changes_along_segments_traveled,
              avg_angle_heading_changes_along_segments_traveled]
              #  parcel_area, parcel_perimeter,
              # ap_distance_to_parcel_boundary]

        # print("ap = " + ','.join(map(str,ap)))
        df.append(ap)
    return pd.DataFrame(df, columns=ap_features)


def shift_aps(ap, segments, shift_distance = 10):
    ap_coords = eval(ap.ap_coordinates)
    ap_coords = (ap_coords['lat'], ap_coords['lng'])
    shifted_ap_coords = None
    shifted_ap_segment = json.loads(ap.transition_road_segment_ids)[1]
    shifted_ap_segment_wkt = segments.loc[shifted_ap_segment].wkt_geom
    wkt_coords = get_wkt_coords(segments.loc[shifted_ap_segment])
    
    # Need to find the end of the wkt that matches where it touches incoming road
    incoming_ap_segment = json.loads(ap.transition_road_segment_ids)[0]
    incoming_wkt_coords = get_wkt_coords(segments.loc[incoming_ap_segment])
    if not (wkt_coords[0] == incoming_wkt_coords[0] or \
            wkt_coords[0] == incoming_wkt_coords[-1]):
        wkt_coords.reverse()
    
    for i in range(1, len(wkt_coords)):
        dist = distance(wkt_coords[i-1], wkt_coords[i]).m
        if dist < shift_distance:
            shift_distance -= dist
            # If the distance between the first two segments is not large enough
            # continue to the next segment
            continue
        else:
            percent_move = shift_distance/dist
            
            # Get the difference in values
            lat_diff = wkt_coords[i][0] - wkt_coords[i-1][0]
            lng_diff = wkt_coords[i][1] - wkt_coords[i-1][1]
            
            # Add % times difference to starting point
            new_lat = wkt_coords[i-1][0] + (percent_move*lat_diff)
            new_lng = wkt_coords[i-1][1] + (percent_move*lng_diff)
            shifted_ap_coords = {'lat': new_lat, 'lng': new_lng}
            
            # Once shifted position is found, stop
            break

    # If we could not shift desired distance along the WKT, just shift to the end.
    if not shifted_ap_coords:
        shifted_ap_coords = {'lat': wkt_coords[-1][0], 'lng': wkt_coords[-1][1]}
    
    return pd.Series((json.dumps(shifted_ap_coords), shifted_ap_segment, shifted_ap_segment_wkt))


# Helper functions to call generation functions
def find_exit_aps_for_address_points(addresses, segments, graph, interior_graph_reversed, cc_dict, cc_list, tree, log=False, log_step=100):
    potential_access_points_df = pd.DataFrame([], columns=ap_features)

    if log:
        logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
        LOGGER = logging.getLogger(__name__)
    
        LOGGER.info("Generating access points...")

    for i in range(len(addresses)):
        if log:
            if i % log_step == 0:
                LOGGER.info("Processing %s (%.1f%%)", i, float(i)/len(addresses)*100)
    
        lat, lng = addresses.iloc[i].rep_point_lat_y, addresses.iloc[i].rep_point_lng_x
        ap_crawl_data = find_graph_crawl_exit_aps(lat, lng, segments, graph, interior_graph_reversed, cc_dict, cc_list, tree)
        ap_df = featurize_graph_crawl_aps(lat, lng, addresses.iloc[i], ap_crawl_data, segments, graph, tree, addresses.iloc[i].name)
        potential_access_points_df = potential_access_points_df.append(ap_df)

    # Shift the generated access points
    if len(potential_access_points_df) > 0:
        potential_access_points_df[['shifted_ap_coordinates', 'shifted_ap_segment', 'shifted_ap_segment_wkt']] = potential_access_points_df.apply(lambda x: shift_aps(x, segments), axis=1)
    else:
        print("No APs generated at all for entire batch")

    if log:
        LOGGER.info("Access point generation complete!")

    return potential_access_points_df


def generate_vee_aps_for_pois(pois, segments, graph, interior_graph_reversed, cc_dict, cc_list, tree, log=False, log_step=100):
    potential_access_points_df = pd.DataFrame([], columns=ap_features)

    if log:
        logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
        LOGGER = logging.getLogger(__name__)
    
        LOGGER.info("Generating access points...")
    
    for i in range(len(pois)):
        if log:
            if i % log_step == 0:
                LOGGER.info("Processing %s (%.1f%%)", i, float(i)/len(addresses)*100)
    
        lat, lng = pois.iloc[i]['poiLat'], pois.iloc[i]['poiLng']  
        ap_crawl_data = find_graph_crawl_aps(lat, lng, segments, graph, interior_graph_reversed, cc_dict, cc_list, tree)
        ap_df = featurize_graph_crawl_aps(lat, lng, pois.iloc[i], ap_crawl_data, segments, graph, tree, pois.iloc[i]['poiId'])
        potential_access_points_df = potential_access_points_df.append(ap_df)

    # Shift the generated access points
    if len(potential_access_points_df) > 0:
        potential_access_points_df[['shifted_ap_coordinates', 'shifted_ap_segment', 'shifted_ap_segment_wkt']] = potential_access_points_df.apply(lambda x: shift_aps(x, segments), axis=1)
    else:
        print("No APs generated at all for entire batch")    
    
    if log:
        LOGGER.info("Access point generation complete!")
    
    return potential_access_points_df


def generate_address_aps_for_pois(pois, segments, graph, interior_graph_reversed, cc_dict, cc_list, tree, use_poi_street_if_lat_lng_street_null=True, log=False, log_step=100):
    potential_access_points_df = pd.DataFrame([], columns=address_ap_features)

    if log:
        logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
        LOGGER = logging.getLogger(__name__)
    
        LOGGER.info("Generating address access points...")
 
    for i in range(len(pois)):
        if log:   
            if i % log_step == 0:
                LOGGER.info("Processing %s (%.1f%%)", i, float(i)/len(addresses)*100)
    
        lat, lng = pois.iloc[i]['poiLat'], pois.iloc[i]['poiLng']
        addr_street = pois.iloc[i].street

        ap_crawl_data = find_address_based_ap(lat, lng, addr_street, segments, graph, interior_graph_reversed, cc_dict, cc_list, tree)
        ap_df = featurize_address_ap(lat, lng, ap_crawl_data, pois.iloc[i]['poiId'])
        potential_access_points_df = potential_access_points_df.append(ap_df)

    if log:
        LOGGER.info("Address access point generation complete!")
   
    return potential_access_points_df


    
