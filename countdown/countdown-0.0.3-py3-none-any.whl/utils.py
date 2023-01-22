"""MIT License

Copyright (c) 2023-present Tanner B. Corcoran

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""
from . import types
import typing


class StaticProperty(typing.Generic[types.T]):
    """A decorator that works similarly to `@property`, but the decorated function must take no 
    arguments.

    Example Usage
    -------------
    ```
    >>> class Example:
    >>>     @StaticProperty
    >>>     def myprop() -> str:
    >>>         return "Woohoo!"
    
    >>> print(Example.myprop)
    'Woohoo!'
    >>> print(Example().myprop)
    'Woohoo!'
    ```
    
    """
    def __init__(self, func: typing.Callable[[], types.T]) -> None:
        self.func = func

    def __get__(self, inst, owner) -> types.T:
        return self.func()
