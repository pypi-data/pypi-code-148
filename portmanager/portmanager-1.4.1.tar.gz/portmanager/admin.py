from django.contrib import admin
from .models import DeviceGroup, ChangeLog


@admin.register(DeviceGroup)
class PMDeviceGroupAdmin(admin.ModelAdmin):
    list_display = ("name", )


@admin.register(ChangeLog)
class PMChangeLogAdmin(admin.ModelAdmin):
    list_display = ("id", )
