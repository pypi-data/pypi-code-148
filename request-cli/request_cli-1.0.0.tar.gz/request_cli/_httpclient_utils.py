from difflib import get_close_matches
from requests.utils import default_headers as _default_headers


# User-Agnet
UA_ANDROID     = "Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.91 Mobile Safari/537.36"
UA_WINDOWNS    = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
UA_MAC         = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
UA_IPHONE      = "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
UA_IPAD        = "Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1"
UA_SYMBIAN     = "Mozilla/5.0 (Symbian/3; Series60/5.2 NokiaN8-00/012.002; Profile/MIDP-2.1 Configuration/CLDC-1.1 ) AppleWebKit/533.4 (KHTML, like Gecko) NokiaBrowser/7.3.0 Mobile Safari/533.4 3gpp-gba"
UA_ANDROID_PAD = "Mozilla/5.0 (Linux; Android 11; Phh-Treble vanilla Build/RQ3A.211001.001;) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/90.0.4430.91 Safari/537.36"

USER_AGENT_ALL = {
    "android"     : UA_ANDROID,
    "windows"     : UA_WINDOWNS,
    "mac"         : UA_MAC,
    "iphone"      : UA_IPHONE,
    "ipad"        : UA_IPAD,
    "symbian"     : UA_SYMBIAN,
    "android_pad" : UA_ANDROID_PAD,
}

# TIMEOUT
TIMEOUT = 7


def default_user_agent(user_agent, overwrite=False):

    if overwrite:
        return user_agent
    matches = get_close_matches(str(user_agent).lower(), USER_AGENT_ALL.keys(), n=1)
    if not matches:
        return UA_ANDROID
    return USER_AGENT_ALL.get(matches[0], UA_ANDROID)


def default_headers(user_agent="android", overwrite=False):

    headers = _default_headers()
    headers.update({"User-Agent": default_user_agent(user_agent, overwrite)})
    return headers
