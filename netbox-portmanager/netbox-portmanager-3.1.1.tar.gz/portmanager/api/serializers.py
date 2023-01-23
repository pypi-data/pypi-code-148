from netbox.api.serializers import NetBoxModelSerializer
from portmanager.models import DeviceGroup, ChangeLog
from dcim.api.nested_serializers import NestedDeviceSerializer

class DeviceGroupSerializer(NetBoxModelSerializer):

    devices = NestedDeviceSerializer(
        many=True,
        help_text="Netbox Devices"
    )

    class Meta:
        model = DeviceGroup
        fields = ('id', 'name','description', "devices", "vlans", "portsec_max")


class ChangeLogSerializer(NetBoxModelSerializer):

    user = NestedDeviceSerializer(
        many=False,
        help_text="User"
    )

    device_group = NestedDeviceSerializer(
        many=False,
        help_text="Device Group"
    )

    class Meta:
        model = ChangeLog
        fields = ('id', 'user', 'device', 'device_group', 'component', 'before', 'after')