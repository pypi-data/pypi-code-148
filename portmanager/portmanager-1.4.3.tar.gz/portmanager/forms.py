from django import forms
from django.conf import settings

from utilities.forms.fields import DynamicModelMultipleChoiceField
from dcim.models import Device
from netbox.forms import NetBoxModelFilterSetForm
from utilities.forms import BootstrapMixin

from .switches.vlan import VLANInterval
from .models import *

PLUGIN_CONF = settings.PLUGINS_CONFIG['portmanager']


class DeviceGroupForm(BootstrapMixin, forms.ModelForm):
    name = forms.CharField(
        max_length=80
    )
    description = forms.CharField(
        max_length=80,
        required=False,
        initial=""
    )
    devices = DynamicModelMultipleChoiceField (
        queryset=Device.objects.all(),
        required=False
    )
    vlans = forms.CharField(
        max_length=300,
        required=False,
        initial="[]"
    )
    community_string = forms.CharField(
        max_length=80,
        required=True,
        initial="public",
    )
    portsec_max = forms.IntegerField(
        min_value=1,
        max_value=16384,
        initial=PLUGIN_CONF.get("init_portsec", 8),
        required=True,
    )

    class Meta:
        model = DeviceGroup
        fields = [
            "name", "description", "devices", "vlans", "community_string", "portsec_max",
        ]
    
    def clean(self):
        vlans = self.cleaned_data.get("vlans")
        if not VLANInterval.check_syntax(vlans):
            self._errors["vlans"] = self.error_class([
                    'Bad format'])

        return super().clean()


class DeviceGroupFilterForm(NetBoxModelFilterSetForm):
    model = DeviceGroup
    fieldsets = (
        (None, ('q')),
    )


class ChangeLogFilterForm(NetBoxModelFilterSetForm):
    model = ChangeLog
    fieldsets = (
        (None, ('q')),
    )


class DeviceFilterForm(NetBoxModelFilterSetForm):
    model = Device

    fieldsets = (
        (None, ('q')),
    )
