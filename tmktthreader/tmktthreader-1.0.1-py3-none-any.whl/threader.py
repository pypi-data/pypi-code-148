from threading import Thread


class Threader:

    def __init__(self, func):
        self._target = func

    def __call__(self, *args, **kwargs):
        t = Thread(target=self._target, args=args, kwargs=kwargs)
        t.start()
        return t
