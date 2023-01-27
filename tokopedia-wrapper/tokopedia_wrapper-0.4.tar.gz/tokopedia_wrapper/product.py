from .base import BaseWrapper
from .query import PDPGetLayout
from functools import cached_property
from urllib.parse import urlparse
import json

class Product(BaseWrapper):
    def __init__(self, link=None, shop_domain=None, product_key=None, **kwargs):
        super().__init__('pdpGetLayout')
        self.link = link
        self.shop_domain = shop_domain
        self.product_key = product_key
        self.kwargs = kwargs
        self.endpoint = 'https://gql.tokopedia.com/graphql/PDPGetLayoutQuery'

    def __get_shop_domain(self):
        if self.link and not self.shop_domain:
            parsed_link = urlparse(self.link)
            path = parsed_link.path.strip('/')
            self.shop_domain = path.split('/')[0]

        return self.shop_domain

    def __get_product_key(self):
        if self.link and not self.product_key:
            parsed_link = urlparse(self.link)
            path = parsed_link.path.strip('/')
            self.product_key = path.split('/')[1]

        return self.product_key

    def __get_product_info(self):
        payload = [
            {
                'operationName': 'PDPGetLayoutQuery',
                'query': PDPGetLayout,
                'variables': {
                    'apiVersion': 1,
                    'productKey': self.__get_product_key(),
                    'shopDomain': self.__get_shop_domain()
                }
            }
        ]

        self.connection.request(method='POST', url=self.endpoint, body=json.dumps(payload), headers=self.headers)

        with self.connection.getresponse() as response:
            data = self.to_json(response)
            self.status_code = response.getcode()
            self.error = data[0]['errors'] if 'errors' in data[0] else None
            self.data = data[0]['data']['pdpGetLayout']

        return self.data

    def __search_product_component(self, key, val):
        return next((filter(lambda x: x.get(key) == val, self.data['components'])), {})

    @cached_property
    def product_media_component(self):
        return next((filter(lambda x: x.get('name') == 'product_media', self.data['components'])), {})

    @cached_property
    def product_content_component(self):
        return next((filter(lambda x: x.get('name') == 'product_content', self.data['components'])), {})

    @cached_property
    def product_detail_component(self):
        return next((filter(lambda x: x.get('name') == 'product_detail', self.data['components'])), {})    

    def __search_product_detail_content(self, title):
        return next((filter(lambda x: x.get('title') == title, self.product_detail_component['data'][0]['content'])), {})

    @cached_property
    def serialize(self):
        self.__get_product_info()
        if not self.data or self.error:
            return None

        return {
            'meta': {
                'pdp_session': self.data['pdpSession'],
                'request_id': self.data['requestID'],
                'product_url': self.data['basicInfo']['url']
            },
            'product': {
                'id': self.data['basicInfo']['id'],
                'name': self.product_content_component['data'][0]['name'],
                'alias': self.data['basicInfo']['alias'],
                'description': self.__search_product_detail_content('Deskripsi')['subtitle'] if self.__search_product_detail_content('Deskripsi') else None,
                'condition': self.__search_product_detail_content('Kondisi')['subtitle'] if self.__search_product_detail_content('Kondisi') else None,
                'weight': self.__search_product_detail_content('Berat Satuan')['subtitle'] if self.__search_product_detail_content('Berat Satuan') else None,
                'category': self.__search_product_detail_content('Kategori')['subtitle'] if self.__search_product_detail_content('Kategori') else None,
                'images': [image['urlOriginal'] for image in self.product_media_component['data'][0]['media'] if image['type'] == 'image'],
                'price': self.product_content_component['data'][0]['price']['value'],
                'stock': self.product_content_component['data'][0]['stock']['value'],
            },
            'shop': {
                'id': self.data['basicInfo']['shopID'],
                'name': self.data['basicInfo']['shopName'],
            }
        }
        return self.data