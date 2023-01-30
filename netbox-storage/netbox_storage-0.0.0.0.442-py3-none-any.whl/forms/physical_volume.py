from django.forms import (
    CharField,
)
from django.urls import reverse_lazy

from netbox.forms import (
    NetBoxModelBulkEditForm,
    NetBoxModelFilterSetForm,
    NetBoxModelImportForm,
    NetBoxModelForm,
)
from utilities.forms import (
    DynamicModelChoiceField, APISelect,
)

from netbox_storage.models import Partition, PhysicalVolume, VolumeGroup, Drive


class PhysicalVolumeForm(NetBoxModelForm):
    """Form for creating a new PhysicalVolume object."""
    drive = DynamicModelChoiceField(
        queryset=Drive.objects.all(),
        label="Drive",
        help_text="The Drive e.g. Hard Drive 1",
    )
    partition = DynamicModelChoiceField(
        queryset=Partition.objects.all(),
        label="Partition",
        query_params={
            'drive_id': '$drive'
        },
        help_text="The Partition of the Drive e.g. /dev/sdc1",
    )
    pv_name = CharField(
        label="Physical Volume Name",
        help_text="Name of the physical Volume e.g. Name of the Partition /dev/sdc1",
    )
    vg = DynamicModelChoiceField(
        queryset=VolumeGroup.objects.all(),
        label="VG Name",
        required=False,
        widget=APISelect(
            attrs={"data-url": reverse_lazy("plugins-api:netbox_storage-api:volumegroup-list")}
        ),
        help_text="The Volume Group for the LogicalVolume e.g. vg_docker",
    )
    description = CharField(
        required=False,
        label="Description",
        help_text="Short Description e.g. Partition 1 on SSD Cluster",
    )

    fieldsets = (
        (
            "Storage Configuration",
            (
                "drive",
                "partition",
            ),
        ),
        (
            "Physical Volume Configuration",
            (
                "pv_name",
                "vg",
                "description",
            ),
        ),
    )

    class Meta:
        model = PhysicalVolume

        fields = (
            "partition",
            "pv_name",
            "vg",
            "description",
        )


class PhysicalVolumeFilterForm(NetBoxModelFilterSetForm):
    """Form for filtering PhysicalVolume instances."""

    model = PhysicalVolume

    drive = DynamicModelChoiceField(
        required=False,
        queryset=Drive.objects.all(),
        label="Drive",
        widget=APISelect(
            attrs={"data-url": reverse_lazy("plugins-api:netbox_storage-api:drive-list")}
        ),
        help_text="The Drive e.g. Hard Drive 1",
    )
    partition = DynamicModelChoiceField(
        required=False,
        queryset=Partition.objects.all(),
        label="Partition",
        widget=APISelect(
            attrs={"data-url": reverse_lazy("plugins-api:netbox_storage-api:partition-list")}
        ),
        help_text="The Partition of the Drive e.g. Partition 1",
    )
    pv_name = CharField(
        required=False,
        label="Physical Volume Name",
        help_text="Name of the physical Volume e.g. Name of the Partition /dev/sdc1",
    )
    vg = DynamicModelChoiceField(
        required=False,
        queryset=VolumeGroup.objects.all(),
        label="VG Name",
        widget=APISelect(
            attrs={"data-url": reverse_lazy("plugins-api:netbox_storage-api:volumegroup-list")}
        ),
        help_text="The Volume Group for the LogicalVolume e.g. vg_docker",
    )
    description = CharField(
        required=False,
        label="Description",
        help_text="Short Description e.g. Partition 1 on SSD Cluster",
    )


class PhysicalVolumeImportForm(NetBoxModelImportForm):
    partition = DynamicModelChoiceField(
        queryset=Partition.objects.all(),
        label="Partition",
        widget=APISelect(
            attrs={"data-url": reverse_lazy("plugins-api:netbox_storage-api:partition-list")}
        ),
        help_text="The Partition of the Drive e.g. Partition 1",
    )
    pv_name = CharField(
        label="Physical Volume Name",
        help_text="Name of the physical Volume e.g. Name of the Partition /dev/sdc1",
    )
    vg = DynamicModelChoiceField(
        queryset=VolumeGroup.objects.all(),
        label="VG Name",
        widget=APISelect(
            attrs={"data-url": reverse_lazy("plugins-api:netbox_storage-api:volumegroup-list")}
        ),
        help_text="The Volume Group for the LogicalVolume e.g. vg_docker",
    )
    description = CharField(
        required=False,
        label="Description",
        help_text="Short Description e.g. Partition 1 on SSD Cluster",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = PhysicalVolume

        fields = (
            "partition",
            "pv_name",
            "vg",
            "description",
        )


class PhysicalVolumeBulkEditForm(NetBoxModelBulkEditForm):
    model = PhysicalVolume

    partition = DynamicModelChoiceField(
        queryset=Partition.objects.all(),
        label="Partition",
        widget=APISelect(
            attrs={"data-url": reverse_lazy("plugins-api:netbox_storage-api:partition-list")}
        ),
        help_text="The Partition of the Drive e.g. Partition 1",
    )
    pv_name = CharField(
        label="Physical Volume Name",
        help_text="Name of the physical Volume e.g. Name of the Partition /dev/sdc1",
    )
    vg = DynamicModelChoiceField(
        queryset=VolumeGroup.objects.all(),
        label="VG Name",
        widget=APISelect(
            attrs={"data-url": reverse_lazy("plugins-api:netbox_storage-api:volumegroup-list")}
        ),
        help_text="The Volume Group for the LogicalVolume e.g. vg_docker",
    )
    description = CharField(
        required=False,
        label="Description",
        help_text="Short Description e.g. Partition 1 on SSD Cluster",
    )

    fieldsets = (
        (
            None,
            ("partition", "pv_name", "vg", "description")
        ),
    )
    nullable_fields = ["description"]
