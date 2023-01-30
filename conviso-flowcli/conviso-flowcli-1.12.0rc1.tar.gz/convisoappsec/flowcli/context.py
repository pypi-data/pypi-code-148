
import click

from convisoappsec.flow import api
from convisoappsec.flow.graphql_api import client
from convisoappsec.flow.resources_api import ConvisoGraphQLInterface
from convisoappsec.version import __version__


class FlowContext(object):
    def __init__(self):
        self.key = None
        self.url = None
        self.insecure = None
        self.ci_provider = None
        self.logger = None

    def create_flow_api_client(self):
        return api.RESTClient(
            key=self.key,
            url=self.url,
            insecure=self.insecure,
            user_agent={
                'name': 'flowcli',
                'version': __version__,
            },
            ci_provider_name=self.ci_provider.name
        )

    def create_conviso_graphql_client(self):
        return client.ConvisoGraphQLClient(
            base_url=self.url,
            apikey=self.key
        )

    def create_conviso_api_interface(self):
        return ConvisoGraphQLInterface(
            self.create_conviso_graphql_client()
        )


pass_flow_context = click.make_pass_decorator(
    FlowContext, ensure=True
)
