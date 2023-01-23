import django_tables2 as tables

from dcim.models import Device
from netbox.tables import NetBoxTable, columns

from .template_code import *
from .models import DeviceGroup, ChangeLog


class InterfaceTable(tables.Table):
    if_name = tables.Column(
        order_by=("name",),
        verbose_name="Name"
    )
    if_description = tables.TemplateColumn(
        IF_TABLE_DESC, 
        verbose_name="Description"
    )
    if_state = tables.TemplateColumn(
        IF_TABLE_STATE, 
        verbose_name="State"
    )
    if_admin_status = tables.TemplateColumn(
        IF_TABLE_ADMIN_STATUS, 
        verbose_name="Admin Status"
    )
    if_ps_max = tables.TemplateColumn(
        IF_TABLE_PS_MAX, 
        verbose_name="MAX Port Security"
    )
    if_poe = tables.Column(
        verbose_name="POE (W)"
    )
    if_vlan = tables.TemplateColumn(
        IF_TABLE_VLAN, 
        verbose_name="VLAN"
    )
    if_index = tables.TemplateColumn(
        IF_TABLE_SNMP_INDEX, 
        verbose_name=""
    )
    if_macs = tables.TemplateColumn(
        IF_TABLE_SHOW_MACS,
        verbose_name="Show MACs"
    )

    class Meta:
        attrs = {
            'class': 'table table-hover object-list',
        }
        row_attrs = {
            "style": lambda record: "" if record.get("if_enabled") else "opacity: 0.65;",
            "title": lambda record: "" if record.get("if_enabled") else record.get("if_comment"),
        }

        fields = (
            "if_name", "if_vlan", "if_description", "if_ps_max", "if_admin_status", "if_state", "if_poe", "if_index", "if_macs", 
        )
        default_columns = (
            "if_name", "if_vlan", "if_description", "if_ps_max", "if_admin_status", "if_poe", "if_state", "if_macs",  
        )
        orderable = False
        empty_text = "Cannot receive response from the device. Please contact the administrator."


class DeviceGroupTable(NetBoxTable):
    name = tables.TemplateColumn(
        order_by=('name',),
        template_code=DEVICE_GROUP_LINK
    )

    description = tables.Column()

    actions = columns.ActionsColumn(
        actions=("edit", "delete")
    )

    class Meta(NetBoxTable.Meta):
        model = DeviceGroup
        fields = (
            'id', 'name', 'description', "vlans", "portsec_max"
        )
        default_columns = (
            'name', 'description', "vlans", "portsec_max"
        )


class ChangeLogTable(NetBoxTable):
    date = tables.DateTimeColumn()
    user = tables.TemplateColumn(
        template_code=USERNAME
    )
    device = tables.Column()
    device_group = tables.Column()
    interface = tables.Column()
    component = tables.Column()
    before = tables.Column()
    after = tables.Column()
    actions = columns.ActionsColumn(
        actions=()
    )

    class Meta(NetBoxTable.Meta):
        model = ChangeLog
        fields = (
            'id', 'date', 'user', "device_group", "device", "interface", "component", "before", "after", "actions"
        )
        default_columns = (
            'id', 'date', 'user', "device_group", "device", "interface", "component", "before", "after", "actions"
        )


class DeviceTable(NetBoxTable):
    actions = None
    name = tables.TemplateColumn(
        order_by=('name',),
        template_code=DEVICE_LINK
    )

    class Meta(NetBoxTable.Meta):
        model = Device
        fields = (
            'pk', 'id', 'name'
        )
        default_columns = (
            'pk', 'name'
        )