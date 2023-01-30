import django_tables2 as tables

from netbox.tables import (
    NetBoxTable,
    ToggleColumn,
    ActionsColumn,
)

from netbox_storage.models import VolumeGroup


class VolumeGroupBaseTable(NetBoxTable):
    """Base class for tables displaying VolumeGroup"""

    vg_name = tables.Column(
        linkify=True,
        verbose_name="Volume Group Name"
    )


class VolumeGroupTable(VolumeGroupBaseTable):
    """Table for displaying VolumeGroup objects."""

    pk = ToggleColumn()

    class Meta(NetBoxTable.Meta):
        model = VolumeGroup
        fields = (
            "pk",
            "vg_name",
            "description",
        )
        default_columns = (
            "vg_name",
            "description"
        )


class RelatedVolumeGroupTable(VolumeGroupBaseTable):
    actions = ActionsColumn(actions=())

    class Meta(NetBoxTable.Meta):
        model = VolumeGroup
        fields = (
            "pk",
            "vg_name",
            "description",
        )
        default_columns = (
            "description"
        )
