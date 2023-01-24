from rest_framework import serializers as _serializers

from b2_utils import models as _models
from b2_utils.serializers.relations import PrimaryKeyRelatedFieldWithSerializer

__all__ = [
    "PrimaryKeyRelatedFieldWithSerializer",
    "PhoneSerializer",
    "CitySerializer",
    "AddressSerializer",
]


class PhoneSerializer(_serializers.ModelSerializer):
    """A Phone serializer"""

    class Meta:
        model = _models.Phone
        fields = ["id", "country_code", "area_code", "number", "created", "modified"]


class CitySerializer(_serializers.ModelSerializer):
    """A City serializer"""

    class Meta:
        model = _models.City
        fields = [
            "id",
            "name",
            "state",
            "created",
            "modified",
        ]


class AddressSerializer(_serializers.ModelSerializer):
    """An Address serializer"""

    city = PrimaryKeyRelatedFieldWithSerializer(
        CitySerializer, queryset=_models.City.objects.all()
    )

    class Meta:
        model = _models.Address
        fields = [
            "id",
            "city",
            "street",
            "number",
            "additional_info",
            "district",
            "zip_code",
            "created",
            "modified",
        ]
