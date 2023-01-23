from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

from netbox.models import RestrictedQuerySet, NetBoxModel, CloningMixin
from dcim.models import Device


class DeviceGroup(CloningMixin, models.Model):
    name = models.CharField(
        max_length=80,
        unique=True,
    )
    description = models.CharField(
        max_length=80,
        default=None
    )
    devices = models.ManyToManyField(
        Device,
        related_name="device_groups"
    )
    vlans = models.CharField(
        max_length=300,
        default="[]"
    )
    community_string = models.CharField(
        max_length=80,
        default="",
    )
    portsec_max = models.IntegerField(
        default=8,
    )
    objects = RestrictedQuerySet.as_manager()

    class Meta:
        verbose_name = "Device Group"
        verbose_name_plural = "Device Groups"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('plugins:portmanager:devicegroup', args=[self.pk])


class ChangeLog(CloningMixin, models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    date = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        db_index=True
    )
    device = models.ForeignKey(
        to=Device,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        default=None,
    )
    device_group = models.ForeignKey(
        to=DeviceGroup,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    interface = models.CharField(
        max_length=80,
        editable=False,
        default=""
    )
    component = models.CharField(
        max_length=80,
        editable=False,
    )
    before = models.CharField(
        max_length=80,
        editable=False,
    )
    after = models.CharField(
        max_length=80,
        editable=False,
    )

    objects = RestrictedQuerySet.as_manager()

    class Meta:
        ordering = ["-date"]
        verbose_name = "Change Log"
        verbose_name_plural = "Changes Log"
        
    def get_absolute_url(self):
        return reverse('plugins:portmanager:changelog', args=[self.pk])
