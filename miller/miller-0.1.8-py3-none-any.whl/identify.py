"""
identify: returns booleans about typing of introspected items
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
    map_files
    map_folders
    map_modules
    map_paths  
    get_files
    get_folders
    get_modules
    get_paths   
    has_files
    has_folders
    has_modules
    has_paths 
    is_file
    is_folder
    is_module
    is_path 
    name_files
    name_folders
    name_modules
    name_paths  
          
    Simple Type Checkers:
        is_container: returns if an item is a container but not a str.
        is_function: returns if an item is a function type.
        is_iterable: returns if an item is iterable but not a str.
        is_nested: dispatcher which returns if an item is a nested container.
        is_nested_dict: returns if an item is a nested dict.
        is_nested_sequence: returns if an item is a nested sequence.
        is_nested_set: returns if an item is a nested set.
        is_sequence: returns if an item is a sequence but not a str. 
    
To Do:
    Adding parsing functionality to commented signature functions to find
        equivalence when one signature has subtypes of the other signature
        (e.g., one type annotation is 'dict' and the other is 'MutableMapping').
        It might be necessary to create a separate Signature-like class to 
        implement this functionality. This includes fixing or abandoning 
        'has_annotations' due to issues matching type annotations.
    Add support for Kinds once that system is complete.
    Add support for types (using type annotations) in the 'contains' function so
        that 'contains' can be applied to classes and not just instances.
    Add 'dispatcher' framework to 'contains' once the dispatcher framework is
        completed in the 'bobbie' package and the Kind system is completed in
        the nagata package. This should replace existing usages of python's
        singledispatch, which doesn't propertly deal with subtypes.
    

    
"""
from __future__ import annotations
from collections.abc import (
    Collection, Container, Hashable, Iterable, Mapping, MutableMapping, 
    MutableSequence, Sequence, Set)
import functools
import inspect
import pathlib
import types
from typing import Any, Type

import camina

from . import rules
from . import identify
 
 
def is_class_attribute(item: object | Type[Any], /, attribute: str) -> bool:
    """Returns if 'attribute' is a class attribute of 'item'.

    Args:
        item (object | Type[Any]): class or instance to examine.
        attribute (str): name of attribute to examine.

    Returns:
        bool: where 'attribute' is a class attribute.
        
    """    
    if not inspect.isclass(item):
        item.__class__
    return (
        hasattr(item, attribute)
        and not is_method(item, attribute = attribute)
        and not is_property(item, attribute = attribute))
      
def is_container(item: object | Type[Any]) -> bool:
    """Returns if 'item' is a container and not a str.
    
    Args:
        item (object | Type[Any]): class or instance to examine.
        
    Returns:
        bool: if 'item' is a container but not a str.
        
    """  
    if not inspect.isclass(item):
        item.__class__ 
    return issubclass(item, Container) and not issubclass(item, str)

def is_dict(item: object | Type[Any]) -> bool:
    """Returns if 'item' is a mutable mapping (generic dict type).
    
    Args:
        item (object | Type[Any]): class or instance to examine.
        
    Returns:
        bool: if 'item' is a mutable mapping type.
        
    """  
    if not inspect.isclass(item):
        item.__class__ 
    return isinstance(item, MutableMapping) 

def is_file(item: str | pathlib.Path) -> bool:
    """Returns whether 'item' is a non-python-module file.
    
    Args:
        item (str | pathlib.Path): path to check.
        
    Returns:
        bool: whether 'item' is a non-python-module file.
        
    """ 
    item = camina.pathlibify(item)
    return (
        item.exists() 
        and item.is_file() 
        and not item.suffix in rules.MODULE_EXTENSIONS)

def is_folder(item: str | pathlib.Path) -> bool:
    """Returns whether 'item' is a path to a folder.
    
    Args:
        item (str | pathlib.Path): path to check.
        
    Returns:
        bool: whether 'item' is a path to a folder.
        
    """ 
    item = camina.pathlibify(item)
    return item.exists() and item.is_dir()

def is_function(item: object | Type[Any]) -> bool:
    """Returns if 'item' is a function type.
    
    Args:
        item (object | Type[Any]): class or instance to examine.
        
    Returns:
        bool: if 'item' is a function type.
        
    """  
    return isinstance(item, types.FunctionType)
   
def is_iterable(item: object | Type[Any]) -> bool:
    """Returns if 'item' is iterable and is NOT a str type.
    
    Args:
        item (object | Type[Any]): class or instance to examine.
        
    Returns:
        bool: if 'item' is iterable but not a str.
        
    """ 
    if not inspect.isclass(item):
        item.__class__ 
    return issubclass(item, Iterable) and not issubclass(item, str)

def is_list(item: object | Type[Any]) -> bool:
    """Returns if 'item' is a mutable sequence (generic list type).
    
    Args:
        item (object | Type[Any]): class or instance to examine.
        
    Returns:
        bool: if 'item' is a mutable list type.
        
    """
    if not inspect.isclass(item):
        item.__class__ 
    return isinstance(item, MutableSequence)
  
def is_method(item: object | Type[Any], attribute: Any) -> bool:
    """Returns if 'attribute' is a method of 'item'.

    Args:
        item (object | Type[Any]): class or instance to examine.
        attribute (str): name of attribute to examine.

    Returns:
        bool: where 'attribute' is a method of 'item'.
        
    """ 
    if isinstance(attribute, str):
        try:
            attribute = getattr(item, attribute)
        except AttributeError:
            return False
    return inspect.ismethod(attribute)
 
def is_module(item: str | pathlib.Path) -> bool:
    """Returns whether 'item' is a python-module file.
    
    Args:
        item (str | pathlib.Path): path to check.
        
    Returns:
        bool: whether 'item' is a python-module file.
        
    """  
    item = camina.pathlibify(item)
    return (
        item.exists() 
        and item.is_file() 
        and item.suffix in rules.MODULE_EXTENSIONS)

@functools.singledispatch
def is_nested(item: object, /) -> bool:
    """Returns if 'item' is nested at least one-level.
    
    Args:
        item (object): instance to examine.
        
    Raises:
        TypeError: if 'item' does not match any of the registered types.
        
    Returns:
        bool: if 'item' is a nested mapping.
        
    """ 
    raise TypeError(f'item {item} is not supported by {__name__}')

@is_nested.register(Mapping)   
def is_nested_dict(item: Mapping[Any, Any], /) -> bool:
    """Returns if 'item' is nested at least one-level.
    
    Args:
        item (Mapping[Any, Any]): class or instance to examine.
        
    Returns:
        bool: if 'item' is a nested mapping.
        
    """ 
    return (
        isinstance(item, Mapping) 
        and any(isinstance(v, Mapping) for v in item.values()))

@is_nested.register(MutableSequence)     
def is_nested_list(item: MutableSequence[Any], /) -> bool:
    """Returns if 'item' is nested at least one-level.
    
    Args:
        item (MutableSequence[Any]): class or instance to examine.
        
    Returns:
        bool: if 'item' is a nested sequence.
        
    """ 
    return (
        identify.is_sequence(item)
        and any(identify.is_sequence(item = v) for v in item))

@is_nested.register(Set)         
def is_nested_set(item: Set[Any], /) -> bool:
    """Returns if 'item' is nested at least one-level.
    
    Args:
        item (item: Set[Any]): class or instance to examine.
        
    Returns:
        bool: if 'item' is a nested set.
        
    """ 
    return (
        identify.is_set(item)
        and any(identify.is_set(item = v) for v in item))

@is_nested.register(tuple)     
def is_nested_tuple(item: tuple[Any, ...], /) -> bool:
    """Returns if 'item' is nested at least one-level.
    
    Args:
        item (tuple[Any, ...]): class or instance to examine.
        
    Returns:
        bool: if 'item' is a nested sequence.
        
    """ 
    return (
        identify.is_sequence(item)
        and any(identify.is_sequence(item = v) for v in item))
    
def is_path(item: str | pathlib.Path) -> bool:
    """Returns whether 'item' is a currently existing path.
    
    Args:
        item (str | pathlib.Path): path to check.
        
    Returns:
        bool: whether 'item' is a currently existing path.
        
    """ 
    item = camina.pathlibify(item)
    return item.exists()

def is_property(item: object | Type[Any], attribute: Any) -> bool:
    """Returns if 'attribute' is a property of 'item'.

    Args:
        item (object | Type[Any]): class or instance to examine.
        attribute (str): name of attribute to examine.

    Returns:
        bool: where 'attribute' is a property of 'item'.
        
    """ 
    if not inspect.isclass(item):
        item.__class__
    if isinstance(attribute, str):
        try:
            attribute = getattr(item, attribute)
        except AttributeError:
            return False
    return isinstance(attribute, property)
    
def is_sequence(item: object | Type[Any]) -> bool:
    """Returns if 'item' is a sequence and is NOT a str type.
    
    Args:
        item (object | Type[Any]): class or instance to examine.
        
    Returns:
        bool: if 'item' is a sequence but not a str.
        
    """ 
    if not inspect.isclass(item):
        item.__class__ 
    return issubclass(item, Sequence) and not issubclass(item, str) 
        
def is_set(item: object | Type[Any]) -> bool:
    """Returns if 'item' is a Set (including generic type sets).
    
    Args:
        item (object | Type[Any]): class or instance to examine.
        
    Returns:
        bool: if 'item' is a set.
        
    """ 
    if not inspect.isclass(item):
        item.__class__ 
    return issubclass(item, Set)
  
def is_variable(
    item: object | Type[Any] | types.ModuleType, 
    attribute: str) -> bool:
    """Returns if 'attribute' is a simple data attribute of 'item'.

    Args:
        item (object | Type[Any] | types.ModuleType): class or instance to 
            examine.
        attribute (str): name of attribute to examine.

    Returns:
        bool: where 'attribute' is a simple variable (and not a method or 
            property) or 'item'.
        
    """ 
    return (
        hasattr(item, attribute)
        and not is_function(item)
        and not is_property(item, attribute = attribute))
