from django.db.models import Q

from netbox.filtersets import NetBoxModelFilterSet

from netbox_storage.models import PhysicalVolume


class PhysicalVolumeFilter(NetBoxModelFilterSet):
    """Filter capabilities for PhysicalVolume instances."""

    class Meta:
        model = PhysicalVolume
        fields = ["pv_name"]

    def search(self, queryset, name, value):
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = (
            Q(pv_name__icontains=value)
        )
        return queryset.filter(qs_filter)
