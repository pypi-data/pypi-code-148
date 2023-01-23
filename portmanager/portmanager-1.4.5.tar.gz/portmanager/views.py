from django.views.generic import View
from django.shortcuts import redirect, render
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import HttpResponseBadRequest

from dcim.models import Device
from netbox.views import generic
from utilities.views import register_model_view
from utilities.permissions import get_permission_for_model, resolve_permission

from .models import DeviceGroup, ChangeLog
from .filtersets import DeviceGroupFilterSet, ChangeLogFilterSet
from .forms import DeviceGroupForm, DeviceGroupFilterForm, ChangeLogFilterForm
from .tables import DeviceGroupTable, DeviceTable, InterfaceTable, ChangeLogTable
from .switches.cisco_switch import CiscoSwitch
from .switches.general_switch import GeneralSwitch
from .utils import get_object_or_none


class InterfaceVlanMacView(View):
    queryset = Device.objects.all()
    queryset_device_group = DeviceGroup.objects.all()
    template = "portmanager/mac.html"

    def get(self, request, pk, pk2, pk3, pk4):
        device_object = get_object_or_404(self.queryset, pk=pk2)
        if device_object is None:
            self.handle_no_permission()
        device_group_object = get_object_or_404(self.queryset_device_group, pk=pk, devices=device_object)
        if device_group_object is None:
            self.handle_no_permission()

        cs = CiscoSwitch(
            fqdn=device_object.name, 
            community_string=device_group_object.community_string, 
        )

        macs, interface_name = cs.load_vlan_interface_macs(if_index=str(pk3), vlan_id=str(pk4))
        return render(request, self.template, {
            "macs": macs,
            "object": device_object,
            "interface": interface_name,
            "vlan": pk4,
        })


class DeviceView(generic.ObjectView):
    queryset = Device.objects.all()
    queryset_device_group = DeviceGroup.objects.all()
    template_name = "portmanager/device.html"

    def get_required_permission(self):
        return get_permission_for_model(DeviceGroup, 'view')

    def has_permission(self):
        user = self.request.user
        self.deploy_perms = False
        self.admin = False

        for perm_name in ["view", "pm-admin", "pm-user"]:
            perm = get_permission_for_model(DeviceGroup, perm_name)
            if user.has_perms((perm, )):
                action = resolve_permission(perm)[1]
                self.queryset_device_group = self.queryset_device_group.all().restrict(user, action)
                self.queryset = self.queryset.filter(device_groups__in=self.queryset_device_group).distinct()
                if perm_name == "pm-admin":
                    self.admin = True
                if perm_name != "view":
                    self.deploy_perms = True
            elif perm_name == "view":
                return False
        return True

    def get(self, request, pk, pk2, **kwargs):
        device_object = get_object_or_none(self.queryset, pk=pk2)
        if device_object is None:
            self.handle_no_permission()
        device_group_object = get_object_or_none(self.queryset_device_group, pk=pk, devices=device_object)
        if device_group_object is None:
            self.handle_no_permission()

        interval_string = device_group_object.vlans
        if self.admin or request.user.is_superuser:
            interval_string = "[1-1000]"

        switch = CiscoSwitch(
            fqdn=device_object.name, 
            community_string=device_group_object.community_string, 
            interval_string=interval_string,
            portsec_max=device_group_object.portsec_max
        )
        switch.load_interfaces_real()
        switch.load_vlans_real()

        table = self.setup_table(switch, device_group_object, device_object)
        return render(request, self.get_template_name(), {
            'object': device_object,
            'devicegroup': device_group_object,
            "table": table,
            "deploy_perms": self.deploy_perms
        })

    def post(self, request, pk, pk2, **kwargs):
        device_object = get_object_or_none(self.queryset, pk=pk2)
        if device_object is None:
            self.handle_no_permission()
        device_group_object = get_object_or_none(self.queryset_device_group, pk=pk, devices=device_object)
        if device_group_object is None:
            self.handle_no_permission()

        interval_string = device_group_object.vlans
        if self.admin or request.user.is_superuser:
            interval_string = "[1-1000]"

        switch = CiscoSwitch(
            fqdn=device_object.name, 
            community_string=device_group_object.community_string, 
            interval_string=interval_string,
            portsec_max=device_group_object.portsec_max
        )
        switch.load_interfaces_real()
        switch.load_vlans_real()

        if "_reload" in request.POST:
            table = self.setup_table(switch, device_group_object, device_object)
            messages.info(request, "Device has been reloaded.")
            return render(request, self.get_template_name(), {
                'object': device_object,
                'devicegroup': device_group_object,
                'table': table,
                "deploy_perms": self.deploy_perms
            })
        
        # Cannot find _deploy in rquest.POST
        if not "_deploy" in request.POST:
            return HttpResponseBadRequest("Cannot find required POST DATA.")
        
        # Raise permission error if not entitled to _deploy
        if not self.deploy_perms:
            self.handle_no_permission()

        post_data = request.POST
        data = {
            "if_index": post_data.getlist("if_index"),
            "if_vlan": post_data.getlist("if_vlan"),
            "if_description": post_data.getlist("if_description"),
            "if_admin_status": post_data.getlist("if_admin_status"),
            "if_ps_max": post_data.getlist("if_ps_max"),
        }
        try:
            success_changes, errors = switch.load_interfaces_changes(data)
        except RuntimeError:
            messages.warning(request, "[ERROR] Please try again or contact administrator.")
            return redirect("plugins:portmanager:device", pk=pk, pk2=pk2)

        for success_change in success_changes:
            ChangeLog(
                user=request.user, 
                device=device_object,
                device_group=device_group_object,
                interface=success_change.get("interface"),
                component=success_change.get("component"), 
                before=success_change.get("before"), 
                after=success_change.get("after")
            ).save()

        if len(success_changes) == 0:
            messages.info(request, "Nothing has changed")
        else:
            messages.success(request, f"Changes: {success_changes}") 
        if len(errors) != 0:
            messages.warning(request, f"Errors: {errors}")

        table = self.setup_table(switch, device_group_object, device_object)
        return render(request, self.get_template_name(), {
            'object': device_object,
            'devicegroup': device_group_object,
            'table': table,
            "deploy_perms": self.deploy_perms
        })

    def setup_table(
        self, 
        switch: GeneralSwitch,
        device_group: DeviceGroup,
        device: Device
    ) -> InterfaceTable:
        interfaces = switch.get_interfaces()
        table = InterfaceTable(interfaces)
        table.vlans = switch.get_vlans()
        table.portsec_max = device_group.portsec_max
        table.device = device
        table.device_group = device_group
        return table


## Device Group

class DeviceGroupListView(generic.ObjectListView):
    queryset = DeviceGroup.objects.all()
    filterset = DeviceGroupFilterSet
    filterset_form = DeviceGroupFilterForm
    table = DeviceGroupTable
    template_name = 'generic/object_list.html'
    actions = ("add", "edit", )


@register_model_view(DeviceGroup)
class DeviceGroupView(generic.ObjectView):
    queryset = DeviceGroup.objects.all()
    template_name = 'portmanager/devicegroup.html'

    def get_extra_context(self, request, instance):
        """
        Return any additional context data to include when rendering the template.
        Args:
            request: The current request
            instance: The object being viewed
        """
        table = DeviceTable(instance.devices.all())
        table.device_group_pk = instance.pk
        return {"table": table}


@register_model_view(DeviceGroup, 'edit')
class DeviceGroupEditView(generic.ObjectEditView):
    queryset = DeviceGroup.objects.all()
    form = DeviceGroupForm
    template_name = 'generic/object_edit.html'


@register_model_view(DeviceGroup, 'delete')
class DeviceGroupDeleteView(generic.ObjectDeleteView):
    queryset = DeviceGroup.objects.all()
    template_name = 'generic/object_delete.html'


## Changelog

class ChangeLogListView(generic.ObjectListView):
    queryset = ChangeLog.objects.all()
    template_name = 'generic/object_list.html'
    table = ChangeLogTable
    actions = ('export',)
    filterset_form = ChangeLogFilterForm
    filterset = ChangeLogFilterSet


@register_model_view(ChangeLog)
class ChangeLogView(generic.ObjectView):
    queryset = ChangeLog.objects.all()
    template_name = "portmanager/changelog/changelog.html"
