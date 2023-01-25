import json
import jsonschema
import simunetcore.utils as utils

class Serializer(object):
    """
    Serializer base class. It manages the serialization of the 
    model instances. `simunet.model` is derived from this class.
    
    """
    
    def __init__(self):
        """
        Creates a new Serialize object.

        """

        pass
    
    def validate(self, schema):
        """
        Validates the current instance against the given schema.

        Parameters
        ----------
        schema : str or dict
            The schema to validate against.

        Raises
        ------
        `SchemaError` if schema is not valid.
        `ValidationError` if instance does not match the schema.

        See Also
        --------
        jsonschema : simunet uses jsonschema to validate json structures.

        """

        # Try to validate the json against the schema
        schema_data = schema if type(schema) == dict else json.loads(schema)
        jsonschema.validate(self.__dump_data(), schema=schema_data)

    def __load_data(self, data, incremental=True):
        """
        Loads data into this instance.

        Parameters
        ----------
        incremental : bool, optional
            Sets wether the whole `__dict__` should be overwritten 
            with `data` or not. Incremental serialization preserves
            attributes that are not present in `data`. Default = True.

        """
        
        if incremental:
            for key in data:
                self.__dict__[key] = data[key]
        else:
            self.__dict__ = data

        
    def __dump_data(self):
        """
        Retuns a dictionary containing the data of this instance.

        Returns
        -------
        data : dict {str : Any}
            The dictionary containing the data of this instance.

        """
       
        return self.__dict__
        
    @classmethod
    def from_string(cls, json_string, decompress=False, **kwargs): 
        """
        Creates an instance from the given json string.

        Parameters
        ----------
        json_string : str
            The json data to deserialize.
        decompress : bool, optional
            Sets wether to decompress the content before deserialization.
            Default = False.
        Returns
        -------
        object : cls
            An object of type `cls` contaiing the data.

        """ 

        obj = cls(**kwargs) 
        obj.loads(json_string, decompress)
        return obj
    
    @classmethod
    def from_file(cls, json_file, decompress=False, **kwargs): 
        """
        Creates an instance from the given file (containg json data).

        Parameters
        ----------
        json_file : str
            The full qualified path name to the file containing the 
            the json data to deserialize.
        decompress : bool, optional
            Sets wether to decompress the content before deserialization.
            Default = False.

        Returns
        -------
        object : cls
            An object of type `cls` contaiing the data.

        """ 
        
        obj = cls(**kwargs) 
        obj.load(json_file, decompress)
        return obj
    
    @classmethod
    def from_data(cls, json_data, **kwargs):
        """
        Creates an instance from the given json data.

        Parameters
        ----------
        json_data : dict (str : Any)
            The json data to deserialize.

        Returns
        -------
        object : cls
            An object of type `cls` contaiing the data.

        """ 
        
        obj = cls(**kwargs) 
        obj.__load_data(json_data)
        return obj
            
    def load(self, json_file, decompress=False):
        """
        Loads the data from the given json file into this instance.

        Parameters
        ----------
        json_file : str
            The full qualified path name to the file containing the 
            the json data to deserialize.
        decompress : bool, optional
            Sets wether to decompress the content before deserialization.
            Default = False.

        """
        
        with open(json_file, "r") as f:
            json_string = f.read()
            self.loads(json_string, decompress)

    def loads(self, json_string, decompress=False):
        """
        Loads the data from from the given json string into this instance.

        Parameters
        ----------
        json_string : str
            The json data to deserialize.
        decompress : bool, optional
            Sets wether to decompress the content before deserialization.
            Default = False.

        """ 
       
        if decompress:
            json_string = utils.decompress(json_string)
        data = json.loads(json_string)
        self.__load_data(data)

    def dump(self, json_file, indent=False, compress=False):
        """
        Dumps the data of this instance in json format into the given file.

        Parameters
        ----------
        json_file : str
            The full qualified path name to the file to serialize into.
        indent : bool, optional
            Sets wether to indent the json (for a better readability)
        compress : bool, optional
            Sets wether to compress the content after serialization.

        """ 
        
        with open(json_file, "w+") as f:
            json_string = self.dumps(indent, compress)
            f.write(json_string)
        
    def dumps(self, indent=None, compress=False):
        """
        Return the dump of the data of this instance in json format 
        as a string.

        Parameters
        ----------
        indent : bool, optional
            Sets wether to indent the json (for a better readability)
        compress : bool, optional
            Sets wether to compress the content after serialization.

        Returns
        -------
        json_string : str
            A string containing the json 
            (compressed and encode if `compress` is set to True).

        """
        
        json_string = json.dumps(self.__dump_data(), indent=indent)
        if compress:
            json_string = utils.compress(json_string)
        return json_string

