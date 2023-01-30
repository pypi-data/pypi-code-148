
from hub.persistence import BaseRepo
from hub.persistence.models import City
from hub.persistence.models import HeatPumpSimulation
from hub.persistence.models import User
from hub.persistence.models import UserRoles
from hub.persistence.models import Application
from hub.persistence.models import UserApplications
from hub.persistence.repositories import UserRepo
from hub.hub_logger import logger


class DBSetup:

  def __init__(self, db_name, app_env, dotenv_path):
    """
    Creates database tables and a default admin user
    :param db_name:
    :param app_env:
    :param dotenv_path:
    """
    repo = BaseRepo(db_name=db_name, app_env=app_env, dotenv_path=dotenv_path)
    User.__table__.create(bind=repo.engine, checkfirst=True)
    City.__table__.create(bind=repo.engine, checkfirst=True)
    Application.__table__.create(bind=repo.engine, checkfirst=True)
    UserApplications.__table__.create(bind=repo.engine, checkfirst=True)
    HeatPumpSimulation.__table__.create(bind=repo.engine, checkfirst=True)
    self._user_repo = UserRepo(db_name=db_name, app_env=app_env, dotenv_path=dotenv_path)
    self._create_admin_user(self._user_repo)

  @staticmethod
  def _create_admin_user(user_repo):
    email = 'admin@hub.com'
    password = 'HubAdmin#!98'
    print('Creating default admin user...')
    user = user_repo.insert('Administrator', email, password, UserRoles.Admin)
    if type(user) is dict:
      logger.info(user)
    else:
      print(f'Created Admin user with email: {email}, password: {password} and role: {UserRoles.Admin.value}')
      logger.info(f'Created Admin user with email: {email}, password: {password} and role: {UserRoles.Admin.value}')
      print('Remember to change the admin default password and email address with the UserFactory')
