"""
Copyright (C) 2022 Corsair M360, Inc - All Rights Reserved.
Unauthorized copying of this file, via any medium is strictly prohibited.
Proprietary and confidential.
"""
import string
import random
import sys

from unittest import mock
from m360.utils import from_json

class Settings(object):
    def __init__(self, cfg=None):
        self.M360 = cfg

class DjangoConf(object):
    def __init__(self, cfg=None):
        self.settings = Settings(cfg)

class DjangoHttp(object):
    def __init__(self, resp):
        self.JsonResponse = resp

class Request(object):
    def __init__(self, env=None, *, headers=None, path=None, meta=None, method="get"):
        self.path = path
        self.method = method
        self.headers = headers
        self.META = meta
        self.M360 = None
        self.GET = None
        self.args = None
        if env:
            self.path = env.get("path") if env.get("path") else self.path
            self.method = env.get("method") if env.get("method") else self.method
            self.headers = env.get("headers") if env.get("headers") else self.headers
            self.args = env.get("args") if env.get("args") else self.args

class Response(object):
    def __init__(self, data, *, status=200, headers=None):
        data_res = from_json(data) if type(data) is str else data
        self.data = data_res
        self.status = status
        self.headers = headers

    def __call__(self, *args, **kwargs):
        # usual method call: res(environ, start_response)
        return args[1](self.data)

class WerkzeugWrappers(object):
    def __init__(self):
        self.Request = Request
        self.Response = Response

class Flask(object):
    def __init__(self):
        self.g = Settings()

class DockerContainer(object):
    def __init__(self, container):
        self.attrs = container

class DockerContainers(object):
    def __init__(self, containers):
        self.containers = []
        for c in containers:
            self.containers.append(DockerContainer(c))

    def list(self, filters=None):
        return self.containers

class Docker(object):
    def __init__(self, containers):
        self.containers = DockerContainers(containers)

    def from_env(self):
        return self

def random_string(length=10, uppercase=False):
    if uppercase:
        txt = string.ascii_uppercase
        return ''.join(random.choice(txt) for _ in range(length))
    else:
        txt = string.ascii_lowercase
        return ''.join(random.choice(txt) for _ in range(length))

def random_numeric_string(length=10):
    dig = string.digits
    return ''.join(random.choice(dig) for _ in range(length))

def random_int(_min=0, _max=10):
    return random.randint(_min, _max)

def mock_django(config=None, handler=None):
    def get_response(data=True, status=200):
        return data
    if not handler:
        handler = get_response
    try:
        sys.modules.pop("django")
        sys.modules.pop("django.http")
        sys.modules.pop("django.http.JsonResponse")
        sys.modules.pop("django.conf")
    except KeyError:
        pass  # ignore errors here
    sys.modules['django'] = mock.Mock()
    sys.modules['django.http'] = DjangoHttp(get_response)
    sys.modules['django.conf'] = DjangoConf(config)
    from m360.frameworks.django.middleware import DjangoMiddleware
    return DjangoMiddleware(handler)

def mock_flask(config=None, handler=None):
    def app(env, start_response):
        if handler:
            return start_response(handler(env))
        else:
            return start_response(env)
    try:
        sys.modules.pop("flask")
        sys.modules.pop("werkzeug")
        sys.modules.pop("werkzeug.wrappers")
    except KeyError:
        pass  # ignore errors here
    sys.modules['flask'] = Flask()
    sys.modules['werkzeug'] = mock.Mock()
    sys.modules['werkzeug.wrappers'] = WerkzeugWrappers()
    from m360.frameworks.flask.middleware import FlaskMiddleware
    return FlaskMiddleware(app, config)

def mock_docker(containers=None):
    try:
        sys.modules.pop("m360")
        sys.modules.pop("m360.maintenance")
        sys.modules.pop("docker")
    except KeyError:
        pass  # ignore errors here
    sys.modules["docker"] = Docker(containers)
