"""Obtain an OCP OAuth token for an SSO IdP with Kerberos support."""

import functools
import typing
from urllib import parse

import html5lib
import requests
import requests_gssapi


class OcpOAuthLogin:
    """Obtain an OCP OAuth token for an SSO IdP with Kerberos support."""

    def __init__(self, api_url: str):
        """Create an instance for a certain cluster represented by its API URL."""
        self.session = requests.Session()
        self.auth = requests_gssapi.HTTPSPNEGOAuth(mutual_authentication=requests_gssapi.OPTIONAL)
        self.meta_url = parse.urljoin(api_url, '/.well-known/oauth-authorization-server')

    @functools.cached_property
    def _token_endpoint(self) -> str:
        """Return the URL of the OAuth token endpoint."""
        response = self.session.get(self.meta_url)
        response.raise_for_status()
        return str(response.json()['token_endpoint'])

    @functools.cached_property
    def identity_providers(self) -> typing.Dict[str, str]:
        """Return a dictionary of all identity providers and their URLs."""
        # https://github.com/openshift/library-go/blob/master/pkg/oauth/oauthdiscovery/urls.go
        response = self.session.get(self._token_endpoint + '/request')
        response.raise_for_status()
        # https://github.com/openshift/oauth-server/blob/master/pkg/server/selectprovider/templates.go
        root = html5lib.parse(response.text, namespaceHTMLElements=False)
        return {
            idp[0]: parse.urljoin(self._token_endpoint, href)
            for e in root.iterfind('.//a[@href]')
            if (idp := parse.parse_qs(parse.urlparse(href := e.attrib['href']).query).get('idp'))
        }

    def token(self, identity_provider: str) -> str:
        """Authenticate with the given identity provider and return an access token."""
        response = self.session.get(self.identity_providers[identity_provider], auth=self.auth)
        response.raise_for_status()
        # https://github.com/openshift/oauth-server/blob/master/pkg/server/tokenrequest/tokenrequest.go
        root = html5lib.parse(response.text, namespaceHTMLElements=False)
        data = {
            e.attrib['name']: e.attrib['value']
            for e in root.iterfind('.//form/input[@type="hidden"]')
        }

        response = self.session.post(response.url, data=data)
        response.raise_for_status()
        # https://github.com/openshift/oauth-server/blob/master/pkg/server/tokenrequest/tokenrequest.go
        root = html5lib.parse(response.text, namespaceHTMLElements=False)
        if (code := root.find('.//code')) is None:
            raise Exception(f'Unable to find access token in response: {response.text}')
        return str(code.text)
