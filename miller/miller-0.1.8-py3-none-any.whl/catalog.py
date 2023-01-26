"""
catalog: returns introspection information in dics
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
    label.name_files
    label.name_folders
    label.name_modules
    label.name_paths  
          
To Do:

    
"""
from __future__ import annotations
import pathlib
import types
from typing import Optional

import camina
import nagata

from . import rules
from . import label
from . import acquire


def map_files(
    item: str | pathlib.Path,
    recursive: Optional[bool] = None) -> dict[str, pathlib.Path]:  
    """Returns dict of python file names and file paths in 'item'.
    
    Args:
        item (str | pathlib.Path): path of folder to examine.
        recursive (Optional[bool]): whether to include subfolders. Defaults to 
            None. If 'recursive' is None, 'defaults.RECURSIVE' is used.
        
    Returns:
        dict[dict[str, pathlib.Path]: dict with keys being file names and values
            being file paths. 
        
    """
    if recursive is None:
        recursive = rules.RECURSIVE   
    kwargs = {'item': item, 'recursive': recursive}
    names = label.name_files(**kwargs)
    files = acquire.get_files(**kwargs)
    return dict(zip(names, files))

def map_folders(
    item: str | pathlib.Path,
    recursive: Optional[bool] = None) -> dict[str, pathlib.Path]:  
    """Returns dict of python folder names and folder paths in 'item'.
    
    Args:
        item (str | pathlib.Path): path of folder to examine.
        recursive (Optional[bool]): whether to include subfolders. Defaults to 
            None. If 'recursive' is None, 'defaults.RECURSIVE' is used.
        
    Returns:
        dict[dict[str, pathlib.Path]: dict with keys being folder names and 
            values being folder paths. 
        
    """
    if recursive is None:
        recursive = rules.RECURSIVE   
    kwargs = {'item': item, 'recursive': recursive}
    names = label.name_folders(**kwargs)
    folders = acquire.get_folders(**kwargs)
    return dict(zip(names, folders))

def map_modules(
    item: str | pathlib.Path,
    recursive: Optional[bool] = None,
    import_modules: Optional[bool] = False) -> (
        dict[str, types.ModuleType] | dict[str, pathlib.Path]):  
    """Returns dict of python module names and modules in 'item'.
    
    Args:
        item (str | pathlib.Path): path of folder to examine.
        recursive (Optional[bool]): whether to include subfolders. Defaults to 
            None. If 'recursive' is None, 'defaults.RECURSIVE' is used.
        import_modules (Optional[bool]): whether the values in the returned dict
            should be imported modules (True) or file paths to modules (False).
        
    Returns:
        dict[str, types.ModuleType] | dict[str, pathlib.Path]: dict with str key 
            names of python modules and values as the paths to corresponding 
            modules or the imported modules (if 'import_modules' is True).
        
    """
    if recursive is None:
        recursive = rules.RECURSIVE   
    kwargs = {'item': item, 'recursive': recursive}
    names = label.name_modules(**kwargs)
    modules = acquire.get_modules(**kwargs, import_modules = import_modules)
    return dict(zip(names, modules))

def map_paths(
    item: str | pathlib.Path,
    recursive: Optional[bool] = None) -> dict[str, pathlib.Path]:  
    """Returns dict of python path names and paths in 'item'.
    
    Args:
        item (str | pathlib.Path): path of folder to examine.
        recursive (Optional[bool]): whether to include subfolders. Defaults to 
            None. If 'recursive' is None, 'defaults.RECURSIVE' is used.
        
    Returns:
        dict[dict[str, pathlib.Path]: dict with keys being paht names and values
            being paths. 
        
    """
    if recursive is None:
        recursive = rules.RECURSIVE   
    kwargs = {'item': item, 'recursive': recursive}
    names = label.name_paths(**kwargs)
    paths = acquire.get_paths(**kwargs)
    return dict(zip(names, paths))
