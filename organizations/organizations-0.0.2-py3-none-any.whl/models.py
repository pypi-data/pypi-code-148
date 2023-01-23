from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from multiselectfield import MultiSelectField
from .enums import NetworksNames


class UserProxy(User):
    class Meta:
        proxy = True
        verbose_name = _("Operator")
        verbose_name_plural = _("Operators")


class OrganizationKeys(models.Model):
    address = models.CharField(max_length=100)
    private_key = models.CharField(max_length=500)
    public_key = models.CharField(max_length=500)
    mnemonic = models.TextField()

    def __str__(self) -> str:
        return self.address


class Organization(models.Model):
    networks = MultiSelectField(
        choices=NetworksNames.choices(), max_choices=2, max_length=1000
    )
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=255)
    keys = models.ForeignKey(
        OrganizationKeys, on_delete=models.SET_NULL, blank=True, null=True
    )
    operators = models.ManyToManyField(UserProxy)

    def __str__(self) -> str:
        return self.name


class OrganizationDID(models.Model):
    network_name = models.CharField(max_length=2500)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    did = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.organization.name


class Issuer(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.organization.name


class Intermediary(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.organization.name
