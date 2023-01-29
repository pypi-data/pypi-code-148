import json

from django.db import models
from vas_core.app.models import BaseModelAbstract
from vas_core.app.models.base import LocalizationField


class Biller(BaseModelAbstract, models.Model):
    biller_id = models.CharField(unique=True, blank=False, null=False,
                                 max_length=255)
    name = LocalizationField()
    description = LocalizationField()
    category = models.ForeignKey("Category", null=True, blank=True,
                                 on_delete=models.SET_NULL)
    provider = models.ForeignKey("Provider", null=True, blank=True,
                                 on_delete=models.SET_NULL)
    country = models.ForeignKey("Country", null=True, blank=True,
                                on_delete=models.SET_NULL)
    display_sequence = models.IntegerField(default=1)
    channels = models.ManyToManyField("Channel")
    accounting_entry = models.OneToOneField("AccountingEntry",
                                            null=True, blank=True,
                                            on_delete=models.SET_NULL)
    narration_format = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-display_sequence', )

    def to_redis(self) -> str:
        channels = self.channels.all()
        data = {
            "name": self.name,
            "desc": self.description,
            "category_id": self.category.id if self.category else None,
            "provider_id": self.provider.id if self.provider else None,
            "country_code": self.country.code,
            "narration": self.narration_format,
            "display_sequence": self.display_sequence,
            "channels": ",".join([c.code for c in channels])
        }
        return json.dumps(data)
