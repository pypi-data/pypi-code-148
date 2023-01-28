from itertools import cycle
from shutil import get_terminal_size
from threading import Thread
from time import sleep

"""
A loader-like context manager

Args:
    desc (str, optional): The loader's description. Defaults to "Loading...".
    end (str, optional): Final print. Defaults to "Done!".
    timeout (float, optional): Sleep time between prints. Defaults to 0.1.
"""

class loading1:
    def __init__(self, desc="Loading...", end="[ ✔ ]", timeout=0.1, fail='[ ❌ ]'):
        self.desc = desc
        self.end = end
        self.timeout = timeout
        self.faill = fail

        self._thread = Thread(target=self._animate, daemon=True)
        self.steps = ['[   ]', '[-  ]', '[-- ]', '[---]', '[ --]', '[  -]']
        self.done = False
        self.fail = False

    def start(self):
        self._thread.start()
        return self

    def _animate(self):
        for c in cycle(self.steps):
            if self.done:
                break
            print(f"\r{c} {self.desc}", flush=True, end="")
            sleep(self.timeout)

    def __enter__(self):
        self.start()

    def stop(self):
        self.done = True
        cols = get_terminal_size((80, 20)).columns
        print("\r" + " " * cols, end="", flush=True)
        print(f"\r{self.end}", flush=True)

    def stopfail(self):
        self.done = True
        self.fail = True
        cols = get_terminal_size((80, 20)).columns
        print("\r" + " " * cols, end="", flush=True)
        print(f"\r{self.faill}", flush=True)

    def __exit__(self, exc_type, exc_value, tb):
        # handle exceptions with those variables ^
        self.stop()

class loading2:
    def __init__(self, desc="Loading...", end="[ ✔ ]", timeout=0.1, fail='[ ❌ ]'):
        self.desc = desc
        self.end = end
        self.timeout = timeout
        self.faill = fail

        self._thread = Thread(target=self._animate, daemon=True)
        self.steps = ['[   ]', '[-  ]', '[ - ]', '[  -]']
        self.done = False
        self.fail = False

    def start(self):
        self._thread.start()
        return self

    def _animate(self):
        for c in cycle(self.steps):
            if self.done:
                break
            print(f"\r{c} {self.desc}", flush=True, end="")
            sleep(self.timeout)

    def __enter__(self):
        self.start()

    def stop(self):
        self.done = True
        cols = get_terminal_size((80, 20)).columns
        print("\r" + " " * cols, end="", flush=True)
        print(f"\r{self.end}", flush=True)

    def stopfail(self):
        self.done = True
        self.fail = True
        cols = get_terminal_size((80, 20)).columns
        print("\r" + " " * cols, end="", flush=True)
        print(f"\r{self.faill}", flush=True)

    def __exit__(self, exc_type, exc_value, tb):
        # handle exceptions with those variables ^
        self.stop()

class loading3:
    def __init__(self, desc="Loading...", end="[ ✔ ]", timeout=0.1, fail='[ ❌ ]'):
        self.desc = desc
        self.end = end
        self.timeout = timeout
        self.faill = fail

        self._thread = Thread(target=self._animate, daemon=True)
        self.steps = ['[   ]', '[-  ]', '[-- ]', '[ --]', '[  -]', '[   ]', '[  -]', '[ --]', '[-- ]', '[-  ]']
        self.done = False
        self.fail = False

    def start(self):
        self._thread.start()
        return self

    def _animate(self):
        for c in cycle(self.steps):
            if self.done:
                break
            print(f"\r{c} {self.desc}", flush=True, end="")
            sleep(self.timeout)

    def __enter__(self):
        self.start()

    def stop(self):
        self.done = True
        cols = get_terminal_size((80, 20)).columns
        print("\r" + " " * cols, end="", flush=True)
        print(f"\r{self.end}", flush=True)

    def stopfail(self):
        self.done = True
        self.fail = True
        cols = get_terminal_size((80, 20)).columns
        print("\r" + " " * cols, end="", flush=True)
        print(f"\r{self.faill}", flush=True)

    def __exit__(self, exc_type, exc_value, tb):
        # handle exceptions with those variables ^
        self.stop()

class loading4:
    def __init__(self, desc="Loading...", end="[ ✔ ]", timeout=0.1, fail='[ ❌ ]'):
        self.desc = desc
        self.end = end
        self.timeout = timeout
        self.faill = fail

        self._thread = Thread(target=self._animate, daemon=True)
        self.steps = ['[   ]', '[-  ]', '[ - ]', '[  -]', '[   ]', '[  -]', '[ - ]', '[-  ]', '[   ]']
        self.done = False
        self.fail = False

    def start(self):
        self._thread.start()
        return self

    def _animate(self):
        for c in cycle(self.steps):
            if self.done:
                break
            print(f"\r{c} {self.desc}", flush=True, end="")
            sleep(self.timeout)

    def __enter__(self):
        self.start()

    def stop(self):
        self.done = True
        cols = get_terminal_size((80, 20)).columns
        print("\r" + " " * cols, end="", flush=True)
        print(f"\r{self.end}", flush=True)

    def stopfail(self):
        self.done = True
        self.fail = True
        cols = get_terminal_size((80, 20)).columns
        print("\r" + " " * cols, end="", flush=True)
        print(f"\r{self.faill}", flush=True)

    def __exit__(self, exc_type, exc_value, tb):
        # handle exceptions with those variables ^
        self.stop()

class loading_custom:
    def __init__(self, desc="Loading...", end="[ ✔ ]", timeout=0.1, steps=None, fail='[ ❌ ]'):
        self.desc = desc
        self.end = end
        self.timeout = timeout
        self.faill = fail

        self._thread = Thread(target=self._animate, daemon=True)
        if steps is None:
            self.steps = ['[   ]', '[-  ]', '[-- ]', '[ --]', '[  -]', '[   ]', '[  -]', '[ --]', '[-- ]', '[-  ]']
        else:
            self.steps = steps
        self.done = False
        self.fail = False

    def start(self):
        self._thread.start()
        return self

    def _animate(self):
        for c in cycle(self.steps):
            if self.done:
                break
            print(f"\r{c} {self.desc}", flush=True, end="")
            sleep(self.timeout)

    def __enter__(self):
        self.start()

    def stop(self):
        self.done = True
        cols = get_terminal_size((80, 20)).columns
        print("\r" + " " * cols, end="", flush=True)
        print(f"\r{self.end}", flush=True)

    def stopfail(self):
        self.done = True
        self.fail = True
        cols = get_terminal_size((80, 20)).columns
        print("\r" + " " * cols, end="", flush=True)
        print(f"\r{self.faill}", flush=True)

    def __exit__(self, exc_type, exc_value, tb):
        # handle exceptions with those variables ^
        self.stop()