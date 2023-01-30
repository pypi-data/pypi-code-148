from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from multiselectfield import MultiSelectField
from network_service_client.client import NetworksNames


class UserProxy(User):
    class Meta:
        proxy = True
        verbose_name = _("Operator")
        verbose_name_plural = _("Operators")

    def __str__(self):
        return f"{self.username} - {self.email}"


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
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    keys = models.ForeignKey(
        OrganizationKeys, on_delete=models.SET_NULL, blank=True, null=True
    )
    operators = models.ManyToManyField(UserProxy, blank=True)

    def __str__(self) -> str:
        return self.name


class OperatorDID(models.Model):
    network_name = models.CharField(max_length=2500)
    operator = models.ForeignKey(UserProxy, on_delete=models.CASCADE)
    did = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{self.operator.email} - {self.network_name} - {self.did}"


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


class Subject(models.Model):
    email = models.EmailField(_("Email"), max_length=200, null=True, blank=True)
    givenName = models.CharField(max_length=255, blank=True)
    familyName = models.CharField(max_length=255, blank=True)
    birthDate = models.DateField(blank=True, null=True)
    intermediary = models.ForeignKey(Intermediary, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Subject")
        verbose_name_plural = _("Subjects")

    def __str__(self) -> str:
        display_text = self.email
        return display_text


class SubjectDID(models.Model):
    network_name = models.CharField(max_length=2500)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    did = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.organization.name


class OrganizationOnboardingNotification(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    operator = models.ForeignKey(UserProxy, on_delete=models.CASCADE)
    sended_at = models.DateTimeField()
    