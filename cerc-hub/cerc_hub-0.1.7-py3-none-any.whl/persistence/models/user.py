"""
Model representation of a User
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Peter Yefi peteryefi@gmail.com
"""

from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy import DateTime, Enum
from hub.persistence.db_config import Base
import datetime
from sqlalchemy.orm import validates
import re
import enum
from sqlalchemy.orm import relationship


class UserRoles(enum.Enum):
  Admin = 'Admin'
  Hub_Reader = 'Hub_Reader'


class User(Base):
  """A model representation of a city
  """
  __tablename__ = "user"
  id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
  name = Column(String, nullable=False)
  email = Column(String, nullable=False, unique=True)
  password = Column(String, nullable=False)
  role = Column(Enum(UserRoles), nullable=False, default=UserRoles.Hub_Reader)
  cities = relationship("City", back_populates="user")
  created = Column(DateTime, default=datetime.datetime.utcnow)
  updated = Column(DateTime, default=datetime.datetime.utcnow)

  @validates("email")
  def validate_email(self, key, address):
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if not re.match(pattern, address):
      raise ValueError("failed simple email validation")
    return address

  def __init__(self, name, email, password, role):
    self.name = name
    self.email = email
    self.password = password
    self.role = role
