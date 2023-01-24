import os
from enum import Enum
from typing import List, Union


class SizeUnits(Enum):
    B  = 0
    KB = 1
    MB = 2
    GB = 3
    TB = 4


class AttributeNotInitialized:
    pass


class AttributeChangeError(Exception):
    pass


class ReadOnlyDescriptor:
    def __set_name__(self, cls, name):
        self.name = name
    def __get__(self, obj, cls):
        return obj.__dict__[self.name]
    def __set__(self, obj, value):
        if obj.__dict__.get(self.name, AttributeNotInitialized) == AttributeNotInitialized:
            obj.__dict__[self.name] = value
        else:
            raise AttributeChangeError(f'Attribute {self.name} cannot be changed.')


class PathAnalyser:
    '''
    Class Attributes:
        full_path 
            entire path including provided object \n
        dir_path 
            entire path of the directory where the provided object is stored
        dir_name 
            only the name of the directory where the provided object is stored
        is_folder 
            returns True if the provided object is a folder
        is_file 
            returns True if the provided object is a file
        name_extended 
            object name with extension
        name 
            this variable holds only the name of the provided object
        extension 
            extension of the object (file extension with a "." as prefix)
    '''
    full_path = ReadOnlyDescriptor()
    dir_path = ReadOnlyDescriptor()
    dir_name = ReadOnlyDescriptor()
    is_folder = ReadOnlyDescriptor()
    is_file = ReadOnlyDescriptor()
    size = ReadOnlyDescriptor()
    name_extended = ReadOnlyDescriptor()
    name = ReadOnlyDescriptor()
    extension = ReadOnlyDescriptor()

    def __init__(self, pathobject: str, current_file: Union[str, None] = None):
        '''
        The parameter pathobject should be the entire path including the object itself. If pathobject is an object 
        in the same directory than just the file name can be assigned to the pathobject. In this case the current_file 
        must be filled with the value of the global variable __file__.
        '''

        if len(pathobject.split(os.path.sep)) == 1:
            if current_file:
                pathobject = os.path.join(os.path.dirname(current_file), pathobject)
            else:
                raise ValueError(f'Object {pathobject} must be the entire path including the object.')
        
        if not os.path.exists(pathobject):
            raise ValueError(f'Object {pathobject} does not exist.')
        
        self.full_path = pathobject
        self.dir_path = os.path.dirname(self.full_path)
        self.dir_name = os.path.basename(self.dir_path) 
        self.is_folder = os.path.isdir(self.full_path)
        self.is_file = os.path.isfile(self.full_path) 

        # size in Bytes
        if self.is_folder:
            size = 0
            for obj in os.scandir(self.full_path):
                size+=os.path.getsize(obj)
            self.size = size
        elif self.is_file:
            self.size = os.path.getsize(self.full_path) 

        self.name_extended = os.path.basename(self.full_path)
        self.name = os.path.splitext(self.name_extended)[0]

        if len(os.path.splitext(self.name_extended)) == 2:
            self.extension = os.path.splitext(self.name_extended)[1]
        else:
            self.extension = None

    def get_size(self, size_unit: Union[SizeUnits, str] ) -> Union[int, float]:
        '''Returns the size of current path object, either as int or as a complex number type'''

        if self.size == 0:
            return 0

        if isinstance(size_unit, SizeUnits):
            pass
        elif isinstance(size_unit, str):
            try:
                size_unit = SizeUnits[size_unit.upper()]
            except:
                raise ValueError(f'Unit: "{size_unit}" is not supported.')
        else:
            raise ValueError(f'Incorrect value {size_unit} for size_unit.')
        
        unit_pow = size_unit.value
        file_size = self.size

        for pow in range(unit_pow):
            file_size = file_size / 1024

        return file_size