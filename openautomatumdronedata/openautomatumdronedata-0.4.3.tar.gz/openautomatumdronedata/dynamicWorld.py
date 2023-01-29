import os
import json
from sys import exec_prefix
import numpy as np

class dynamicWorld():
    """
        Represents all dynamic objects in a dataset

        :param path2JSON: Path to automatum data json file


        :var UUID:  Unique UUID of the dataset 
        :var frame_count:  Number of images/frames 
        :var fps:  Frame Rate 
        :var delta_t:  Time between two frames (1/fps) \[s\]
        :var utm_referene_point: Reference point in the world coordinate system in UTM-Format. This reference point is the center of the coordinate system for the given position. The points is given as a tuple of (x \[m\], y \[m\], letter, number)-
        :var dynamicObjects: List of dynamic object. Its recommended to use the included functions to access the dynamic objects. 
        :var maxTime:  Maximum time of the dataset \[s\]
        :var DrivenDistanceInMeter: Accumulated driven distance in meter
        :var MedianDrivenDistanceInMeter: Median driven distance 

    """
    def __init__(self, path2JSON):
        """
            Loads the dataset

            :param dataSetFolderPath: Path to a folder containing a valid automatum.data dataset.
        """        
        if(not os.path.isfile(path2JSON)):
            raise FileNotFoundError("The dynamic world json couldn't be found - Path: %s" % path2JSON)

        with open(path2JSON) as f:
            dynamicWorldData = json.load(f) 
        
        if(dynamicWorldData["Release"] < 3.0):
            raise Exception("This version is only compatible with the released datasets of version 3.x. If you still want to use version 1.x go to the compatibility table in the documentation and install the correct version. (https://openautomatumdronedata.readthedocs.io/en/latest/readme_include.html).")

        self.UUID = dynamicWorldData["UUID"]

        self.frame_count = dynamicWorldData["videoInfo"]["frame_count"]
        self.fps = dynamicWorldData["videoInfo"]["fps"]
        self.delta_t = 1 / self.fps
        self.utm_referene_point = dynamicWorldData["UTM-ReferencePoint"]
        self.dynamicObjects = dict()
        self.maxTime = 0


        self.DrivenDistanceInMeter = dynamicWorldData["DrivenDistanceInMeter"]
        self.MedianDrivenDistanceInMeter = dynamicWorldData["MedianDrivenDistanceInMeter"]
       
        for dynObjData in dynamicWorldData["objects"]:

            dynObj = dynamicObject.dynamic_object_factory(dynObjData, self.delta_t)
            self.dynamicObjects[dynObjData["UUID"]] = dynObj
            self.maxTime = max(self.maxTime, dynObj.get_last_time())


    def get_length_of_dataset_in_seconds(self):
        """Returns the complete length of the dataset in seconds. 

        """
        return self.maxTime 

    def __len__(self):
        """
            Overwrite the length operator 
        """
        return len(self.dynamicObjects)

    def __str__(self):
        """
            Overwrite the string Method
        """
        dataSetString = "Dataset %s consits of the %d objects:\n" % (self.UUID, len(self))
        for dynObj in self.dynamicObjects.values():
            dataSetString += "'--> %s [%s] with %d entries from %0.2f s to %0.2f s\n" % (str(type(dynObj)), dynObj.UUID, len(dynObj), dynObj.get_first_time(), dynObj.get_last_time())

        return dataSetString

    def get_dynObj_by_UUID(self, UUID):
        """
            Returns the dynamic object with the given UUID string. 
            If no object is found, None is returned. 
        """
        if(UUID in self.dynamicObjects):
            return self.dynamicObjects[UUID]
        else:
            return None

    def get_list_of_dynamic_objects(self):
        """
            Returns the list of dynamic objects.
        """
        return list(self.dynamicObjects.values())

    def get_list_of_dynamic_objects_for_specific_time(self, time):
        """
            Returns the list of dynamic objects that are visitable at the given time.
        """
        objList = list()
        for obj in self.dynamicObjects.values():
            if(obj.is_visible_at(time)):
                objList.append(obj)
        return objList
               

class dynamicObject():
    """
        Base Class for all dynamic objects


        Per Object the following information are available as scalar:

        :var type: Type of the object as string
        :var length:  Length of the object \[m\]
        :var width:  Width of the object \[m\]
        :var UUID:  Unique UUID of the object 
        :var delta_t:  Time difference between two data points (equal at all objects and with the ```dynamicObject```)

        Per object the following information are available as vector over time: 

        :var x_vec:  X-Position of the assumed center of gravity of the object in the local coordinate system
        :var y_vec:  Y-Position of the assumed center of gravity of the object in the local coordinate system
        :var vx_vec:  Velocity in X-direction of the local coordinate system 
        :var vy_vec:  Velocity in Y-direction of the local coordinate system 
        :var ax_vec:  Acceleration of the object in X-direction **in the vehicle coordinate system**
        :var ay_vec:  Acceleration of the object in Y-direction **in the vehicle coordinate system**
        :var jerk_x_vec:  Jerk of the object in X-direction **in the vehicle coordinate system**. Only if available in your dataset, if not the value is None 
        :var jerk_y_vec:  Jerk of the object in Y-direction **in the vehicle coordinate system**. Only if available in your dataset, if not the value is None
        :var time:  Vector of the timestamp in the dataset recording for the mention values. 
        :var psi_vec:  Vector of orientation of objects. 
        :var curvature_vec:  Driving Curvature of the object. Only if available in your dataset, if not the value is None
        :var lane_id_vec:  Id of the lane of the object in the corresponding xodr 
        :var road_id_vec:  Id of the road of the object in the corresponding xodr 
        :var road_type_list: List of strings that describes the road type at every time step of the object. Only if available in your dataset, if not the value is None
        :var object_relation_dict_list: Gives the UUID of all surrounding objects as a dict in format ```{"front_ego": <uuid>,  "behind_ego": <uuid>,  "front_left": <uuid>,  "behind_left": <uuid>,  "front_right": <uuid>,  "behind_right": <uuid>}``` If an object relation does not exist, e.g. since there is no object, than the value will be ```None``. 
        :var lane_change_flag_vec: Vector of bool values, whereby True means that a lane change occurred. In newer Datasets a vector of Integers. Whereby, -1 means lane change to the left, +1 means lane change to the right and 0 means no lane change. 
        :var distance_left_lane_marking: Vector which gives the distance to the left lane marking
        :var distance_right_lane_marking: Vector which gives the distance to the right lane marking
        :var tth_dict_vec: Gives the Time-To-Collision to all surrounding objects as a dict in format ```{"front_ego": <ttc>,  "behind_ego": <ttc>,  "front_left": <ttc>,  "behind_left": <ttc>,  "front_right": <ttc>,  "behind_right": <ttc>}``` If the value can not be calculated, e.g. the relevant object is to fast, than the value will be set to ```-1```. If no object exists, the value will be set to ```None``` 
        :var ttc_dict_vec: Gives the Time-To-Headway to all surrounding objects as a dict in format ```{"front_ego": <tth>,  "behind_ego": <tth>,  "front_left": <tth>,  "behind_left": <tth>,  "front_right": <tth>,  "behind_right": <tth>}``` If the value can not be calculated, e.g. the relevant object is to fast, than the value will be set to ```-1```. If no object exists, the value will be set to ```None``` 
        :var lat_dist_dict_vec: Gives the lateral distance the surrounding objects as a dict in format ```{"front_ego": <latDist>,  "behind_ego": <latDist>,  "front_left": <latDist>,  "behind_left": <latDist>,  "front_right": <latDist>,  "behind_right": <latDist>}```. If no object exists, the value will be set to ```None```.  Only if available in your dataset, if not the value is None
        :var long_dist_dict_vec: Gives the long distance the surrounding objects as a dict in format ```{"front_ego": <longDist>,  "behind_ego": <longDist>,  "front_left": <longDist>,  "behind_left": <longDist>,  "front_right": <longDist>,  "behind_right": <longDist>}```. If no object exists, the value will be set to ```None```.  Only if available in your dataset, if not the value is None
    """
    def __init__(self, movement_dynamic, delta_t):
        self.x_vec = movement_dynamic["x_vec"]
        self.y_vec = movement_dynamic["y_vec"]
        self.vx_vec = movement_dynamic["vx_vec"]
        self.vy_vec = movement_dynamic["vy_vec"]
        self.psi_vec = movement_dynamic["psi_vec"]
        self.ax_vec = movement_dynamic["ax_vec"]
        self.ay_vec = movement_dynamic["ay_vec"]
        self.length = movement_dynamic["length"]
        self.width = movement_dynamic["width"]
        self.time = movement_dynamic["time"]
        self.UUID = movement_dynamic["UUID"]

        self.delta_t = delta_t



        # Values which are not part of all datasets 
        if("lane_id_vec" in movement_dynamic):
            self.lane_id_vec = movement_dynamic["lane_id_vec"]
        else:
            self.lane_id_vec = None            
        if("road_id_vec" in movement_dynamic):            
            self.road_id_vec = movement_dynamic["road_id_vec"]
        else:
            self.road_id_vec = None
        if("object_relation_dict_list" in movement_dynamic):             
            self.object_relation_dict_list = movement_dynamic["object_relation_dict_list"]
        else:
            self.object_relation_dict_list = None

        if("lane_change_flag_vec" in movement_dynamic):
            self.lane_change_flag_vec = movement_dynamic["lane_change_flag_vec"]
        else:
            self.lane_change_flag_vec = None 
        if("distance_left_lane_marking" in movement_dynamic):
            self.distance_left_lane_marking = movement_dynamic["distance_left_lane_marking"]
        else:
            self.distance_left_lane_marking = None 
        if("distance_right_lane_marking" in movement_dynamic):
            self.distance_right_lane_marking = movement_dynamic["distance_right_lane_marking"]
        else:
            self.distance_right_lane_marking = None 

        if("tth_dict_vec" in movement_dynamic):
            self.tth_dict_vec = movement_dynamic["tth_dict_vec"]
        else:
            self.tth_dict_vec = None 

        if("ttc_dict_vec" in movement_dynamic):
            self.ttc_dict_vec = movement_dynamic["ttc_dict_vec"]
        else:
            self.ttc_dict_vec = None                         
            
        if("lat_dist_dict_vec" in movement_dynamic):
            self.lat_dist_dict_vec = movement_dynamic["lat_dist_dict_vec"]
        else:
            self.lat_dist_dict_vec = None    

        if("long_dist_dict_vec" in movement_dynamic):
            self.long_dist_dict_vec = movement_dynamic["long_dist_dict_vec"]
        else:
            self.long_dist_dict_vec = None     

        if("jerk_x_vec" in movement_dynamic):
            self.jerk_x_vec = movement_dynamic["jerk_x_vec"]
        else:
            self.jerk_x_vec = None    

        if("jerk_y_vec" in movement_dynamic):
            self.jerk_y_vec = movement_dynamic["jerk_y_vec"]
        else:
            self.jerk_y_vec = None 


        if("curvature_vec" in movement_dynamic):
            self.curvature_vec = movement_dynamic["curvature_vec"]
        else:
            self.curvature_vec = None    

        if("road_type_list" in movement_dynamic):
            self.road_type_list = movement_dynamic["road_type_list"]
        else:
            self.road_type_list = None                                                       

    def __eq__(self, other):
        """Overwrite compare operator

        :param other: Other dynamic world object
        """
        self.UUID == other.UUID
        
    def __len__(self):
        """
            Overwrite the length operator 
        """
        return len(self.x_vec)

    def get_first_time(self):
        """
            :return: Returns the time the object occurs the first time
        """
        return self.time[0]

    def get_last_time(self):
        """
            :return: Returns the time the object occurs the last time
        """
        return self.time[-1]

    def is_visible_at(self, time):
        """
            Checks if the object is visible at the given time
            :return: Returns true if the object is visiable.
        """
        return (time > self.get_first_time() - self.delta_t / 2 and time < self.get_last_time() + self.delta_t / 2)

    def next_index_of_specific_time(self, time):
        """
            Returns the index that is next to the given time. 
            If the object is not visible in that time step. 
            The function returns None.

            :return: Next index to a given time. 
        """
        if(not self.is_visible_at(time)):
            return None
        return max(0, min(len(self), round((time - self.get_first_time()) / self.delta_t)))

    def get_object_relation_for_defined_time(self, time):
        """Returns object relation for a given time stamp. 
        Returns None if object relation are not calculated or object not in that time.


        :param time: Evaluted Time
        :return: Dict of objects relations in the format ```{"front_ego": <uuid>,  "behind_ego": <uuid>,  "front_left": <uuid>,  "behind_left": <uuid>,  "front_right": <uuid>,  "behind_right": <uuid>}``` If an object relation does not exist, e.g. since there is no object, than the value will be ```None``. 

        """
        if(self.object_relation_dict_list is not None):
            idx = self.next_index_of_specific_time(time)
            if(idx is not None):
                return self.object_relation_dict_list[idx]
        return None


    def get_object_position_for_defined_time(self, time):
        """Returns object position for a given time stamp. 
        Returns None if object relation are not calculated or object not in that time

        :param time: Evaluted Time
        :return: y position (None if object does not exist on the given time step)
        :return: y position (None if object does not exist on the given time step)
        """
        if(self.object_relation_dict_list is not None):
            idx = self.next_index_of_specific_time(time)
            if(idx is not None):
                return self.x_vec[idx], self.y_vec[idx]
        return None, None

        
    @staticmethod
    def dynamic_object_factory(obj_data_dict, delta_t):
        """
            Object factory to decode the objects that are 
            specified in the json right into the corresponding objects.
        """
        obj_factory_dict = {
            "car": carObject,
            "van": vanObject,
            "truck": truckObject,
            "carWithTrailer": carWithTrailerObject,
            "motorcycle": motorcycleObject
        }
        return obj_factory_dict[obj_data_dict["objType"]](obj_data_dict, delta_t)


    def rotate_and_translate_position(self, dx, dy, dps, time):
        """Returns the position after rotation with dpsi and translation with dx and dy.
        """
        idx = self.next_index_of_specific_time(time)
        c, s = np.cos(dps), np.sin(dps)
        R = np.array(((c, -s), (s, c)))

        pos = np.matmul(R, np.array([self.x_vec[idx] + dx, self.y_vec[idx] + dy]))
        return pos[0], pos[1]


    def get_lat_and_long(self, time, other):
        """Returns the lateral and longitudinal distance from the current object to the given object.

        :param time: Time of evaluation
        :param other: Other dynamic object.

        :return: Longitudinal Distance 
        :return: Lateral Distance 

        """
        if(not self.is_visible_at(time)):
            raise Exception("The object %s is not visible at time %f. Therefore, the lateral and longitudinal distance to %s, can not be calculated." % (self.UUID, time, other.UUID))
        if(not other.is_visible_at(time)):
            raise Exception("The object %s is not visible at time %f. Therefore, the lateral and longitudinal distance to %s, can not be calculated." % (other.UUID, time, self.UUID))
            
        idx = self.next_index_of_specific_time(time)

        return other.rotate_and_translate_position(-self.x_vec[idx], -self.y_vec[idx],
                                                   -self.psi_vec[idx], time)

class carObject(dynamicObject):
    """
        Class for representing a car object. 
        Inheritances from dynamicObject which currently provides the main functionality. 
    """
    
    def __init__(self, movement_dynamic, delta_t):
        dynamicObject.__init__(self, movement_dynamic, delta_t)
        self.type = "car"
        

class truckObject(dynamicObject):
    """
        Class for representing a track object. 
        Inheritances from dynamicObject which currently provides the main functionality. 
    """
    def __init__(self, movement_dynamic, delta_t):
        dynamicObject.__init__(self, movement_dynamic, delta_t)
        self.type = "truck"
        

class carWithTrailerObject(dynamicObject):
    """
        Class for representing a trailer object. 
        Inheritances from dynamicObject which currently provides the main functionality. 
    """
    def __init__(self, movement_dynamic, delta_t):
        dynamicObject.__init__(self, movement_dynamic, delta_t)
        self.type = "carWithTrailer"

class vanObject(dynamicObject):
    """
        Class for representing a van object. 
        Inheritances from dynamicObject which currently provides the main functionality. 
    """
    def __init__(self, movement_dynamic, delta_t):
        dynamicObject.__init__(self, movement_dynamic, delta_t)
        self.type = "van"
        

class motorcycleObject(dynamicObject):
    """
        Class for representing a trailer object. 
        Inheritances from dynamicObject which currently provides the main functionality. 
    """
    def __init__(self, movement_dynamic, delta_t):
        dynamicObject.__init__(self, movement_dynamic, delta_t)
        self.type = "motorcycle"



            