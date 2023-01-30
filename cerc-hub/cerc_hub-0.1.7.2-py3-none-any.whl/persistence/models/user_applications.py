"""
Model representation of the user applications
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Guille Gutierrez Guillermo.GutierrezMorote@concordia.ca
"""

import datetime

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy import DateTime

from hub.persistence.db_config import Base


class UserApplications(Base):
  """
  A model representation of the user applications
  """
  __tablename__ = "user_applications"
  user_id = Column(Integer, ForeignKey('user.id'))
  application_id = Column(Integer, ForeignKey('application.id'))

  created = Column(DateTime, default=datetime.datetime.utcnow)
  updated = Column(DateTime, default=datetime.datetime.utcnow)

  def __init__(self, user_id, application_id):
    self.user_id = user_id
    self.application_id = application_id
