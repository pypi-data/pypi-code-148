import django_tables2 as tables

from netbox.tables import (
    NetBoxTable,
    ToggleColumn,
)

from netbox_storage.models import Drive


class DriveTable(NetBoxTable):
    """Table for displaying Drives objects."""

    pk = ToggleColumn()
    virtual_machine = tables.Column(
        linkify=True
    )
    identifier = tables.Column(
        linkify=True
    )
    size = tables.Column(
        linkify=True
    )
    cluster = tables.Column(
        linkify=True
    )

    class Meta(NetBoxTable.Meta):
        model = Drive
        fields = (
            "pk",
            "size",
            "cluster",
            "identifier",
            "virtual_machine",
            "description",
        )
        default_columns = (
            "virtual_machine",
            "identifier",
            "size",
            "cluster",
        )
