import django_tables2 as tables

from netbox.tables import (
    NetBoxTable,
    ToggleColumn,
    ActionsColumn,
)

from netbox_storage.models import Partition


class PartitionBaseTable(NetBoxTable):
    """Base class for tables displaying Partition"""

    drive = tables.Column(
        linkify=True
    )
    device = tables.Column(
        linkify=True
    )
    size = tables.Column(
        linkify=True
    )
    type = tables.Column(
        linkify=True
    )


class PartitionTable(PartitionBaseTable):
    """Table for displaying Partition objects."""

    pk = ToggleColumn()

    class Meta(NetBoxTable.Meta):
        model = Partition
        fields = (
            "pk",
            "drive",
            "device",
            "size",
            "description",
        )
        default_columns = (
            "device",
            "size",
            "type"
        )


class RelatedPartitionTable(PartitionBaseTable):
    actions = ActionsColumn(actions=())

    class Meta(NetBoxTable.Meta):
        model = Partition
        fields = (
            "drive",
            "device",
            "size",
        )
        default_columns = (
            "drive",
            "device",
            "size",
        )
