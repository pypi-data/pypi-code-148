import sys
import traceback
from argparse import ArgumentParser
from collections.abc import Callable
from functools import wraps
from time import sleep
from typing import ParamSpec, TypeVar, Union

from .base import ConfigurableItem, Item, NestableItem, Params
from .utils import PLUGIN_PATH, copy_to_clipboard, deserialize_callback, refreshplugin


P = ParamSpec('P')
R = TypeVar('R')
MetaDecorator = Union[
    Callable[..., None],
    Callable[[Callable[..., R]], Callable[..., None]]
]


class Divider(Item):
    title = '---'


class Reset(Item):
    title = '~~~'


class HeaderItem(ConfigurableItem):
    pass


class MenuItem(NestableItem):

    def add_item(self, title: str = '', **params: Params) -> 'MenuItem':
        item = MenuItem(title, **params)
        self.children.append(item)
        return item

    def add_divider(self) -> Item:
        item = Divider()
        self.children.append(item)
        return item


class Menu(MenuItem):
    def __init__(self, title: str = '', **params: Params) -> None:
        super().__init__(title, **params)
        self.headers: list[Item] = []
        self.body: list[Item] = []
        self._main: Callable[..., None] | None = None
        self._repeat_interval: int | float = 0
        self._parser = ArgumentParser(add_help=False)
        self._parser.add_argument('--script-callbacks', nargs='+')


    def __str__(self) -> str:
        lines = [self._render_line()]
        for item in self.headers:
            lines.append(str(item))
        lines.append(str(Divider()))
        for item in self.children:
            lines.append(str(item))
        return '\n'.join(lines) + '\n'

    def _run_callbacks(self, callbacks: list[str]) -> None:
        for callback in callbacks:
            func: Callable[..., object]
            args: P.args
            kwargs: P.kwargs
            func, args, kwargs = deserialize_callback(callback)
            func(*args, **kwargs)

    def add_header(self, title: str, **params: Params) -> Item:
        item = HeaderItem(title, **params)
        self.headers.append(item)
        return item

    def clear(self) -> None:
        self.title = ''
        self._alternate = None
        self._callbacks.clear()
        self.params.clear()
        self.headers.clear()
        self.children.clear()

    def runner(
        self, func: Callable[..., R] | None = None, *, reset: bool = True
    ) -> MetaDecorator[R]:

        def wrapperfactory(inner_func: Callable[P, R]) -> Callable[..., None]:
            @wraps(inner_func)
            def wrapper(*args: P.args, **kwargs: P.kwargs) -> None:
                if reset:
                    self.clear()
                try:
                    inner_func(*args, **kwargs)
                except Exception: # pylint: disable=broad-except
                    exc_info = sys.exc_info()
                    traceback_text = ''.join(traceback.format_exception(*exc_info)).strip()
                    self.clear()
                    self.title = f':exclamationmark.triangle.fill: {PLUGIN_PATH.name}'
                    self.params['sfcolor'] = 'yellow'
                    error_item = self.add_item('Error running plugin')
                    error_item.add_item('Traceback')
                    error_item.add_divider()
                    error_item.add_item(
                        traceback_text, size=12, font='courier',
                        tooltip='Copy traceback to clipboard'
                    ).add_callback(copy_to_clipboard, traceback_text)
                    self.add_divider()
                    self.add_item(
                        'Refresh', sfimage='arrow.clockwise'
                    ).add_callback(refreshplugin)
            return wrapper

        def decorator(inner_func: Callable[..., R]) -> Callable[..., None]:
            self._main = wrapperfactory(inner_func)
            return self._main

        if func is None:
            return decorator
        self._main = wrapperfactory(func)
        return self._main


    def set_repeat_interval(self, interval: int | float) -> None:
        self._repeat_interval = interval

    def run(self, repeat_interval: int | None = None) -> None:
        args = self._parser.parse_args()
        if args.script_callbacks is not None:
            self._run_callbacks(args.script_callbacks)
            return
        if self._main is None:
            raise RuntimeError('no main function specified')
        if not repeat_interval:
            self._main()
            print(self)
            return

        self.set_repeat_interval(repeat_interval)
        while True:
            self._main()
            print(Reset())
            print(self, flush=True)
            sleep(self._repeat_interval)
