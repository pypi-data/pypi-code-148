"""
Model representation of a City
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Peter Yefi peteryefi@gmail.com
"""

from sqlalchemy import Column, Integer, String, Sequence, ForeignKey
from sqlalchemy import DateTime, PickleType, Float
from hub.persistence.db_config import Base
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
import datetime
import numpy as np


class City(Base):
  """A model representation of a city
  """
  __tablename__ = "city"
  id = Column(Integer, Sequence('city_id_seq'), primary_key=True)
  city = Column(PickleType, nullable=False)
  name = Column(String, nullable=False)
  srs_name = Column(String, nullable=False)
  climate_reference_city = Column(String, nullable=True)
  time_zone = Column(String, nullable=True)
  country_code = Column(String, nullable=False)
  latitude = Column(Float)
  longitude = Column(Float)
  lower_corner = Column(JSONB, nullable=False)
  upper_corner = Column(JSONB, nullable=False)
  hub_release = Column(String, nullable=False)
  city_version = Column(Integer, nullable=False)
  user_id = Column(Integer, ForeignKey('user.id'))
  user = relationship("User", back_populates="cities")
  created = Column(DateTime, default=datetime.datetime.utcnow)
  updated = Column(DateTime, default=datetime.datetime.utcnow)

  def __init__(self, city, name, srs_name, country_code, l_corner, u_corner, user_id):
    self.city = city
    self.user_id = user_id
    self.name = name
    self.srs_name = srs_name
    self.country_code = country_code
    l_corner = l_corner.tolist() if type(l_corner) == np.ndarray else l_corner
    u_corner = u_corner.tolist() if type(u_corner) == np.ndarray else u_corner
    self.lower_corner = l_corner
    self.upper_corner = u_corner
