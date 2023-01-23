import copy
import sys

import collections
from .request import Request


if sys.version_info[0] == 3:
    def iteritems(d, **kw):
        return iter(d.items(**kw))

elif sys.version_info[0] == 2:
    def iteritems(d, **kw):
        return iter(d.iteritems(**kw))


# Settings
api_secret = None
api_public = None
api_version = None


# API constants
api_main = 'https://api.omise.co'
api_vault = 'https://vault.omise.co'


__all__ = [
    'Account',
    'Balance',
    'BankAccount',
    'Capability',
    'Card',
    'Chain',
    'Charge',
    'Collection',
    'Customer',
    'Dispute',
    'Document',
    'Event',
    'Forex',
    'Link',
    'Occurrence',
    'Receipt',
    'Recipient',
    'Refund',
    'Search',
    'Schedule',
    'Source',
    'Token',
    'Transaction',
    'Transfer',
]


def _get_class_for(type):
    """Returns a :type:`class` corresponding to :param:`type`.

    Used for getting a class from object type in JSON response. Usually, to
    instantiate the Python object from response, this function is called in
    the form of ``_get_class_for(data['object']).from_data(data)``.

    :type type: str
    :rtype: class
    """
    return {
        'account': Account,
        'balance': Balance,
        'bank_account': BankAccount,
        'capability': Capability,
        'card': Card,
        'chain': Chain,
        'charge': Charge,
        'customer': Customer,
        'dispute': Dispute,
        'document': Document,
        'event': Event,
        'forex': Forex,
        'link': Link,
        'list': Collection,
        'occurrence': Occurrence,
        'receipt': Receipt,
        'recipient': Recipient,
        'refund': Refund,
        'schedule': Schedule,
        'search': Search,
        'source': Source,
        'token': Token,
        'transfer': Transfer,
        'transaction': Transaction,
    }.get(type)


def _as_object(data):
    """Returns a Python :type:`object` from API response.

    Accepts a :type:`dict` returned from Omise API and instantiate it as
    Python object using the class returned from :func:`_get_class_for`.

    :type data: dict | list
    :rtype: T <= Base
    """
    if isinstance(data, list):
        return [_as_object(i) for i in data]
    elif isinstance(data, dict):
        class_ = _get_class_for(data.get('object'))
        if not class_:
            class_ = Base
        return class_.from_data(data)
    return data


class Base(object):
    """Provides a base class for all API classes.

    The base class that all API classes inherit from. The instance of
    this class proxies its attributes access to :type:`dict` and also
    track changes made to it.

    Basic usage::

        >>> import omise
        >>> obj = omise.Base.from_data({'id': 'test'})
        <Base id='test' at 0x7f0d931cf740>
        >>> obj.id
        'test'
    """

    def __init__(self):
        super(Base, self).__init__()
        self._attributes = dict()
        self._changes = set()

    def __setattr__(self, key, value):
        if key[0] == '_':
            super(Base, self).__setattr__(key, value)
        else:
            self._changes.add(key)
            self._attributes[key] = value

    def __getattr__(self, key):
        if key[0] == '_':
            raise AttributeError(key)
        try:
            value = self._attributes[key]
            if isinstance(value, dict):
                return _as_object(value)
            return value
        except KeyError as e:
            raise AttributeError(*e.args)

    def __repr__(self):
        id_ = self._attributes.get('id')
        return '<%s%s at %s>' % (
            type(self).__name__,
            ' id=%s' % repr(str(id_)) if id_ else '',
            hex(id(self)))

    @classmethod
    def from_data(cls, data):
        """Instantiate the class with the given data.

        Creates a new instance of this class with :param:`data` assigned to it.
        This method is what is called after the data is retrieved from the API.

        :param data: data to instantiate this class with.
        :type data: dict
        """
        instance = cls()
        instance._reload_data(data)
        return instance

    @classmethod
    def _request(cls):
        return NotImplementedError

    @classmethod
    def _collection_path(cls):
        return NotImplementedError

    @classmethod
    def _instance_path(cls, *args):
        raise NotImplementedError

    def _reload_data(self, data):
        self._attributes = dict()
        for k, v in iteritems(data):
            self._attributes[k] = v
        self._changes = set()
        return self

    @property
    def changes(self):
        """Property that returns a :type:`dict` of attributes pending update.

        This method is used to track changes made to attribute of an instance
        which is often used to determine which attributes to update on the
        server when :method:`update` is called.

        :rtype: dict
        """
        return dict((c, self._attributes.get(c)) for c in self._changes)


class _MainResource(Base):

    @classmethod
    def _request(cls, *args, **kwargs):
        return Request(api_secret, api_main, api_version).send(*args, **kwargs)

    def _upload(cls, *args, **kwargs):
        return Request(api_secret, api_main, api_version).send_file(*args, **kwargs)

    def _nested_object_path(self, association_cls):
        return (
            self.__class__._collection_path(),
            self.id, association_cls._collection_path()
        )


class _VaultResource(Base):

    @classmethod
    def _request(cls, *args, **kwargs):
        return Request(api_public, api_vault, api_version).send(*args, **kwargs)


class _PublicResource(Base):

    @classmethod
    def _request(cls, *args, **kwargs):
        return Request(api_public, api_main, api_version).send(*args, **kwargs)


class Account(_MainResource, Base):
    """API class representing accounts details.

    This API class is used for retrieving account information such as creator
    email or account creation date. The account retrieved by this API is the
    account associated with API secret key.

    Basic usage::

        >>> import omise
        >>> omise.api_secret = 'skey_test_4xs8breq3htbkj03d2x'
        >>> account = omise.Account.retrieve()
        <Account id='acct_4xs8bre8a8vhrgijcjg' at 0x7f7410021990>
        >>> account.email
        None
    """

    @classmethod
    def _instance_path(cls, *args):
        return 'account'

    @classmethod
    def retrieve(cls):
        """Retrieve the account details associated with the API key.

        :rtype: Account
        """
        return _as_object(cls._request('get', cls._instance_path()))

    def reload(self):
        """Reload the account details.

        :rtype: Account
        """
        return self._reload_data(self._request('get', self._instance_path()))

    def update(self, **kwargs):
        """Update account settings with the given arguments.

        See the `update an account`_ section in the API documentation for list
        of available arguments.

        Basic usage::

            >>> import omise
            >>> omise.api_secret = 'skey_test_4xs8breq3htbkj03d2x'
            >>> account = omise.Account.retrieve()
            >>> account.update(webhook_uri='https://omise-flask-example.herokuapp.com/webhook')
            <Account id='account_test_5kms3d70v77fs5c37v6' at 0x108cec240>

        :param \*\*kwargs: arguments to update an account.
        :rtype: Account

        .. _update an account:
        ..     https://www.omise.co/account-api#update
        """

        changed = copy.deepcopy(self.changes)
        changed.update(kwargs)
        return self._reload_data(
            self._request('patch',
                          self._attributes['location'],
                          changed))


class Balance(_MainResource, Base):
    """API class representing balance details.

    This API class is used for retrieving current balance of the account.
    Balance do not have ID associated to it and is immutable.

    Basic usage::

        >>> import omise
        >>> omise.api_secret = 'skey_test_4xs8breq3htbkj03d2x'
        >>> balance = omise.Balance.retrieve()
        <Balance at 0x7f7410021868>
        >>> balance.total
        0
    """

    @classmethod
    def _instance_path(cls, *args):
        return 'balance'

    @classmethod
    def retrieve(cls):
        """Retrieve the balance details for current account.

        :rtype: Balance
        """
        return _as_object(cls._request('get', cls._instance_path()))

    def reload(self):
        """Reload the balance details.

        :rtype: Balance
        """
        return self._reload_data(self._request('get', self._instance_path()))


class BankAccount(Base):
    """API class representing bank account details.

    This API class represents a bank account information returned from other
    APIs. Bank accounts are not created directly with this class, but instead
    created with :class:`Recipient`.

    Basic usage::

        >>> import omise
        >>> omise.api_secret = 'skey_test_4xs8breq3htbkj03d2x'
        >>> recipient = omise.Recipient.retrieve('recp_test_5086xmr74vxs0ajpo78')
        >>> bank_account = recipient.bank_account
        <BankAccount name='SOMCHAI PRASERT' at 0x7f79c41e9d00>
        >>> bank_account.name
        'SOMCHAI PRASERT'
    """

    def __repr__(self):
        name = self._attributes.get('name')
        return '<%s%s at %s>' % (
            type(self).__name__,
            ' name=%s' % repr(str(name)) if name else '',
            hex(id(self)))


class Capability(_PublicResource, Base):
    """API class representing capability details.

    This API class is used for retrieving the account capabilities. It requires
    the public key to be set in ``omise.api_public``.

    Basic usage::

        >>> import omise
        >>> omise.api_public = 'pkey_test_4xs8breq32civvobx15'
        >>> capability = omise.Capability.retrieve()
        <Capability at 0x7f9b242bddd0>
        >>> capability.zero_interest_installments
        True
    """

    @classmethod
    def _instance_path(cls, *args):
        return 'capability'

    @classmethod
    def retrieve(cls):
        """Retrieve the account capabilities.

        :rtype: Capability
        """
        return _as_object(cls._request('get', cls._instance_path()))

    def reload(self):
        """Reload the capability details.

        :rtype: Capability
        """
        return self._reload_data(self._request('get', self._instance_path()))


class Token(_VaultResource, Base):
    """API class for creating and retrieving credit card token with the API.

    Credit card tokens are a unique ID that represents a card that could
    be used in place of where a card is required. Token can be used only
    once and invoked immediately after it is used.

    This API class is used for retrieving and creating token representing
    a card with the vault API. Unlike most other API, this API requires the
    public key to be set in ``omise.api_public``.

    Basic usage::

        >>> import omise
        >>> omise.api_public = 'pkey_test_4xs8breq32civvobx15'
        >>> token = omise.Token.retrieve('tokn_test_4xs9408a642a1htto8z')
        <Token id='tokn_test_4xs9408a642a1htto8z' at 0x7f406b384990>
        >>> token.used
        False
    """

    @classmethod
    def _collection_path(cls):
        return 'tokens'

    @classmethod
    def _instance_path(cls, token_id):
        return ('tokens', token_id)

    @classmethod
    def create(cls, **kwargs):
        """Create a credit card token with the given card details.

        In production environment, the token should be created with
        `Omise.js <https://docs.omise.co/omise-js>`_ and credit card details
        should never go through your server. This method should only be used
        for creating fake data in test mode.

        See the `create a token`_ section in the API documentation for list
        of available arguments.

        Basic usage::

            >>> import omise
            >>> omise.api_public = 'pkey_test_4xs8breq32civvobx15'
            >>> token = omise.Token.create(
            ...     name='Somchai Prasert',
            ...     number='4242424242424242',
            ...     expiration_month=10,
            ...     expiration_year=2018,
            ...     city='Bangkok',
            ...     postal_code='10320',
            ...     security_code=123
            ... )
            <Token id='tokn_test_4xs9408a642a1htto8z' at 0x7f406b384990>

        .. _create a token: https://docs.omise.co/api/tokens/#create-a-token

        :param \*\*kwargs: arguments to create a token.
        :rtype: Token
        """
        transformed_args = dict(card=kwargs)
        return _as_object(
            cls._request('post',
                         cls._collection_path(),
                         transformed_args))

    @classmethod
    def retrieve(cls, token_id):
        """Retrieve the token details for the given :param:`token_id`.

        :param token_id: a token id to retrieve.
        :type token_id: str
        :rtype: Token
        """
        return _as_object(cls._request('get', cls._instance_path(token_id)))

    def reload(self):
        """Reload the token details.

        :rtype: Token
        """
        return self._reload_data(
            self._request('get',
                          self._instance_path(self._attributes['id'])))


class Card(_MainResource, Base):
    """API class representing card details.

    This API class represents a card information returned from other APIs.
    Cards are not created directly with this class, but instead created with
    :class:`Token`.

    Basic usage::

        >>> import omise
        >>> omise.api_secret = 'skey_test_4xsjvwfnvb2g0l81sjz'
        >>> customer = omise.Customer.retrieve('cust_test_4xsjvylia03ur542vn6')
        >>> card = customer.cards.retrieve('card_test_4xsjw0t21xaxnuzi9gs')
        <Card id='card_test_4xsjw0t21xaxnuzi9gs' at 0x7f406b384ab8>
        >>> card.last_digits
        '4242'
    """

    @classmethod
    def _collection_path(cls):
        return 'cards'

    @classmethod
    def _instance_path(cls, customer_id, card_id):
        return ('customers', customer_id, 'cards', card_id)

    @classmethod
    def retrieve(cls, customer_id, card_id):
        """Retrieve the card details for the given :param:`card_id`.

        :param customer_id: a customer id of card id.
        :type customer_id: str
        :param card_id: a card id to retrieve.
        :type card_id: str
        :rtype: Card
        """
        return _as_object(cls._request('get', cls._instance_path(customer_id, card_id)))

    def reload(self):
        """Reload the card details.

        :rtype: Card
        """
        return self._reload_data(
            self._request('get',
                          self._attributes['location']))

    def update(self, **kwargs):
        """Update the card information with the given card details.

        See the `update a card`_ section in the API documentation for list
        of available arguments.

        Basic usage::

            >>> import omise
            >>> omise.api_secret = 'skey_test_4xsjvwfnvb2g0l81sjz'
            >>> cust = omise.Customer.retrieve('cust_test_4xsjvylia03ur542vn6')
            >>> card = cust.cards.retrieve('card_test_4xsjw0t21xaxnuzi9gs')
            >>> card.update(
            ...     expiration_month=11,
            ...     expiration_year=2017,
            ...     name='Somchai Praset',
            ...     postal_code='10310'
            ... )
            <Card id='card_test_4xsjw0t21xaxnuzi9gs' at 0x7f7911746ab8>

        :param \*\*kwargs: arguments to update a card.
        :rtype: Card

        .. _update a card: https://docs.omise.co/api/cards/#update-a-card
        """
        changed = copy.deepcopy(self.changes)
        changed.update(kwargs)
        return self._reload_data(
            self._request('patch',
                          self._attributes['location'],
                          changed))

    def destroy(self):
        """Delete the card and unassociated it from the customer.

        Basic usage::

            >>> import omise
            >>> omise.api_secret = 'skey_test_4xsjvwfnvb2g0l81sjz'
            >>> cust = omise.Customer.retrieve('cust_test_4xsjvylia03ur542vn6')
            >>> card = cust.cards.retrieve('card_test_4xsjw0t21xaxnuzi9gs')
            >>> card.destroy()
            <Card id='card_test_4xsjw0t21xaxnuzi9gs' at 0x7f7911746868>
            >>> card.destroyed
            True

        :rtype: Card
        """
        return self._reload_data(
            self._request('delete',
                          self._attributes['location']))

    @property
    def destroyed(self):
        """Returns ``True`` if card has been deleted.

        :rtype: bool
        """
        return self._attributes.get('deleted', False)


class Chain(_MainResource, Base):
    """API class representing chain details.

    This API class is used for retrieving and revoking chains. Chains represent
    sub-merchant accounts which have authorized another account to create
    charges and perform other actions on their behalf.

    Basic usage::

        >>> import omise
        >>> omise.api_secret = 'skey_test_4xs8breq3htbkj03d2x'
        >>> chain = omise.Chain.retrieve('acch_test_5lals6ot3vlz6lsnfhn')
        <Chain id='acch_test_5lals6ot3vlz6lsnfhn' at 0x7fd6689af450>
        >>> chain.email
        'john.doe@example.com'
    """

    @classmethod
    def _collection_path(cls):
        return 'chains'

    @classmethod
    def _instance_path(cls, chain_id):
        return ('chains', chain_id)

    @classmethod
    def retrieve(cls, chain_id=None):
        """Retrieve the sub-merchant chain details for the given
        :param:`chain_id`. If :param:`chain_id` is not given, all sub-merchant
        chains will be returned instead.

        :param chain_id: (optional) a chain id to retrieve.
        :type chain_id: str
        :rtype: Chain
        """
        if chain_id:
            return _as_object(cls._request('get', cls._instance_path(chain_id)))
        return _as_object(cls._request('get', cls._collection_path()))

    @classmethod
    def list(cls):
        """Return a list of sub-merchant chains belonging to your account.

        :rtype: LazyCollection
        """
        return LazyCollection(cls._collection_path())

    def reload(self):
        """Reload the sub-merchant chain details.

        :rtype: Chain
        """
        return self._reload_data(
            self._request('get',
                          self._instance_path(self._attributes['id'])))

    def revoke(self):
        """Revoke the sub-merchant chain.

        Basic usage::

            >>> import omise
            >>> omise.api_secret = 'skey_test_4xs8breq3htbkj03d2x'
            >>> chain = omise.Chain.retrieve('acch_test_5lals6ot3vlz6lsnfhn')
            >>> chain.revoke()
            <Chain id='acch_test_5lals6ot3vlz6lsnfhn' at 0x7f9c60abdc90>
            >>> chain.revoked
            True

        :rtype: Chain
        """

        path = self._instance_path(self._attributes['id']) + ('revoke',)
        return self._reload_data(self._request('post', path))


class Charge(_MainResource, Base):
    """API class representing a charge.

    This API class is used for retrieving and creating a charge to the
    specific credit card. There are two modes of a charge: authorize and
    capture. Authorize is for holding an amount of a charge in credit card's
    available balance and capture for capturing that authorized amount.

    Basic usage::

        >>> import omise
        >>> omise.api_secret = 'skey_test_4xsjvwfnvb2g0l81sjz'
        >>> charge = omise.Charge.retrieve('chrg_test_4xso2s8ivdej29pqnhz')
        <Charge id='chrg_test_4xso2s8ivdej29pqnhz' at 0x7fed3241b990>
        >>> charge.amount
        100000
    """

    @classmethod
    def _collection_path(cls):
        return 'charges'

    @classmethod
    def _instance_path(cls, charge_id):
        return ('charges', charge_id)

    @classmethod
    def create(cls, **kwargs):
        """Create a charge to the given card details.

        See the `create a charge`_ section in the API documentation for list
        of available arguments.

        Basic usage::

            >>> import omise
            >>> omise.api_secret = 'skey_test_4xsjvwfnvb2g0l81sjz'
            >>> charge = omise.Charge.create(
            ...     amount=100000,
            ...     currency='thb',
            ...     description='Order-384',
            ...     ip='127.0.0.1',
            ...     card='tokn_test_4xs9408a642a1htto8z',
            ... )
            <Charge id='chrg_test_4xso2s8ivdej29pqnhz' at 0x7fed3241b868>

        .. _create a charge: https://docs.omise.co/api/charges/#create-a-charge

        :param \*\*kwargs: arguments to create a charge.
        :rtype: Charge
        """
        return _as_object(
            cls._request('post',
                         cls._collection_path(),
                         kwargs))

    @classmethod
    def retrieve(cls, charge_id=None):
        """Retrieve the charge details for the given :param:`charge_id`.

        :param charge_id: a charge id to retrieve.
        :type charge_id: str
        :rtype: Charge
        """
        if charge_id:
            return _as_object(
                cls._request('get',
                             cls._instance_path(charge_id)))
        return _as_object(cls._request('get', cls._collection_path()))

    @classmethod
    def list(cls):
        """Return all charges that belongs to your account

        :rtype: LazyCollection
        """
        return LazyCollection(cls._collection_path())

    def reload(self):
        """Reload the charge details.

        :rtype: Charge
        """
        return self._reload_data(
            self._request('get',
                          self._instance_path(self._attributes['id'])))

    def update(self, **kwargs):
        """Update the charge details with the given arguments.

        See the `update a charge`_ section in the API documentation for list
        of available arguments.

        Basic usage::

            >>> import omise
            >>> omise.api_secret = 'skey_test_4xsjvwfnvb2g0l81sjz'
            >>> charge = omise.Charge.retrieve('chrg_test_4xso2s8ivdej29pqnhz')
            >>> charge.update(description='Another description')
            <Charge id='chrg_test_4xso2s8ivdej29pqnhz' at 0x7fed3241bab8>

        :param \*\*kwargs: arguments to update a charge.
        :rtype: Charge

        .. _update a charge: https://docs.omise.co/api/charges/#update-a-charge
        """
        changed = copy.deepcopy(self.changes)
        changed.update(kwargs)
        return self._reload_data(
            self._request('patch',
                          self._instance_path(self._attributes['id']),
                          changed))

    def capture(self):
        """Capture an authorized charge.

        :rtype: Charge
        """
        path = self._instance_path(self._attributes['id']) + ('capture',)
        return self._reload_data(self._request('post', path))

    def reverse(self):
        """Reverse an uncaptured charge.

        :rtype: Charge
        """
        path = self._instance_path(self._attributes['id']) + ('reverse',)
        return self._reload_data(self._request('post', path))

    def expire(self):
        """Set a charge that has not yet been authorized to expire. Supported
        payment method: Alipay (Barcode)
        
        :rtype: Charge
        """
        path = self._instance_path(self._attributes['id']) + ('expire',)
        return self._reload_data(self._request('post', path))

    def refund(self, **kwargs):
        """Refund a refundable charge.

        See the `create a refund`_ section in the API documentation for list of
        available arguments.

        :rtype: Refund

        .. _create a refund: https://docs.omise.co/api/refunds/#create-a-refund
        """
        path = self._instance_path(self._attributes['id']) + ('refunds',)
        refund = _as_object(self._request('post', path, kwargs))
        self.reload()
        return refund

    def list_refunds(self):
        """Return all refunds that belong to the charge

        :rtype: LazyCollection
        """
        return LazyCollection(self._nested_object_path(Refund))

    def list_events(self):
        """Return all events that belong to the charge

        :rtype: LazyCollection
        """
        return LazyCollection(self._nested_object_path(Event))

    @classmethod
    def schedule(cls):
        """Retrieve all charge schedules.

        :rtype: Schedule

        .. _retrieve all charge schedules:
        https://docs.omise.co/charge-schedules-api
        """
        return _as_object(
            cls._request('get',
                         ('charges', 'schedules',)))


class Collection(Base):
    """Proxy class representing a collection of items."""

    def __len__(self):
        return len(self._attributes['data'])

    def __iter__(self):
        for obj in self._attributes['data']:
            yield _as_object(obj)

    def __getitem__(self, item):
        return _as_object(self._attributes['data'][item])

    def retrieve(self, object_id=None):
        """Retrieve the specific :param:`object_id` from the list of objects.

        If no :param:`object_id` is given, a list of all objects will be
        returned instead. This is equivalent of calling ``list(collection)``.

        :param object_id: an object id to retrieve.
        :type object_id: str
        :rtype: T <= Base
        """
        if object_id is None:
            return list(self)
        else:
            for obj in self._attributes['data']:
                if obj['id'] == object_id:
                    return _as_object(obj)


class Customer(_MainResource, Base):
    """API class representing a customer in an account.

    This API class is used for retrieving and creating a customer in an
    account. The customer can be used for storing credit card details
    (using token) for later use.

    Basic usage::

        >>> import omise
        >>> omise.api_secret = 'skey_test_4xsjvwfnvb2g0l81sjz'
        >>> customer = omise.Customer.retrieve('cust_test_4xtrb759599jsxlhkrb')
        <Customer id='cust_test_4xtrb759599jsxlhkrb' at 0x7fb02625f990>
        >>> customer.email
        'john.doe@example.com'
    """

    @classmethod
    def _collection_path(cls):
        return 'customers'

    @classmethod
    def list(cls):
        """Return all customers that belongs to your account

        :rtype: LazyCollection
        """
        return LazyCollection(cls._collection_path())

    @classmethod
    def _instance_path(cls, customer_id):
        return ('customers', customer_id)

    @classmethod
    def create(cls, **kwargs):
        """Create a customer with the given card token.

        See the `create a customer`_ section in the API documentation for list
        of available arguments.

        Basic usage::

            >>> import omise
            >>> omise.api_secret = 'skey_test_4xsjvwfnvb2g0l81sjz'
            >>> customer = omise.Customer.create(
            ...     description='John Doe (id: 30)',
            ...     email='john.doe@example.com',
            ...     card='tokn_test_4xs9408a642a1htto8z',
            ... )
            <Customer id='cust_test_4xtrb759599jsxlhkrb' at 0x7fb02625fab8>

        .. _create a customer:
        ..     https://docs.omise.co/api/customers/#create-a-customer

        :param \*\*kwargs: arguments to create a customer.
        :rtype: Customer
        """
        return _as_object(
            cls._request('post',
                         cls._collection_path(),
                         kwargs))

    @classmethod
    def retrieve(cls, customer_id=None):
        """Retrieve the customer details for the given :param:`customer_id`.

        :param customer_id: a customer id to retrieve.
        :type customer_id: str
        :rtype: Customer
        """
        if customer_id:
            return _as_object(
                cls._request('get',
                             cls._instance_path(customer_id)))
        return _as_object(cls._request('get', cls._collection_path()))

    def reload(self):
        """Reload the customer details.

        :rtype: Customer
        """
        return self._reload_data(
            self._request('get',
                          self._instance_path(self._attributes['id'])))

    def update(self, **kwargs):
        """Update the customer details with the given arguments.

        See the `update a customer`_ section in the API documentation for list
        of available arguments.

        Basic usage::

            >>> import omise
            >>> omise.api_secret = 'skey_test_4xsjvwfnvb2g0l81sjzx'
            >>> cust = omise.Customer.retrieve('cust_test_4xtrb759599jsxlhkrb')
            >>> cust.update(
            ...     email='john.smith@example.com',
            ...     description='Another description',
            ... )
            <Customer id='cust_test_4xtrb759599jsxlhkrb' at 0x7f319de7f990>

        :param \*\*kwargs: arguments to update a customer.
        :rtype: Customer

        .. _update a customer:
        ..     https://docs.omise.co/api/customers/#update-a-customer
        """
        changed = copy.deepcopy(self.changes)
        changed.update(kwargs)
        return self._reload_data(
            self._request('patch',
                          self._instance_path(self._attributes['id']),
                          changed))

    def destroy(self):
        """Delete the customer from the server.

        Basic usage::

            >>> import omise
            >>> omise.api_secret = 'skey_test_4xsjvwfnvb2g0l81sjzx'
            >>> cust = omise.Customer.retrieve('cust_test_4xtrb759599jsxlhkrb')
            >>> cust.destroy()
            <Customer id='cust_test_4xtrb759599jsxlhkrb' at 0x7ff72d8d1990>
            >>> cust.destroyed
            True

        :rtype: Customer
        """
        return self._reload_data(
            self._request('delete',
                          self._instance_path(self._attributes['id'])))

    def list_cards(self):
        """Returns all cards that belong to a given customer.

        :rtype: LazyCollection
        """
        return LazyCollection(self._nested_object_path(Card))

    def list_schedules(self):
        """Returns all charge schedules that belong to a given customer.

        :rtype: LazyCollection
        """
        return LazyCollection(self._nested_object_path(Schedule))

    @property
    def destroyed(self):
        """Returns ``True`` if customer has been deleted.

        :rtype: bool
        """
        return self._attributes.get('deleted', False)

    def schedule(self):
        """Retrieve all charge schedules that belong to customer.

        :rtype: Schedule

        .. _retrieve all charge schedules for a given customer:
        https://docs.omise.co/charge-schedules-api
        """
        path = self._instance_path(self._attributes['id']) + ('schedules',)
        schedules = _as_object(self._request('get', path))
        return schedules


class LazyCollection(object):
    """Proxy class representing a lazy collection of items."""
    def __init__(self, collection_path):
        self.collection_path = collection_path
        self._exhausted = False

    def __len__(self):
        return self._fetch_objects(limit=1, offset=0)['total']

    def __iter__(self):
        self.limit = 100
        self.listing = collections.deque([])
        self._total_data_length = 0

        return self

    def __next__(self):
        if (self.listing is None) or len(self.listing) == 0:
            self._next_batch(limit=self.limit, offset=self._total_data_length)

        self._total_data_length += 1
        return _as_object(self.listing.popleft())

    def next(self):
        return self.__next__()

    def offset(self, **kwargs):
        limit = kwargs.pop('limit', 20)
        offset = kwargs.pop('offset', 0)
        order = kwargs.pop('order', None)

        obj = self._fetch_objects(limit=limit, offset=offset, order=order)
        data = obj['data']

        return [_as_object(item) for item in data]

    def _next_batch(self, **kwargs):
        if self._exhausted:
            raise StopIteration

        obj = self._fetch_objects(limit=kwargs['limit'], offset=kwargs['offset'])
        data = obj['data']

        if len(data) > 0:
            self._update_listing(data)
        else:
            raise StopIteration

    def _update_listing(self, data):
        self.listing.extend(data)

        if len(data) < self.limit:
            self._exhausted = True

    def _fetch_objects(self, **kwargs):
        order = kwargs.pop('order', None)

        return Request(api_secret, api_main, api_version).send(
            'get',
            self.collection_path,
            payload={
                'limit': kwargs['limit'],
                'offset': kwargs['offset'],
                'order': order
            }
        )


class Dispute(_MainResource, Base):
    """API class representing a dispute in an account.

    This API class is used for retrieving and updating a dispute in an
    account for charge back handling.

    Basic usage::

        >>> import omise
        >>> omise.api_secret = 'skey_test_4xs8breq3htbkj03d2x'
        >>> dispute = omise.Dispute.retrieve('dspt_test_4zgf15h89w8t775kcm8')
        <Dispute id='dspt_test_4zgf15h89w8t775kcm8' at 0x7fd06ce3d5d0>
        >>> dispute.status
        'open'
    """

    @classmethod
    def _collection_path(cls, status=None):
        if status:
            return ('disputes', status)
        return 'disputes'

    @classmethod
    def _instance_path(cls, dispute_id):
        return ('disputes', dispute_id)

    @classmethod
    def retrieve(cls, *args, **kwargs):
        if len(args) > 0:
            return _as_object(cls._request('get', cls._instance_path(args[0])))
        elif 'status' in kwargs:
            return _as_object(
                cls._request('get',
                             cls._collection_path(kwargs['status'])))
        return _as_object(cls._request('get', cls._collection_path()))

    @classmethod
    def list(cls):
        """Return all disputes that belongs to your account

        :rtype: LazyCollection
        """
        return LazyCollection(cls._collection_path())

    @classmethod
    def list_open_disputes(cls):
        """Return all open disputes that belongs to your account

        :rtype: LazyCollection
        """
        return LazyCollection(cls._collection_path("open"))

    @classmethod
    def list_pending_disputes(cls):
        """Return all pending disputes that belongs to your account

        :rtype: LazyCollection
        """
        return LazyCollection(cls._collection_path("pending"))

    @classmethod
    def list_closed_disputes(cls):
        """Return all closed disputes that belongs to your account

        :rtype: LazyCollection
        """
        return LazyCollection(cls._collection_path("closed"))

    def list_documents(self):
        """Returns all documents that belong to a given dispute.

        :rtype: LazyCollection
        """
        return LazyCollection(self._nested_object_path(Document))

    def reload(self):
        """Reload the dispute details.

        :rtype: Dispute
        """
        return self._reload_data(
            self._request('get',
                          self._instance_path(self._attributes['id'])))

    def update(self, **kwargs):
        """Update the dispute details with the given arguments.

        See the `update a dispute`_ section in the API documentation for list
        of available arguments.

        Basic usage::

            >>> import omise
            >>> omise.api_secret = 'skey_test_4xs8breq3htbkj03d2x'
            >>> dspt = omise.Dispute.retrieve('dspt_test_4zgf15h89w8t775kcm8')
            >>> dspt.update(message='Proofs and other information')
            <Dispute id='dspt_test_4zgf15h89w8t775kcm8' at 0x7fd06cd56210>

        :param \*\*kwargs: arguments to update a dispute.
        :rtype: Recipient

        .. _update a dispute:
        ..     https://docs.omise.co/api/recipients/#disputes-update
        """
        changed = copy.deepcopy(self.changes)
        changed.update(kwargs)
        return self._reload_data(
            self._request('patch',
                          self._instance_path(self._attributes['id']),
                          changed))

    def accept(self):
        """Accept the dispute.

        Basic usage::

            >>> import omise
            >>> omise.api_secret = 'skey_test_4xs8breq3htbkj03d2x'
            >>> dspt = omise.Dispute.retrieve('dspt_test_5mr57xawhq7j28az3ak')
            >>> dspt.status
            'open'
            >>> dspt.accept()
            <Dispute id='dspt_test_5mr57xawhq7j28az3ak' at 0x7ff4fcabddd0>
            >>> dspt.status
            'lost'

        :rtype: Dispute
        """
        path = self._instance_path(self._attributes['id']) + ('accept',)
        return self._reload_data(self._request('patch', path))

    def upload_document(self, document):
        """Add a dispute evidence document.

        See the `create a document`_ section in the API documentation for list
        of available arguments.

        :rtype: Document

        .. _create a document: https://www.omise.co/documents-api#create
        """
        path = self._instance_path(self._attributes['id']) + ('documents',)
        document = _as_object(self._upload('post', path, files=document))
        self.reload()
        return document


class Document(_MainResource, Base):
    """API class representing a dispute document in an account.

    This API class is used for managing dispute document files. Documents are
    used to help resolve disputes. Supported file types include PNG, JPG, and
    PDF.

    Basic usage::

        >>> import omise
        >>> omise.api_secret = 'skey_test_4xs8breq3htbkj03d2x'
        >>> dispute = omise.Dispute.retrieve('dspt_test_5mr4ox8e818viqtaqs1')
        >>> document = dispute.documents.retrieve("docu_test_5mr4oyqphijal1ps9u6")
        <Document id='docu_test_5mr4oyqphijal1ps9u6' at 0x7ffdbb90d410>
        >>> document.filename
        'evidence.png'
    """

    @classmethod
    def _collection_path(cls):
        return 'documents'

    @classmethod
    def _instance_path(cls, dispute_id, document_id):
        return ('disputes', dispute_id, 'documents', document_id)

    @classmethod
    def retrieve(cls, dispute_id, document_id):
        """Retrieve the document details for the given :param:`document_id`.

        :param dispute_id: a dispute id of a document.
        :type dispute_id: str
        :param document_id: a document id to retrieve.
        :type document_id: str
        :rtype: Document
        """
        return _as_object(cls._request('get', cls._instance_path(dispute_id, document_id)))

    def reload(self):
        """Reload the document details.

        :rtype: Document
        """
        return self._reload_data(
            self._request('get',
                          self._attributes['location']))

    def destroy(self):
        """Delete the document and unassociated it from the dispute.

        Basic usage::

            >>> import omise
            >>> omise.api_secret = 'skey_test_4xs8breq3htbkj03d2x'
            >>> dispute = omise.Dispute.retrieve('dspt_test_5mr4ox8e818viqtaqs1')
            >>> document = dispute.documents.retrieve("docu_test_5mr4oyqphijal1ps9u6")
            >>> document.destroy()
            <Document id='docu_test_5mr4oyqphijal1ps9u6' at 0x7ffdbb90d410>
            >>> document.destroyed
            True

        :rtype: Document
        """
        return self._reload_data(
            self._request('delete',
                          self._attributes['location']))

    @property
    def destroyed(self):
        """Returns ``True`` if document has been deleted.

        :rtype: bool
        """
        return self._attributes.get('deleted', False)


class Event(_MainResource, Base):
    """API class representing an event in an account.

    This API class is used for retrieving an event in an
    account. The event represents event object from webhooks.

    Basic usage::

        >>> import omise
        >>> omise.api_secret = 'skey_test_4xs8breq3htbkj03d2x'
        >>> event = omise.Event.retrieve('evnt_test_5086xmr74vxs0ajpo78')
        <Event id='evnt_test_5086xmr74vxs0ajpo78' at 0x7f79c41e9eb8>
        >>> event.key
        'charge.create'
    """

    @classmethod
    def _collection_path(cls):
        return 'events'

    @classmethod
    def _instance_path(cls, event_id):
        return ('events', event_id)

    @classmethod
    def retrieve(cls, event_id=None):
        """Retrieve the event details for the given :param:`event_id`.
        If :param:`event_id` is not given, all events will be returned
        instead.

        :param event_id: (optional) an event id to retrieve.
        :type event_id: str
        :rtype: Event
        """
        if event_id:
            return _as_object(cls._request('get', cls._instance_path(event_id)))
        return _as_object(cls._request('get', cls._collection_path()))

    @classmethod
    def list(cls):
        """Return all events that belongs to your account

        :rtype: LazyCollection
        """
        return LazyCollection(cls._collection_path())

    def reload(self):
        """Reload the event details.

        :rtype: Event
        """
        return self._reload_data(
            self._request('get',
                          self._instance_path(self._attributes['id'])))


class Forex(_MainResource, Base):
    """API class retrieves the currency exchange.

    The Forex API retrieves the currency exchange rate used in
    conversions for multi-currency transactions based on account's PSP.

    Basic usage::

        >>> import omise
        >>> omise.api_secret = 'skey_test_4xs8breq3htbkj03d2x'
        >>> forex = omise.Forex.retrieve('usd')
        <Forex at 0x10bd794e0>
        >>> forex.rate
        32.747069
    """

    @classmethod
    def retrieve(cls, currency):
        """Retrieve the exchange rate for the given :param:`currency`.

        :param currency: a currency to exchange.
        :type currency: str
        :rtype: Forex
        """
        return _as_object(
            cls._request('get', ('forex', currency)))


class Link(_MainResource, Base):
    """API class representing a link.

    This API class is used for retrieving and creating a link.
    The link can be used for creating a charge for once or multiple times.

    Basic usage::

        >>> import omise
        >>> omise.api_secret = 'skey_test_4xs8breq3htbkj03d2x'
        >>> link = omise.Link.retrieve('link_test_5086xmr74vxs0ajpo78')
        <Link id='link_test_5086xmr74vxs0ajpo78' at 0x7f79c41e9eb8>
        >>> link.amount
        10000
    """

    @classmethod
    def _collection_path(cls):
        return 'links'

    @classmethod
    def _instance_path(cls, link_id):
        return ('links', link_id)

    @classmethod
    def create(cls, **kwargs):
        """Create a link for creating charge once or multiple times.

        See the `create a link`_ section in the API documentation for list
        of available arguments.

        Basic usage::

            >>> import omise
            >>> omise.api_secret = 'skey_test_4xsjvwfnvb2g0l81sjz'
            >>> link = omise.Link.create(
            ...     amount=100000,
            ...     currency='thb',
            ...     description='Description of order-384',
            ...     title='Order-384',
            ... )
            <Link id='link_test_4xso2s8ivdej29pqnhz' at 0x7fed3241b868>

        .. _create a link: https://docs.omise.co/links-api/#create-a-link

        :param \*\*kwargs: arguments to create a link.
        :rtype: Link
        """
        return _as_object(
            cls._request('post',
                         cls._collection_path(),
                         kwargs))

    @classmethod
    def retrieve(cls, link_id=None):
        """Retrieve the link details for the given :param:`link_id`.

        :param link_id: a link id to retrieve.
        :type link_id: str
        :rtype: Link
        """
        if link_id:
            return _as_object(
                cls._request('get',
                             cls._instance_path(link_id)))
        return _as_object(cls._request('get', cls._collection_path()))

    @classmethod
    def list(cls):
        """Return all links that belongs to your account.

        :rtype: LazyCollection
        """
        return LazyCollection(cls._collection_path())

    def reload(self):
        """Reload the link details.

        :rtype: Link
        """
        return self._reload_data(
            self._request('get',
                          self._instance_path(self._attributes['id'])))

    def destroy(self):
        """Delete the link from the server.

        Basic usage::

            >>> import omise
            >>> omise.api_secret = 'skey_test_4xsjvwfnvb2g0l81sjz'
            >>> link = omise.Link.retrieve('link_test_5dsoxxan7gxrqihu8rs')
            >>> link.destroy()
            <Link id='link_test_5dsoxxan7gxrqihu8rs' at 0x7fcc349bdd90>
            >>> link.destroyed
            True

        :rtype: Link
        """
        return self._reload_data(
            self._request('delete',
                          self._instance_path(self.id)))

    @property
    def destroyed(self):
        """Returns ``True`` if the link has been deleted.

        :rtype: bool
        """
        return self._attributes.get('deleted', False)


class Occurrence(_MainResource, Base):
    """API class representing occurrence information.

    This API class is used for retrieving a individual occurrence.

    Basic usage::

        >>> import omise
        >>> omise.api_secret = 'skey_test_4xsjvwfnvb2g0l81sjz'
        >>> occurrence = omise.Occurrence.retrieve('occu_test_587bugap9mm42nuddig')
        <Occurrence id='occu_test_587bugap9mm42nuddig' at 0x1063b1f98>
    """

    @classmethod
    def _instance_path(cls, occurrence_id):
        return ('occurrences', occurrence_id)

    @classmethod
    def retrieve(cls, occurrence_id):
        """Retrieve the occurrence details for the given :param:`occurrence_id`.

        :param occurrence_id: a occurrence id to retrieve.
        :type occurrence_id: str
        :rtype: Occurrence
        """
        return _as_object(
            cls._request('get',
                         cls._instance_path(occurrence_id)))


class Receipt(_MainResource, Base):
    @classmethod
    def _collection_path(cls):
        return 'receipts'

    @classmethod
    def _instance_path(cls, receipt_id):
        return ('receipts', receipt_id)

    @classmethod
    def retrieve(cls, receipt_id=None):
        """Retrieve the receipt details for the given :param:`receipt_id`.

        :param receipt_id: a receipt id to retrieve.
        :type receipt_id: str
        :rtype: Receipt
        """
        if receipt_id:
            return _as_object(
                cls._request('get',
                             cls._instance_path(receipt_id)))
        return _as_object(cls._request('get', cls._collection_path()))

    @classmethod
    def list(cls):
        """Return all receipts that belongs to your account.

        :rtype: LazyCollection
        """
        return LazyCollection(cls._collection_path())


class Recipient(_MainResource, Base):
    """API class representing a recipient in an account.

    This API class is used for retrieving and creating a recipient in an
    account. The recipient can be used to transfer the balance to specific
    bank accounts.

    Basic usage::

        >>> import omise
        >>> omise.api_secret = 'skey_test_4xs8breq3htbkj03d2x'
        >>> recipient = omise.Recipient.retrieve('recp_test_5086xmr74vxs0ajpo78')
        <Recipient id='recp_test_5086xmr74vxs0ajpo78' at 0x7f79c41e9eb8>
        >>> recipient.name
        'Foobar Baz'
    """

    @classmethod
    def _collection_path(cls):
        return 'recipients'

    @classmethod
    def _instance_path(cls, recipient_id):
        return ('recipients', recipient_id)

    @classmethod
    def create(cls, **kwargs):
        """Create a recipient with the given parameters.

        See the `create a recipient`_ section in the API documentation for list
        of available arguments.

        Basic usage::

            >>> import omise
            >>> omise.api_secret = 'skey_test_4xsjvwfnvb2g0l81sjz'
            >>> customer = omise.Recipient.create(
            ...     name='Somchai Prasert',
            ...     email='somchai.prasert@example.com',
            ...     type='individual',
            ...     bank_account=dict(
            ...       brand='bbl',
            ...       number='1234567890',
            ...       name='SOMCHAI PRASERT'
            ...     )
            ... )
            <Recipient id='recp_test_5086xmr74vxs0ajpo78' at 0x7f79c41e9e90>

        .. _create a recipient:
        ..     https://docs.omise.co/api/recipients/#recipients-create

        :param \*\*kwargs: arguments to create a recipient.
        :rtype: Recipient
        """
        return _as_object(
            cls._request('post',
                         cls._collection_path(),
                         kwargs))

    @classmethod
    def retrieve(cls, recipient_id=None):
        """Retrieve the recipient details for the given :param:`recipient_id`.
        If :param:`recipient_id` is not given, all recipients will be returned
        instead.

        :param recipient_id: (optional) a recipient id to retrieve.
        :type recipient_id: str
        :rtype: Recipient
        """
        if recipient_id:
            return _as_object(cls._request('get',
                                           cls._instance_path(recipient_id)))
        return _as_object(cls._request('get', cls._collection_path()))

    @classmethod
    def list(cls):
        """Return all recipients that belongs to your account

        :rtype: LazyCollection
        """
        return LazyCollection(cls._collection_path())

    def reload(self):
        """Reload the recipient details.

        :rtype: Recipient
        """
        return self._reload_data(
            self._request('get',
                          self._instance_path(self._attributes['id'])))

    def update(self, **kwargs):
        """Update the recipient details with the given arguments.

        See the `update a recipient`_ section in the API documentation for list
        of available arguments.

        Basic usage::

            >>> import omise
            >>> omise.api_secret = 'skey_test_4xsjvwfnvb2g0l81sjz'
            >>> recp = omise.Recipient.retrieve('recp_test_5086xmr74vxs0ajpo78')
            >>> recp.update(
            ...     email='somchai@prasert.com',
            ...     bank_account=dict(
            ...       brand='kbank',
            ...       number='1234567890',
            ...       name='SOMCHAI PRASERT'
            ...     )
            ... )
            <Recipient id='recp_test_5086xmr74vxs0ajpo78' at 0x7f79c41e9d00>

        :param \*\*kwargs: arguments to update a recipient.
        :rtype: Recipient

        .. _update a recipient:
        ..     https://docs.omise.co/api/recipients/#recipients-update
        """
        changed = copy.deepcopy(self.changes)
        changed.update(kwargs)
        return self._reload_data(
            self._request('patch',
                          self._instance_path(self._attributes['id']),
                          changed))

    def destroy(self):
        """Delete the recipient from the server.

        Basic usage::

            >>> import omise
            >>> omise.api_secret = 'skey_test_4xsjvwfnvb2g0l81sjz'
            >>> recp = omise.Recipient.retrieve('recp_test_5086xmr74vxs0ajpo78')
            >>> recp.destroy()
            <Recipient id='recp_test_5086xmr74vxs0ajpo78' at 0x7f775ff01c60>
            >>> recp.destroyed
            True

        :rtype: Recipient
        """
        return self._reload_data(
            self._request('delete',
                          self._instance_path(self.id)))

    @property
    def destroyed(self):
        """Returns ``True`` if the recipient has been deleted.

        :rtype: bool
        """
        return self._attributes.get('deleted', False)


class Refund(_MainResource, Base):
    """API class representing refund information.

    This API class represents a refund information returned from the refund API.
    Refunds are not created directly with this class, but instead can be created
    using :meth:`Charge.refund`.

    Basic usage::

        >>> import omise
        >>> omise.api_secret = 'skey_test_4xsjvwfnvb2g0l81sjz'
        >>> charge = omise.Charge.retrieve('chrg_test_4xso2s8ivdej29pqnhz')
        >>> refund = charge.refunds.retrieve('rfnd_test_4ypcvo03ktuw0uki7un')
        <Refund id='rfnd_test_4ypcvo03ktuw0uki7un' at 0x7fd6095096f8>
        >>> refund.amount
        10000
    """

    @classmethod
    def list(cls):
        """Return all refunds that belongs to your account.

        :rtype: LazyCollection
        """
        return LazyCollection(cls._collection_path())

    @classmethod
    def _collection_path(cls):
        return 'refunds'

    def reload(self):
        """Reload the refund details.

        :rtype: Refund
        """
        return self._reload_data(
            self._request('get',
                          self._attributes['location']))


class Search(_MainResource, Base):
    """API class for searching.

    This API class is used for retrieving results from your account.
    Currently, Search API is supported to search only Charge, Dispute,
    Recipient and Customer.

    Basic usage::

        >>> import omise
        >>> omise.api_secret = 'skey_test_4xsjvwfnvb2g0l81sjz'
        >>> search = omise.Search.execute('charge', **{
            'query': 'thb',
            'filters': {
                'amount': '1000..2000',
                'captured': 'true'
            }
        })
        <Search at 0x1029e57f0>
        >>> search[0]
        <Charge id='chrg_test_58505fmz8hbaln3283s' at 0x10291edd8>
    """

    def __len__(self):
        return len(self._attributes['data'])

    def __iter__(self):
        for obj in self._attributes['data']:
            yield _as_object(obj)

    def __getitem__(self, item):
        return _as_object(self._attributes['data'][item])

    @classmethod
    def execute(cls, scope, **options):
        querystring = ['?scope=%s' % scope]

        for key, val in options.items():
            if isinstance(val, dict):
                for k, v in val.items():
                    querystring.append('%s[%s]=%s' % (key, k, v))
            else:
                querystring.append('%s=%s' % (key, val))

        return _as_object(
            cls._request('get',
                         ('search', '&'.join(querystring))))


class Schedule(_MainResource, Base):
    """API class representing schedule information.

    This API class is used for retrieving or creating or deleting a scheduled
    charge.

    Basic usage::

        >>> import omise
        >>> omise.api_secret = 'skey_test_4xsjvwfnvb2g0l81sjz'
        >>> schedule = omise.Schedule.retrieve('schd_test_4xso2s8ivdej29pqnhz')
        <Schedule id='schd_test_58509af8d7nf901pf91' at 0x1063b1f98>
    """

    @classmethod
    def _collection_path(cls):
        return 'schedules'

    @classmethod
    def _instance_path(cls, schedule_id):
        return ('schedules', schedule_id)

    @classmethod
    def create(cls, **kwargs):
        """Create a schedule charge object to
        the bank account.

        See the `create a schedule`_ section in the API documentation for list
        of available arguments.

        Basic usage::

            >>> import omise
            >>> omise.api_secret = 'skey_test_4xsjvwfnvb2g0l81sjz'
            >>> schedule = omise.Schedule.create(
                every=1,
                period='month',
                on={
                    'weekday_of_month': 'second_monday'
                },
                end_date='2018-05-01',
                charge={
                    'customer': 'cust_test_58505eu8s3szip5tzk8',
                    'amount': 100000,
                    'description': 'Membership fee'
                }
            )
            <Schedule id='schd_test_5851n56mg0rg90gvphj' at 0x1031d34e0>

        .. _create a schedule:
        ..     https://docs.omise.co/schedules-api#create-a-schedule

        :param \*\*kwargs: arguments to create a schedule.
        :rtype: Schedule
        """
        return _as_object(
            cls._request('post',
                         cls._collection_path(),
                         kwargs))

    @classmethod
    def retrieve(cls, schedule_id=None):
        """Retrieve the schedule object for the given :param:`schedule_id`.
        If :param:`schedule_id` is not given, all schedules will be returned
        instead.

        :param schedule_id: (optional) a schedule id to retrieve.
        :type schedule_id: str
        :rtype: Schedule
        """
        if schedule_id:
            return _as_object(
                cls._request('get',
                             cls._instance_path(schedule_id)))

        return _as_object(cls._request('get', cls._collection_path()))

    @classmethod
    def list(cls):
        """Returns all schedules that belongs to your account.

        :rtype: LazyCollection
        """
        return LazyCollection(cls._collection_path())

    def reload(self):
        """Reload the schedule details.

        :rtype: Schedule
        """
        return self._reload_data(
            self._request('get',
                          self._instance_path(self._attributes['id'])))

    def destroy(self):
        """Delete the schedule from the server.

        This method will delete the schedule.

        Basic usage::

            >>> import omise
            >>> omise.api_secret = 'skey_test_4xsjvwfnvb2g0l81sjz'
            >>> schd = omise.Schedule.retrieve('schd_test_5851n56mg0rg90gvphj')
            >>> schd.destroy()
            <Schedule id='schd_test_5851n56mg0rg90gvphj' at 0x1063b1f98>
            >>> schd.destroyed
            True
        :rtype: Schedule
        """
        return self._reload_data(
            self._request('delete',
                          self._instance_path(self.id)))

    @property
    def destroyed(self):
        """Returns ``True`` if the schedule has been deleted.

        :rtype: bool
        """
        status = self._attributes.get('status')
        return status == 'deleted'

    def occurrence(self):
        """Retrieve all occurrences for a given schedule.

        :rtype: Occurrence

        https://docs.omise.co/occurrences-api
        """
        path = self._instance_path(self._attributes['id']) + ('occurrences',)
        occurrences = _as_object(self._request('get', path))
        return occurrences


class Source(_MainResource, Base):
    """API class for creating Source.

    This API class is used for creating a source which are enabled to the
    following payment methods.

    Basic usage::

        >>> import omise
        >>> omise.api_secret = 'skey_test_4xsjvwfnvb2g0l81sjz'
        >>> source = omise.Source.create(
            amount=100000,
            currency='thb',
            type='internet_banking_scb'
        )
        <Source id='src_test_59ldo3ltuz7418db4ol' at 0x106473668>
        >>> charge = omise.Charge.create(
            amount=100000,
            currency='thb',
            source=source.id,
            return_uri='https://www.omise.co'
        )
        <Charge id='chrg_test_4xso2s8ivdej29pqnhz' at 0x7fed3241b990>
        >>> charge.source
        <Source id='src_test_59ldo3ltuz7418db4ol' at 0x1064736a0>

        or

        charge = omise.Charge.create(
            amount=100000,
            currency='thb',
            source={
                'type': 'internet_banking_scb'
            },
            return_uri='https://www.omise.co'
        )
    """

    @classmethod
    def _instance_path(cls, source_id):
        return ('sources', source_id)

    @classmethod
    def create(cls, **kwargs):
        return _as_object(
            cls._request('post',
                         'sources', kwargs))

    @classmethod
    def retrieve(cls, source_id):
        """Retrieve the source details for the given :param:`source_id`.

        :param source_id: a source id to retrieve.
        :type source_id: str
        :rtype: Source
        """
        return _as_object(
            cls._request('get',
                         cls._instance_path(source_id)))

class Transfer(_MainResource, Base):
    """API class representing a transfer.

    This API class is used for retrieving a transfer information and create
    a transfer to the bank account given in account settings. The transfer
    amount must always be less than the current balance.

    Basic usage::

        >>> import omise
        >>> omise.api_secret = 'skey_test_4xsjvwfnvb2g0l81sjz'
        >>> transfer = omise.Transfer.retrieve('trsf_test_4xs5px8c36dsanuwztf')
        <Transfer id='trsf_test_4xs5px8c36dsanuwztf' at 0x7ff72d8d1868>
        >>> transfer.amount
        50000
    """

    @classmethod
    def _collection_path(cls):
        return 'transfers'

    @classmethod
    def _instance_path(cls, transfer_id):
        return ('transfers', transfer_id)

    @classmethod
    def create(cls, **kwargs):
        """Create a transfer to the bank account.

        See the `create a transfer`_ section in the API documentation for list
        of available arguments.

        Basic usage::

            >>> import omise
            >>> omise.api_secret = 'skey_test_4xsjvwfnvb2g0l81sjz'
            >>> transfer = omise.Transfer.create(amount=100000)
            <Transfer id='trsf_test_4y3miv1nhy0dceit4w4' at 0x7f6ef55b0990>

        .. _create a transfer:
        ..     https://docs.omise.co/api/transfers/#create-a-transfer

        :param \*\*kwargs: arguments to create a transfer.
        :rtype: Transfer
        """
        return _as_object(
            cls._request('post',
                         cls._collection_path(),
                         kwargs))

    @classmethod
    def retrieve(cls, transfer_id=None):
        """Retrieve the transfer details for the given :param:`transfer_id`.
        If :param:`transfer_id` is not given, all transfers will be returned
        instead.

        :param transfer_id: (optional) a transfer id to retrieve.
        :type transfer_id: str
        :rtype: Transfer
        """
        if transfer_id:
            return _as_object(
                cls._request('get',
                             cls._instance_path(transfer_id)))
        return _as_object(cls._request('get', cls._collection_path()))

    @classmethod
    def list(cls):
        """Return all transfers that belongs to your account.

        :rtype: LazyCollection
        """
        return LazyCollection(cls._collection_path())

    def reload(self):
        """Reload the transfer details.

        :rtype: Transfer
        """
        return self._reload_data(
            self._request('get',
                          self._instance_path(self._attributes['id'])))

    def update(self, **kwargs):
        """Update the transfers details with the given arguments.

        This method will update the transfer if it is still in the pending
        state (i.e. not sent or paid.) An attempt to update a non-pending
        transfers will result in an error.

        See the `update a transfer`_ section in the API documentation for list
        of available arguments.

        Basic usage::

            >>> import omise
            >>> omise.api_secret = 'skey_test_4xsjvwfnvb2g0l81sjz'
            >>> trsf = omise.Transfer.retrieve('trsf_test_4xs5px8c36dsanuwztf')
            >>> trsf.update(amount=50000)
            <Transfer id='trsf_test_4xs5px8c36dsanuwztf' at 0x7f037c6c9f90>

        :param \*\*kwargs: arguments to update the transfer.
        :rtype: Customer

        .. _update a transfer:
        ..     https://docs.omise.co/api/transfers/#update-a-transfer
        """
        changed = copy.deepcopy(self.changes)
        changed.update(kwargs)
        return self._reload_data(
            self._request('patch',
                          self._instance_path(self.id),
                          changed))

    def destroy(self):
        """Delete the transfer from the server if it is not yet sent.

        This method will cancel the transfer if it is still in the pending
        state (i.e. not sent or paid.) An attempt to delete a non-pending
        transfers will result in an error.

        Basic usage::

            >>> import omise
            >>> omise.api_secret = 'skey_test_4xsjvwfnvb2g0l81sjz'
            >>> trsf = omise.Transfer.retrieve('trsf_test_4y3miv1nhy0dceit4w4')
            >>> trsf.destroy()
            <Transfer id='trsf_test_4y3miv1nhy0dceit4w4' at 0x7f037f8707d0>
            >>> trsf.destroyed
            True

        :rtype: Customer
        """
        return self._reload_data(
            self._request('delete',
                          self._instance_path(self.id)))

    @property
    def destroyed(self):
        """Returns ``True`` if the transfer has been deleted.

        :rtype: bool
        """
        return self._attributes.get('deleted', False)


class Transaction(_MainResource, Base):
    """API class representing a transaction.

    This API class is used for retrieving a transaction information for
    bookkeeping such as that made by :class:`Charge` and :class:`Transfer`
    operations.

    Basic usage::

        >>> import omise
        >>> omise.api_secret = 'skey_test_4xsjvwfnvb2g0l81sjz'
        >>> omise.Transaction.retrieve()
        <Collection at 0x7f6ef55b0ab8>
        >>> omise.Transaction.retrieve('trxn_test_4xuy2z4w5vmvq4x5pfs')
        <Transaction id='trxn_test_4xuy2z4w5vmvq4x5pfs' at 0x7fd953fa1990>
    """

    @classmethod
    def _collection_path(cls):
        return 'transactions'

    @classmethod
    def _instance_path(cls, transaction_id):
        return ('transactions', transaction_id)

    @classmethod
    def retrieve(cls, transaction_id=None):
        """Retrieve the transaction details for the given
        :param:`transaction_id`. If :param:`transaction_id` is not given, all
        transactions will be returned instead.

        :param transaction_id: (optional) a transaction id to retrieve.
        :type transaction_id: str
        :rtype: Transaction
        """
        if transaction_id:
            return _as_object(
                cls._request('get',
                             cls._instance_path(transaction_id)))
        return _as_object(cls._request('get', cls._collection_path()))

    @classmethod
    def list(cls):
        """Return all transactions that belongs to your account.

        :rtype: LazyCollection
        """
        return LazyCollection(cls._collection_path())

    def reload(self):
        """Reload the transaction details.

        :rtype: Transaction
        """
        return self._reload_data(
            self._request('get',
                          self._instance_path(self._attributes['id'])))
