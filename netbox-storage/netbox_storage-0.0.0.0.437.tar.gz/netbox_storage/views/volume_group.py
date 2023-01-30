from netbox.views import generic

from netbox_storage.filters import VolumeGroupFilter, PhysicalVolumeFilter, LogicalVolumeFilter
from netbox_storage.forms import (
    VolumeGroupImportForm,
    VolumeGroupFilterForm,
    VolumeGroupForm,
    VolumeGroupBulkEditForm
)

from netbox_storage.models import VolumeGroup, PhysicalVolume, LogicalVolume
from netbox_storage.tables import VolumeGroupTable, PhysicalVolumeTable, LogicalVolumeTable
from utilities.views import register_model_view, ViewTab


class VolumeGroupListView(generic.ObjectListView):
    queryset = VolumeGroup.objects.all()
    filterset = VolumeGroupFilter
    filterset_form = VolumeGroupFilterForm
    table = VolumeGroupTable


class VolumeGroupView(generic.ObjectView):
    """Display VolumeGroup details"""

    queryset = VolumeGroup.objects.all()


class VolumeGroupEditView(generic.ObjectEditView):
    """View for editing a VolumeGroup instance."""

    queryset = VolumeGroup.objects.all()
    form = VolumeGroupForm
    default_return_url = "plugins:netbox_storage:volumegroup_list"


class VolumeGroupDeleteView(generic.ObjectDeleteView):
    queryset = VolumeGroup.objects.all()
    default_return_url = "plugins:netbox_storage:volumegroup_list"


class VolumeGroupBulkImportView(generic.BulkImportView):
    queryset = VolumeGroup.objects.all()
    model_form = VolumeGroupImportForm
    table = VolumeGroupTable
    default_return_url = "plugins:netbox_storage:volumegroup_list"


class VolumeGroupBulkEditView(generic.BulkEditView):
    queryset = VolumeGroup.objects.all()
    filterset = VolumeGroupFilter
    table = VolumeGroupTable
    form = VolumeGroupBulkEditForm


class VolumeGroupBulkDeleteView(generic.BulkDeleteView):
    queryset = VolumeGroup.objects.all()
    table = VolumeGroupTable


@register_model_view(VolumeGroup, "physicalvolumes")
class VolumeGroupPhysicalVolumeListView(generic.ObjectChildrenView):
    queryset = VolumeGroup.objects.all()
    child_model = PhysicalVolume
    table = PhysicalVolumeTable
    filterset = PhysicalVolumeFilter
    template_name = "netbox_storage/volumegroup/physicalvolume.html"
    hide_if_empty = True

    tab = ViewTab(
        label="Physical Volumes",
        badge=lambda obj: obj.physical_volume_count(),
        hide_if_empty=True,
    )

    def get_children(self, request, parent):
        return PhysicalVolume.objects.filter(
            vg=parent
        )


@register_model_view(VolumeGroup, "logicalvolumes")
class VolumeGroupPhysicalVolumeListView(generic.ObjectChildrenView):
    queryset = VolumeGroup.objects.all()
    child_model = LogicalVolume
    table = LogicalVolumeTable
    filterset = LogicalVolumeFilter
    template_name = "netbox_storage/volumegroup/logicalvolume.html"
    hide_if_empty = True

    tab = ViewTab(
        label="Logical Volumes",
        badge=lambda obj: obj.logical_volume_count(),
        hide_if_empty=True,
    )

    def get_children(self, request, parent):
        return LogicalVolume.objects.filter(
            vg=parent
        )
