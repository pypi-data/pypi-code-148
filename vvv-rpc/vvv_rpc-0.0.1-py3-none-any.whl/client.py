import json
import queue
import inspect
import builtins
import threading
import requests
class client:
    def __init__(self, interface=None, win_index=None):
        self.interface = interface or 'http://127.0.0.1:18089'
        self.config_url = self.interface + '/config'
        self.win_index = win_index or 0
        self.run_script_url = self.interface + '/run_script'
        self.run_script_quick_url = self.interface + '/run_only_script'

    def make_post_data(self, data=None):
        data = data or {}
        if self.win_index: data["win_index"] = self.win_index
        return data

    def post_interface(self, url, data):
        s = requests.post(url, data=data).json()
        if s['status'] == 'success':
            return s.get('message', None)
        else:
            raise Exception(s['message'])

    def try_json_load(self, jsondata):
        try:
            return json.loads(jsondata)
        except:
            return jsondata

    def go_url(self, url, proxy=None):
        data = self.make_post_data({"url": url})
        if proxy: data['proxy'] = proxy
        return self.post_interface(self.config_url, data)

    def get_match_list(self):
        return self.post_interface(self.config_url, self.make_post_data({"show_match_url_list": True}))

    def remove_match_url(self, match_url):
        return self.post_interface(self.config_url, self.make_post_data({"match_url": match_url, "is_remove": True}))

    def set_match_url(self, match_url, value=None, vtype:'None or "base64"'=None):
        data = self.make_post_data({"match_url": match_url})
        if value: data['value'] = value
        if vtype: data['vtype'] = vtype
        return self.post_interface(self.config_url, data)

    def run_script_quick(self, script):
        return self.try_json_load(self.post_interface(self.run_script_quick_url, self.make_post_data({"script": script})))

    def run_script(self, scripts, wait_util_true=None):
        data = self.make_post_data({"scripts": scripts})
        if wait_util_true: data["wait_util_true"] = wait_util_true
        return self.try_json_load(self.post_interface(self.run_script_url, data))

    def get_url_by_scripts(self, match_url, scripts, wait_util_true=None):
        data = self.make_post_data({"match_url": match_url, "scripts": scripts})
        if wait_util_true: data["wait_util_true"] = wait_util_true
        return self.try_json_load(self.post_interface(self.run_script_url, data))

    def get_url_by_elements(self, match_url, elements):
        return self.try_json_load(self.post_interface(self.run_script_url, self.make_post_data({"match_url": match_url, "elements": elements})))

    def clear_add_script(self):
        return self.post_interface(self.config_url, self.make_post_data({"clear_script": True}))

    def add_script_before_load_url(self, add_script, atype=None):
        data = self.make_post_data({"add_script": add_script})
        if atype: data['atype'] = atype
        return self.post_interface(self.config_url, data)

    def set_position(self, x, y):
        if not (type(x) == int and type(y) == int):
            raise TypeError('set_position type error. x:{},y:{}'.format(x, y))
        return self.post_interface(self.config_url, self.make_post_data({"position": "{},{}".format(x, y)}))

    def restart(self):
        return self.post_interface(self.config_url, self.make_post_data({ "is_restart": True }))

    def disabled_http_only(self, enable=True):
        return self.post_interface(self.config_url, self.make_post_data({ "disabled_http_only": enable }))

    def clear_storage_data(self, enable=True):
        return self.post_interface(self.config_url, self.make_post_data({ "clear_storage_data": enable }))

def get_code():
    ret = inspect.getsourcelines(client)[0]
    return 'import json\nimport requests\n' + ''.join(ret)

class server:
    def __init__(self, taskerlist):
        self.taskerlist = taskerlist
        self.tasklist = queue.Queue()
        for idx, tasker in enumerate(self.taskerlist):
            # tasker.taskerlist = self.taskerlist
            td = threading.Thread(target=self.looper, args=(tasker,))
            td.vvv_tasker = tasker
            td.start()
        lock = threading.RLock()

        _org_print = print
        def _new_print(*arg,**kw):
            lock.acquire()
            td = threading.current_thread()
            vvv_tasker = getattr(td, 'vvv_tasker', None)
            if vvv_tasker:
                name = '{} :: {}'.format(vvv_tasker.interface, vvv_tasker.win_index)
                name = "[{}]".format(name.center(34))
                _org_print(name,*arg,**kw)
            else:
                _org_print(*arg,**kw)
            lock.release()
        builtins.print = _new_print

    def put(self, task):
        self.tasklist.put(task)

    def looper(self, tasker):
        while(1):
            task = self.tasklist.get()
            task[0](tasker, *task[1], **task[2])

    def __call__(self, func):
        def _(*a, **kw):
            self.put([func, a, kw])
        _.taskerlist = self.taskerlist
        return _

if __name__ == '__main__':
    print(get_code())

    @server([
        client('http://127.0.0.1:18089',0),
        client('http://127.0.0.1:18089',1),
    ])
    def some(vvv, url):
        print(vvv, url)

    for i in range(10):
        some('123')