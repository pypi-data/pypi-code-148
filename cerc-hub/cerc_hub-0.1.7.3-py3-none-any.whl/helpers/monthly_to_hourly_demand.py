"""
monthly_to_hourly_demand module
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""
import calendar as cal
import pandas as pd
from hub.city_model_structure.building_demand.occupant import Occupant
import hub.helpers.constants as cte


class MonthlyToHourlyDemand:
  """
  MonthlyToHourlyDemand class
  """
  def __init__(self, building, conditioning_seasons):
    self._hourly_heating = pd.DataFrame()
    self._hourly_cooling = pd.DataFrame()
    self._building = building
    self._conditioning_seasons = conditioning_seasons

  def hourly_heating(self, key):
    """
    hourly distribution of the monthly heating of a building
    :param key: string
    :return: [hourly_heating]
    """
    # todo: this method and the insel model have to be reviewed for more than one thermal zone
    external_temp = self._building.external_temperature[cte.HOUR]
    # todo: review index depending on how the schedules are defined, either 8760 or 24 hours
    for usage in self._building.usages:
      temp_set = float(usage.heating_setpoint)-3
      temp_back = float(usage.heating_setback)-3
      # todo: if these are data frames, then they should be called as (Occupancy should be in low case):
      # usage.schedules.Occupancy
      # self._conditioning_seasons.heating
      occupancy = Occupant().get_complete_year_schedule(usage.schedules['Occupancy'])
      heating_schedule = self._conditioning_seasons['heating']

      hourly_heating = []
      i = 0
      j = 0
      temp_grad_day = []
      for month in range(1, 13):
        temp_grad_month = 0
        month_range = cal.monthrange(2015, month)[1]
        for _ in range(1, month_range+1):
          external_temp_med = 0
          for hour in range(0, 24):
            external_temp_med += external_temp[key][i]/24
          for hour in range(0, 24):
            if external_temp_med < temp_set and heating_schedule[month-1] == 1:
              if occupancy[hour] > 0:
                hdd = temp_set - external_temp[key][i]
                if hdd < 0:
                  hdd = 0
                temp_grad_day.append(hdd)
              else:
                hdd = temp_back - external_temp[key][i]
                if hdd < 0:
                  hdd = 0
                temp_grad_day.append(hdd)
            else:
              temp_grad_day.append(0)

            temp_grad_month += temp_grad_day[i]
            i += 1

        for _ in range(1, month_range + 1):
          for hour in range(0, 24):
            monthly_demand = self._building.heating[cte.MONTH][month-1]
            if monthly_demand == 'NaN':
              monthly_demand = 0
            if temp_grad_month == 0:
              hourly_demand = 0
            else:
              hourly_demand = float(monthly_demand)*float(temp_grad_day[j])/float(temp_grad_month)
            hourly_heating.append(hourly_demand)
            j += 1
      self._hourly_heating = pd.DataFrame(data=hourly_heating, columns=['monthly to hourly'])
    return self._hourly_heating

  def hourly_cooling(self, key):
    """
    hourly distribution of the monthly cooling of a building
    :param key: string
    :return: [hourly_cooling]
    """
    # todo: this method and the insel model have to be reviewed for more than one thermal zone
    external_temp = self._building.external_temperature[cte.HOUR]
    # todo: review index depending on how the schedules are defined, either 8760 or 24 hours
    for usage in self._building.usages:
      temp_set = float(usage.cooling_setpoint)
      temp_back = 100
      occupancy = Occupant().get_complete_year_schedule(usage.schedules['Occupancy'])
      cooling_schedule = self._conditioning_seasons['cooling']

      hourly_cooling = []
      i = 0
      j = 0
      temp_grad_day = []
      for month in range(1, 13):
        temp_grad_month = 0
        month_range = cal.monthrange(2015, month)[1]
        for _ in range(1, month_range[1] + 1):
          for hour in range(0, 24):
            if external_temp[key][i] > temp_set and cooling_schedule[month - 1] == 1:
              if occupancy[hour] > 0:
                cdd = external_temp[key][i] - temp_set
                if cdd < 0:
                  cdd = 0
                temp_grad_day.append(cdd)
              else:
                cdd = external_temp[key][i] - temp_back
                if cdd < 0:
                  cdd = 0
                temp_grad_day.append(cdd)
            else:
              temp_grad_day.append(0)

            temp_grad_month += temp_grad_day[i]
            i += 1

        for _ in range(1, month_range[1] + 1):
          for hour in range(0, 24):
            #            monthly_demand = self._building.heating[cte.MONTH]['INSEL'][month-1]
            monthly_demand = self._building.cooling[cte.MONTH][month - 1]
            if monthly_demand == 'NaN':
              monthly_demand = 0
            if temp_grad_month == 0:
              hourly_demand = 0
            else:
              hourly_demand = float(monthly_demand) * float(temp_grad_day[j]) / float(temp_grad_month)
            hourly_cooling.append(hourly_demand)
            j += 1
      self._hourly_cooling = pd.DataFrame(data=hourly_cooling, columns=['monthly to hourly'])
    return self._hourly_cooling
