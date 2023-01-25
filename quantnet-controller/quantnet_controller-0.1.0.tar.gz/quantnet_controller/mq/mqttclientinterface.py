from abc import ABC, abstractmethod

class MQTTClientInterface(ABC):

    # @abstractmethod
    # def publish(self, topic, msg, qos, retain):
    #     pass
    #
    # @abstractmethod
    # def subscribe(self, topic, qos):
    #     pass
        
    @abstractmethod    
    def topic_match(self, sub, topic):
        """ TODO: check if topic start with sub """
        raise NotImplementedError
    
    @abstractmethod
    def topic_tokenise(self, topic):
        """ TODO: break the topic into token array """
        raise NotImplementedError