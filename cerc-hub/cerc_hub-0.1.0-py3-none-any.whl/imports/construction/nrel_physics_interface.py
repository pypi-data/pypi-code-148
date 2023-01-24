"""
Nrel-based interface, it reads format defined within the CERC team based on NREL structure
and enriches the city with archetypes and materials
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""

from imports.construction.helpers.storeys_generation import StoreysGeneration


class NrelPhysicsInterface:
  """
  NrelPhysicsInterface abstract class
  """

  # todo: verify windows
  @staticmethod
  def _calculate_view_factors(thermal_zone):
    """
    Get thermal zone view factors matrix
    :return: [[float]]
    """
    total_area = 0
    for thermal_boundary in thermal_zone.thermal_boundaries:
      total_area += thermal_boundary.opaque_area
      for thermal_opening in thermal_boundary.thermal_openings:
        total_area += thermal_opening.area

    view_factors_matrix = []
    for thermal_boundary_1 in thermal_zone.thermal_boundaries:
      values = []
      for thermal_boundary_2 in thermal_zone.thermal_boundaries:
        value = 0
        if thermal_boundary_1.id != thermal_boundary_2.id:
          value = thermal_boundary_2.opaque_area / (total_area - thermal_boundary_1.opaque_area)
        values.append(value)
      for thermal_boundary in thermal_zone.thermal_boundaries:
        for thermal_opening in thermal_boundary.thermal_openings:
          value = thermal_opening.area / (total_area - thermal_boundary_1.opaque_area)
          values.append(value)
      view_factors_matrix.append(values)

    for thermal_boundary_1 in thermal_zone.thermal_boundaries:
      values = []
      for thermal_opening_1 in thermal_boundary_1.thermal_openings:
        for thermal_boundary_2 in thermal_zone.thermal_boundaries:
          value = thermal_boundary_2.opaque_area / (total_area - thermal_opening_1.area)
          values.append(value)
        for thermal_boundary in thermal_zone.thermal_boundaries:
          for thermal_opening_2 in thermal_boundary.thermal_openings:
            value = 0
            if thermal_opening_1.id != thermal_opening_2.id:
              value = thermal_opening_2.area / (total_area - thermal_opening_1.area)
            values.append(value)
        view_factors_matrix.append(values)
    thermal_zone.view_factors_matrix = view_factors_matrix

  @staticmethod
  def _create_storeys(building, archetype, divide_in_storeys):
    building.average_storey_height = archetype.average_storey_height
    building.storeys_above_ground = 1
    thermal_zones = StoreysGeneration(building, building.internal_zones[0],
                                      divide_in_storeys=divide_in_storeys).thermal_zones
    building.internal_zones[0].thermal_zones = thermal_zones

  def enrich_buildings(self):
    """
    Raise not implemented error
    """
    raise NotImplementedError
