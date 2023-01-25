
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
# Profile                                                                     #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

PROFILE_URL = 'https://services.radio-canada.ca/toutv/subscribers/profile?version=6&device=phone_android'
PROFILE_HEADERS = {
    'accept-encoding': 'gzip',
    'authorization': 'Bearer {access_token}',
    'connection': 'Keep-Alive',
    'content-type': 'application/x-www-form-urlencoded',
    'user-agent': '',
    'x-rc-device-id': '{device_id}',
    'x-requested-with': '{device_id}',
}