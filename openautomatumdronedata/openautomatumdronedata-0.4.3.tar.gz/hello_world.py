from openautomatumdronedata.dataset import droneDataset
import os
import numpy as np


path_to_dataset_folder = os.path.abspath("datasets/hw-a9-stammhamm-015-39f0066a-28f0-4a68-b4e8-5d5024720c4e")
dataset = droneDataset(path_to_dataset_folder)

dynWorld = dataset.dynWorld

print(dynWorld.UUID)
print(dynWorld.frame_count)
print(dynWorld.fps)
print(dynWorld.delta_t)
print(dynWorld.utm_referene_point)
print(dynWorld.maxTime)
print(dynWorld.DrivenDistanceInMeter)
print(dynWorld.MedianDrivenDistanceInMeter)
#print(dynWorld.dynamicObjects) # Possible but not recommended. Use further discussed functions.

dynObjectList = dynWorld.get_list_of_dynamic_objects_for_specific_time(1.0)
dynObject = dynObjectList[-1]

print(dynObject.x_vec)
print(dynObject.y_vec)
print(dynObject.vx_vec)
print(dynObject.vy_vec)
print(dynObject.psi_vec)
print(dynObject.ax_vec)
print(dynObject.ay_vec)
print(dynObject.length)
print(dynObject.width)
print(dynObject.time)
print(dynObject.UUID)
print(dynObject.delta_t) 

len(dynWorld) # Returns the number of included object
dynObjectList = dynWorld.get_list_of_dynamic_objects_for_specific_time(1.0)

print(dynObject.get_first_time()) # Returns the time the object occurs the first time
print(dynObject.get_last_time()) # Returns the time the object occurs the last time
print(dynObject.is_visible_at(10)) # Checks if the object is visible at the given time
 
time_vec = np.arange(dynObject.get_first_time(),
                      dynObject.get_last_time(),
                      dynObject.delta_t)
# Print positions
x_vec = dynObject.x_vec
y_vec = dynObject.y_vec
for time in time_vec:
    idx = dynObject.next_index_of_specific_time(time)
    print("At time %0.2f the vehicle is at position %0.2f, %0.2f" % (time, x_vec[idx], y_vec[idx]))


print(dynObject.lane_id_vec)  
print(dynObject.road_id_vec) 

object_relation_dict = dynObject.object_relation_dict_list[0] 
print(object_relation_dict["front_ego"])
print(object_relation_dict["behind_ego"])
print(object_relation_dict["front_left"])
print(object_relation_dict["behind_left"])
print(object_relation_dict["front_right"])
print(object_relation_dict["behind_right"])

dynObject2 = dynObjectList[1]

long_distance, lat_distance = dynObject.get_lat_and_long(1.0, dynObject2)
print(long_distance, lat_distance)

statWorld = dataset.statWorld