import django_tables2 as tables

from netbox.tables import (
    NetBoxTable,
    ToggleColumn,
    ActionsColumn,
)

from netbox_storage.models import LogicalVolume


class LogicalVolumeBaseTable(NetBoxTable):
    """Base class for tables displaying LogicalVolume"""

    fs = tables.Column(
        linkify=True,
        verbose_name="Filesystem"
    )
    vg = tables.Column(
        linkify=True,
        verbose_name="Volume Group Name"
    )
    lv_name = tables.Column(
        linkify=True,
        verbose_name="Logical Volume Name"
    )


class LogicalVolumeTable(LogicalVolumeBaseTable):
    """Table for displaying LogicalVolume objects."""

    pk = ToggleColumn()

    class Meta(NetBoxTable.Meta):
        model = LogicalVolume
        fields = (
            "pk",
            "vg",
            "lv_name",
            "path",
            "fs",
            "description",
        )
        default_columns = (
            "vg",
            "lv_name",
            "path",
            "fs",
            "description"
        )


class RelatedLogicalVolumeTable(LogicalVolumeBaseTable):
    actions = ActionsColumn(actions=())

    class Meta(NetBoxTable.Meta):
        model = LogicalVolume
        fields = (
            "pk",
            "vg",
            "lv_name",
            "path",
            "fs",
            "description",
        )
        default_columns = (
            "fs",
            "description"
        )
