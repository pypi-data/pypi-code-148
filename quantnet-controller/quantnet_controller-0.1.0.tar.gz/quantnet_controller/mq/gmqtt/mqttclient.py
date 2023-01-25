import asyncio
import logging
import uuid
import json
import uvloop
from gmqtt import Client
from ..mqttclientinterface import MQTTClientInterface

class MQTTClient(MQTTClientInterface, Client):
    def __init__(self, client_id, clean_session=True, optimistic_acknowledgement=True,
                 will_message=None, **kwargs):
        super(MQTTClient, self).__init__(client_id, clean_session, optimistic_acknowledgement, will_message, **kwargs)
        
        self.handler = None
        
    def set_handler(self, handler):
        self._handler = handler
        
    def topic_match(self, sub, topic):
        """ check if topic start with sub """
        return True if sub in topic else False
    
    def topic_tokenise(self, topic):
        """ TODO: break the topic into token array """
        return topic.split('/')
    
    def set_will(self, topic, msg, qos, ratain):
        """ TODO: set the will message """
        pass
    
    def set_tls_psk(self, id, psk):
        """ TODO: set the psk """
        pass
    
    def set_ca(self, capath):
        """ TODO setup the ca """
        pass