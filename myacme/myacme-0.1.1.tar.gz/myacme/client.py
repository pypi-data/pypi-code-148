'''
MyACME client library

Copyright: Copyright 2021-2023 AXY axy@declassed.art
License: BSD, see LICENSE for details.
'''

__all__ = [
    'MyAcmeClient',
    'MyAcmeError',
    'MyAcmeHttpError',
    'MyAcmeStateFS',
    'MyAcmeAuthzManual',
    'MyAcmeAuthzScript',
    'get_certificate_validity_period',
    'idna_decode',
    'idna_encode'
]

import base64
import hashlib
import json
import logging
import os
import re
import shlex
import subprocess
import tempfile
import time
import traceback

import idna
import requests

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography import x509
import cryptography.utils

logger = logging.getLogger(__name__)

class MyAcmeError(Exception):
    pass

class MyAcmeHttpError(MyAcmeError):

    def __init__(self, response):
        self.status = response.status_code
        try:
            payload = response.json()
            self.error_type = payload.get('type', '')
            self.detail = payload.get('detail', '')
        except Exception:
            self.error_type = ''
            self.detail = ''

class MyAcmeClient:

    #----------------------------------------------------------
    # Defaults

    rsa_key_size = 4096

    user_agent = 'MyACME beta'

    #----------------------------------------------------------
    # Initialization

    def __init__(self, directory_url, account_key=None):
        '''
        Initialize the instance of client object and if `account_key` argument
        is provided, set account key.
        If `account_key` argument is not provided, the user should set the key
        explicitly before using calling client methods.
        '''
        self._directory_url = directory_url
        self._acme_directory = None  # cached value, see acme_directory property
        self._account_key = None     # placeholder, see account_key property
        self._account_url = None     # cached value, see account_url property
        self._replay_nonce = None    # placeholder, the value will be initialized on first request

        if account_key:
            self.account_key = account_key

    @property
    def acme_directory(self):
        '''
        The directory object, as returned by ACME server.
        '''
        if not self._acme_directory:
            response = requests.get(self._directory_url, headers=self._make_request_headers())
            if response.status_code // 100 != 2:
                raise MyAcmeHttpError(response)
            self._acme_directory = response.json()
        return self._acme_directory

    #----------------------------------------------------------
    # Delay

    def delay(self, seconds):
        '''
        Let the user customize it.
        '''
        logger.debug('Delay for %s seconds', seconds)
        time.sleep(seconds)

    #----------------------------------------------------------
    # Account management

    @property
    def account_key(self):
        '''
        `account_key` property to get or set private key for ACME account.

        Setting account key is a mandatory initialization task.
        This can be done by `__init__` if `account_key` argument is provided.
        Otherwise, the user should set the key explicitly before calling other methods.

        Account key is mandatory for ACME protocol. Even if the account does not exist yet,
        the user should set account key to be able to call `create_account` method.

        The format for the key is PEM.
        '''
        return private_key_to_pem(self._account_key)

    @account_key.setter
    def account_key(self, account_key):
        self._account_key = private_key_from_pem(account_key)
        # reset cached account url
        self._account_url = None

    def generate_account_key(self):
        '''
        Generate private key for ACME account.

        Returns:
            bytes: private key in PEM format
        '''
        private_key = rsa.generate_private_key(
            public_exponent = 65537,
            key_size =  self.rsa_key_size
        )
        return private_key_to_pem(private_key)

    @property
    def account_url(self):
        '''
        Account URL is returned by ACME newAccount call and cached internally.
        This URL is required for many methods, so it's desirable to save it after account creation.
        Otherwise an extra call to ACME server will be issued to obtain this URL.
        This may break nonce sequence. Therefore, this property should be accessed BEFORE getting a nonce.

        This URL is reset in the following cases:
        * account key is set
        * account is deactivated
        '''
        if not self._account_url:
            response = self._new_account(only_return_existing=True)
            self._account_url = response.headers.get('Location', None)
        return self._account_url

    @account_url.setter
    def account_url(self, account_url):
        self._account_url = account_url

    def create_account(self, contact=[]):
        '''
        Create new account.

        The user should set account key before calling this method.

        Contacts by default is an empty list. Contacts are OPTIONAL for ACME protocol.
        If the user, for example, generates a certificate for an email server TLS,
        this implies no contact email is available yet.

        Args:
            contact (list): contact URLs, in the form "mailto:admin@example.org"

        Returns:
            str: URL for the account. This URL is cached for subsequent requests.
        '''
        response = self._new_account(contact=contact)
        self._account_url = response.headers['Location']
        return self._account_url

    def update_account(self, contact=[]):
        '''
        Update existing account.

        Args:
            contact (list): contact URLs, in the form "mailto:admin@example.org"
        '''
        self._simple_request(self.account_url, {'contact': contact})

    def get_account_status(self):
        '''
        Returns:
            account status (valid/deactivated/revoked), None if account does not exist
        '''
        try:
            response = self._new_account(only_return_existing=True)
        except MyAcmeHttpError as e:
            if e.status == 403:
                # deactivated or nonexistent
                return False
            elif e.error_type == 'urn:ietf:params:acme:error:accountDoesNotExist':
                return False
            else:
                raise
        payload = response.json()
        return payload['status']

    def change_account_key(self, new_account_key):
        '''
        Account key rollover. Set new account key for this object on success.
        Before calling this function ``new_account_key`` should be saved somewhere to avoid losing it on failure.
        '''
        old_account_key = self._account_key
        new_account_key = private_key_from_pem(new_account_key)

        # prepare inner JWS object
        old_key = {
            'protected': {
                'url': self.acme_directory['keyChange']
            },
            'payload': {
                'account': self.account_url,
                'oldKey': jwk_public(old_account_key)
            }
        }
        signed_old_key = jws(old_key, new_account_key)

        self._simple_request(self.acme_directory['keyChange'], signed_old_key)
        self._account_key = new_account_key

    def deactivate_account(self):
        '''
        Deactivate account.
        '''
        self._simple_request(self.account_url, {'status': 'deactivated'})
        self._account_url = None

    #----------------------------------------------------------
    # Helpers

    @property
    def _nonce(self):
        if not self._replay_nonce:
            self._replay_nonce = self._get_nonce()
        return self._replay_nonce

    def _get_nonce(self):
        '''
        Get new nonce value from ACME server.
        '''
        response = requests.head(self.acme_directory['newNonce'], headers=self._make_request_headers())
        if response.status_code != 200:
            raise MyAcmeHttpError(response)
        return response.headers['Replay-Nonce']

    def _make_request_headers(self, headers=None):
        return {
            'User-Agent': self.user_agent,
            **(headers or {})
        }

    def _post_as_get(self, url, signed_request):
        '''
        Issue POST-as-GET request.
        '''
        post_data = indented_json(signed_request)
        request_headers = self._make_request_headers({'Content-Type': 'application/jose+json'})
        self._replay_nonce = None  # drop used nonce, just in case of requests.post failure
        response = requests.post(url, headers=request_headers, data=post_data)
        self._replay_nonce = response.headers['Replay-Nonce']
        logger.debug('POST AS GET: %s', url)
        for k, v in response.headers.items():
            logger.debug(f'{k}: {v}')
        logger.debug(response.content.decode('ascii'))
        if response.status_code // 100 != 2:
            raise MyAcmeHttpError(response)
        return response

    def _simple_request(self, url, payload):
        '''
        Shorthand wrapper for typical requests.
        '''
        account_url = self.account_url
        nonce = self._nonce
        request = {
            'protected': {
                'nonce': nonce,
                'url': url,
                'kid': account_url
            },
            'payload': payload
        }
        signed_request = jws(request, self._account_key)
        return self._post_as_get(url, signed_request)

    def _new_account(self, contact=[], only_return_existing=False):
        '''
        Send newAccount request.
        This is a helper for account management methods.
        '''
        request = {
            'protected': {
                'nonce': self._nonce,
                'url': self.acme_directory['newAccount']
            },
            'payload': {
                'termsOfServiceAgreed': True,
                'contact': contact,
                'onlyReturnExisting': only_return_existing
            }
        }
        signed_request = jws(request, self._account_key)
        response = self._post_as_get(self.acme_directory['newAccount'], signed_request)
        return response

    #----------------------------------------------------------
    # Certificate issuance helpers

    def _new_order(self, domains):
        '''
        Issue `newOrder` request.

        There's no way to get the list of orders for Let's Encrypt, at least.
        However, repeated newOrder request with same parameters returns same URLs.
        '''
        response = self._simple_request(
            self.acme_directory['newOrder'],
            {'identifiers': [{'type': 'dns', 'value': idna_encode(domain_name)} for domain_name in domains]}
        )
        payload = response.json()
        order_url = response.headers['Location']  # https://www.rfc-editor.org/errata/eid5979
        return order_url, payload

    def _get_order(self, order_url):
        '''
        Issue request to order_url.
        '''
        # As of time of writing neither RFC8555 nor its errata specify the format of payload
        #     which seems to be empty string, not {}
        response = self._simple_request(order_url, '')
        payload = response.json()
        return payload

    def _authz_status(self, authz_url):
        '''
        Issue request for authorization URL, as returned by `newOrder` request.
        '''
        # Retry-After is not supported
        # https://github.com/letsencrypt/boulder/blob/master/docs/acme-divergences.md
        response = self._simple_request(authz_url, '')
        return response.json()

    def _challenge(self, challenge_url):
        '''
        Respond to challenge_url to start authorization.
        '''
        response = self._simple_request(challenge_url, {})
        return response.json()

    def _finalize(self, finalize_url, csr):
        '''
        Send CSR to finalize_url.
        '''
        response = self._simple_request(finalize_url, {'csr': csr})
        return response.json()

    def _download_certificate(self, certificate_url):
        response = self._simple_request(certificate_url, '')
        return response.content

    #----------------------------------------------------------
    # Certificate issuance

    def process_order(self, domains, authenticator, state, private_key=None, csr=None, csr_fields=None):
        '''
        Shorthand method to obtain a certificate.
        '''
        domains = [domains] if isinstance(domains, str) else domains
        order = MyAcmeOrder(self, domains, authenticator, state, private_key=private_key, csr=csr, csr_fields=csr_fields)
        attempt = 1
        while True:
            try:
                status = order.process_order()
                if status == 'failed':
                    logger.error('Failed processing certificate order for %s', ', '.join(domains))
                    return None
                else:
                    return order
            except MyAcmeError:
                # protocol error, need to investgate
                raise
            except Exception:
                # temporary error?
                if attempt >= 5:
                    raise
                logger.error('Failed attempt %s to get a certificate for %s', attempt, ', '.join(domains))
                logger.debug(traceback.format_exc())
                attempt += 1


class MyAcmeOrder:
    '''
    MyAcmeOrder implements state machine to apply for certificate issuance.

    To apply for certificate issuance the user should call `process_order` method.
    Normally, this method returns completion status as string, either 'complete' or 'failed'.
    In case of error, network error, for example, it raises an exception.
    In such a case it should be called again.

    This class generates private key and CSR if the user does not provide them.
    If the user provides CSR, private key is unnecessary for certificate issuance.
    If the user provides private key but does not provide a CSR, the CSR will be generated automatically.
    If the user provides neither CSR, nor private key, both will be auto-generated.
    '''

    retry_delay_min = 5   # seconds
    retry_delay_max = 60  # seconds

    def __init__(self, acme, domains, authenticator, state, private_key=None, csr=None, csr_fields=None, **kwargs):
        '''
        Args:
            acme: an instance of `MyAcmeClient` class
            domains: domain name or list of domain names
            authenticator: an instance of ``MyAcmeAuthzABC`` subclass
            private_key (bytes): private key for the certificate in PEM format. If not provided, the key will be generated.
                                 Private key is unnecessary if CSR is provided, so this argument will not be used.
            csr (bytes): CSR in PEM format.
            csr_fields (dict): additional fields to include in CSR. Not used if CSR is provided by user.
        '''
        self.acme = acme
        self.domains = [domains] if isinstance(domains, str) else domains
        self.authenticator = authenticator
        self.state = state
        self._custom_private_key = private_key_from_pem(private_key) if private_key else None
        self._custom_csr = csr_from_pem(csr) if csr else None
        self._custom_csr_fields = dict(csr_fields) if csr_fields is not None else dict()

    _transitions = {
        # current state   transition method   possible next states, returned by transition method
        'new':            ('_new_order',      ('authorization', 'failed', 'complete', 'finalization', 'wait-issuance')),
        'authorization':  ('_authorization',  ('finalization', 'authorization', 'failed')),
        'finalization':   ('_finalization',   ('failed', 'complete', 'wait-issuance', 'download-cert')),
        'wait-issuance':  ('_wait_issuance',  ('download-cert', 'failed', 'complete', 'wait-issuance')),
        'download-cert':  ('_download_cert',  ('complete', ))
        # terminal states: complete, failed
    }

    def _get_transition(self):
        '''
        Get transition entry for current state.
        '''
        state = self.state['current_state']
        if state not in self._transitions:
            raise MyAcmeError(f'Internall error: bad state {state}')
        return self._transitions[state]

    def _make_new_state(self, order_status):
        '''
        Map order status to new state.
        '''
        if order_status == 'pending':
            # the order is awaiting authorization
            return 'authorization'
        if order_status == 'ready':
            # the order has passed authorization
            return 'finalization'
        if order_status == 'processing':
            # certificate issuance is still in progress
            return 'wait-issuance'
        if order_status == 'valid':
            # certificate has been issued
            return 'download-cert'
        if order_status == 'invalid':
            # the order is cancelled, expired, or CSR is invalid
            return 'failed'

        raise MyAcmeError(f'ACME protocol error: bad order status {order_status}')

    def process_order(self):
        '''
        Returns:
            str: status of processing: complete or failed
        '''
        # initialize state
        self.state.load()
        if self.state.get('current', None) in ['complete', 'failed']:
            # previous order complete
            self.state.clear()
        if len(self.state) == 0:
            # no saved state, start new order
            self.state['current_state'] = 'new'

        # run state machine
        while self.state['current_state'] not in ['complete', 'failed']:
            next_method, next_states = self._get_transition()
            next_method = getattr(self, next_method)
            new_state = next_method()
            if new_state not in next_states:
                raise MyAcmeError(f'Internal error: bad new state {new_state}')
            self.state['current_state'] = new_state

            # save state after each transition
            self.state.save()

        return self.state['current_state']

    def get_certificate(self):
        '''
        Get issued certificate.
        This method should be called after ``process_order`` returns "complete".

        Returns:
            certificate, as bytes, or None if ``process_order`` is not complete
        '''
        if self.state.get('certificate', None):
            return self.state['certificate'].encode('ascii')
        else:
            return None

    def get_private_key(self):
        '''
        Get auto-generated private key.
        Such a key is saved in state object.

        Returns:
            private key in PEM format as bytes or None if the key was not generated,
            i.e. the user provided the key or CSR
        '''
        if self.state.get('private_key', None):
            return self.state['private_key'].encode('ascii')
        else:
            return None

    def _rate_limit_delay(self, identifier):
        '''
        Calculate delay value from number of attempts and delay execution by calling `self.acme.delay`.

        Args:
            identifier: name of the data structure in `self.state`
        '''
        now = time.time()
        data = self.state.setdefault(identifier, {'attempt': 0, 'delay_start': now})
        data['attempt'] += 1
        # calculate delay_end from previous delay_start
        data['delay_end'] = data['delay_start'] + min((data['attempt'] - 1) * self.retry_delay_min, self.retry_delay_max)
        data['delay_start'] = now
        # calculate period from current time and delay_end
        seconds = data['delay_end'] - now
        if seconds > 0.0:
            self.acme.delay(max(1.0, seconds))

    def _new_order(self):
        '''
        Issue new order request.
        '''
        logger.debug('New order')
        order_url, order = self.acme._new_order(self.domains)
        # If an order already exists, Let's Encrypt returns it in response to newOrder request.
        # The returned order has "ready" status. For some reason, subsequent finalize
        # fails with orderNotReady error.
        # Extra request to get the order fixes the problem.
        order = self.acme._get_order(order_url)
        self.state['order'] = order
        self.state['order_url'] = order_url
        return self._make_new_state(order['status'])

    def _authorization(self):
        '''
        Check statuses of authorizations and process pending ones.
        '''
        logger.debug('Authorization')

        order = self.state['order']
        order_url = self.state['order_url']

        valid_authorizations = 0
        invalid_authorizations = 0
        for authz_url in order['authorizations']:
            if self._process_authz(authz_url):
                valid_authorizations += 1
            else:
                invalid_authorizations += 1

        # check if all authorizations are valid
        if len(order['authorizations']) == valid_authorizations:
            return 'finalization'

        # check if all authorizations are invalid
        elif len(order['authorizations']) == invalid_authorizations:
            # Let's Encrypt does not implement the ability to retry challenges:
            # https://github.com/letsencrypt/boulder/blob/master/docs/acme-divergences.md#section-82
            # Return state based on order status, which, definitely, is failed.
            # We could return failed without getting order, just do this for the record in the saved state.
            logger.error('Authorization failed')
            order = self.acme._get_order(order_url)
            self.state['order'] = order
            return self._make_new_state(order['status'])

        else:
            # not all authorizations are valid yet, try again?
            return 'new'

            # XXX needs edge case testing when wrong key_digest is set by setup_authz,
            #     this might lead to infinite loop;
            #     break such a loop using retry count?
            #     anyway, state approach might need revising
            #return 'authorization'

    def _process_authz(self, authz_url):
        '''
        Process authorization for given URL.
        Return True if authorization is succeeded, False if not.
        '''
        logger.debug('Processing authorization %s', authz_url)
        authz_statuses = self.state.setdefault('authz_statuses', dict())
        challenges_sent = self.state.setdefault('challenges_sent', dict())
        authz_need_cleanup = self.state.setdefault('authz_need_cleanup',
                                                   dict())  # set() is better but it's not JSON-serializable
        while True:
            # get status for authz_url
            self._rate_limit_delay('authz_rate_limit')
            authz_status = self.acme._authz_status(authz_url)
            authz_statuses[authz_url] = authz_status

            if authz_status['status'] == 'pending':
                # check if challenge is already sent
                if authz_url not in challenges_sent:
                    # challenge is not sent yet, do that
                    challenges_sent[authz_url] = self._setup_authz(authz_url)
                    authz_need_cleanup[authz_url] = True
                    self.state.save()
                continue

            # check if status is valid for this authz_url
            if authz_status['status'] == 'valid':
                result = True
            else:
                # consider all other statuses as invalid, that includes deactivated and revoked
                result = False

            if authz_url in authz_need_cleanup:
                self._cleanup_authz(authz_url)
                del authz_need_cleanup[authz_url]
                self.state.save()

            return result

    def _setup_authz(self, authz_url):
        '''
        Setup authorization for given authz_url.
        Return challange_sent dict.
        '''
        authz_status = self.state['authz_statuses'][authz_url]

        # collect authorization methods and parameters
        authz_params = dict()  # {challenge_type: {token: ..., key: ..., key_digest: ...}}
        challenge_urls = dict()
        for challenge in authz_status['challenges']:
            key_authz = challenge['token'] + '.' + thumbprint_public(self.acme._account_key)
            key_digest = sha256_base64url(key_authz.encode('ascii'))
            authz_params[challenge['type']] = {
                'token': challenge['token'],
                'key': key_authz,
                'key_digest': key_digest
            }
            challenge_urls[challenge['type']] = challenge['url']

        # setup authorization
        # note: validation_method is an alias for challenge_type

        domain = idna_decode(authz_status['identifier']['value'])
        used_validation_method = self.authenticator.setup_domain_validation(domain, authz_params)

        # issue challenge request to start authorization
        chal_url = challenge_urls[used_validation_method]
        logger.debug('Sending challenge request for %s', chal_url)
        self.acme._challenge(chal_url)

        return {
            'url': chal_url,
            'type': used_validation_method,
            'params': authz_params[used_validation_method]
        }

    def _cleanup_authz(self, authz_url):
        '''
        Call `cleanup_domain_validation` for the challenge sent.
        '''
        try:
            authz_status = self.state['authz_statuses'][authz_url]
            challenges_sent = self.state['challenges_sent']
            if authz_url in challenges_sent:
                chs = challenges_sent[authz_url]
                used_validation_method = chs['type']
                authz_params = chs['params']
                domain = idna_decode(authz_status['identifier']['value'])
                self.authenticator.cleanup_domain_validation(domain, used_validation_method, authz_params)
        except Exception:
            logger.error('cleanup_domain_validation failed')
            logger.debug(traceback.format_exc())

    def _finalization(self):
        '''
        All authorizations have passed, upload CSR to the finalize URL
        '''
        logger.debug('Finalization')
        if self._custom_csr:
            # CSR is provided by user
            csr = base64url(self._custom_csr)
        else:
            # will generate CSR
            # need a private key for signing CSR
            if self._custom_private_key:
                # private key is provided by user
                private_key = self._custom_private_key
            else:
                # generate private key
                private_key = rsa.generate_private_key(
                    public_exponent = 65537,
                    key_size = self.acme.rsa_key_size
                )
                self.state['private_key'] = private_key_to_pem(private_key).decode('ascii')
            # generate CSR
            csr = self._generate_csr(private_key)

        finalize_url = self.state['order']['finalize']
        order = self.acme._finalize(finalize_url, csr)
        self.state['order'] = order
        return self._make_new_state(order['status'])

    def _wait_issuance(self):
        '''
        Poll the order URL.
        '''
        logger.debug('Awaiting certificate issuance')
        self._rate_limit_delay('order_rate_limit')
        order = self.acme._get_order(self.state['order_url'])
        self.state['order'] = order
        return self._make_new_state(order['status'])

    def _download_cert(self):
        '''
        Download certificate from ACME server.
        '''
        logger.debug('Downloading certificate')
        certificate_url = self.state['order']['certificate']
        self.state['certificate'] = self.acme._download_certificate(certificate_url).decode('ascii')
        return 'complete'

    def _generate_csr(self, private_key):
        '''
        Generate CSR.
        '''
        # instantiate CSR builder
        builder = x509.CertificateSigningRequestBuilder()

        # prepare list of NameOID attributes
        name_list = [
            x509.NameAttribute(x509.oid.NameOID.COMMON_NAME, idna_encode(self.domains[0]))
        ]
        for name, value in self._custom_csr_fields.items():
            name = '_'.join(re.split('[ _]+', name.upper()))
            if name == 'COMMON_NAME':
                # already defined, avoid overriding
                continue
            if not hasattr(x509.oid.NameOID, name):
                raise MyAcmeError(f'Bad CSR field name {name}')
            name_list.append(x509.NameAttribute(getattr(x509.oid.NameOID, name), value))

        builder = builder.subject_name(x509.Name(name_list))

        # add SAN extension for multiple domains
        if len(self.domains) > 1:
            san = x509.SubjectAlternativeName([x509.DNSName(idna_encode(domain)) for domain in self.domains])
            builder = builder.add_extension(san, critical=False)

        # build CSR
        request = builder.sign(private_key, hashes.SHA256())
        csr = request.public_bytes(serialization.Encoding.DER)
        return base64url(csr)

class MyAcmeStateFS(dict):
    '''
    State is a subclass of `dict` with `load` and `save` methods for persistence.

    This subclass implements saving state to a file in JSON, i.e.

        directory/example.com.myacme.json
    '''
    def __init__(self, domains, directory):
        domains = [domains] if isinstance(domains, str) else domains
        self.directory = os.path.expanduser(directory)
        self.basename = domains[0].lower().replace('*', 'STAR')
        self.state_filename = os.path.join(directory, self.basename + '.myacme.json')

    def load(self):
        if os.path.exists(self.state_filename):
            with open(self.state_filename, 'rb') as f:
                for k, v in json.load(f).items():
                    self[k] = v

    def save(self):
        # atomically replace the state
        with self.create_temp_file() as temp_file:
            temp_file.write(indented_json(dict(self.items())))
            temp_filename = temp_file.name
        os.replace(temp_filename, self.state_filename)

    def create_temp_file(self):
        return tempfile.NamedTemporaryFile(
            prefix = self.basename + '.',
            dir = self.directory,
            delete = False
        )

class MyAcmeAuthzManual:
    '''
    Print instructions how to setup domain validation and wait for user input.
    '''
    def setup_domain_validation(self, domain, authz_params):
        '''
        This method is called for all available challenge types methods for `domain`.

        Args:
            domain: domain name for which to setup validation
            authz_params (dict): {challenge_type: {token: ..., key: ..., key_digest: ...}}

        Returns:
            str: applied validation method, i.e. challenge_type, http-01, dns-01, etc.
        '''
        available_methods = []
        if 'dns-01' in authz_params:
            available_methods.append('dns-01')
            params = authz_params['dns-01']
            print()
            print(f'=== How to set up dns-01 validation for {domain} ===')
            print('Create the following TXT record:')
            print(f"_acme-challenge.{idna_encode(domain)}. 300 IN TXT \"{params['key_digest']}\"")
        if 'http-01' in authz_params:
            available_methods.append('http-01')
            params = authz_params['http-01']
            print()
            print(f'=== How to set up http-01 validation for {domain} ===')
            print(f"Write the following value to {domain}/.well-known/acme-challenge/{params['token']}")
            print(params['key'])
        if len(available_methods) == 0:
            if len(authz_params) == 0:
                raise MyAcmeError('No domain validation methods are provided')
            else:
                raise MyAcmeError(f'Domain validation methods {", ".join(sorted(authz_params.keys()))} are not supported')
        print()
        while True:
            for validation_method in available_methods:
                s = input(f'Use {validation_method} (y/n)? ')
                if s.lower().strip() == 'y':
                    return validation_method

    def cleanup_domain_validation(self, domain, validation_method, authz_params):
        '''
        This method should remove files or DNS records or other data used for domain validattion.

        Args:
            domain: domain name for which to cleanup validation
            validation_method: the method used for validation as returned by setup_domain_validation.
            authz_params: parameters for specific validation method, i.e. {token: ..., key: ..., key_digest: ...}
        '''
        if validation_method == 'dns-01':
            print()
            print(f"Please remove TXT record _acme-challenge.{idna_encode(domain)}. 300 IN TXT \"{authz_params['key_digest']}\"")
            input('Press ENTER when done')
        elif validation_method == 'http-01':
            print()
            print(f"Please remove static file {domain}/.well-known/acme-challenge/{authz_params['token']}")
            input('Press ENTER when done')

class MyAcmeAuthzScript:
    '''
    Invoke commands for setting up/cleaning up domain validation.

    Configuration example:

        {
            'dns-01': {
                'setup': [
                    'myacme-zonefile /etc/bind/primary/{subdomain[1]} add-acme-challenge {domain} {key_digest}',
                    'rndc reload {idna_subdomain[1]}',
                    'sleep 10'
                ],
                'cleanup': [
                    'myacme-zonefile /etc/bind/primary/{subdomain[1]} del-acme-challenge {domain} {key_digest}',
                    'rndc reload {idna_subdomain[1]}'
                ]
            },
            'http-01': {
                'setup': [
                    'mkdir -p /var/www/{domain}/.well-known/acme-challenge',
                    'echo {key} >/var/www/{domain}/.well-known/acme-challenge/{token}'
                ],
                'cleanup': [
                    'rm /var/www/{domain}/.well-known/acme-challenge/{token}'
                ]
            }
        }

    Keys other than 'http-01' and 'dns-01' are ignored.

    Substitutions for commands, shell-escaped:

    * domain:          primary domain name, leading wildcard, if any, is stripped
    * idna_domain:     primary domain name, in IDNA encoding; leading wildcard, if any, is stripped
    * subdomain:       list of subdomains, see a note below
    * idna_subdomain:  list subdomains in IDNA encoding, see a note below
    * token:           domain validation token
    * key:             domain validation key for http-01
    * key_digest:      domain validation key digest for dns-01

    The index for subdomain and idna_subdomain can be treated as subdomain level:
    0 is TLD, 1 is a second-level domain (apex or bare domain), and so on.
    E.g. for abc.example.com subdomain[0] is com, subdomain[1] is example.com, subdomain[2] is abc.example.com

    '''
    def __init__(self, config):
        '''
        Args:
            config (dict): configuration object
        '''
        self.config = config

    def setup_domain_validation(self, domain, authz_params):
        '''
        This method is called for all available challenge types methods for `domain`.

        Args:
            domain: domain name for which to setup validation
            authz_params (dict): {challenge_type: {token: ..., key: ..., key_digest: ...}}

        Returns:
            str: applied validation method, i.e. challenge_type, http-01, dns-01, etc.
        '''
        # get available validation methods
        validation_methods = sorted(set(authz_params.keys()).intersection(self.config.keys()))
        if len(validation_methods) == 0:
            raise MyAcmeError(f"No suitable validation methods provided for {domain}: "
                              f"needed {', '.join(sorted(authz_params.keys()))}; "
                              f"provided {', '.join(sorted(self.config.keys()))}")

        # choose validation method
        validation_method = validation_methods[0]

        # prepare substitutions
        substitutions = self._prepare_substitutions(domain, authz_params[validation_method])

        # run setup commands
        self._run_commands(self.config[validation_method]['setup'], substitutions)

        return validation_method

    def cleanup_domain_validation(self, domain, validation_method, authz_params):
        '''
        This method should remove files or DNS records or other data used for domain validattion.

        Args:
            domain: domain name for which to cleanup validation
            validation_method: the method used for validation as returned by setup_domain_validation.
            authz_params: parameters for specific validation method, i.e. {token: ..., key: ..., key_digest: ...}
        '''
        # prepare substitutions
        substitutions = self._prepare_substitutions(domain, authz_params)

        # run cleanup commands
        self._run_commands(self.config[validation_method]['cleanup'], substitutions)

    def _prepare_substitutions(self, domain, authz_params):
        '''
        Prepare substitutions for setup/cleanup commands.
        '''
        idna_domain = idna_encode(domain)
        domain_parts = domain.split('.')
        idna_domain_parts = idna_domain.split('.')
        return dict(
            domain          = shlex.quote(domain),
            idna_domain     = shlex.quote(idna_domain),
            subdomain       = [shlex.quote('.'.join(domain_parts[i-1:])) for i in range(len(domain_parts),0,-1)],
            idna_subdomain  = [shlex.quote('.'.join(idna_domain_parts[i-1:])) for i in range(len(idna_domain_parts),0,-1)],
            token           = shlex.quote(authz_params['token']),
            key             = shlex.quote(authz_params['key']) if 'key' in authz_params else '',
            key_digest      = shlex.quote(authz_params['key_digest']) if 'key_digest' in authz_params else ''
        )

    def _run_commands(self, commands, substitutions):
        '''
        Apply substitutions and run commands.
        '''
        for command in commands:
            command = command.format_map(substitutions)
            logger.debug('Executing %s', command)
            result = subprocess.run(command, capture_output=True, text=True, shell=True)
            if result.returncode != 0:
                raise Exception(f'Failed {command}: {result.stderr or result.stdout}')

#-----------------------------------------------------------------------------------
# Helper functions

def get_certificate_validity_period(cert_bytes):
    '''
    Get dates from the certificate between which it is valid.

    Args:
        cert_bytes: certificate in PEM format

    Returns:
        tuple: (not_valid_before, not_valid_after), datetime, UTC, inclusive.
    '''
    cert = x509.load_pem_x509_certificate(cert_bytes)
    return (cert.not_valid_before, cert.not_valid_after)

def base64url(b):
    '''
    https://tools.ietf.org/html/rfc4648#section-5
    The function accepts bytes and returns string, to simplify typical use cases.
    '''
    return base64.urlsafe_b64encode(b).replace(b'=', b'').decode('ascii')

def sha256_base64url(b):
    '''
    Calculate SHA256 hash of bytes and return an ASCII string in base64url format.
    The function accepts bytes and returns string, to simplify typical use cases.
    '''
    return base64url(hashlib.sha256(b).digest())

def indented_json(value):
    '''
    Serialize value to indented JSON.
    Indented JSON is used for most ACME requests.

    Returns:
        bytes: serialized value in UTF-8
    '''
    return json.dumps(value, sort_keys=True, indent=4).encode('utf-8')

def compact_json(value):
    '''
    Serialize value to compact JSON.
    Compact JSON is used for key thumbprints.

    Returns:
        bytes: serialized value in UTF-8
    '''
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode('utf-8')

def private_key_to_pem(private_key):
    '''
    Convert private key to PEM format, as bytes.
    '''
    return private_key.private_bytes(
        encoding = serialization.Encoding.PEM,
        format = serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm = serialization.NoEncryption()
    )

def private_key_from_pem(key_bytes):
    '''
    Return private key object from `key_bytes` in PEM format.
    '''
    return serialization.load_pem_private_key(key_bytes, None)

def csr_to_pem(csr):
    '''
    Convert CSR to PEM format, as bytes.
    '''
    return csr.public_bytes(csr, serialization.Encoding.PEM)

def csr_from_pem(csr_bytes):
    '''
    Return CSR object from `csr_bytes` in PEM format.
    '''
    return x509.load_pem_x509_certificate(csr_bytes)

def jws(request, private_key):
    '''
    Build signed request.
    https://tools.ietf.org/html/rfc7515
    '''
    # make a copy of protected header to modify
    protected = request['protected'].copy()

    # set algorithm and key fields
    # TODO set these fields depending on private key class?
    protected['alg'] = 'RS256'
    if 'kid' not in protected:
        protected['jwk'] = jwk_public(private_key)

    # encode protected headers and payload
    protected = base64url(indented_json(protected))
    if request['payload'] == '':
        # somewhat strange, but empty string should produce empty string
        # i.e. if we encoded empty string in normal way, it would look as IiI which stands for ""
        payload = ''
    else:
        payload = base64url(indented_json(request['payload']))

    # calculate signature
    signing_input = '.'.join((
        protected,
        payload
    ))
    signature = private_key.sign(signing_input.encode('ascii'), padding.PKCS1v15(), hashes.SHA256())

    # prepare output
    signed_request = {
        'signature': base64url(signature),
        'protected': protected,
        'payload': payload
    }
    return signed_request

def jwk_public(private_key):
    '''
    Make JWK representation of public key.
    '''
    public_numbers = private_key.public_key().public_numbers()
    return {
        'kty': 'RSA',
        'e': base64url(cryptography.utils.int_to_bytes(public_numbers.e)),
        'n': base64url(cryptography.utils.int_to_bytes(public_numbers.n))
    }

def thumbprint_public(private_key):
    '''
    Make thumbpring of public key.
    https://tools.ietf.org/html/rfc8555#section-8.1

    Returns:
        str: thumbprint of public key
    '''
    # make JWK representation of public key
    key = jwk_public(private_key)
    # encode to compact JSON
    key = compact_json(key)
    # compute thumbprint
    return sha256_base64url(key)

def idna_encode(domain):
    '''
    Encode domain name to ASCII representation in IDNA encoding.
    '''
    # encode each part except stars
    parts = ['*' if part == '*' else idna.encode(part).decode('ascii') for part in domain.split('.')]
    return '.'.join(parts)

def idna_decode(domain):
    '''
    Decode domain name from IDNA.
    '''
    # decode each part except stars
    parts = ['*' if part == '*' else idna.decode(part) for part in domain.split('.')]
    return '.'.join(parts)
