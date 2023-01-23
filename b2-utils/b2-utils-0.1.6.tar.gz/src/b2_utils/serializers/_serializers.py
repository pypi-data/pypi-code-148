from rest_framework import fields, serializers

from b2_utils.models import Address, City, Phone

__all__ = [
    "PrimaryKeyRelatedFieldWithSerializer",
    "UpdatableFieldsSerializer",
    "CitySerializer",
    "PhoneSerializer",
    "AddressSerializer",
]


class PrimaryKeyRelatedFieldWithSerializer(serializers.PrimaryKeyRelatedField):
    def __init__(self, representation_serializer, write_protected=False, **kwargs):
        self.representation_serializer = representation_serializer
        self.write_protected = write_protected
        super().__init__(**kwargs)

    def to_representation(self, value):
        if callable(value):
            return self.representation_serializer(value.all(), many=True).data

        instance = self.queryset.get(pk=value.pk)

        return self.representation_serializer(instance).data

    def validate_empty_values(self, data):
        if self.write_protected:
            raise fields.SkipField

        return super().validate_empty_values(data)


class UpdatableFieldsSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        meta = getattr(self, "Meta", None)
        updatable_fields = getattr(meta, "updatable_fields", {})
        non_updatable_fields = getattr(meta, "non_updatable_fields", {})

        assert not (updatable_fields and non_updatable_fields), (
            "Cannot set both 'updatable_fields' and 'non_updatable_fields' options on "
            f"serializer {self.__class__.__name__}."
        )

        method = getattr(kwargs.get("context", {}).get("request", {}), "method", None)
        data = kwargs.get("data", {})

        if method in {"PATCH", "PUT"}:
            if updatable_fields:
                kwargs["data"] = {
                    key: value for key, value in data.items() if key in updatable_fields
                }
            if non_updatable_fields:
                kwargs["data"] = {
                    key: value
                    for key, value in data.items()
                    if key not in non_updatable_fields
                }

        super().__init__(*args, **kwargs)


class PhoneSerializer(serializers.ModelSerializer):
    """A Phone serializer"""

    class Meta:
        model = Phone
        fields = ["id", "country_code", "area_code", "number", "created", "modified"]


class CitySerializer(serializers.ModelSerializer):
    """A City serializer"""

    class Meta:
        model = City
        fields = [
            "id",
            "name",
            "state",
            "created",
            "modified",
        ]


class AddressSerializer(serializers.ModelSerializer):
    """An Address serializer"""

    city = PrimaryKeyRelatedFieldWithSerializer(
        CitySerializer, queryset=City.objects.all()
    )

    class Meta:
        model = Address
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
