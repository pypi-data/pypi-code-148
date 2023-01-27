import numpy as np
import matplotlib.pyplot as plt
from drama.performance.sar import SARModeFromCfg
from drama.io import cfg
from drama.mission.timeline import LatLonTimeline



def viewing_geometry (par_file, mode, orbit_resolution, latitudes, longitudes):
    """
    A function that uses the LatLonTimeline function from drama to estimte the viewing geometry of sentinel-1 for a list or grid of coordinates. 
    
    Input:
        - par_file: parameter file with specified orbit values for S1
        - mode: mode of S1: IWS, EM, StripMap
        - orbit_resolution: the desired orbit resolution
        - latitudes: list or grid values with the latitudes of the points
        - longitudes: list or grid values with the longitudes of the points
        
    output
        - nr_asc_obs: list of the number of available ascending observations for particular location
        - nr_desc_obs: list of the number of available descending observations for particular location
        - asc_inc: list of the incidence angles of the ascending acquisitions per location 
        - desc_inc: list of the incidence angles of the descending acquisitions per location  
        - asc_alpha: list of the azimuth of the ZDP of the ascending acquisitions per location  
        - desc_alpha: list of the azimuth of the ZDP of the descending acquisitions per location 
    
    """
    # function to define the viewing geomtry for a list of points

    # The number of orbits per cycle and the repeat cyle are some hard coded values but can be changed here
    n_orbits_cycle = 175
    lon_repeat_cycle = 360 / n_orbits_cycle

    # the timeline function is a function that estimates among others the viewing geometry per location on Earth
    # Ask drama to compute the acquisition geometry for our range of lat and lon.
    timeline = LatLonTimeline(
        par_file, np.ravel(latitudes), np.ravel(longitudes), inc_angle_range=(mode.incs[0, 0], mode.incs[-1, 1]), dlat=orbit_resolution, dlon=orbit_resolution
    )
    
	

    # Define number of ascending and descending observations per point

    asc_acqs, desc_acqs = timeline.compute_timeline()

    nr_asc_obs = np.array([len(acq.theta_i) for acq in asc_acqs]).reshape(longitudes.shape)
    nr_desc_obs = np.array([len(acq.theta_i) for acq in desc_acqs]).reshape(longitudes.shape)


    # Define zero arrays to fill with incidence angles and azimuths of the ZDP later on
    desc_inc = np.empty((len(np.ravel(latitudes)),np.max(nr_desc_obs)))
    desc_inc[:] = np.nan
    desc_alpha = np.empty((len(np.ravel(latitudes)),np.max(nr_desc_obs)))
    desc_alpha[:] = np.nan

    asc_inc = np.empty((len(np.ravel(latitudes)),np.max(nr_asc_obs)))
    asc_inc[:] = np.nan
    asc_alpha = np.empty((len(np.ravel(latitudes)),np.max(nr_asc_obs)))
    asc_alpha[:] = np.nan

    # Loop trough all points and safe the incidence angle and azimuth angles of the ZDP
    for i in range(len(np.ravel(latitudes))):
        x_a = len(asc_acqs[i].theta_i)
        x_d = len(desc_acqs[i].theta_i)
        
        asc_inc[i,0:x_a] = asc_acqs[i].theta_i
        asc_alpha[i,0:x_a] = asc_acqs[i].northing + 2*np.pi

        desc_inc[i,0:x_d] = desc_acqs[i].theta_i
        desc_alpha[i,0:x_d] = desc_acqs[i].northing
        
    return nr_asc_obs, nr_desc_obs, asc_inc, desc_inc, asc_alpha, desc_alpha


def inc_azimuth_max(latitudes, longitudes, inc, alpha):
    """
    A function to estimate the minimum and maximum incidence and heading angle per location
    
    Input:
        Latitudes: a list or grid with latitudes of the locations
        Longitudes: a list or grid with longitudes of the locations
        Inc: a 2D array with incidence angles available per location [radians]
        alpha: a 2D array with azimuth angles of the ZDP per location [radians]
        
    Output:
        inc_max = The maximum incidence angle per location
        inc_min = The minimum incidence angle per location
        inc_alpha_max = The azimuth of the ZDP corresponsing to the maximum incidence angle per location
        inc_alpha_min = The azimuth of the ZDP corresponsing to the minimum incidence angle per location
        
        alpha_inc_max = The maximum azimuth of the ZDP per location
        alpha_inc_min = The maximum azimuth of the ZDP per location
        alpha_max = The incidence angle correspoding by the maximum azimuth of the ZDP per location
        alpha_min = The incidence angle correspoding by the minimum azimuth of the ZDP per location
    
    """
    
    # Loop trough all points (in the grid)
    inc_max = np.zeros(len(np.ravel(latitudes)))
    inc_min = np.zeros(len(np.ravel(latitudes)))
    inc_alpha_max = np.zeros(len(np.ravel(latitudes)))
    inc_alpha_min = np.zeros(len(np.ravel(latitudes)))

    alpha_inc_max = np.zeros(len(np.ravel(latitudes)))
    alpha_inc_min = np.zeros(len(np.ravel(latitudes)))
    alpha_max = np.zeros(len(np.ravel(latitudes)))
    alpha_min = np.zeros(len(np.ravel(latitudes)))


    for i in range(len(np.ravel(latitudes))):

        #Create arrays with the incidence and azimuth angles per point
        inc_arr = inc[i,:]
        alpha_arr = alpha[i,:]
                
        no_nan_inc = inc_arr.size - sum(~np.isnan(inc_arr))
        no_nan_alpha = alpha_arr.size - sum(~np.isnan(alpha_arr))

                
        if no_nan_inc == inc_arr.size or no_nan_alpha == alpha_arr.size: #Do not estimate min and max for locations without a viewing geometry
            inc_max[i] = np.nan
            inc_min[i] = np.nan
            alpha_inc_max[i] = np.nan
            alpha_inc_min[i] = np.nan
            
            alpha_max[i] = np.nan
            alpha_min[i] = np.nan
            inc_alpha_max[i] = np.nan
            inc_alpha_min[i] = np.nan
            
        else: 
            # Find the maximum and minimum incidence angles and index
            inc_max[i] = np.nanmax(inc_arr)
            inc_min[i] = np.nanmin(inc_arr)
            i_inc_max = np.where(inc_arr == np.nanmax(inc_arr))
            i_inc_min = np.where(inc_arr == np.nanmin(inc_arr))

            # Find corresponding heading angles
            alpha_inc_max[i] = alpha_arr[i_inc_max[0][0]]
            alpha_inc_min[i] = alpha_arr[i_inc_min[0][0]]


            # Find the maximum and minimum heading angles of the ZDP and index
            alpha_max[i] = np.nanmax(alpha_arr)
            alpha_min[i] = np.nanmin(alpha_arr)
            i_alpha_max = np.where(alpha_arr == np.nanmax(alpha_arr))
            i_alpha_min = np.where(alpha_arr == np.nanmin(alpha_arr))

            # Find corresponding heading angles
            inc_alpha_max[i] = inc_arr[i_alpha_max[0][0]]
            inc_alpha_min[i] = inc_arr[i_alpha_min[0][0]]

    #Convert the arrays to grid (if needed)
    inc_max = inc_max.reshape(latitudes.shape)
    inc_min = inc_min.reshape(latitudes.shape)
    inc_alpha_max = inc_alpha_max.reshape(latitudes.shape)
    inc_alpha_min = inc_alpha_min.reshape(latitudes.shape)

    alpha_inc_max = alpha_inc_max.reshape(latitudes.shape)
    alpha_inc_min = alpha_inc_min.reshape(latitudes.shape)
    alpha_max = alpha_max.reshape(latitudes.shape)
    alpha_min = alpha_min.reshape(latitudes.shape)
    
    return inc_max, inc_min, inc_alpha_max, inc_alpha_min, alpha_max, alpha_min, alpha_inc_max, alpha_inc_min






def vector2plane(normal_vec, point, x, y):
    """
    A function that provides the values to parameterize the plane orthogonal to the Line-of-Sight ('normal_vec') vector:
    a*x+b*y+c*z+d=0 
    
    Where [a,b,c] is a point at the plane (the end point of the LoS unit vector, or the 'normal_vec').
 
    When x and y are the limits for the planes this functions also computes the values for z
    
    
    Input:
        normal_vec: the vector that is normal to the plane (the LoS vector)
        point: a point that lies in the plane [a,b,c]
        x: array with x values for the plane equation
        y: array with y values for the plane equation
        
    Output:
        d value for the plane equation
        z values for the coefficients describing the plane
        xx and yy are meshgrids for the planes
    """
    
    # d can be computed with the dot product of the point at the plane and the normal vector
    d = -point.dot(normal_vec)
    
    # Create the meshgrid for x and y
    xx, yy = np.meshgrid(x,y)
    
    # Calculate corresponding z
    z = (-normal_vec[0] * xx - normal_vec[1] * yy - d) * 1. /normal_vec[2]
    
    return d, z, xx, yy
    
    
def plane_intersect(a, b):
    """
    The function plane_intersect compute two points that are located on the intersection line of two planes a and b. 
    
    The planes a and b are described by four parameters:
    
    a, b   4-tuples/lists
           Ax + By +Cz + D = 0
           A,B,C,D in order  

    output: 2 points on line of intersection, np.arrays, shape (3,)
    """
    a_vec, b_vec = np.array(a[:3]), np.array(b[:3])

    aXb_vec = np.cross(a_vec, b_vec)

    A = np.array([a_vec, b_vec, aXb_vec])
    d = np.array([-a[3], -b[3], 0.]).reshape(3,1)

    p_inter = np.linalg.solve(A, d).T

    return p_inter[0], (p_inter + aXb_vec)[0]


def phi_zeta(inc, alpha_d):
    """
    Compute the orientaion, given by phi and zeta, of the null line based on the viewing geometry two satellites. 
    The orientation of the null line is estimated from the cross product between the two LoS vectors. 
    
    Input:
        inc = the incidence angles of the two viewing geometries in randians. An example: inc = np.array([inc_a,inc_d])
        alpha_d = the azimuth of the  angles of the two viewing geometries in randians. An example: alpha_d = np.array([inc_a,inc_d])
    
    Output:
        phi = azimuth angle of the null line [degrees]
        zeta = elevation angle of the null line [degrees]
    
    """
    
    if len(inc)!=2 or len(alpha_d) !=2:
        print ('The orientation of the null line can only estimated when there are two incidence angles and azimuths of the zero-doppler plane')
        
      
    # The cross product between the two LoS vectors
    dir_null_space_e = np.sin(inc[0])*np.cos(alpha_d[0])*np.cos(inc[1]) - np.cos(inc[0])*np.sin(inc[1])*np.cos(alpha_d[1])
    dir_null_space_n = -np.sin(inc[0])*np.sin(alpha_d[0])*np.cos(inc[1]) + np.cos(inc[0])*np.sin(inc[1])*np.sin(alpha_d[1])
    dir_null_space_u = np.sin(inc[0])*np.sin(alpha_d[0])*np.sin(inc[1])*np.cos(alpha_d[1]) -np.sin(inc[0])*np.cos(alpha_d[0])*np.sin(inc[1])*np.sin(alpha_d[1])

    # Compute ground projection of the line
    ground_proj = np.sqrt(dir_null_space_e**2 + dir_null_space_n**2)

    # Compute phi (azimuth angle of the null line)
    phi = np.rad2deg(np.arctan(dir_null_space_e / dir_null_space_n))

    # Compute zeta (elevation angle of the null line)
    zeta = np.rad2deg(np.arctan(dir_null_space_u / ground_proj))

    return phi, zeta

def phi_zeta_grid(inc_grid_asc, inc_grid_dsc, azimuth_grid_asc, azimuth_grid_dsc):
    """
    Compute the orientaion, given by phi and zeta, of the null line based on the viewing geometry two satellites. 
    The orientation of the null line is estimated from the cross product between the two LoS vectors. 
    
    This script should be used when the values of the viewing geometry are available over a grid
    
    Input:
        inc = the incidence angles of the two viewing geometries in randians. An example: inc = np.array([inc_a,inc_d])
        alpha_d = the azimuth of the  angles of the two viewing geometries in randians. An example: alpha_d = np.array([inc_a,inc_d])
    
    Output:
        phi = azimuth angle of the null line [degrees]
        zeta = elevation angle of the null line [degrees]
    
    """
    
    inc_a = np.ravel(inc_grid_asc)
    inc_d = np.ravel(inc_grid_dsc)
    alpha_d_a = np.ravel(azimuth_grid_asc)
    alpha_d_d = np.ravel(azimuth_grid_dsc)
    
    phi = np.zeros(len(inc_a))
    zeta = np.zeros(len(inc_a))
    
    for i in range(len(inc_a)):
    #for i in range(10):
        
        inc = (np.array([inc_a[i], inc_d[i]]))
        alpha_d = (np.array([alpha_d_a[i], alpha_d_d[i]]))
        
               
        phi[i], zeta[i] = phi_zeta(inc, alpha_d) 
        
    phi = phi.reshape(inc_grid_asc.shape)
    zeta = zeta.reshape(inc_grid_asc.shape)
    
    return phi, zeta
    
    
    
def null_space_2sat(inc, alpha_d, plot, title_los1, title_los2):
    """
    A function that estimates the orientation of the null based on two viewing geometries. 
    It can also plot the orientation of the two LoS vectors and the corresponsing null spaces
    It also plots the null line. 
    
    Input:
        inc = the incidence angles of the two viewing geometries in randians. An example: inc = np.array([inc_a,inc_d])
        alpha_d = the azimuth of the  angles of the two viewing geometries in randians. An example: alpha_d = np.array([inc_a,inc_d])
        plot: specfy whether the null line and the null spaces need to be plotted (1 is plot, 0 means no plot)
        title_los1, title_los2 are the corresponsing labels of the LoS unit vectors
        
    Output:
        unit_los_enu: Matrix with the unit vector describing the LoS vectors
        zeta: elevation angle of the null line [degrees]
        phi: azimuth angle of the null line [degrees]
        x: elevation angle of the projection of the null line onto the EU plane [degrees]
        
    """
    
    
    if len(inc) !=2 or len(alpha_d) !=2:
        print (inc, alpha_d)
        print ('The orientation of the null line can only estimated when there are two incidence angles and azimuths of the zero-doppler plane')
        
    
    ############## Compute unit LoS vectors ##############
    r = 1
    east_los = r*np.sin(inc)*np.sin(alpha_d)
    north_los = r*np.sin(inc)*np.cos(alpha_d)
    up_los = r*np.cos(inc)

    # Compute the unit LoS vectors
    unit_los_enu = np.zeros((3,1))

    for i in range(len(inc)):
        unit_los_enu = np.hstack((unit_los_enu, np.matrix([[east_los[i]], [north_los[i]], [up_los[i]]])))

    unit_los_enu = np.delete(unit_los_enu, 0, 1)
    
    ############## Compute null spaces for both the satellites ##############
    # Compute the surfaces perpendicular to the unit LoS vectors
    # When we have a vector [a,b,c] then we have the plane equation: a*x+b*y+c*z+d=0
    # We need to compute d --> when we know a point on the plane we can compute d. 
    # The point at the plane is given by the end point of the unit LoS vector [a,b,c]

    x, y = np.linspace(-1,1,100), np.linspace(-1,1,100)

    # define normal vector and point for the plane corresponding to the asc obs.
    point_asc  = np.array([unit_los_enu[0,0], unit_los_enu[1,0], unit_los_enu[2,0]])
    normal_asc = np.array([unit_los_enu[0,0], unit_los_enu[1,0], unit_los_enu[2,0]])

    # define normal vector and point for the plane corresponding to the desc obs.
    point_dsc  = np.array([unit_los_enu[0,1], unit_los_enu[1,1], unit_los_enu[2,1]])
    normal_dsc = np.array([unit_los_enu[0,1], unit_los_enu[1,1], unit_los_enu[2,1]])

    # Compute the z coordinates for the two planes and the d values that are needed to describe the parameters of the plane equation
    d_asc, zz_asc, xx_asc, yy_asc = vector2plane(normal_asc, point_asc, x, y)
    d_dsc, zz_dsc, xx_dsc, yy_dsc = vector2plane(normal_dsc, point_dsc, x, y)


    ############## Compute equation for the intersection line of the two planes #############
    # Compute the equation for the intersection line of the two planes
    # Based on the functions of the two planes we can compute the intersection line. 

    # Define coefficients of the two null spaces (for asc en dsc)
    coef_asc = (normal_asc[0], normal_asc[1], normal_asc[2], d_asc)
    coef_dsc= (normal_dsc[0], normal_dsc[1], normal_dsc[2], d_dsc)

    # Compute the coordinates for two points at the intersection line
    pnt_one, pnt_two = plane_intersect(coef_asc, coef_dsc)

    # Try the vector equation for the two points (such that the line becomes longer)
    t = np.linspace(-2,2,200)
    dir_vec = pnt_two-pnt_one

    x_line = np.zeros(200)
    y_line = np.zeros(200)
    z_line = np.zeros(200)
    z_ground = np.zeros(200)
    EU_proj = np.ones(200)*-1
    NU_proj = np.ones(200)

    for i in range(len(t)):
        line_coor = pnt_one + t[i]*dir_vec
        x_line[i] = line_coor[0]
        y_line[i] = line_coor[1]
        z_line[i] = line_coor[2]


    ############# Estimate the angles describing the null line ##################

    # Compute differences between the two points
    e_diff = -1*(pnt_one[0] - pnt_two[0])
    n_diff = -1*(pnt_one[1] - pnt_two[1])
    u_diff = -1*(pnt_one[2] - pnt_two[2])

    # Compute ground projection of the line
    ground_proj = np.sqrt(e_diff**2 + n_diff**2)

    # Compute phi (azimuth angle of the null line)
    phi = np.rad2deg(np.arctan(e_diff / n_diff))

    # Compute zeta (elevation angle of the null line)
    zeta = np.rad2deg(np.arctan(u_diff / ground_proj))

    
    # Compute xi (elevation angle of the projection of the null line onto the EU plane)
    xi = np.rad2deg(np.arctan(u_diff / e_diff))
       
    #For plotting we only want the values within the 'box'
    zz_asc[zz_asc>2]=['nan']
    xx_asc[zz_asc>2]=['nan']
    yy_asc[zz_asc>2]=['nan']
    zz_dsc[zz_dsc>2]=['nan']
    xx_dsc[zz_dsc>2]=['nan']
    yy_dsc[zz_dsc>2]=['nan']
    
    mask = (x_line<1)&(x_line>-1) & (y_line<1) & (y_line>-1)& (z_line<2) & (z_line>0)


    if plot == 1:
        plt3d = plt.figure(figsize=(8,8)).gca(projection='3d')
        
        # plot the two surfaces
        plt3d.plot_surface(xx_asc, yy_asc, zz_asc, alpha=0.5, rstride=100, cstride=100, color = 'b')
        plt3d.plot_surface(xx_dsc, yy_dsc, zz_dsc, alpha=0.5, rstride=100, cstride=100, color = 'green')

        # Plot the unit LoS vectors
        plt3d.plot([0,unit_los_enu[0,0]],[0,unit_los_enu[1,0]], [0,unit_los_enu[2,0]], label=title_los1, linewidth=2, color = 'b')
        plt3d.plot([0,unit_los_enu[0,1]],[0,unit_los_enu[1,1]], [0,unit_los_enu[2,1]], label=title_los2, linewidth=2, color = 'g')

        # Plot the 'projections' of the LoS vectors
        plt3d.plot([unit_los_enu[0,0],unit_los_enu[0,0]],[unit_los_enu[1,0],unit_los_enu[1,0]], [0,unit_los_enu[2,0]], 
                   linewidth=1, color = 'b', ls = '--', alpha = 0.6)
        plt3d.plot([0,unit_los_enu[0,0]],[0,unit_los_enu[1,0]], [0,0], linewidth=1, color = 'b',
                  ls = '--', alpha = 0.6)

        plt3d.plot([unit_los_enu[0,1],unit_los_enu[0,1]],[unit_los_enu[1,1],unit_los_enu[1,1]], [0,unit_los_enu[2,1]], 
                   linewidth=1, color = 'g', ls = '--', alpha = 0.6)
        plt3d.plot([0,unit_los_enu[0,1]],[0,unit_los_enu[1,1]], [0,0], linewidth=1, color = 'g',
                  ls = '--', alpha = 0.6)



        # Plot the null line
        plt3d.plot(x_line[mask], y_line[mask], z_line[mask], lw=2, c='r', label = 'Null line')
        plt3d.plot(x_line[mask], y_line[mask], z_ground[mask], lw=1, c='r', ls = '--', alpha = 0.7)
        plt3d.plot(x_line[mask], NU_proj[mask], z_line[mask], lw=1, c='r', ls = '--', alpha = 0.7)
        plt3d.plot(EU_proj[mask], y_line[mask], z_line[mask], lw=1, c='r', ls = '--', alpha = 0.7)
    
        
        # Set axis etc
        plt3d.set_xlim([-1,1])
        plt3d.set_ylim([-1,1])
        plt3d.set_zlim([0,2])
        plt3d.set_box_aspect([1,1,1]) 
        plt3d.set_zlabel('Up', fontsize = 12)
        plt3d.set_ylabel('North', fontsize = 12)
        plt3d.set_xlabel('East', fontsize = 12)
        plt.title(r'$\phi$ = '+ str(np.around(phi, 2)) + ', $\zeta$ = ' + str(np.around(zeta, 2))
                  #+ ', $\alpha$ = ' + str(np.around(xi, 2))
                  , fontsize = 20)
        
        plt.legend()
        plt.show()


    return unit_los_enu, zeta, phi, xi
            
