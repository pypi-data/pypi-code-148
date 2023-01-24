from typing import Optional, Tuple

import requests
from django.conf import settings
from shopcloud_django_instrumenting import tracing

from monitoring import models


class Plugin:
    NAME = "SQL_SAGE_GATEWAY_V1"

    def proceed(self, span: tracing.Span, metric: models.Metric, **kwargs) -> Tuple[bool, Optional[int]]:
        if settings.TEST_MODE:
            return True, 5

        with span.start_span('fetch') as sub_span:
            connector = "sage" if metric.source.meta_connector is None else metric.source.meta_connector
            data = {
                'query': metric.query,
            }
            if metric.source.meta_db is not None:
                data['db'] = metric.source.meta_db
            url = f'https://{metric.source.meta_api_endpoint}/databases/{connector}/query'
            sub_span.set_tag('url', url)
            sub_span.set_tag('method', 'POST')
            sub_span.set_tag('connector', connector)
            sub_span.set_tag('db', data.get('db', ''))
            response = requests.post(
                url,
                headers={
                    'X-API-KEY': metric.source.meta_api_password,
                    'UserAgent': 'markeptlace-suppliers',
                },
                json=data
            )
            sub_span.set_tag('status_code', str(response.status_code))
            if not (200 <= response.status_code <= 299):
                if response.status_code == 404:
                    return False, 0
                sub_span.log_kv(response.json())
                return False, 0
            datas = response.json().get('results', [])
            if len(datas) == 0:
                raise Exception('No data returned')
            return True, int(datas[0].get('total', 0))
