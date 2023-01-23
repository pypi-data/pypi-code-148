from django.urls import path
from .views import *


urlpatterns = [
    # Device Group
    path("device-group/", DeviceGroupListView.as_view(), name='devicegroup_list'),
    path("device-group/add/", DeviceGroupEditView.as_view(), name='devicegroup_add'),
    path("device-group/<int:pk>/", DeviceGroupView.as_view(), name='devicegroup'),
    path("device-group/<int:pk>/edit/", DeviceGroupEditView.as_view(), name='devicegroup_edit'),
    path("device-group/<int:pk>/delete/", DeviceGroupDeleteView.as_view(), name='devicegroup_delete'),
    path("device-group/<int:pk>/device/<int:pk2>/", DeviceView.as_view(), name="device"),
    path("device-group/<int:pk>/device/<int:pk2>/interface/<str:pk3>/vlan/<str:pk4>/", InterfaceVlanMacView.as_view(), name="interface_mac"),
    
    # Change Log
    path("change-log/", ChangeLogListView.as_view(), name="changelog_list"),
    path("change-log/<int:pk>/", ChangeLogView.as_view(), name="changelog"),
]