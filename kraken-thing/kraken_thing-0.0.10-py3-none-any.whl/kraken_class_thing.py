import datetime
from kraken_thing import json_xp as json
from kraken_thing.kraken_class_observation import Observation
import uuid
from urllib.parse import urlparse
from kraken_schema_org import kraken_schema_org as k
from kraken_thing import normalize_id
import sys
import kraken_datatype as dt 
from kraken_schema_org import kraken_schema_org as k
from kraken_thing import normalize_value as nv


class Thing:

    def __init__(self, record_type = None, record_id = None):
        """
        A class to represent a schema.org Thing
        """
        
        self.db = []
        self.things = None     # Reference to things collection

        # Load record if record instead of record_type
        if record_type and isinstance(record_type, dict):
            self.load(record_type)
        else:
            self.record_type = record_type
            self.record_id = record_id

            
        # Add id if none
        if record_type and not record_id:
            self.record_id = str(uuid.uuid4())

    
    def __str__(self):
        
       
        return str(self.summary)

    def __repr__(self):
        return str(self.dump())


    def __eq__(self, other):
        """
        """

        if not isinstance(other, Thing):
            return False
        
        if self.record_id and self.record_id == other.record_id and self.record_type and self.record_type == other.record_type:
            return True
        else:
            return False

    def __add__(self, other):
        """
        """
        
        new_t = Thing()

        #Load self record
        new_t.set_observations(self.get_observations())

        # Load other record
        new_t.set_observations(other.get_observations())

        return new_t

    def merge(self, other):
        '''Add obs from other in self
        '''
                
        # Copy observations
        observations = other.get_observations()
        self.set_observations(observations)
            
        return


    @property
    def summary(self):
        '''
        '''
        content = []
        content.append('@type: ' + str(self.record_type) )
        content.append('@id: ' + str(self.record_id) )
        content.append(40 * '-' )

        for i in self.get_observations():
            content.append(str(i.key) + ': ' + ((20 - len(i.key)) * ' ' )+ str(i.value) )
        return '\n'.join(content)


    @property
    def summary_sources(self):
        '''Starting with no sources, shows hierarchy
        '''
        content = []
        base_obs = []
        for i in self.get_observations():
            if not i.source_observations_id:
                base_obs.append(i)


        def recurse_relations_sources(obs, level=0):
            content = []
            for i in obs:
                hierarchy = str((level * 4 * ' ')) + str((20 - level * 4) * '-') + '  '
                content.append(hierarchy + str(i))
                content += recurse_relations_sources(i.child_observations, level + 1)
                
            return content
        
        content = recurse_relations_sources(base_obs)
        
        return '\n'.join(content)

    @property
    def summary_childs(self):
        '''For each, shows where it comes from
        '''
        content = []
        obs = self.get_observations()

        def recurse_relations_childs(obs, level=0):
            content = []
            for i in obs:
                hierarchy = str((level * 4 * ' ')) + str((20 - level * 4) * '-') + '  '
                content.append(hierarchy + str(i))
                content += recurse_relations_childs(i.source_observations, level + 1)
                
            return content
        content = recurse_relations_childs(obs)
        
        return '\n'.join(content)
            
            
    
    """ Main
    """
    
    def set(self, key, value, metadata = None):
        """Create a new observation with key value. 
        """

        # Error handling
        if not value:
            return 

        
        # Handle lists (in reverse so it conserves proper order)
        if isinstance(value, list) and not isinstance(value, str):
            for i in reversed(value):
                self.set(key, i, metadata)
            return


        # Initialize 
        observations = []
        
        # Get original observation (as is key value)
        o = self.new_observation(key, value, metadata)
        if o:
            observations.append(o)

        # Normalize observation key value
        o = self.normalize_observation(observations[-1])
        if o:
            observations.append(o)
        
        # normalize record_id
        o = self.normalize_record_id_from_observation(observations[-1])
        if o:
            observations.append(o)
        
        # Add obs to db
        self.set_observations(observations)
        

    def get(self, key, include_non_valid = True):
        """
        Retrieve all values for given key from best to worst

        
        Parameters
        ----------
        key: str
            Key of the value to get
        invclude_non_valid: includes obs where key or value are not validated
        """
        if not key.startswith('@') and not key.startswith('schema:'):
            key = 'schema:' + key

        obs = []
        for i in self.db:
            if i.key == key:
                obs.append(i)

        if not obs or len(obs) == 0:
            return []

        # Sort observations
        values = []
        for i in sorted(obs, reverse=True):
            if include_non_valid or (i.valid_key and i.valid_value):
                values.append(i.value)
            
            
        return values

    def get_best(self, key):
        '''Returns best value
        '''
        
        value = self.get(key, False)

        if not value:
            value = self.get(key, True)

        if value and len(value) > 0:
            return value[0]
        else:
            return None


        
    def load(self, record, append=False):
        """
        Load complete record
        
        Parameters
        ----------
        record: dict
            Dict of the record to load. Also accepts json.
        append: bool
            If true, will append value to existing value
        """

        # Handle json
        if isinstance(record, str):
            record = json.loads(record)
                
        # Add id if none
        for key, value in record.items():
            self.set(key, value)
            
        return
     
        

    def dump(self):
        """Dump complete record without class
        """

        # Add id if none
        if self.record_type and not self.record_id:
            self.record_id = str(uuid.uuid4())
        
        record = {}

        # Convert Things to dict
        for k in self.keys:

            if not record.get(k, None):
                record[k] = []

            values = self.get(k)
            
            if not isinstance(values, list):
                values = [values]

            for v in values:
                if isinstance(v, Thing):
                    v = v.dump()

                if v not in record[k]:
                    record[k].append(v)
            
        
        # Fix @type and @id
        record['@type'] = self.record_type
        record['@id'] = self.record_id
        
        # Remove lists and empty values
        new_record = {}
        for k, v in record.items():
            if v and len(v) == 1:
                new_record[k] = v[0]
            elif v and len(v) > 1:
                new_record[k] = v
        
        return new_record

    @property
    def json(self):
        """
        """
        return json.dumps(self.dump())
        
    @json.setter
    def json(self, value):
        """
        """
        record = json.loads(value)
        self.load(record)
        

    """Observations
    """

    def set_observations(self, observation):
        '''
        '''
        if isinstance(observation, list):
            for i in observation:
                self.set_observations(i)
            return
            
        if observation not in self.db:
            self.db.append(observation)
        
        # Add parents and childs
        for i in observation.source_observations_id:
            source_obs = self.get_observation(i)

            if source_obs not in observation.source_observations:
                observation.source_observations.append(source_obs)
            
            if observation not in source_obs.child_observations:
                source_obs.child_observations.append(observation)

    
    def get_observation(self, observation_id):
        '''Return an observation by id
        '''
        for i in self.db:
            if i.observation_id == observation_id:
                return i
        return None
    
    def get_observations(self, key = None):
        '''Returns all observations sorted best to worst by group key
        '''

        obs = []

        # Get obs by key
        for key1 in self.keys:
            key_obs = []
            for i in self.db:
                if key and i.key == key and i.key == key1:
                    key_obs.append(i)
                elif not key and i.key == key1:
                    key_obs.append(i)

            key_obs = sorted(key_obs, reverse=True)
            obs += key_obs
        
        return obs

    def get_best_observation(self, key = None):
        '''
        '''
        obs = self.get_best_observations(key)

        if len(obs) > 0:
            return obs[0]
        else:
            return None
        
    
    def load_observations(self, observations):
        '''Load observations in list of dict format
        '''
        if not isinstance(observations, list):
            observations = [observations]

        for i in observations:
            o = Observation(self.record_type, self.record_id)
            o.load(i)
            self.set_observations(o)
            
        return

    def dump_observations(self):
        '''Returns list of obs in dict format
        '''
        obs = []
        for i in self.db:
            obs.append(i.dump())

        return obs

    def new_observation(self, key, value, metadata = None):
        '''
        '''
        # Convert to thing if record
        if isinstance(value, dict) and '@type' in value.keys():
            new_v = Thing()
            new_v.load(value)
            value = new_v
            
        # Record original value
        observation = Observation(key, value)

        # Load metadata
        observation.metadata = metadata

        return observation

    
    def normalize_observation(self, observation):
        '''Normalize key and value. If both different, create new observation
        '''

        # Get normalized key value
        normalized_record_type = k.normalize_type(self.record_type)
        normalized_key = k.normalize_key(observation.key) if not observation.key.startswith('@') else observation.key
        normalized_value = nv.normalize_value(normalized_record_type, observation.key, observation.value)   


        # Update input observation if key or value already normalized
        if normalized_key == observation.key:
            observation.valid_key = True
        if normalized_value == observation.value:
            observation.valid_value = True

        # Address if value is thing
        if isinstance(observation.value, Thing):
            observation.valid_value = True

        # Skip if already normalized
        if observation.valid_key and observation.valid_value:
            return None

        # Create new observation
        normalized_observation = observation.get_copy()
        normalized_observation.source_observations_id = observation.observation_id
        normalized_observation.instrument = 'normalize key and value'

        # Assign normalized key
        if normalized_key:
            normalized_observation.key = normalized_key
            normalized_observation.valid_key = True

        # Assign normalized value
        if normalized_value:
            normalized_observation.value = normalized_value
            normalized_observation.valid_value = True

        return normalized_observation

    def normalize_record_id_from_observation(self, observation):
        '''Records nromalized record_id if exist
        '''

        # Add observation with record_id (if new info makes it available)
        record = {
            '@type': self.record_type, 
            observation.key: observation.value
        }
        normalized_record_id = normalize_id.normalize_id(record)

        if normalized_record_id:
            normalized_observation = observation.get_copy()
            
            normalized_observation.source_observations_id = observation.observation_id            
            normalized_observation.instrument = 'normalize record_id'

            normalized_observation.key = '@id'
            normalized_observation.valid_key = True

            normalized_observation.value = normalized_record_id
            normalized_observation.valid_value = True
            
            return normalized_observation

        return None


    
    """Properties
    """
    @property
    def record_type(self):
        '''
        '''
        record_type = self.get_best('@type')
        return record_type

    @record_type.setter
    def record_type(self, value):
        '''
        '''
        
        self.set('@type', value)

        

    @property
    def record_id(self):
        '''
        '''

        record_id = self.get_best('@id')
        return record_id
        

    @record_id.setter
    def record_id(self, value):
        '''
        '''
    
        if isinstance(value, list) and len(value) == 0:
            return
        if isinstance(value, list) and len(value) == 1:
            value=value[0]
        if value is not None and not isinstance(value, str):
            return

        self.set('@id', value)
            

    @property
    def record_ids(self):
        '''Return list of current and original record_ids
        '''
        record_ids = []
        record_ids.append(self.record_id)
        for i in self._original_record_ids:
            if i not in record_ids:
                record_ids.append(i)
        return record_ids
    


    @property
    def record_ref(self):
        record = {
            '@type': self.record_type,
            '@id': self.record_id
        }
        return record

    @record_ref.setter
    def record_ref(self, value):
        self.load(value)

    @property
    def keys(self, valid = False):
        '''
        '''

        # Get keys
        keys = []
        for i in self.db:
            if i.key not in keys:
                if valid and not i.valid_key:
                    continue
                else: 
                    keys.append(i.key)
                    
        keys = sorted(keys)
        return keys
        
    
    @property
    def name(self):
        return self.get_best('schema:name')

    @name.setter
    def name(self, value):
        self.set('schema:name', value)

    @property
    def url(self):
        return self.get_best('schema:url')

    @url.setter
    def url(self, value):
        self.set('schema:url', value)

    @property
    def url_domain(self):
        '''
        '''
        data = self.get_best('schema:url')
        domain = None
        
        if data:
            domain = urlparse(data).netloc
            domain = domain.replace('www.', '')
        
        return domain


    
    '''Methods
    '''
    def update_record_ref(self, old_record_type, old_record_id, new_record_type, new_record_id):
        '''Updates all value with new record_ref
        '''
        for i in self.get_observations():
            if isinstance(i.value, Thing):
                if i.original_value.record_type == old_record_type and i.original_value.record_id == old_record_id:
                    i.original_value.record_type = new_record_type
                    i.original_value.record_id = new_record_id
            
        


    
    """Conditions
    """

    @property
    def is_status_active(self):
        """
        """
        if self.get_best('schema:actionStatus') == 'schema:ActiveActionStatus':
            return True
        return False

    @property
    def is_status_completed(self):
        """
        """
        if self.get_best('schema:actionStatus') == 'schema:CompletedActionStatus':
            return True
        return False

    @property
    def is_status_failed(self):
        """
        """
        if self.get_best('schema:actionStatus') == 'schema:FailedActionStatus':
            return True
        return False

    @property
    def is_status_potential(self):
        """
        """
        if self.get_best('schema:actionStatus') == 'schema:PotentialActionStatus':
            return True
        return False

    
    """Actions
    """
    def set_status_active(self):
        """
        """
        self.set('schema:actionStatus', 'schema:ActiveActionStatus')
    
    def set_status_completed(self):
        """
        """
        self.set('schema:actionStatus', 'schema:CompletedActionStatus')
    
    def set_status_failed(self):
        """
        """
        self.set('schema:actionStatus', 'schema:FailedActionStatus')
    
    def set_status_potential(self):
        """
        """
        self.set('schema:actionStatus', 'schema:PotentialActionStatus')


    '''System properties
    '''
    @property
    def memory_size(self):
        '''Returns memory size taken by object
        '''
        size = 0
        size += sys.getsizeof(self) / 1024

        for i in self.db:
            size += i.memory_size
        
        return round(size, 2)