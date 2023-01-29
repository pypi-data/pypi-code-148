
from openautomatumdronedata.dynamicWorld import *
from openautomatumdronedata.staticWorld import *
import os 
import numpy as np


class droneDataset():
    """
        Represents a full automatum data dataset and decodes the information. 

        Information's related to objects and their behavior over time a represented in the dynamic world. 
        Information's realted to lane geometry a represented in the static world.


        :param dataSetFolderPath: Path to a folder containing a valid automatum.data dataset.

        :var dynWorld: Dynamic World of the dataset
        :var statWorld: Static World of the dataset
    """


    def __init__(self, dataSetFolderPath):
        """
        Creating a automatum drone dataset object, to access the utility functions.

        """
        self.dynWorld = dynamicWorld(os.path.join(dataSetFolderPath, "dynamicWorld.json"))
        self.statWorld = xodrStaticWorld((os.path.join(dataSetFolderPath, "staticWorld.xodr")))


    def get_lane_assignment(self, x, y):
        """Returns the lane ID vector of the given point

        :param x: x value of the point
        :param y: y value of the point
        :return: Lane assignment as ID of xodr lane (0 means not in road)
        """
        return self.statWorld.calculate_point_to_lane_assignment(x,y)



    def calculate_on_demand_values_for_all_objects(self):
        """
        Based on the combination of dynamic and static world additional values for dynamic objects could be calculated.
        Since these values are not part of the dataset, they can be determined on demand by calling this function.

        Notice: The calculation is quiet expensive, so that it could take a view seconds.

        Per dynamic object the following values are determined:

        * lane_id: Vector with the xodr lane id of the object at every timestamp 
        * object_relation_dict_list: dict with the UUID of the relevant objects
        """

        for dyn_obj in self.dynWorld.get_list_of_dynamic_objects():
            dyn_obj.lane_id = list()
            for x, y in zip(dyn_obj.x_vec, dyn_obj.y_vec):
                id_lane, id_road = self.get_lane_assignment(x,y)
                dyn_obj.lane_id.append(id_lane)

        time_vec = np.arange(0, self.dynWorld.maxTime, self.dynWorld.delta_t)
        for time in time_vec:
            obj_in_timestamp = self.dynWorld.get_list_of_dynamic_objects_for_specific_time(time)
            for dyn_obj in obj_in_timestamp:
                dyn_obj.calculate_object_relations(obj_in_timestamp, time)

        


