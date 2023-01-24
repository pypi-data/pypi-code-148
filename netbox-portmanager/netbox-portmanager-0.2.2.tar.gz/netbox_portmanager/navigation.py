from extras.plugins import PluginMenuButton, PluginMenuItem
from utilities.choices import ButtonColorChoices
from extras.plugins import PluginMenu


item1 = PluginMenuItem(
    link="plugins:netbox-portmanager:devicegroup_list",
    link_text="Device Groups",
    permissions=["netbox-portmanager.view_devicegroup"],
    buttons=(
        PluginMenuButton(
            link="plugins:netbox-portmanager:devicegroup_add",
            title="Add",
            icon_class="mdi mdi-plus-thick",
            color=ButtonColorChoices.GREEN,
            permissions=["netbox-portmanager.add_devicegroup"]
        ),
    )
)


item2 = PluginMenuItem(
    link="plugins:netbox-portmanager:changelog_list",
    link_text="Change Log",
    permissions=["netbox-portmanager.view_changelog"]
)


menu = PluginMenu(
    label='Portmanager',
    groups=(
        ('Portmanager', (item1, item2)),
    ),
    icon_class='mdi mdi-web'
)