from rest_framework.viewsets import ViewSet
from rest_framework.permissions import AllowAny
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .serializers import (
    FeatureToggleSerializer,
)
from rest_framework.decorators import action
from rest_framework.response import Response
from waffle.models import Switch
from typing import List


class FeatureToggleView(ViewSet):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        method="get",
        manual_parameters=[],
        responses={200: openapi.Response("", FeatureToggleSerializer)},
    )
    @action(detail=False, methods=["get"])
    def get_all_toggles(self, request):
        toggles: List[Switch] = Switch.objects.all()
        response: FeatureToggleSerializer = FeatureToggleSerializer(toggles, many=True)
        return Response(response.data)
