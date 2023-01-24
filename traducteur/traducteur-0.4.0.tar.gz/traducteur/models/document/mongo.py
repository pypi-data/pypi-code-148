import os

from bson import ObjectId
from typing import Optional
from pydantic import Field

from ..base import BaseDatabaseModel
from ...managers.mongo import MongoModelManager


class PydanticObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')


class BaseMongoModel(BaseDatabaseModel):
    id: Optional[PydanticObjectId] = Field(alias='_id')

    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        json_encoders = {
            ObjectId: str,
            PydanticObjectId: str
        }

    def save(self):
        manager = self.__get_manager()
        if self.created_at is None:
            super().save()
            return manager.insert_one(self)
        else:
            super().save()
            return manager.update_one(self)

    def delete(self):
        super().delete()
        manager = self.__get_manager()
        return manager.delete_one(self)

    @classmethod
    def __get_manager(cls) -> MongoModelManager:
        con_str = os.environ['MONGO_CONNECTION_STR']
        db_name = os.environ['MONGO_DATABASE_NAME']
        return MongoModelManager(con_str, db_name)

    @classmethod
    def get(cls, id: str):
        manager = cls.__get_manager()
        result = manager.get_one(cls.__name__, id)
        return cls.from_dict(result) if result else None

    @classmethod
    def get_where_raw(cls, query, **kwargs):
        manager = cls.__get_manager()
        return manager.get_many(cls.__name__, query, **kwargs)

    @classmethod
    def get_where(cls, query, **kwargs):
        result = cls.get_where_raw(query, **kwargs)
        return [cls.from_dict(i) for i in result] if len(result) > 0 else None

    @classmethod
    def get_one_where(cls, query, **kwargs):
        manager = cls.__get_manager()
        result = manager.get_one(cls.__name__, query, **kwargs)
        return cls.from_dict(result) if result else None

    @classmethod
    def all(cls, **kwargs):
        manager = cls.__get_manager()
        result = manager.get_all(cls.__name__, **kwargs)
        return [cls.from_dict(i) for i in result] if len(result) > 0 else None

    @classmethod
    def exists(cls, id: str) -> bool:
        try:
            return cls.__get_manager().exists(cls.__name__, id=id)
        except Exception:
            return False

    @classmethod
    def exists_where(cls, query) -> bool:
        try:
            return cls.__get_manager().exists_where(cls.__name__, query)
        except Exception:
            return False
