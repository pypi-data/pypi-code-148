from copy import deepcopy

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# BASE                                                                        #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

WEB_HEADERS = {
    'accept': 'application/json, text/plain, */*',
    'accept-encoding': 'gzip, deflate',
    'accept-language': 'fr-CA,en-US;q=0.9',
    'connection': 'keep-alive',
    'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
    'origin': 'https://account.bellmedia.ca',
    'referer': 'https://account.bellmedia.ca/bdu/?loginUrl=https://account.bellmedia.ca/api/login/v2.1?grant_type=bdu_password&provider_id=urn:bell:ca:idp:prod',
    'user-agent': '{user_agent}',
    'x-requested-with': '{app_headers_tag}'
}

APP_HEADERS = {
    'accept-encoding': 'gzip',
    'authorization': 'Basic {app_token}',
    'connection': 'keep-alive',
    'user-agent': 'okhttp/4.9.0'
}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Captcha                                                                     #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

CAPTCHA_URL = 'https://www.google.com/recaptcha/api2/anchor?ar=1&k=6Lfv5XAUAAAAAAXwhe8t2ssyPuoiMuFE2XyJzpEF&co=aHR0cHM6Ly9hY2NvdW50LmJlbGxtZWRpYS5jYTo0NDM.&hl=fr-CA&v=u35fw2Dx4G0WsO6SztVYg4cV&size=invisible&cb=b5zztvhcdb5b'

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Login                                                                       #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

LOGIN_URL = 'https://account.bellmedia.ca/api/login/v2.1'
LOGIN_BODY = {
    'username': '{username}',
    'password': '{password}',
    'grant_type': 'bdu_password',
    'provider_id': 'urn:bell:ca:idp:prod',
    'recaptcha_token': '{captcha}'
    }
LOGIN_HEADERS = deepcopy(WEB_HEADERS)
LOGIN_HEADERS['authorization'] = 'Basic {app_token}'

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Refresh                                                                     #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

REFRESH_URL = 'https://account.bellmedia.ca/api/login/v2.1?grant_type=refresh_token'
REFRESH_BODY = {
    'refresh_token': '{refresh_token}',
    'profile_id': '{profile_id}'
}
REFRESH_HEADERS = deepcopy(APP_HEADERS)
REFRESH_HEADERS['content-type'] = 'application/x-www-form-urlencoded'

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Magic Generate                                                              #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

MAGIC_GENERATE_URL = 'https://account.bellmedia.ca/api/magic-link/v2.1/generate'
MAGIC_GENERATE_HEADERS = deepcopy(WEB_HEADERS)
MAGIC_GENERATE_HEADERS['authorization'] = 'Bearer {login_token}'

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Magic Login                                                                 #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

MAGIC_LOGIN_URL = 'https://account.bellmedia.ca/api/login/v2.1?grant_type=magic_link_token'
MAGIC_LOGIN_BODY = {
    'magic_link_token': '{magic_token}'
}
MAGIC_LOGIN_HEADERS = deepcopy(APP_HEADERS)
MAGIC_LOGIN_HEADERS['content-type'] = 'application/x-www-form-urlencoded'

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Profile                                                                     #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

PROFILE_URL = 'https://account.bellmedia.ca/api/profile/v1.1'
PROFILE_HEADERS = deepcopy(APP_HEADERS)
PROFILE_HEADERS['authorization'] = 'Bearer {access_token}'