#coding=utf-8
import json

import web
G_Coding = "utf-8"
def coding(code = None):
    global G_Coding
    if code is None:
        return G_Coding
    G_Coding = code

pass
class Output:
    def __init__(self):
        self.init()
    def init(self):
        self.rst = None
        self._finish = False
    def finish(self, mark = None):
        if mark is None:
            return self._finish
        self._finish = mark
    def set(self, key, val):
        if self.rst is None:
            self.rst = {}
        self.rst[key] = val
    def update(self, obj):
        if self.rst is None:
            self.rst = {}
        self.rst.update(obj)
    def set_bytes(self, bts):
        self.rst = bts
    def set_str(self, s):
        self.rst = s
    def contain(self, key):
        return key in self.datas
    def out(self):
        if self.rst is None:
            return None
        if type(self.rst) == dict:
            self.rst = json.dumps(self.rst)
        return self.rst
    def __call__(self):
        return self.out()

pass
class Input:
    def init(self, url = None, type = None):
        self.url = url
        self.type = type
        self.datas_post = self.load()
        self.datas_get = self.input()
        self.datas = self.datas_post
        self.datas.update(self.datas_get)
    def load(self):
        data = self.data()
        if data is None:
            return {}
        if data.strip()[0] != b"{"[0]:
            data = data.decode(coding())
            arr = data.split("&")
            rst = {}
            for v in arr:
                x = v.split("=")
                if len(x)==2:
                    rst[x[0]] = x[1]
        else:
            try:
                rst = json.loads(data.decode(coding()))
            except Exception as exp:
                print("LOAD ERROR:", exp)
                print("DATA:", data)
                return exp
        return rst
    def data(self):
        _data = web.data()
        if _data is None or len(_data) == 0:
            return None
        return _data
    def input(self, *argv, **maps):
        return web.input(*argv, **maps)
    def set(self, key, val):
        self.datas[key] = val
    def update(self, obj):
        self.datas.update(obj)
    def contain(self, key):
        return key in self.datas
    def get(self, key = None, default = None):
        if key is None:
            return self.datas
        if key not in self.datas:
            return default
        return self.datas[key]

pass
GET = "get"
POST = "post"
class BaseDeal:
    def _init(self):
        self.input = Input()
        self.output = Output()
        self.session = None
        self.cookie = None
    def __init__(self):
        self._init()
    def build(self, url, type):
        self.input.init(url, type)
        self.output.init()
    def _set(self, deal):
        self.input = deal.input
        self.output = deal.output
    def init(self, *args, **maps):
        pass
    def get(self):
        self.deal()
    def post(self):
        self.deal()
    def deal(self):
        pass
    def GET(self, url):
        self.build(url, GET)
        self.init()
        self.get()
        return self.output()
    def POST(self, url):
        self.build(url, POST)
        self.init()
        self.post()
        return self.output()

pass
Base = BaseDeal
class WebApplication(web.application):
    def run(self, port = 8080, ip = "0.0.0.0", *middleware):
        func = self.wsgifunc(*middleware)
        return web.httpserver.runsimple(func, (ip, port))

pass

urls = (
    '/(.*)', 'WebMain'
)

class Container:
    def __init__(self, controller = None):
        self.controller = controller
    def set(self, controller):
        self.controller = controller
    def GET(self, url):
        if self.controller is None:
            return "ERROR NOT IMPLEMENT CONTROLLER"
        return self.controller.GET(url)
    def POST(self, url):
        if self.controller is None:
            return "ERROR NOT IMPLEMENT CONTROLLER"
        return self.controller.POST(url)

pass
container = Container()
class WebMain:
    def GET(self, url):
        return container.GET(url)
    def POST(self, url):
        return container.POST(url)

pass

app = WebApplication(urls, globals())
def run(port = 8080, ip = "0.0.0.0"):
    app.run(port = port, ip = ip)

pass
def init(controller):
    container.set(controller)

pass

"""

from . import webz
webz.init(None)
webz.run(8080, "127.0.0.1")


"""

rurls = []

class SimpleRedirect:
    def run(self):
        urls = (
            '/(.*)', 'SimpleRedirect',
        )
        print("[SimpleRedirect] Server Init on:", self.port, self.ip, "to", self.url)
        app = WebApplication(urls, globals())
        app.run(port = self.port, ip = self.ip)
        print("[SimpleRedirect] Server Run")
    def __init__(self, url="", port=8080, ip = '127.0.0.1'):
        self.url = url
        self.port = port
        self.ip = ip
        rurls.append(url)
    def GET(self, url):
        print("[REDIRECT]: ", url, "TO", rurls[0])
        s = """
        <html>
        <head>
        <meta http-equiv="refresh" content="1,url=%s">
        </head>
        <body></body></html>
        """
        return s%(rurls[0],)
    def POST(self, url):
        return self.GET(url)

pass
def _redirect(port, url):
    obj = SimpleRedirect(url, port)
    obj.run()

pass
def redirect(port, url):
    import multiprocessing
    p = multiprocessing.Process(target = _redirect,args = [port, url])
    p.daemon = True
    p.start()

pass