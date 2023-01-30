import datetime
from peewee import *


class BasePeeweeModel(Model):
    created_at = DateTimeField(default=datetime.datetime.now())
    updated_at = DateTimeField(default=datetime.datetime.now())
