import inspect
import types
from simunetcore import Model
from simunetcore import MQTTModel
from simunetcore import AWSModel
from simunetcore import RESTModel
from simunetcore import logger
        
class Factory(dict):
    """The simunet factory class."""

    def __init__(self):
        """
        Creates a new factory object and 
        registers the core simunet models 
        (AWSModel, MQTTModel and RESTModel).
 
        """
        super().__init__()
       
        self["AWSModel"] = AWSModel
        self["MQTTModel"] = MQTTModel
        self["RESTModel"] = RESTModel

    def register(self, code, namespace = "simunetcore.factory"):
        """
        Rergisters a peice of code as a model in the factory 
        under the the given namespace.

        Parameters
        ----------
        code : str
            The source code of the model class. 
        namespace : str, optional
            The namespace used for the model.
            It is registered as <namespace>.<class_name>
            For example Registering a class `TestModel` 
            in the namespace `my.models`  leads to the 
            dict entry: {'Test': <class 'my.models.TestModel'>}.
            Default = 'simunetcore.factory'.

        """            
                    # create a factory module
        factory_module = types.ModuleType(namespace)
        factory_module.__loader__ = self

        exec(code, factory_module.__dict__)
        members_list = inspect.getmembers(factory_module, inspect.isclass)
        for item in members_list:
            if issubclass(item[1], Model) and item[1] is not Model:
                self[item[0]] = item[1]
                logger.info("Registered {}: {}".format(item[0], item[1]))
