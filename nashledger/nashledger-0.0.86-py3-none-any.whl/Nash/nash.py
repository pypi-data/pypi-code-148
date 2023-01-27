from erp_sync.Resources.clients import Client
from erp_sync.Resources.users import Users
from erp_sync.Resources.resource import Resource

# This class is responsible for configuring and checking of developer credentials.
# It's the class that will be called first before a developer accesses Nash Framework - Nash's API resources

# This class is also a Resource class
class Nash(Resource):
    # Since all classes are going to be called from this class,
    # You can use this class to set attributes of other classes/resources
    _headers = {
        'Content-Type': 'application/json',
        'Accept-Encoding': 'gzip, deflate, br',
    }

    _params = {}

    _response = {}

    _is_logged_in = False

    _client = None

    _access_token = None

    _user_id = -1

    # When intializing this class, set the default request headers and params
    def __init__(self, oauth2_client_id=None, client_secret=None, auth_scope=None):
        super().__init__("NashAPI", self._headers, self._params)
        # If auth credential are provided in the constructor go ahead and initiate a log in request
        if oauth2_client_id and client_secret and auth_scope:
            self.login(oauth2_client_id=oauth2_client_id,
                       client_secret=client_secret, auth_scope=auth_scope)

    # Use this method to login a user into the nash framework
    def login(self, oauth2_client_id=None, client_secret=None, auth_scope=None):
        # authenticate and provide user credentials

        auth_token_url = super().ERP_CONF.get(super().AUTHENTICATE, {}).get('url', '') + "/" \
            + super().ERP_CONF.get(super().AUTHENTICATE, {}).get('read', {}
                                                                   ).get('operations', {}).get(super().AUTH_GET_TOKEN, '')[0]

        super().set_oauth2_client_id(oauth2_client_id=oauth2_client_id)\
            .set_client_secret(client_secret=client_secret)\
            .set_auth_token_url(auth_token_url=auth_token_url)\
            .set_auth_scope(auth_scope=auth_scope)\
            .fetch_identity_token()

        return self

    # Use this method to sign up a user into the nash framework
    def sign_up(self, payload=None, method='POST', endpoint="/users", log_in_user=True):
        # authenticate and provide user credentials
        # set response here

        # Call the method exec to make the request to A.P.I. endpoint and return the data that will be returned in this method
        self._response = Users(self).new(payload, method, endpoint).response()

        if log_in_user:
            if 'created_at' in self._response:

                self.login(payload={"username": payload.get(
                    "username"), "password": payload.get("password")}).response()

        return self

    # Use this method to get access to the ERP/Client class, this is the gateway to the ERP Resources/Entities and 
    def client(self, client_id=-1):

        self._client = Client(self, client_id).set_client_id(client_id=super().get_client_id())\
                    .set_client_secret(client_secret=super().get_client_secret())\
                    .set_auth_token_url(auth_token_url=super().get_auth_token_url())\
                    .set_auth_scope(auth_scope=super().get_auth_scope())

        return self._client
    
    # TODO This method should return an authenticated user's data
    # def user(self):
    #     pass

    # Method to check if a user is logged in
    def is_logged_in(self):
        return self._is_logged_in