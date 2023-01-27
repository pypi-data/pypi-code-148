"""
City repository with database CRUD operations
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Peter Yefi peteryefi@gmail.com
"""

from hub.persistence import BaseRepo
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from hub.persistence.models import User
from hub.persistence.models import UserRoles
from hub.helpers.auth import Auth
from typing import Union, Dict
from hub.hub_logger import logger
import datetime


class UserRepo(BaseRepo):
  _instance = None

  def __init__(self, db_name: str, dotenv_path: str, app_env: str):
    super().__init__(db_name, dotenv_path, app_env)

  def __new__(cls, db_name, dotenv_path, app_env):
    """
    Implemented for a singleton pattern
    """
    if cls._instance is None:
      cls._instance = super(UserRepo, cls).__new__(cls)
    return cls._instance

  def insert(self, name: str, email: str, password: str, role: UserRoles) -> Union[User, Dict]:
    user = self.get_by_email(email)
    if user is None:
      try:
        if Auth.validate_password(password):
          user = User(name=name, email=email, password=Auth.hash_password(password), role=role)
          self.session.add(user)
          self.session.flush()
          self.session.commit()
          return user
      except SQLAlchemyError as err:
        logger.error(f'An error occurred while creating user: {err}')
    else:
      return {'message': f'user with {email} email already exists'}

  def update(self, user_id: int, name: str, email: str, password: str, role: UserRoles) -> Union[Dict, None]:
    """
    Updates a user
    :param user_id: the id of the user to be updated
    :param name: the name of the user
    :param email: the email of the user
    :param password: the password of the user
    :param role: the role of the user
    :return:
    """
    try:
      if Auth.validate_password(password):
        self.session.query(User).filter(User.id == user_id) \
          .update({'name': name, 'email': email, 'password': Auth.hash_password(password), 'role': role,
                   'updated': datetime.datetime.utcnow()})
      self.session.commit()
    except SQLAlchemyError as err:
      logger.error(f'Error while updating user: {err}')
      return {'err_msg': 'Error occurred while updated user'}

  def get_by_email(self, email: str) -> [User]:
    """
    Fetch user based on the email address
    :param email: the email of the user
    :return: [User] with the provided email
    """
    try:
      return self.session.execute(select(User).where(User.email == email)).first()
    except SQLAlchemyError as err:
      logger.error(f'Error while fetching user by email: {err}')

  def delete_user(self, user_id: int):
    """
    Deletes a user with the id
    :param user_id: the user id
    :return: None
    """
    try:
      self.session.query(User).filter(User.id == user_id).delete()
      self.session.commit()
    except SQLAlchemyError as err:
      logger.error(f'Error while fetching user: {err}')

  def get_user_by_email_and_password(self, email: str, password: str) -> [User]:
    """
    Fetch user based on the email and password
    :param email: the email of the user
    :param password: the password of the user
    :return: [User] with the provided email and password
    """
    try:
      user = self.session.execute(select(User).where(User.email == email)).first()
      if user:
        if Auth.check_password(password, user[0].password):
          return user
        else:
          return {'message': 'Wrong email/password combination'}
      return {'message': 'user not found'}
    except SQLAlchemyError as err:
      logger.error(f'Error while fetching user by email: {err}')
