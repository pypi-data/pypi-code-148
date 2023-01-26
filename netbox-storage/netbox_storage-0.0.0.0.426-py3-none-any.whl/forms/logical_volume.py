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

from netbox_storage.models import Filesystem, LogicalVolume, VolumeGroup, Drive
from virtualization.models import VirtualMachine


class LogicalVolumeForm(NetBoxModelForm):
    """Form for creating a new LogicalVolume object."""
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
    vg = DynamicModelChoiceField(
        queryset=VolumeGroup.objects.all(),
        label="VG Name",
        widget=APISelect(
            attrs={"data-url": reverse_lazy("plugins-api:netbox_storage-api:volumegroup-list")}
        ),
        help_text="The Volume Group for the LogicalVolume e.g. vg_docker",
    )
    lv_name = CharField(
        label="LV Name",
        help_text="Logical Volume Name e.g. lv_docker",
    )
    size = FloatField(
        label="Size (GB)",
        help_text="The size of the logical volume e.g. 25",
        validators=[MinValueValidator(1)],
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
        model = LogicalVolume

        fields = (
            "virtual_machine",
            "drive",
            "vg",
            "lv_name",
            "size",
            "fs",
            "path",
            "description",
        )


class LogicalVolumeFilterForm(NetBoxModelFilterSetForm):
    """Form for filtering LogicalVolume instances."""

    model = LogicalVolume

    vg = DynamicModelChoiceField(
        queryset=VolumeGroup.objects.all(),
        label="VG Name",
        required=False
    )
    lv_name = CharField(
        required=False,
        label="LV Name",
    )
    path = CharField(
        required=False,
        label="Path",
    )
    fs = DynamicModelChoiceField(
        queryset=Filesystem.objects.all(),
        required=False,
        widget=APISelect(
            attrs={"data-url": reverse_lazy("plugins-api:netbox_storage-api:filesystem-list")}
        ),
        label="Filesystem Name",
    )


class LogicalVolumeImportForm(NetBoxModelImportForm):
    fs = DynamicModelChoiceField(
        queryset=Filesystem.objects.all(),
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = LogicalVolume

        fields = (
            "vg",
            "lv_name",
            "fs",
            "path",
            "description",
        )


class LogicalVolumeBulkEditForm(NetBoxModelBulkEditForm):
    model = LogicalVolume

    vg = DynamicModelChoiceField(
        queryset=VolumeGroup.objects.all(),
        required=False
    )
    lv_name = CharField(
        required=False,
        label="LV Name",
    )
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
            ("vg", "lv_name", "path", "fs", "description"),
        ),
    )
    nullable_fields = ["description"]
