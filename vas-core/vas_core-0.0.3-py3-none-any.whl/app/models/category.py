import json

from django.db import models
from vas_core.app.models.base import BaseModelAbstract, LocalizationField


class Category(BaseModelAbstract, models.Model):
    description = LocalizationField()
    country = models.ForeignKey("Country", on_delete=models.DO_NOTHING,
                                null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('description', )

    def get_description(self, lang) -> str:
        return self.description.get(lang.lower())

    def to_redis(self) -> str:
        data = {
            "desc": self.description,
            "country_code": self.country.code
        }
        return json.dumps(data)
