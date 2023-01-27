"""
Constant module
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2023 Concordia CERC group
Project Coder Peter Yefi peteryefi@gmail.com
"""

import bcrypt
import re


class Auth(object):

  @staticmethod
  def validate_password(password: str) -> bool:
    """
    Validates a password
    :param password: the password to validate
    :return:
    """
    pattern = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
    pattern = re.compile(pattern)
    if not re.search(pattern, password):
      raise ValueError("Password must be between 6 to 20 characters and must have at least a number, an uppercase "
                       "letter, a lowercase letter, and a special character")
    return True

  @staticmethod
  def hash_password(password: str) -> str:
    """
    Hashes a password
    :param password: the password to be hashed
    :return:
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(14)).decode('utf-8')

  @staticmethod
  def check_password(password: str, hashed_password) -> bool:
    """
    Hashes a password
    :param password: the password to be checked
    :param hashed_password: the hashed password
    :return:
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))





