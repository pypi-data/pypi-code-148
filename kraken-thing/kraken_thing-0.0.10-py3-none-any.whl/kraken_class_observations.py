from kraken_thing.class_small_db import Small_db 

from kraken_thing.kraken_class_observation import Observation



class Observations:

    def __init__(self):

        self.db = Small_db()
        self.param1 = 'obs'


    def get(self, observation_id = None):
        '''
        '''

        return self.db.get(self.param1, observation_id)

    def set(self, observation):
        '''
        '''

        self.db.set(self.param1, observation.observation_id, observation)
        
        
