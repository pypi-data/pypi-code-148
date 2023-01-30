"""
Occupant module
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Sanam Dabirian sanam.dabirian@mail.concordia.ca
Code contributors: Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""


class Occupant:
  """
  Occupant class
  """

  def __init__(self):
    """
    Constructor
    """

    self._heat_dissipation = None
    self._occupancy_rate = None
    self._occupant_type = None
    self._arrival_time = None
    self._departure_time = None
    self._break_time = None
    self._day_of_week = None
    self._pd_of_meetings_duration = None

  @property
  def heat_dissipation(self):
    """
    Get heat dissipation of occupants in W/person
    :return: float
    """
    return self._heat_dissipation

  @heat_dissipation.setter
  def heat_dissipation(self, value):
    """
    Set heat dissipation of occupants in W/person
    :param value: float
    """
    self._heat_dissipation = float(value)

  @property
  def occupancy_rate(self):
    """
    Get rate of schedules
    :return: float
    """
    return self._occupancy_rate

  @occupancy_rate.setter
  def occupancy_rate(self, value):
    """
    Set rate of schedules
    :param value: float
    """
    self._occupancy_rate = float(value)

  @property
  def occupant_type(self):
    """
    Get type of schedules
    :return: str
    """
    return self._occupant_type

  @occupant_type.setter
  def occupant_type(self, value):
    """
    Set type of schedules
    :param value: float
    """
    self._occupant_type = float(value)

  @property
  def arrival_time(self):
    """
    Get the arrival time of the occupant (for office building) in UTC with format YYYYMMDD HH:mm:ss
    :return: time
    """
    return self._arrival_time

  @arrival_time.setter
  def arrival_time(self, value):
    """
    Set the arrival time of the occupant (for office building) in UTC with format YYYYMMDD HH:mm:ss
    :param value: time
    """
    self._arrival_time = value

  @property
  def departure_time(self):
    """
    Get the departure time of the occupant (for office building) in UTC with format YYYYMMDD HH:mm:ss
    :return: time
    """
    return self._departure_time

  @departure_time.setter
  def departure_time(self, value):
    """
    Set the departure time of the occupant (for office building) in UTC with format YYYYMMDD HH:mm:ss
    :param value: str
    """
    self._departure_time = value

  @property
  def break_time(self):
    """
    Get the lunch or break time of the occupant (for office building) in UTC with format ????
    :return: break time
    """
    # todo @Sanam: define this format, is it the starting time? is it a list with both, starting and ending time?
    return self._break_time

  @property
  def day_of_week(self):
    """
    Get the day of the week (MON, TUE, WED, THU, FRI, SAT, SUN)
    :return: str
    """
    # todo @Sanam: is this a property or should it be a function
    #  to get the day of the week of an specific day of the year?
    return self._day_of_week

  @property
  def pd_of_meetings_duration(self):
    """
    Get the probability distribution of the meeting duration
    :return: ??
    """
    # todo @Sanam: what format are you expecting here??
    return self._pd_of_meetings_duration

  @pd_of_meetings_duration.setter
  def pd_of_meetings_duration(self, value):
    """
    Get the probability distribution of the meeting duration
    :param value: ??
    :return:
    """
    # todo @Sanam: what format are you expecting here??
    self._pd_of_meetings_duration = value
