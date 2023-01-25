###############################################################################
# Copyright 2020 ScPA StarLine Ltd. All Rights Reserved.
#
# Created by Slastnikova Anna <slastnikova02@mail.ru>
# and Rami Al-Naim <alnaim.ri@starline.ru>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
###############################################################################


import math
import argparse
import utm
import sys

from lxml import etree
from io import StringIO

from .road import Node, Way, Relation

from .proto.map import map_pb2

borderTypes = {"UNKNOWN": 0,
               "DOTTED_YELLOW": 1,
               "DOTTED_WHITE": 2,
               "SOLID_YELLOW": 3,
               "SOLID_WHITE": 4,
               "DOUBLE_YELLOW": 5,
               "CURB": 6}


def readNodes(e):
    nodes = {}

    # Read all nodes and their coordinates into an array
    for node in e.findall('node'):
        n = Node(node.get("id"), float(
            node.get("lat")), float(node.get("lon")))

        for tag in node.findall('tag'):
            if tag.get('k') == "lanelet_node_type":
                n.lanelet_node_type = tag.get('v')

        nodes[node.get("id")] = n
    return nodes


def readWays(e, nodes):
    ways = {}

    # Read all roads/ways into an array
    for way in e.findall('way'):
        way_id = way.get("id")
        w = Way(way_id)

        # Read all information about each way
        for tag in way.findall('tag'):
            if tag.get('k') == "type":
                w.type = tag.get('v')
            elif tag.get('k') == "subtype":
                w.subtype = tag.get('v')

        # Get nodes
        way_nodes = way.findall('nd')

        # Connect to the nodes
        for nd in way_nodes:
            node = nodes[nd.get("ref")]
            node.parents.append(w)
            w.nodes.append(node)

        if len(way_nodes) > 0:
            ways[w.id] = w

    return ways


def readRelations(e, ways):
    all_relations = []
    for rel in e.findall('relation'):
        r = Relation(rel.get("id"))
        tag_type = None
        tag_subtype = None
        speed_limit = None
        for tag in rel.findall('tag'):
            if tag.get('k') == "type":
                tag_type = tag.get('v')
            elif tag.get('k') == "subtype":
                tag_subtype = tag.get('v')
            elif tag.get('k') == "speed_limit":
                speed_limit = tag.get('v')

        if tag_type != "lanelet":
            continue

        r.speed_limit = speed_limit

        for member in rel.findall('member'):
            if member.get('type') == "way":
                way = ways[member.get('ref')]

                if member.get('role') == "left":
                    r.left = way
                elif member.get('role') == "right":
                    r.right = way

                way.relations.append(r)

        if r.left is not None and r.right is not None:
            all_relations.append(r)

    return all_relations


def readLanelet2(filename: str = None, xml: StringIO = None):
    if filename is not None:
        lanelet2_map = etree.parse(filename).getroot()
    elif xml is not None:
        lanelet2_map = etree.parse(xml).getroot()
    else:
        return 

    nodes = readNodes(lanelet2_map)
    ways = readWays(lanelet2_map, nodes)
    relations = readRelations(lanelet2_map, ways)

    return relations


def get_border_type(type_stat):

    main_type = max(type_stat, key=type_stat.get)
    secondary_type = max(
        [t for t in type_stat if t != main_type], default=None)
    if main_type is None and secondary_type is None:
        return borderTypes["SOLID_WHITE"]

    result_type = None
    if secondary_type is not None:
        if type_stat[main_type] != type_stat[secondary_type]:
            secondary_type = None

        if secondary_type == 'virtual':
            secondary_type = None

    if secondary_type is not None:
        if main_type in ['virtual']:
            main_type = secondary_type
            secondary_type = None

    if secondary_type is not None:
        if 'curbstone' in main_type or 'curbstone' in secondary_type:
            result_type = "CURB"

        elif 'solid' in main_type or 'solid' in secondary_type:
            result_type = "SOLID_WHITE"

        elif 'dashed' in main_type or 'dashed' in secondary_type:
            result_type = "DOTTED_WHITE"

        elif 'virtual' in main_type or 'virtual' in secondary_type:
            result_type = "UNKNOWN"

        elif 'wall' in main_type or 'wall' in secondary_type:
            result_type = "CURB"

        elif 'other' in main_type or 'other' in secondary_type:
            result_type = "UNKNOWN"

        else:
            result_type = "SOLID_WHITE"

    else:
        if 'curbstone' in main_type:
            result_type = "CURB"

        elif 'solid' in main_type:
            result_type = "SOLID_WHITE"

        elif 'dashed' in main_type:
            result_type = "DOTTED_WHITE"

        elif 'virtual' in main_type:
            result_type = "UNKNOWN"

        elif 'wall' in main_type:
            result_type = "CURB"

        elif 'other' in main_type:
            result_type = "UNKNOWN"

        else:
            result_type = "SOLID_WHITE"

    return borderTypes[result_type]


def way_to_boundary(way):
    points = []
    lanelet_node_type = []
    for node in way.nodes:
        lanelet_node_type.append(node.lanelet_node_type)
        type_stat = dict((i, lanelet_node_type.count(i))
                         for i in lanelet_node_type)
        apollo_border_type = get_border_type(type_stat)

        proj = utm.from_latlon(node.lat, node.lng)[:2]
        points.append([proj[0], proj[1]])
    return apollo_border_type, points


def count_dist_array(p1, p2):
    return count_dist(p1[0], p1[1], p2[0], p2[1])


def count_dist_nodes(n1, n2):
    return count_dist(n1.lat, n1.lng, n2.lat, n2.lng)


def count_dist(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


# c1, c2 - гипотетические первая и последняя точки центральной прямой,
# p - гипотетически первая точка левой границы
# проверяем, что p лежит слева от c1c2
# https://stackoverflow.com/questions/1560492/how-to-tell-whether-a-point-is-to-the-right-or-left-side-of-a-line
def is_left(c1, c2, p):
    return ((c2.lat - c1.lat)*(p.lng - c1.lng) - (c2.lng - c1.lng)*(p.lat - c1.lat)) <= 0


def check_if_correct_dir(left, right):
    lp = [left.nodes[0], left.nodes[-1]]
    rp = [right.nodes[0], right.nodes[-1]]
    if count_dist_nodes(lp[0], rp[0]) <= count_dist_nodes(lp[0], rp[1]):
        pairs = [[lp[0], rp[0]], [lp[1], rp[1]]]
    else:
        pairs = [[lp[0], rp[1]], [lp[1], rp[0]]]

    cp = []

    n = Node("central1")
    n.lat = (pairs[0][0].lat + pairs[0][1].lat) / 2
    n.lng = (pairs[0][0].lng + pairs[0][1].lng) / 2
    cp.append(n)

    n = Node("central2")
    n.lat = (pairs[1][0].lat + pairs[1][1].lat) / 2
    n.lng = (pairs[1][0].lng + pairs[1][1].lng) / 2
    cp.append(n)

    if not is_left(cp[0], cp[1], lp[0]):
        left.nodes.reverse()
        cp.reverse()

    if (count_dist_nodes(left.nodes[0], right.nodes[0]) >
            count_dist_nodes(left.nodes[0], right.nodes[-1])):
        right.nodes.reverse()


#--------------------------------------

def get_node_relations(n):
        n_ways = []
        for p in n.parents:
            n_ways.append(p)

        n_rel = []
        for w in n_ways:
            for r in w.relations:
                n_rel.append(r)
        return n_rel


def get_parent_or_child_id(left, right, parent=True):
    if parent:
        index = 0
    else:
        index = -1

    ln = left.nodes[index]
    ln_rel = get_node_relations(ln)

    rn = right.nodes[index]
    rn_rel = get_node_relations(rn)

    intersected_relations = set(ln_rel) & set(rn_rel)
    return intersected_relations


def add_relations(lane_pb, rel):
    parents = get_parent_or_child_id(rel.left, rel.right, parent=True)
    for parent in parents:
        if parent.id == rel.id:
            continue
        lane_pb.predecessor_id.add().id = parent.id

    children = get_parent_or_child_id(rel.left, rel.right, parent=False)
    for child in children:
        if child.id == rel.id:
            continue
        lane_pb.successor_id.add().id = child.id

#--------------------------------------


def add_road(map_pb, rel):
    road_pb = map_pb.road.add()
    id = "road_" + rel.id
    road_pb.id.id = id
    road_pb.type = 2
    section_pb = road_pb.section.add()
    section_pb.id.id = "1"
    section_pb.lane_id.add().id = rel.id


def buildTxt(relations, filename=None):
    map_pb = map_pb2.Map()
    for rel in relations:
        check_if_correct_dir(rel.left, rel.right)
        lane_pb = map_pb.lane.add()
        lane_pb.id.id = rel.id
        central_curve_pb = lane_pb.central_curve.segment.add()
        left_boundary_pb = lane_pb.left_boundary.curve.segment.add()
        right_boundary_pb = lane_pb.right_boundary.curve.segment.add()

        left_boundary_type, left_boundary_points = way_to_boundary(rel.left)
        right_boundary_type, right_boundary_points = way_to_boundary(rel.right)

        for i in range(len(left_boundary_points)):
            point_pb = left_boundary_pb.line_segment.point.add()
            point_pb.x = left_boundary_points[i][0]
            point_pb.y = left_boundary_points[i][1]

        boundary_type = lane_pb.left_boundary.boundary_type.add()
        boundary_type.s = 0
        boundary_type.types.append(left_boundary_type)

        for i in range(len(right_boundary_points)):
            point_pb = right_boundary_pb.line_segment.point.add()
            point_pb.x = right_boundary_points[i][0]
            point_pb.y = right_boundary_points[i][1]

        boundary_type = lane_pb.right_boundary.boundary_type.add()
        boundary_type.s = 0
        boundary_type.types.append(right_boundary_type)

        # Рассчитываем центральную кривую
        for i in range(min(len(left_boundary_points), len(right_boundary_points))):
            point_pb = central_curve_pb.line_segment.point.add()
            point_pb.x = (
                right_boundary_points[i][0] + left_boundary_points[i][0]) / 2
            point_pb.y = (
                right_boundary_points[i][1] + left_boundary_points[i][1]) / 2

        # Добавляем дополнительную точку в конце центральной прямой, если количество точек не одинаково
        i = len(right_boundary_points) - 1
        j = len(left_boundary_points) - 1
        if i != j:
            point_pb = central_curve_pb.line_segment.point.add()
            point_pb.x = (
                right_boundary_points[i][0] + left_boundary_points[j][0]) / 2
            point_pb.y = (
                right_boundary_points[i][1] + left_boundary_points[j][1]) / 2

        add_relations(lane_pb, rel)
        add_road(map_pb, rel)

    if filename is not None:
        map_file = open(filename, 'w')
        map_file.write(str(map_pb))
        map_file.close()
    else:
        return StringIO(str(map_pb))


def get_AOD_from_LL2_with_console():

    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', help="Input filename")
    parser.add_argument('output_file', help="Output filename")
    args = parser.parse_args()

    if args.input_file:
        input_file = args.input_file

    if args.output_file:
        output_file = args.output_file

    relations = readLanelet2(input_file)
    buildTxt(relations, output_file)


if __name__ == "__main__":
    get_AOD_from_LL2_with_console()
