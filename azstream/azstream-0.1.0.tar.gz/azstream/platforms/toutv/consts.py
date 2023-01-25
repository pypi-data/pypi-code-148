# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# BASE                                                                        #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

APP_HEADERS = {
    'phone': {
        'accept-encoding': 'gzip',
        'authorization': 'client-key {client_id}',
        'connection': 'Keep-Alive',
        'user-agent': '{app_user_agent}'
    },
    'tv': {
        'Accept-Encoding': 'identity',
        'Accept': '*/*',
        'Authorization': 'Client-Key {client_id}',
        'User-Agent': '{app_user_agent}'
    }
}
RC_SERVICES_BASE_URL = 'https://services.radio-canada.ca'