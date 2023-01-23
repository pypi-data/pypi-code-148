from netbox.api.viewsets import NetBoxModelViewSet
from portmanager.models import DeviceGroup, ChangeLog
from .serializers import DeviceGroupSerializer, ChangeLogSerializer

class DeviceGroupViewSet(NetBoxModelViewSet):
    queryset = DeviceGroup.objects.all()
    serializer_class = DeviceGroupSerializer

class ChangeLogViewSet(NetBoxModelViewSet):
    queryset = ChangeLog.objects.all()
    serializer_class = ChangeLogSerializer