from . import models
from netbox.search import SearchIndex, register_search


@register_search
class DriveIndex(SearchIndex):
    model = models.Drive
    fields = (
        ('size', 100),
        ('identifier', 100),
        ('description', 100),
    )


@register_search
class PartitionIndex(SearchIndex):
    model = models.Partition
    fields = (
        ('device', 100),
        ('size', 100),
        ('type', 100),
        ('description', 100),
    )


@register_search
class VolumeGroupIndex(SearchIndex):
    model = models.VolumeGroup
    fields = (
        ('vg_name', 100),
        ('description', 100),
    )


@register_search
class PhysicalVolumeIndex(SearchIndex):
    model = models.PhysicalVolume
    fields = (
        ('pv_name', 100),
        ('description', 100),
    )


@register_search
class FilesystemIndex(SearchIndex):
    model = models.PhysicalVolume
    fields = (
        ('filesystem', 100),
        ('description', 100),
    )


@register_search
class LogicalVolumeIndex(SearchIndex):
    model = models.LogicalVolume
    fields = (
        ('lv_name', 100),
        ('size', 100),
        ('path', 100),
        ('description', 100),
    )


@register_search
class LinuxVolumeIndex(SearchIndex):
    model = models.LogicalVolume
    fields = (
        ('size', 100),
        ('path', 100),
        ('description', 100),
    )
