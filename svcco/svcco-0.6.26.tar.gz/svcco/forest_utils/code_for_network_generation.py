import svcco
import pyvista as pv
import numpy as np

# Basic Parameters for Vascular Networks
# All units below are expressed in centimeters-grame-second units

flow_rate = (10/60)                 # mL/sec
pressure_drop = 0.5*1333            # Pa
min_distance_from_boundary = 2/10   # cm
min_distance_from_vessel   = 1.5/10 # cm

# Constructing vascular network for first cube (4x4 cm)

cube_side_size = 4 # cm
adjusted_cube_side_size = cube_side_size - 2*min_distance_from_boundary

cube = pv.Cube(x_length=adjusted_cube_side_size,
               y_length=adjusted_cube_side_size,
               z_length=adjusted_cube_side_size).triangulate().subdivide(4)

boundary = svcco.surface()
boundary.set_data(cube.points,cube.point_normals)
boundary.solve()
boundary.build(q=4)

start_points = [[np.array([-cube_side_size/2,-1,1]),
                 np.array([-cube_side_size/2,1,-1])]]

network = svcco.forest(boundary,number_of_networks=1,trees_per_network=[2],
                       start_points=start_points,convex=True)
network.networks[0][0].set_parameters(Pperm=0.5,Pterm=0,Qterm=0.1)
network.networks[0][1].set_parameters(Pperm=0.5,Pterm=0,Qterm=0.1)
network.set_roots()
network.add(2,radius_buffer=2*min_distance_from_vessel)
