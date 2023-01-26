"""
check: returns booleans about introspection information contents 
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
    report.get_files
    report.get_folders
    report.get_modules
    report.get_paths   
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
          
To Do:

    
"""
from __future__ import annotations
from collections.abc import (
    Collection, Container, Hashable, Iterable, Mapping, MutableMapping, 
    MutableSequence, Sequence, Set)
import dataclasses
import functools
import inspect
import pathlib
import types
from typing import Any, Optional, Type

import camina

from . import rules
from . import identify
from . import acquire


def has_attributes(
    item: object | Type[Any], 
    attributes: MutableSequence[str]) -> bool:
    """Returns whether 'attributes' exist in 'item'.

    Args:
        item (object | Type[Any]): class or instance to examine.
        attributes (MutableSequence[str]): names of attributes to check to see
            if they exist in 'item'.
            
    Returns:
        bool: whether all 'attributes' exist in 'items'.
    
    """
    return all(hasattr(item, a) for a in attributes)

def has_fields(
    item: dataclasses.dataclass | Type[dataclasses.dataclass], 
    fields: MutableSequence[str]) -> bool:
    """Returns whether 'attributes' exist in dataclass 'item'.

    Args:
        item (dataclasses.dataclass | Type[dataclasses.dataclass]): 
            dataclass or dataclass instance to examine.
        fields (MutableSequence[str]): names of attributes to check to see
            if they exist in 'item'.
    
    Raises:
        TypeError: if 'item' is not a dataclass.
        
    Returns:
        bool: whether all 'attributes' exist in 'items'.
    
    """
    if dataclasses.is_dataclass(item):
        all_fields = [f.name for f in dataclasses.fields(item)]
        return all(a in all_fields for a in fields)
    else:
        raise TypeError('item must be a dataclass')
 
def has_files(
    item: str | pathlib.Path,
    elements: list[str | pathlib.Path]) -> bool:  
    """Returns whether all 'elements' are in 'item'.
  
    Args:
        item (str | pathlib.Path): path of folder to examine.
        elements (list[str | pathlib.Path]): list of paths to test whether they 
            are in 'item'.
        
    Returns:
        bool: whether all 'elements' are in 'item'.
        
    """ 
    item = camina.pathlibify(item)
    paths = acquire.get_paths(item, recursive = False)
    elements = [camina.pahlibify(p) for p in elements]
    return all(elements in paths)
          
def has_folders(
    item: str | pathlib.Path,
    elements: list[str | pathlib.Path]) -> bool:  
    """Returns whether all 'elements' are in 'item'.
  
    Args:
        item (str | pathlib.Path): path of folder to examine.
        elements (list[str | pathlib.Path]): list of paths to test whether they 
            are in 'item'.
        
    Returns:
        bool: whether all 'elements' are in 'item'.
        
    """ 
    item = camina.pathlibify(item)
    paths = acquire.get_paths(item, recursive = False)
    elements = [camina.pahlibify(p) for p in elements]
    return all(elements in paths)
     
def has_methods(
    item: object | Type[Any], 
    methods: str | MutableSequence[str]) -> bool:
    """Returns whether 'item' has 'methods' which are methods.

    Args:
        item (object | Type[Any]): class or instance to examine.
        methods (str | MutableSequence[str]): name(s) of methods to check 
            to see if they exist in 'item' and are types.MethodType.
            
    Returns:
        bool: whether all 'methods' exist in 'items' and are types.MethodType.
        
    """
    methods = list(camina.iterify(methods))
    return all(identify.is_method(item, attribute = m) for m in methods)
 
def has_modules(
    item: str | pathlib.Path,
    elements: list[str | pathlib.Path]) -> bool:  
    """Returns whether all 'elements' are in 'item'.
  
    Args:
        item (str | pathlib.Path): path of folder to examine.
        elements (list[str | pathlib.Path]): list of paths to test whether they 
            are in 'item'.
        
    Returns:
        bool: whether all 'elements' are in 'item'.
        
    """ 
    item = camina.pathlibify(item)
    paths = acquire.get_paths(item, recursive = False)
    elements = [camina.pahlibify(p) for p in elements]
    return all(elements in paths)
   
def has_paths(
    item: str | pathlib.Path,
    elements: list[str | pathlib.Path]) -> bool:  
    """Returns whether all 'elements' are in 'item'.
  
    Args:
        item (str | pathlib.Path): path of folder to examine.
        elements (list[str | pathlib.Path]): list of paths to test whether they 
            are in 'item'.
        
    Returns:
        bool: whether all 'elements' are in 'item'.
        
    """ 
    item = camina.pathlibify(item)
    paths = acquire.get_paths(item, recursive = False)
    elements = [camina.pahlibify(p) for p in elements]
    return all(elements in paths)
   
def has_properties(
    item: object | Type[Any], 
    properties: str | MutableSequence[str]) -> bool:
    """Returns whether 'item' has 'properties' which are properties.

    Args:
        item (object | Type[Any]): class or instance to examine.
        properties (MutableSequence[str]): names of properties to check to see 
            if they exist in 'item' and are property type.
            
    Returns:
        bool: whether all 'properties' exist in 'items'.
        
    """
    properties = list(camina.iterify(properties))
    return all(identify.is_property(item, attribute = p) for p in properties)
    
def has_signatures(
    item: object | Type[Any], 
    signatures: Mapping[str, inspect.Signature]) -> bool:
    """Returns whether 'item' has 'signatures' of its methods.

    Args:
        item (object | Type[Any]): class or instance to examine.
        signatures (Mapping[str, inspect.Signature]): keys are the names of 
            methods and values are the corresponding method signatures.
            
    Returns:
        bool: whether all 'signatures' exist in 'items'.
        
    """
    keys = [a for a in dir(item) if identify.is_method(item, attribute = a)]
    values = [inspect.signature(getattr(item, m)) for m in keys]
    item_signatures = dict(zip(keys, values))
    pass_test = True
    for name, parameters in signatures.items():
        if (name not in item_signatures or item_signatures[name] != parameters):
            pass_test = False
    return pass_test
   
def has_traits(
    item: object | Type[Any],
    attributes: Optional[MutableSequence[str]] = None,
    methods: Optional[MutableSequence[str]] = None,
    properties: Optional[MutableSequence[str]] = None) -> bool:
    """Returns if 'item' has 'attributes', 'methods' and 'properties'.

    Args:
        item (object | Type[Any]): class or instance to examine.
        attributes (MutableSequence[str]): names of attributes to check to see
            if they exist in 'item'.
        methods (MutableSequence[str]): name(s) of methods to check to see if 
            they exist in 'item' and are types.MethodType.          
        properties (MutableSequence[str]): names of properties to check to see 
            if they exist in 'item' and are property type.
                          
    Returns:
        bool: whether all passed arguments exist in 'items'.    
    
    """
    if not inspect.isclass(item):
        item.__class__ 
    attributes = attributes or []
    methods = methods or []
    properties = properties or []
    signatures = signatures or {}
    return (
        has_attributes(item, attributes = attributes)
        and has_methods(item, methods = methods)
        and has_properties(item, properties = properties)
        and has_signatures(item, signatures = signatures))
  
@functools.singledispatch
def has_contents(
    item: object, /,
    contents: Type[Any] | tuple[Type[Any], ...]) -> bool:
    """Returns whether 'item' contains the type(s) in 'contents'.

    Args:
        item (object): item to examine.
        contents (Type[Any] | tuple[Type[Any], ...]): types to check for in 
            'item' contents.
        
    Raises:
        TypeError: if 'item' does not match any of the registered types.
        
    Returns:
        bool: whether 'item' holds the types in 'contents'.
        
    """
    raise TypeError(f'item {item} is not supported by {__name__}')

@has_contents.register(Mapping)    
def has_contents_dict(
    item: Mapping[Hashable, Any], /, 
    contents: tuple[Type[Any] | tuple[Type[Any], ...],
                    Type[Any] | tuple[Type[Any], ...]]) -> bool:
    """Returns whether dict 'item' contains the type(s) in 'contents'.

    Args:
        item (Mapping[Hashable, Any]): item to examine.
        contents (tuple[Type[Any] | tuple[Type[Any], ...], Type[Any] | 
            tuple[Type[Any], ...]]): types to check for in 'item' contents.

    Returns:
        bool: whether 'item' holds the types in 'contents'.
        
    """
    return (
        has_contents_serial(item.keys(), contents = contents[0])
        and has_contents_serial(item.values(), contents = contents[1]))

@has_contents.register(MutableSequence)   
def has_contents_list(
    item: MutableSequence[Any], /,
    contents: Type[Any] | tuple[Type[Any], ...]) -> bool:
    """Returns whether list 'item' contains the type(s) in 'contents'.

    Args:
        item (MutableSequence[Any]): item to examine.
        contents (Type[Any] | tuple[Type[Any], ...]): types to check for in 
            'item' contents.

    Returns:
        bool: whether 'item' holds the types in 'contents'.
        
    """
    return has_contents_serial(item, contents = contents)

@has_contents.register(Set)   
def has_contents_set(
    item: Set[Any], /,
    contents: Type[Any] | tuple[Type[Any], ...]) -> bool:
    """Returns whether list 'item' contains the type(s) in 'contents'.

    Args:
        item (Set[Any]): item to examine.
        contents (Type[Any] | tuple[Type[Any], ...]): types to check for in 
            'item' contents.

    Returns:
        bool: whether 'item' holds the types in 'contents'.
        
    """
    return has_contents_serial(item, contents = contents)

@has_contents.register(tuple)   
def has_contents_tuple(
    item: tuple[Any, ...], /,
    contents: Type[Any] | tuple[Type[Any], ...]) -> bool:
    """Returns whether tuple 'item' contains the type(s) in 'contents'.

    Args:
        item (tuple[Any, ...]): item to examine.
        contents (Type[Any] | tuple[Type[Any], ...]): types to check for in 
            'item' contents.

    Returns:
        bool: whether 'item' holds the types in 'contents'.
        
    """
    if isinstance(contents, tuple) and len(item) == len(contents):
        technique = has_contents_parallel
    else:
        technique = has_contents_serial
    return technique(item, contents = contents)

@has_contents.register(Sequence)   
def has_contents_parallel(
    item: Sequence[Any], /,
    contents: tuple[Type[Any], ...]) -> bool:
    """Returns whether parallel 'item' contains the type(s) in 'contents'.

    Args:
        item (Sequence[Any]): item to examine.
        contents (tuple[Type[Any], ...]): types to check for in 'item' contents.

    Returns:
        bool: whether 'item' holds the types in 'contents'.
        
    """
    return all(isinstance(item[i], contents[i]) for i in enumerate(item))

@has_contents.register(Container)       
def has_contents_serial(
    item: Container[Any], /,
    contents: Type[Any] | tuple[Type[Any], ...]) -> bool:
    """Returns whether serial 'item' contains the type(s) in 'contents'.

    Args:
        item (Container[Any]): item to examine.
        contents (Type[Any] | tuple[Type[Any], ...]): types to check for in 
            'item' contents.

    Returns:
        bool: whether 'item' holds the types in 'contents'.
        
    """
    return all(isinstance(i, contents) for i in item)
