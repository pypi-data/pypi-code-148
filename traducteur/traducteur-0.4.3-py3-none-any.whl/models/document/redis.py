import redis
import os

from ..base import BaseDatabaseModel


class BaseRedisModel(BaseDatabaseModel):
    @classmethod
    def get(cls, uuid: str):
        r = cls.redis_instance()
        out = r.get(uuid)
        return cls.from_json(out) if isinstance(out, bytes) else None

    def save(self):
        r = self.redis_instance()
        r.set(self.id, self.json(), ex=float(os.environ.get('REDIS_TTL', None)))
        return self

    def delete(self):
        r = self.redis_instance()
        r.delete(self.id)

    @staticmethod
    def redis_instance():
        return redis.Redis(host=os.environ.get('REDIS_HOST'), port=int(os.environ.get('REDIS_PORT', '6379')))