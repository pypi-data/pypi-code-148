"""
label: returns introspection information in lists of names of introspected items
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
    Container Reporters:
        get_types
        get_types_dict
        get_types_list
        get_types_sequence
    Class and Instance Reporters:
        get_annotations
        get_attributes
        get_methods
        get_properties
        get_signatures
        get_variables
        name_attributes
        name_methods
        name_parameters
        name_properties
        name_variables
    Module Reporters:
        get_classes
        get_functions
        name_classes
        name_functions   

        
ToDo:
    Add support for Kinds once that system is complete.

"""
from __future__ import annotations
from collections.abc import (
    Container, Hashable, Iterable, Mapping, MutableSequence, Sequence, Set)
import dataclasses
import functools
import inspect
import pathlib
import sys
import types
from typing import Any, Optional, Type

import camina
import nagata

from . import rules
from . import identify
from . import acquire


def name_attributes(
    item: object | Type[Any], 
    include_private: bool = False) -> list[str]:
    """Returns attribute names of 'item'.
    
    Args:
        item (object | Type[Any]): item to examine.
        include_private (bool): whether to include items that begin with '_'
            (True) or to exclude them (False). Defauls to False.
                        
    Returns:
        list[str]: names of attributes in 'item'.
            
    """
    names = dir(item)
    if not include_private:
        names = camina.drop_privates(names)
    return names

def name_fields(
    item: dataclasses.dataclass | Type[dataclasses.dataclass], 
    include_private: bool = False) -> list[str]:
    """Returns whether 'attributes' exist in dataclass 'item'.

    Args:
        item (dataclasses.dataclass | Type[dataclasses.dataclass]): dataclass or 
            dataclass instance to examine.
        include_private (bool): whether to include items that begin with '_'
            (True) or to exclude them (False). Defauls to False.    
    Raises:
        TypeError: if 'item' is not a dataclass.
        
    Returns:
        list[str]: names of fields in 'item'.
    
    """
    if dataclasses.is_dataclass(item):
        attributes = [f.name for f in dataclasses.fields(item)]
        if not include_private:
            attributes = camina.drop_privates(attributes)
        return attributes
    else:
        raise TypeError('item must be a dataclass')

def name_files(
    item: str | pathlib.Path,
    recursive: Optional[bool] = None) -> list[str]:  
    """Returns list of names of non-python-module file paths in 'item'.
    
    The 'stem' property of 'pathlib.Path' is used for the names.
        
    Args:
        item (str | pathlib.Path): path of folder to examine.
        recursive (bool): whether to include subfolders. Defaults to None. If
            'recursive' is None, 'defaults.RECURSIVE' is used.
        
    Returns:
        list[str]: a list of names of non-python-module file paths in 'item'.
        
    """
    if recursive is None:
        recursive = rules.RECURSIVE   
    item = camina.pathlibify(item)
    kwargs = {'item': item, 'recursive': recursive}
    return [p.stem for p in acquire.get_files(**kwargs)]
          
def name_folders(
    item: str | pathlib.Path,
    recursive: Optional[bool] = None) -> list[str]:  
    """Returns list of names of folder paths in 'item'.
    
    Args:
        item (str | pathlib.Path): path of folder to examine.
        recursive (bool): whether to include subfolders. Defaults to None. If
            'recursive' is None, 'defaults.RECURSIVE' is used.
        
    Returns:
        list[str]: a list of folder paths in 'item'.
        
    """
    if recursive is None:
        recursive = rules.RECURSIVE   
    item = camina.pathlibify(item)
    kwargs = {'item': item, 'recursive': recursive}
    return [p.name for p in acquire.get_folders(**kwargs)]
       
def name_methods(
    item: object | Type[Any], 
    include_private: bool = False) -> list[str]:
    """Returns method names of 'item'.
    
    Args:
        item (object | Type[Any]): item to examine.
        include_private (bool): whether to include items that begin with '_'
            (True) or to exclude them (False). Defauls to False.
                        
    Returns:
        list[str]: names of methods in 'item'.
            
    """
    methods = [
        a for a in dir(item)
        if identify.is_method(item, attribute = a)]
    if not include_private:
        methods = camina.drop_privates(methods)
    return methods
      
def name_modules(
    item: str | pathlib.Path,
    recursive: Optional[bool] = None) -> list[str]:  
    """Returns list of names of paths to python modules in 'item'.
    
    The 'stem' property of 'pathlib.Path' is used for the names.
    
    Args:
        item (str | pathlib.Path): path of folder to examine.
        recursive (bool): whether to include subfolders. Defaults to None. If
            'recursive' is None, 'defaults.RECURSIVE' is used.
        
    Returns:
        list[str]: a list of names of paths to python modules in 'item'.
        
    """
    if recursive is None:
        recursive = rules.RECURSIVE   
    item = camina.pathlibify(item)
    kwargs = {'item': item, 'recursive': recursive}
    return [p.stem for p in acquire.get_modules(**kwargs)]
  
def name_parameters(item: Type[Any]) -> list[str]:
    """Returns list of parameters based on annotations of 'item'.

    Args:
        item (Type[Any]): class to get parameters to.

    Returns:
        list[str]: names of parameters in 'item'.
        
    """          
    return list(item.__annotations__.keys())
 
def name_paths(
    item: str | pathlib.Path,
    recursive: Optional[bool] = None) -> list[str]:  
    """Returns list of names of paths in 'item'.
    
    For folders, the 'name' property of 'pathlib.Path' is used. For files, the
    'stem' property is.
    
    Args:
        item (str | pathlib.Path): path of folder to examine.
        recursive (bool): whether to include subfolders. Defaults to None. If
            'recursive' is None, 'defaults.RECURSIVE' is used.
        
    Returns:
        list[str]: a list of names of paths in 'item'.
        
    """
    if recursive is None:
        recursive = rules.RECURSIVE   
    kwargs = {'item': item, 'recursive': recursive}
    return (
        name_files(**kwargs) 
        + name_folders(**kwargs) 
        + name_modules(**kwargs))

def name_properties(
    item: object | Type[Any], 
    include_private: bool = False) -> list[str]:
    """Returns method names of 'item'.
    
    Args:
        item (object | Type[Any]): item to examine.
        include_private (bool): whether to include items that begin with '_'
            (True) or to exclude them (False). Defauls to False.
                        
    Returns:
        list[str]: names of properties in 'item'.
            
    """
    if not inspect.isclass(item):
        item.__class__
    properties = [
        a for a in dir(item)
        if identify.is_property(item, attribute = a)]
    if not include_private:
        properties = camina.drop_privates(properties)
    return properties

def name_variables(
    item: object | Type[Any], 
    include_private: bool = False) -> list[str]:
    """Returns variable names of 'item'.
    
    Args:
        item (object | Type[Any]): item to examine.
        include_private (bool): whether to include items that begin with '_'
            (True) or to exclude them (False). Defauls to False.
                        
    Returns:
        list[str]: names of attributes in 'item' that are neither methods nor
            properties.
            
    """
    names = [
        a for a in dir(item) 
        if identify.is_variable(item, attribute = a)]
    if not include_private:
        names = camina.drop_privates(names)
    return names
  
def name_classes(
    item: types.ModuleType | str, 
    include_private: bool = False) -> list[str]:
    """Returns list of string names of classes in 'item'.
    
    Args:
        item (types.ModuleType | str): module or its name to inspect.
        include_private (bool): whether to include items that begin with '_'
            (True) or to exclude them (False). Defauls to False.
        
    Returns:
        list[Type[types.FunctionType]]: list of functions in 'item'.
        
    """
    if isinstance(item, str):
        item = sys.modules[item]
    names = [    
        m[0] for m in inspect.getmembers(item, inspect.isclass)
        if m[1].__module__ == item.__name__]
    if not include_private:
        names = camina.drop_privates(names)
    return names
       
def name_functions(
    item: types.ModuleType | str, 
    include_private: bool = False) -> list[str]:
    """Returns list of string names of functions in 'item'.
    
    Args:
        item (types.ModuleType | str): module or its name to inspect.
        include_private (bool): whether to include items that begin with '_'
            (True) or to exclude them (False). Defauls to False.
        
    Returns:
        list[Type[types.FunctionType]]: list of functions in 'item'.
        
    """
    if isinstance(item, str):
        item = sys.modules[item]
    names = [
        m[0] for m in inspect.getmembers(item, inspect.isfunction)
        if m[1].__module__ == item.__name__]
    if not include_private:
        names = camina.drop_privates(names)
    return names
