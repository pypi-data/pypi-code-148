from numpy.typing import ArrayLike
from typing import Optional

import numpy as np
import scipy.interpolate
import trimesh


def generate_bracelet_electrodes(skin_mesh: trimesh.Trimesh,
                                 first_electrode_location: ArrayLike,
                                 bracelet_plane_normal_vector: ArrayLike,
                                 nb_arrays: int,
                                 distance_between_arrays: float,
                                 nb_electrodes_per_array: int,
                                 distance_between_electrodes: Optional[float] = None) -> ArrayLike:
    """Create bracelet electrodes

    Creates electrode locations for a bracelet electrode configuration. Can produce multiple arrays of electrodes
    encircling the skin surface.

    Args:
        skin_mesh: An instance of the trimesh.Trimesh class representing skin surface mesh.
        first_electrode_location: A numpy array containing 3D coordinates of the first electrode of the first array.
            Does not have to be precisely on the skin mesh - the point will be projected onto it.
        bracelet_plane_normal_vector: A numpy array containing the direction of the normal vector defining the bracelet
            section planes. Note, that all the arrays have the same normal vector.
        nb_arrays: The number of electrode arrays in the bracelet. If larger than 1, the initial bracelet_plan is
            shifted in the direction of the normal vector for a distance distance_between_arrays.
        distance_between_arrays: Distance between electrode arrays in the bracelet, in meters. Note, that all the arrays
            are equidistant.
        nb_electrodes_per_array: The number of electrodes in arrays. The electrodes are ordered in a clockwise direction
            with respect to the bracelet_plane_normal_vector. If the distance_between_electrodes parameter is 0, all the
            arrays will have the same number of electrodes uniformly covering the corresponding section circumferences.
            It will likely result in different inter electrode distances for different arrays.
        distance_between_electrodes: The distance between electrodes of an array, in meters. If not 0, will generate
            equidistant in a clockwise direction starting from the first_electrode_location.


    Returns:
        A numpy array of size (nb_arrays, nb_electrodes_per_array, 3) containing the coordinates of all the electrode
        centers.

    """

    plane_normal = bracelet_plane_normal_vector / np.linalg.norm(bracelet_plane_normal_vector)
    array_elec_centers = np.zeros([nb_arrays, nb_electrodes_per_array, 3])
    for i in range(nb_arrays):
        plane_origin = first_electrode_location + i * distance_between_arrays * plane_normal
        section_vertices = _get_section_vertices(skin_mesh, plane_origin, plane_normal,
                                                 plane_origin)
        electrode_centers = _get_electrode_centers(section_vertices, distance_between_electrodes,
                                                   nb_electrodes_per_array)
        array_elec_centers[i] = electrode_centers
    return array_elec_centers


def _get_electrode_centers(section_vertices, elec_dist=None, nb_elec=None):
    vert_dist = np.linalg.norm(np.diff(section_vertices, axis=0), axis=1)
    vert_dist = np.hstack([0, vert_dist])
    cumul_vert_dist = np.cumsum(vert_dist)

    if nb_elec is None:
        nb_elec = int(cumul_vert_dist[-1] / elec_dist)
    if elec_dist is None:
        elec_dist = cumul_vert_dist[-1] / nb_elec
    cumul_elec_dist = np.array([i * elec_dist for i in range(nb_elec)])
    idx = np.searchsorted(cumul_vert_dist, cumul_elec_dist)
    if np.any(idx >= len(section_vertices)):
        raise ValueError(
            'The length of the electrode array is larger then the perimeter of corresponding arm cross section.')
    return section_vertices[idx]


def _get_section_vertices(mesh, plane_origin, plane_normal, first_elec_location, n_vertices_per_section=500):
    # Get intersection path
    section_path = mesh.section(plane_normal, plane_origin)
    section_vertices = section_path.vertices[section_path.entities[0].points]

    # Check direction
    section_path_2d, _ = section_path.to_planar()
    section_vertices_2d = section_path_2d.vertices[section_path_2d.entities[0].points]
    if _test_path_direction(section_vertices_2d) < 0:
        section_vertices = section_vertices[::-1]

    # Resample path to make more dense and uniform
    section_vertices = _resample_path(section_vertices, n_vertices_per_section)
    section_vertices = section_vertices[:-1]  # remove last vertices because the same as the first one

    # Redefine the first vertex
    first_electrode = np.argmin(np.linalg.norm(section_vertices - first_elec_location[None], axis=1))
    section_vertices = np.roll(section_vertices, -first_electrode, axis=0)
    return section_vertices


def _resample_path(path_vertices, n_samples):
    """ Resamples path to a new number of vertices

    Uniformly resamples path to a new number of vertices using a linear interpolation between
    initial vertices.

    Args:
        path_vertices: A 2D numpy array with the shape of (N, 3). N is the number of vertices. The
            order of vertices is important because it defines a path.
        n_samples: The number of vertices after resampling.

    Returns:
        vertices_new: A 2D numpy array with the shape of (n_samples, 3).

    """
    edges = np.diff(path_vertices, axis=0)
    dist = np.hstack([0, np.linalg.norm(edges, axis=1)])
    dist = np.cumsum(dist)
    f_x = scipy.interpolate.interp1d(dist, path_vertices[:, 0], kind='linear')
    f_y = scipy.interpolate.interp1d(dist, path_vertices[:, 1], kind='linear')
    f_z = scipy.interpolate.interp1d(dist, path_vertices[:, 2], kind='linear')

    dist_new = np.linspace(0, dist[-1], n_samples)
    vertices_new = np.zeros([n_samples, 3])
    vertices_new[:, 0] = f_x(dist_new)
    vertices_new[:, 1] = f_y(dist_new)
    vertices_new[:, 2] = f_z(dist_new)
    return vertices_new


def _test_path_direction(path_vertices):
    """ Tests the direction of the 2D path

    Computes the area bounded by the path. If it's sign is positive, the path is oriented
    clockwise, if negative - counterclockwise.

    Args:
        path_vertices: A 2D numpy array with a shape of (N, 2), where N is the number of path
            vertices. The order of vertices is important because it defines a path. Note,
            that for the closed path first and last vertices should be the same.

    Returns:
        area: The area of the region enclosed by the path.

    """

    area = 0
    for i in range(path_vertices.shape[0]-1):
        area += (path_vertices[i+1, 0] - path_vertices[i, 0]) * \
                (path_vertices[i+1, 1] + path_vertices[i, 1])
    return 0.5 * area
