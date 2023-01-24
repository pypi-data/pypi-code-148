from typing import Optional, Tuple

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from shopcloud_django_toolbox import GID, Event
from shopcloud_streams import Event as StreamEvent


class SourceType:
    SQL_QUERY_V1 = 'SQL_QUERY_V1'
    NOT_SUCCESS_V1 = 'NOT_SUCCESS_V1'
    SQL_SAGE_GATEWAY_V1 = 'SQL_SAGE_GATEWAY_V1'


class Source(GID, models.Model):
    name = models.CharField(
        max_length=255,
    )
    code = models.CharField(
        max_length=255,
        unique=True,
    )
    type = models.CharField(
        max_length=255,
        choices=(
            (SourceType.SQL_QUERY_V1, SourceType.SQL_QUERY_V1),
            (SourceType.NOT_SUCCESS_V1, SourceType.NOT_SUCCESS_V1),
            (SourceType.SQL_SAGE_GATEWAY_V1, SourceType.SQL_SAGE_GATEWAY_V1),
        )
    )
    meta_api_endpoint = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    meta_api_username = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    meta_api_password = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    meta_connector = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    meta_db = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return f"{self.code}"

    def __str__(self):
        return f"{self.code}"

    def proceed(self, span, metric: 'Metric') -> Tuple[bool, Optional[int]]:
        from monitoring.plugins.sources import PLUGINS
        erp_code = self.type.upper()
        if erp_code not in PLUGINS:
            raise Exception('Plugin not exists')
        try:
            return PLUGINS[erp_code].proceed(span, metric)
        except Exception:
            return False, None


class MetricType:
    TECHNICAL = 'TECHNICAL'
    PROCESS = 'PROCESS'


class Metric(GID, models.Model):
    name = models.CharField(
        max_length=255,
    )
    code = models.CharField(
        max_length=255,
        unique=True,
    )
    source = models.ForeignKey(
        Source,
        on_delete=models.CASCADE,
        related_name='metrics',
    )
    last_run_at = models.DateTimeField(
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(
        default=True,
    )
    is_ok = models.BooleanField(
        default=True,
    )
    query = models.TextField()
    description = models.TextField(
        blank=True
    )
    value = models.IntegerField(
        null=True,
        blank=True,
    )
    value_min = models.IntegerField(
        null=True,
        blank=True,
    )
    value_max = models.IntegerField(
        null=True,
        blank=True,
    )
    contact_person = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    type = models.CharField(
        max_length=255,
        choices=(
            (MetricType.TECHNICAL, MetricType.TECHNICAL),
            (MetricType.PROCESS, MetricType.PROCESS),
        ),
        default=MetricType.TECHNICAL,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return f"{self.code}"

    def __str__(self):
        return f"{self.code}"

    def fire_alarm(self, span):
        if not self.is_active:
            return None

        app_title = settings.APP_TITLE

        if app_title is None:
            app_title = "APP"

        app_title = f"{app_title}-Monitoring"

        base_url = settings.BASE_URL

        if base_url.endswith("/"):
            base_url = base_url[:-1]

        action_url = base_url + reverse("admin:monitoring_metric_changelist")

        StreamEvent('de.talk-point.streams/notification_fired', {
            'notification': {
                "type": "MS_MONITORING_METRIC_ALARM",
                "title": f"{app_title}: Alarm for metric {self.code}",
                "reference": f"ms-monitoring-alarm-created-{self.id}-{timezone.now().strftime('%Y-%m-%d')}",
                "sections": [
                    {
                        "topLabel": "Name",
                        "content": self.code,
                    },
                    {
                        "topLabel": "Value",
                        "content": self.value,
                    },
                    {
                        "topLabel": "Description",
                        "content": self.description if self.description is not None else "",
                    },
                    {
                        "topLabel": "type",
                        "content": self.type,
                    },
                    {
                        "topLabel": "Kontaktperson",
                        "content": self.contact_person,
                    },
                    {
                        "topLabel": "Aktion",
                        "content": "Bitte überprüfen ob der Alarm problematisch ist",
                        "link": f"{action_url}?q={self.id}",
                        "link_title": "Zur Metrik",
                    },
                ]
            }
        }).fire()

    @staticmethod
    def fire_event_proceed(model: str, pk: int):
        event = Event(
            name="de.talk-point.marketplace-suppliers/monitoring/metrics/proceed",
            model=model,
        )
        event.add_task(
            queue="monitoring-metrics-proceed",
            url=f"monitoring/api/metrics/{pk}/proceed/",
            json={}
        )
        event.fire()

    def proceed(self, span) -> bool:
        is_success, value = self.source.proceed(span, self)

        before_is_ok = self.is_ok
        self.is_ok = True
        self.value = value
        self.last_run_at = timezone.now()

        if not is_success:
            self.is_ok = False
        else:
            if value is None:
                self.is_ok = False
            else:
                if self.value_min is not None and self.value <= self.value_min:
                    self.is_ok = False

                if self.value_max is not None and self.value >= self.value_max:
                    self.is_ok = False
        self.save()

        if before_is_ok != self.is_ok:
            if not self.is_ok:
                self.fire_alarm(span)

        return self.is_ok
