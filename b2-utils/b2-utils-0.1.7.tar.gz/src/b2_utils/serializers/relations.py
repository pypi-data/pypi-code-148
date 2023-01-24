from rest_framework import fields as _fields
from rest_framework import relations as _relations

__all__ = ["PrimaryKeyRelatedFieldWithSerializer"]


class PrimaryKeyRelatedFieldWithSerializer(_relations.PrimaryKeyRelatedField):
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
            raise _fields.SkipField

        return super().validate_empty_values(data)
