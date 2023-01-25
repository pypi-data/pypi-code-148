import requests
from pandas import DataFrame
import settings


def get_table(SQL_command, params=()):
    data = settings.config['DB']['body']
    data['queryString'] = SQL_command % params
    response = requests.post(url=settings.config['DB']['url'], data=data)
    assert response.json()['success']
    df = DataFrame(response.json()['data'])
    return df
