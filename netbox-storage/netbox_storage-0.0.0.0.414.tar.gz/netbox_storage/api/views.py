from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.routers import APIRootView

from netbox.api.viewsets import NetBoxModelViewSet

from netbox_storage.api.serializers import (
    DriveSerializer,
    FilesystemSerializer, PartitionSerializer, PhysicalVolumeSerializer, LogicalVolumeSerializer,
    VolumeGroupSerializer, LinuxVolumeSerializer
)
from netbox_storage.filters import DriveFilter, FilesystemFilter, \
    PartitionFilter, PhysicalVolumeFilter, LogicalVolumeFilter, VolumeGroupFilter, LinuxVolumeFilter
from netbox_storage.models import Drive, Filesystem, Partition, PhysicalVolume, LogicalVolume, VolumeGroup, LinuxVolume


class NetboxStorageRootView(APIRootView):
    """
    NetboxDNS API root view
    """

    def get_view_name(self):
        return "NetboxStorage"


class DriveViewSet(NetBoxModelViewSet):
    queryset = Drive.objects.all()
    serializer_class = DriveSerializer
    filterset_class = DriveFilter

    @action(detail=True, methods=["get"])
    def drive(self, request, pk=None):
        drives = Drive.objects.filter(drive__id=pk)
        serializer = DriveSerializer(drives, many=True, context={"request": request})
        return Response(serializer.data)


class FilesystemViewSet(NetBoxModelViewSet):
    queryset = Filesystem.objects.all()
    serializer_class = FilesystemSerializer
    filterset_class = FilesystemFilter

    @action(detail=True, methods=["get"])
    def filesystem(self, request, pk=None):
        filesystem = Filesystem.objects.filter(filesystem__id=pk)
        serializer = FilesystemSerializer(filesystem, many=True, context={"request": request})
        return Response(serializer.data)


class PartitionViewSet(NetBoxModelViewSet):
    queryset = Partition.objects.all()
    serializer_class = PartitionSerializer
    filterset_class = PartitionFilter

    @action(detail=True, methods=["get"])
    def partition(self, request, pk=None):
        partition = Partition.objects.filter(partition__id=pk)
        serializer = PartitionSerializer(partition, many=True, context={"request": request})
        return Response(serializer.data)


class PhysicalVolumeViewSet(NetBoxModelViewSet):
    queryset = PhysicalVolume.objects.all()
    serializer_class = PhysicalVolumeSerializer
    filterset_class = PhysicalVolumeFilter

    @action(detail=True, methods=["get"])
    def physicalvolume(self, request, pk=None):
        physicalvolume = PhysicalVolume.objects.filter(physicalvolume__id=pk)
        serializer = PhysicalVolumeSerializer(physicalvolume, many=True, context={"request": request})
        return Response(serializer.data)


class LogicalVolumeViewSet(NetBoxModelViewSet):
    queryset = LogicalVolume.objects.all()
    serializer_class = LogicalVolumeSerializer
    filterset_class = LogicalVolumeFilter

    @action(detail=True, methods=["get"])
    def logicalvolume(self, request, pk=None):
        logicalvolume = LogicalVolume.objects.filter(logicalvolume__id=pk)
        serializer = LogicalVolumeSerializer(logicalvolume, many=True, context={"request": request})
        return Response(serializer.data)


class VolumeGroupViewSet(NetBoxModelViewSet):
    queryset = VolumeGroup.objects.all()
    serializer_class = VolumeGroupSerializer
    filterset_class = VolumeGroupFilter

    @action(detail=True, methods=["get"])
    def volumegroup(self, request, pk=None):
        volumegroup = VolumeGroup.objects.filter(volumegroup__id=pk)
        serializer = VolumeGroupSerializer(volumegroup, many=True, context={"request": request})
        return Response(serializer.data)


class LinuxVolumeViewSet(NetBoxModelViewSet):
    queryset = LinuxVolume.objects.all()
    serializer_class = LinuxVolumeSerializer
    filterset_class = LinuxVolumeFilter

    @action(detail=True, methods=["get"])
    def linuxvolume(self, request, pk=None):
        linuxvolume = LinuxVolume.objects.filter(linuxvolume__id=pk)
        serializer = LinuxVolumeSerializer(linuxvolume, many=True, context={"request": request})
        return Response(serializer.data)
