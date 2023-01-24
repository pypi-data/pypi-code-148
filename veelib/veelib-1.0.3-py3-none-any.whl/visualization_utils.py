import folium
import json
import sys
sys.path.append("/workspace/pyspark-app")

import ndm_road_segment_utils as ndm_utils


def plot_access_point_lat_lng(ap_coordinates, poi_map, color):
    ap_coords = eval(ap_coordinates)
    ap_coords = (ap_coords['lat'], ap_coords['lng'])
    folium.Marker(ap_coords, popup="{}".format(ap_coords), icon=folium.Icon(color=color)).add_to(poi_map)

    return poi_map


def plot_custom_access_points(data, poi_map, color, format_glov=True):
    if type(data) == str:
        data = eval(data)
    
    for ep in data:
        if type(ep) == str:
            ep = eval(ep)

        if format_glov:
            if ep['type'] == 'DRIVING':
                coord = (ep['point']['lat'], ep['point']['lng'])
                folium.Marker(coord, popup="{}".format(coord), icon=folium.Icon(color=color)).add_to(poi_map)  
        else:
            coord = (ep['lat'], ep['lng'])
            folium.Marker(coord, popup="{}".format(coord), icon=folium.Icon(color=color)).add_to(poi_map)  
    
    return poi_map


def process_access_points(data):
    res = set()
    try: 
        entries = json.loads(data)
        for accs_pt in entries:
            if accs_pt['type'] == 'DRIVING':
                location = (accs_pt['point']['lat'], accs_pt['point']['lng'])
                res.add(location) 
    except:
        pass

    return res


def map_single_address(address, access_points, plot_entries=True):
    center = (address.rep_point_lat_y, address.rep_point_lng_x)
    name = address.name

    m = folium.Map(
        tiles='http://imagery.geo.apple.com/tile?v=prod&style=7&z={z}&x={x}&y={y}',
        location=center,
        zoom_start=17,
        attr='Apple Map',
        detect_retina=True
    )
    if plot_entries:
        for i, accs_pt in access_points.iterrows():   
            coords = ndm_utils.get_wkt_coords(accs_pt)
            folium.Marker(coords[0], popup="{}".format(accs_pt), icon=folium.Icon(color='blue')).add_to(m)

    folium.RegularPolygonMarker(center, number_of_sides=6, radius=6, fill_opacity=0.6, color='blue',
                                popup="{} {}".format(address.name, center)).add_to(m)
    return m


def process_access_points_w_threshold(data, threshold):
    res = set()
    res_bad = set()
    try: 
        entries = json.loads(data)
        for accs_pt in entries:
            if accs_pt['type'] == 'DRIVING':
                location = (accs_pt['point']['lat'], accs_pt['point']['lng'])
                if accs_pt['model_score'] >= threshold:
                    res.add(location) 
                else:
                    res_bad.add(location)
    except Exception as e:
        print(e)
        pass

    return res, res_bad


def process_existing_aps(data):
    res = set()
    try:
        entries = json.loads(data)
        for ap in entries:
            if 'ENTRY' in ap['road_access_point']['drivingDirection']:
                location =(ap['road_access_point']['location']['lat'], ap['road_access_point']['location']['lng'])
                res.add(location)
    except Exception as e:
        print(e)
        pass
    print(res)
    return res



def map_single_poi_w_threshold(poi, threshold, include_existing=False):
    center = (poi.lat, poi.lng)
    name = poi.poi_id
    selected_entries_poi, not_selected = process_access_points_w_threshold(poi.selected_aps, threshold)
    existing_aps = process_existing_aps(poi.access_point)

    m = folium.Map(
        tiles='http://imagery.geo.apple.com/tile?v=prod&style=7&z={z}&x={x}&y={y}',
        location=center,
        zoom_start=17,
        attr='Apple Map',
        detect_retina=True
    )
    for s_pt in selected_entries_poi:
        folium.Marker(s_pt, popup="{}".format(s_pt), icon=folium.Icon(color='green')).add_to(m)

    for b_pt in not_selected:
        folium.Marker(b_pt, popup="{}".format(b_pt), icon=folium.Icon(color='red')).add_to(m)
  
    if include_existing:
        for e_pt in existing_aps:
            folium.Marker(e_pt, popup="{}".format(e_pt), icon=folium.Icon(color='lightblue')).add_to(m)
      

    folium.RegularPolygonMarker(center, number_of_sides=6, radius=6, fill_opacity=0.6, color='blue', 
                                popup="{} {}".format(name, center)).add_to(m)    
    return m


def map_single_poi(poi, plot_entries=True, plot_correct=False, plot_selected=False):
    center = (poi.poiLat, poi.poiLng)
    name = poi.poiId
    unselected_entries_poi = process_access_points(poi.l)
    selected_entries_poi = process_access_points(poi.selected_aps)

    m = folium.Map(
        tiles='http://imagery.geo.apple.com/tile?v=prod&style=7&z={z}&x={x}&y={y}',
        location=center,
        zoom_start=17,
        attr='Apple Map',
        detect_retina=True
    )
    for accs_pt in entries_poi:
        folium.Marker(accs_pt, popup="{}".format(accs_pt), icon=folium.Icon(color='blue')).add_to(m)
  
    for s_pt in selected_entries_poi:
        folium.Marker(s_pt, popup="{}".format(s_pt), icon=folium.Icon(color='green')).add_to(m)

    for c_pt in correct_entries_poi:
        folium.Marker(c_pt, popup="{}".format(c_pt), icon=folium.Icon(color='white')).add_to(m)
  

    folium.RegularPolygonMarker(center, number_of_sides=6, radius=6, fill_opacity=0.6, color='blue', 
                                popup="{} {}".format(name, center)).add_to(m)    
    return m