from typing import  Optional, Tuple
from opcua.client.client import Client
from pydantic import AnyUrl, BaseModel, Field
from pydantic.class_validators import validator
from pydevmgr_core  import BaseObject, BaseNode
from .config import uaconfig
from dataclasses import dataclass
import opcua



def kjoin(*names) -> str:        
    return ".".join(a for a in names if a)

def ksplit(key: str) -> Tuple[str,str]:
    """ ksplit(key) ->  prefix, name
    
    >>> ksplit('a.b.c')
    ('a.b', 'c')
    """
    s, _, p = key[::-1].partition(".")
    return p[::-1], s[::-1]

def ua_engine(**kwargs):
    """ Create a new Ua Engine to be used by any pydevmgr's com= argument """
    return UaEngine.new( None, UaEngine.Config.parse_obj(kwargs))


class UaEngineConfig(BaseObject.Engine.Config):
    namespace: int = Field(default_factory=lambda : uaconfig.namespace)
    address: AnyUrl = Field(default_factory=lambda : uaconfig.default_address) 
    prefix: str = ""
    
    @validator('address', pre=True)
    def _map_address(cls, address):
        return uaconfig.host_mapping.get(str(address), address)
    
class UaNodeEngineConfig(BaseNode.Engine.Config):
    suffix: str = ""


def _parse_com_node_to_engine(com):
    if com is None:
        com = UaEngine.new(None,None)
    elif isinstance(com, opcua.Client):
        com = UaEngine(client=com)
    elif isinstance(com, dict):
        com = UaEngine.new(None, UaEngineConfig(**com))
    elif isinstance(com, str):
        com = UaEngine.new(None, UaEngineConfig(address=com))
    return com 

@dataclass
class UaNodeEngine(BaseNode.Engine):
    # --------------------------------------     
    client: Optional[opcua.Client] = None
    node_client: Optional[opcua.Node] = None
    node_id: str = ""
    node_name: str = "" 
    # -------------------------------------- 

    
    Config = UaNodeEngineConfig
    _ua_variant_type = None # cash the type for next value parsing  
    

    @classmethod
    def new(cls, com= None, config=None, *, node_suffix=None):
        if com is None:
            # engine = super().new()
            return cls()
        
        parent_engine = _parse_com_node_to_engine(com) 
        if config is None:
            config = cls.Config()
        
        engine = super().new(parent_engine, config)
        if node_suffix is None:
            node_suffix = config.suffix
        
        node_name = kjoin(parent_engine.prefix, node_suffix)
        
        engine.node_id = "ns={};s={}".format(parent_engine.namespace, node_name)
        engine.client = parent_engine.client
        engine.node_client = engine.client.get_node(engine.node_id) 
        engine.node_name = node_name
                    
        return engine 
    

@dataclass
class UaRpcEngine(UaNodeEngine):
    method_id: str = ""
    
    @classmethod
    def new(cls, com, config=None):
        if config is None:
            config = UaNodeEngineConfig()
        
        # method name is the last member on config.suffix 
        node_suffix, method_name = ksplit(config.suffix)
        engine = super().new(com, config, node_suffix = node_suffix)
        engine.method_id = "{}:{}".format(com.namespace, method_name)
        
        return engine  



@dataclass
class UaEngine(BaseObject.Engine):
    Config = UaEngineConfig
    
    client: Optional[opcua.Client] = None
    namespace: int = 4
    prefix: str = ""
    
    @classmethod
    def new(cls, com=None, config=None):

        if config is None:
            config = cls.Config()
        
        
                 
         
        if com is None:
            engine = super().new(None, config) 

            client, namespace, prefix = (
                opcua.Client( str(config.address) ), 
                config.namespace, 
                config.prefix
            )
            
        elif (isinstance(com, BaseObject.Engine) and not isinstance(com, UaEngine)):
            engine = super().new(com, config) 

            client, namespace, prefix = (
                opcua.Client( str(config.address) ), 
                config.namespace, 
                config.prefix
            )

        elif isinstance(com, str):
            engine = super().new(None, config) 

            client, namespace, prefix = (
                opcua.Client( com ), 
                config.namespace, 
                config.prefix
            )
        elif isinstance(com,Client):
            engine = super().new(None, config)
            client, namespace, prefix = (
                com, 
                config.namespace, 
                config.prefix
            )

        else:
            engine = super().new(com, config)

            client, namespace, prefix = (
                com.client,
                com.namespace,
                kjoin(com.prefix, config.prefix) 
            )
        
        engine.client = client 
        engine.namespace = namespace
        engine.prefix = prefix

        return engine 



    
