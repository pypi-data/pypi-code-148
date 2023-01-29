
import xml.etree.ElementTree as ET
import numpy as np
import copy
import math
import os










class xodrStaticWorld():
    """
        Representing the static world of dataset

        

        Notice: This implementation is only a very basic xodr-reader. 
        Its just handling the basic functionality needed for the current state of 
        automatum-data datasets.

        :param path2XODR: Path to a xodr file. 

        :var roads: A List of roads contained in the xodr. Roads are represtend by ``xodrRoad``.

    """

    def __init__(self, path2XODR, sampleWidth=1.0):
        """
            Init function. 
        """
        self.roads = list()

        if(not os.path.isfile(path2XODR)):
            raise FileNotFoundError("The xodr-file could not be found under: %s" % path2XODR)
        tree = ET.parse(path2XODR)
        root = tree.getroot()
        for child in root:
            if "road" in child.tag:
                self.roads.append(xodrRoad(self, child, sampleWidth=sampleWidth))



    def get_lane_marking_dicts(self, with_centerline=False):
        """
        This functions returns all lane markings of the static world. 

        Therefore, a list of line samplings, e.g. for plotting is created.

        The format of the return type is:
        [{x_vec: [...], y_vec: [...], type: "borken", color: "white", width: 0.12}, 
        {x_vec: [...], y_vec: [...], type: "solid",  color: "white", width: 0.12},
        .
        .
        .
        {x_vec: [...], y_vec: [...], type: "solid",  color: "white", width: 0.12},
        ]
        
        Types:
        
        * solid: Solid lane marking
        * dashed: Dashed lane marking
        * center_line: Center line fo the corresponding road element

        with_centerline: controles if the center line is included in the list of lines, or if only real road markings are returned

        """
        allLineList = list()
        for road in self.roads:
            allLineList = allLineList + road.get_lane_marking_dicts(with_centerline)
        
        return allLineList

    def get_road(self, road_id):
        """Returns the road by a given ID

        :param road_id: _description_
        :type road_id: _type_
        :return: _description_
        :rtype: _type_
        """
        for road in self.roads:
            if(road.id == road_id):
                return road

        return None

class xodrMiddleLine():
    """This Class represents the middle lane between both sides of the road. 

    :var x_vec: Vector of x position
    :var y_vec: Vector of y position
    :var offset: Lateral offset between the original reference line and the Middle line. 
    
    
    """

    def __init__(self, parent):

        self.s_vec = list()
        self.x_vec_center_line = list()
        self.y_vec_center_line = list()
        self.offset_vec = list()
        self.geo_vec = list()

        self.parent = parent 

        # Actual Render Data
        self.x_vec = list()
        self.y_vec = list() 
        self.off_vec = list()
        self.theta_vec = list()

    def add_discrete_reference_line_point(self, s, x, y, off, geo):
        self.s_vec.append(s)
        self.x_vec_center_line.append(x)
        self.y_vec_center_line.append(y)
        self.offset_vec.append(off)
        self.geo_vec.append(geo)
        

    def sample_me(self):
        self.s_vec = copy.copy(self.s_vec)


        if(len(self.s_vec) != len(self.offset_vec) and len(self.s_vec) != len(self.offset_vec) and len(self.s_vec) != len(self.x_vec_center_line) and len(self.s_vec) != len(self.y_vec_center_line)):
            raise Exception("Render of Lane, not all input values the same size")

        for index, (s_sample, x_pos_ref_line, y_pos_ref_line, off_value, geo_ref_line) in enumerate(zip(self.s_vec, self.x_vec_center_line, self.y_vec_center_line, self.offset_vec, self.geo_vec)):
            
            if(index == 0 or last_geo != geo_ref_line):
                segmentAngle = geo_ref_line.hdg + np.pi 
            else:
                dx = self.x_vec_center_line[index - 1] - x_pos_ref_line
                dy = self.y_vec_center_line[index - 1] - y_pos_ref_line
                if(abs(dx) < 0.0001 and abs(dy) < 0.0001):
                    
                    segmentAngle = geo_ref_line.hdg + np.pi 
                    if(abs(segmentAngle - self.theta_vec[index - 1]) < 0.001):
                        raise Exception("Inconsitcy in heading of roads")
                else:
                    segmentAngle = math.atan2(dy, dx)
            last_geo = geo_ref_line


            theta = (segmentAngle - np.pi / 2)

            c, s = np.cos(theta), np.sin(theta)
            R = np.array(((c, -s), (s, c)))

            lineVec = np.matmul(R, np.array([1, 0])) * off_value
            self.theta_vec.append(theta)
            self.x_vec.append(x_pos_ref_line + lineVec[0])
            self.y_vec.append(y_pos_ref_line + lineVec[1])


    def get_lane_marking_dicts(self):
        """ Returns the lane marking plotting vector for the center line"""
        if(self.s_vec is None):
            raise Exception("Please call sample_me before activating the plotting")

        return [{"x_vec": list(self.x_vec), "y_vec": list(self.y_vec), "type": "centerline", "color": "white", "width": 0.12}]


class xodrRoad():
    """
        This class represents a road.

        :param roadXML: XML-Tree of a road element
        :param sampleWidth: Sample width that is used to calculate a plotable representation of the xodr.

        :var name: Name of th road 
        :var length: Length of the road
        :var id: ID of Road (Currently unused, since automatum-data currently constit of one road)
        :var junction: Information about Junctions (Currently unused, since automatum-data currently constit of one road)
        :var geometry: Representation of reference line 
        :var lanesections: Object that represents all lanes 

    """

    def __init__(self, parent, roadXML, sampleWidth=1.0):
        """
            Inits a Road element and decodes the given roadxml tree. 
            Aditionally the sampling is triggered. 
        """

        self.parent = parent
        self.name = roadXML.attrib['name']
        self.length = float(roadXML.attrib['length'])
        self.id = int(roadXML.attrib['id'])
        self.junction = int(roadXML.attrib['junction'])
        self.predecessor = None
        self.successor = None

        self.geometry = list()
        self.middle_lines = list()
        self.lanesections = list()
        self.lane_offset = list()
        geometry_found = False
        for child in roadXML:
            if "planView" in child.tag:
                for geoChild in child:
                    if "geometry" in geoChild.tag:
                        geometry_found = True
                        self.geometry.append(xodrGeometry.create_geo_obj(geoChild))
                        self.middle_lines.append(xodrMiddleLine(self))
                    else:
                        raise Exception("Unexpected XODR Format: Expected geometry, however given is %s" % geoChild.tag)


            first_lane_section = True
            if "lanes" in child.tag:
                for idx, laneChild in enumerate(child):
                    last_lane_section = idx == (len(child) - 1)
                    if "laneSection" in laneChild.tag:
                        try:
                            self.lanesections.append(xodrLaneSection(laneChild, first_lane_section=first_lane_section, last_lane_section=last_lane_section))
                            first_lane_section = False
                        except Exception as e:
                            raise Exception("While loading the lanes of road %d the following error occurs: %s" % (self.id, str(e)))
                    elif "laneOffset" in laneChild.tag:
                        self.lane_offset.append(xodrLaneOffset(laneChild))

                    else:
                        raise Exception("Unexpected XODR Format: Expected geometry, however given is %s" % laneChild.tag)

            if "link" in child.tag:
                for link_child in child:
                    if "predecessor" in link_child.tag:
                        self.predecessor = {"elementType": link_child.attrib["elementType"], 
                                            "elementId": int(link_child.attrib["elementId"])}
                        if('contactPoint' in link_child.attrib):
                            self.predecessor["contactPoint"] = link_child.attrib["contactPoint"]                                               
                    if "successor" in link_child.tag:
                        self.successor = {"elementType": link_child.attrib["elementType"], 
                                          "elementId": int(link_child.attrib["elementId"])}   
                        if('contactPoint' in link_child.attrib):
                            self.successor["contactPoint"] = link_child.attrib["contactPoint"]                                         
        
        if(not geometry_found):
            raise Exception("Unexpected XODR Format: Expected planView in road %s" % (self.name))
        self.sample_me(sampleWidth)



    
    def get_lane_marking_dicts(self, with_centerline=True):
        """
        This functions returns all lane markings corresponding to this static world object.

        Therefore, a list of line samplings, e.g. for plotting is created.

        The format of the return type is:
        [{x_vec: [...], y_vec: [...], type: "borken", color: "white", width: 0.12}, 
        {x_vec: [...], y_vec: [...], type: "solid",  color: "white", width: 0.12},
        .
        .
        .
        {x_vec: [...], y_vec: [...], type: "solid",  color: "white", width: 0.12},
        ]

        Types:

        * solid: Solid lane marking
        * dashed: Dashed lane marking
        * center_line: Center line fo the corresponding road element
            
        """

        lineList = list()
        if(with_centerline): 
            for geo in self.geometry:
                lineList += geo.get_lane_marking_dicts()
        for middle_line in self.middle_lines:
            lineList += middle_line.get_lane_marking_dicts() 
        
        for laneSec in self.lanesections:
            lineList += laneSec.get_lane_marking_dicts()

        return lineList


    def get_lane_offset(self, s):
        """Return the lane offset


        """
        lane_offset_for_given_s = 0.0
        for idx, lane_offset in enumerate(self.lane_offset):
            if(idx + 1 < len(self.lane_offset)):
                next_lane_offset = self.lane_offset[idx + 1]
                before_next_lane_offset = s < next_lane_offset.s
            else: 
                before_next_lane_offset = True

            if(s >= lane_offset.s and before_next_lane_offset):
                lane_offset_for_given_s = lane_offset.get_offset(s)
        return lane_offset_for_given_s


    def sample_me(self, sampleWidth):
        """ Calculates the sampled value (point vector) of this static world element. """

        for geo, middle_line in zip(self.geometry, self.middle_lines):
            geo.sample_me(sampleWidth)

            for s_value, x_value, y_value in zip(geo.s_vec, geo.x_vec, geo.y_vec):

                for idx, lane_sec in enumerate(self.lanesections):
                    if(idx + 1 < len(self.lanesections)):
                        next_lane_sec = self.lanesections[idx + 1]
                    else:
                        next_lane_sec = None
                    offset = self.get_lane_offset(s_value)
                    lane_sec.check_if_s_value_is_relevant_and_add(s_value, offset, x_value, y_value, geo, next_lane_sec)
                    middle_line.add_discrete_reference_line_point(s_value, x_value, y_value, offset, geo)
            middle_line.sample_me()
        for lane_sec in self.lanesections:
            lane_sec.sample_me(geo)            

    def __str__(self):
        """ Overwrite to string method"""
        return "Road %s length %.2f, ID: %d, Junction: %d" % (self.name, self.length, self.id, self.junction)


class xodrLaneOffset():
    """Defines a Lane offset for a road  
    """

    def __init__(self, lane_offset_XML):
        self.s = float(lane_offset_XML.attrib["s"])
        self.a = float(lane_offset_XML.attrib["a"])
        self.b = float(lane_offset_XML.attrib["b"])
        self.c = float(lane_offset_XML.attrib["c"])
        self.d = float(lane_offset_XML.attrib["d"])


    def get_offset(self, s):
        """Returns the offset for a given distance
        """

        if(s < self.s):
            raise Exception("The given s %f is smaller than the start s of the offset function")

        s_offset_free = s - self.s
        return self.a + self.b * s_offset_free + self.c * s_offset_free**2 + self.d * s_offset_free**3 


    def is_offset_relevant(self, s):
        """Returns ture if the given distance s is behind the start value of the lane offset 

        """
        return s >= self.s
        
class xodrLaneSection():
    """
        Defines a XODR laneSection thats holds a number of lanes. 

        :param xmlLaneSection: xmlTree of a lane section

        :var s: Length of this lane section element along the reference line
        :var lane: List of lane elements which belong to this lane section
        :var first_lane_section: True if this lane section is the first one in the road
        :var last_lane_section: True if this lane section is the last one in the road
    """
    def __init__(self, xmlLaneSection, first_lane_section=True, last_lane_section=True):
        """ Decodes the xmlTree of a LaneSection"""
        self.s = float(xmlLaneSection.attrib['s'])
        self.first_lane_section = first_lane_section
        self.last_lane_section = last_lane_section
        self.s_vec = list()
        self.off_vec = list()
        self.x_ref_line = list()
        self.y_ref_line = list()
        self.geo_ref_line = list()
        self.lanes = list()

        for child in xmlLaneSection:
            if("right" in child.tag or "left" in child.tag):
                for leftrightLanes in child:
                    if "lane" in leftrightLanes.tag:
                        new_lane = xodrLane(leftrightLanes)
                        self.lanes.append(new_lane)
                        if(not first_lane_section and new_lane.predecessor is not None and new_lane.id != new_lane.predecessor):
                            raise Exception("A transition of the predecessor lane id (%d to %d) on the lane section (s: %f) within a road is not allowed" % (new_lane.id, new_lane.predecessor, self.s))
                        if(not last_lane_section and new_lane.successor is not None and new_lane.id != new_lane.successor):
                            raise Exception("A transition of the successor lane id (%d to %d) on the lane section (s: %f) within a road is not allowed" % (new_lane.id, new_lane.successor, self.s))

                    else:
                        raise Exception("Unexpected XODR Format: Expectation lane, given %s" % child.tag)



    def get_lane_id(self, d, l, lane_offset=0):
        """Returns the lane_id for a given point, defined by the distance l along the reference line 
        and the orthogonal distance from the reference line. 

        :param d: Orthogonal distance from reference line (signed according definition in xodr)
        :param l: Distance along the reference line
        :param lane_offset: A general Offset of this lane section compared to the center line 

        :return: Id of the lane (0 if out of range)
        """

        posLines = list()
        negLines = list()

        for lane in self.lanes:
            if(lane.id < 0):
                negLines.append(lane)
            else:
                posLines.append(lane)

        negLines.sort()
        negLines.reverse()

        posLines.sort()
        l_normed = l - self.s
        d_normed = d - lane_offset
        if(d_normed > 0):
            curr_lane_offset = 0
            for idx, lane in enumerate(posLines):
                if(idx == 0):
                    curr_lane_offset += lane_offset
                curr_lane_width = lane.get_lane_width(l_normed, consider_sign=True)
                curr_lane_offset += curr_lane_width
                if(curr_lane_offset >= d):
                    return lane.id

        if(d_normed < 0):
            curr_lane_offset = 0
            for idx, lane in enumerate(negLines):
                if(idx == 0):
                    curr_lane_offset += lane_offset 
                curr_lane_width = lane.get_lane_width(l_normed, consider_sign=True)
                curr_lane_offset += curr_lane_width
                if(curr_lane_offset <= d):
                    return lane.id

        
        return 0


    def __str__(self):
        """
            Overwrites str()
        """
        return "LaneSection: s: %.2f, x: %.2f, y: %.2f, hgd: %.2f, length %.2f" % (self.s, self.x, self.y, self.hdg, self.length)

    def check_if_s_value_is_relevant_and_add(self, s, off_value, x_ref_line, y_ref_line, geo_element, suc_lane_section):
        """Adds a new value for sampling the lane to the s_vec

        """
        relevant_based_on_suc = suc_lane_section is None or s < suc_lane_section.s
        relevant_based_on_cur = s >= self.s
        if(relevant_based_on_suc and relevant_based_on_cur):

            self.s_vec.append(s)
            self.off_vec.append(off_value)
            self.x_ref_line.append(x_ref_line)
            self.y_ref_line.append(y_ref_line)
            self.geo_ref_line.append(geo_element)
        

        

    def get_lane_marking_dicts(self):
        """
        This functions returns all lane markings corresponding to this static world object.

        Therefore, a list of line samplings, e.g. for plotting is created.

        The format of the return type is:
        [{x_vec: [...], y_vec: [...], type: "borken", color: "white", width: 0.12}, 
        {x_vec: [...], y_vec: [...], type: "solid",  color: "white", width: 0.12},
        .
        .
        .
        {x_vec: [...], y_vec: [...], type: "solid",  color: "white", width: 0.12},
        ]

        Types:
        
        * solid: Solid lane marking
        * dashed: Dashed lane marking
        * center_line: Center line fo the corresponding road element
            
        """        
        lineList = list()
        for lane in self.lanes:   
            lineList += lane.get_lane_marking_dicts()
        return lineList

    def sample_me(self, geo):
        """ Samples this geometry object """        
        posLines = list()
        negLines = list()

        for lane in self.lanes:
            if(lane.id < 0):
                negLines.append(lane)
            else:
                posLines.append(lane)

        negLines.sort()
        negLines.reverse()

        posLines.sort()

        
        lastLane = None
        for lane in posLines:
            lane.sample_me(self.s_vec, self.off_vec, self.x_ref_line, self.y_ref_line, self.geo_ref_line, self.s, innerLane=lastLane)
            lastLane = lane


        lastLane = None
        for lane in negLines:
            lane.sample_me(self.s_vec, self.off_vec, self.x_ref_line, self.y_ref_line, self.geo_ref_line, self.s, innerLane=lastLane)
            lastLane = lane



            

    def get_lane(self, lane_id):
        """Returns the lane object for the given lane_id.
        """
        for lane in self.lanes:
            if(lane.id == lane_id):
                return lane
        return None

class xodrLaneWidth():


    def __init__(self, xmlLaneWidth):

        self.s = float(xmlLaneWidth.attrib['sOffset'])
        self.a = float(xmlLaneWidth.attrib['a'])
        self.b = float(xmlLaneWidth.attrib['b'])
        self.c = float(xmlLaneWidth.attrib['c'])
        self.d = float(xmlLaneWidth.attrib['d'])



    def get_lane_width(self, s):
        if(s < self.s):
            raise Exception("This lane width definition is not applied to the given s %f" % s)
        ds = s - self.s
        lane_width = self.a + self.b * ds + self.c * ds * ds + self.d * ds * ds * ds 
        return lane_width


class xodrLane():
    """
        Represents a XODR lane


        :param xmlLane: xmlTree of a lane

        :var id: ID of the Lane
        :var type: Type of the lane, e.g. drivable or shoulder
        :var width: Dict with all primate's of a third order polynom to define the width of the lane
        :var roadmark: Dict of further information of road marks (Not completely set in automatum data)
        :var material: Dict of further information of road material (Not set in automatum data)
        :var speed: Dict of further information of speed limits (Not set in automatum data)

    """
    def __init__(self, xmlLane):
        """Init function 

        :param xmlLane: xmlTree of a lane
        """
        self.id = int(xmlLane.attrib['id'])
        self.type = xmlLane.attrib['type']
        self.width_list = list()
        self.roadmark = dict()
        self.material = dict()
        self.speed = dict()

        self.s_vec = list()
        self.x_vec = list()
        self.y_vec = list()
        self.theta_vec = list()
        self.lane_width_vec = list()
        self.lateral_offset_vec = list()
        self.predecessor = None
        self.successor = None

        for laneChild in xmlLane:
            if("width" in laneChild.tag):
                self.width_list.append(xodrLaneWidth(laneChild))

            if("link" in laneChild.tag):
                for link_child in laneChild:
                    if("predecessor" in link_child.tag):
                        if(self.predecessor is not None):
                            raise Exception("The lane %d has multiple predecessor, which is not allowed" % self.id)
                        self.predecessor = int(link_child.attrib['id'])
                    if("successor" in link_child.tag):
                        if(self.successor is not None):
                            raise Exception("The lane %d has multiple successor, which is not allowed" % self.id)                        
                        self.successor = int(link_child.attrib['id'])
        
            if("roadMark" in laneChild.tag and (laneChild.attrib['type'] == "broken" or laneChild.attrib['type'] == "solid")):
                self.roadmark['sOffset'] = float(laneChild.attrib['sOffset'])
                self.roadmark['type'] = laneChild.attrib['type']
                self.roadmark['color'] = laneChild.attrib['color']
                self.roadmark['width'] = float(laneChild.attrib['width'])
                self.roadmark['height'] = float(laneChild.attrib['height'])
              
            if(len(self.material) == 0 and "material" in laneChild.tag):        
                self.material['sOffset'] = float(laneChild.attrib['sOffset'])
                self.material['friction'] = laneChild.attrib['friction']

            if(len(self.speed) == 0 and "speed" in laneChild.tag):        
                self.speed['sOffset'] = float(laneChild.attrib['sOffset'])
                self.speed['max'] = float(laneChild.attrib['max'])
                self.speed['unit'] = laneChild.attrib['unit']

        if(len(self.roadmark) == 0):
            self.roadmark['sOffset'] = 0.0
            self.roadmark['type'] = "unknown"
            self.roadmark['color'] = "unknown"
            self.roadmark['width'] = 0.0
            self.roadmark['height'] = 0.0

    def __lt__(self, other):
        """ Overwrite Compare operator to enable sorting of lines elements"""
        return self.id < other.id

    def get_lane_width(self, s, consider_sign=True):
        """Returns the lane_width of the lane on a defined position of s 

        :param s: Distance along the lane, started by current lane section
        :param consider_sign: If True the sign is considered (negative if lane id is negative)

        :return: Lateral offset of lane 

        """
        lane_width_found = False
        if(consider_sign):
            sign_of_lane = np.sign(self.id)
        else:
            sign_of_lane = 1

        
        for width_index, width in enumerate(self.width_list):
            if(width_index + 1 < len(self.width_list)):
                next_width_element_fits = s < self.width_list[width_index + 1].s
            else:
                # We have no next width element, so the current is applied for all given distance
                next_width_element_fits = True

            if(s >= width.s and next_width_element_fits):
                lane_width_results = width.get_lane_width(s)
                lane_width_found = True

        if(not lane_width_found):
            raise Exception("No Defined lane with for given distance %s " % s)

        return sign_of_lane * lane_width_results

    def sample_me(self, s_vec, off_vec, x_vec, y_vec, geo_vec, s_offset, innerLane=None):
        """ Samples this geometry object """  
        self.s_vec = copy.copy(s_vec)


        if(len(s_vec) != len(off_vec) and len(s_vec) != len(off_vec) and len(s_vec) != len(x_vec) and len(s_vec) != len(y_vec)):
            raise Exception("Render of Lane, not all input values the same size")
        last_geo = geo_vec[0]
        for index, (s_sample, x_pos_ref_line, y_pos_ref_line, off_value, geo_ref_line) in enumerate(zip(s_vec, x_vec, y_vec, off_vec, geo_vec)):
            ds = s_sample - s_offset
            


            lane_width = self.get_lane_width(ds, consider_sign=False)
            self.lane_width_vec.append(lane_width)

            
            if(innerLane is None):
                if self.id > 0:
                    lateral_offset = off_value + lane_width
                else:

                    lateral_offset = -off_value + lane_width
            else:
                lateral_offset = lane_width + innerLane.lateral_offset_vec[index]


            self.lateral_offset_vec.append(lateral_offset)
            
            if(index == 0 or last_geo != geo_ref_line):
                segmentAngle = geo_ref_line.hdg + np.pi 

        
            else:
                dx = x_vec[index - 1] - x_pos_ref_line
                dy = y_vec[index - 1] - y_pos_ref_line
                if(abs(dx) < 0.0001 and abs(dy) < 0.0001):
                    
                    segmentAngle = geo_ref_line.hdg + np.pi 
                    if(abs(segmentAngle - self.theta_vec[index - 1]) < 0.001):
                        raise Exception("Inconsitcy in heading of roads")
                else:
                    segmentAngle = math.atan2(dy, dx)
            last_geo = geo_ref_line

            if self.id > 0:
                theta = (segmentAngle - np.pi / 2)
            else:
                theta = (segmentAngle + np.pi / 2)

            c, s = np.cos(theta), np.sin(theta)
            R = np.array(((c, -s), (s, c)))

            lineVec = np.matmul(R, np.array([1, 0])) * lateral_offset
            self.theta_vec.append(theta)
            self.x_vec.append(x_pos_ref_line + lineVec[0])
            self.y_vec.append(y_pos_ref_line + lineVec[1])


        

    def get_lane_marking_dicts(self):
        """
        This functions returns all lane markings corresponding to this static world object.

        Therefore, a list of line samplings, e.g. for plotting is created.

        The format of the return type is:
        [{x_vec: [...], y_vec: [...], type: "borken", color: "white", width: 0.12}, 
        {x_vec: [...], y_vec: [...], type: "solid",  color: "white", width: 0.12},
        .
        .
        .
        {x_vec: [...], y_vec: [...], type: "solid",  color: "white", width: 0.12},
        ]

        Types:
        
        * solid: Solid lane marking
        * dashed: Dashed lane marking
        * center_line: Center line fo the corresponding road element
            
        """              
        if(self.s_vec is None):
            raise Exception("Please call sample_me before activating the plotting")

        return [{"x_vec": self.x_vec, "y_vec": self.y_vec, "type": self.roadmark['type'], "color": self.roadmark['color'], "width": self.roadmark['width']}]







class xodrGeometry():
    """
        Main class for all further geometry objects. 

        Based on xodr specification the following forms are supported by the corresponding child classes: 

        * Straight Line by ``xodrGeometryLine``
        * Arc by ``xodrGeometryCurvature``
        * Spiral (not implemented)
        * Cubic polynom (not implemented)
        * Parametric cubic curve (not implemented)

        :param xmlGeometry: xmlTree of a geometry object

        :var s: Start distance of the Geometry 
        :var x: Coordinate system x-position
        :var y:  Coordinate system y-position
        :var hdg:  Coordinate system heading
        :var length: Relevant length of the geometry object
    """
    def __init__(self, xmlGeometry):
        """
            Init function that decodes the given xmlTree
            
            
        """
        self.s = float(xmlGeometry.attrib['s'])
        self.x = float(xmlGeometry.attrib['x'])
        self.y = float(xmlGeometry.attrib['y'])
        self.hdg = float(xmlGeometry.attrib['hdg'])
        self.length = float(xmlGeometry.attrib['length'])

        self.s_vec = None
        self.x_vec = None
        self.y_vec = None

    @staticmethod
    def create_geo_obj(xmlGeometry):
        """
            Object factory thats create the correct child class
        """
        if("line" in xmlGeometry[0].tag):
            return xodrGeometryLine(xmlGeometry)
        elif("arc" in xmlGeometry[0].tag):
            return xodrGeometryCurvature(xmlGeometry)
        elif("paramPoly3" in xmlGeometry[0].tag):
            return xodrGeometryPoly3(xmlGeometry)
        else: 
            raise Exception("Geometry Format %s is not supported yet." % xmlGeometry[0].tag)


    def sample_me(self, sampleWidth):
        """ Sample of geometry object have to be overwritten by the child class"""
        raise NotImplementedError("Have to be overwritten by child class")




    def __lt__(self, other):
        """Overwrite left operator to enable a sorting based on start distance s
        """
        return self.s < other.s


class xodrGeometryCurvature(xodrGeometry):
    """ Geometry Class for a XODR Curvature

    Overwrites the base class ``xodrGeometry``

    :param xmlGeometry: xmlTree of a geometry object

    :var curvature: Curvature of the reference line
    """
    def __init__(self, xmlGeometry):
        """ Reads the Curvature relevant parameter and call the main class"""


        xodrGeometry.__init__(self, xmlGeometry) 
        self.curvature = float(xmlGeometry[0].attrib['curvature'])


    def __str__(self):
        return "Curvature: curvature: %.2f, s: %.2f, x: %.2f, y: %.2f, hgd: %.2f, length %.2f" % (self.curvature, self.s, self.x, self.y, self.hdg, self.length)

    def sample_me(self, sampleWidth):  
        """ Samples this geometry object """
        self.s_vec = np.arange(self.s, self.s + self.length, sampleWidth)
        if(self.s_vec[-1] > self.s + self.length):
            raise Exception("The S-Vec is larger than the actual road element")
        elif(self.s_vec[-1] < self.s + self.length):
            self.s_vec = np.append(self.s_vec, self.s + self.length)


        d_psi = 0
        x_vec_local = [0]
        y_vec_local = [0]      
        last_s_sample = 0  
        for index, s_sample in enumerate(self.s_vec):

            if(index == 0):
                delta_sample_width = 0
            else:
                delta_sample_width = s_sample - last_s_sample
            last_s_sample = s_sample
            d_psi += delta_sample_width * self.curvature
        
            theta = (d_psi)
            c, s = np.cos(theta), np.sin(theta)
            R = np.array(((c, -s), (s, c)))

            lineVec = np.matmul(R, np.array([1, 0]))
            lineVec = delta_sample_width * lineVec / math.sqrt(lineVec[0] * lineVec[0] + lineVec[1] * lineVec[1])
            if(index > 0):
                x_vec_local.append(x_vec_local[-1] + lineVec[0])
                y_vec_local.append(y_vec_local[-1] + lineVec[1])
            else:
                x_vec_local = [0]
                y_vec_local = [0]   


        theta = (self.hdg)
        c, s = np.cos(theta), np.sin(theta)
        R = np.array(((c, -s), (s, c)))

        self.x_vec = list()
        self.y_vec = list()

        for x_value, y_value in zip(x_vec_local, y_vec_local):
            global_point = np.matmul(R, np.array([x_value, y_value])) + np.array([self.x, self.y])

            self.x_vec.append(global_point[0])
            self.y_vec.append(global_point[1])

    def get_lane_marking_dicts(self):
        """ Returns the lane marking plotting vector for the center line"""
        if(self.s_vec is None):
            raise Exception("Please call sample_me before activating the plotting")

        return [{"x_vec": list(self.x_vec), "y_vec": list(self.y_vec), "type": "centerline", "color": "white", "width": 0.12}]



class xodrGeometryLine(xodrGeometry):
    """ Geometry Class for a XODR Line
    
    Notice: No further variables than xodrGeometry
    """
    def __init__(self, xmlGeometry):
        """ Reads no additional and call the main class"""
        xodrGeometry.__init__(self, xmlGeometry) 

    def __str__(self):
        """ Overwrite str()"""
        return "Line: s: %.2f, x: %.2f, y: %.2f, hgd: %.2f, length %.2f" % (self.s, self.x, self.y, self.hdg, self.length)

    def sample_me(self, sampleWidth):
        """ Samples this geometry object """
        self.s_vec = np.arange(self.s, self.s + self.length, sampleWidth)
        if(self.s_vec[-1] > self.s + self.length):
            raise Exception("The S-Vec is larger than the actual road element")
        elif(self.s_vec[-1] + 0.00001 < self.s + self.length):
            self.s_vec = np.append(self.s_vec, self.s + self.length)


        theta = (self.hdg)
        c, s = np.cos(theta), np.sin(theta)
        R = np.array(((c, -s), (s, c)))

        lineVec = np.matmul(R, np.array([1, 0]))
        lineVec = lineVec / math.sqrt(lineVec[0] * lineVec[0] + lineVec[1] * lineVec[1])

        self.x_vec = list()
        self.y_vec = list()
        for s_sample in self.s_vec:
            scaledLineVec = lineVec * (s_sample - self.s)
            self.x_vec.append(self.x + scaledLineVec[0])
            self.y_vec.append(self.y + scaledLineVec[1])
        self.x_vec = np.asarray(self.x_vec)
        self.y_vec = np.asarray(self.y_vec)

        
    def get_lane_marking_dicts(self):
        """
        This functions returns all lane markings corresponding to this static world object.

        Therefore, a list of line samplings, e.g. for plotting is created.

        The format of the return type is:
        [{x_vec: [...], y_vec: [...], type: "borken", color: "white", width: 0.12}, 
        {x_vec: [...], y_vec: [...], type: "solid",  color: "white", width: 0.12},
        .
        .
        .
        {x_vec: [...], y_vec: [...], type: "solid",  color: "white", width: 0.12},
        ]

        Types:
        
        * solid: Solid lane marking
        * dashed: Dashed lane marking
        * center_line: Center line fo the corresponding road element
            
        """
        if(self.s_vec is None):
            raise Exception("Please call sample_me before activating the plotting")

        return [{"x_vec": list(self.x_vec), "y_vec": list(self.y_vec), "type": "centerline", "color": "white", "width": 0.12}]



class xodrGeometryPoly3(xodrGeometry):
    """Geometry Class for a XODR Poly 3rd Order

    Overwrites the base class ``xodrGeometry``
    """
    def __init__(self, xmlGeometry):
        """ Reads the Curvature relevant parameter and call the main class"""


        xodrGeometry.__init__(self, xmlGeometry) 
        self.aU = float(xmlGeometry[0].attrib['aU'])
        self.bU = float(xmlGeometry[0].attrib['bU'])
        self.cU = float(xmlGeometry[0].attrib['cU'])
        self.dU = float(xmlGeometry[0].attrib['dU'])
        self.aV = float(xmlGeometry[0].attrib['aV'])
        self.bV = float(xmlGeometry[0].attrib['bV'])
        self.cV = float(xmlGeometry[0].attrib['cV'])
        self.dV = float(xmlGeometry[0].attrib['dV'])        



    def __str__(self):
        return "Curvature: a: %.2f,b: %.2f,c: %.2f,d: %.2f, s: %.2f, x: %.2f, y: %.2f, hgd: %.2f, length %.2f" % (self.a, self.b, self.c, self.d, self.s, self.x, self.y, self.hdg, self.length)



    def sample_me(self, sampleWidth):  
        """ Samples this geometry object """
        self.s_vec = np.arange(self.s, self.s + self.length, sampleWidth)
        if(self.s_vec[-1] > self.s + self.length):
            raise Exception("The S-Vec is larger than the actual road element")
        elif(self.s_vec[-1] + 0.00001 < self.s + self.length):
            self.s_vec = np.append(self.s_vec, self.s + self.length)


        x_vec_local = list()
        y_vec_local = list()
        for index, s_sample in enumerate(self.s_vec):
            s_offset_free = s_sample - self.s
            x_local = self.aU + self.bU * s_offset_free + self.cU * s_offset_free**2 + self.dU * s_offset_free**3
            y_local = self.aV + self.bV * s_offset_free + self.cV * s_offset_free**2 + self.dV * s_offset_free**3
            x_vec_local.append(x_local)
            y_vec_local.append(y_local)


        theta = (self.hdg)
        c, s = np.cos(theta), np.sin(theta)
        R = np.array(((c, -s), (s, c)))

        self.x_vec = list()
        self.y_vec = list()

        for x_value, y_value in zip(x_vec_local, y_vec_local):
            global_point = np.matmul(R, np.array([x_value, y_value])) + np.array([self.x, self.y])

            self.x_vec.append(global_point[0])
            self.y_vec.append(global_point[1])

    def get_lane_marking_dicts(self):
        """ Returns the lane marking plotting vector for the center line"""
        if(self.s_vec is None):
            raise Exception("Please call sample_me before activating the plotting")

        return [{"x_vec": list(self.x_vec), "y_vec": list(self.y_vec), "type": "centerline", "color": "white", "width": 0.12}]


