import abc
from uuid import  uuid4
import yaml

class PlugInConfiguration(yaml.YAMLObject):
    """ """

    yaml_tag = "!dabapush:PluginConfiguration"

    def __init__(self, name: str, id: str or None) -> None:
        super().__init__()

        self.name = name
        self.id = id if id is not None else str(uuid4())

    @classmethod
    @abc.abstractclassmethod
    def get_instance(self) -> object or None:
        """Get a configured instance of the appropriate reader or writer plugin.
        
        """
     