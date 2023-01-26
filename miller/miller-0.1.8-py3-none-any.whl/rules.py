"""
rules: global settings for miller
Corey Rayburn Yung <coreyrayburnyung@gmail.com>
Copyright 2020-2022, Corey Rayburn Yung
License: Apache-2.0

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

Contents:  

        
ToDo:


"""
from __future__ import annotations
from collections.abc import Callable, Sequence
from typing import Any, Type

import camina


MODULE_EXTENSIONS: list[str] = ['.py', '.pyc']
NAMER: Callable[[object | Type[Any]], str] = camina.namify
RECURSIVE: bool = False

    
def set_module_extensions(extensions: Sequence[str]) -> None:
    """Sets the global default rule of python module suffixes.

    Args:
        extensions (Sequence[str]): file extensions of python modules.

    Raises:
        TypeError: if 'extensions' is not a sequence of str type.
        
    """
    if (isinstance(extensions, Sequence) 
            and not isinstance(extensions, str)
            and all(isinstance(i, str) for i in extensions)):
        globals()['MODULE_EXTENSIONS'] = extensions
    else:
        raise TypeError('extensions argument must be a sequence of strings')
    
def set_namer(namer: Callable[[object | Type[Any]], str]) -> None:
    """Sets the global default function used to name items.

    Args:
        namer (Callable[[object | Type[Any]], str]): function that returns a 
            str name of any item passed.

    Raises:
        TypeError: if 'namer' is not callable.
        
    """
    if isinstance(namer, Callable):
        globals()['NAMER'] = namer
    else:
        raise TypeError('extensions argument must be a sequence of strings')
    
def set_recursion(recursive: bool) -> None:
    """Sets the global default rule whether tools should be recursive.
    
    If a 'recursive' argument is passed to a function that takes one, that
    argument will always take precedence. However, the default value is used 
    when an argument is not passed.

    Args:
        recursive (bool): value to set the RECURSIVE variable to.

    Raises:
        TypeError: if 'recursive' is not a boolean type.
        
    """
    if isinstance(recursive, bool):
        globals()['RECURSIVE'] = recursive
    else:
        raise TypeError('recursive argument must be a boolean type')

        