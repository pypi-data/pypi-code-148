import django_filters
from django.db.models import Q

from netbox.filtersets import BaseFilterSet
from dcim.models import Device

from .models import DeviceGroup, ChangeLog


class DeviceGroupFilterSet(BaseFilterSet):
    q = django_filters.CharFilter(
        method='search',
        label='Search',
    )
    class Meta:
        model = DeviceGroup
        fields = ['id', 'name']

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value)
        ).distinct()


class DeviceFilterSet(BaseFilterSet):
    q = django_filters.CharFilter(
        method='search',
        label='Search',
    )
    class Meta:
        model = Device
        fields = ['id', 'name']

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value)
        ).distinct()


class ChangeLogFilterSet(BaseFilterSet):
    q = django_filters.CharFilter(
        method='search',
        label='Search',
    )

    class Meta:
        model = ChangeLog
        fields = ['id', 'component']

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(component__icontains=value) |
            Q(user__username=value) |
            Q(device_group__name=value)
        ).distinct()
