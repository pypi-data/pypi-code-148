from copy import deepcopy

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# BASE                                                                        #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

APP_HEADERS = {
    'accept-encoding': 'gzip',
    'authorization': 'Basic {app_token}',
    'connection': 'keep-alive',
    'user-agent': 'okhttp/4.10.0'
}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Login                                                                       #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

LOGIN_URL = 'https://account.bellmedia.ca/api/login/v2.1?grant_type=password'
LOGIN_BODY = {
    'username': '{username}',
    'password': '{password}'
}
LOGIN_HEADERS = deepcopy(APP_HEADERS)
LOGIN_HEADERS['authorization'] = 'Basic {app_token}'
LOGIN_HEADERS['content-type'] = 'application/x-www-form-urlencoded'

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Refresh                                                                     #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

REFRESH_URL = 'https://account.bellmedia.ca/api/login/v2.1?grant_type=refresh_token'
REFRESH_BODY = {
    'refresh_token': '{refresh_token}',
    'profile_id': '{profile_id}'
}
REFRESH_HEADERS = deepcopy(APP_HEADERS)
REFRESH_HEADERS['authorization'] = 'Basic {app_token}'
REFRESH_HEADERS['content-type'] = 'application/x-www-form-urlencoded'

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Profile                                                                     #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

PROFILE_URL = 'https://account.bellmedia.ca/api/profile/v1.1'
PROFILE_HEADERS = deepcopy(APP_HEADERS)
PROFILE_HEADERS['authorization'] = 'Bearer {access_token}'