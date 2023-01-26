from django.forms import (
    CharField,
)

from netbox.forms import (
    NetBoxModelBulkEditForm,
    NetBoxModelFilterSetForm,
    NetBoxModelImportForm,
    NetBoxModelForm,
)

from netbox_storage.models import VolumeGroup


class VolumeGroupForm(NetBoxModelForm):
    """Form for creating a new VolumeGroup object."""

    vg_name = CharField(
        label="VG Name",
        help_text="Volume Group Name e.g. docker",
    )

    class Meta:
        model = VolumeGroup

        fields = (
            "vg_name",
            "description",
        )


class VolumeGroupFilterForm(NetBoxModelFilterSetForm):
    """Form for filtering VolumeGroup instances."""

    model = VolumeGroup

    vg_name = CharField(
        required=False,
        label="VG Name",
    )


class VolumeGroupImportForm(NetBoxModelImportForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = VolumeGroup

        fields = (
            "vg_name",
            "description",
        )


class VolumeGroupBulkEditForm(NetBoxModelBulkEditForm):
    model = VolumeGroup

    vg_name = CharField(
        required=False,
        label="VG Name",
    )
    description = CharField(max_length=255, required=False)

    fieldsets = (
        (
            None,
            ("vg_name", "description"),
        ),
    )
    nullable_fields = ["description"]
