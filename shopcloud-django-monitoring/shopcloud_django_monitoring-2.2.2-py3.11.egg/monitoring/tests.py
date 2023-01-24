from inspect import getmembers, isfunction

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from shopcloud_django_instrumenting import tracing
from shopcloud_django_toolbox import TestAdminTestCase
from shopcloud_django_toolbox.tests import BaseTestApiAuthorization, SetupClass

from . import models, seeds


class TestAPIEndpointAuthorization(TestCase):
    def test_api_authorization(self):
        urls = [
            'sources',
            'metrics',
        ]
        client = APIClient()
        for x in urls:
            r = client.get(f'/monitoring/api/{x}/')
            self.assertIn(r.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_302_FOUND])


class TestApiAuthorization(BaseTestApiAuthorization):
    app_name = "monitoring"

    def test_model_sources(self):
        self.run_test_endpoint("sources")

    def test_model_metrics(self):
        self.run_test_endpoint("metrics")


class TestAdminPages(TestAdminTestCase):
    MODULE = 'monitoring'

    def test_admin_source(self):
        self.run_for_model('source')

    def test_admin_metric(self):
        self.run_for_model('metric', is_check_search=True)


class TestMetricAlarm(SetupClass):
    def test_cron(self):
        client = APIClient()
        client.login(username=self.username, password=self.pwd)

        seeds.generate_metric()
        seeds.generate_metric()

        response = client.post(
            '/monitoring/api/metrics/cron/',
            data={},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_metric_proceed(self):
        client = APIClient()
        client.login(username=self.username, password=self.pwd)

        metric = seeds.generate_metric()

        response = client.post(
            f'/monitoring/api/metrics/{metric.id}/proceed/',
            data={},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        metric = models.Metric.objects.get(pk=metric.id)
        self.assertEqual(metric.is_ok, True)

    def test_metric_proceed_not_found(self):
        client = APIClient()
        client.login(username=self.username, password=self.pwd)

        response = client.post(
            f'/monitoring/api/metrics/{100}/proceed/',
            data={},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_metric_min_value(self):
        client = APIClient()
        client.login(username=self.username, password=self.pwd)

        metric = seeds.generate_metric()

        metric.value_min = 10
        metric.save()
        self.assertEqual(metric.is_ok, True)

        response = client.post(
            f'/monitoring/api/metrics/{metric.id}/proceed/',
            data={},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        metric = models.Metric.objects.get(pk=metric.id)
        self.assertEqual(metric.is_ok, False)

    def test_metric_max_value(self):
        client = APIClient()
        client.login(username=self.username, password=self.pwd)

        metric = seeds.generate_metric()

        metric.value_max = 2
        metric.save()
        self.assertEqual(metric.is_ok, True)

        response = client.post(
            f'/monitoring/api/metrics/{metric.id}/proceed/',
            data={},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        metric = models.Metric.objects.get(pk=metric.id)
        self.assertEqual(metric.is_ok, False)

    def test_plugin_not_exists(self):
        client = APIClient()
        client.login(username=self.username, password=self.pwd)

        metric = seeds.generate_metric()
        metric.source.type = 'not_exists'

        is_fired = False
        try:
            metric.proceed(tracing.Tracer('service', 'operation'))
        except Exception:
            is_fired = True
        self.assertEqual(is_fired, True)

    def test_plugin_not_success(self):
        client = APIClient()
        client.login(username=self.username, password=self.pwd)

        metric = seeds.generate_metric()
        source = metric.source
        source.type = models.SourceType.NOT_SUCCESS_V1
        source.save()
        self.assertEqual(metric.is_ok, True)

        response = client.post(
            f'/monitoring/api/metrics/{metric.id}/proceed/',
            data={},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        metric = models.Metric.objects.get(pk=metric.id)
        self.assertEqual(metric.is_ok, False)

    def test_plugin_sql_query_v1_query_not_valid(self):
        client = APIClient()
        client.login(username=self.username, password=self.pwd)

        metric = seeds.generate_metric()
        metric.query = ""
        metric.save()
        source = metric.source
        source.type = models.SourceType.SQL_QUERY_V1
        source.save()

        response = client.post(
            f'/monitoring/api/metrics/{metric.id}/proceed/',
            data={},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        metric = models.Metric.objects.get(pk=metric.id)
        self.assertEqual(metric.is_ok, False)
        self.assertEqual(metric.value, None)

    def test_plugin_sql_query_v1(self):
        client = APIClient()
        client.login(username=self.username, password=self.pwd)

        metric = seeds.generate_metric()
        metric.query = "SELECT 111 AS total FROM auth_user LIMIT 1"
        metric.save()
        source = metric.source
        source.type = models.SourceType.SQL_QUERY_V1
        source.save()

        response = client.post(
            f'/monitoring/api/metrics/{metric.id}/proceed/',
            data={},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        metric = models.Metric.objects.get(pk=metric.id)
        self.assertEqual(metric.value, 111)


class RepresentationTest(TestCase):
    def test_representations(self):
        members = getmembers(seeds, isfunction)

        for _name, func in [x for x in members if "generate" in x[0]]:
            model = func()
            if model is not None:
                model.__repr__()
                model.__str__()
