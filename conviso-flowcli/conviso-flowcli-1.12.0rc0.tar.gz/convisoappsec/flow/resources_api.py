from urllib.parse import urlparse

from convisoappsec.flow.graphql_api import mutations, queries


class ConvisoGraphQLInterface:
    """ Communication base with Conviso Platform resources using its GraphQL API Client."""

    def __init__(self, conviso_api_client):
        self.__conviso_graphql_client = conviso_api_client
        self.url = conviso_api_client.url

    def query(self, query, variables={}):
        return self.__conviso_graphql_client.query(
            query, variables
        )

    @property
    def assets(self):
        return AssetsAPI(self)


class AssetsAPI(object):
    """ To operations on Asset's resources in Conviso Platform. """

    def __init__(self, conviso_client_interface):
        self.__conviso_client_interface = conviso_client_interface

    def create_asset(self, asset_model):
        graphql_variables = {
            'companyId': asset_model.company_id,
            'name': asset_model.name,
            'scanType': asset_model.scan_type,
        }

        graphql_collection = self.__conviso_client_interface.query(
            mutations.create_asset,
            graphql_variables
        )

        first_key = list(graphql_collection.keys())[0]
        assets_collection = graphql_collection.get(first_key).get('asset')

        return assets_collection

    def get_by_company_id(self, comapany_id, page=1, limit=32):
        graphql_variables = {
            "id": comapany_id,
            "page": page,
            "limit": limit
        }

        graphql_collection = self.__conviso_client_interface.query(
            queries.get_assets,
            graphql_variables
        )

        assets_by_company = {
            'assets': graphql_collection['assets']['collection']
        }

        return assets_by_company

    def get_asset_url(self, company_id, asset_id):
        parsed_url = urlparse(self.__conviso_client_interface.url)
        asset_path = '/scopes/{}/assets/{}'.format(
            company_id, asset_id
        )
        parsed_url = parsed_url._replace(path=asset_path)
        return parsed_url.geturl()
