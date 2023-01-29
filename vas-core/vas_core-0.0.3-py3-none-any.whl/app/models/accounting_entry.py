from django.db import models

from vas_core.app.models import BaseModelAbstract


class AccountConfig(BaseModelAbstract, models.Model):
    account = models.CharField(max_length=100, null=False, blank=False)
    description = models.CharField(max_length=100, null=False, blank=False)
    is_dynamic = models.BooleanField(default=False)


class FeeAccountConfig(BaseModelAbstract, models.Model):
    account = models.ForeignKey("AccountConfig", on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=5, max_digits=50, null=False,
                                 blank=False)
    is_percentage = models.BooleanField(default=False)


class AccountingEntry(BaseModelAbstract, models.Model):
    settlement_account = models.ForeignKey("AccountConfig",
                                           on_delete=models.CASCADE)
    fees = models.ManyToManyField("FeeAccountConfig", null=True, blank=True)
