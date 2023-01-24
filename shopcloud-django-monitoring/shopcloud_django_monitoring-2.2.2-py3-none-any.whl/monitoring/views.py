from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.authentication import (BasicAuthentication,
                                           SessionAuthentication)
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.response import Response
from shopcloud_django_instrumenting import tracing

from . import models, serializers


class SourceViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.SourceSerializer
    queryset = models.Source.objects.all()
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, DjangoModelPermissions)
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)


class MetricViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.MetricSerializer
    queryset = models.Metric.objects.all()
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, DjangoModelPermissions)
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = {}
    search_fields = ()

    def get_serializer_class(self):
        if self.action == "proceed":
            return serializers.ActionEmptySerializer
        if self.action == "cron":
            return serializers.ActionEmptySerializer
        return self.serializer_class

    @action(detail=False, methods=["post"], url_path="cron")
    def cron(self, request):
        tr = tracing.DjangoAPITracer(request)

        metric_ids = models.Metric.objects.filter(is_active=True).values_list('id', flat=True)

        with tr.start_span('proceed') as span:
            for pk in metric_ids:
                models.Metric.fire_event_proceed(models.Metric.__name__, pk)

        return Response({
            'trace': tr.close(),
            'results': metric_ids,
        }, status=status.HTTP_201_CREATED if tr.is_success else status.HTTP_422_UNPROCESSABLE_ENTITY)

    @action(detail=True, methods=["post"], url_path="proceed")
    def proceed(self, request, pk):
        tr = tracing.DjangoAPITracer(request)

        metric = models.Metric.objects.filter(pk=pk).first()
        if metric is None:
            return Response({
                'trace': tr.close(),
                'errors': {
                    'connector_id': 'not found',
                },
            }, status=status.HTTP_404_NOT_FOUND if tr.is_success else status.HTTP_422_UNPROCESSABLE_ENTITY)

        with tr.start_span('proceed') as span:
            metric.proceed(span)

        metric = models.Metric.objects.filter(pk=pk).first()

        return Response({
            'trace': tr.close(),
            'result': serializers.MetricSerializer(metric).data,
        }, status=status.HTTP_201_CREATED if tr.is_success else status.HTTP_422_UNPROCESSABLE_ENTITY)
