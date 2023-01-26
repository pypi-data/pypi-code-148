from netbox.views import generic

from netbox_storage.filters import VolumeGroupFilter
from netbox_storage.forms import (
    VolumeGroupImportForm,
    VolumeGroupFilterForm,
    VolumeGroupForm,
    VolumeGroupBulkEditForm
)

from netbox_storage.models import VolumeGroup
from netbox_storage.tables import VolumeGroupTable


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
