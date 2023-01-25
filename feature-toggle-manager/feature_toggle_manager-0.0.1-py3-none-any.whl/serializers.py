from rest_framework import serializers
from waffle.models import Switch


class FeatureToggleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Switch
        fields = (
            "name",
            "active",
        )
