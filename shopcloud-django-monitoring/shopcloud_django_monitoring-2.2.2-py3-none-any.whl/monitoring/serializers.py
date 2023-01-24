from rest_framework import serializers

from . import models


class ActionEmptySerializer(serializers.Serializer):
    pass


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Source
        fields = '__all__'
        read_only_fields = (
            'id',
            'created_at',
            'updated_at',
        )


class MetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Metric
        fields = '__all__'
        read_only_fields = (
            'id',
            'created_at',
            'updated_at',
        )
