from django.core.validators import MinValueValidator
from django.forms import (
    CharField, FloatField,
)

from netbox.forms import (
    NetBoxModelBulkEditForm,
    NetBoxModelFilterSetForm,
    NetBoxModelImportForm,
    NetBoxModelForm,
)
from utilities.forms import (
    DynamicModelChoiceField,
    APISelect,
)

from django.urls import reverse_lazy

from netbox_storage.models import Filesystem, LinuxVolume, Drive, Partition
from virtualization.models import VirtualMachine


class LinuxVolumeForm(NetBoxModelForm):
    """Form for creating a new LinuxVolume object."""
    virtual_machine = DynamicModelChoiceField(
        queryset=VirtualMachine.objects.all(),
        required=False,
    )
    drive = DynamicModelChoiceField(
        queryset=Drive.objects.all(),
        query_params={
            'virtual_machine_id': '$virtual_machine',
        },
        help_text="The Storage Cluster of the drive",
    )
    partition = DynamicModelChoiceField(
        queryset=Partition.objects.all(),
        label="Partition",
        widget=APISelect(
            attrs={"data-url": reverse_lazy("plugins-api:netbox_storage-api:partition-list")}
        ),
        query_params={
            'drive_id': '$drive',
        },
        help_text="The Partition for the LinuxVolume e.g. /dev/sda1",
    )
    size = FloatField(
        label="Size (GB)",
        help_text="The size of the logical volume e.g. 25",
        validators=[MinValueValidator(0.0)],
    )
    path = CharField(
        label="Path",
        help_text="The mounted path of the volume e.g. /var/lib/docker",
    )
    fs = DynamicModelChoiceField(
        queryset=Filesystem.objects.all(),
        label="Filesystem Name",
        widget=APISelect(
            attrs={"data-url": reverse_lazy("plugins-api:netbox_storage-api:filesystem-list")}
        ),
        help_text="The Filesystem of the Volume e.g. ext4",
    )

    class Meta:
        model = LinuxVolume

        fields = (
            "virtual_machine",
            "drive",
            "partition",
            "size",
            "fs",
            "path",
            "description",
        )


class LinuxVolumeFilterForm(NetBoxModelFilterSetForm):
    """Form for filtering LinuxVolume instances."""

    model = LinuxVolume

    virtual_machine = DynamicModelChoiceField(
        queryset=VirtualMachine.objects.all(),
    )
    drive = DynamicModelChoiceField(
        queryset=Drive.objects.all(),
        query_params={
            'virtual_machine_id': '$virtual_machine',
        },
        help_text="The Storage Cluster of the drive",
    )
    partition = DynamicModelChoiceField(
        queryset=Partition.objects.all(),
        label="Partition",
        widget=APISelect(
            attrs={"data-url": reverse_lazy("plugins-api:netbox_storage-api:partition-list")}
        ),
        query_params={
            'drive_id': '$drive',
        },
        help_text="The Partition for the LinuxVolume e.g. /dev/sda1",
    )
    size = FloatField(
        label="Size (GB)",
        help_text="The size of the logical volume e.g. 25",
        validators=[MinValueValidator(0.0)],
    )
    path = CharField(
        label="Path",
        help_text="The mounted path of the volume e.g. /var/lib/docker",
    )
    fs = DynamicModelChoiceField(
        queryset=Filesystem.objects.all(),
        label="Filesystem Name",
        widget=APISelect(
            attrs={"data-url": reverse_lazy("plugins-api:netbox_storage-api:filesystem-list")}
        ),
        help_text="The Filesystem of the Volume e.g. ext4",
    )


class LinuxVolumeImportForm(NetBoxModelImportForm):
    fs = DynamicModelChoiceField(
        queryset=Filesystem.objects.all(),
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = LinuxVolume

        fields = (
            "fs",
            "path",
            "description",
        )


class LinuxVolumeBulkEditForm(NetBoxModelBulkEditForm):
    model = LinuxVolume

    path = CharField(
        required=False,
        label="Path",
    )
    fs = DynamicModelChoiceField(
        queryset=Filesystem.objects.all(),
        required=False,
        label="Filesystem Name",
    )
    description = CharField(max_length=255, required=False)

    fieldsets = (
        (
            None,
            ("path", "fs", "description"),
        ),
    )
    nullable_fields = ["description"]
