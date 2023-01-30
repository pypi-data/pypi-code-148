"""
Polygon module
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""

from __future__ import annotations
import math
import sys
from typing import List
import numpy as np
from trimesh import Trimesh
import trimesh.intersections

from hub.city_model_structure.attributes.plane import Plane
from hub.city_model_structure.attributes.point import Point
import hub.helpers.constants as cte


class Polygon:
  """
  Polygon class
  """

  def __init__(self, coordinates):
    self._area = None
    self._points = None
    self._points_list = None
    self._normal = None
    self._inverse = None
    self._edges = None
    self._coordinates = coordinates
    self._triangles = None
    self._vertices = None
    self._faces = None
    self._plane = None

  @property
  def points(self) -> List[Point]:
    """
    Get the points belonging to the polygon [[x, y, z],...]
    :return: [Point]
    """
    if self._points is None:
      self._points = []
      for coordinate in self.coordinates:
        self._points.append(Point(coordinate))
    return self._points

  @property
  def plane(self) -> Plane:
    """
    Get the polygon plane
    :return: Plane
    """
    if self._plane is None:
      self._plane = Plane(normal=self.normal, origin=self.points[0])
    return self._plane

  @property
  def coordinates(self) -> List[np.ndarray]:
    """
    Get the points in the shape of its coordinates belonging to the polygon [[x, y, z],...]
    :return: [np.ndarray]
    """
    return self._coordinates

  @staticmethod
  def _module(vector):
    x2 = vector[0] ** 2
    y2 = vector[1] ** 2
    z2 = vector[2] ** 2
    return math.sqrt(x2+y2+z2)

  @staticmethod
  def _scalar_product(vector_0, vector_1):
    x = vector_0[0] * vector_1[0]
    y = vector_0[1] * vector_1[1]
    z = vector_0[2] * vector_1[2]
    return x+y+z

  def contains_point(self, point):
    """
    Determines if the given point is contained by the current polygon
    :return: boolean
    """
    # fixme: This method doesn't seems to work.
    n = len(self.vertices)
    angle_sum = 0
    for i in range(0, n):
      vector_0 = self.vertices[i]
      vector_1 = self.vertices[(i+1) % n]
      # set to origin
      vector_0[0] = vector_0[0] - point.coordinates[0]
      vector_0[1] = vector_0[1] - point.coordinates[1]
      vector_0[2] = vector_0[2] - point.coordinates[2]
      vector_1[0] = vector_1[0] - point.coordinates[0]
      vector_1[1] = vector_1[1] - point.coordinates[1]
      vector_1[2] = vector_1[2] - point.coordinates[2]
      module = Polygon._module(vector_0) * Polygon._module(vector_1)

      scalar_product = Polygon._scalar_product(vector_0, vector_1)
      angle = np.pi/2
      if module != 0:
        angle = abs(np.arcsin(scalar_product / module))
      angle_sum += angle
    return abs(angle_sum - math.pi*2) < cte.EPSILON

  def contains_polygon(self, polygon):
    """
    Determines if the given polygon is contained by the current polygon
    :return: boolean
    """

    for point in polygon.points:
      if not self.contains_point(point):
        return False
    return True

  @property
  def points_list(self) -> np.ndarray:
    """
    Get the solid surface point coordinates list [x, y, z, x, y, z,...]
    :return: np.ndarray
    """
    if self._points_list is None:
      s = self.coordinates
      self._points_list = np.reshape(s, len(s) * 3)
    return self._points_list

  @property
  def edges(self) -> List[List[Point]]:
    """
    Get polygon edges list
    :return: [[Point]]
    """
    if self._edges is None:
      self._edges = []
      for i in range(0, len(self.points) - 1):
        point_1 = self.points[i]
        point_2 = self.points[i + 1]
        self._edges.append([point_1, point_2])
      self._edges.append([self.points[len(self.points) - 1], self.points[0]])
    return self._edges

  @property
  def area(self):
    """
    Get surface area in square meters
    :return: float
    """
    # New method to calculate area
    if self._area is None:
      if len(self.points) < 3:
        sys.stderr.write('Warning: the area of a line or point cannot be calculated 1. Area = 0\n')
        return 0
      alpha = 0
      vec_1 = self.points[1].coordinates - self.points[0].coordinates
      for i in range(2, len(self.points)):
        vec_2 = self.points[i].coordinates - self.points[0].coordinates
        alpha += self._angle_between_vectors(vec_1, vec_2)
      if alpha == 0:
        sys.stderr.write('Warning: the area of a line or point cannot be calculated 2. Area = 0\n')
        return 0
      horizontal_points = self._points_rotated_to_horizontal
      area = 0
      for i in range(0, len(horizontal_points) - 1):
        point = horizontal_points[i]
        next_point = horizontal_points[i + 1]
        area += (next_point[1] + point[1]) / 2 * (next_point[0] - point[0])
      next_point = horizontal_points[0]
      point = horizontal_points[len(horizontal_points) - 1]
      area += (next_point[1] + point[1]) / 2 * (next_point[0] - point[0])
      self._area = abs(area)
    return self._area

  @property
  def _points_rotated_to_horizontal(self):
    """
    polygon points rotated to horizontal
    :return: [float]
    """
    z_vector = [0, 0, 1]
    normal_vector = self.normal
    horizontal_points = []
    x = normal_vector[0]
    y = normal_vector[1]

    if x == 0 and y == 0:
      # Already horizontal
      for point in self.points:
        horizontal_points.append([point.coordinates[0], point.coordinates[1], 0])
    else:
      alpha = self._angle_between_vectors(normal_vector, z_vector)
      rotation_line = np.cross(normal_vector, z_vector)
      third_axis = np.cross(normal_vector, rotation_line)
      w_1 = rotation_line / np.linalg.norm(rotation_line)
      w_2 = normal_vector
      w_3 = third_axis / np.linalg.norm(third_axis)
      rotation_matrix = np.array([[1, 0, 0],
                                  [0, np.cos(alpha), -np.sin(alpha)],
                                  [0, np.sin(alpha), np.cos(alpha)]])
      base_matrix = np.array([w_1, w_2, w_3])
      rotation_base_matrix = np.matmul(base_matrix.transpose(), rotation_matrix.transpose())
      rotation_base_matrix = np.matmul(rotation_base_matrix, base_matrix)

      if rotation_base_matrix is None:
        sys.stderr.write('Warning: rotation base matrix returned None\n')
      else:
        for point in self.points:
          new_point = np.matmul(rotation_base_matrix, point.coordinates)
          horizontal_points.append(new_point)
    return horizontal_points

  @property
  def normal(self) -> np.ndarray:
    """
    Get surface normal vector
    :return: np.ndarray
    """
    if self._normal is None:
      points = self.coordinates
      # todo: IF THE FIRST ONE IS 0, START WITH THE NEXT
      point_origin = points[len(points) - 2]
      vector_1 = points[len(points) - 1] - point_origin
      vector_2 = points[0] - point_origin
      vector_3 = points[1] - point_origin
      cross_product = np.cross(vector_1, vector_2)
      if np.linalg.norm(cross_product) != 0:
        cross_product = cross_product / np.linalg.norm(cross_product)
        alpha = self._angle_between_vectors(vector_1, vector_2)
      else:
        cross_product = [0, 0, 0]
        alpha = 0
      if len(points) == 3:
        return cross_product
      if np.linalg.norm(cross_product) == 0:
        return cross_product
      alpha += self._angle(vector_2, vector_3, cross_product)
      for i in range(0, len(points) - 4):
        vector_1 = points[i + 1] - point_origin
        vector_2 = points[i + 2] - point_origin
        alpha += self._angle(vector_1, vector_2, cross_product)
      vector_1 = points[len(points) - 1] - point_origin
      vector_2 = points[0] - point_origin
      if alpha < 0:
        cross_product = np.cross(vector_2, vector_1)
      else:
        cross_product = np.cross(vector_1, vector_2)
      self._normal = cross_product / np.linalg.norm(cross_product)
    return self._normal

  @staticmethod
  def _angle(vector_1, vector_2, cross_product):
    """
    alpha angle in radians
    :param vector_1: [float]
    :param vector_2: [float]
    :param cross_product: [float]
    :return: float
    """
    accepted_normal_difference = 0.01
    cross_product_next = np.cross(vector_1, vector_2)
    if np.linalg.norm(cross_product_next) != 0:
      cross_product_next = cross_product_next / np.linalg.norm(cross_product_next)
      alpha = Polygon._angle_between_vectors(vector_1, vector_2)
    else:
      cross_product_next = [0, 0, 0]
      alpha = 0
    delta_normals = 0
    for j in range(0, 3):
      delta_normals += cross_product[j] - cross_product_next[j]
    if np.abs(delta_normals) < accepted_normal_difference:
      return alpha
    return -alpha

  def triangulate(self) -> List[Polygon]:
    """
    Triangulates a polygon following the ear clipping methodology
    :return: list[triangles]
    """
    # todo: review triangulate_polygon in
    #  https://github.com/mikedh/trimesh/blob/dad11126742e140ef46ba12f8cb8643c83356467/trimesh/creation.py#L415,
    #  it had a problem with a class called 'triangle', but, if solved,
    #  it could be a very good substitute of this method
    #  this method is very dirty and has an infinite loop solved with a counter!!
    if self._triangles is None:
      points_list = self.points_list
      normal = self.normal
      if np.linalg.norm(normal) == 0:
        sys.stderr.write('Not able to triangulate polygon\n')
        return [self]
      # are points concave or convex?
      total_points_list, concave_points, convex_points = self._starting_lists(points_list, normal)

      # list of ears
      ears = []
      j = 0
      while (len(concave_points) > 3 or len(convex_points) != 0) and j < 100:
        j += 1
        for i in range(0, len(concave_points)):
          ear = self._triangle(points_list, total_points_list, concave_points[i])
          rest_points = []
          for points in total_points_list:
            rest_points.append(list(self.coordinates[points]))
          if self._is_ear(ear, rest_points):
            ears.append(ear)
            point_to_remove = concave_points[i]
            previous_point_in_list, next_point_in_list = self._enveloping_points(point_to_remove,
                                                                                 total_points_list)
            total_points_list.remove(point_to_remove)
            concave_points.remove(point_to_remove)
            # Was any of the adjacent points convex? -> check if changed status to concave
            for convex_point in convex_points:
              if convex_point == previous_point_in_list:
                concave_points, convex_points, end_loop = self._if_concave_change_status(normal,
                                                                                         points_list,
                                                                                         convex_point,
                                                                                         total_points_list,
                                                                                         concave_points,
                                                                                         convex_points,
                                                                                         previous_point_in_list)
                if end_loop:
                  break
                continue
              if convex_point == next_point_in_list:
                concave_points, convex_points, end_loop = self._if_concave_change_status(normal,
                                                                                         points_list,
                                                                                         convex_point,
                                                                                         total_points_list,
                                                                                         concave_points,
                                                                                         convex_points,
                                                                                         next_point_in_list)
                if end_loop:
                  break
                continue
            break
        if len(total_points_list) <= 3 and len(convex_points) > 0:
          sys.stderr.write('Not able to triangulate polygon\n')
          return [self]
      if j >= 100:
        sys.stderr.write('Not able to triangulate polygon\n')
        return [self]
      last_ear = self._triangle(points_list, total_points_list, concave_points[1])
      ears.append(last_ear)
      self._triangles = ears
    return self._triangles

  @staticmethod
  def _starting_lists(points_list, normal) -> [List[float], List[float], List[float]]:
    """
    creates the list of vertices (points) that define the polygon (total_points_list), together with other two lists
    separating points between convex and concave
    :param points_list: points_list
    :param normal: normal
    :return: list[point], list[point], list[point]
    """
    concave_points = []
    convex_points = []
    # lists of concave and convex points
    # case 1: first point
    point = points_list[0:3]
    previous_point = points_list[len(points_list) - 3:]
    next_point = points_list[3:6]
    index = 0
    total_points_list = [index]
    if Polygon._point_is_concave(normal, point, previous_point, next_point):
      concave_points.append(index)
    else:
      convex_points.append(index)
    # case 2: all points except first and last
    for i in range(0, int((len(points_list) - 6) / 3)):
      point = points_list[(i + 1) * 3:(i + 2) * 3]
      previous_point = points_list[i * 3:(i + 1) * 3]
      next_point = points_list[(i + 2) * 3:(i + 3) * 3]
      index = i + 1
      total_points_list.append(index)
      if Polygon._point_is_concave(normal, point, previous_point, next_point):
        concave_points.append(index)
      else:
        convex_points.append(index)
    # case 3: last point
    point = points_list[len(points_list) - 3:]
    previous_point = points_list[len(points_list) - 6:len(points_list) - 3]
    next_point = points_list[0:3]
    index = int(len(points_list) / 3) - 1
    total_points_list.append(index)
    if Polygon._point_is_concave(normal, point, previous_point, next_point):
      concave_points.append(index)
    else:
      convex_points.append(index)
    return total_points_list, concave_points, convex_points

  @staticmethod
  def _triangle(points_list, total_points_list, point_position) -> Polygon:
    """
    creates a triangular polygon out of three points
    :param points_list: points_list
    :param total_points_list: [point]
    :param point_position: int
    :return: polygon
    """
    index = point_position * 3
    previous_point_index, next_point_index = Polygon._enveloping_points_indices(point_position, total_points_list)
    points = points_list[previous_point_index:previous_point_index + 3]
    points = np.append(points, points_list[index:index + 3])
    points = np.append(points, points_list[next_point_index:next_point_index + 3])
    rows = points.size // 3
    points = points.reshape(rows, 3)
    triangle = Polygon(points)
    return triangle

  @staticmethod
  def _enveloping_points_indices(point_position, total_points_list):
    """
    due to the fact that the lists are not circular, a method to find the previous and next points
    of an specific one is needed
    :param point_position: int
    :param total_points_list: [point]
    :return: int, int
    """
    previous_point_index = None
    next_point_index = None
    if point_position == total_points_list[0]:
      previous_point_index = total_points_list[len(total_points_list) - 1] * 3
      next_point_index = total_points_list[1] * 3
    if point_position == total_points_list[len(total_points_list) - 1]:
      previous_point_index = total_points_list[len(total_points_list) - 2] * 3
      next_point_index = total_points_list[0] * 3
    for i in range(1, len(total_points_list) - 1):
      if point_position == total_points_list[i]:
        previous_point_index = total_points_list[i - 1] * 3
        next_point_index = total_points_list[i + 1] * 3
    return previous_point_index, next_point_index

  @staticmethod
  def _enveloping_points(point_to_remove, total_points_list):
    """
    due to the fact that the lists are not circular, a method to find the previous and next points
    of an specific one is needed
    :param point_to_remove: point
    :param total_points_list: [point]
    :return: point, point
    """
    index = total_points_list.index(point_to_remove)
    if index == 0:
      previous_point_in_list = total_points_list[len(total_points_list) - 1]
      next_point_in_list = total_points_list[1]
    elif index == len(total_points_list) - 1:
      previous_point_in_list = total_points_list[len(total_points_list) - 2]
      next_point_in_list = total_points_list[0]
    else:
      previous_point_in_list = total_points_list[index - 1]
      next_point_in_list = total_points_list[index + 1]
    return previous_point_in_list, next_point_in_list

  @staticmethod
  def _is_ear(ear, points) -> bool:
    """
    finds whether a triangle is an ear of the polygon
    :param ear: polygon
    :param points: [point]
    :return: boolean
    """
    area_ear = ear.area
    for point in points:
      area_points = 0
      point_is_not_vertex = True
      for i in range(0, 3):
        if abs(np.linalg.norm(point) - np.linalg.norm(ear.coordinates[i])) < 0.0001:
          point_is_not_vertex = False
          break
      if point_is_not_vertex:
        for i in range(0, 3):
          if i != 2:
            new_points = ear.coordinates[i][:]
            new_points = np.append(new_points, ear.coordinates[i + 1][:])
            new_points = np.append(new_points, point[:])
          else:
            new_points = ear.coordinates[i][:]
            new_points = np.append(new_points, point[:])
            new_points = np.append(new_points, ear.coordinates[0][:])
          rows = new_points.size // 3
          new_points = new_points.reshape(rows, 3)
          new_triangle = Polygon(new_points)
          area_points += new_triangle.area
      if abs(area_points - area_ear) < 1e-6:
        # point_inside_ear = True
        return False
    return True

  @staticmethod
  def _if_concave_change_status(normal, points_list, convex_point, total_points_list,
                                concave_points, convex_points, point_in_list) -> [List[float], List[float], bool]:
    """
    checks whether an convex specific point change its status to concave after removing one ear in the polygon
    returning the new convex and concave points lists together with a flag advising that the list of total points
    already 3 and, therefore, the triangulation must be finished.
    :param normal: normal
    :param points_list: points_list
    :param convex_point: int
    :param total_points_list: [point]
    :param concave_points: [point]
    :param convex_points: [point]
    :param point_in_list: int
    :return: list[points], list[points], boolean
    """
    end_loop = False
    point = points_list[point_in_list * 3:(point_in_list + 1) * 3]
    pointer = total_points_list.index(point_in_list) - 1
    if pointer < 0:
      pointer = len(total_points_list) - 1
    previous_point = points_list[total_points_list[pointer] * 3:total_points_list[pointer] * 3 + 3]
    pointer = total_points_list.index(point_in_list) + 1
    if pointer >= len(total_points_list):
      pointer = 0
    next_point = points_list[total_points_list[pointer] * 3:total_points_list[pointer] * 3 + 3]
    if Polygon._point_is_concave(normal, point, previous_point, next_point):
      if concave_points[0] > convex_point:
        concave_points.insert(0, convex_point)
      elif concave_points[len(concave_points) - 1] < convex_point:
        concave_points.append(convex_point)
      else:
        for point_index in range(0, len(concave_points) - 1):
          if concave_points[point_index] < convex_point < concave_points[point_index + 1]:
            concave_points.insert(point_index + 1, convex_point)
      convex_points.remove(convex_point)
      end_loop = True
    return concave_points, convex_points, end_loop

  @staticmethod
  def _point_is_concave(normal, point, previous_point, next_point) -> bool:
    """
    returns whether a point is concave
    :param normal: normal
    :param point: point
    :param previous_point: point
    :param next_point: point
    :return: boolean
    """
    is_concave = False
    accepted_error = 0.1
    points = np.append(previous_point, point)
    points = np.append(points, next_point)
    rows = points.size // 3
    points = points.reshape(rows, 3)
    triangle = Polygon(points)
    error_sum = 0
    for i in range(0, len(normal)):
      error_sum += triangle.normal[i] - normal[i]
    if np.abs(error_sum) < accepted_error:
      is_concave = True
    return is_concave

  @staticmethod
  def _angle_between_vectors(vec_1, vec_2):
    """
    angle between vectors in radians
    :param vec_1: vector
    :param vec_2: vector
    :return: float
    """
    if np.linalg.norm(vec_1) == 0 or np.linalg.norm(vec_2) == 0:
      sys.stderr.write("Warning: impossible to calculate angle between planes' normal. Return 0\n")
      return 0
    cosine = np.dot(vec_1, vec_2) / np.linalg.norm(vec_1) / np.linalg.norm(vec_2)
    if cosine > 1 and cosine - 1 < 1e-5:
      cosine = 1
    elif cosine < -1 and cosine + 1 > -1e-5:
      cosine = -1
    alpha = math.acos(cosine)
    return alpha

  @property
  def inverse(self):
    """
    Get the polygon coordinates in reversed order
    :return: [np.ndarray]
    """
    if self._inverse is None:
      self._inverse = self.coordinates[::-1]
    return self._inverse

  def divide(self, plane):
    """
    Divides the polygon in two by a plane
    :param plane: plane that intersects with self to divide it in two parts (Plane)
    :return: Polygon, Polygon, [Point]
    """
    tri_polygons = Trimesh(vertices=self.vertices, faces=self.faces)
    intersection = trimesh.intersections.mesh_plane(tri_polygons, plane.normal, plane.origin.coordinates)
    polys_1 = trimesh.intersections.slice_mesh_plane(tri_polygons, plane.opposite_normal, plane.origin.coordinates)
    polys_2 = trimesh.intersections.slice_mesh_plane(tri_polygons, plane.normal, plane.origin.coordinates)
    triangles_1 = []
    for triangle in polys_1.triangles:
      triangles_1.append(Polygon(triangle))
    polygon_1 = self._reshape(triangles_1)
    triangles_2 = []
    for triangle in polys_2.triangles:
      triangles_2.append(Polygon(triangle))
    polygon_2 = self._reshape(triangles_2)
    return polygon_1, polygon_2, intersection

  def _reshape(self, triangles) -> Polygon:
    edges_list = []
    for i in range(0, len(triangles)):
      for edge in triangles[i].edges:
        if not self._edge_in_edges_list(edge, edges_list):
          edges_list.append(edge)
        else:
          edges_list = self._remove_from_list(edge, edges_list)
    points = self._order_points(edges_list)
    return Polygon(points)

  @staticmethod
  def _edge_in_edges_list(edge, edges_list):
    for edge_element in edges_list:
      if (edge_element[0].distance_to_point(edge[0]) == 0 and edge_element[1].distance_to_point(edge[1]) == 0) or \
          (edge_element[1].distance_to_point(edge[0]) == 0 and edge_element[0].distance_to_point(
            edge[1]) == 0):
        return True
    return False

  @staticmethod
  def _order_points(edges_list):
    # todo: not sure that this method works for any case -> RECHECK
    points = edges_list[0]
    for _ in range(0, len(points)):
      for i in range(1, len(edges_list)):
        point_1 = edges_list[i][0]
        point_2 = points[len(points) - 1]
        if point_1.distance_to_point(point_2) == 0:
          points.append(edges_list[i][1])
    points.remove(points[len(points) - 1])
    array_points = []
    for point in points:
      array_points.append(point.coordinates)
    return np.array(array_points)

  @staticmethod
  def _remove_from_list(edge, edges_list):
    new_list = []
    for edge_element in edges_list:
      if not ((edge_element[0].distance_to_point(edge[0]) == 0 and edge_element[1].distance_to_point(
          edge[1]) == 0) or
              (edge_element[1].distance_to_point(edge[0]) == 0 and edge_element[0].distance_to_point(
                edge[1]) == 0)):
        new_list.append(edge_element)
    return new_list

  @property
  def vertices(self) -> np.ndarray:
    """
    Get polyhedron vertices
    :return: np.ndarray(int)
    """
    if self._vertices is None:
      vertices, self._vertices = [], []
      _ = [vertices.extend(s.coordinates) for s in self.triangulate()]
      for vertex_1 in vertices:
        found = False
        for vertex_2 in self._vertices:
          found = False
          power = 0
          for dimension in range(0, 3):
            power += math.pow(vertex_2[dimension] - vertex_1[dimension], 2)
          distance = math.sqrt(power)
          if distance == 0:
            found = True
            break
        if not found:
          self._vertices.append(vertex_1)
      self._vertices = np.asarray(self._vertices)
    return self._vertices

  @property
  def faces(self) -> List[List[int]]:
    """
    Get polyhedron triangular faces
    :return: [face]
    """
    if self._faces is None:
      self._faces = []

      for polygon in self.triangulate():
        face = []
        points = polygon.coordinates
        if len(points) != 3:
          sub_polygons = polygon.triangulate()
          # todo: I modified this! To be checked @Guille
          if len(sub_polygons) >= 1:
            for sub_polygon in sub_polygons:
              face = []
              points = sub_polygon.coordinates
              for point in points:
                face.append(self._position_of(point, face))
              self._faces.append(face)
        else:
          for point in points:
            face.append(self._position_of(point, face))
          self._faces.append(face)
    return self._faces

  def _position_of(self, point, face):
    """
    position of a specific point in the list of points that define a face
    :return: int
    """
    vertices = self.vertices
    for i in range(len(vertices)):
      # ensure not duplicated vertex
      power = 0
      vertex2 = vertices[i]
      for dimension in range(0, 3):
        power += math.pow(vertex2[dimension] - point[dimension], 2)
      distance = math.sqrt(power)
      if i not in face and distance == 0:
        return i
    return -1
