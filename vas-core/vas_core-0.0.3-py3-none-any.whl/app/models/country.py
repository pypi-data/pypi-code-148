import json

from django.db import models
from vas_core.app.models.base import BaseModelAbstract


class Country(BaseModelAbstract, models.Model):
    name = models.CharField(max_length=255, blank=False, null=False,
                            unique=True)
    code = models.CharField(max_length=3, blank=False, null=False,
                            unique=True)
    default_lang = models.CharField(default='en', max_length=2, null=True,
                                    blank=True)

    def save(self, keep_deleted=False, **kwargs):
        self.code = self.code.upper()
        super(BaseModelAbstract, self).save(keep_deleted, **kwargs)

    def to_redis(self) -> str:
        data = {
            "name": self.name,
            "lang": self.default_lang,
        }
        return json.dumps(data)

