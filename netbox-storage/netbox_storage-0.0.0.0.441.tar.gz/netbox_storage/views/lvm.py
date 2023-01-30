from netbox.views import generic

from netbox_storage.filters import DriveFilter, PartitionFilter
from netbox_storage.forms import (
    LVMForm,
)
from netbox_storage.models import Drive, Partition
from netbox_storage.tables import DriveTable, PartitionTable
from utilities.views import ViewTab, register_model_view


class LVMAddView(generic.ObjectEditView):
    """View for editing a Drive instance."""
    queryset = Drive.objects.all()
    form = LVMForm
    default_return_url = "plugins:netbox_storage:drive_list"
