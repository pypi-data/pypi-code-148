
import datetime
import kraken_datatype as dt 
from kraken_schema_org import kraken_schema_org as k
from kraken_thing import json_xp as json
import sys
import uuid
from kraken_thing import normalize_value as nv


class Observation:

    def __init__(self, key=None, value=None, credibility = None, date = None):

        
        
        self.observation_id = str(uuid.uuid4())
        self.record_type = 'observation'
        self.record_id = self.observation_id

        self._key = key

        self.valid_key = False
        
        self._value = value
        self.original_value = value
        self.normalized_value = None
        self.valid_value = False     # bool if value has been validated
        self.value = value
        self.credibility = credibility
        self.date = date
        self._source_observations_id = []  # The observation_ids used to generate this observations
        self.source_observations = []      # The actual observations (when available)
        self.child_observations = []       # the observations dependant on this one
        self.instrument = None
        
        self.db_date = datetime.datetime.now()


        # metadata
        self.agent = None
        self.instrument = None
        self.object = None

        self.key = key
        self.value = value



    def __str__(self):
        '''
        '''

        o_id = str(self.observation_id)
        if len(o_id) > 9:
            o_id = o_id[:3] + '...' + o_id[-3:]
        
        key = self.key
        valid_key = str(self.valid_key)[0]

        value = str(self.value)
        valid_value = str(self.valid_value)[0]

        c = self.credibility
        d = self.date

        source_o = str(self.source_observations_id)
        if len(source_o) > 1: 
            source_o = str(len(source_o)) + ' items'
        elif len(source_o) == 1:
            source_o = source_o[0]
            if len(source_o) > 9:
                source_o = source_o[:3] + '...' + source_o[-3:]

        
        content = '{o_id} - {key}: {value} (valid: {valid_key} {valid_value} source: {source_o} c: {c} d:{d})'.format(
            o_id = o_id,
            key  =key,
            valid_key = valid_key,
            value = value,
            valid_value = valid_value,
            c = c,
            d = d,
            source_o = source_o
            
        )
        return content

        

    
    def __repr__(self):

        return json.dumps(self.dump())

    
    def __eq__(self, other):
        '''
        '''

        if self.dump() == other.dump():
            return True

        return False


    def __gt__(self, other):
        '''
        '''
        if not self.base_equal(other):
            if self.key > other.key:
                return True
            return False

        # Validity
        if self.valid_value == True and other.valid_value == False:
            return True
        if self.valid_value == False and other.valid_value == True:
            return False
            
        # Credibility
        if self.credibility and not other.credibility:
            return True
        if other.credibility and not self.credibility:
            return False
        
        if self.credibility and other.credibility and self.credibility > other.credibility:
            return True
        if self.credibility and other.credibility and self.credibility < other.credibility:
            return False

            
        # date
        if self.date and not other.date:
            return True
        if other.date and not self.date:
            return False
        
        if self.date and other.date and self.date > other.date:
            return True
        if self.date and other.date and self.date < other.date:
            return False

        # db date
        if self.db_date and not other.db_date:
            return True
        if other.db_date and not self.db_date:
            return False
        
        if self.db_date and other.db_date and self.db_date > other.db_date:
            return True
        if self.db_date and other.db_date and self.db_date < other.db_date:
            return False

        
        return False

    def __ge__(self, other):
        '''
        '''
        if self > other:
            return True

        if self.logic_equal(other):
            return True
            
        return False

    
    def __lt__(self, other):
        '''
        '''
        if other > self:
            return True
        return False

    def __le__(self, other):
        '''
        '''
        
        if other > self:
            return True

        if self.logic_equal(other):
            return True
            
        return False

    
    def base_equal(self, other):
        '''Equality for only basic fields
        '''
        #if not self.record_type == other.record_type:
        #    return None
        #if not self.record_id == other.record_id:
        #    return False
        if not self.key == other.key:
            return False
        return True

    def logic_equal(self, other):
        '''Equality on all but value 
        '''
        if not self.base_equal(other):
            return False

        if not self.credibility == other.credibility:
            return False
        if not self.date == other.date:
            return False

        return True


    @property
    def metadata(self):
        '''Return metadata of observation
        '''

        record = {}
        for k in self.keys():
            record[k] = getattr(self, k)

        return record

    
    @metadata.setter
    def metadata(self, value):
        '''Sets metadata
        '''

        if not value:
            return

        if not isinstance(value, dict):
            return
            
        for k, v in value.keys():
            setattr(self, k, v)

        return
        
    
    def keys(self):
        '''
        '''
        return [ 'key', 'valid_key', 'value', 'valid_value', 'source_observation', 'instrument', 'credibility', 'date']

    def metadata_keys(self):
        '''
        '''
        return ['source_observation', 'instrument', 'credibility', 'date']

        
    def load(self, record):
        '''
        '''

        for i in self.keys():
            setattr(self, i, record.get(i, None))

    
    def dump(self):
        '''
        '''
        record = {}
        for i in self.keys():
            value = getattr(self, i, None)
            record[i] = value

        return record


    '''properties
    '''

    @property
    def key(self):
        '''
        '''
        return self._key
        

    @key.setter
    def key(self, value):
        '''
        '''

        self._key = value        
        #self.valid_key = False
        #if value == '@type' or value == '@id' or value == k.normalize_key(value):
        #    self.valid_key = True

    
    @property 
    def value(self):
        '''
        '''
        return self._value


    @value.setter
    def value(self, value):
        '''
        '''

        self._value = value
        
        # Validate value
        #self.valid_value = False
        
        
        # Get datatypes
        #if value == nv.normalize_value(self.record_type, self.key, value):
        #    self.valid_value = True


    @property
    def source_observations_id(self):
        '''
        '''
        return self._source_observations_id

    @source_observations_id.setter
    def source_observations_id(self, values):
        '''
        '''
        if not isinstance(values, list):
            values = [values]

        for value in values:
            if value not in self._source_observations_id:
                self._source_observations_id.append(value)



    
    '''Methods
    '''

    def get_copy(self):
        '''Return a copy if itself
        '''
        o = Observation()
        o.load(self.dump())
        return o

    '''System properties
    '''
    @property
    def memory_size(self):
        '''Returns memory size taken by object
        '''
        size = 0
        size += sys.getsizeof(self) / 1024
        
        return round(size, 2)
