import os

"""ParserBase defines some methods of the YAMLParser class."""

class ParserBase():
    
    def __init__(self, filepath = 'src/yamls/config.yaml'):
        self.filepath = filepath
    
    """_try_get is a method that takes a dictionary variable and a string field as arguments and tries to return the dictionary value corresponding to the key field"""
    def _try_get(self, variable: dict, field, error_msg=None):
        try:
            return variable[field]
        except KeyError:
            if not error_msg:
                error_msg = f'the field `{field}` is required.'
            file_name = self.filepath.split('/')[-1]
            error_msg = f'Error in file {file_name}: {error_msg}'
            raise ValueError(error_msg)
        
    """ _get is a method that receives as arguments a dictionary variable and a string field and tries to return the value of the dictionary corresponding to the key field."""
        
    def _get(self, variable: dict, field, default_value):
        try:
            return variable[field]
        except:
            return default_value