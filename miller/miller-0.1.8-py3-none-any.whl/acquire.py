"""
acquire: returns introspection information in lists of introspected items
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
        label.name_attributes
        label.name_methods
        label.name_parameters
        label.name_properties
        label.name_variables
    Module Reporters:
        get_classes
        get_functions
        label.name_classes
        label.name_functions   

        
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
from . import label

   
""" Class and Instance Reporters """   
     
def get_annotations(
    item: object | types.ModuleType, 
    include_private: bool = False) -> dict[str, Type[Any]]:
    """Returns dict of attributes of 'item' with type annotations.
    
    This function follows the best practices suggested for compatibility with
    Python 3.9 and before (without relying on the newer functionality of 3.10):
    https://docs.python.org/3/howto/annotations.html
    
    Args:
        item (object): instance to examine.
        include_private (bool): whether to include items that begin with '_'
            (True) or to exclude them (False). Defauls to False.
                        
    Returns:
        dict[str, Any]: dict of attributes in 'item' (keys are attribute names 
            and values are type annotations) that are type annotated.
            
    """
    if isinstance(item, type):
        annotations = item.__dict__.get('__annotations__', None)
    else:
        annotations = getattr(item, '__annotations__', None)
    if include_private:
        return annotations
    else:
        return {k: v for k, v in annotations.items() if not k.startswith('_')}

def get_attributes(
    item: object, 
    include_private: bool = False) -> dict[str, Any]:
    """Returns dict of attributes of 'item'.
    
    Args:
        item (Any): item to examine.
        include_private (bool): whether to include items that begin with '_'
            (True) or to exclude them (False). Defauls to False.
                        
    Returns:
        dict[str, Any]: dict of attributes in 'item' (keys are attribute names 
            and values are attribute values).
            
    """
    attributes = label.name_attributes(item, include_private = include_private)
    values = [getattr(item, m) for m in attributes]
    return dict(zip(attributes, values))

def get_fields(
    item: dataclasses.dataclass | Type[dataclasses.dataclass], 
    include_private: bool = False) -> dict[str, dataclasses.Field]:
    """Returns whether 'attributes' exist in dataclass 'item'.

    Args:
        item (dataclasses.dataclass | Type[dataclasses.dataclass]): dataclass or 
            dataclass instance to examine.
        include_private (bool): whether to include items that begin with '_'
            (True) or to exclude them (False). Defauls to False.    
    Raises:
        TypeError: if 'item' is not a dataclass.
        
    Returns:
        dict[str, dataclasses.Field]: dict of fields in 'item' (keys are 
            attribute names and values are dataclass fields).
    
    """
    if dataclasses.identify.is_dataclass(item):
        attributes = {f.name: f for f in dataclasses.fields(item)}
        if not include_private:
            attributes = camina.drop_privates(attributes)
        return attributes
    else:
        raise TypeError('item must be a dataclass')
    
def get_methods(
    item: object | Type[Any], 
    include_private: bool = False) -> dict[str, types.MethodType]:
    """Returns dict of methods of 'item'.
    
    Args:
        item (object | Type[Any]): class or instance to examine.
        include_private (bool): whether to include items that begin with '_'
            (True) or to exclude them (False). Defauls to False.

    Returns:
        dict[str, types.MethodType]: dict of methods in 'item' (keys are method 
            names and values are methods).
        
    """ 
    methods = label.name_methods(item, include_private = include_private)
    return [getattr(item, m) for m in methods]

def get_properties(
    item: object, 
    include_private: bool = False) -> dict[str, Any]:
    """Returns properties of 'item'.

    Args:
        item (object): instance to examine.
        include_private (bool): whether to include items that begin with '_'
            (True) or to exclude them (False). Defauls to False.

    Returns:
        dict[str, Any]: dict of properties in 'item' (keys are property names 
            and values are property values).
        
    """    
    properties = label.name_properties(item, include_private = include_private)
    values = [getattr(item, p) for p in properties]
    return dict(zip(properties, values))

def get_signatures(
    item: object | Type[Any], 
    include_private: bool = False) -> dict[str, inspect.Signature]:
    """Returns dict of method signatures of 'item'.

    Args:
        item (object | Type[Any]): class or instance to examine.
        include_private (bool): whether to include items that begin with '_'
            (True) or to exclude them (False). Defauls to False.

    Returns:
        dict[str, inspect.Signature]: dict of method signatures in 'item' (keys 
            are method names and values are method signatures).
                   
    """ 
    methods = label.name_methods(item, include_private = include_private)
    signatures = [inspect.signature(getattr(item, m)) for m in methods]
    return dict(zip(methods, signatures))

def get_variables(
    item: object, 
    include_private: bool = False) -> dict[str, Any]:
    """Returns dict of attributes of 'item' that are not methods or properties.
    
    Args:
        item (object): instance to examine.
        include_private (bool): whether to include items that begin with '_'
            (True) or to exclude them (False). Defauls to False.
                        
    Returns:
        dict[str, Any]: dict of attributes in 'item' (keys are attribute names 
            and values are attribute values) that are not methods or properties.
            
    """
    attributes = label.name_attributes(item, include_private = include_private)
    methods = label.name_methods(item, include_private = include_private)
    properties = label.name_properties(item, include_private = include_private)
    variables = [
        a for a in attributes if a not in methods and a not in properties]
    values = [getattr(item, m) for m in variables]
    return dict(zip(variables, values))

""" Module Reporters """
          
def get_classes(
    item: types.ModuleType | str, 
    include_private: bool = False) -> list[Type[Any]]:
    """Returns list of classes in 'item'.
    
    Args:
        item (types.ModuleType | str): module or its name to inspect.
        include_private (bool): whether to include items that begin with '_'
            (True) or to exclude them (False). Defauls to False.
        
    Returns:
        list[Type[Any]]: list of classes in 'item'.
        
    """
    if isinstance(item, str):
        item = sys.modules[item]
    classes = [
        m[1] for m in inspect.getmembers(item, inspect.isclass)
        if m[1].__module__ == item.__label.name__]
    if not include_private:
        classes = camina.drop_privates(classes)
    return classes
        
def get_functions(
    item: types.ModuleType | str, 
    include_private: bool = False) -> list[types.FunctionType]:
    """Returns list of functions in 'item'.
    
    Args:
        item (types.ModuleType | str): module or its name to inspect.
        include_private (bool): whether to include items that begin with '_'
            (True) or to exclude them (False). Defauls to False.
        
    Returns:
        list[Type[types.FunctionType]]: list of functions in 'item'.
        
    """
    if isinstance(item, str):
        item = sys.modules[item]
    functions = [
        m[1] for m in inspect.getmembers(item, inspect.isfunction)
        if m[1].__module__ == item.__label.name__]
    if not include_private:
        functions = camina.drop_privates(functions)
    return functions 
    
def get_files(
    item: str | pathlib.Path, 
    recursive: Optional[bool] = None,
    suffix: Optional[str] = '*') -> list[pathlib.Path]:  
    """Returns list of non-python module file paths in 'item'.
    
    Args:
        item (str | pathlib.Path): path of folder to examine. 
        recursive (Optional[bool]): whether to include subfolders. Defaults to 
            None. If 'recursive' is None, 'defaults.RECURSIVE' is used.
        suffix (Optional[str]): file suffix to match. Defaults to '*' (all 
            suffixes).
        
    Returns:
        list[pathlib.Path]: a list of file paths in 'item'.
        
    """
    if recursive is None:
        recursive = rules.RECURSIVE   
    paths = get_paths(item, recursive = recursive, suffix = suffix)
    return [p for p in paths if identify.is_file(item = p)]

def get_folders(
    item: str | pathlib.Path,
    recursive: Optional[bool] = None) -> list[pathlib.Path]:  
    """Returns list of folder paths in 'item'.
    
    Args:
        item (str | pathlib.Path): path of folder to examine.
        recursive (bool): whether to include subfolders. Defaults to None. If
            'recursive' is None, 'defaults.RECURSIVE' is used.
        
    Returns:
        list[pathlib.Path]: a list of folder paths in 'item'.
        
    """
    if recursive is None:
        recursive = rules.RECURSIVE   
    paths = get_paths(item, recursive = recursive)
    return [p for p in paths if identify.is_folder(item = p)]

def get_modules(
    item: str | pathlib.Path,
    recursive: Optional[bool] = None,
    import_modules: Optional[bool] = False) -> (
        list[pathlib.Path |types.ModuleType]):  
    """Returns list of python module paths in 'item'.
    
    Args:
        item (str | pathlib.Path): path of folder to examine.
        recursive (bool): whether to include subfolders. Defaults to None. If
            'recursive' is None, 'defaults.RECURSIVE' is used.
        import_modules (Optional[bool]): whether the values in the returned dict
            should be imported modules (True) or file paths to modules (False).
                    
    Returns:
        list[pathlib.Path |types.ModuleType]: a list of python module paths in 
            'item' or imported modules if 'import_modules' is True.
            
    """
    if recursive is None:
        recursive = rules.RECURSIVE   
    paths = get_paths(item, recursive = recursive)
    modules = [p for p in paths if identify.is_module(item = p)]
    if import_modules:
        modules = [nagata.from_file_path(path = p) for p in modules]
    return modules
    
def get_paths(
    item: str | pathlib.Path, 
    recursive: Optional[bool] = None,
    suffix: Optional[str] = '*') -> list[pathlib.Path]:  
    """Returns list of all paths in 'item'.
    
    Args:
        item (str | pathlib.Path): path of folder to examine. 
        recursive (Optional[bool]): whether to include subfolders. Defaults to 
            None. If 'recursive' is None, 'defaults.RECURSIVE' is used.
        suffix (Optional[str]): file suffix to match. Defaults to '*' (all 
            suffixes).
        
    Returns:
        list[pathlib.Path]: a list of all paths in 'item'.
        
    """
    if recursive is None:
        recursive = rules.RECURSIVE   
    item = camina.pathlibify(item) 
    if recursive:
        return list(item.rglob(f'*.{suffix}'))
    else:
        return list(item.glob(f'*.{suffix}'))
   
      
""" Class and Instance Reporters """   
     
def get_annotations(
    item: object, 
    include_private: bool = False) -> dict[str, Type[Any]]:
    """Returns dict of attributes of 'item' with type annotations.
    
    Args:
        item (object): instance to examine.
        include_private (bool): whether to include items that begin with '_'
            (True) or to exclude them (False). Defauls to False.
                        
    Returns:
        dict[str, Any]: dict of attributes in 'item' (keys are attribute names 
            and values are type annotations) that are type annotated.
            
    """
    annotations = item.__annotations__
    if include_private:
        return annotations
    else:
        return {k: v for k, v in annotations.items() if not k.startswith('_')}

def get_attributes(
    item: object, 
    include_private: bool = False) -> dict[str, Any]:
    """Returns dict of attributes of 'item'.
    
    Args:
        item (Any): item to examine.
        include_private (bool): whether to include items that begin with '_'
            (True) or to exclude them (False). Defauls to False.
                        
    Returns:
        dict[str, Any]: dict of attributes in 'item' (keys are attribute names 
            and values are attribute values).
            
    """
    attributes = label.name_attributes(item, include_private = include_private)
    values = [getattr(item, m) for m in attributes]
    return dict(zip(attributes, values))

def get_fields(
    item: dataclasses.dataclass | Type[dataclasses.dataclass], 
    include_private: bool = False) -> dict[str, dataclasses.Field]:
    """Returns whether 'attributes' exist in dataclass 'item'.

    Args:
        item (dataclasses.dataclass | Type[dataclasses.dataclass]): dataclass or 
            dataclass instance to examine.
        include_private (bool): whether to include items that begin with '_'
            (True) or to exclude them (False). Defauls to False.    
    Raises:
        TypeError: if 'item' is not a dataclass.
        
    Returns:
        dict[str, dataclasses.Field]: dict of fields in 'item' (keys are 
            attribute names and values are dataclass fields).
    
    """
    if dataclasses.identify.is_dataclass(item):
        attributes = {f.name: f for f in dataclasses.fields(item)}
        if not include_private:
            attributes = camina.drop_privates(attributes)
        return attributes
    else:
        raise TypeError('item must be a dataclass')
    
def get_methods(
    item: object | Type[Any], 
    include_private: bool = False) -> dict[str, types.MethodType]:
    """Returns dict of methods of 'item'.
    
    Args:
        item (object | Type[Any]): class or instance to examine.
        include_private (bool): whether to include items that begin with '_'
            (True) or to exclude them (False). Defauls to False.

    Returns:
        dict[str, types.MethodType]: dict of methods in 'item' (keys are method 
            names and values are methods).
        
    """ 
    methods = label.name_methods(item, include_private = include_private)
    return [getattr(item, m) for m in methods]

def get_properties(
    item: object, 
    include_private: bool = False) -> dict[str, Any]:
    """Returns properties of 'item'.

    Args:
        item (object): instance to examine.
        include_private (bool): whether to include items that begin with '_'
            (True) or to exclude them (False). Defauls to False.

    Returns:
        dict[str, Any]: dict of properties in 'item' (keys are property names 
            and values are property values).
        
    """    
    properties = label.name_properties(item, include_private = include_private)
    values = [getattr(item, p) for p in properties]
    return dict(zip(properties, values))

def get_signatures(
    item: object | Type[Any], 
    include_private: bool = False) -> dict[str, inspect.Signature]:
    """Returns dict of method signatures of 'item'.

    Args:
        item (object | Type[Any]): class or instance to examine.
        include_private (bool): whether to include items that begin with '_'
            (True) or to exclude them (False). Defauls to False.

    Returns:
        dict[str, inspect.Signature]: dict of method signatures in 'item' (keys 
            are method names and values are method signatures).
                   
    """ 
    methods = label.name_methods(item, include_private = include_private)
    signatures = [inspect.signature(getattr(item, m)) for m in methods]
    return dict(zip(methods, signatures))

def get_variables(
    item: object, 
    include_private: bool = False) -> dict[str, Any]:
    """Returns dict of attributes of 'item' that are not methods or properties.
    
    Args:
        item (object): instance to examine.
        include_private (bool): whether to include items that begin with '_'
            (True) or to exclude them (False). Defauls to False.
                        
    Returns:
        dict[str, Any]: dict of attributes in 'item' (keys are attribute names 
            and values are attribute values) that are not methods or properties.
            
    """
    attributes = label.name_attributes(item, include_private = include_private)
    methods = label.name_methods(item, include_private = include_private)
    properties = label.name_properties(item, include_private = include_private)
    variables = [
        a for a in attributes if a not in methods and a not in properties]
    values = [getattr(item, m) for m in variables]
    return dict(zip(variables, values))

def get_classes(
    item: types.ModuleType | str, 
    include_private: bool = False) -> list[Type[Any]]:
    """Returns list of classes in 'item'.
    
    Args:
        item (types.ModuleType | str): module or its name to inspect.
        include_private (bool): whether to include items that begin with '_'
            (True) or to exclude them (False). Defauls to False.
        
    Returns:
        list[Type[Any]]: list of classes in 'item'.
        
    """
    if isinstance(item, str):
        item = sys.modules[item]
    classes = [
        m[1] for m in inspect.getmembers(item, inspect.isclass)
        if m[1].__module__ == item.__name__]
    if not include_private:
        classes = camina.drop_privates(classes)
    return classes
        
def get_functions(
    item: types.ModuleType | str, 
    include_private: bool = False) -> list[types.FunctionType]:
    """Returns list of functions in 'item'.
    
    Args:
        item (types.ModuleType | str): module or its name to inspect.
        include_private (bool): whether to include items that begin with '_'
            (True) or to exclude them (False). Defauls to False.
        
    Returns:
        list[Type[types.FunctionType]]: list of functions in 'item'.
        
    """
    if isinstance(item, str):
        item = sys.modules[item]
    functions = [
        m[1] for m in inspect.getmembers(item, inspect.isfunction)
        if m[1].__module__ == item.__name__]
    if not include_private:
        functions = camina.drop_privates(functions)
    return functions 


@functools.singledispatch
def get_types(item: object) -> Optional[
    tuple[Type[Any], ...] |
    tuple[tuple[Type[Any], ...], tuple[Type[Any], ...]]]:
    """Returns types contained in 'item'.

    Args:
        item (object): item to examine.
    
    Returns:
        Optional[Union[tuple[Type[Any], ...], tuple[tuple[Type[Any], ...], 
            tuple[Type[Any], ...]]]]:: returns the types of things contained 
            in 'item'. Returns None if 'item' is not a container.
        
    """
    raise TypeError(f'item {item} is not supported by {__name__}')

@get_types.register(Mapping)  
def get_types_dict(
    item: Mapping[Hashable, Any]) -> Optional[
        tuple[tuple[Type[Any], ...], tuple[Type[Any], ...]]]:
    """Returns types contained in 'item'.

    Args:
        item (object): item to examine.
    
    Returns:
        Optional[tuple[Type[Any], ...]]: returns the types of things contained 
            in 'item'. Returns None if 'item' is not a container.
        
    """
    if isinstance(item, Mapping):
        key_types = get_types_sequence(item.keys())
        value_types = get_types_sequence(item.values())
        return tuple([key_types, value_types])
    else:
        return None

@get_types.register(MutableSequence)  
def get_types_list(item: list[Any]) -> Optional[tuple[Type[Any], ...]]:
    """Returns types contained in 'item'.

    Args:
        item (list[Any]): item to examine.
    
    Returns:
        Optional[tuple[Type[Any], ...]]: returns the types of things contained 
            in 'item'. Returns None if 'item' is not a container.
        
    """
    if isinstance(item, list):
        key_types = get_types_sequence(item.keys())
        value_types = get_types_sequence(item.values())
        return tuple([key_types, value_types])
    else:
        return None

@get_types.register(Sequence)    
def get_types_sequence(item: Sequence[Any]) -> Optional[tuple[Type[Any], ...]]:
    """Returns types contained in 'item'.

    Args:
        item (Sequence[Any]): item to examine.
    
    Returns:
        Optional[tuple[Type[Any], ...]]: returns the types of things contained 
            in 'item'. Returns None if 'item' is not a container.
        
    """
    if isinstance(item, Sequence):
        all_types = []
        for thing in item:
            kind = type(thing)
            if not kind in all_types:
                all_types.append(kind)
        return tuple(all_types)
    else:
        return None

