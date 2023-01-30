from .libs.requests.cookies import RequestsCookieJar


class Cookie(RequestsCookieJar):
    def __init__(self, *args, **kwargs):
        super(Cookie, self).__init__(*args, **kwargs)
